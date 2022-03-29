from sly import Lexer
import lexercoba

if __name__ == '__main__':
    lexer = lexercoba.UntukLexer()
    env = {}
      
    while True:
          
        try:
            text = input('Cek > ')
          
        except EOFError:
            break
          
        if text:
            lex = lexer.tokenize(text)
            for token in lex:
                print(token)
