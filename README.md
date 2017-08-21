# Grap

A Python program (3.6) that: 
- translates a pattern specification provided as a
command line argument into a regular expression 
- processes lines of input text received from stdin using Regular Expressions to qualify matches 
- writes each matching input line to
stdout. 

Each line of input should be terminated by the newline character '\n', and the program should terminate when it receives EOF (end of file).

The program parses a pattern specification, generating a Regular Expression which expresses that pattern. The program relies upon Pythons “re” module to execute matches to qualify each line of text received on stdin, and uses PCRE style syntax.

## Instructions
### Running the program

The program can be executed as follows:

```$ cat input.txt | grap "is this message %{0} ballpark %{1S3}" > output.txt```

If run without a piped file as follows:

```$ grap "is this message %{0} ballpark %{1S3}"```

The program will accept user input and will print/repeat that input if it matches the argument.

To stop the program, type ```:quit```


### Running the tests

From the command line, enter the root directory of the program and run:

```py -m unittest -v tests/grap_test.py```

## Program Usage

Grap can be used both as a module in a larger project and directly for command line usage. It also supports one or more patterns supplied on the command line, and treating them as a logical OR when matching lines. For example:

```$ cat input.txt | program "is this message %{0} ballpark %{1}" "is this %{0}" > output.txt```

Will match either 
```"is this message in the ballpark of being very very interesting"``` 
or 
```"is this message interesting"```

## Pattern Specification

Grepper takes as arguments **text strings**, delimited with token capture sequences which identify the variable text
extracted from the message.

A token capture sequence is represented as a:

1. percent sign '**%**' character 
2. followed by a '**{**' character
3. followed by a **non-negative integer**
4. followed by an **optional** token capture **modifier**, 
5. and finally a '**}**' character. 

The non-negative integer denotes the index into the token list associated with the rule to which the pattern belongs. Non-consecutive indexed tokens found will be ignored. 

For example in the input ```"foo %{0} is a %{2}"``` the second token will be treated as a string literal and will not be parsed. In the example ```"foo %{0} is a %{1}"``` both tokens will be parsed.

A string input can contain up to 100 tokens, numbered between 0 and 99.

A simple token capture sequence is written as ```%{0}``` and ```%{25}```, and will capture any amount of text which occurs between the adjacent text literals. 

A pattern with only simple token escape sequences follows:

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

A token capture modifier specifies special handling of the token capture in order to differentiate between otherwise ambiguous patterns. 

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

# CodeTrace
CodeTrace allows you to view a functional trace log line, printed on STDERR, of every class method called. It is designed for use as a decorator and takes some optional parameters to modify output.

It contains a single static method 'trace'.

There are three levels of trace supported; full, quiet, and skipped/none.
## Instructions

### Using the program
#### Full Trace
Enabling full trace of method:
```
@CodeTrace.trace
def pattern_and_token_match(self, pattern, string):
```
Full trace writes the following to stderr:

1. Timestamp
2. Calling class
3. Calling method name
4. Any parameters passed to the method
5. Return value(s) from the method.

Example output:
```
[20150102-18:56:17.306945] Grap *** ENTER pattern_and_token_match(Grap Obj, some regex, string to test)
[20150102-18:56:17.306964] Grap *** EXIT  pattern_and_token_match(True)
```

#### Quiet and Skip
Enabling quiet trace of method:
```
@CodeTrace.trace(quiet=True)
def pattern_and_token_match(self, pattern, string):
```

Quiet trace writes the following to stderr:

1. Timestamp
2. Calling class
3. Calling method name

Example output:
```
[20150102-18:56:17.306945] Grap *** ENTER pattern_and_token_match()
[20150102-18:56:17.306964] Grap *** EXIT  pattern_and_token_match()
```

Skipping trace of method:
```
@CodeTrace.trace(skip=True)
def pattern_and_token_match(self, pattern, string):
```

Skipping omits any trace output from the method it decorates.

### Running the tests

From the command line, enter the root directory of the program and run:

```py -m unittest -v tests/code_trace_test.py```

Manually verify output is as expected.