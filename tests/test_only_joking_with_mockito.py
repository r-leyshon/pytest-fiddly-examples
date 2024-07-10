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
    # Create a mock response object with the expected properties and methods
    mock_response = requests.models.Response()
    mock_response.status_code = 200
    mock_response._content = b'{"joke": "' + ULTI_JOKE.encode("utf-8") + b'"}'
    mock_response.headers = {"Content-Type": "application/json"}
    # Use mockito to mock requests.get to return the mock response
    when(requests).get(...).thenReturn(mock_response)
    # Call the function to test
    joke = example_pkg.only_joking.get_joke(f="application/json")
    # Assert the expected result
    assert joke == ULTI_JOKE
    unstub()


def test_get_joke_text_mockito():
    # Create a mock response object with the expected properties and methods
    mock_response = requests.models.Response()
    mock_response.status_code = 200
    mock_response._content = ULTI_JOKE.encode("utf-8")
    mock_response.headers = {"Content-Type": "text/plain"}
    # Use mockito to mock requests.get to return the mock response
    when(requests).get(...).thenReturn(mock_response)
    # Call the function to test
    joke = example_pkg.only_joking.get_joke(f="text/plain")
    assert joke == ULTI_JOKE
    unstub()


def test__handle_response_not_implemented_mockito():
    # Create a mock response object with a Content-Type that is not supported
    mock_response = requests.models.Response()
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "text/html"}
    when(
        example_pkg.only_joking
        )._query_endpoint(...).thenReturn(mock_response)
    # Call the function and assert it raises NotImplementedError
    with pytest.raises(
        NotImplementedError,
        match="This client accepts 'application/json' or 'text/plain' format"):
        example_pkg.only_joking._handle_response(mock_response)    
    unstub()


def test__handle_response_http_error_mockito():
    # Create a mock response object with an error status
    mock_response = requests.models.Response()
    mock_response.status_code = 404
    mock_response.reason = "Not Found"
    # Use mockito to mock the response object
    when(example_pkg.only_joking)._query_endpoint(...).thenReturn(mock_response)
    # Call the function and assert it raises HTTPError
    with pytest.raises(requests.HTTPError, match="404: Not Found"):
        example_pkg.only_joking._handle_response(mock_response)
    unstub()
