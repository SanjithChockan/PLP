import lexer

def parseError(msg):
    print("Parse Error: " + msg + " at line " + str(lexer.line))

def lex():
    global nextToken
    global input
    [nextToken, input] = lexer.lex(input)

def parg():
    good = nextToken[0] == lexer.STRING_TOKEN
    if good:
        lex()
    else:
        parseError("Expected String")
    return good

def parsePrint():
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
    if nextToken[0] != lexer.LEXEME:
        parseError("Expected command got: " + str(nextToken))
        return False
    if nextToken[1] == "get":
        lex()
        if nextToken[0] == lexer.ID_TOKEN:
            lex()
            return True
        else:
            parseError("Expected ID")
            return False
    return False

def parseValue():
    good = nextToken[0] == lexer.ID_TOKEN or nextToken[0] == lexer.INT_TOKEN
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
    good = nextToken[1] == ">" or nextToken[1] == ">=" or nextToken[1] == "<" or nextToken[1] == "<=" or nextToken[1] == "==" or nextToken[1] == "!="
    if good:
        lex()
        if parseValue():
            lex()
            return True

    return False

def parseFactor():
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
    if parseTerm():
        if parse_t_expr():
            lex()
            return True

def parse_b_expr():
    if nextToken[1] == "and" or nextToken[1] == "or":
        lex()
        if parse_n_expr():
            lex()
            return True

    return False

def parseExpr():
    if parse_n_expr():
        if parse_b_expr():
            lex()
            return True

def parseAssign():
    if nextToken[0] != lexer.LEXEME:
        parseError("Expected command got: " + str(nextToken))
        return False
    good = nextToken[0] == lexer.ID_TOKEN
    if good():
        lex()
        if nextToken[0] == lexer.LEXEME and nextToken[1] == '=':
            if parseExpr():
                lex()
                return True

def parseIf():
    if nextToken[0] != lexer.LEXEME:
        parseError("Expected command got: " + str(nextToken))
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
    global nextToken
    global input
    bool_return = parsePrint() or parseInput() or parseAssign() or parseIf() or parseWhile() or parseDoWhile()

    return bool_return


def parseStmtList():
    if parseStmt():
        if nextToken[0] == lexer.LEXEME and nextToken[1] == ";":
            lex()
            return parseStmtList()
        else:
            return True
    else:
        return False

def parseProg():
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
    if parseProg():
        if nextToken[0] != lexer.END_OF_INPUT:
          print("Parse Error: unrecognized trailing characters")
        else:
          print("Valid Program")

