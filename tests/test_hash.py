from sync_tool.hash import get_sha256
from tests.base_test_framework import BaseTest


class TestHash(BaseTest):
    """Unit tests for hash module."""

    def test_get_sha256(self):
        """Confirm that method for getting SHA256 checksum works as expected."""
        self.assertEqual(
            get_sha256(self._get_fixture_path("mock_local/stuff/file_a.txt")),
            "SEacD8laIsCh/vATw7L7hYZn0KB+ql1Z8MIl3/1wO+k=",
        )
