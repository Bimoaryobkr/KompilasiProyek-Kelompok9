from sly import Lexer

class UntukLexer(Lexer):

    tokens = {NAME, NUMBER, STRING, PRINT, IF, THEN, ELSE, FOR, TO}
    ignore = '\t '
    literals = { '=', '+', '-', '/', 
                '*', '(', ')', ',', ';'}
  
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    STRING = r'\".*?\"'
    PRINT = r'tulis'
    IF = r'bila'
    THEN = r'maka'
    ELSE = r'lain'
    FOR = r'untuk'
    TO = r'hingga'

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


