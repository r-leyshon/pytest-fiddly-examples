"""Checking integers for prime numbers."""


def is_num_prime(pos_int: int) -> bool:
    """Check if a positive integer is a prime number.

    Parameters
    ----------
    pos_int : int
        A positive integer.

    Returns
    -------
    bool
        True if the number is a prime number.

    Raises
    ------
    TypeError
        Value passed to `pos_int` is not an integer.
    ValueError
        Value passed to `pos_int` is less than or equal to 0.
    """
    if not isinstance(pos_int, int):
        raise TypeError("`pos_int` must be a positive integer.")
    if pos_int <= 0:
        raise ValueError("`pos_int` must be a positive integer.")
    elif pos_int == 1:
        return False
    else:
        for i in range(2, (pos_int // 2) + 1):
            # If divisible by any number 2<>n/2, it is not prime
            if (pos_int % i) == 0:
                return False
        else:
            return True


if __name__ == "__main__":
    for i in range(1, 101):
        print(f"{i}: {is_num_prime(i)}")
