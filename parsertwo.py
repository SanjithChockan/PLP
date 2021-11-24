import lexer

def lex():
    global nextToken
    global input
    [nextToken, input] = lexer.lex(input)


def parg():
    print("In parg()")
    print("(nextToken[0], nextToken[1]) = (", nextToken[0], ", ", nextToken[1], ")")
    good = (nextToken[0] == lexer.STRING_TOKEN)
    print("Is valid print argument: ", good)
    if not good:
        print("Expected String or Expression")
    # increment to next token
    lex()
    return good

def parsePrint():
    print("In parsePrint()")
    print("(nextToken[0], nextToken[1]) = (", nextToken[0], ", ", nextToken[1], ")")
    if nextToken[0] != lexer.LEXEME:
        return False
    if nextToken[1] == "print":
        # increment to next token
        lex()
        if parg():
            return True
    return False
def parseStmt():
    print("In parseStmt()")
    global nextToken
    global input

    bool_return = parsePrint()

    return bool_return

def parseStmtList():
    print("In parseStmtList()")
    if parseStmt():
        print("parseStmt() returns True")
        print("(nextToken[0], nextToken[1]) = (", nextToken[0], ", ", nextToken[1], ")")
        if nextToken[0] == lexer.LEXEME and nextToken[1] == ";":
            lex()
            # returns True and breaks out of parseStmtList() if it reaches the end of the program
            if nextToken[0] == lexer.END_OF_INPUT:
                return True
            return parseStmtList()
        elif nextToken[0] == lexer.LEXEME and nextToken[1] != ";":
            print("Expected a \";\"")
            return False
        else:
            return True
    return False

def parseProg():
    print("In parseProg()")
    if parseStmtList():
        print("parseStmtList() returns True")
        print("(nextToken[0], nextToken[1]) = (", nextToken[0], ", ", nextToken[1], ")")
        if nextToken[0] != lexer.END_OF_INPUT:
            return parseProg()
        else:
            return True
    return False

filename = input("Enter file name: ")
file = open(filename)
input = list(file.read())
lex()

if nextToken[0] == lexer.ERROR:
    print("Lex Error: ",nextToken[1])
else:
    print("Before if parseProg next token: ", nextToken[0])
    if parseProg():
        if nextToken[0] != lexer.END_OF_INPUT:
          print("Parse Error: unrecognized trailing characters")
        else:
          print("Valid Program")
    else:
        print("Program not Valid")