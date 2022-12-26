import os
from unittest import TestCase
from unittest.mock import Mock, patch


class BaseTest(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.module_path = ""

    def _get_patch(self, target: str, *args, **kwargs) -> Mock:
        patch_obj = patch(self.module_path + target, autospec=True, *args, **kwargs)
        patch_obj.start()
        return patch_obj

    def _get_fixture_path(self, fixture: str) -> str:
        return os.path.join(os.getcwd().split("tests")[0], "tests", "fixtures", fixture)
