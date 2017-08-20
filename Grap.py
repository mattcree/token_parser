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

    @CodeTrace.trace
    def run(self, params):
        grepper = Grap()
        regex = grepper.multiple_pattern_logical_or_regex(params[1:])
        for line in sys.stdin:
            if grepper.do_match(regex, line):
                sys.stdout.write(line+ "\n")

    @CodeTrace.trace
    def translate_pattern_to_regex(self, pattern):
        self.reset_count()
        return r" ".join([self.to_token(token) for token in pattern.split(" ")]) + self.newline_or_end_of_string

    @CodeTrace.trace
    def multiple_pattern_logical_or_regex(self, pattern_array):
        return "(" + r"|".join([self.translate_pattern_to_regex(pattern) for pattern in pattern_array]) + ")"

    @CodeTrace.trace
    def do_match(self, pattern, string):
        if re.match(pattern, string):
            return True
        return False

    @CodeTrace.trace
    def reset_count(self):
        self.token_count = 0

    @CodeTrace.trace
    def to_token(self, token):
        if not self.do_match(self.any_token_shape, token):
            return token
        if self.do_match(self.simple_token_shape, token):
            regex = self.process_standard_token(token, self.token_count)
            self.token_count += 1
            return regex
        if self.do_match(self.greedy_token_shape, token):
            regex = self.process_greedy_token(token, self.token_count)
            self.token_count += 1
            return regex
        if self.do_match(self.space_limited_token_shape, token):
            regex = self.process_space_limited_token(token, self.token_count)
            self.token_count += 1
            return regex

    @CodeTrace.trace
    def process_standard_token(self, token, current_index):
        index = token[2:-1]
        if int(index) != current_index:
            return IndexError
        return self.simple_token_regex

    @CodeTrace.trace
    def process_greedy_token(self, token, current_index):
        index = token[2:-2]
        if int(index) != current_index:
            print("Expected token index " + str(current_index) + " but found " + index)
            return IndexError
        return self.greedy_token_regex

    @CodeTrace.trace
    def process_space_limited_token(self, token, current_index):
        index_and_spaces = token[2:-1].split("S")
        index = index_and_spaces[0]
        if int(index) != current_index:
            return IndexError
        spaces = int(index_and_spaces[1])
        return self.generate_space_limited_regex(spaces)

    @CodeTrace.trace
    def generate_space_limited_regex(self, number):
        return "(" + ((self.space_limited_token + " ") * (number + 1))[0:-1] + ")"

    def __repr__(self):
        return "Grepper Obj"

if __name__ == '__main__':
    Grap().run(sys.argv)