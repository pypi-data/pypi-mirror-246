"""
This module contains test cases for prime factors of number
"""


import unittest
from prime_functions import all_prime_factors

class PrimeFactorsTest(unittest.TestCase):
    """This class contains test cases for prime factors of number"""

    def setUp(self):
        self.num = 48

    def tearDown(self):
        self.num = 0

    def test_prime_factors(self):
        """This function checks prime factors of given number"""
        # Act
        result = all_prime_factors(self.num)
        print(result)
        # Assert
        self.assertEqual(result, {2:4, 3:1})



if __name__ == "__main__":
    unittest.main()
