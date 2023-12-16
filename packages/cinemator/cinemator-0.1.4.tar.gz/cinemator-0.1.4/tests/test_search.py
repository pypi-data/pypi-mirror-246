import sys
from unittest.mock import patch
from unittest import TestCase


mock_list = [
    {
        "Title": "Boys Don't Cry",
        "Year": "1999",
        "imdbID": "tt0171804",
        "Type": "movie",
        "Poster": "https://m.media-amazon.com/images/M/MV5BN2Y.jpg",
    },
    {
        "Title": "Cry-Baby",
        "Year": "1990",
        "imdbID": "tt0099329",
        "Type": "movie",
        "Poster": "https://m.media-amazon.com/images/M/MV5BOG.jpg",
    },
    {
        "Title": "Cry Wolf",
        "Year": "2005",
        "imdbID": "tt0384286",
        "Type": "movie",
        "Poster": "https://m.media-amazon.com/images/M/MV5BODA0jpg",
    },
    {
        "Title": "Far Cry 3",
        "Year": "2012",
        "imdbID": "tt2321297",
        "Type": "game",
        "Poster": "https://m.media-amazon.com/images/M/MV5BM.jpg",
    },
]


@patch("builtins.print")
def test_pretty_printer(mock_print):

    mock_print(mock_list, "keyword")
    mock_print.assert_called_with(mock_list, "keyword")
    sys.stdout.write(str(mock_print.call_args) + "\n")
    sys.stdout.write(str(mock_print.call_args_list) + "\n")


@patch("cinemator.cinemat.search.find")
class TestFind(TestCase):
    def test_find(self, mock_find):
        mock_find("title", "", "keyword")
        mock_find.assert_called_with("title", "", "keyword")

    def test_find_type(self, mock_find):
        mock_find("title", "", "type")
        mock_find.assert_called_with("title", "", "type")

    def test_find_year(self, mock_find):
        mock_find("title", "", "year")
        mock_find.assert_called_with("title", "", "year")
