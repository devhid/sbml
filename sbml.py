from lexer import tokens
import ply.yacc as yacc

# precedence for rules
precedence = (
    ('left', 'DISJUNCTION'),
    ('left', 'CONJUNCTION'),
    ('left', 'LESS_THAN', 'LESS_THAN_EQUAL', 'GREATER_THAN', 'GREATER_THAN_EQUAL', 'EQUAL_TO', 'NOT_EQUAL_TO'),
    ('left', 'ADDITION', 'SUBTRACTION'),
    ('left', 'MULTIPLICATION', 'DIVISION', 'MODULUS', 'INTEGER_DIVISION'),
    ('right', 'EXPONENTIATION'),
    ('right', 'UMINUS'),
    ('left', 'LBRACKET', 'RBRACKET'),
    ('left', 'HASHTAG'),
    ('left', 'LPAREN', 'RPAREN')
)

# dictionary of names
names = {}

# to handle list operations
lst = []

# temp tuple list
tup_list = []

def p_statement_assign(p):
    "statement : VARIABLE ASSIGNMENT expression"
    names[p[1]] = p[3]


def p_statement_expr(p):
    """
    statement : expression
              | boolean_expr
              | boolean_comparison
    """
    p[0] = p[1]

def p_boolean_expr(p):
    """
    boolean_expr : boolean_conjunction
                 | boolean_disjunction
                 | boolean_negation
    """
    p[0] = p[1]

def p_boolean_conjunction(p):
    "boolean_conjunction : boolean_comparison CONJUNCTION boolean_comparison"
    p[0] = p[1] and p[3]

def p_boolean_disjunction(p):
    "boolean_disjunction : boolean_comparison DISJUNCTION boolean_comparison"
    p[0] = p[1] or p[3]

def p_boolean_negation(p):
    "boolean_negation : NEGATION boolean_comparison"
    p[0] = not p[2]

def p_boolean_comparison(p):
    """
    boolean_comparison : boolean
                       | expression LESS_THAN expression
                       | expression LESS_THAN_EQUAL expression
                       | expression GREATER_THAN expression
                       | expression GREATER_THAN_EQUAL expression
                       | expression EQUAL_TO expression
                       | expression NOT_EQUAL_TO expression
    """

    if len(p) == 2:
        p[0] = p[1]
    else:
        if p[2] == '<':
            p[0] = p[1] < p[3]
        elif p[2] == '<=':
            p[0] = p[1] <= p[3]
        elif p[2] == '>':
            p[0] = p[1] > p[3]
        elif p[2] == '>=':
            p[0] = p[1] > p[3]
        elif p[2] == '==':
            p[0] = p[1] == p[3]
        elif p[2] == '<>':
            p[0] = p[1] != p[3]
    
def p_boolean(p):
    """
    boolean : BOOLEAN_TRUE
            | BOOLEAN_FALSE
    """
    p[0] = p[1]

def p_expression_binop(p):
    """
    expression : expression ADDITION expression
               | expression SUBTRACTION expression
               | expression MULTIPLICATION expression
               | expression DIVISION expression
               | expression INTEGER_DIVISION expression
               | expression MODULUS expression
               | expression EXPONENTIATION expression
    """
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]
    elif p[2] == 'div':
        p[0] = p[1] // p[3]
    elif p[2] == 'mod':
        p[0] = p[1] % p[3]
    elif p[2] == '**':
        p[0] = p[1] ** p[3]


def p_expression_uminus(p):
    "expression : SUBTRACTION expression %prec UMINUS"
    p[0] = -p[2]

def p_expression_group(p):
    "expression : LPAREN expression RPAREN"
    p[0] = p[2]

def p_expression_number(p):
    "expression : number"
    p[0] = p[1]

def p_number(p):
    """
    number : INTEGER
           | REAL
    """
    p[0] = p[1]

def p_expression_indexing(p):
    "expression : indexing"
    p[0] = p[1]

def p_indexing(p):
    """
    indexing : indexing_string
             | indexing_list
             | indexing_tuple
    """
    p[0] = p[1]

def p_indexing_tuple(p):
    "indexing_tuple : HASHTAG INTEGER tuple"

    # indices start at 1 in SML so we subtract 1
    p[2] = p[2] - 1

    if p[2] < 0 or p[2] >= len(p[3]):
        print("SEMANTIC ERROR")
        return
    
    p[0] = p[3][p[2]]

def p_indexing_list(p):
    "indexing_list : list LBRACKET expression RBRACKET"

    expr_type = type(p[3]).__name__

    if expr_type != 'int': # make sure expression is not a string, can't index with that.
        print("SEMANTIC ERROR")
    
    if p[3] < 0 or p[3] >= len(p[1]):
        print("SEMANTIC ERROR")
    
    p[0] = p[1][p[3]]

def p_indexing_string(p):
    "indexing_string : STRING LBRACKET expression RBRACKET"

    p[1] = p[1][1:-1] # trim quotes

    expr_type = type(p[3]).__name__

    if expr_type != 'int': # make sure expression is not a string, can't index with that.
        print("SEMANTIC ERROR")
        return
    
    if p[3] < 0 or p[3] >= len(p[1]):
        print("SEMANTIC ERROR")
        return
    
    p[0] = p[1][p[3]]

def p_list(p): # @TODO clean up the code here too if possible
    """
    list : LBRACKET element list_tail RBRACKET
         | LBRACKET RBRACKET
    """
    global lst

    if p[2] != ']':
        p[0] = [p[2]]

    if len(p) > 3:
        p[0] += p[3]
    
    lst = []

def p_list_tail(p):
    """
    list_tail : COMMA element list_tail
              | empty
    """
    global lst

    if len(p) > 2:
        lst = [p[2]] + lst
        
        if len(p) > 3:
            for i in range(4, len(p) - 1, 2):
                lst = p[i] + lst
    
    p[0] = lst

def p_tuple(p):
    "tuple : LPAREN element COMMA element tuple_tail RPAREN"
    p[0] = tuple([p[2], p[4]] + p[5])

def p_tuple_tail(p):
    """
    tuple_tail : COMMA element tuple_tail
               | empty
    """
    global tup_list

    if len(p) > 2:
        tup_list = [p[2]] + tup_list
        
        if len(p) > 3:
            for i in range(4, len(p) - 1, 2):
                tup_list = p[i] + tup_list
    
    p[0] = tup_list


def p_element(p):
    """
    element : expression
            | STRING
    """
    p[0] = p[1]

def p_expression_name(p):
    "expression : VARIABLE"
    try:
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p)
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

input_file = 'parse.txt'
with open(input_file) as fd:
    for line in fd:
        result = parser.parse(line.strip())
        print(line.strip() + ' = ' + str(result))
        

# while True:
#     try:
#         s = input('calc > ')
#     except EOFError:
#         break
#     if not s:
#         continue
#     print(parser.parse(s))