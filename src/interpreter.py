from .tokenizer import Tokenizer
from .parser import Parser
from .stack import Stack
from .types import Types

class Interpreter:
    def __init__(self):
        self.program = {}
        self.jump_stack = Stack()
        self.lines = []

    def peek_pgm(self):
        return self.program.copy()

    def dump(self):
        print('pgm:')
        for line, stmt in self.program.items():
            for tok in stmt:
                print(tok)
        print(f'lines: {self.lines}')
        print(f'jump_stack: {self.jump_stack}')

        self.parser.dump()

    def interpret(self, src):
        idx = self.load_program(src)
        next_line = self.lines[0]

        while idx < len(self.lines):
            stmt = self.program[self.lines[idx]]
            (jump_to, state) = self.parser.parse(stmt[1:], stmt[0])

            if state == Types.STATE_GOTO:
                idx = self.lines.index(jump_to)
                next_line = jump_to

            elif state == Types.STATE_LOOP_START:
                self.jump_stack.push(next_line)
                idx += 1
                next_line = self.lines[idx]

            elif state == Types.STATE_LOOP_NORMAL:
                idx = self.lines.index(self.jump_stack.pop())
                next_line = self.lines[idx]

            elif state == Types.STATE_LOOP_DONE:
                idx += 1
                while idx < len(self.lines):
                    toks = self.program[self.lines[idx]]
                    if len(toks) > 1 and toks[0].kind == Types.KW_NEXT \
                       and toks[1].lexeme == jump_to:

                        idx += 1
                        if idx < len(self.lines):
                            next_line = self.lines[idx]
                            break
                    idx += 1

            elif state == Types.STATE_GOSUB:
                if idx + 1 < len(self.lines):
                    self.jump_stack.push(self.lines[idx + 1])
                idx = self.lines.index(jump_to)
                next_line = jump_to

            elif state == Types.STATE_RETURN:
                idx = self.lines.index(self.jump_stack.pop())
                next_line = self.lines[idx]

            elif idx + 1 < len(self.lines):
                idx += 1
                next_line = self.lines[idx]

            else:
                break
    
    def load_program(self, src):
        self.tokenizer = Tokenizer()
        self.parser = Parser()
        first_line = None

        for line in src:
            tokens = self.tokenizer.lex(line)

            if not first_line:
                first_line = int(tokens[0].lexeme)
            self.program[int(tokens[0].lexeme)] = tokens

        self.lines = list(self.program.keys())
        self.lines.sort()
        return self.lines.index(first_line)
