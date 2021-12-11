import parsertwo
import lexer

def evaluate(value):
    print("Inside evaluate")
    if value[0] == lexer.STRING_TOKEN:
        return value[1]

def interpreter(prog):
    for stmt in prog:
        if stmt[0] == "print":
            print(evaluate(stmt[1]))

        elif stmt[0] == "get":
            parsertwo.symtab[stmt[1]] = int(input("Input Number: "))
    
        elif stmt[0] == "if":
            print("Inside if statement")
            # get left side of expression
            print("stmt[1]: ", stmt[1])
            print("stmt[2]: ", stmt[2])
            if stmt[1][0][0] == lexer.ID_TOKEN:
                reg1 = parsertwo.symtab[stmt[1][0][1]]
            elif stmt[1][0][0] == lexer.INT_TOKEN:
                reg1 = stmt[1][0][1]
            # get right side of expression
            if stmt[1][2][0] == lexer.ID_TOKEN:
                reg2 = parsertwo.symtab[stmt[1][2][1]]
            elif stmt[1][2][0] == lexer.INT_TOKEN:
                reg2 = stmt[1][2][1]

            good = False

            if stmt[1][1] == "<":
                print("Reg1: ", reg1, " Reg2: ", reg2)
                if reg1 < reg2:
                    good = True
            elif stmt[1][1] == "<=":
                print("Reg1: ", reg1, " Reg2: ", reg2)
                if reg1 <= reg2:
                    good = True
            elif stmt[1][1] == ">":
                print("Reg1: ", reg1, " Reg2: ", reg2)
                if reg1 > reg2:
                    good = True
            elif stmt[1][1] == ">=":
                print("Reg1: ", reg1, " Reg2: ", reg2)
                if reg1 >= reg2:
                    good = True
            elif stmt[1][1] == "==":
                print("Reg1: ", reg1, " Reg2: ", reg2)
                if reg1 == reg2:
                    good = True
            elif stmt[1][1] == "!=":
                print("Reg1: ", reg1, " Reg2: ", reg2)
                if reg1 == reg2:
                    good = True
            if good:
                interpreter([stmt[2]])
            elif not good and len(stmt) > 3:
                interpreter([stmt[3]])


prog = parsertwo.fileInput()
print(prog)
interpreter(prog)