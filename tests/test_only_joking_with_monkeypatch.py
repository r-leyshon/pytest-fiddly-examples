"""Test only_joking.py using monkeypatch to mock api calls."""
import pytest
import requests

from example_pkg.only_joking import get_joke, _handle_response
import example_pkg.only_joking


def test_get_joke_monkeypatched_entirely(monkeypatch, ULTI_JOKE):
    """Completely replace the entire get_joke return value.

    Not a good idea for testing as none of our source code will be tested. But
    this demonstrates how to entirely scrub a function and replace with any
    placeholder value at pytest runtime."""
    # step 1
    def _mock_joke():
        """Return the joke text.

        monkeypatch.setattr expects the value argument to be callable. In plain
        English, a function or class."""
        return ULTI_JOKE
    # step 2
    monkeypatch.setattr(
        target=example_pkg.only_joking,
        name="get_joke",
        value=_mock_joke
        )
    # step 3 & 4
    # Use the module's namespace to correspond with the monkeypatch
    assert example_pkg.only_joking.get_joke() == ULTI_JOKE 


def test_get_joke_monkeypatched_no_OOP(monkeypatch, ULTI_JOKE):
    # step 1: Mock the response object
    def mock_response(*args, **kwargs):
        resp = requests.models.Response()
        resp.status_code = 200
        resp._content = ULTI_JOKE.encode("UTF8")
        resp.headers = {"Content-Type": "text/plain"}
        return resp
    
    # step 2: Patch requests.get
    monkeypatch.setattr(requests, "get", mock_response)
    # step 3: Use requests.get
    joke = get_joke()
    # step 4: Assert
    assert joke == ULTI_JOKE, f"Expected:\n'{ULTI_JOKE}\nFound:\n{joke}'"
    # will also work for json format
    joke = get_joke(f="application/json")
    assert joke == ULTI_JOKE, f"Expected:\n'{ULTI_JOKE}\nFound:\n{joke}'"


## Docs solution


@pytest.fixture
def _mock_response(ULTI_JOKE):
    """Return a class instance that will mock all the properties of a response
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


def test_get_joke_json_monkeypatched(monkeypatch, _mock_response, ULTI_JOKE):
    """Test behaviour when user asked for JSON joke.

    Test get_joke using the mock class fixture. This approach is the
    implementation suggested in the pytest docs.
    """
    # step 1: Mock
    def _mock_get_good_resp(*args, **kwargs):
        """Return fixtures with the correct header.

        If the test uses "text/plain" format, we need to return a MockResponse
        class instance with headers attribute equal to
        {"Content-Type": "text/plain"}, likewise for JSON.
        """
        f = kwargs["headers"]["Accept"]
        return _mock_response(f)
    # Step 2: Patch
    monkeypatch.setattr(requests, "get", _mock_get_good_resp)
    # Step 3: Use
    j_json = get_joke(f="application/json")
    # Step 4: Assert
    assert j_json == ULTI_JOKE, f"Expected:\n'{ULTI_JOKE}\nFound:\n{j_json}'"


def test_get_joke_text_monkeypatched(monkeypatch, _mock_response, ULTI_JOKE):
    """Test behaviour when user asked for plain text joke."""
    # step 1: Mock
    def _mock_get_good_resp(*args, **kwargs):
        f = kwargs["headers"]["Accept"]
        return _mock_response(f)
    # step 2: Patch
    monkeypatch.setattr(requests, "get", _mock_get_good_resp)
    # step 3: Use
    j_txt = get_joke(f="text/plain")
    # step 4: Assert
    assert j_txt == ULTI_JOKE, f"Expected:\n'{ULTI_JOKE}\nFound:\n{j_txt}'"


def test_get_joke_not_implemented_monkeypatched(
    monkeypatch, _mock_response):
    """Test behaviour when user asked for HTML response."""
    #  step 1: Mock
    def _mock_get_good_resp(*args, **kwargs):
        f = kwargs["headers"]["Accept"]
        return _mock_response(f)
    # step 2: Patch
    monkeypatch.setattr(requests, "get", _mock_get_good_resp)
    # step 3 & 4 Use (try to but exception is raised) & Assert
    with pytest.raises(
        NotImplementedError,
        match="This client accepts 'application/json' or 'text/plain' format"):
        get_joke(f="text/html")



@pytest.fixture
def _mock_bad_response():
    class MockBadResponse:
        def __init__(self, *args, **kwargs):
            self.ok = False
            self.status_code = 404
            self.reason = "Not Found"
    return MockBadResponse


def test_get_joke_http_error_monkeypatched(
    monkeypatch, _mock_bad_response):
    """Test bad HTTP response."""
    #  step 1: Mock
    def _mock_get_bad_response(*args, **kwargs):
        f = kwargs["headers"]["Accept"]
        return _mock_bad_response(f)
    #  step 2: Patch
    monkeypatch.setattr(requests, "get", _mock_get_bad_response)
    # step 3 & 4 Use (try to but exception is raised) & Assert
    with pytest.raises(requests.HTTPError, match="404: Not Found"):
        get_joke()
