Name: Parikshita Tripathi
CWID: A20327943

CS-585: Natural Language Processing

An implementation of the Earley Parser in Python. 
We did not use the given Java code so we used the Python implementation of Earley parser to do this assignment.

The grammar file is a plain text file. It can be edited with any plain text editor, e.g. Notepad or Notepad++ on Microsoft Windows, jEdit, Vim or Emacs (Aquamacs) on Mac OS X or Linux systems. The grammar files are expected to be encoded in UTF-8. The line ending is irrelevant, i.e. it can be a Windows or a Unix one. The rules are simple CFG rules with one left-hand side symbol, and any combination of symbols and terminals in the right-hand side:

NP -> Art Adj N

The file can contain comments that are introduced with a #, as in the following two lines:

# Grammar:
S -> NP VP # simple sentence rule


Rules contain a left-hand side and a right-hand side. The separating character sequence can be:

->

as well as similar combinations of minus or equal characters followed by a larger character.

Y\The grammars could be phrase structure rules as the examples above, or grammars of the following type, for example right linear grammars:

X -> a Y
Y -> b
Y -> b Z
Z -> a Y

Command line arguments to be supplied while running the code are:

-g GRAMMARFILE

and

-i EXAMPLE_SENTENCE

An example call of the parser might look like this:

./ChartyPy3.py -g PSG1.txt -i “John loves Mary”

Important is to surround the input sentence with double quotes, as shown in the command above.

-l arguments prints the tree in bracketed format.

Example input output:

Command:
./ChartyPy3.py -g PSG1.txt -i "John loves Mary" -l

Output:
\Tree [.S [.NP [.N John ] ] [.VP [.V loves ] [.NP [.N Mary ] ] ] ]
