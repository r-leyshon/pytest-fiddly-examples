"""Demonstrate scoping fixtures."""
import pandas as pd
import pytest


@pytest.fixture(scope="session")
def _mystery_machine():
    """Session-scoped fixture returning pandas dataframe."""
    return pd.DataFrame(
        {
            "name": ["Daphne", "Fred", "Scooby Doo", "Shaggy", "Velma"],
            "fave_food": [
                "carrots",
                "beans",
                "scooby snacks",
                "burgers",
                "hot dogs",
            ],
            "has_munchies": [True] * 5,
            "stomach_contents": ["empty"] * 5,
        }
    )


@pytest.fixture(scope="session")
def _mm_session_scoped(_mystery_machine):
    """Session-scoped fixture returning the _mystery_machine dataframe.

    As the src functions update their input df inplace, _mm_session_scoped will
    be modified instead of _mystery_machine directly.

    """
    return _mystery_machine.copy(deep=True)


@pytest.fixture(scope="module")
def _mm_module_scoped(_mystery_machine):
    """Module-scoped _mystery_machine dataframe."""
    return _mystery_machine.copy(deep=True)


@pytest.fixture(scope="class")
def _mm_class_scoped(_mystery_machine):
    """Class-scoped _mystery_machine dataframe."""
    return _mystery_machine.copy(deep=True)


@pytest.fixture(scope="function")
def _mm_function_scoped(_mystery_machine):
    """Function-scoped _mystery_machine dataframe."""
    return _mystery_machine.copy(deep=True)
