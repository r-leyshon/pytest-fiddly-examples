"""Tests for primes module."""
import pytest

from example_pkg.primes import is_num_prime, sum_if_prime


def test_is_num_primes_exceptions_manually():
    """Testing the function's defensive checks.

    Here we have to repeat a fair bit of pytest boilerplate.
    """
    with pytest.raises(TypeError, match="must be a positive integer."):
        is_num_prime(1.0)
    with pytest.raises(ValueError, match="must be a positive integer."):
        is_num_prime(-1)


@pytest.mark.parametrize(
    "some_integers, exception_types", [(1.0, TypeError), (-1, ValueError)]
    )
def test_is_num_primes_exceptions_parametrized(some_integers, exception_types):
    """The same defensive checks but this time with parametrized input.

    Less lines in the test but if we increase the number of cases, we need to
    add more lines to the parametrized fixture instead.
    """
    with pytest.raises(exception_types, match="must be a positive integer."):
        is_num_prime(some_integers)


def test_is_num_primes_manually():
    """Test several positive integers return expected boolean.

    This is quite a few lines of code. Note that this runs as a single test.
    """
    assert is_num_prime(1) == False
    assert is_num_prime(2) == True
    assert is_num_prime(3) == True
    assert is_num_prime(4) == False
    assert is_num_prime(5) == True


def test_is_num_primes_with_list():
    """Test the same values using lists.

    Less lines but is run as a single test.
    """
    answers = [is_num_prime(i) for i in range(1, 6)]
    assert answers == [False, True, True, False, True]


@pytest.mark.parametrize(
    "some_integers, answers",
    [(1, False), (2, True), (3, True), (4, False), (5, True)]
    )
def test_is_num_primes_parametrized(some_integers, answers):
    """The same tests but this time with parametrized input.

    Fewer lines and 5 seperate tests are run by pytest.
    """
    assert is_num_prime(some_integers) == answers


# if my list of cases is growing, I can employ other tactics to reduce
# complexity
in_ = range(1, 21)
out = [
    False, True, True, False, True, False, True, False, False, False,
    True, False, True, False, False, False, True, False, True, False,
    ]


@pytest.mark.parametrize("some_integers, some_answers", zip(in_, out))
def test_is_num_primes_with_parametrized_lists(some_integers, some_answers):
    """The same tests but this time with zipped inputs."""
    assert is_num_prime(some_integers) == some_answers


def test_sum_if_prime_with_manual_combinations():
    """Manually check several cases."""
    assert sum_if_prime(1, 1) == (1, 1)
    assert sum_if_prime(1, 2) == (1, 2)
    assert sum_if_prime(1, 3) == (1, 3)
    assert sum_if_prime(1, 4) == (1, 4)
    assert sum_if_prime(1, 5) == (1, 5)
    assert sum_if_prime(2, 1) == (2, 1)
    assert sum_if_prime(2, 2) == (4,) # the first case where both are primes
    assert sum_if_prime(2, 3) == (5,) 
    assert sum_if_prime(2, 4) == (2, 4)
    assert sum_if_prime(2, 5) == (7,)
    # ...


# Using stacked parametrization, we can avoid manually typing the cases out,
# though we do still need to define a dictionary of the expected answers...
@pytest.fixture
def expected_answers() -> dict:
    """A dictionary of expected answers for all combinations of 1 through 5.

    First key corresponds to `pos_int1` and second key is `pos_int2`.

    Returns
    -------
    dict
        Dictionary of cases and their expected tuples.
    """
    expected= {
        1: {1: (1,1), 2: (1,2), 3: (1,3), 4: (1,4), 5: (1,5),},
        2: {1: (2,1), 2: (4,), 3: (5,), 4: (2,4), 5: (7,),},
        3: {1: (3,1), 2: (5,), 3: (6,), 4: (3,4), 5: (8,),},
        4: {1: (4,1), 2: (4,2), 3: (4,3), 4: (4,4), 5: (4,5),},
        5: {1: (5,1), 2: (7,), 3: (8,), 4: (5,4), 5: (10,),},
    }
    return expected


@pytest.mark.parametrize("first_ints", range(1,6))
@pytest.mark.parametrize("second_ints", range(1,6))
def test_sum_if_prime_stacked_parametrized_inputs(
    first_ints, second_ints, expected_answers):
    """Using stacked parameters to set up combinations of all cases."""
    assert isinstance(sum_if_prime(first_ints, second_ints), tuple)
    answer = sum_if_prime(first_ints, second_ints)
    # using the parametrized values, pull out their keys from the
    # expected_answers dictionary
    assert answer == expected_answers[first_ints][second_ints]
