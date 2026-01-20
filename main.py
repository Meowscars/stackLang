import lexer
import interpreter

file = "script.sl"

with open(file) as f:
    content = f.read()

tokenizer = lexer.Lexer()
runner = interpreter.Interpreter()

tokenizedContent = tokenizer.lex(content)
#print(tokenizedContent)
runner.interpret(tokenizedContent)