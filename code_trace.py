from datetime import datetime
import sys

class CodeTrace(object):


    @staticmethod
    def trace(*args, **kwargs):
        entry_trace = "[{0}] {1} *** {2} {3}{4}\n"
        exit_trace = "[{0}] {1} *** {2}  {3}({4})\n"
        entry_text = "ENTER"
        exit_text = "EXIT"

        # Full Trace
        # Writes log trace to stderr including input/output values
        # produced by functions
        def __trace(func):
            def wrapper(*args, **kwargs):
                return CodeTrace.write_and_return(func, args, kwargs, entry_trace,
                                                  exit_trace, entry_text, exit_text, True)
            return wrapper

        # Quiet Trace
        # Writes simple log trace to stderr without input/output values
        def __quiet_trace(func):
            def wrapper(*args, **kwargs):
                return CodeTrace.write_and_return(func, args, kwargs, entry_trace,
                                                  exit_trace, entry_text, exit_text, False)
            return wrapper

        # Skip trace
        # No log trace written
        def __skip_trace(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper

        # If only the wrapped function is passed to CodeTrace.trace the
        # verbose/full trace is run used. If 'quiet' is provided as an argument
        # i.e. CodeTrace.trace('quiet'), the quiet trace will be run. For
        # any other argument, the trace will be skipped.
        if len(args) == 1 and callable(args[0]):
            return __trace(args[0])
        if kwargs is not None:
            if kwargs.get("quiet"):
                return __quiet_trace
        return __skip_trace

    @staticmethod
    def write_and_return(func, args, kwargs, enter_style,exit_style, enter_txt, exit_txt, show_results):
        entry_values = args if show_results else "()"
        CodeTrace.write(func, enter_style, enter_txt, entry_values)
        result = func(*args, **kwargs)
        show_return = result if show_results else ""
        CodeTrace.write(func, exit_style, exit_txt, show_return)
        return result

    @staticmethod
    def write(func, style, text, values):
        time_format = "%Y-%m-%d %H:%M:%S.%f"
        now = datetime.now().strftime(time_format)
        class_name = func.__qualname__.split(".")[0]
        function_name = func.__name__
        sys.stderr.write(style.format(now, class_name, text,
                                      function_name, values))