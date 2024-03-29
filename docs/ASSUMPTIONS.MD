## Assumptions:
### Pattern Translation to Regex

1. The non-negative integer token index should be sequential 
	- Range between 0 and 99 (two digits)
	- Tokens which are not consecutive should be ignored when parsing

2. Tokens of the form *%{0}*
	- Can include spaces
	- Equivalent to Regex **(.+?)** allowing any character as many times as possible (at least one character)

3. Tokens of the form *%{0S0}*
	- 'Whitespace' refers to space characters specifically
	- *%{0S1}* should be represented as **((\w+?) (\w+?))** in RegEx
	- *%{0S3}* indicates sequences like 'word word word word' and not 'word   ' or '   word' or 'word word  '
		- should be no trailing whitespace
		- words must be present for token to match (number of words = the number of spaces + 1)
		- can't simply contain the correct number of spaces without words

4. Tokens of the form %{0G}
	- RegEx representation **(.+)** 

5. No trailing whitespace on each line
	- the newline character should appear at the end of the last word in the string to match
	    - Rather than "foo bar is a ", examples showed "foo bar is a"

6. Similar behaviour to command line usage should be available in Class usage
    - i.e. there should be some way to iterate through a file, writing matches