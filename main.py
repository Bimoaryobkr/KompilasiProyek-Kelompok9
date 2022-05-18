import bahasaidn

from sys import *

lexer = bahasaidn.UntukLexer()
parser = bahasaidn.UntukParser()
env = {}

file = open(argv[1])
text = file.readlines()
for line in text:
    tree = parser.parse(lexer.tokenize(line))
    bahasaidn.UntukEksekusi(tree, env)