import lexer

symtab = {}
isDoWhile = False

def lex():
    global nextToken
    global input
    [nextToken, input] = lexer.lex(input)

def parse_n_expr():
    print("In parse_n_expr()")
    if parseTerm():
        print("parseTerm() returns True")
        if parse_t_expr():
            print("parse_t_expr() returns True")
            return True
    return False

def parse_t_expr():
    # Complete
    print("In parse_t_expr()")
    if nextToken[1] == "+" or nextToken[1] == "-":
        # increment to next token
        lex()
        if parse_n_expr():
            return True
        else:
            return False
    return True

def parseTerm():
    print("In parseTerm()")
    if parseFactor():
        print("parseFactor returns True")
        if parse_f_expr():
            print("parse_f_expr returns True")
            return True

def parse_f_expr():
    print("Inside parse_f_expr")
    if nextToken[1] == "*" or nextToken[1] == "/" or nextToken[1] == "%":
        print("Debugging in parse_f_expr")
        print("(nextToken[0], nextToken[1]) = (", nextToken[0], ", ", nextToken[1], ")")
        # increment to next token
        lex()
        if parseTerm():
            return True
        else:
            return False
    return True

def parseFactor():
    print("Inside parseFactor()")
    if parseValue():
        print("parseValue() returns True")
        if parse_v_expr():
            print("parse_v_expr() returns True")
            return True
    return False

def parse_v_expr():
    # Complete
    print("In parse_v_expr()")
    good = nextToken[1] == ">" or nextToken[1] == ">=" or nextToken[1] == "<" or nextToken[1] == "<=" or nextToken[1] == "==" or nextToken[1] == "!="
    if good:
        # increment to next token
        lex()
        if parseValue():
            print("parseValue returns True; inside parse_v_expr()")
            return True
        else:
            return False
    return True

def parseValue():
    print("Inside parseValue()")
    good = nextToken[0] == lexer.ID_TOKEN or nextToken[0] == lexer.INT_TOKEN
    if good:
        print("Valid value; Either ID or INT")
        # increment to next token
        print("(nextToken[0], nextToken[1]) = (", nextToken[0], ", ", nextToken[1], ")")
        lex()
        print("(nextToken[0], nextToken[1]) = (", nextToken[0], ", ", nextToken[1], ")")
        return True
    if nextToken[1] == "-" or nextToken == "not":
        # increment to next token and check whether if it is a valid Value
        lex()
        if parseValue():
            return True
        return False

    if nextToken[1] == "(":
        print("Expression starts with opening parenthesis: (")
        # increment to next token
        lex()
        if parseExpr():
            print("parseExpr return True (inside parenthesis)")
            if nextToken[1] == ")":
                print("Expression closes with closing parenthesis: )")
                # increment to next token
                lex()
                return True
    return False

def parse_b_expr():
    print("In parse_b_expr")
    if nextToken[1] == "and" or nextToken[1] == "or":
        # increment to next token
        lex()
        if parse_n_expr():
            print("parse_n_expr() returns True (inside parse_b_expr)")
            return True
        else:
            return False
    return True

def parseExpr():
    print("In parseExpr()")
    if parse_n_expr():
        print("parse_n_expr() returns True")
        if parse_b_expr():
            print("parse_b_expr() return True")
            return True
    # returns False if expression not Valid
    return False

def parg():
    print("In parg()")
    print("(nextToken[0], nextToken[1]) = (", nextToken[0], ", ", nextToken[1], ")")
    # Checks if the argument inside of print is either a STRING_TOKEN or a valid expression
    good = (nextToken[0] == lexer.STRING_TOKEN) or parseExpr()
    print("Is valid print argument: ", good)
    if not good:
        print("Expected String or Expression")
    # increment to next token if it is a string only
    if nextToken[0] == lexer.STRING_TOKEN:
        v = nextToken
        lex()
        return v
    # figure out for expression
    return good

def parsePrint():
    print("In parsePrint()")
    print("(nextToken[0], nextToken[1]) = (", nextToken[0], ", ", nextToken[1], ")")
    if nextToken[0] != lexer.LEXEME:
        return False
    if nextToken[1] == "print":
        # increment to next token
        lex()
        v = parg()
        if v == False:
            return False
        else:
            return ["print", v]
    return False

def parseInput():
    print("In parseInput()")
    # increment to next Token
    lex()
    #check if token is a valid ID Token
    if nextToken[0] == lexer.ID_TOKEN:
        # increment to next Token
        lex()
        return True
    print("Expected ID after \"get\"")
    return False

