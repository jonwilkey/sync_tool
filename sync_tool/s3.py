"""Module for uploading, downloading, deleting and listing objects in S3."""

import logging
import math
from typing import Iterator

import boto3
from botocore.exceptions import ClientError

log = logging.getLogger()


def upload_file(bucket: str, key: str, file_name: str, sha256: bytes) -> bool:
    """Upload a file to an S3 bucket.

    :param bucket: Bucket to upload to
    :param key: The name of the key to upload to
    :param file_name: The path to the file to upload
    :param sha256: SHA256 digest of file to upload
    :return: True if file was uploaded and has matching MD5 value, else False
    """
    s3_client = boto3.client("s3")
    try:
        with open(file_name, "rb") as f:
            s3_client.put_object(Body=f, Bucket=bucket, Key=key, ChecksumSHA256=sha256)
    except ClientError as e:
        log.error(e)
        return False
    return True


def download_file(bucket: str, key: str, file_name: str) -> bool:
    """Download a file from an S3 bucket.

    :param bucket: Bucket to download from
    :param key: The name of the key to download from
    :param file_name: The path to the file to download to
    :return: True if file was uploaded, else False
    """
    s3 = boto3.resource("s3")
    try:
        s3.Bucket(bucket).download_file(key, file_name)
    except ClientError as e:
        log.error(e)
        return False
    return True


def delete_files(bucket: str, keys: list[str]) -> bool:
    """Delete all keys located in specified bucket.

    If more than 1000 keys are specified for deletion, :param:`keys` is split into
    sub-lists of <= 1000 keys each a separate calls to :meth:`delete_objects` is called
    for each sub-list.

    :param bucket: Bucket to delete files from
    :param keys: Keys to be deleted
    :return: True if files were deleted, False if any batch of deletes failed
    """
    s3_client = boto3.client("s3")
    try:
        for keys_chunk in _chunk_list(keys):
            s3_client.delete_objects(
                Bucket=bucket, Delete={"Objects": [{"Key": key} for key in keys_chunk]}
            )
    except ClientError as e:
        log.error(e)
        return False
    return True


def get_keys(bucket: str, prefix: str) -> set[str]:
    """Get all keys in specified bucket under the specified prefix.

    :param bucket: Bucket to get keys from
    :param prefix: Prefix of keys to get
    :return: Set of keys belonging to desired prefix in specified bucket
    """
    s3_client = boto3.client("s3")
    response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
    keys = {item["Key"] for item in response.get("Contents", [])}
    while response["IsTruncated"]:
        response = s3_client.list_objects_v2(
            Bucket=bucket,
            Prefix=prefix,
            ContinuationToken=response["NextContinuationToken"],
        )
        keys.update({item["Key"] for item in response["Contents"]})
    return keys


def _chunk_list(input_list: list, max_size: int = 1000) -> Iterator[list]:
    """Yield striped chunks from l of up to the given max size.

    :param input_list: Input list
    :param max_size: Max allowed size of chunked lists, defaults to 1000
    :yield: List(s) of up to max size
    """
    n = math.ceil(len(input_list) / max_size)
    for i in range(0, n):
        yield input_list[i::n]
