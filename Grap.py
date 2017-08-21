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
    newline_or_string_end = "(\\n|$)"

    def __init__(self):
        self.token_count = 0

    @staticmethod
    @CodeTrace.trace
    def run(params):
        """
        For use from the command line. Creates a new instance of a Grap
        object, generates a Regular Expression based on arguments provided
        and iterates through stdin, writing to stdout any matches found
        between the generated RegEx and the current line of stdin.

        @param params: command line arguments
        @type params: List of String
        """
        grap = Grap()
        regex = grap.translate_multiple_patterns(params[1:])
        for line in sys.stdin:
            if grap.pattern_and_token_match(regex, line):
                sys.stdout.write(line)

    ### Translation of Patterns to Regex ###

    @CodeTrace.trace
    def translate_multiple_patterns(self, pattern_array):
        """
        Takes a list of strings containing literal text and tokens, and
        translates each string to strings containing literal text and
        Regular Expressions. These translated strings are then joined
        to form a RegEx string capture group with logical OR operators
        between each translated pattern.

        @param pattern_array: List of patterns to be translated to RegEx
        @type pattern_array: List
        @return: RegEx with one or more RegEx patterns separated by logical OR
        @rtype: String
        """
        regexs = [self.translate_to_regex(pattern) for pattern in pattern_array]
        return "({0})".format("|".join(regexs))

    @CodeTrace.trace
    def translate_to_regex(self, pattern):
        """
        The input pattern is split on spaces, and each word is checked
        for whether it is a token or not. Tokens are exchanged for the
        Regular Expression represented by that token. The RegEx string
        is then rejoined with spaces between words and RegEx. A newline
        OR end of string RegEx is added to allow for RegEx which finds
        matches on single strings or within multi-line contexts.

        @param pattern: A string containing literals and tokens
        @type pattern: String
        @return: A string containing literals and regex
        @rtype: String
        """
        #Resets count between patterns
        self.reset_count()
        regex = [self.token_to_regex(token) for token in pattern.split(" ")]
        return " ".join(regex) + self.newline_or_string_end


    ### Token Count Manipulation ###

    @CodeTrace.trace
    def reset_count(self):
        self.token_count = 0

    @CodeTrace.trace
    def increment_token_count(self):
        self.token_count += 1

    @CodeTrace.trace
    def token_count_is_correct(self, token_index):
        if token_index == self.token_count:
            return True
        return False

    @CodeTrace.trace
    def increment_and_get_token(self, token):
        self.increment_token_count()
        return token

    @CodeTrace.trace
    def token_to_regex(self, token):
        """
        If Token matches known Token shape, Token is processed/translated to
        the RegEx counterpart of the Token. If it does not match any Token type,
        the Token is returned.

        @param token: Potential Token for processing
        @type token: String
        @return: RegEx of Token
        @rtype: String
        """
        if self.pattern_and_token_match(self.simple_token_shape, token):
            return self.process_standard_token(token)
        if self.pattern_and_token_match(self.greedy_token_shape, token):
            return self.process_greedy_token(token)
        if self.pattern_and_token_match(self.space_limited_token_shape, token):
            return self.process_space_limited_token(token)
        return token

    ### Processing/Translating Tokens to RegEx ###

    @CodeTrace.trace
    def pattern_and_token_match(self, pattern, string):
        return True if re.match(pattern, string) else False

    @CodeTrace.trace
    def process_token(self, index, tok_to_get, original):
        # Checks index matches current token_count and increments and returns
        # the tok_to_get if it does. Returns original token otherwise.
        return self.increment_and_get_token(tok_to_get) \
            if self.token_count_is_correct(index) else original

    @CodeTrace.trace
    def process_standard_token(self, token):
        # Parsing index from the token
        index = int(token[2:-1])
        return self.process_token(index, self.simple_token_regex, token)

    @CodeTrace.trace
    def process_greedy_token(self, token):
        index = int(token[2:-2])
        return self.process_token(index, self.greedy_token_regex, token)

    @CodeTrace.trace
    def process_space_limited_token(self, token):
        # Splits the token on the 'S'
        index_and_spaces = token[2:-1].split("S")
        index = int(index_and_spaces[0])
        num_of_spaces = int(index_and_spaces[1])
        regex = self.generate_space_limited_regex(num_of_spaces)
        return self.process_token(index, regex, token)

    @CodeTrace.trace
    def generate_space_limited_regex(self, number):
        # Multiplies the space_limited_token + space by number param, removes
        # the final space, and surrounds RegEx in capture group parenthesis
        return "({0})".format(((self.space_limited_token + " ") * (number + 1))[0:-1])

    def __repr__(self):
        return "Grap Object"

if __name__ == '__main__':
    Grap().run(sys.argv)