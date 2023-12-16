# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from mimetypes import guess_type

from sqlalchemy.exc import IntegrityError

import kadi.lib.constants as const
from .files import get_custom_mimetype
from .models import Chunk
from .models import ChunkState
from .models import File
from .models import FileState
from .models import UploadState
from kadi.ext.db import db
from kadi.lib.db import acquire_lock
from kadi.lib.db import update_object
from kadi.lib.plugins.utils import signal_resource_change
from kadi.lib.revisions.core import create_revision
from kadi.lib.storage.local import create_chunk_storage


def delete_upload(upload):
    """Delete an existing upload.

    This will mark the upload for deletion, i.e. only the upload's state will be
    changed.

    :param upload: The upload to delete.
    """
    upload.state = UploadState.INACTIVE


def remove_upload(upload):
    """Remove an upload from storage and from the database.

    Note that this function issues one or more database commits.

    :param upload: The upload to remove.
    """
    chunk_storage = create_chunk_storage()
    upload_storage = upload.storage

    delete_upload(upload)
    db.session.commit()

    # Remove any chunks related to the upload as well.
    for chunk in upload.chunks:
        filepath = chunk_storage.create_filepath(f"{upload.id}-{chunk.index}")
        chunk_storage.delete(filepath)

        db.session.delete(chunk)

    filepath = upload_storage.create_filepath(str(upload.id))
    upload_storage.delete(filepath)

    db.session.delete(upload)
    db.session.commit()


def save_chunk_data(upload, index, size, file_object, checksum=None):
    """Save the chunk data of an upload.

    Each chunk uses the UUID of the given upload (see :attr:`.Upload.id`) combined with
    its index as base identifier in the form of ``"<uuid>-<index>"`` for file path
    generation.

    Note that this function issues one or more database commits.

    :param upload: The upload.
    :param index: The index of the chunk.
    :param size: The size of the chunk in bytes.
    :param file_object: A file-like object representing the actual uploaded file.
    :param checksum: (optional) The MD5 checksum of the chunk. If given it will be used
        to verify the checksum after saving the chunk.
    :raises KadiFilesizeExceededError: If the chunk exceeds the maximum size of its
        storage.
    :raises KadiFilesizeMismatchError: If the actual size of the chunk does not match
        the provided size.
    :raises KadiChecksumMismatchError: If the actual checksum of the chunk does not
        match the provided checksum.
    """
    chunk = Chunk.update_or_create(upload=upload, index=index, size=size)
    db.session.commit()

    chunk_storage = create_chunk_storage()

    try:
        filepath = chunk_storage.create_filepath(f"{upload.id}-{index}")

        chunk_storage.save(filepath, file_object)
        chunk_storage.validate_size(filepath, size)

        if checksum:
            chunk_storage.validate_checksum(filepath, checksum)

        chunk.state = ChunkState.ACTIVE

    except:
        chunk.state = ChunkState.INACTIVE
        raise

    finally:
        # Always update the upload's timestamp manually, since the timestamp is used for
        # checking the upload's expiration.
        upload.update_timestamp()
        db.session.commit()


def merge_chunk_data(upload, task=None):
    """Merge the chunk data of an upload.

    Uses :func:`complete_file_upload` to complete the file upload process.

    :param upload: The upload.
    :param task: (optional) A :class:`.Task` object that can be provided if this
        function is executed in a task. In that case, the progress of the given task
        will be updated.
    :return: See :func:`complete_file_upload`.
    """
    chunk_storage = create_chunk_storage()
    upload_storage = upload.storage

    try:
        upload_path = upload_storage.create_filepath(str(upload.id))
        upload_storage.ensure_filepath_exists(upload_path)

        upload_file = upload_storage.open(upload_path, mode="wb")

        # Merge the uploaded chunks.
        for chunk in upload.active_chunks.order_by(Chunk.index.asc()):
            chunk_path = chunk_storage.create_filepath(f"{upload.id}-{chunk.index}")
            chunk_file = chunk_storage.open(chunk_path)

            upload_file.write(chunk_file.read())

            chunk_storage.close(chunk_file)

            if task is not None:
                task.update_progress((chunk.index + 1) / upload.chunk_count * 100)
                db.session.commit()

        upload_storage.close(upload_file)

    except:
        db.session.rollback()
        delete_upload(upload)
        db.session.commit()

        raise

    return complete_file_upload(upload)


