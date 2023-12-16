from cinemat.__main__ import search, type, imdb, info, details, year
from click.testing import CliRunner
from unittest import TestCase
import pytest


@pytest.fixture()
def mock_cli():
    return CliRunner()


class TestMain(TestCase):
    mock_cli = CliRunner()

    def test_search_command(self):
        res = self.mock_cli.invoke(search, ["--title", "title"])
        assert res.exit_code == 0

    def test_type_command(self):
        res = self.mock_cli.invoke(type, ["--title", "title", "--type", "movie"])
        assert res.exit_code == 0

    def test_imdb_command(self):
        res = self.mock_cli.invoke(imdb, ["--imdb", "tt0069467"])
        assert res.exit_code == 0

    def test_info_command(self):
        res = self.mock_cli.invoke(info)
        assert res.exit_code == 0

    def test_details_command(self):
        res = self.mock_cli.invoke(details, ["--title", "title", "--plot", "full", "--tomatoes", "tomat"])
        assert res.exit_code == 0

    def test_year_command(self):
        res=self.mock_cli.invoke(year,['--title','title','--year','1972'])
        assert res.exit_code == 0
