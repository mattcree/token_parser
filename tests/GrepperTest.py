import unittest
from Grepper import Grepper


class TestGrepperMethods(unittest.TestCase):

    #Testing Regex Patterns

    def test_token_match_any_token_simple(self):
        self.grep = Grepper()
        self.assertTrue(self.grep.token_match(self.grep.any_token_shape, "%{0}"))

    def test_token_match_any_token_greedy(self):
        self.grep = Grepper()
        self.assertTrue(self.grep.token_match(self.grep.any_token_shape, "%{0G}"))

    def test_token_match_any_token_space_limited(self):
        self.grep = Grepper()
        self.assertTrue(self.grep.token_match(self.grep.any_token_shape, "%{0S3}"))

    def test_token_match_will_not_match_any_ther_pattern(self):
        self.grep = Grepper()
        self.assertFalse(self.grep.token_match(self.grep.any_token_shape, "%{0S3"))

    def test_token_match_simple_token_to_simple_token(self):
        self.grep = Grepper()
        self.assertTrue(self.grep.token_match(self.grep.simple_token_shape, "%{0}"))

    def test_token_match_simple_token_to_simple_token_with_two_digit_index(self):
        self.grep = Grepper()
        self.assertTrue(self.grep.token_match(self.grep.simple_token_shape, "%{99}"))

    def test_token_match_simple_should_not_match_any_other_pattern(self):
        self.grep = Grepper()
        self.assertFalse(self.grep.token_match(self.grep.simple_token_shape, "%{99G}"))

    def test_token_match_greedy_token_with_single_digit(self):
        self.grep = Grepper()
        self.assertTrue(self.grep.token_match(self.grep.greedy_token_shape, "%{0G}"))

    def test_token_match_greedy_token_with_two_digits(self):
        self.grep = Grepper()
        self.assertTrue(self.grep.token_match(self.grep.greedy_token_shape, "%{99G}"))

    def test_token_match_greedy_token_should_not_match_other_pattern(self):
        self.grep = Grepper()
        self.assertFalse(self.grep.token_match(self.grep.greedy_token_shape, "%{99}"))


    #Testing Token Processing

    def test_process_standard_token_should_return_regex_of_standard_token(self):
        self.grep = Grepper()
        self.assertEqual(self.grep.process_standard_token("%{99}", 99), self.grep.simple_token_regex)

    def test_process_standard_token_should_fail_if_number_different_from_index(self):
        self.grep = Grepper()
        self.assertEqual(self.grep.process_standard_token("%{99}", 15), EOFError)

    def test_process_greedy_token_return_regex_of_greedy_token(self):
        self.grep = Grepper()
        self.assertEqual(self.grep.process_greedy_token("%{15G}", 15), self.grep.greedy_token_regex)

    def test_process_greedy_token_should_fail_if_number_different_from_index(self):
        self.grep = Grepper()
        self.assertEqual(self.grep.process_greedy_token("%{15G}", 5), EOFError)

    def test_process_space_limited_token_should_return_regex_of_space_limited_token(self):
        self.grep = Grepper()
        self.assertEqual(self.grep.process_space_limited_token("%{15S34}", 5), EOFError)

if __name__ == '__main__':
    unittest.main()