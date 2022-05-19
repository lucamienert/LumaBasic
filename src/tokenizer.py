from .token import Token
from .types import Types

class Tokenizer:
    def __init__(self):
        self.__pos = 0
        self.__stmt = None

    def lex(self, stmt):
        tokens = []
        self.__pos = 0
        self.__stmt = stmt
        c = self.peek()

        while c is not None:
            while c.isspace():
                c = self.consume()
                if not c.isspace():
                    self.rewind()
                    break
            start_pos = self.__pos + 1

            if c == '"':
                t = self.lex_string(start_pos)
            elif c.isalpha():
                t = self.lex_word(start_pos)
            elif c.isdigit():
                t = self.lex_number(start_pos)
            elif c in Types.SYMBOLS:
                t = self.lex_symbol(start_pos)
            else:
                raise SyntaxError(f"Unknown token starting with '{c}'")

            tokens.append(t)
            c = self.peek()
        return tokens

    def lex_string(self, start_pos):
        self.consume()
        lexeme = ''
        c = self.consume()

        while c is not None:
            if c == '"':
                break
            lexeme += c
            c = self.consume()
        return Token((start_pos, self.__pos), Types.TT_STRING, lexeme)

    def lex_number(self, start_pos):
        lexeme = ''
        c = self.consume()
        is_float = False

        while c is not None:
            if not c.isdigit():
                if c == '.' and not is_float:
                    is_float = True
                else:
                    self.rewind()
                    break
            lexeme += c
            c = self.consume()
        tt = Types.TT_UFLOAT if is_float else Types.TT_UINT
        return Token((start_pos, self.__pos), tt, lexeme)

    def lex_word(self, start_pos):
        lexeme = ''
        c = self.consume()

        while c is not None:
            if not (c.isalnum() or c in ['_', '$']):
                self.rewind()
                break
            lexeme += c
            c = self.consume()

        if lexeme in Types.KEYWORDS:
            tt = Types.KEYWORDS[lexeme]
        else:
            tt = Types.TT_IDENTIFIER
        return Token((start_pos, self.__pos), tt, lexeme.upper())

    def lex_symbol(self, start_pos):
        c = self.consume()
        c2 = self.peek()

        if c is not None and c2 is not None and ((c + c2) in Types.SYMBOLS):
            lexeme = c + self.consume()
        else:
            lexeme = c
        return Token((start_pos, self.__pos), Types.SYMBOLS[lexeme], lexeme)

    def consume(self):
        c = self.peek()
        self.__pos += 1 if c is not None else 0
        return c

    def rewind(self):
        self.__pos -= 1 if self.__pos > 0 else 0

    def peek(self):
        if self.__pos >= len(self.__stmt):
            return None
        return self.__stmt[self.__pos]
