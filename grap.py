#!/usr/bin/env python
import sys, re
from code_trace import CodeTrace

class Grap(object):

    # RegEx for 'shape' of Tokens
    standard_token_shape = re.compile(r"^%{[0-9]{1,2}}$")
    greedy_token_shape = re.compile(r"^%{[0-9]{1,2}G}$")
    space_limited_token_shape = re.compile(r"^%{[0-9]{1,2}S[0-9]{1,2}}$")
    # RegEx representation of Tokens
    standard_token_regex = "(.+?)"
    greedy_token_regex = "(.+)"
    space_limited_token = "(\w+?)"
    newline_or_string_end = "(\\n|$)"

    def __init__(self):
        self.token_count = 0

    #Public Methods
    @staticmethod
    @CodeTrace.trace(skip=True)
    def run(params):
        """
        For use from the command line. Internally creates a new instance
        of a Grap object, generates a Regular Expression based on arguments
        provided and iterates through stdin, writing to stdout any matches found
        between the generated RegEx and the current line of stdin.

        @param params: command line arguments
        @type params: List of String
        """
        grap = Grap()
        regex = grap.translate_multiple_patterns(params[1:])
        for line in sys.stdin:
            if line == ":quit\n":
                sys.exit()
            if grap.pattern_and_token_match(regex, line):
                sys.stdout.write(line)



    # Translation of Patterns to Regex
    @CodeTrace.trace(skip=True)
    def translate_multiple_patterns(self, pattern_array):
        """
        Takes one or more patterns and translates them to RegEx representations
        separated by logical OR.

        @param pattern_array: List of patterns to be translated to RegEx
        @type pattern_array: List
        @return: RegEx with one or more RegEx patterns separated by logical OR
        @rtype: String
        """
        regexs = [self.translate_to_regex(pattern) for pattern in pattern_array]
        return "({0})".format("|".join(regexs))

    @CodeTrace.trace(skip=True)
    def translate_to_regex(self, pattern):
        """
        The input pattern is processed and tokens are replaced by a Regular
        Expression representation of the token. Non tokens are unaffected.

        @param pattern: A string containing literals and tokens
        @type pattern: String
        @return: A string containing literals and regex
        @rtype: String
        """
        #Resets count between patterns
        self.__reset_count()
        translation = [self.__token_to_regex(token) for token in pattern.split(" ")]
        return " ".join(translation) + self.newline_or_string_end


    @CodeTrace.trace(skip=True)
    def pattern_and_token_match(self, pattern, token):
        if re.match(pattern, token):
            return True
        return False

    #For internal use in the class only
    # Token Count Manipulation
    @CodeTrace.trace(skip=True)
    def __reset_count(self):
        self.token_count = 0

    @CodeTrace.trace(skip=True)
    def __increment_token_count(self):
        self.token_count += 1

    @CodeTrace.trace(skip=True)
    def __token_count_is_correct(self, token_index):
        if token_index == self.token_count:
            return True
        return False

    @CodeTrace.trace(skip=True)
    def __increment_and_get_token(self, token):
        self.__increment_token_count()
        return token

    # Processing/Translating Tokens to RegEx
    @CodeTrace.trace(skip=True)
    def __token_to_regex(self, token):
        # If Token matches known Token shape, Token is processed/translated to
        # the RegEx counterpart of the Token. If it does not match any Token type,
        # the Token is returned.
        if self.pattern_and_token_match(self.standard_token_shape, token):
            return self.__process_standard_token(token)
        if self.pattern_and_token_match(self.greedy_token_shape, token):
            return self.__process_greedy_token(token)
        if self.pattern_and_token_match(self.space_limited_token_shape, token):
            return self.__process_space_limited_token(token)
        return token

    @CodeTrace.trace(skip=True)
    def __trim_token_and_process(self, trim_from, trim_to, token_type, original):
        # Parsing index from the token
        index = int(original[trim_from:trim_to])
        return self.__process_token(index, token_type, original)

    @CodeTrace.trace(skip=True)
    def __process_token(self, index, tok_to_get, original):
        # Returns the original token/string if the instance's
        # Token count doesn't match the current token's index
        if self.__token_count_is_correct(index):
            return self.__increment_and_get_token(tok_to_get)
        return original

    @CodeTrace.trace(skip=True)
    def __process_standard_token(self, token):
        # Takes a standard token and returns a standard token
        return self.__trim_token_and_process(2, -1, self.standard_token_regex, token)

    @CodeTrace.trace(skip=True)
    def __process_greedy_token(self, token):
       return self.__trim_token_and_process(2, -2, self.greedy_token_regex, token)

    @CodeTrace.trace(skip=True)
    def __process_space_limited_token(self, token):
        # Splits the token on the 'S'
        index_and_spaces = token[2:-1].split("S")
        index = int(index_and_spaces[0])
        num_of_spaces = int(index_and_spaces[1])
        regex = self.__generate_space_limited_regex(num_of_spaces)
        return self.__process_token(index, regex, token)

    @CodeTrace.trace(skip=True)
    def __generate_space_limited_regex(self, number):
        # Multiplies the space_limited_token + space by number param, removes
        # the final space, and surrounds RegEx in capture group parenthesis
        return "({0})".format(((self.space_limited_token + " ") * (number + 1))[0:-1])

    def __repr__(self):
        return "Grap Object"

if __name__ == '__main__':
    Grap().run(sys.argv)