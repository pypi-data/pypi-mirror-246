# Copyright 2021 - 2023 Universität Tübingen, DKFZ, EMBL, and Universität zu Köln
# for the German Human Genome-Phenome Archive (GHGA)
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
#

"""Main domain logic."""

import os
from pathlib import Path
from queue import Empty, Queue
from typing import List

from ghga_connector.core import exceptions
from ghga_connector.core.api_calls import (
    UploadStatus,
    WorkPackageAccessor,
    await_download_url,
    check_url,
    get_download_urls,
    get_file_header_envelope,
    get_part_upload_urls,
    patch_multipart_upload,
    start_multipart_upload,
)
from ghga_connector.core.file_operations import (
    Crypt4GHDecryptor,
    Crypt4GHEncryptor,
    calc_part_ranges,
    download_file_parts,
    is_file_encrypted,
    read_file_parts,
    upload_file_part,
)
from ghga_connector.core.message_display import AbstractMessageDisplay


def upload(  # noqa C901, pylint: disable=too-many-statements,too-many-branches
    *,
    api_url: str,
    file_id: str,
    file_path: Path,
    message_display: AbstractMessageDisplay,
    server_pubkey: str,
    my_public_key_path: Path,
    my_private_key_path: Path,
) -> None:
    """
    Core command to upload a file. Can be called by CLI, GUI, etc.
    """

    if not my_public_key_path.is_file():
        raise exceptions.PubKeyFileDoesNotExistError(pubkey_path=my_public_key_path)

    if not my_private_key_path.is_file():
        raise exceptions.PrivateKeyFileDoesNotExistError(
            private_key_path=my_private_key_path
        )

    if not file_path.is_file():
        raise exceptions.FileDoesNotExistError(file_path=file_path)

    if is_file_encrypted(file_path):
        raise exceptions.FileAlreadyEncryptedError(file_path=file_path)

    if not check_url(api_url):
        raise exceptions.ApiNotReachableError(api_url=api_url)

    try:
        upload_id, part_size = start_multipart_upload(
            api_url=api_url, file_id=file_id, pubkey_path=my_public_key_path
        )
    except exceptions.NoUploadPossibleError as error:
        raise error
    except exceptions.UploadNotRegisteredError as error:
        raise error
    except exceptions.UserHasNoUploadAccessError as error:
        raise error
    except exceptions.FileNotRegisteredError as error:
        raise error
    except exceptions.BadResponseCodeError as error:
        raise error
    except exceptions.CantChangeUploadStatusError as error:
        message_display.failure(f"The file with id '{file_id}' was already uploaded.")
        raise error
    except exceptions.RequestFailedError as error:
        message_display.failure("The request to start a multipart upload has failed.")
        raise error

    encryptor = Crypt4GHEncryptor(
        server_pubkey=server_pubkey,
        my_private_key_path=my_private_key_path,
    )

    encrypted_file_path = encryptor.encrypt_file(file_path=file_path)

    try:
        upload_file_parts(
            api_url=api_url,
            upload_id=upload_id,
            part_size=part_size,
            file_path=Path(encrypted_file_path),
        )
    except exceptions.ConnectionFailedError as error:
        message_display.failure("The upload failed too many times and was aborted.")
        raise error
    finally:
        # remove temporary encrypted file
        os.remove(encrypted_file_path)

    try:
        patch_multipart_upload(
            api_url=api_url,
            upload_id=upload_id,
            upload_status=UploadStatus.UPLOADED,
        )
    except exceptions.BadResponseCodeError as error:
        message_display.failure(
            f"The request to confirm the upload with id '{upload_id}' was invalid."
        )
        raise error
    except exceptions.RequestFailedError as error:
        message_display.failure(f"Confirming the upload with id '{upload_id}' failed.")
        raise error
    message_display.success(f"File with id '{file_id}' has been successfully uploaded.")


def upload_file_parts(
    *,
    api_url: str,
    upload_id: str,
    part_size: int,
    file_path: Path,
) -> None:
    """
    Uploads a file using a specific upload id via uploading all its parts.
    """

    with open(file_path, "rb") as file:
        file_parts = read_file_parts(file, part_size=part_size)
        upload_urls = get_part_upload_urls(api_url=api_url, upload_id=upload_id)

        for part, upload_url in zip(file_parts, upload_urls):
            upload_file_part(presigned_url=upload_url, part=part)


