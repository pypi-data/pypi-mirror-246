"""
This module check whether a number is prime or not
"""


def is_prime(num) -> bool:
    """This function checks if a number is prime or not

    Args:
        num (_type_): integer number to be checked for primality

    Raises:
        TypeError: if num is not an integer
        valueError: if num is negative

    Returns:
        _type_: returns True if number is prime else False

    Examples:
        >>> is_prime(7)
        True
        >>> is_prime(8)
        False
    """

    try:
        if num < 0:
            raise ValueError("Number must be positive")
        if not isinstance(num, int):
            raise TypeError("Number must be an integer")

        if num < 2:
            return False
        i = 2
        while i * i <= num:
            if num % i == 0:
                return False
            i += 1
    except TypeError:
        print("Number should be an integer only!!")
    except ValueError:
        print("Number should be positive integer only!!")

    return True
