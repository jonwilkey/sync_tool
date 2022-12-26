from tests.base_test_framework import BaseTest

from sync_tool.hash import get_sha256


class TestHash(BaseTest):
    def test_get_sha256(self):
        self.assertEqual(
            get_sha256(self._get_fixture_path("config.json")),
            "garadtt0f3aMgyHd5Yv3eNEcwLaDzruvmmvS1QLfq0o=",
        )
