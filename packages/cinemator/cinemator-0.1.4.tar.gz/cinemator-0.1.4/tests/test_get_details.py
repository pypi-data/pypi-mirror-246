from unittest import TestCase
from unittest.mock import patch


@patch("cinemator.cinemat.get_details.show_details", return_value="Media Details")
class TestShowDetails(TestCase):
    movie_name = "baby bois"

    def test_details_full_plot(self, mock_details):
        res = mock_details(self.movie_name, "full", "")
        assert res == "Media Details"

    def test_details_short_plot(self, mock_details):
        res = mock_details(self.movie_name, "short", "")
        assert res == "Media Details"

    def test_details_with_tomat(self, mock_details):
        res = mock_details(self.movie_name, "", "tomat")
        assert res == "Media Details"

    def test_details_without_tomat_plot(self, mock_details):
        res = mock_details(self.movie_name, "", "")
        assert res == "Media Details"

    def test_details_with_tomat_full_plot(self, mock_details):
        res = mock_details(self.movie_name, "", "")
        assert res == "Media Details"



@patch("cinemator.cinemat.get_details.show_details_imdb", return_value="Media Details")
def test_get_details_imdb(mock_show_details_imdb):
    mock_show_details_imdb("tt0069467", "imdb")
    mock_show_details_imdb.assert_called_with("tt0069467", "imdb")