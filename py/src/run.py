from parser import Parser
from context import Context
from interpreter import Interpreter
from lexer import Lexer
from values.number import Number
import functions.builtinfunction as bf
from symbol_table import SymbolTable

import math

Number.null = Number(0)
Number.false = Number(0)
Number.true = Number(1)
Number.math_PI = Number(math.pi)

bf.BuiltInFunction.print       = bf.BuiltInFunction("print")
bf.BuiltInFunction.print_ret   = bf.BuiltInFunction("print_ret")
bf.BuiltInFunction.input       = bf.BuiltInFunction("input")
bf.BuiltInFunction.input_int   = bf.BuiltInFunction("input_int")
bf.BuiltInFunction.clear       = bf.BuiltInFunction("clear")
bf.BuiltInFunction.is_number   = bf.BuiltInFunction("is_number")
bf.BuiltInFunction.is_string   = bf.BuiltInFunction("is_string")
bf.BuiltInFunction.is_list     = bf.BuiltInFunction("is_list")
bf.BuiltInFunction.is_function = bf.BuiltInFunction("is_function")
bf.BuiltInFunction.append      = bf.BuiltInFunction("append")
bf.BuiltInFunction.pop         = bf.BuiltInFunction("pop")
bf.BuiltInFunction.extend      = bf.BuiltInFunction("extend")
bf.BuiltInFunction.len			= bf.BuiltInFunction("len")
bf.BuiltInFunction.run			= bf.BuiltInFunction("run")

global_symbol_table = SymbolTable()
global_symbol_table.set("NULL", Number.null)
global_symbol_table.set("FALSE", Number.false)
global_symbol_table.set("TRUE", Number.true)
global_symbol_table.set("MATH_PI", Number.math_PI)
global_symbol_table.set("sysout", bf.BuiltInFunction.print)
global_symbol_table.set("PRINT_RET", bf.BuiltInFunction.print_ret)
global_symbol_table.set("INPUT", bf.BuiltInFunction.input)
global_symbol_table.set("INPUT_INT", bf.BuiltInFunction.input_int)
global_symbol_table.set("CLEAR", bf.BuiltInFunction.clear)
global_symbol_table.set("CLS", bf.BuiltInFunction.clear)
global_symbol_table.set("IS_NUM", bf.BuiltInFunction.is_number)
global_symbol_table.set("IS_STR", bf.BuiltInFunction.is_string)
global_symbol_table.set("IS_LIST", bf.BuiltInFunction.is_list)
global_symbol_table.set("IS_FUN", bf.BuiltInFunction.is_function)
global_symbol_table.set("APPEND", bf.BuiltInFunction.append)
global_symbol_table.set("POP", bf.BuiltInFunction.pop)
global_symbol_table.set("EXTEND", bf.BuiltInFunction.extend)
global_symbol_table.set("LEN", bf.BuiltInFunction.len)
global_symbol_table.set("RUN", bf.BuiltInFunction.run)

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error: 
        return None, error
    
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error: 
        return None, ast.error

    interpreter = Interpreter()
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error