import lexer

symtab = {}
isDoWhile = False

def lex():
    global nextToken
    global input
    [nextToken, input] = lexer.lex(input)

def parse_n_expr():
    pTerm = parseTerm()
    if pTerm != False:
        t_expr = parse_t_expr()
        if t_expr != False:
            return pTerm + t_expr
    return False

def parse_t_expr():
    # Complete
    if nextToken[1] == "+" or nextToken[1] == "-":
        # increment to next token
        sign = nextToken[1]
        lex()
        n_expr = parse_n_expr()
        if n_expr != False:
            return [sign] + n_expr
        else:
            return False
    return []

def parseTerm():
    pFactor = parseFactor()
    if pFactor != False:
        f_expr = parse_f_expr()
        if f_expr != False:
            return pFactor + f_expr

def parse_f_expr():
    if nextToken[1] == "*" or nextToken[1] == "/" or nextToken[1] == "%":
        op = nextToken[1]
        # increment to next token
        lex()
        pTerm = parseTerm()
        if pTerm != False:
            return [op] + pTerm
        else:
            return False
    return []

def parseFactor():
    pValue = parseValue()
    if pValue != False:
        v_expr = parse_v_expr()
        if v_expr != False:
            return pValue + v_expr
    return False

def parse_v_expr():
    # Complete
    good = nextToken[1] == ">" or nextToken[1] == ">=" or nextToken[1] == "<" or nextToken[1] == "<=" or nextToken[1] == "==" or nextToken[1] == "!="
    if good:
        # increment to next token
        tmp = nextToken[1]
        lex()
        pValue = parseValue()
        if pValue != False:
            return [tmp] + pValue
        else:
            return False
    return []

def parseValue():
    good = nextToken[0] == lexer.ID_TOKEN or nextToken[0] == lexer.INT_TOKEN
    if good:
        tmp = nextToken
        # increment to next token
        lex()
        return [tmp]
    if nextToken[1] == "-" or nextToken == "not":
        # increment to next token and check whether if it is a valid Value
        lex()
        tmp = nextToken
        pValue = parseValue()
        if pValue != False:
            return ["-", nextToken]
        return False

    if nextToken[1] == "(":
        # increment to next token
        lex()
        if parseExpr():
            if nextToken[1] == ")":
                # increment to next token
                lex()
                return True
    return False

def parse_b_expr():
    if nextToken[1] == "and" or nextToken[1] == "or":
        tmp = nextToken[1]
        # increment to next token
        lex()
        n_expr = parse_n_expr()
        if n_expr != False:
            return [tmp] + n_expr
        else:
            return False
    return []

def parseExpr():
    n_expr = parse_n_expr()
    if n_expr != False:
        b_expr = parse_b_expr()
        if b_expr != False:
            return n_expr + b_expr
    # returns False if expression not Valid
    return False

def parg():
    # Checks if the argument inside of print is either a STRING_TOKEN or a valid expression
    good = (nextToken[0] == lexer.STRING_TOKEN) or parseExpr()
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
    # increment to next Token
    lex()
    #check if token is a valid ID Token
    if nextToken[0] == lexer.ID_TOKEN:
        tmp = nextToken[1]
        # increment to next Token
        lex()
        return ["get", tmp]
    print("Expected ID after \"get\"")
    return False

def parseIf():
    #increment to next Token
    lex()
    # check if expression is valid
    pExpr = parseExpr()
    if pExpr != False:
        if nextToken[1] == "then":
            # increment to next token
            lex()
            parseList = parseStmtList()
            if parseList != False:
                if nextToken[1] == "else":
                    # increment to next token
                    lex()
                    parseList2 = parseStmtList()
                    if parseList2 != False:
                        if nextToken[1] == "end":
                            # increment to next token
                            lex()
                            return ["if", pExpr, parseList, parseList2]
    return False

def parseWhile():
    # increment to next token
    lex()
    pExpr = parseExpr()
    print("pExpr: ", pExpr)
    if pExpr != False:
        if nextToken[1] == "do":
            # increment to next token
            lex()
            print("nextToken: ", nextToken)
            parseList = parseStmtList()
            print("parseList: ", parseList)
            if parseList != False:
                if nextToken[1] == "end":
                    # increment to next token
                    lex()
                    return ["while", pExpr, parseList]
    return False

def parseAssign():
    # increment to next token
    lex()
    if nextToken[1] == "=":
        # incrmeent to next token
        lex()
        if parseExpr():
            return True
    return False

def parseDoWhile():
    global isDoWhile
    isDoWhile = True
    # increment to next token
    lex()
    parseList = parseStmtList()
    if parseList != False:
        if nextToken[1] == "while":
            # increment to next token
            lex()
            pExpr = parseExpr()
            if pExpr != False:
                if nextToken[1] == "end":
                    # increment to next Token
                    lex()
                    #reset isDoWhile
                    isDoWhile = False
                    return ["do", parseList, pExpr]
    return False

def parseStmt():
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
            return []
        return parseWhile()
    elif nextToken[0] == lexer.ID_TOKEN:
        return parseAssign()
    # next two elif statements pertain to if statements
    elif nextToken[1] == "else":
        return True
    # also helps with while and do while loops
    elif nextToken[1] == "end":
        return []

    print("command not found")
    return False

def parseStmtList():
    parse = parseStmt()
    if parse != False:
        if nextToken[0] == lexer.LEXEME and nextToken[1] == ";":
            # increment to next token after end of statement
            lex()
            # returns True and breaks out of parseStmtList() if it reaches the end of the program
            if nextToken[0] == lexer.END_OF_INPUT:
                return [parse]
            return [parse] + parseStmtList()
        # next two if statements pertains to parseIf()
        if nextToken[0] == lexer.LEXEME and nextToken[1] == "else":
            return parse
        if nextToken[0] == lexer.LEXEME and nextToken[1] == "end":
            return parse
        # this if statement takes care of do while
        if nextToken[0] == lexer.LEXEME and nextToken[1] == "while":
            return parse
        elif nextToken[0] == lexer.LEXEME and nextToken[1] != ";":
            print("Expected a \";\"")
            return False
        else:
            return True
    return False

def parseProg():
    parseList = parseStmtList()
    if parseList != False:
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
        prog = parseProg()
        if prog != False:
            if nextToken[0] != lexer.END_OF_INPUT:
              print("Parse Error: unrecognized trailing characters")
            else:
              return prog
        else:
            print("Program not Valid")