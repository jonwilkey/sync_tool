import os
from unittest import TestCase
from unittest.mock import Mock, patch


class BaseTest(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.module_path = ""

        # Ensure that any environment variables with actual AWS credentials are mocked
        os.environ["AWS_ACCESS_KEY_ID"] = "testing"
        os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
        os.environ["AWS_SECURITY_TOKEN"] = "testing"
        os.environ["AWS_SESSION_TOKEN"] = "testing"
        os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

    def _get_patch(self, target: str, *args, **kwargs) -> Mock:
        patch_obj = patch(self.module_path + target, autospec=True, *args, **kwargs)
        patch_obj.start()
        return patch_obj

    def _get_fixture_path(self, fixture: str) -> str:
        return os.path.join(os.getcwd().split("tests")[0], "tests", "fixtures", fixture)
