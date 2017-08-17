import unittest
from Grepper import Grepper


class TestGrepperMethods(unittest.TestCase):

    def test_space_limited_regex_with_zero(self):
        self.grep = Grepper()
        self.assertEqual(self.grep.space_limited_regex(0), "(.+)")

    def test_space_limited_regex_with_greater_than_zero(self):
        self.grep = Grepper()
        self.assertEqual(self.grep.space_limited_regex(3), "(.+ .+ .+ .+)")

    def test_replace_standard_token(self):
        self.grep = Grepper()
        self.assertEqual(self.grep.replace_standard_tokens("foo %{0} is a %{1}"), "foo (.+) is a (.+)")
if __name__ == '__main__':
    unittest.main()