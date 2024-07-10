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


def test_get_joke_json_magicmocked():
    """Test behaviour when user asked for JSON joke."""
    # step 1: Mock
    mock_response = MagicMock(spec=requests.models.Response)
    mock_response.ok = True
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json.return_value = {"joke": ULTI_JOKE}
    # step 2: Patch
    with patch("requests.get", return_value=mock_response):
        # step 3: Use
        joke = get_joke(f="application/json")
        # step 4: Assert
        assert joke == ULTI_JOKE


def test_get_joke_text_magicmocked():
    """Test behaviour when user asked for plain text joke."""
    # step 1: Mock
    mock_response = MagicMock(spec=requests.models.Response)
    mock_response.ok = True
    mock_response.headers = {"Content-Type": "text/plain"}
    mock_response.text = ULTI_JOKE
    # step 2: Patch
    with patch("requests.get", return_value=mock_response):
        # step 3: Use
        joke = get_joke(f="text/plain")
        # step 4: Assert
        assert joke == ULTI_JOKE


def test__handle_response_not_implemented_magicmocked():
    """Test behaviour when user asked for HTML response."""
    # step 1: Mock
    mock_response = MagicMock(spec=requests.models.Response)
    mock_response.ok = True
    mock_response.headers = {"Content-Type": "text/html"}
    #  step 2: Patch
    with patch("requests.get", return_value=mock_response):
        # step 3 & 4 Use (try to but exception is raised) & Assert
        with pytest.raises(
            NotImplementedError,
            match="client accepts 'application/json' or 'text/plain' format"):
            get_joke(f="text/html")


def test_get_joke_http_error_magicmocked():
    """Test bad HTTP response."""
    # step 1: Mock
    mock_response = MagicMock(spec=requests.models.Response)
    mock_response.ok = False
    mock_response.status_code = 404
    mock_response.reason = "Not Found"
    # step 2: Patch
    with patch("requests.get", return_value=mock_response):
        # step 3 & 4 Use (try to but exception is raised) & Assert
        with pytest.raises(requests.HTTPError, match="404: Not Found"):
            get_joke()
