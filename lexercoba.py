from pyclbr import Function
from sly import Lexer

class UntukLexer(Lexer):

    tokens = {NAME, NUMBER, STRING, PRINT, IF, THEN, ELSE, FOR, TO, FUN, EQEQ, ARROW}
    ignore = '\t '
    literals = { '=', '+', '-', '/', '*', '(', ')', ',', ';'}
  
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    STRING = r'\".*?\"'
    PRINT = r'tulis'
    IF = r'bila'
    THEN = r'maka'
    ELSE = r'lain'
    FOR = r'untuk'
    TO = r'hingga'
    FUN = r'fungsi'
    EQEQ = r'=='
    ARROW = r'->'

    @_(r'\d+')
    def NUMBER(self, t):
        
        t.value = int(t.value) 
        return t
  
    @_(r'//.*')
    def COMMENT(self, t):
        pass
  
    @_(r'\n+')
    def newline(self, t):
        self.lineno = t.value.count('\n')

if __name__ == '__main__':
    lexer = UntukLexer()
    env = {}
    while True:
        try:
            text = input('Cek Lexer > ')
        except EOFError:
            break
        if text:
            lex = lexer.tokenize(text)
            for token in lex:
                print(token)