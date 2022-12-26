import json

from tests.base_test_framework import BaseTest

from sync_tool.config import Config, load_config


class TestConfig(BaseTest):
    def setUp(self):
        super().setUp()
        with open(self._get_fixture_path("config.json"), "r") as f:
            self.config_data = json.load(f)

    def test_config_post_init(self):
        config = Config(**self.config_data, direction="up")
        self.assertDictEqual(
            config.sync_plan, {"/mnt/c/some_directory": "mock/key"}
        )

    def test_load_config(self):
        config = load_config(self._get_fixture_path("config.json"), "down")
        self.assertEqual(
            config,
            Config(
                local_to_s3_paths={
                    "/mnt/c/some_directory": "mock/key"
                },
                s3_bucket="fake-bucket",
                direction="down",
            ),
        )

    def test_config_post_init_raises_with_bad_direction_arg(self):
        with self.assertRaisesRegex(ValueError, "'bad' is not a valid value"):
            Config(**self.config_data, direction="bad")
