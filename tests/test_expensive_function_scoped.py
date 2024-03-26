"""Tests for expensive.py using function-scoped fixture."""
from contextlib import nullcontext as does_not_raise
import pytest

from example_pkg.expensive import ExpensiveDoodah


@pytest.fixture(scope="function")
def module_doodah():
    """Function-scoped ExpensiveDoodah."""
    return ExpensiveDoodah(2)


class TestA:
    """A test class."""

    def test_1(self, module_doodah):
        """Test 1."""
        with does_not_raise():
            module_doodah

    def test_2(self, module_doodah):
        """Test 2."""
        with does_not_raise():
            module_doodah

    def test_3(self, module_doodah):
        """Test 3."""
        with does_not_raise():
            module_doodah
