"""Test only_joking.py using unittest to mock api calls."""
import pytest
from unittest.mock import MagicMock, patch
import requests

from example_pkg.only_joking import get_joke
import example_pkg.only_joking


def test_get_joke_magicmocked_entirely(ULTI_JOKE):
    """Completely replace the entire get_joke return value.

    Not a good idea for testing as none of our source code will be tested. But
    this demonstrates how to entirely scrub a function and replace with any
    placeholder value at pytest runtime."""
    # step 1
    mock_joke = MagicMock(return_value=ULTI_JOKE)
    # step 2
    with patch("example_pkg.only_joking.get_joke", mock_joke):
        # step 3
        joke = example_pkg.only_joking.get_joke()
        # step 4
        assert joke == ULTI_JOKE


def test_get_joke_json_magicmocked(ULTI_JOKE):
    """Test behaviour when user asked for JSON joke."""
    # step 1: Mock
    _mock_response = MagicMock(spec=requests.models.Response)
    _mock_response.ok = True
    _mock_response.headers = {"Content-Type": "application/json"}
    _mock_response.json.return_value = {"joke": ULTI_JOKE}
    # step 2: Patch
    with patch("requests.get", return_value=_mock_response):
        # step 3: Use
        joke = get_joke(f="application/json")
        # step 4: Assert
        assert joke == ULTI_JOKE


def test_get_joke_text_magicmocked(ULTI_JOKE):
    """Test behaviour when user asked for plain text joke."""
    # step 1: Mock
    _mock_response = MagicMock(spec=requests.models.Response)
    _mock_response.ok = True
    _mock_response.headers = {"Content-Type": "text/plain"}
    _mock_response.text = ULTI_JOKE
    # step 2: Patch
    with patch("requests.get", return_value=_mock_response):
        # step 3: Use
        joke = get_joke(f="text/plain")
        # step 4: Assert
        assert joke == ULTI_JOKE


def test_get_joke_not_implemented_magicmocked():
    """Test behaviour when user asked for HTML response."""
    # step 1: Mock
    _mock_response = MagicMock(spec=requests.models.Response)
    _mock_response.ok = True
    _mock_response.headers = {"Content-Type": "text/html"}
    #  step 2: Patch
    with patch("requests.get", return_value=_mock_response):
        # step 3 & 4 Use (try to but exception is raised) & Assert
        with pytest.raises(
            NotImplementedError,
            match="client accepts 'application/json' or 'text/plain' format"):
            get_joke(f="text/html")


def test_get_joke_http_error_magicmocked():
    """Test bad HTTP response."""
    # step 1: Mock
    _mock_response = MagicMock(spec=requests.models.Response)
    _mock_response.ok = False
    _mock_response.status_code = 404
    _mock_response.reason = "Not Found"
    # step 2: Patch
    with patch("requests.get", return_value=_mock_response):
        # step 3 & 4 Use (try to but exception is raised) & Assert
        with pytest.raises(requests.HTTPError, match="404: Not Found"):
            get_joke()