def download(  # pylint: disable=too-many-arguments, too-many-locals # noqa: C901, R0914
    *,
    api_url: str,
    output_dir: Path,
    part_size: int,
    message_display: AbstractMessageDisplay,
    max_wait_time: int,
    work_package_accessor: WorkPackageAccessor,
    file_id: str,
    file_extension: str = "",
) -> None:
    """
    Core command to download a file. Can be called by CLI, GUI, etc.
    """

    if not check_url(api_url):
        raise exceptions.ApiNotReachableError(api_url=api_url)

    # construct file name with suffix, if given
    file_name = f"{file_id}"
    if file_extension:
        file_name = f"{file_id}{file_extension}"

    # check output file
    output_file = output_dir / f"{file_name}.c4gh"
    if output_file.exists():
        raise exceptions.FileAlreadyExistsError(output_file=str(output_file))

    # with_suffix() might overwrite existing suffixes, do this instead
    output_file_ongoing = output_file.parent / (output_file.name + ".part")
    if output_file_ongoing.exists():
        output_file_ongoing.unlink()

    # stage download and get file size
    download_url_tuple = await_download_url(
        file_id=file_id,
        max_wait_time=max_wait_time,
        message_display=message_display,
        work_package_accessor=work_package_accessor,
    )

    # get file header envelope
    try:
        envelope = get_file_header_envelope(
            file_id=file_id,
            work_package_accessor=work_package_accessor,
        )
    except (
        exceptions.FileNotRegisteredError,
        exceptions.EnvelopeNotFoundError,
        exceptions.ExternalApiError,
    ) as error:
        message_display.failure(
            f"The request to get an envelope for file '{file_id}' failed."
        )
        raise error

    # perform the download
    try:
        download_parts(
            envelope=envelope,
            output_file=str(output_file_ongoing),
            file_id=file_id,
            part_size=part_size,
            file_size=download_url_tuple[1],
            work_package_accessor=work_package_accessor,
        )
    except exceptions.ConnectionFailedError as error:
        # Remove file, if the download failed.
        output_file_ongoing.unlink()
        raise error
    except exceptions.NoS3AccessMethodError as error:
        output_file_ongoing.unlink()
        raise error

    # rename fully downloaded file
    if output_file.exists():
        raise exceptions.DownloadFinalizationError(file_path=output_file)
    output_file_ongoing.rename(output_file)

    message_display.success(
        f"File with id '{file_id}' has been successfully downloaded."
    )


def download_parts(  # pylint: disable=too-many-locals
    *,
    max_concurrent_downloads: int = 5,
    max_queue_size: int = 10,
    part_size: int,
    file_size: int,
    file_id: str,
    output_file: str,
    envelope: bytes,
    work_package_accessor: WorkPackageAccessor,
):
    """
    Downloads a file from the given URL using multiple threads and saves it to a file.

    :param max_concurrent_downloads: Maximum number of parallel downloads.
    :param max_queue_size: Maximum size of the queue.
    :param part_size: Size of each part to download.
    """

    # Split the file into parts based on the part size
    part_ranges = calc_part_ranges(part_size=part_size, total_file_size=file_size)

    # Create a queue object to store downloaded parts
    queue: Queue = Queue(maxsize=max_queue_size)

    # Get the download urls
    download_urls = get_download_urls(
        file_id=file_id, work_package_accessor=work_package_accessor
    )

    # Download the file parts in parallel
    download_file_parts(
        max_concurrent_downloads=max_concurrent_downloads,
        queue=queue,
        part_ranges=part_ranges,
        download_urls=download_urls,
    )

    # Write the downloaded parts to a file
    with open(output_file, "wb") as file:
        # put envelope in file
        file.write(envelope)
        offset = len(envelope)
        downloaded_size = 0
        while downloaded_size < file_size:
            try:
                start, part = queue.get(block=False)
            except Empty:
                continue
            file.seek(offset + start)
            file.write(part)
            downloaded_size += len(part)
            queue.task_done()


def get_wps_token(max_tries: int, message_display: AbstractMessageDisplay) -> List[str]:
    """
    Expect the work package id and access token as a colon separated string
    The user will have to input this manually to avoid it becoming part of the
    command line history.
    """
    for _ in range(max_tries):
        work_package_string = input(
            "Please paste the complete download token "
            + "that you copied from the GHGA data portal: "
        )
        work_package_parts = work_package_string.split(":")
        if not (
            len(work_package_parts) == 2
            and 20 <= len(work_package_parts[0]) < 40
            and 80 <= len(work_package_parts[1]) < 120
        ):
            message_display.display(
                "Invalid input. Please enter the download token "
                + "you got from the GHGA data portal unaltered."
            )
            continue
        return work_package_parts
    raise exceptions.InvalidWorkPackageToken(tries=max_tries)


def decrypt_file(
    input_file: Path, output_file: Path, decryption_private_key_path: Path
):
    """Delegate decryption of a file Crypt4GH"""
    decryptor = Crypt4GHDecryptor(decryption_key_path=decryption_private_key_path)
    decryptor.decrypt_file(input_path=input_file, output_path=output_file)
