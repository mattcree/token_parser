import unittest
from Grepper import Grepper


class TestGrepperMethods(unittest.TestCase):

    def test_space_limited_regex_with_zero(self):
        self.grep = Grepper()
        self.assertEqual(self.grep.space_limited_regex(0), "\w+?")

    def test_space_limited_regex_with_greater_than_zero(self):
        self.grep = Grepper()
        self.assertEqual(self.grep.space_limited_regex(3), "\w+? \w+? \w+? \w+?")


if __name__ == '__main__':
    unittest.main()