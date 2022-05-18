import math
import random

from .stack import Stack
from .types import Types

class Parser:
    def __init__(self):
        self.index = 0
        self.tokens = []
        self.line_number = 0
        self.symbols = {}
        self.operation_stack = Stack()
        self.program_data = []
        self.out_buffer = []
        self.in_buffer = []

    def peek_symbols(self):
        return self.symbols.copy()

    def peek_data(self):
        return self.program_data.copy()

    def peek_output(self):
        return self.out_buffer.copy()

    def dump(self):
        print(f'symbols: {self.symbols}')
        print(f'data: {self.program_data}')
        print(f'output buffer: {self.out_buffer}')
        print(f'input buffer: {self.in_buffer}')

    def parse(self, tokens, line_no_tok):
        self.index = 0
        self.tokens = tokens
        self.line_number = line_no_tok.lexeme
        self.token = self.tokens[self.index]
        return self.parse_stmt()

    def parse_stmt(self):
        k = self.token.kind
        if k == Types.KW_REM:
            return (None, Types.STATE_NORMAL)
        elif k == Types.TT_IDENTIFIER:
            self.parse_assign()
            return (None, Types.STATE_NORMAL)
        elif k in self.PARSE_DICT:
            return self.PARSE_DICT[k](self)
        self.parser_raise('Unexpected statement found')

    def consume(self):
        self.index += 1
        if not self.index >= len(self.tokens):
            self.token = self.tokens[self.index]

    def parser_raise(self, msg, err_type=SyntaxError):
        e = f"{msg} on line {self.line_number}\n\tcurrent token: {self.token}"
        raise err_type(e)

    def assert_syntax(self, expected_kind):
        actual_kind = self.token.kind
        if actual_kind != expected_kind:
            actual = self.get_token_name(actual_kind)
            expected = self.get_token_name(expected_kind)
            self.parser_raise(f"Expected '{expected}', but got '{actual}'")

    def get_token_name(self, tok_id):
        if tok_id >= 0 and tok_id <= 3:
            return ["STRING", "INT", "FLOAT", "IDENTIFIER"][tok_id]
        for k, v in Types.KEYWORDS.items():
            if v == tok_id:
                return k
        for k, v in Types.SYMBOLS.items():
            if v == tok_id:
                return k
        raise Exception(f'Could not find token with ID {tok_id}')

    def is_rel_op(self, t):
        return t in [Types.SYM_LT, Types.SYM_LE, Types.SYM_EQ,
                     Types.SYM_GE, Types.SYM_GT, Types.SYM_NE]

    def pop_two(self):
        return (self.operation_stack.pop(), self.operation_stack.pop())

    def parse_assign(self):
        var = self.token.lexeme
        self.consume()

        if self.token.kind == Types.SYM_EQ:
            self.consume()
            self.parse_expr_logic()
            self.symbols[var] = self.operation_stack.pop()
        elif self.token.kind == Types.SYM_LPAREN:
            self.parse_assign_arr(f'@{var}')
        else:
            self.parser_raise(f"Could not assign variable '{var}'")

    def parse_assign_arr(self, var):
        self.assert_syntax(Types.SYM_LPAREN)
        self.consume()
        indices = self.parse_list([Types.SYM_COMMA])

        if var not in self.symbols:
            self.parser_raise(f"Array '{var[1:]}' is undefined", KeyError)
        dims = self.get_array_dimension(self.symbols[var])
        dim_len = len(dims)

        if dim_len != len(indices):
            self.parser_raise(f"Invalid access to array '{var[1:]}'", IndexError)
        self.assert_syntax(Types.SYM_RPAREN)
        self.consume()                                 # )
        self.assert_syntax(Types.SYM_EQ)
        self.consume()                                 # =

        self.parse_expr()
        val = self.operation_stack.pop()

        try:
            if dim_len == 1:
                self.symbols[var][indices[0]-1] = val
            elif dim_len == 2:
                self.symbols[var][indices[0]-1][indices[1]-1] = val
            elif dim_len == 3:
                self.symbols[var][indices[0]-1][indices[1]-1][indices[2]-1] = val
            else:
                self.parser_raise('Invalid array dimensions', RuntimeError)
        except IndexError as e:
            self.parser_raise('Array index out of bounds', e)

    def parse_data(self):
        self.consume()
        self.program_data.extend(self.parse_list([Types.SYM_COMMA]))
        return (None, Types.STATE_NORMAL)

    def parse_dim(self):
        self.consume()
        var = f'@{self.token.lexeme}'
        self.consume()
        self.assert_syntax(Types.SYM_LPAREN)
        self.consume()
        dims = self.parse_list([Types.SYM_COMMA])
        self.assert_syntax(Types.SYM_RPAREN)
        self.consume()
        dim_len = len(dims)

        if dim_len == 0:
            self.parser_raise('Array declared with no dimensions')
        elif dim_len < 0:
            self.parser_raise('Array declared with invalid dimensions')
        elif dim_len > 3:
            self.parser_raise('Array declared with too many dimensions')

        if dim_len == 1:
            arr_init = [0] * (dims[0]+1)
        elif dim_len == 2:
            arr_init = [[0] * (dims[0]+1) for i in range(dims[1]+1)]
        elif dim_len == 3:
            arr_init = [[[0] * (dims[0]+1) for i in range(dims[1]+1)] for j in range(dims[2]+1)]

        self.symbols[var] = arr_init

        return (None, Types.STATE_NORMAL)

    def parse_end(self):
        return (None, Types.STATE_HALT)

    def parse_list(self, delimiters):
        vals = []
        if not self.index >= len(self.tokens):
            self.parse_expr()
            vals.append(self.operation_stack.pop())

            while self.token.kind in delimiters:
                self.consume()
                self.parse_expr()
                vals.append(self.operation_stack.pop())

        return vals

    def parse_expr(self):
        self.parse_term()

        while self.token.kind in [Types.SYM_ADD, Types.SYM_SUB]:
            op = self.token.kind
            self.consume()
            self.parse_term()
            (r, l) = self.pop_two()
            self.operation_stack.push((l + r) if op == Types.SYM_ADD else (l - r))

    def parse_term(self):
        self.parse_factor()
        while self.token.kind in [Types.SYM_MUL, Types.SYM_DIV, Types.SYM_MOD]:
            op = self.token.kind
            self.consume()
            self.parse_factor()
            (r, l) = self.pop_two()

            if op == Types.SYM_MUL:
                self.operation_stack.push(l * r)
            elif op == Types.SYM_DIV:
                self.operation_stack.push(l / r)
            else:
                self.operation_stack.push(l % r)

    def parse_factor(self):
        if self.token.kind == Types.TT_STRING:
            self.operation_stack.push(self.token.lexeme)
            self.consume()

        elif self.token.kind == Types.TT_UINT:
            self.operation_stack.push(int(self.token.lexeme))
            self.consume()

        elif self.token.kind == Types.TT_UFLOAT:
            self.operation_stack.push(float(self.token.lexeme))
            self.consume()

        elif self.token.kind == Types.TT_IDENTIFIER:
            var = self.token.lexeme

            if f'@{var}' in self.symbols:
                self.parse_factor_array()
            elif var in self.symbols:
                self.operation_stack.push(self.symbols[var])
            else:
                self.parser_raise(f"Variable '{var}' is undefined")
            self.consume()

        elif self.token.kind in self.BIF_DICT:
            self.parse_bif()

        elif self.token.kind == Types.SYM_LPAREN:
            self.consume()
            self.parse_expr_logic()
            self.consume()

        else:
            self.parser_raise('Unexpected value for factor', RuntimeError)

    def parse_bif(self):
        bif = self.token.lexeme
        bif_kind = self.token.kind
        self.consume()
        self.assert_syntax(Types.SYM_LPAREN)
        self.consume()
        self.parse_expr()

        try:
            val = self.operation_stack.pop()
            self.operation_stack.push(self.BIF_DICT[bif_kind](self, val))
        except TypeError as e_t:
            self.parser_raise(f'Invalid argument type given to {bif}', e_t)
        except ValueError as e_v:
            self.parser_raise(f'Invalid argument given to {bif}', e_v)

        self.assert_syntax(Types.SYM_RPAREN)
        self.consume()

    def parse_factor_array(self):
        var = f'@{self.token.lexeme}'
        self.consume()
        self.assert_syntax(Types.SYM_LPAREN)
        self.consume()
        indices = self.parse_list([Types.SYM_COMMA])
        self.assert_syntax(Types.SYM_RPAREN)
        self.consume()
        elem = self.__get_arr_elem(self.symbols[var], indices)
        self.operation_stack.push(elem)

    def __get_arr_elem(self, arr, indices):
        dims = len(indices)
        if dims != len(self.get_array_dimension(arr)):
            self.parser_raise('Array dimension mismatch', RuntimeError)
        try:
            if dims == 1:
                return arr[indices[0]-1]
            elif dims == 2:
                return arr[indices[0]-1][indices[1]-1]
            elif dims == 3:
                return arr[indices[0]-1][indices[1]-1][indices[2]-1]
        except IndexError as e:
            self.parser_raise('Array index out of bounds', e)

    def get_array_dimension(self, arr):
        if not type(arr) == list:
            return []
        return [len(arr)] + self.get_array_dimension(arr[0])

    def parse_expr_logic(self):
        if self.token.kind == Types.KW_NOT:
            self.parse_not()
        else:
            self.parse_expr_rel()

        while self.token.kind in [Types.KW_AND, Types.KW_OR, Types.KW_XOR]:
            op = self.token.kind
            self.consume()

            if self.token.kind == Types.KW_NOT:
                self.parse_not()
            else:
                self.parse_expr_rel()
            (r, l) = self.pop_two()

            if op == Types.KW_AND:
                val = l and r
            elif op == Types.KW_OR:
                val = l or r
            else:
                val = l ^ r
            self.operation_stack.push(val)

    def parse_expr_rel(self):
        self.parse_expr()

        if self.is_rel_op(self.token.kind):
            op = self.token.kind
            self.consume()
            self.parse_expr()
            (r, l) = self.pop_two()

            if op == Types.SYM_LT:
                val = l < r
            elif op == Types.SYM_LE:
                val = l <= r
            elif op == Types.SYM_EQ:
                val = l == r
            elif op == Types.SYM_GE:
                val = l >= r
            elif op == Types.SYM_GT:
                val = l > r
            elif op == Types.SYM_NE:
                val = l != r
            self.operation_stack.push(val)

    def parse_for(self):
        self.consume()
        var = self.token.lexeme
        self.consume()
        self.assert_syntax(Types.SYM_EQ)
        self.consume()

        self.parse_expr()
        start = self.operation_stack.pop()
        self.assert_syntax(Types.KW_TO)
        self.consume()

        self.parse_expr()
        end = self.operation_stack.pop()

        step = 1
        if self.index < len(self.tokens):
            self.assert_syntax(Types.KW_STEP)
            self.consume()
            self.parse_expr()
            step = self.operation_stack.pop()

        self.symbols[var] += step

        if self.symbols[var] > end and step > 0:
            return (self.symbols[var], Types.STATE_LOOP_DONE)
        elif self.symbols[var] < end and step < 0:
            return (self.symbols[var], Types.STATE_LOOP_DONE)
        return (None, Types.STATE_LOOP_START)

    def parse_next(self):
        self.consume()
        return (None, Types.STATE_LOOP_NORMAL)

    def parse_gosub(self):
        self.consume()
        self.parse_expr()
        return (self.operation_stack.pop(), Types.STATE_GOSUB)

    def parse_return(self):
        self.consume()
        return (None, Types.STATE_RETURN)

    def parse_goto(self):
        self.consume()
        self.parse_expr()
        return (self.operation_stack.pop(), Types.STATE_GOTO)

    def parse_if(self):
        self.consume()
        self.parse_expr_logic()
        cond = self.operation_stack.pop()

        self.assert_syntax(Types.KW_THEN)
        self.consume()

        if self.token.kind == Types.KW_GOTO:
            self.consume()
        self.parse_expr()

        if cond:
            return (self.operation_stack.pop(), Types.STATE_GOTO)

        if self.token.kind == Types.KW_ELSE:
            self.consume()

            if self.token.kind == Types.KW_GOTO:
                self.consume
            self.parse_expr()
            return (self.operation_stack.pop(), Types.STATE_GOTO)
        return (None, Types.STATE_NORMAL)

    def parse_input(self):
        self.consume()

        if self.token.kind == Types.TT_STRING:
            self.parse_expr_logic()
            prompt = self.operation_stack.pop()
            self.assert_syntax(Types.SYM_SEMICOLON)
            self.consume()
        else:
            prompt = '?'

        var_list = self.parse_list()
        for var in var_list:
            try:
                self.symbols[var] = input(prompt)
            except Exception:
                self.parser_raise(f'Error reading input into {var}', RuntimeError)
        return (None, Types.STATE_NORMAL)

    def parse_let(self):
        self.consume()
        self.parse_assign()
        return (None, Types.STATE_NORMAL)

    def parse_not(self):
        self.consume()
        self.parse_expr_rel()
        self.operation_stack.push(not self.operation_stack.pop())

    def parse_sysout(self):
        buffer = ''
        self.consume()
        if not self.index >= len(self.tokens):
            zones = self.parse_list([Types.SYM_COMMA, Types.SYM_SEMICOLON])
            buffer = ''.join(map(str, zones))
        print(buffer)
        self.out_buffer.append(buffer)
        return (None, Types.STATE_NORMAL)

    def parse_read(self):
        self.consume()
        var_list = self.parse_list([Types.SYM_COMMA])

        try:
            for var in var_list:
                self.symbols[var] = self.program_data.pop(0)
        except Exception:
            self.parser_raise("Error reading data", RuntimeError)
        return (None, Types.STATE_NORMAL)

    def abs(self, val):
        return abs(val)

    def asc(self, val):
        return ord(val)

    def atn(self, val):
        return math.atan(val)

    def chr(self, val):
        return chr(val)

    def cos(self, val):
        return math.cos(val)

    def exp(self, val):
        return math.exp(val)

    def int(self, val):
        return math.floor(val)

    def left(self, val):
        args = self.parse_list([Types.SYM_COMMA])
        if len(args) != 2:
            self.parser_raise(f'Expected 2 arguments, but got {len(args)}')
        return str(val[0:args[2]])

    def len(self, val):
        return len(val)

    def log(self, val):
        return math.log(val)

    def mid(self, val):
        args = self.parse_list([Types.SYM_COMMA])
        if len(args) != 3:
            self.parser_raise(f'Expected 3 arguments, but got {len(args)}')
        return str(val[args[1]:args[2]])

    def right(self, val):
        args = self.parse_list([Types.SYM_COMMA])
        if len(args) != 2:
            self.parser_raise(f'Expected 2 arguments, but got {len(args)}')
        return str(val[args[2]:-1])

    def rnd(self, val):
        if self.token.kind == Types.SYM_RPAREN:
            args = [val]
        else:
            args = self.parse_list([Types.SYM_COMMA])

        if len(args) == 1:
            return random.randrange(args[0])
        elif len(args) == 2:
            return random.randrange(args[1], args[2])
        else:
            self.parser_raise(f'Expected 1 or 2 arguments, but got {len(args)}')

    def sgn(self, val):
        if val < 0:
            return -1
        if val > 0:
            return 1
        return 0

    def sin(self, val):
        return math.sin(val)

    def spc(self, val):
        return ' ' * val

    def sqr(self, val):
        return math.sqrt(val)

    def str(self, val):
        return str(val)

    def tan(self, val):
        return math.tan(val)

    PARSE_DICT = {
        Types.KW_DATA: parse_data, 
        Types.KW_DIM: parse_dim,
        Types.KW_END: parse_end, 
        Types.KW_FOR: parse_for,
        Types.KW_GOSUB: parse_gosub, 
        Types.KW_GOTO: parse_goto,
        Types.KW_IF: parse_if, 
        Types.KW_INPUT: parse_input,
        Types.KW_LET: parse_let, 
        Types.KW_SYSOUT: parse_sysout,
        Types.KW_READ: parse_read, 
        Types.KW_NEXT: parse_next
    }

    BIF_DICT = {
        Types.KW_ABS: abs, Types.KW_ASC: asc,
        Types.KW_ATN: atn, Types.KW_CHR: chr,
        Types.KW_COS: cos, Types.KW_EXP: exp,
        Types.KW_INT: int, Types.KW_LEFT: left,
        Types.KW_LEN: len, Types.KW_LOG: log,
        Types.KW_MID: mid, Types.KW_RIGHT: right,
        Types.KW_RND: rnd, Types.KW_SGN: sgn,
        Types.KW_SIN: sin, Types.KW_SPC: spc,
        Types.KW_SQR: sqr, Types.KW_STR: str,
        Types.KW_TAN: tan,
    }
