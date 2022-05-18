class Tokens:
    TOKEN_INT = 'INT'
    TOKEN_FLOAT = 'FLOAT'
    TOKEN_STRING = 'STRING'
    TOKEN_IDENTIFIER = 'IDENTIFIER'
    TOKEN_KEYWORD = 'KEYWORD'
    TOKEN_PLUS = 'PLUS'
    TOKEN_MINUS = 'MINUS'
    TOKEN_MUL = 'MUL'
    TOKEN_DIV = 'DIV'
    TOKEN_POW = 'POW'
    TOKEN_EQ = 'EQ'
    TOKEN_LPAREN = 'LPAREN'
    TOKEN_RPAREN = 'RPAREN'
    TOKEN_LSQUARE = 'LSQUARE'
    TOKEN_RSQUARE = 'RSQUARE'
    TOKEN_EE = 'EE'
    TOKEN_NE = 'NE'
    TOKEN_LT = 'LT'
    TOKEN_GT = 'GT'
    TOKEN_LTE = 'LTE'
    TOKEN_GTE = 'GTE'
    TOKEN_COMMA = 'COMMA'
    TOKEN_ARROW = 'ARROW'
    TOKEN_NEWLINE = 'NEWLINE'
    TOKEN_EOF = 'EOF'

    KEYWORDS = [
        'decl',
        'and',
        'or',
        'not',
        'if',
        'elseif',
        'else',
        'for',
        'to',
        'step',
        'while',
        'def',
        'then',
        'end',
        'return',
        'continue',
        'break',
    ]

class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end.copy()

    def matches(self, type_, value):
        return self.type == type_ and self.value == value