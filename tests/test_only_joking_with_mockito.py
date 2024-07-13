from mockito import when, unstub
import pytest
import requests

import example_pkg.only_joking


def test_get_joke_mockitoed_entirely(ULTI_JOKE):
    """Completely replace the entire get_joke return value.

    Not a good idea for testing as none of our source code will be tested. But
    this demonstrates how to entirely scrub a function and replace with any
    placeholder value at pytest runtime."""
    # step 1 & 2
    when(example_pkg.only_joking).get_joke().thenReturn(ULTI_JOKE)
    # step 3
    joke = example_pkg.only_joking.get_joke()
    # step 4
    assert joke == ULTI_JOKE
    unstub()


def test_get_joke_json_mockitoed(ULTI_JOKE):
    """Test behaviour when user asked for JSON joke."""
    # step 1: Mock
    _mock_response = requests.models.Response()
    _mock_response.status_code = 200
    _mock_response._content = b'{"joke": "' + ULTI_JOKE.encode("utf-8") + b'"}'
    _mock_response.headers = {"Content-Type": "application/json"}
    # step 2: Patch
    when(requests).get(...).thenReturn(_mock_response)
    # step 3: Use
    joke = example_pkg.only_joking.get_joke(f="application/json")
    # step 4: Assert
    assert joke == ULTI_JOKE
    unstub()


def test_get_joke_text_mockitoed(ULTI_JOKE):
    """Test behaviour when user asked for plain text joke."""
    # step 1: Mock
    _mock_response = requests.models.Response()
    _mock_response.status_code = 200
    _mock_response._content = ULTI_JOKE.encode("utf-8")
    _mock_response.headers = {"Content-Type": "text/plain"}
    # step 2: Patch
    when(requests).get(...).thenReturn(_mock_response)
    # step 3: Use
    joke = example_pkg.only_joking.get_joke(f="text/plain")
    # step 4: Assert
    assert joke == ULTI_JOKE
    unstub()


def test_get_joke_not_implemented_mockitoed():
    """Test behaviour when user asked for HTML response."""
    # step 1: Mock
    _mock_response = requests.models.Response()
    _mock_response.status_code = 200
    _mock_response.headers = {"Content-Type": "text/html"}
    # step 2: Patch
    when(
        example_pkg.only_joking
        )._query_endpoint(...).thenReturn(_mock_response)
    # step 3 & 4 Use (try to but exception is raised) & Assert
    with pytest.raises(
        NotImplementedError,
        match="This client accepts 'application/json' or 'text/plain' format"):
        example_pkg.only_joking.get_joke(f="text/html")
    unstub()


def test_get_joke_http_error_mockitoed():
    """Test bad HTTP response."""
    # step 1: Mock
    _mock_response = requests.models.Response()
    _mock_response.status_code = 404
    _mock_response.reason = "Not Found"
    # step 2: Patch
    when(example_pkg.only_joking)._query_endpoint(...).thenReturn(
        _mock_response)
    # step 3 & 4 Use (try to but exception is raised) & Assert
    with pytest.raises(requests.HTTPError, match="404: Not Found"):
        example_pkg.only_joking.get_joke()
    unstub()
