"""
This module find prime factors of a positive integer
"""


def all_prime_factors(num) -> dict:
    """This function return prime factors of a number

    Args:
        num (_type_): integer number

    Raises:
        TypeError: if num is not an integer
        valueError: if num is negative

    Returns:
        _type_: returns dictionary of prime factors

    Examples:
        >>> prime_factors(7)
        {7:1}
        >>> prime_factors(8)
        {2:3}
    """
    factors = {}
    try:
        if num < 0:
            raise ValueError("Number must be positive")
        if not isinstance(num, int):
            raise TypeError("Number must be an integer")

        while 0 == num % 2:
            factors[2] = factors.get(2, 0) + 1
            num = num // 2

        while 0 == num % 3:
            factors[3] = factors.get(3, 0) + 1
            num = num // 3

        i = 5
        while i * i <= num:
            while 0 == num % i:
                factors[i] = factors.get(i, 0) + 1
                num = num // i
            while 0 == num % (i + 2):
                factors[i + 2] = factors.get(i + 2, 0) + 1
                num = num // (i + 2)
            i = i + 6

        if num > 3:
            factors[num] = factors.get(num, 0) + 1

    except TypeError:
        print("Number should be an integer only!!")
    except ValueError:
        print("Number should be positive integer only!!")

    return factors
