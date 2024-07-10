"""Test only_joking.py using unittest to mock api calls."""
import pytest
from unittest.mock import MagicMock, patch
import requests

from example_pkg.only_joking import _query_endpoint, _handle_response, get_joke
import example_pkg.only_joking

ULTI_JOKE = """
"Doc, I can't stop singing 'The Green, Green Grass of Home.'" "That sounds like
Tom Jones Syndrome." "Is it common?" Well, "It's Not Unusual."
"""


def test_get_joke_magicmocked_entirely():
    """Completely replace the entire get_joke return value.

    Not a good idea for testing as none of our source code will be tested. But
    this demonstrates how to entirely scrub a function and replace with any
    placeholder value at pytest runtime."""
    mock_joke = MagicMock(return_value=ULTI_JOKE)
    with patch("example_pkg.only_joking.get_joke", mock_joke):
        joke = example_pkg.only_joking.get_joke()
        assert joke == ULTI_JOKE


def test_get_joke_json_magicmock():
    # Create a mock response object with the expected properties and methods
    mock_response = MagicMock(spec=requests.models.Response)
    mock_response.ok = True
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json.return_value = {"joke": ULTI_JOKE}
    # Use patch to mock requests.get to return the mock response
    with patch("requests.get", return_value=mock_response):
        # Call the function to test
        joke = get_joke(f="application/json")
        # Assert the expected result
        assert joke == ULTI_JOKE


def test_get_joke_text_magicmock():
    # Create a mock response object with the expected properties and methods
    mock_response = MagicMock(spec=requests.models.Response)
    mock_response.ok = True
    mock_response.headers = {"Content-Type": "text/plain"}
    mock_response.text = ULTI_JOKE
    # Use patch to mock requests.get to return the mock response
    with patch("requests.get", return_value=mock_response):
        # Call the function to test
        joke = get_joke(f="text/plain")
        # Assert the expected result
        assert joke == ULTI_JOKE


def test__handle_response_not_implemented_magicmock():
    # Create a mock response object with a Content-Type that is not supported
    mock_response = MagicMock(spec=requests.models.Response)
    mock_response.ok = True
    mock_response.headers = {"Content-Type": "text/html"}
    # Call the function and assert it raises NotImplementedError
    with pytest.raises(
        NotImplementedError,
        match="This client accepts 'application/json' or 'text/plain' format"):
        _handle_response(mock_response)


def test__handle_response_http_error_magicmock():
    # Create a mock response object with an error status
    mock_response = MagicMock(spec=requests.models.Response)
    mock_response.ok = False
    mock_response.status_code = 404
    mock_response.reason = "Not Found"
    # Call the function and assert it raises HTTPError
    with pytest.raises(requests.HTTPError, match="404: Not Found"):
        _handle_response(mock_response)
