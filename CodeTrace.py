from time import gmtime, strftime
import sys

class CodeTrace(object):

     def trace(*args):
        def _trace(func):
            def wrapper(*args, **kwargs):
                class_name = func.__qualname__.split(".")[0]
                function_name = func.__name__
                sys.stderr.write("[" + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "] "
                                  + class_name
                                  + " *** ENTER " + function_name
                                  + str(args) + "\n")
                result = func(*args, **kwargs)
                sys.stderr.write("[" + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "] "
                                  + class_name
                                  + " ***  EXIT " + func.__name__
                                  + "(" +str(result) + ")\n")
                return result
            return wrapper

        def _quiet_trace(func):
            def wrapper(*args, **kwargs):
                class_name = func.__qualname__.split(".")[0]
                function_name = func.__name__
                sys.stderr.write("[" + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "] "
                                  + class_name
                                  + " *** ENTER " + function_name
                                  + "\n")
                result = func(*args, **kwargs)
                sys.stderr.write("[" + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "] "
                                  + class_name
                                  + " ***  EXIT " + function_name
                                  + "\n")
                return result
            return wrapper

        def _skip_trace(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper

        if len(args) == 1 and callable(args[0]):
            return _trace(args[0])
        if args[0] == 'quiet':
            return _quiet_trace
        else:
            return _skip_trace