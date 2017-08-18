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

    def run(self, params):
        return

    def token_match(self, token, string):
        return re.match(token, string)

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
        spaces = index_and_spaces[1]
        return self.generate_space_limited_regex(spaces)

    def generate_space_limited_regex(self, number):
        space_limited = "(" + self.simple_token_regex
        for i in range(0, number):
            space_limited += " "
            space_limited += self.simple_token_regex
        return space_limited + ")"

if __name__ == '__main__':
    Grepper().run(sys.argv)