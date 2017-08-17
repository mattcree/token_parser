#!/usr/bin/python
import sys, re


class Grepper(object):

    def __init__(self):
        self.word = "\w+?"
        self.greedy_word = "\w+"
        self.space = " "

    def run(self, params):
        return 0

    def parse_spec_string(self, string):
        return 0

    def token_to_regex(self, token):
        return 0

    def greedy_regex(self):
        return

    def space_limited_regex(self, number):
        regex = self.word
        for i in range(0,number):
            regex += self.space
            regex += self.word
        return regex

if __name__ == '__main__':
    Grepper().run(sys.argv)