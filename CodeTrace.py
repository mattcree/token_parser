from time import gmtime, strftime
import sys

class CodeTrace(object):

    def trace(fn):
        def wrapped(*args, **kw):
            sys.stderr.write("[" + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "] " + fn.__qualname__[0:4] + " *** ENTER: " +fn.__name__ + str(args) + "\n")
            result = fn(*args, **kw)
            sys.stderr.write("[" + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "] " + fn.__qualname__[0:4] + " *** EXIT: " + fn.__name__ + "(" +str(result) + ")\n")
            return result
        return wrapped