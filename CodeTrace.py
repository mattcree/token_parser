from datetime import datetime
import sys

class CodeTrace(object):

     @staticmethod
     def trace(*args):
        entry_text = "ENTER"
        exit_text = "EXIT"
        newline = "\n"
        entry_trace = "[{0}] {1} *** {2} {3}{4} {5}"
        exit_trace = "[{0}] {1} *** {2}  {3}({4}) {5}"
        time_format = "%Y-%m-%d %H:%M:%S.%f"

        # Full Trace
        # Writes log trace to stderr including input/output values
        # produced by functions
        def _trace(func):
            def wrapper(*args, **kwargs):
                class_name = func.__qualname__.split(".")[0]
                function_name = func.__name__
                entry_timestamp = datetime.now().strftime(time_format)

                # Writing the Entry trace to stderr
                sys.stderr.write(entry_trace.format(entry_timestamp,
                                                    class_name,
                                                    entry_text,
                                                    function_name,
                                                    str(args),
                                                    newline)
                )

                result = func(*args, **kwargs)
                exit_timestamp = datetime.now().strftime(time_format)

                # Writing the Exit trace to stderr
                sys.stderr.write(exit_trace.format(exit_timestamp,
                                                   class_name,
                                                   exit_text,
                                                   function_name,
                                                   result,
                                                   newline)
                )

                return result
            return wrapper

        # Quiet Trace
        # Writes simple log trace to stderr without input/output values
        def _quiet_trace(func):
            def wrapper(*args, **kwargs):
                class_name = func.__qualname__.split(".")[0]
                function_name = func.__name__
                entry_timestamp = datetime.now().strftime(time_format)

                sys.stderr.write(exit_trace.format(entry_timestamp,
                                                    class_name,
                                                    entry_text,
                                                    function_name,
                                                    "",
                                                    newline)
                )

                result = func(*args, **kwargs)
                exit_timestamp = datetime.now().strftime(time_format)

                sys.stderr.write(exit_trace.format(exit_timestamp,
                                                   class_name,
                                                   exit_text,
                                                   function_name,
                                                   "",
                                                   newline)
                )

                return result
            return wrapper

        # Skip trace
        # No log trace written
        def _skip_trace(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper

        # If only the wrapped function is passed to CodeTrace.trace the
        # verbose/full trace is run used. If 'quiet' is provided as an argument
        # i.e. CodeTrace.trace('quiet'), the quiet trace will be run. For
        # any other argument, the trace will be skipped.

        if len(args) == 1 and callable(args[0]):
            return _trace(args[0])
        if args[0] == 'quiet':
            return _quiet_trace
        else:
            return _skip_trace