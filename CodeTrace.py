from time import gmtime, strftime
import sys

class CodeTrace(object):

    @staticmethod
    def trace(fn):
        from itertools import chain
        def wrapped(*v, **k):
            name = fn.__qualname__
            sys.stderr.write("[" + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "] ENTER: %s(%s)" % (name, ", ".join(map(repr, chain(v, k.values())))) + "\n")
            return fn(*v, **k)
        return wrapped
