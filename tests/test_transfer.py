import os

import boto3
from moto import mock_s3

from sync_tool.config import load_config
from sync_tool.hash import get_sha256
from sync_tool.s3 import upload_file
from sync_tool.transfer import get_src_dst_map
from tests.base_test_framework import BaseTest


@mock_s3
class TestTransfer(BaseTest):
    """Unit tests for transfer module."""

    def setUp(self) -> None:
        """Setup fixtures."""
        super().setUp()
        self.config = load_config(self._get_fixture_path("config.json"), direction="up")
        self.config.local_to_s3_paths = {
            self._get_fixture_path("mock_local/stuff/"): "stuff",
            self._get_fixture_path("mock_local/things/"): "things",
        }

        # Mock S3 bucket setup
        s3 = boto3.client("s3", region_name="us-east-1")
        s3.create_bucket(Bucket=self.config.s3_bucket)
        for root, _, files in os.walk(self._get_fixture_path("mock_bucket")):
            for f in files:
                name = os.path.join(root, f)
                upload_file(
                    bucket=self.config.s3_bucket,
                    key=name.split("mock_bucket/")[1],
                    file_name=name,
                    sha256=get_sha256(name),
                )

    def test_get_src_dst_map_upload(self):
        """Confirm that src-to-dst map is created as expected for uploading."""
        m = get_src_dst_map(config=self.config)
        expected = {
            self._get_fixture_path(f"mock_local/{path}"): path
            for path in [
                "stuff/file_a.txt",
                "stuff/file_b.txt",
                "things/subthings/file_c.txt",
                "things/subthings/file_d.txt",
            ]
        }
        self.assertDictEqual(m, expected)

    def test_get_src_dst_map_download(self):
        """Confirm that src-to-dst map is created as expected for downloading."""
        self.config.direction = "down"
        m = get_src_dst_map(config=self.config)
        expected = {
            path: self._get_fixture_path(f"mock_local/{path}")
            for path in [
                "stuff/file_a.txt",
                "things/file_b.txt",
                "things/subthings/file_c.txt",
                "things/subthings/file_d.txt",
            ]
        }
        self.assertDictEqual(m, expected)
