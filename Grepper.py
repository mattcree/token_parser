#!/usr/bin/python
import sys, re


class Grepper(object):

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

    def run(self, params):
        return

    def do_match(self, pattern, string):
        return re.match(pattern, string)

    def translate_pattern_to_regex(self, pattern):
        self.token_count = 0
        return r" ".join([self.to_token(token) for token in pattern.split(" ")]) + self.newline_or_end_of_string

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

    def process_standard_token(self, token, current_index):
        index = token[2:-1]
        if int(index) != current_index:
            return EOFError
        return self.simple_token_regex

    def process_greedy_token(self, token, current_index):
        index = token[2:-2]
        if int(index) != current_index:
            return EOFError
        return self.greedy_token_regex

    def process_space_limited_token(self, token, current_index):
        index_and_spaces = token[2:-1].split("S")
        index = index_and_spaces[0]
        if int(index) != current_index:
            return EOFError
        spaces = int(index_and_spaces[1])
        return self.generate_space_limited_regex(spaces)

    def generate_space_limited_regex(self, number):
        return "(" + ((self.space_limited_token + " ") * (number + 1))[0:-1] + ")"

if __name__ == '__main__':
    Grepper().run(sys.argv)