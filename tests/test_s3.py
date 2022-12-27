import os
import tempfile

import boto3
from moto import mock_s3

from sync_tool.hash import get_sha256
from sync_tool.s3 import _chunk_list, delete_files, download_file, get_keys, upload_file
from tests.base_test_framework import BaseTest


@mock_s3
class TestS3(BaseTest):
    """Unittests for s3 module."""

    def setUp(self) -> None:
        """Setup test fixtures."""
        super().setUp()

        # Create test bucket and upload one file
        self.bucket = "test_bucket"
        s3 = boto3.client("s3", region_name="us-east-1")
        s3.create_bucket(Bucket=self.bucket)
        self.key = "some/key/name"
        self.content = b"Mock file created during setup as test fixture"
        with tempfile.NamedTemporaryFile(
            suffix=".txt", prefix="setup_created_file", dir=os.getcwd()
        ) as f:
            f.write(self.content)
            upload_file(
                bucket=self.bucket,
                key=self.key,
                file_name=f.name,
                sha256=get_sha256(f.name),
            )

    def test_upload_file(self):
        """Confirm that upload_file method works as intended."""
        with tempfile.NamedTemporaryFile(
            suffix=".txt", prefix="fake_file", dir=os.getcwd()
        ) as f:
            f.write(b"Hello world")
            result = upload_file(
                bucket=self.bucket,
                key=self.key,
                file_name=f.name,
                sha256=get_sha256(f.name),
            )
            self.assertTrue(result)

    def test_upload_file_fails_missing_bucket(self):
        """Confirm that if a ClientError is raised upload fails."""
        with tempfile.NamedTemporaryFile(
            suffix=".txt", prefix="fake_file", dir=os.getcwd()
        ) as f:
            f.write(b"Hello world")
            result = upload_file(
                bucket="non_existent_bucket",
                key=self.key,
                file_name=f.name,
                sha256=get_sha256(f.name),
            )
            self.assertFalse(result)

    def test_download_file(self):
        """Confirm that download_file method works as intended."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fp = os.path.join(tmpdir, "test.txt")
            result = download_file(bucket=self.bucket, key=self.key, file_name=fp)
            self.assertTrue(result)

    def test_download_file_missing_key(self):
        """Confirm that if ClientError is raised download fails."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fp = os.path.join(tmpdir, "test.txt")
            result = download_file(
                bucket=self.bucket, key="not/there/file.txt", file_name=fp
            )
        self.assertFalse(result)

    def test_delete_files(self):
        """Confirm that delete_files method works as intended."""
        self.assertTrue(delete_files(bucket=self.bucket, keys=[self.key]))

    def test_delete_files_missing_bucket(self):
        """Confirm that if ClientError is raised delete fails."""
        self.assertFalse(delete_files(bucket="not_a_bucket", keys=[self.key]))

    def test_chunk_list(self):
        """Confirm chunking lists into sub-lists no larger than max_size works."""
        self.assertListEqual(
            [[1, 4], [2, 5], [3]],
            [chunk for chunk in _chunk_list(input_list=[1, 2, 3, 4, 5], max_size=2)],
        )
        self.assertListEqual(
            [[1] * 501, [1] * 500],
            [chunk for chunk in _chunk_list(input_list=[1] * 1001)],
        )
        self.assertListEqual(
            [[1] * 1000], [chunk for chunk in _chunk_list(input_list=[1] * 1000)]
        )

    def test_get_keys(self):
        """Confirm that method for getting keys from a bucket works as intended."""
        with tempfile.NamedTemporaryFile(
            suffix=".txt", prefix="setup_created_file", dir=os.getcwd()
        ) as f:
            f.write(self.content)
            for i in range(1003):
                upload_file(
                    bucket=self.bucket,
                    key=f"{self.key}_{i}",
                    file_name=f.name,
                    sha256=get_sha256(f.name),
                )
        expected = {self.key}
        expected.update({f"{self.key}_{i}" for i in range(1003)})
        self.assertSetEqual(
            expected,
            get_keys(bucket=self.bucket, prefix=self.key),
        )

        self.assertSetEqual(set(), get_keys(bucket=self.bucket, prefix="missing"))
