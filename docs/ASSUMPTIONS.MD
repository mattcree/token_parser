## Assumptions:
### Pattern Translation to Regex

1. The non-negative integer token index should be sequential 
	- Range between 0 and 99 (two digits)
	- Tokens which are not consecutive should be ignored when parsing

2. Tokens of the form %{0}
	- Can include spaces
	- Equivalent to Regex '.+?' allowing any character as many time as possible (at least one character)

3. Tokens of the form %{0S0}
	-'Whitespace' characters means 'spaces' specifically
	-'Space limited' token %{0S3} translates to 'word word word word' and not 'word   ' or '   word' or 'word word  '
	- words must be present for token to match (number of words = the number of spaces + 1)
	- can't simply contain the correct number of spaces without words
	- the number represents spaces between words
	- should be no trailing whitespace

4. Tokens of the form %{0G}
	- RegEx representation '.+' 

### Code Tracing