import requests
import responses

from unittest.mock import patch


@responses.activate
def test_requests():
    responses.add(responses.GET, "http://someurl", json={"Title": "All the movies and medias"}, status=200)
    res = requests.get("http://someurl")
    mock_res = {"Title": "All the movies and medias"}
    res_pretty = res.json()
    assert res_pretty["Title"] == mock_res["Title"]
    assert responses.calls[0].request.url == "http://someurl/"


@patch("cinemator.cinemat.restful_events.make_get")
def test_make_get(mock_get):
    mock_get.return_value = {"Title": "All the movies and medias"}
    res = mock_get()
    assert res == {"Title": "All the movies and medias"}
