import run as run
import sys

filename = sys.argv[1]

def main():
    if filename.endswith('.luma'):
        with open(filename, 'r') as file:
            data = file.read()
    else:
        print('File must end with ".luma"')
        exit()

    result, error = run.run('<stdin>', data)

    if error:
        print(error.as_string())
    elif result:
        if len(result.elements) == 1:
            print(repr(result.elements[0]))
        else:
            print(repr(result))

if __name__ == '__main__':
    main()
