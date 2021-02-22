import os

from click.testing import CliRunner


# TODO: https://click.palletsprojects.com/en/7.x/testing/
from microwler.cli.cmd import add_project, run_crawler


class TestCLI:
    runner = CliRunner()
    folder = os.path.join(os.getcwd(), 'projects')

    def test_add_project(self):
        result = self.runner.invoke(add_project, ['quotes', 'https://quotes.toscrape.com/'])
        assert result.exit_code == 0
        assert os.path.exists(os.path.join(self.folder, 'quotes.py'))

    def test_run_crawler(self):
        result = self.runner.invoke(run_crawler, ['quotes'])
        assert result.exit_code == 0
