# Problem Definition

Write a program in Python (2.7.x or 3.x) that: 
- translates a pattern specification provided as a
command line argument into a regular expression, 
- processes lines of input text received from stdin
using that regular expression to qualify matches, 
- and finally writes each matching input line to
stdout. 

Each line of input is terminated by the newline character '\n', and the program should terminate when it receives EOF (end of file).

The program should be executable as follows:

```$ cat input.txt | program "is this message %{0} ballpark %{1S3}" > output.txt```

The program should be structured to parse the pattern specification and generated a regular expression which expresses the pattern. The program should then use the “re” module, using PCRE style syntax, to execute matches to qualify each line of text received on stdin.

# Python Considerations

The program should be implemented as a *class module with a \_\_main\_\_ section* to allow the code to be used both as a reusable module in a larger project and directly for command line usage. The class should have appropriately named methods for code functionality/reuse. Granularity of
methods is left to you.

Support: One or more patterns supplied on the command line and treat as a logical OR when
matching lines.

## Automation/Code Tracing

It is often important to be able to retrospectively walk through a code run
long after the execution has finished. The program should implement a functional trace log line,
printed on STDERR, of every class method called.

The log should include:
1. Timestamp
2. Calling class
3. Calling method name
4. Any parameters passed to the method
5. Return value(s) from the method.

Example (output format of the data is up to you):
```
[20150102-18:56:17.306945] Grepper *** ENTER matchLine(This is blah blah)
[20150102-18:56:17.306964] Grepper *** EXIT matchLine(True)
```

Preferred is a general purpose solution that does not require you to modify the internals of any of
the Class methods. I.e. write a CodeTrace class with a single class method called trace() so you use
that as a decorator to your program’s class methods.

Example:
```@CodeTrace.trace()
def matchLine(self, line):
```
## Advanced Python (Bonus Points)

Enhance the trace method to support passing optional modifying parameters in the
decorator:

a. skip=True – Bypass printing anything
b. quiet=True – Bypass printing the input/return values in the output.

Example:
```
@CodeTrace.trace(quiet=True)
def methodName(…
```
# Pattern Specification

A pattern is a **text string**, delimited with token capture sequences which identify the variable text extracted from the message. 

A token capture sequence is represented as a:

1. percent sign '**%**' character 
2. followed by a '**{**' character
3. followed by a **non-negative integer**
4. followed by an **optional** token capture **modifier**, 
5. and finally a '**}**' character. 

The non-negative integer denotes the index into the token list associated with the rule to which the pattern belongs. A simple token capture sequence would be written as ```%{0}``` and ```%{25}```, and will capture any amount of text which occurs between the adjacent text literals. 

For example of a pattern with only simple token escape sequences follows:

```"foo %{0} is a %{1}"```

which would match the following text strings:

```
"foo blah is a bar"
"foo blah is a very big boat"
```

but would not match the following text strings:

```
"foo blah is bar"
"foo blah"
"foo blah is"
```

A token capture modifier specifies special handling of the token capture in order to differentiate
otherwise ambiguous patterns. 

There are two types of token capture modifiers: 

1. space limitation (S#)
2. and greedy (G). 

A space limitation modifier specifies a precise number of whitespace characters
which must be appear between text literals in order to match the associated token capture
sequence. 

For example, the token capture sequence ```%{1S2}``` specifies:
- token one (1), 
- with a space limitation modifier of exactly two (2) spaces. 

For example, the pattern:

```"foo %{0} is a %{1S0}"```

which would match the following text string:

```"foo blah is a bar"```

but would not match the following text strings:

```
"foo blah is a very big boat"
"foo blah is bar"
"foo blah"
"foo blah is"
```

The whitespace modifier is intended to be used to limit possibly ambiguous matches, as in the example above, or in cases where two token capture sequencesoccur adjacent within a pattern without intervening literal text. 

For example, the pattern:

```"the %{0S1} %{1} ran away"```

would match the text string

```"the big brown fox ran away"```

which would capture "big brown" for token ```%{0S1}```, and "fox" for token ```%{1}```

A greedy token capture modifier specifies special handling of the token capture in order to differentiate patterns which are ambiguous due to repetitions of token value text that also occurs in the literal text of the pattern. The greedy capture modifier captures as mush as possible text between preceding and following string literals. 

For example, the pattern:

```"bar %{0G} foo %{1}"```

would match the text string:

```"bar foo bar foo bar foo bar foo"```

and capture "foo bar foo bar" for token specifier ```%{0G}``` and "bar foo" for token specifier ```%{1}```.


# Program Evaluation

The program should be be in source form and should use what you consider good coding standards. 
Comments should be used within the code to explain interesting or tricky segments that would help someone else who needs to maintain the code. 
Clarity and correctness are of paramount importance, with efficiency following those.