import idnlexer
import idnparser
import idninterpreter

from sys import *

lexer = idnlexer.UntukLexer()
parser = idnparser.UntukParser()
env = {}

file = open(argv[1])
text = file.readlines()
for line in text:
    tree = parser.parse(lexer.tokenize(line))
    idninterpreter.UntukEksekusi(tree, env)