#!/usr/bin/python
import sys, re
from CodeTrace import CodeTrace


class Grap(object):

    def __init__(self):
        self.any_token_shape = re.compile(r"%{.+}")
        self.simple_token_shape = re.compile(r"%{[0-9]{1,2}}")
        self.greedy_token_shape = re.compile(r"%{[0-9]{1,2}G}")
        self.space_limited_token_shape = re.compile(r"%{[0-9]{1,2}S[0-9]{1,2}}")
        self.simple_token_regex = "(.+?)"
        self.greedy_token_regex = "(.+)"
        self.space_limited_token = "(\w+?)"
        self.newline_or_end_of_string = "(\\n|$)"
        self.token_count = 0

    @staticmethod
    def run(params):
        """
        For use from the command line. Creates a new instance of a Grap object,
        generates a Regular Expression based on arguments provided from the command
        line, and iterates through stdin, writing to stdout any matches found
        between the generated RegEx and the current line of stdin.

        @param params: command line arguments
        @type params: List of String

        """
        grap = Grap()
        regex = grap.multiple_pattern_logical_or_regex(params[1:])
        for line in sys.stdin:
            if grap.do_match(regex, line):
                sys.stdout.write(line)

    @CodeTrace.trace('skip')
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
        return r" ".join([self.token_to_regex(token) for token in pattern.split(" ")]) + self.newline_or_end_of_string

    @CodeTrace.trace('skip')
    def multiple_pattern_logical_or_regex(self, pattern_array):
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

    @CodeTrace.trace('skip')
    def reset_count(self):
        self.token_count = 0

    @CodeTrace.trace('skip')
    def increment_index(self):
        self.token_count += 1

    @CodeTrace.trace('skip')
    def check_token_count(self, token_index):
        if token_index == self.token_count:
            return True
        return False

    @CodeTrace.trace('skip')
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
        if not self.do_match(self.any_token_shape, token):
            return token
        if self.do_match(self.simple_token_shape, token):
            return self.process_standard_token(token)
        if self.do_match(self.greedy_token_shape, token):
            return self.process_greedy_token(token)
        if self.do_match(self.space_limited_token_shape, token):
            return self.process_space_limited_token(token)

    @CodeTrace.trace('skip')
    def do_match(self, pattern, string):
        return True if re.match(pattern, string) else False

    @CodeTrace.trace('skip')
    def process_standard_token(self, token):
        index = int(token[2:-1])
        if self.check_token_count(index):
            self.increment_index()
            return self.simple_token_regex
        return token

    @CodeTrace.trace('skip')
    def process_greedy_token(self, token):
        index = int(token[2:-2])
        if self.check_token_count(index):
            self.increment_index()
            return self.greedy_token_regex
        return token

    @CodeTrace.trace('skip')
    def process_space_limited_token(self, token):
        index_and_spaces = token[2:-1].split("S")
        index = int(index_and_spaces[0])
        spaces = int(index_and_spaces[1])
        if self.check_token_count(index):
            self.increment_index()
            return self.generate_space_limited_regex(spaces)
        return token

    @CodeTrace.trace('skip')
    def generate_space_limited_regex(self, number):
        return "(" + ((self.space_limited_token + " ") * (number + 1))[0:-1] + ")"

    def __repr__(self):
        return "Grepper Obj"

if __name__ == '__main__':
    Grap().run(sys.argv)