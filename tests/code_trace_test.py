import unittest, sys
from code_trace import CodeTrace


class TestCodeTraceMethods(unittest.TestCase):
    input = "some input"

    @CodeTrace.trace
    def helper(self, input):
        print("I processed {0}".format(input))
        new_output = "this is the output"
        return new_output

    @CodeTrace.trace(quiet=True)
    def quiet_helper(self, input):
        print("I processed {0}".format(input))
        new_output = "this is the output"
        return new_output

    @CodeTrace.trace(skip=True)
    def skip_helper(self, input):
        print("I processed {0}".format(input))
        new_output = "this is the output"
        return new_output

    def test_codetrace_writes_full_trace(self):
        print("\n\nTest Full Trace")
        print("================")
        output = self.helper(self.input)
        assert output is not None
        print("================")
        print("")

    def test_codetrace_writes_quiet_trace(self):
        print("\n\nTest Quiet Trace")
        print("================")
        output = self.quiet_helper(self.input)
        assert output is not None
        print("================")
        print("")

    def test_codetrace_writes_skip_trace(self):
        print("\n\nTest Skip Trace")
        print("================")
        output = self.skip_helper(self.input)
        assert output is not None
        print("================")
        print("")
        assert output is not None

if __name__ == '__main__':
    Grap().run(sys.argv)