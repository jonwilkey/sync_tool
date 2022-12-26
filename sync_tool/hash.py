"""Module for getting the hash/checksum."""

import base64
import hashlib


def get_sha256(filepath: str, buffer_size: int = 2**16) -> str:
    """Get the base64 encoded SHA256 checksum of the content of the specified file.

    :param filepath: Path to the file to get the checksum for
    :param buffer_size: Amount of content to read from file at a time, defaults to 2**16
    :return: Base64 encoded SHA256 checksum of the content of the specified file
    """
    with open(filepath, "rb") as f:
        sha256 = hashlib.sha256()
        while True:
            data = f.read(buffer_size)
            if not data:
                break
            sha256.update(data)
    return base64.b64encode(sha256.digest()).decode("utf-8")
