# Grepper

A program in Python (2.7.x or 3.x) that: 
- translates a pattern specification provided as a
command line argument into a regular expression 
- processes lines of input text received from stdin
using that regular expression to qualify matches 
- and finally writes each matching input line to
stdout. 

Each line of input should be terminated by the newline character '\n', and the program should terminate when it receives EOF (end of file).

The program is executable as follows:

```$ cat input.txt | program "is this message %{0} ballpark %{1S3}" > output.txt```

The program is structured to parse a pattern specification and generateds a regular expression which expresses the pattern. The program is relies upon Pythons “re” module to execute matches to qualify each line of text received on stdin, and uses PCRE style syntax.

# Program Usage

Grepper can be used both as a module in a larger project and directly for command line usage. It also supports one or more patterns supplied on the command line, and treating them as a logical OR when matching lines. For example:

```$ cat input.txt | program "is this message %{0} ballpark %{1}" "is this %{0}" > output.txt```

Will match either 
```"is this message in the ballpark of being very very interesting"``` 
or 
```"is this message interesting"```

# Pattern Usage Specification

Grepper takes as arguments **text strings**, delimited with token capture sequences which identify the variable text
extracted from the message.

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