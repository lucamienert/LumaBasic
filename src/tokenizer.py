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
        c = self.__peek()

        while c is not None:
            while c.isspace():
                c = self.__consume()
                if not c.isspace():
                    self.__rewind()
                    break
            start_pos = self.__pos + 1

            if c == '"':
                t = self.__lex_string(start_pos)
            elif c.isalpha():
                t = self.__lex_word(start_pos)
            elif c.isdigit():
                t = self.__lex_number(start_pos)
            elif c in Types.SYMBOLS:
                t = self.__lex_symbol(start_pos)
            else:
                raise SyntaxError(f"Unknown token starting with '{c}'")

            tokens.append(t)
            c = self.__peek()
        return tokens

    def __lex_string(self, start_pos):
        self.__consume()
        lexeme = ''
        c = self.__consume()

        while c is not None:
            if c == '"':
                break
            lexeme += c
            c = self.__consume()
        return Token((start_pos, self.__pos), Types.TT_STRING, lexeme)

    def __lex_number(self, start_pos):
        lexeme = ''
        c = self.__consume()
        is_float = False

        while c is not None:
            if not c.isdigit():
                if c == '.' and not is_float:
                    is_float = True
                else:
                    self.__rewind()
                    break
            lexeme += c
            c = self.__consume()
        tt = Types.TT_UFLOAT if is_float else Types.TT_UINT
        return Token((start_pos, self.__pos), tt, lexeme)

    def __lex_word(self, start_pos):
        lexeme = ''
        c = self.__consume()

        while c is not None:
            if not (c.isalnum() or c in ['_', '$']):
                self.__rewind()
                break
            lexeme += c
            c = self.__consume()

        if lexeme in Types.KEYWORDS:
            tt = Types.KEYWORDS[lexeme]
        else:
            tt = Types.TT_IDENTIFIER
        return Token((start_pos, self.__pos), tt, lexeme.upper())

    def __lex_symbol(self, start_pos):
        c = self.__consume()
        c2 = self.__peek()

        if c is not None and c2 is not None and ((c + c2) in Types.SYMBOLS):
            lexeme = c + self.__consume()  # two char symbol
        else:
            lexeme = c
        return Token((start_pos, self.__pos), Types.SYMBOLS[lexeme], lexeme)

    def __consume(self):
        c = self.__peek()
        self.__pos += 1 if c is not None else 0
        return c

    def __rewind(self):
        self.__pos -= 1 if self.__pos > 0 else 0

    def __peek(self):
        if self.__pos >= len(self.__stmt):
            return None
        return self.__stmt[self.__pos]
