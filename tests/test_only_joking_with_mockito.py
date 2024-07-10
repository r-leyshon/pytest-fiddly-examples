from mockito import when, unstub
import pytest
import requests

import example_pkg.only_joking

ULTI_JOKE = ("Doc, I can't stop singing 'The Green, Green Grass of Home.' That "
"sounds like Tom Jones Syndrome. Is it common? Well, It's Not Unusual.")


def test_get_joke_mockitoed_entirely():
    """Completely replace the entire get_joke return value.

    Not a good idea for testing as none of our source code will be tested. But
    this demonstrates how to entirely scrub a function and replace with any
    placeholder value at pytest runtime."""
    when(example_pkg.only_joking).get_joke().thenReturn(ULTI_JOKE)
    joke = example_pkg.only_joking.get_joke()
    assert joke == ULTI_JOKE
    unstub()


def test_get_joke_json_mockito():
    # step 1: Mock
    mock_response = requests.models.Response()
    mock_response.status_code = 200
    mock_response._content = b'{"joke": "' + ULTI_JOKE.encode("utf-8") + b'"}'
    mock_response.headers = {"Content-Type": "application/json"}
    # step 2: Patch
    when(requests).get(...).thenReturn(mock_response)
    # step 3: Use
    joke = example_pkg.only_joking.get_joke(f="application/json")
    # step 4: Assert
    assert joke == ULTI_JOKE
    unstub()


def test_get_joke_text_mockito():
    # step 1: Mock
    mock_response = requests.models.Response()
    mock_response.status_code = 200
    mock_response._content = ULTI_JOKE.encode("utf-8")
    mock_response.headers = {"Content-Type": "text/plain"}
    # step 2: Patch
    when(requests).get(...).thenReturn(mock_response)
    # step 3: Use
    joke = example_pkg.only_joking.get_joke(f="text/plain")
    # step 4: Assert
    assert joke == ULTI_JOKE
    unstub()


def test_get_joke_not_implemented_mockito():
    # step 1: Mock
    mock_response = requests.models.Response()
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "text/html"}
    # step 2: Patch
    when(
        example_pkg.only_joking
        )._query_endpoint(...).thenReturn(mock_response)
    # step 3 & 4 Use (try to but exception is raised) & Assert
    with pytest.raises(
        NotImplementedError,
        match="This client accepts 'application/json' or 'text/plain' format"):
        example_pkg.only_joking.get_joke(f="text/html")
    unstub()


def test_get_joke_http_error_mockito():
    # step 1: Mock
    mock_response = requests.models.Response()
    mock_response.status_code = 404
    mock_response.reason = "Not Found"
    # step 2: Patch
    when(example_pkg.only_joking)._query_endpoint(...).thenReturn(
        mock_response)
    # step 3 & 4 Use (try to but exception is raised) & Assert
    with pytest.raises(requests.HTTPError, match="404: Not Found"):
        example_pkg.only_joking.get_joke()
    unstub()
