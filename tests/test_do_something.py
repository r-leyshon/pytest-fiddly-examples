import pytest

from example_pkg.do_something import (
    croissant,
    take_a_nap,
    check_site_available,
    goofy_wrapper
    )


def test_nothing():
    pass


@pytest.mark.flaky
def test_croissant():
    assert croissant()


@pytest.mark.slow
def test_take_a_nap():
    out = take_a_nap(how_many_seconds=3)
    assert isinstance(out, str), f"a string was not returned: {type(out)}"
    assert out == "Rise and shine!", f"unexpected string pattern: {out}"


@pytest.mark.integration
def test_check_site_available():
    url = "https://thedatasavvycorner.com/"
    assert check_site_available(url), f"site {url} is down..."


@pytest.mark.integration
@pytest.mark.classy
class TestGoofyWrapper:
    @pytest.mark.subclassy
    def test_goofy_wrapper_url_exists(self):
        assert goofy_wrapper(
            "https://thedatasavvycorner.com/", 1
            ).endswith("Your site is up!"),"The site wasn't up."
    @pytest.mark.subclassy
    def test_goofy_wrapper_url_does_not_exist(self):
        assert goofy_wrapper(
            "https://thegoofycorner.com/", 1
            ).endswith("Your site is down!"), "The site wasn't down."
