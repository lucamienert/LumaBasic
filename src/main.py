from .interpreter import Interpreter

def main(filename):
    if filename.endswith('.luma'):
        with open(filename, 'r') as file:
            data = file.read().splitlines()

    interpreter = Interpreter()
    interpreter.interpret(data)