from click.testing import CliRunner

from sync_tool.cli import run
from tests.base_test_framework import BaseTest


class TestCli(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.runner = CliRunner()

    def test_run_both_up_and_down(self):
        result = self.runner.invoke(run, ["--down", "--up"])
        self.assertEqual(result.exit_code, 1)
        self.assertIsInstance(result.exception, ValueError)
        self.assertEqual(
            result.exception.args, ("Please specify either --up or --down, not both",)
        )

    def test_run_neither_up_or_down(self):
        result = self.runner.invoke(run)
        self.assertEqual(result.exit_code, 1)
        self.assertIsInstance(result.exception, ValueError)
        self.assertEqual(
            result.exception.args, ("Please specify either --up or --down",)
        )