def save_upload_data(upload, file_object):
    """Save the directly uploaded data of an upload.

    :param upload: The upload.
    :param file_object: A file-like object representing the actual uploaded file.
    :return: See :func:`complete_file_upload`.
    """
    storage = upload.storage

    try:
        filepath = storage.create_filepath(str(upload.id))
        storage.save(filepath, file_object)

    except:
        db.session.rollback()
        delete_upload(upload)
        db.session.commit()

        raise

    return complete_file_upload(upload)


def complete_file_upload(upload):
    """Performs necessary steps to complete a file upload.

    Validates the upload in regards to its stored data and creates or updates the
    corresponding file.

    Note that this function issues one or more database commits or rollbacks.

    :param upload: The upload to complete.
    :return: The newly created or updated file or ``None`` if it could not be created
        due to a file name conflict or updated due to a replaced file already being
        deleted.
    :raises KadiFilesizeExceededError: If the upload exceeds the maximum size of its
        storage.
    :raises KadiFilesizeMismatchError: If the actual size of the upload does not match
        the provided size.
    :raises KadiChecksumMismatchError: If the actual checksum of the upload does not
        match the provided checksum.
    """
    storage = upload.storage

    try:
        upload_path = storage.create_filepath(str(upload.id))
        storage.validate_size(upload_path, upload.size)

        calculated_checksum = upload.calculated_checksum

        if calculated_checksum is None:
            calculated_checksum = storage.get_checksum(upload_path)

        if upload.checksum is not None:
            storage.validate_checksum(
                upload_path, upload.checksum, actual=calculated_checksum
            )

        new_file_created = False

        # Check whether the upload replaces an existing file.
        if upload.file is None:
            try:
                file = File.create(
                    creator=upload.creator,
                    record=upload.record,
                    storage=upload.storage,
                    name=upload.name,
                    description=upload.description,
                    size=upload.size,
                    checksum=calculated_checksum,
                )

                # Commit here already, so the file can be referenced and deleted later
                # if something went wrong.
                db.session.commit()

            except IntegrityError:
                db.session.rollback()
                return None

            new_file_created = True
        else:
            # Lock the file to make sure replacing the metadata and actual file data
            # happens in a single transaction.
            file = acquire_lock(upload.file)

            # Check if the file still exists and is active.
            if file is None or file.state != FileState.ACTIVE:
                # Release the file lock.
                db.session.commit()
                return None

            update_object(
                file,
                description=upload.description,
                size=upload.size,
                checksum=calculated_checksum,
            )

        # Move the completed upload to the correct location.
        filepath = storage.create_filepath(str(file.id))
        storage.move(upload_path, filepath)

        # Determine the magic MIME type, and possibly a custom MIME type, based on the
        # file's content.
        base_mimetype = storage.get_mimetype(filepath)
        custom_mimetype = get_custom_mimetype(file, base_mimetype=base_mimetype)
        magic_mimetype = base_mimetype if custom_mimetype is None else custom_mimetype

        # Determine the regular MIME type. If no MIME type was given explicitly for the
        # upload, or it is equal to the default MIME type, the custom MIME type is
        # taken, if applicable. Otherwise, try to guess the regular MIME type from the
        # filename and fall back to the magic MIME type.
        mimetype = upload.mimetype

        if mimetype == const.MIMETYPE_BINARY:
            if custom_mimetype is not None:
                mimetype = custom_mimetype
            else:
                mimetype = guess_type(file.name)[0] or magic_mimetype

        update_object(
            file,
            mimetype=mimetype,
            magic_mimetype=magic_mimetype,
            state=FileState.ACTIVE,
        )
        delete_upload(upload)

        if db.session.is_modified(file):
            file.record.update_timestamp()

        # Note that the creator of the upload will be used for the revision. For
        # existing files, the original creator of the file will stay the same.
        revision_created = create_revision(file, user=upload.creator)

        # Releases the file lock as well.
        db.session.commit()

        if revision_created:
            signal_resource_change(file, user=upload.creator, created=new_file_created)

        return file

    except:
        db.session.rollback()

        # If something went wrong when replacing a file, check whether the old file is
        # still intact and delete it if not.
        if upload.file is not None:
            try:
                filepath = storage.create_filepath(str(upload.file.id))
                storage.validate_checksum(filepath, upload.file.checksum)
            except:
                from .files import delete_file

                delete_file(upload.file, user=upload.creator)

        delete_upload(upload)
        db.session.commit()

        raise
