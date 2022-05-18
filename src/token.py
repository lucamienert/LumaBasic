class Token:
    def __init__(self, pos, kind, lexeme):
        if type(pos) is not tuple:
            raise TypeError(f"Expected pos of type tuple, but got {type(pos)}")

        self.pos = pos
        self.kind = kind
        self.lexeme = lexeme

    def __str__(self):
        s = f"Position=({self.pos[0]}:{self.pos[1]})"
        s += f", Kind={self.kind}"
        s += f", Lexeme='{self.lexeme}'"
        return s