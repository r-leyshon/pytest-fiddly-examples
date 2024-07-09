"""Test only_joking.py using monkeypatch to mock api calls."""
import pytest
import requests

from example_pkg.only_joking import get_joke, _handle_response

ULTI_JOKE = """
"Doc, I can't stop singing 'The Green, Green Grass of Home.'" "That sounds like
Tom Jones Syndrome." "Is it common?" Well, "It's Not Unusual."
"""


def test_get_joke_no_OOP(monkeypatch):
    # step 1, mock the response object
    def mock_response(*args, **kwargs):
        resp = requests.models.Response()
        resp.status_code = 200
        resp._content = ULTI_JOKE.encode("UTF8")
        resp.headers = {"Content-Type": "text/plain"}
        return resp
    
    # step 2, patch requests.get
    monkeypatch.setattr(requests, "get", mock_response)
    # step 3, use requests.get
    joke = get_joke()
    # step 4, make an assertion
    assert joke == ULTI_JOKE, f"Expected:\n'{ULTI_JOKE}\nFound:\n{joke}'"
    # will also work for json format
    joke = get_joke(f="application/json")
    assert joke == ULTI_JOKE, f"Expected:\n'{ULTI_JOKE}\nFound:\n{joke}'"


## Docs solution


@pytest.fixture
def _mock_response():
    """Step 1, mock the response object

    Return a class instance that will mock all the properties of a response
    object that get_joke needs to work.
    """
    HEADERS_MAP = {
        "text/plain": {"Content-Type": "text/plain"},
        "application/json": {"Content-Type": "application/json"},
        "text/html": {"Content-Type": "text/html"},
    }

    class MockResponse:
        def __init__(self, f, *args, **kwargs):
            self.ok = True
            self.f = f
            self.headers = HEADERS_MAP[f] # header corresponds to format that
            # the user requested
            self.text = ULTI_JOKE 

        def json(self):
            if self.f == "application/json":
                return {"joke": ULTI_JOKE}
            return None

    return MockResponse


def test_get_joke_with_OOP(monkeypatch, _mock_response):
    """Test get_joke using the mock class fixture.

    This approach is the implementation suggested in the pytest docs.
    """
    def _mock_get_good_resp(*args, **kwargs):
        """Step 2, Return fixtures with the correct header.

        If the test uses "text/plain" format, we need to return a MockResponse
        class instance with headers attribute equal to
        {"Content-Type": "text/plain"}, likewise for JSON.
        """
        f = kwargs["headers"]["Accept"]
        return _mock_response(f)
    # Step 3, patch requests.get
    monkeypatch.setattr(requests, "get", _mock_get_good_resp)
    # Step 4, use function
    # Test for plain text format
    j_txt = get_joke(f="text/plain")
    # Test for JSON format
    j_json = get_joke(f="application/json")
    # Step 5, make assertions
    assert j_txt == ULTI_JOKE, f"Expected:\n'{ULTI_JOKE}\nFound:\n{j_txt}'"
    assert j_json == ULTI_JOKE, f"Expected:\n'{ULTI_JOKE}\nFound:\n{j_json}'"
    with pytest.raises(
        NotImplementedError,
        match="This client accepts 'application/json' or 'text/plain' format"):
        get_joke(f="text/html")


@pytest.fixture
def _mock_bad_response():
    class MockBadResponse:
        def __init__(self, *args, **kwargs):
            self.ok = False
            self.status_code = 429
            self.reason = "Too many requests"
    return MockBadResponse


def test_get_joke_bad_response(monkeypatch, _mock_bad_response):
    def _mock_get_bad_response(*args, **kwargs):
        f = kwargs["headers"]["Accept"]
        return _mock_bad_response(f)
    monkeypatch.setattr(requests, "get", _mock_get_bad_response)
    # check func raises on bad response
    with pytest.raises(requests.HTTPError, match="429: Too many requests"):
        get_joke()
