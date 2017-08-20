from time import gmtime, strftime
import sys

class CodeTrace(object):

    def trace(fn):
        def wrapped(*args, **kw):
            sys.stderr.write("[" + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "] ENTER: " + fn.__qualname__ + str(args) + "\n")
            result = fn(*args, **kw)
            sys.stderr.write("[" + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "] EXIT: " + fn.__qualname__ + "(" +str(result) + ")\n")
            return result
        wrapped.__name__ = fn.__name__
        wrapped.__doc__ = fn.__doc__
        return wrapped


