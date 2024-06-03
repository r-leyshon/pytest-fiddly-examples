"""Tests for primes module."""
import pytest

from example_pkg.primes import is_num_prime


def test_is_num_primes_manually():
    assert is_num_prime(1) == False
    assert is_num_prime(2) == True
    assert is_num_prime(3) == True
    assert is_num_prime(4) == False
    assert is_num_prime(5) == True


@pytest.mark.parametrize(
    "some_integers, answers",
    [(1, False), (2, True), (3, True), (4, False), (5, True)]
    )
def test_is_num_primes_with_parametrized(some_integers, answers):
    assert is_num_prime(some_integers) == answers


def test_is_num_primes_with_list():
    answers = [is_num_prime(i) for i in range(1, 6)]
    assert answers == [False, True, True, False, True]


def test_is_num_primes_exceptions_manually():
    with pytest.raises(TypeError, match="must be a positive integer."):
        is_num_prime(1.0)
    with pytest.raises(ValueError, match="must be a positive integer."):
        is_num_prime(-1)


@pytest.mark.parametrize(
    "some_integers, exception_types",
    [(1.0, TypeError), (-1, ValueError)]
    )
def test_is_num_primes_exceptions_parametrized(some_integers, exception_types):
    with pytest.raises(exception_types, match="must be a positive integer."):
        is_num_prime(some_integers)
