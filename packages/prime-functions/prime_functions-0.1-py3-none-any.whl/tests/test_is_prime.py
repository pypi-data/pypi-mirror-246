"""
This module contains test cases for is_prime function
"""


import unittest
from prime_functions import is_prime


class IsPrimeTest(unittest.TestCase):
    """This class contains test cases for is_prime function"""

    def setUp(self):
        self.prime_number = 97
        self.non_prime_number = 20

    def tearDown(self):
        self.prime_number = 0
        self.non_prime_number = 0

    def test_prime_number(self):
        """This function checks if a number is prime or not"""
        # Act
        result = is_prime(self.prime_number)

        # Assert
        self.assertEqual(result, True)

    def test_non_prime_number(self):
        """This function checks if a number is non prime or not"""
        # Act
        result = is_prime(self.non_prime_number)

        # Assert
        self.assertEqual(result, False)


if __name__ == "__main__":
    unittest.main()