def parseIf():
    print("In parseIf()")
    #increment to next Token
    lex()
    # check if expression is valid
    if parseExpr():
        print("parseExpr() returns True (inside of parseIf())")
        if nextToken[1] == "then":
            # increment to next token
            lex()
            if parseStmtList():
                print("parseStmtList returns True (inside parseIf() after then)")
                print("Debugging")
                print("(nextToken[0], nextToken[1]) = (", nextToken[0], ", ", nextToken[1], ")")
                if nextToken[1] == "else":
                    # increment to next token
                    lex()
                    if parseStmtList():
                        print("parseStmtList returns True (inside parseIf() after else)")
                        if nextToken[1] == "end":
                            # increment to next token
                            lex()
                            return True
    print("If statement not implemented right")
    return False

def parseWhile():
    print("In parseWhile()")
    # increment to next token
    lex()
    if parseExpr():
        print("parseExpr() returns True")
        if nextToken[1] == "do":
            # increment to next token
            lex()
            if parseStmtList():
                print("parseStmtList() returns True")
                if nextToken[1] == "end":
                    # increment to next token
                    lex()
                    return True
    print("While loop not implemented right")
    return False

def parseAssign():
    print("Inside parseAssign()")
    # increment to next token
    lex()
    if nextToken[1] == "=":
        # incrmeent to next token
        lex()
        if parseExpr():
            print("parseExpr returns True")
            return True
    print("Assigned incorrenctly")
    return False

def parseDoWhile():
    global isDoWhile
    isDoWhile = True
    print("Inside parseDoWhile()")
    # increment to next token
    lex()
    if parseStmtList():
        print("parseStmtList() returns True")
        if nextToken[1] == "while":
            # increment to next token
            lex()
            if parseExpr():
                print("parseExpr() returns True")
                if nextToken[1] == "end":
                    # increment to next Token
                    lex()
                    #reset isDoWhile
                    isDoWhile = False
                    return True
    print("Do while loop wasn't implemented right")
    return False

def parseStmt():
    print("In parseStmt()")
    global nextToken
    global input
    isDoWhile

    if nextToken[1] == "print":
        return parsePrint()
    elif nextToken[1] == "get":
        return parseInput()
    elif nextToken[1] == "if":
        return parseIf()
    elif nextToken[1] == "do":
        return parseDoWhile()
    elif nextToken[1] == "while":
        if isDoWhile:
            return True
        return parseWhile()
    elif nextToken[0] == lexer.ID_TOKEN:
        return parseAssign()
    # next two elif statements pertain to if statements
    elif nextToken[1] == "else":
        return True
    # also helps with while and do while loops
    elif nextToken[1] == "end":
        return True

    print("command not found")
    return False

def parseStmtList():
    print("In parseStmtList()")
    parse = parseStmt()
    if parse != False:
        print("parseStmt() returns True")
        print("(nextToken[0], nextToken[1]) = (", nextToken[0], ", ", nextToken[1], ")")
        if nextToken[0] == lexer.LEXEME and nextToken[1] == ";":
            # increment to next token after end of statement
            lex()
            # returns True and breaks out of parseStmtList() if it reaches the end of the program
            if nextToken[0] == lexer.END_OF_INPUT:
                return [parse]
            return [parse] + parseStmtList()
        # next two if statements pertains to parseIf()
        if nextToken[0] == lexer.LEXEME and nextToken[1] == "else":
            return True
        if nextToken[0] == lexer.LEXEME and nextToken[1] == "end":
            return True
        # this if statement takes care of do while
        if nextToken[0] == lexer.LEXEME and nextToken[1] == "while":
            return True
        elif nextToken[0] == lexer.LEXEME and nextToken[1] != ";":
            print("Expected a \";\"")
            return False
        else:
            return True
    return False

def parseProg():
    print("In parseProg()")
    parseList = parseStmtList()
    if parseList != False:
        print("parseStmtList() returns True")
        print("(nextToken[0], nextToken[1]) = (", nextToken[0], ", ", nextToken[1], ")")
        if nextToken[0] != lexer.END_OF_INPUT:
            return parseList + parseProg()
        else:
            return parseList
    return False

def fileInput():
    global input
    filename = input("Enter file name: ")
    file = open(filename)
    input = list(file.read())
    lex()

    if nextToken[0] == lexer.ERROR:
        print("Lex Error: ",nextToken[1])
    else:
        print("Before if parseProg next token: ", nextToken[0])
        prog = parseProg()
        if prog != False:
            if nextToken[0] != lexer.END_OF_INPUT:
              print("Parse Error: unrecognized trailing characters")
            else:
              return prog
        else:
            print("Program not Valid")