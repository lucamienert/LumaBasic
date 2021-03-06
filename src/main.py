from .interpreter import Interpreter

def main(filename):
    if filename.endswith('.lbas'):
        with open(filename, 'r') as file:
            data = file.read().splitlines()

    interpreter = Interpreter()
    interpreter.interpret(data)
