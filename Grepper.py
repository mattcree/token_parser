#!/usr/bin/python
import sys, re


class Grepper(object):

    def __init__(self):
        self.standard_token = ".+"
        self.space_limited_token = "\w+?"
        self.space = " "

    def run(self, params):
        return 0

    def parse_spec_string(self, string):
        return 0

    def token_to_regex(self, token):
        return 0

    def greedy_regex(self):
        return 0

    def replace_standard_tokens(self, string):
        return re.sub(r"%{[0-9]{1,2}}", "(" + self.standard_token + ")", string)

    def space_limited_regex(self, number):
        regex = "(" + self.standard_token
        for i in range(0,number):
            regex += self.space
            regex += self.standard_token
        return regex + ")"

if __name__ == '__main__':
    Grepper().run(sys.argv)