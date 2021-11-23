import lexer

def parseError(msg):
    print("Parse Error: " + msg + " at line " + str(lexer.line))

def lex():
    global nextToken
    global input
    [nextToken, input] = lexer.lex(input)

# takes either a STRING or an EXPR
def parg():
    print("At parg(), nextToken[0] == ", nextToken[0])
    good = nextToken[0] == lexer.STRING_TOKEN
    if good:
        lex()
    else:
        parseError("Expected String")
    return good

def parsePrint():
    print("In parsePrint()")
    if nextToken[0] != lexer.LEXEME:
        parseError("Expected command got: " + str(nextToken))
        return False
    if nextToken[1] == "print":
        lex()
        if parg():
            lex()
            return True
    return False

def parseInput():
    print("In parseInput()")
    if nextToken[0] != lexer.LEXEME:
        parseError("Expected command got: " + str(nextToken))
        return False
    if nextToken[1] == "get":
        lex()
        if nextToken[0] == lexer.ID_TOKEN:
            lex()
            print("get returns true!")
            return True
        else:
            parseError("Expected ID")
            return False
    return False

def parseValue():
    print("Inside of parseValue()")
    good = nextToken[0] == lexer.ID_TOKEN or nextToken[0] == lexer.INT_TOKEN
    print("nextToken[0]: ", nextToken[0])
    print("Good value: ", good)
    if good:
        lex()
        return True
    if nextToken[1] == "-" or nextToken[1] == "not":
        lex()
        return True
    if nextToken[1] == "(":
        lex()
        if parseExpr():
            lex()
            if nextToken[1] == ")":
                lex()
                return True
    return False

def parse_v_expr():
    print("Inside of parse_v_expr()")
    print("nextToken[1]: ", nextToken[1])
    good = nextToken[1] == ">" or nextToken[1] == ">=" or nextToken[1] == "<" or nextToken[1] == "<=" or nextToken[1] == "==" or nextToken[1] == "!="
    if good:
        lex()
        if parseValue():
            lex()
            return True

    return False

def parseFactor():
    print("Inside of parseFactor()")
    if parseValue():
        if parse_v_expr():
            lex()
            return True

def parse_f_expr():
    if nextToken[1] == "*" or nextToken[1] == "/" or nextToken[1] == "%":
        if parseTerm():
            lex()
            return True
    return False

def parseTerm():
    print("Inside of parseTerm()")
    if parseFactor():
        if parse_f_expr():
            lex()
            return True

def parse_t_expr():
    if nextToken[1] == "+" or nextToken[1] == "-":
        lex()
        if parse_n_expr():
            lex()
            return True

    return False

def parse_n_expr():
    print("Inside of parse_n_expr()")
    if parseTerm():
        if parse_t_expr():
            lex()
            return True

def parse_b_expr():
    print("Inside of parse_b_expr()")
    print("nextToken[1]", nextToken[1])
    if nextToken[1] == "and" or nextToken[1] == "or":
        lex()
        if parse_n_expr():
            lex()
            return True

    return False

# Fix up this mess! Make sure it goes in right order so the if statement works!
def parseExpr():
    print("Inside of parseExpr()")
    if parse_n_expr():
        if parse_b_expr():
            lex()
            return True

def parseAssign():
    print("In parseAssign()")
    if nextToken[0] != lexer.LEXEME:
        parseError("Expected command got: " + str(nextToken))
        return False
    good = nextToken[0] == lexer.ID_TOKEN
    if good:
        lex()
        if nextToken[0] == lexer.LEXEME and nextToken[1] == '=':
            if parseExpr():
                lex()
                return True

def parseIf():
    print("In parseIf()")
    if nextToken[0] != lexer.LEXEME:
        parseError("Expected command got: " + str(nextToken))
    print("Printing inside of parseIf(): ", nextToken[1])
    if nextToken[1] == "if":
        lex()
        if parseExpr():
            if nextToken[1] == "then":
                lex()
                if parseStmtList():
                    if nextToken[1] == "else":
                        lex()
                        if parseStmtList():
                            if nextToken[1] == "end":
                                lex()
                                return True
    return False

def parseWhile():
    print("In parseWhile()")
    if nextToken[0] != lexer.LEXEME:
        parseError("Expected command got: " + str(nextToken))

    if nextToken[1] == "while":
        lex()
        if parseExpr():
            if nextToken[1] == "do":
                lex()
                if parseStmtList():
                    if nextToken[1] == "end":
                        lex()
                        return True
    return False

def parseDoWhile():
    print("In parseDoWhile()")
    if nextToken[0] != lexer.LEXEME:
        parseError("Expected command got: " + str(nextToken))

    if nextToken[1] == "do":
        lex()
        if parseStmtList():
            if nextToken[1] == "while":
                lex()
                if parseExpr():
                    if nextToken[1] == "end":
                        lex()
                        return True
    return False

def parseStmt():
    print("In parseStmt()")
    global nextToken
    global input
    bool_return = parsePrint() or parseInput() or parseAssign() or parseIf() or parseWhile() or parseDoWhile()

    return bool_return


def parseStmtList():
    print("In parseStmtList()")
    if parseStmt():
        print("After parseStmt()")
        print(nextToken[0], ", ", nextToken[1])
        if nextToken[0] == lexer.LEXEME and nextToken[1] == ";":
            lex()
            return parseStmtList()
        else:
            return True
    else:
        return False

def parseProg():
    print("In parseProg()")
    if parseStmtList():
        if nextToken[0] != lexer.END_OF_INPUT and not (nextToken[0] == lexer.LEXEME and nextToken[1] == "end"):
            return parseProg()
        else:
            return True
    else:
        return False

# Read entire std input into an array
# This is done for convenience. Usually, the lexer would read directly from a file
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
