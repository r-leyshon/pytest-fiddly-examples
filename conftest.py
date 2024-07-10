import pytest


@pytest.fixture(scope="session")
def ULTI_JOKE():
    return ("Doc, I can't stop singing 'The Green, Green Grass of Home.' That "
    "sounds like Tom Jones Syndrome. Is it common? Well, It's Not Unusual.")
    