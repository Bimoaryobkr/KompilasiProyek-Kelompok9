from sly import Lexer

class UntukLexer(Lexer):

    tokens = {NAME, NUMBER, STRING, PRINT, IF, THEN, ELSE, FOR, TO, FUNCTION, EQUALITY, ARROW}
    ignore = '\t '
    literals = { '=', '+', '-', '/', '*', '(', ')', ',', ';'}
  

    IF = r'BILA'
    THEN = r'MAKA'
    ELSE = r'LAIN'
    FOR = r'UNTUK'
    TO = r'HINGGA'
    FUNCTION = r'FUNGSI'
    PRINT = r'TULIS'
    ARROW = r'->'
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    STRING = r'\".*?\"'
    EQUALITY = r'=='
    
    @_(r'\d+')
    def NUMBER(self, t):
        
        t.value = int(t.value) 
        return t
  
    @_(r'`.*')
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