"""Demonstrate scoping fixtures."""
import pandas as pd
import pytest

@pytest.fixture(scope="session")
def mystery_machine():
    
     return pd.DataFrame({
        "name": ["Daphne", "Fred", "Scooby Doo", "Shaggy", "Velma"],
        "fave_food": ["carrots", "beans", "scooby snacks", "burgers", "hot dogs"],
        "has_munchies": [True] * 5,
        "stomach_contents": ["empty"] * 5,
    })


@pytest.fixture(scope="session")
def mm_session_scoped(mystery_machine):
    return mystery_machine


@pytest.fixture(scope="module")
def mm_module_scoped(mystery_machine):
    return mystery_machine


@pytest.fixture(scope="class")
def mm_class_scoped(mystery_machine):
    return mystery_machine


@pytest.fixture(scope="function")
def mm_function_scoped(mystery_machine):
    return mystery_machine
