import unittest, grap
from grap import Grap


class TestGrapMethods(unittest.TestCase):

    # Testing Multiple Pattern Input as Logical OR
    def test_produce_regex_of_multiple_inputs_should_allow_multiple_patterns_to_be_processed_by_same_instance(self):
        self.grep = Grap()
        input = ["foo %{0} is a %{1}", "the %{0S1} %{1} ran away", "bar %{0G} foo %{1}"]
        expected_output = "(foo (.+?) is a (.+?)(\\n|$)|the ((\w+?) (\w+?)) (.+?) ran away(\\n|$)|bar (.+) foo (.+?)(\\n|$))"
        self.assertEqual(self.grep.translate_multiple_patterns(input), expected_output)

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

    # Testing Translation Matches
    # Standard Tokens
    # Positive Match
    def test_translation_with_standard_tokens(self):
        self.grep = Grap()
        pattern = self.grep.translate_to_regex("foo %{0} is a %{1}")
        self.assertTrue(self.grep.pattern_and_token_match(pattern, "foo blah is a bar"))

    def test_translation_with_standard_tokens_longer_string(self):
        self.grep = Grap()
        pattern = self.grep.translate_to_regex("foo %{0} is a %{1}")
        self.assertTrue(self.grep.pattern_and_token_match(pattern, "foo blah is a very big boat"))

    # Negative Match
    def test_translation_with_standard_tokens_should_not_match_one(self):
        self.grep = Grap()
        pattern = self.grep.translate_to_regex("foo %{0} is a %{1}")
        self.assertFalse(self.grep.pattern_and_token_match(pattern, "foo blah is bar"))

    def test_translation_with_standard_tokens_should_not_match_two(self):
        self.grep = Grap()
        pattern = self.grep.translate_to_regex("foo %{0} is a %{1}")
        self.assertFalse(self.grep.pattern_and_token_match(pattern, "foo blah is"))

    def test_translation_with_standard_tokens_should_not_match_three(self):
        self.grep = Grap()
        pattern = self.grep.translate_to_regex("foo %{0} is a %{1}")
        self.assertFalse(self.grep.pattern_and_token_match(pattern, "foo blah"))

    #Malformed Token
    def test_translation_with_standard_tokens_should_not_match_similar_to_token(self):
        self.grep = Grap()
        pattern = self.grep.translate_to_regex("foo %{0} is a %{1}%")
        self.assertFalse(self.grep.pattern_and_token_match(pattern, "foo bar is a bed"))

    # Space Limited Token
    # Positive Match
    def test_translation_with_space_limited_tokens(self):
        self.grep = Grap()
        pattern = self.grep.translate_to_regex("the %{0S1} %{1} ran away")
        self.assertTrue(self.grep.pattern_and_token_match(pattern, "the big brown fox ran away"))

    def test_translation_with_space_limited_tokens(self):
        self.grep = Grap()
        pattern = self.grep.translate_to_regex("foo %{0} is a %{1S0}")
        self.assertTrue(self.grep.pattern_and_token_match(pattern, "foo blah is a bar"))

    # Negative Match
    def test_translation_with_space_limited_tokens_should_not_match_one(self):
        self.grep = Grap()
        pattern = self.grep.translate_to_regex("foo %{0} is a %{1S0}")
        self.assertFalse(self.grep.pattern_and_token_match(pattern, "foo blah is a very big boat"))

    def test_translation_with_space_limited_tokens_should_not_match_two(self):
        self.grep = Grap()
        pattern = self.grep.translate_to_regex("foo %{0} is a %{1S0}")
        self.assertFalse(self.grep.pattern_and_token_match(pattern, "foo blah is bar"))

    def test_translation_with_space_limited_tokens_should_not_match_three(self):
        self.grep = Grap()
        pattern = self.grep.translate_to_regex("foo %{0} is a %{1S0}")
        self.assertFalse(self.grep.pattern_and_token_match(pattern, "foo blah is"))

    def test_translation_with_space_limited_tokens_should_not_match_four(self):
        self.grep = Grap()
        pattern = self.grep.translate_to_regex("foo %{0} is a %{1S0}")
        self.assertFalse(self.grep.pattern_and_token_match(pattern, "foo blah"))

    # Malformed Token
    def test_translation_with_space_limited_tokens_should_not_match_similar_to_token(self):
        self.grep = Grap()
        pattern = self.grep.translate_to_regex("foo %{0} is %{1S1}%")
        self.assertFalse(self.grep.pattern_and_token_match(pattern, "foo bar is a bed"))

    # Greedy Tokens
    # Positive Match
    def test_translation_with_greedy_token(self):
        self.grep = Grap()
        pattern = self.grep.translate_to_regex("bar %{0G} foo %{1}")
        self.assertTrue(self.grep.pattern_and_token_match(pattern, "bar foo bar foo bar foo bar foo"))

    # Negative Match
    def test_translation_with_greedy_tokens_should_not_match(self):
        self.grep = Grap()
        pattern = self.grep.translate_to_regex(" %{0G}")
        self.assertFalse(self.grep.pattern_and_token_match(pattern, "space"))

    # Malformed Token
    def test_translation_with_greedy_tokens_should_not_match_similar_to_token(self):
        self.grep = Grap()
        pattern = self.grep.translate_to_regex("foo %{0} is %{1G1}%")
        self.assertFalse(self.grep.pattern_and_token_match(pattern, "foo bar is a big bed"))

    # Testing Translation Produces Expected Output
    def test_translation_to_pattern_with_greedy_token(self):
        self.grep = Grap()
        self.assertEqual(self.grep.translate_to_regex("foo %{0} is a %{1G}"), "foo (.+?) is a (.+)(\\n|$)")

    def test_translation_to_pattern_with_space_limited_token(self):
        self.grep = Grap()
        self.assertEqual(self.grep.translate_to_regex("foo %{0} is a %{1S2}"), "foo (.+?) is a ((\w+?) (\w+?) (\w+?))(\\n|$)")

    def test_translation_pattern_with_standard_token(self):
        self.grep = Grap()
        self.assertEqual(self.grep.translate_to_regex("foo %{0} is a %{1}"), "foo (.+?) is a (.+?)(\\n|$)")

    # Testing To Token
    # Non-tokens
    def test_to_token_should_return_word_if_word_is_not_token(self):
        self.grep = Grap()
        self.assertEqual(self.grep._Grap__token_to_regex("foo"), "foo")

    # Standard Tokens
    def test_to_token_should_return_standard_token_regex_if_word_is_standard_token(self):
        self.grep = Grap()
        self.assertEqual(self.grep._Grap__token_to_regex("%{0}"), self.grep.standard_token_regex)

    def test_to_token_standard_token_should_return_input_if_index_is_not_consecutive_starting_at_zero(self):
        self.grep = Grap()
        self.assertEqual(self.grep._Grap__token_to_regex("%{1}"), "%{1}")

    # Space Limited Tokens
    def test_to_token_space_limited_should_return_space_limited_token_regex_if_word_is_space_limited_token(self):
        self.grep = Grap()
        self.assertEqual(self.grep._Grap__token_to_regex("%{0S2}"), "((\w+?) (\w+?) (\w+?))")

    def test_to_token_space_limited_token_should_return_input_if_index_is_not_consecutive_starting_at_zero(self):
        self.grep = Grap()
        self.assertEqual(self.grep._Grap__token_to_regex("%{1}"), "%{1}")

    # Greedy Token
    def test_to_token_greedy_token_should_return_regex_of_greedy_token_if_word_is_greedy_token(self):
        self.grep = Grap()
        self.assertEqual(self.grep._Grap__token_to_regex("%{0G}"), self.grep.greedy_token_regex)

    def test_to_token_greedy_token_should_return_input_if_index_not_consecutive_starting_at_zero(self):
        self.grep = Grap()
        self.assertEqual(self.grep._Grap__token_to_regex("%{1G}"), "%{1G}")

    # Space Limited Token
    # Generating Regex String with Spaces
    def test_generate_space_limited_regex_should_return_regex_defined_number_of_spaces(self):
        self.grep = Grap()
        self.assertEqual(self.grep._Grap__generate_space_limited_regex(3), "((\w+?) (\w+?) (\w+?) (\w+?))")

    def test_generate_space_limited_regex_should_return_standard_token_when_given_zero(self):
        self.grep = Grap()
        self.assertEqual(self.grep._Grap__generate_space_limited_regex(0), "((\w+?))")

    def test_generate_space_limited_regex_should_return_standard_token_twice_with_space_between_when_given_one(self):
        self.grep = Grap()
        self.assertEqual(self.grep._Grap__generate_space_limited_regex(1), "((\w+?) (\w+?))")

    # Testing Regex for Token Shapes/Pattern
    # Standard Token Shape
    def test_token_match_standard_token_to_standard_token(self):
        self.grep = Grap()
        self.assertTrue(self.grep.pattern_and_token_match(self.grep.standard_token_shape, "%{0}"))

    def test_token_match_standard_token_to_standard_token_with_two_digit_index(self):
        self.grep = Grap()
        self.assertTrue(self.grep.pattern_and_token_match(self.grep.standard_token_shape, "%{99}"))

    def test_token_match_standard_should_not_match_any_other_pattern(self):
        self.grep = Grap()
        self.assertFalse(self.grep.pattern_and_token_match(self.grep.standard_token_shape, "%{99G}"))

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

    # Space Limited Token Shape
    def test_token_match_space_limited_token_with_single_digit(self):
        self.grep = Grap()
        self.assertTrue(self.grep.pattern_and_token_match(self.grep.space_limited_token_shape, "%{0S0}"))

    def test_token_match_space_limited_token_with_two_digits(self):
        self.grep = Grap()
        self.assertTrue(self.grep.pattern_and_token_match(self.grep.space_limited_token_shape, "%{10S10}"))

    def test_token_match_space_limited_token__should_not_match_other_pattern(self):
        self.grep = Grap()
        self.assertFalse(self.grep.pattern_and_token_match(self.grep.space_limited_token_shape, "%{99G}"))

    # Testing Instance Creation of Grap
    def test_grap_object_constructor(self):
        grep = Grap()
        self.assertTrue(grep is not None)

if __name__ == '__main__':
    unittest.main()