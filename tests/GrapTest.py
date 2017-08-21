import unittest
from Grap import Grap


class TestGrapMethods(unittest.TestCase):

    # Testing Multiple Pattern Input as Logical OR
    def test_produce_regex_of_multiple_inputs(self):
        self.grep = Grap()
        input = ["foo %{0} is a %{1}", "the %{0S1} %{1} ran away", "bar %{0G} foo %{1}"]
        expected_output = "(foo (.+?) is a (.+?)(\\n|$)|the ((\w+?) (\w+?)) (.+?) ran away(\\n|$)|bar (.+) foo (.+?)(\\n|$))"
        self.assertEqual(self.grep.translate_multiple_patterns(input), expected_output)

    def test_multiple_inputs_act_as_logical_OR_matching_third_input(self):
        self.grep = Grap()
        input = ["foo %{0} is a %{1}", "the %{0S1} %{1} ran away", "bar %{0G} foo %{1}"]
        regex = self.grep.translate_multiple_patterns(input)
        test = "bar foo bar foo bar foo bar foo"
        self.assertTrue(self.grep.pattern_and_token_match(regex, test))

    def test_multiple_inputs_act_as_logical_or_matching_second_input(self):
        self.grep = Grap()
        input = ["foo %{0} is a %{1}", "the %{0S1} %{1} ran away", "bar %{0G} foo %{1}"]
        regex = self.grep.translate_multiple_patterns(input)
        test = "the big brown fox ran away"
        self.assertTrue(self.grep.pattern_and_token_match(regex, test))

    def test_multiple_inputs_act_as_logical_or_matching_first_input(self):
        self.grep = Grap()
        input = ["foo %{0} is a %{1}", "the %{0S1} %{1} ran away", "bar %{0G} foo %{1}"]
        regex = self.grep.translate_multiple_patterns(input)
        test = "foo bar is a very big boat"
        self.assertTrue(self.grep.pattern_and_token_match(regex, test))

    def test_multiple_inputs_act_as_logical_or_should_fail_if_none_match(self):
        self.grep = Grap()
        input = ["foo %{0} is a %{1}", "the %{0S1} %{1} ran away", "bar %{0G} foo %{1}"]
        regex = self.grep.translate_multiple_patterns(input)
        test = "this definitely does not match"
        self.assertFalse(self.grep.pattern_and_token_match(regex, test))

    # Testing Matches
    # Simple Tokens
    # Positive Match
    def test_matching_with_simple_tokens(self):
        self.grep = Grap()
        pattern = self.grep.translate_to_regex("foo %{0} is a %{1}")
        print(pattern)
        self.assertTrue(self.grep.pattern_and_token_match(pattern, "foo blah is a bar"))

    def test_matching_with_simple_tokens_longer_string(self):
        self.grep = Grap()
        pattern = self.grep.translate_to_regex("foo %{0} is a %{1}")
        self.assertTrue(self.grep.pattern_and_token_match(pattern, "foo blah is a very big boat"))

    # Negative Match
    def test_matching_with_simple_tokens_should_not_match_one(self):
        self.grep = Grap()
        pattern = self.grep.translate_to_regex("foo %{0} is a %{1}")
        self.assertFalse(self.grep.pattern_and_token_match(pattern, "foo blah is bar"))

    def test_matching_with_simple_tokens_should_not_match_two(self):
        self.grep = Grap()
        pattern = self.grep.translate_to_regex("foo %{0} is a %{1}")
        self.assertFalse(self.grep.pattern_and_token_match(pattern, "foo blah is"))

    def test_matching_with_simple_tokens_should_not_match_three(self):
        self.grep = Grap()
        pattern = self.grep.translate_to_regex("foo %{0} is a %{1}")
        self.assertFalse(self.grep.pattern_and_token_match(pattern, "foo blah"))

    # Space Limited Token
    # Positive Match
    def test_matching_with_space_limited_tokens(self):
        self.grep = Grap()
        pattern = self.grep.translate_to_regex("the %{0S1} %{1} ran away")
        self.assertTrue(self.grep.pattern_and_token_match(pattern, "the big brown fox ran away"))

    def test_matching_with_space_limited_tokens(self):
        self.grep = Grap()
        pattern = self.grep.translate_to_regex("foo %{0} is a %{1S0}")
        self.assertTrue(self.grep.pattern_and_token_match(pattern, "foo blah is a bar"))

    # Negative Match
    def test_matching_with_space_limited_tokens_should_not_match_one(self):
        self.grep = Grap()
        pattern = self.grep.translate_to_regex("foo %{0} is a %{1S0}")
        self.assertFalse(self.grep.pattern_and_token_match(pattern, "foo blah is a very big boat"))

    def test_matching_with_space_limited_tokens_should_not_match_two(self):
        self.grep = Grap()
        pattern = self.grep.translate_to_regex("foo %{0} is a %{1S0}")
        self.assertFalse(self.grep.pattern_and_token_match(pattern, "foo blah is bar"))

    def test_matching_with_space_limited_tokens_should_not_match_three(self):
        self.grep = Grap()
        pattern = self.grep.translate_to_regex("foo %{0} is a %{1S0}")
        self.assertFalse(self.grep.pattern_and_token_match(pattern, "foo blah is"))

    def test_matching_with_space_limited_tokens_should_not_match_four(self):
        self.grep = Grap()
        pattern = self.grep.translate_to_regex("foo %{0} is a %{1S0}")
        self.assertFalse(self.grep.pattern_and_token_match(pattern, "foo blah"))

    # Greedy Tokens
    # Positive Match
    def test_matching_with_simple_tokens(self):
        self.grep = Grap()
        pattern = self.grep.translate_to_regex("bar %{0G} foo %{1}")
        self.assertTrue(self.grep.pattern_and_token_match(pattern, "bar foo bar foo bar foo bar foo"))

    # Testing Translation from Pattern to Regex
    # Greedy Pattern
    def test_translate_to_pattern_should_interpolate_greedy_regex(self):
        self.grep = Grap()
        self.assertEqual(self.grep.translate_to_regex("foo %{0} is a %{1G}"), "foo (.+?) is a (.+)(\\n|$)")

    def test_translate_to_pattern_should_interpolate_space_limited(self):
        self.grep = Grap()
        self.assertEqual(self.grep.translate_to_regex("foo %{0} is a %{1S2}"), "foo (.+?) is a ((\w+?) (\w+?) (\w+?))(\\n|$)")

    def test_translate_pattern_to_regex(self):
        self.grep = Grap()
        self.assertEqual(self.grep.translate_to_regex("foo %{0} is a %{1}"), "foo (.+?) is a (.+?)(\\n|$)")

    def test_to_token_should_return_word_if_word_is_not_token(self):
        self.grep = Grap()
        self.assertEqual(self.grep.token_to_regex("foo"), "foo")

    # Standard Tokens
    def test_to_token_should_return_standard_token_regex_if_word_is_standard_token(self):
        self.grep = Grap()
        self.assertEqual(self.grep.token_to_regex("%{0}"), "(.+?)")

    def test_to_token_should_return_standard_token_regex_if_word_is_standard_token(self):
        self.grep = Grap()
        self.assertEqual(self.grep.token_to_regex("%{0}"), "(.+?)")

    def test_to_token_should_return_return_token_if_index_is_not_consecutive_starting_at_zero(self):
        self.grep = Grap()
        self.assertEqual(self.grep.token_to_regex("%{1}"), "%{1}")

    def test_to_token_should_return_fail_if_index_is_different_than_expected(self):
        self.grep = Grap()
        self.assertEqual(self.grep.token_to_regex("%{1}"), "%{1}")


    # Testing Regex for Token Shapes/Pattern
    # Simple/Standard Token Shape
    def test_token_match_simple_token_to_simple_token(self):
        self.grep = Grap()
        self.assertTrue(self.grep.pattern_and_token_match(self.grep.simple_token_shape, "%{0}"))

    def test_token_match_simple_token_to_simple_token_with_two_digit_index(self):
        self.grep = Grap()
        self.assertTrue(self.grep.pattern_and_token_match(self.grep.simple_token_shape, "%{99}"))

    def test_token_match_simple_should_not_match_any_other_pattern(self):
        self.grep = Grap()
        self.assertFalse(self.grep.pattern_and_token_match(self.grep.simple_token_shape, "%{99G}"))

    # Greedy Token Shape
    def test_token_match_greedy_token_with_single_digit(self):
        self.grep = Grap()
        self.assertTrue(self.grep.pattern_and_token_match(self.grep.greedy_token_shape, "%{0G}"))

    def test_token_match_greedy_token_with_two_digits(self):
        self.grep = Grap()
        self.assertTrue(self.grep.pattern_and_token_match(self.grep.greedy_token_shape, "%{99G}"))

    def test_token_match_greedy_token_should_not_match_other_pattern(self):
        self.grep = Grap()
        self.assertFalse(self.grep.pattern_and_token_match(self.grep.greedy_token_shape, "%{99}"))


    # Testing Token Processing
    # Standard Token
    def test_process_standard_token_should_return_regex_of_standard_token(self):
        self.grep = Grap()
        self.assertEqual(self.grep.process_standard_token("%{0}"), self.grep.simple_token_regex)

    def test_process_standard_token_should_return_token_if_index_not_consecutive_starting_at_zero(self):
        self.grep = Grap()
        self.assertEqual(self.grep.process_standard_token("%{1}"), "%{1}")

    # Greedy Token
    def test_process_greedy_token_return_regex_of_greedy_token(self):
        self.grep = Grap()
        self.assertEqual(self.grep.process_greedy_token("%{0G}"), self.grep.greedy_token_regex)

    def test_process_greedy_token_should_fail_if_index_not_consecutive_starting_at_zero(self):
        self.grep = Grap()
        self.assertEqual(self.grep.process_greedy_token("%{1G}"), "%{1G}")

    # Space Limited Token
    def test_generate_space_limited_regex_should_return_regex_defined_number_of_spaces(self):
        self.grep = Grap()
        self.assertEqual(self.grep.generate_space_limited_regex(3), "((\w+?) (\w+?) (\w+?) (\w+?))")

    def test_generate_space_limited_regex_should_return_simple_token_when_given_zero(self):
        self.grep = Grap()
        self.assertEqual(self.grep.generate_space_limited_regex(0), "((\w+?))")

    def test_generate_space_limited_regex_should_return_simple_token_twice_with_space_between_when_given_one(self):
        self.grep = Grap()
        self.assertEqual(self.grep.generate_space_limited_regex(1), "((\w+?) (\w+?))")

    def test_process_space_limited_token_should_return_token_if_index_not_consecutive_starting_at_zero(self):
        self.grep = Grap()
        self.assertEqual(self.grep.process_space_limited_token("%{1S1}"), "%{1S1}")

    def test_process_space_limited_token_should_return_number_of_spaces_given_after_S(self):
        self.grep = Grap()
        self.assertEqual(self.grep.process_space_limited_token("%{0S1}"), "((\w+?) (\w+?))")

if __name__ == '__main__':
    unittest.main()