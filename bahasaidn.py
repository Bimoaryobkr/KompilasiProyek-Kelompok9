from sly import Lexer
from sly import Parser

#Lexer
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

#Parser
class UntukParser(Parser):
    tokens = UntukLexer.tokens

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
        )

    def __init__(self):
        self.env = { }
    @_('')
    def statement(self, p):
        pass

    @_('NAME')
    def expr(self, p):
        return ('var', p.NAME)

    @_('NUMBER')
    def expr(self, p):
        return ('num', p.NUMBER)

    @_('expr')
    def statement(self, p):
        return (p.expr)

    @_('expr "+" expr')
    def expr(self, p):
        return ('add', p.expr0, p.expr1)

    @_('expr "-" expr')
    def expr(self, p):
        return ('sub', p.expr0, p.expr1)

    @_('expr "*" expr')
    def expr(self, p):
        return ('mul', p.expr0, p.expr1)

    @_('expr "/" expr')
    def expr(self, p):
        return ('div', p.expr0, p.expr1)

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return p.expr

    @_('FOR var_assign TO expr THEN statement')
    def statement(self, p):
        return ('for_loop', ('for_loop_setup', p.var_assign, p.expr), p.statement)

    @_('IF condition THEN statement ELSE statement')
    def statement(self, p):
        return ('if_stmt', p.condition, ('branch', p.statement0, p.statement1))

    @_('FUNCTION NAME "(" ")" ARROW statement')
    def statement(self, p):
        return ('function_def', p.NAME, p.statement)

    @_('NAME "(" ")"')
    def statement(self, p):
        return ('function_call', p.NAME)

    @_('expr EQUALITY expr')
    def condition(self, p):
        return ('condition_equality', p.expr0, p.expr1)

    @_('var_assign')
    def statement(self, p):
        return p.var_assign

    @_('NAME "=" expr')
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.expr)

    @_('NAME "=" STRING')
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.STRING)
        
    @_('PRINT expr')
    def expr(self, p):
        return ('print', p.expr)

    @_('PRINT STRING')
    def statement(self, p):
        return ('print', p.STRING)

#Interpreter
class UntukEksekusi:

    def __init__(self, tree, env):
        self.env = env
        result = self.walkTree(tree)
        if result is not None and isinstance(result, int):
            print(result)
        if isinstance(result, str) and result[0] == '"':
            print(result)

    def walkTree(self, node):

        if isinstance(node, int):
            return node
        if isinstance(node, str):
            return node

        if node is None:
            return None

        if node[0] == 'program':
            if node[1] == None:
                self.walkTree(node[2])
            else:
                self.walkTree(node[1])
                self.walkTree(node[2])

        if node[0] == 'num':
            return node[1]

        if node[0] == 'str':
            return node[1]

## Interpreter untuk melakukan PRINT
        if node[0] == 'print':
            if node[1][0] == '"':
                print(node[1][1:len(node[1])-1])
            else:
                return self.walkTree(node[1])

## Interpreter untuk penggunaan IF
        if node[0] == 'if_stmt':
            result = self.walkTree(node[1])
            if result:
                return self.walkTree(node[2][1])
            return self.walkTree(node[2][2])

        if node[0] == 'condition_equality':
            return self.walkTree(node[1]) == self.walkTree(node[2])

## Interpreter untuk penggunaan FUNCTION (fungsi)
        if node[0] == 'function_def':
            self.env[node[1]] = node[2]

        if node[0] == 'function_call':
            try:
                return self.walkTree(self.env[node[1]])
            except LookupError:
                print("Undefined function '%s'" % node[1])
                return 0

## Interpreter untuk operasi perhitungan
        if node[0] == 'add':
            return self.walkTree(node[1]) + self.walkTree(node[2])
        elif node[0] == 'sub':
            return self.walkTree(node[1]) - self.walkTree(node[2])
        elif node[0] == 'mul':
            return self.walkTree(node[1]) * self.walkTree(node[2])
        elif node[0] == 'div':
            return int(self.walkTree(node[1]) / self.walkTree(node[2]))

        if node[0] == 'var_assign':
            self.env[node[1]] = self.walkTree(node[2])
            return node[1]

        if node[0] == 'var':
            try:
                return self.env[node[1]]
            except LookupError:
                print("Undefined variable '"+node[1]+"' found!")
                return 0

## Interpreter untuk penggunaan FOR (perulangan/looping)
        if node[0] == 'for_loop':
            if node[1][0] == 'for_loop_setup':
                loop_setup = self.walkTree(node[1])

                loop_count = self.env[loop_setup[0]]
                loop_limit = loop_setup[1]

                for i in range(loop_count+1, loop_limit+1):
                    res = self.walkTree(node[2])
                    if res is not None:
                        print(res)
                    self.env[loop_setup[0]] = i
                del self.env[loop_setup[0]]

        if node[0] == 'for_loop_setup':
            return (self.walkTree(node[1]), self.walkTree(node[2]))


if __name__ == '__main__':
    lexer = UntukLexer()
    parser = UntukParser()
    env = {}
    while True:
        try:
            text = input('Cek > ')
        except EOFError:
            break
        if text:
            tree = parser.parse(lexer.tokenize(text))
            UntukEksekusi(tree, env)