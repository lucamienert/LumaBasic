from interpreter import Interpreter
from parser import Parser
from tokenizer import Tokenizer

import sys

def main():
    filename = sys.argv[1]
    if filename.endswith('.lmath'):
        with open(filename, 'r') as file:
            data = file.read()

    tokenizer = Tokenizer(data)
    tokens = tokenizer.generate_tokens()

    parser = Parser(tokens)
    ast = parser.parse()
    if not ast:
        raise Exception("Not AST!")

    interpreter = Interpreter()
    value = interpreter.visit(ast)
    print(f"[MATH]: {value}")

if __name__ == '__main__':
    main()