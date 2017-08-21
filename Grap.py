#!/usr/bin/python
import sys, re
from CodeTrace import CodeTrace


class Grap(object):

    simple_token_shape = re.compile(r"%{[0-9]{1,2}}")
    greedy_token_shape = re.compile(r"%{[0-9]{1,2}G}")
    space_limited_token_shape = re.compile(r"%{[0-9]{1,2}S[0-9]{1,2}}")
    simple_token_regex = "(.+?)"
    greedy_token_regex = "(.+)"
    space_limited_token = "(\w+?)"
    newline_or_end_of_string = "(\\n|$)"

    def __init__(self):
        self.token_count = 0

    @staticmethod
    @CodeTrace.trace
    def run(params):
        """
        For use from the command line. Creates a new instance of a Grap object,
        generates a Regular Expression based on arguments provided and iterates
        through stdin, writing to stdout any matches found between the generated
        RegEx and the current line of stdin.

        @param params: command line arguments
        @type params: List of String
        """
        grap = Grap()
        regex = grap.translate_multiple_patterns(params[1:])
        for line in sys.stdin:
            if grap.pattern_and_token_match(regex, line):
                sys.stdout.write(line)

    @CodeTrace.trace
    def translate_pattern_to_regex(self, pattern):
        """
        Resets the token count to zero for the current instance of Grap. Then,
        the input pattern is split on whitespace, and each word is checked
        for whether it is a token or not. If a token is found, it is exchanged
        for the Regular Expression representation of that token. The string is
        then rejoined with spaces between words and tokens. A newline OR end
        of string RegEx is added to allow for RegEx which finds matches on single
        strings or within multi-line contexts.

        @param pattern: A string containing literals and tokens
        @type pattern: String
        @return: A string containing literals and regex
        @rtype: String
        """
        self.reset_count()
        return " ".join([self.token_to_regex(token) for token in pattern.split(" ")]) + self.newline_or_end_of_string

    @CodeTrace.trace
    def translate_multiple_patterns(self, pattern_array):
        """
        Takes a list of Strings containing literal text and tokens, and translates
        each String to Strings containing literal text and Regular Expressions.
        These translated strings are then joined to form a RegEx string capture group
        with logical OR operators between each translated pattern.

        @param pattern_array: List of Strings containing literal text and tokens
        @type pattern_array: List
        @return: String of RegEx with one or more RegEx patterns separated by logical OR
        @rtype: String
        """
        return "(" + r"|".join([self.translate_pattern_to_regex(pattern) for pattern in pattern_array]) + ")"

    @CodeTrace.trace
    def reset_count(self):
        self.token_count = 0

    @CodeTrace.trace
    def increment_index(self):
        self.token_count += 1

    @CodeTrace.trace
    def token_count_is_correct(self, token_index):
        if token_index == self.token_count:
            return True
        return False

    @CodeTrace.trace
    def increment_and_get_token(self, token):
        self.increment_index()
        return token

    @CodeTrace.trace
    def token_to_regex(self, token):
        """
        Checks if token param matches shape of token i.e. checks if token param is a token. If not,
        returns token param. The token param is then checked against specific token types to
        find which it matches and returns a RegEx based on that token's shape.

        @param token: String containing token or
        @type token:
        @return:
        @rtype:
        """
        if self.pattern_and_token_match(self.simple_token_shape, token):
            return self.process_standard_token(token)
        if self.pattern_and_token_match(self.greedy_token_shape, token):
            return self.process_greedy_token(token)
        if self.pattern_and_token_match(self.space_limited_token_shape, token):
            return self.process_space_limited_token(token)
        return token

    @CodeTrace.trace
    def pattern_and_token_match(self, pattern, string):
        return True if re.match(pattern, string) else False

    @CodeTrace.trace
    def process_standard_token(self, token):
        index = int(token[2:-1])
        return self.process_token(index, self.simple_token_regex, token)

    @CodeTrace.trace
    def process_greedy_token(self, token):
        index = int(token[2:-2])
        return self.process_token(index, self.greedy_token_regex, token)

    @CodeTrace.trace
    def process_space_limited_token(self, token):
        index_and_spaces = token[2:-1].split("S")
        index = int(index_and_spaces[0])
        num_of_spaces = int(index_and_spaces[1])
        return self.process_token(index, self.generate_space_limited_regex(num_of_spaces), token)

    @CodeTrace.trace
    def process_token(self, index, token_to_get, original_token):
        return self.increment_and_get_token(token_to_get) if self.token_count_is_correct(index) else original_token

    @CodeTrace.trace
    def generate_space_limited_regex(self, number):
        return "({0})".format(((self.space_limited_token + " ") * (number + 1))[0:-1])

    def __repr__(self):
        return "Grap Object"

if __name__ == '__main__':
    Grap().run(sys.argv)