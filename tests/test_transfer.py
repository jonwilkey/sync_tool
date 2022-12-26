import unittest

from tests.base_test_framework import BaseTest

from sync_tool.config import load_config
from sync_tool.transfer import get_src_dst_map


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

    @unittest.skip
    def test_get_src_to_dst_map_download(self):
        """Confirm that src-to-dst map is created as expected for downloading."""
        config = load_config(self._get_fixture_path("config.json"), direction="down")
        m = get_src_dst_map(config=config)
        expected = {
            path: self._get_fixture_path(path)
            for path in [
                "stuff/file_a.txt",
                "things/file_b.txt",
                "things/subthings/file_c.txt",
                "things/subthings/file_d.txt",
            ]
        }
        self.assertDictEqual(m, expected)
