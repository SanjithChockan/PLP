import parsertwo
import lexer

def evaluate(value):
    if value[0] == lexer.STRING_TOKEN:
        print("Inside of evaluate()")
        print("value[1]: ", value[1])
        return value[1]

def interpreter(prog):
    print("Inside of interpreter()")
    for stmt in prog:
        print("stmt[0]: ", stmt[0])
        if stmt[0] == "print":
            print(evaluate(stmt[1]))

prog = parsertwo.fileInput()
print(prog)
interpreter(prog)