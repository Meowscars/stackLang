import lexer
import interpreter
from sys import argv, exit

def readFile(file):
    with open(file) as f:
        content = f.read()
    return content

def startCycle(contents):
    lex  = lexer.Lexer()
    interpret = interpreter.Interpreter()

    result = lex.lex(contents)

    interpret.interpret(result)

if __name__ == "__main__":
    if len(argv) == 2:
        filePath = argv[1]
    else:
        exit("No file name!")
    
    startCycle(readFile(filePath))