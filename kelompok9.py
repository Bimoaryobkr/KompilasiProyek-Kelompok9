#CONSTANTA
from distutils.log import error
from lib2to3.pgen2 import token


DIGITS = '0123456789'
ABJAD = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

# PESAN ERROR 

class Error:
    def __init__(self, pos_start, pos_end,  error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        result += f'File {self.pos_start.fn}, Baris {self.pos_start.ln + 1 }'
        return result
class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end,'Karakter tidak diketahui', details)

# POSISI ERROR

class Posisi:
    def __init__(self, indx, ln, col, fn,ftxt ):
        self.indx = indx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt=ftxt

    def advance(self, currenct_char):
        self.indx += 1
        self.col += 1

        if currenct_char == '\n':
            self.ln += 1
            self.col = 0
        return

    def copy(self):
        return Posisi(self.indx, self.ln, self.col, self.fn, self.ftxt)

# INISIALISASI TOKEN
TT_INT='INT'
TT_FLOAT='FLOAT'
TT_PLUS='OPERATOR TAMBAH'
TT_MINUS='OPERATOR KURANG'
TT_MUL='OPERATOR KALI'
TT_DIV='OPERATOR BAGI'
TT_LPAREN='KURUNG BUKA'
TT_RPAREN='KURUNG TUTUP'
TT_CABD='KAREKTER ABJAD'

class Token:
    def __init__(self,type_,value=None):
        self.type=type_
        self.value=value
    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

# INI BAGIAN LEXER
class Lexer:
    def __init__(self,fn, text):
        self.fn = fn
        self.text=text
        self.pos= Posisi(-1, 0, -1, fn, text)
        self.current_char=None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.indx] if self.pos.indx < len(self.text) else None

    def make_tokens(self):
        tokens = []
        while self.current_char !=None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char in ABJAD:
                tokens.append(self.make_abc())

            elif self.current_char =='+':
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.current_char =='-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.current_char =='*':
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.current_char =='/':
                tokens.append(Token(TT_DIV))
                self.advance()
            elif self.current_char =='(':
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.current_char ==')':
                tokens.append(Token(TT_RPAREN))
                self.advance()
            else:
                pos_start= self.pos.copy()
                char = self.current_char
                self.advance()
                return[], IllegalCharError(pos_start,self.pos, "'" + char + "'")

        return tokens, None

    def make_number(self):
        num_str=''
        dot_count=0

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1 : break
                dot_count += 1
                num_str +='.'
            else:
                num_str += self.current_char
            self.advance()
        if dot_count == 0:
            return Token(TT_INT, int(num_str))
        else:
            return Token(TT_FLOAT, float(num_str))
            
    def make_abc(self):
        num_abc=''
        dot_abc=0

        while self.current_char != None and self.current_char in ABJAD:
            if self.current_char == '/t':
                if dot_abc == 1 : break
                dot_abc += 1
                num_abc +='/t'
            else:
                num_abc += self.current_char
            self.advance()
            return Token(TT_CABD,num_abc)

# Menjalankan (RUN) File

def Run(fn, text):
    lexer= Lexer(fn, text)
    token, error = lexer.make_tokens()

    return token, error
