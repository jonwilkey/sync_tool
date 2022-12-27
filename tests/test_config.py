import json

from sync_tool.config import Config, load_config
from tests.base_test_framework import BaseTest


class TestConfig(BaseTest):
    """Unit tests for config module."""

    def setUp(self):
        """Setup fixtures."""
        super().setUp()
        with open(self._get_fixture_path("config.json"), "r") as f:
            self.config_data = json.load(f)
        self.expected_local_to_s3_paths = self.config_data["local_to_s3_paths"]

    def test_config_post_init(self):
        """Confirm that post_init method on Config class creates expected sync plan."""
        config = Config(**self.config_data, direction="up")
        self.assertDictEqual(config.sync_plan, self.expected_local_to_s3_paths)

    def test_load_config(self):
        """Confirm that loading config from JSON behaves as expected."""
        config = load_config(self._get_fixture_path("config.json"), "down")
        self.assertEqual(
            config,
            Config(
                local_to_s3_paths=self.expected_local_to_s3_paths,
                s3_bucket="fake-bucket",
                direction="down",
            ),
        )
        self.assertDictEqual(
            config.sync_plan, {v: k for k, v in self.expected_local_to_s3_paths.items()}
        )

    def test_config_post_init_raises_with_bad_direction_arg(self):
        """Config that if bad direction value is given that ValueError is raised."""
        with self.assertRaisesRegex(ValueError, "'bad' is not a valid value"):
            Config(**self.config_data, direction="bad")
