
import ply.lex as lex
import ply.yacc as yacc

reserved = {
    'mod': 'MODULUS',
    'div': 'INTEGER_DIVISION'
}

tokens = [
    'LPAREN',
    'RPAREN',
    'VARIABLE', 
    'INTEGER', 
    'ADDITION', 
    'SUBTRACTION', 
    'MULTIPLICATION', 
    'DIVISION',
    'EXPONENTIATION',
    'ASSIGNMENT' 
] + list(reserved.values())

# token definitions
t_ADDITION = r'\+'
t_SUBTRACTION = r'-'
t_MULTIPLICATION = r'\*'
t_DIVISION = r'/'
t_EXPONENTIATION = r'\*\*'
t_MODULUS = r'\%'
t_INTEGER_DIVISION = r'div'
t_ASSIGNMENT = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_VARIABLE(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'VARIABLE') # check for reserved words
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lex.lex()

# Parsing rules

precedence = (
    ('left', 'ADDITION', 'SUBTRACTION'),
    ('left', 'MULTIPLICATION', 'DIVISION', 'MODULUS', 'INTEGER_DIVISION'),
    ('right', 'EXPONENTIATION'),
    ('right', 'UMINUS'),
    ('left', 'LPAREN', 'RPAREN')
)

# dictionary of names
names = {}

def p_statement_assign(p):
    'statement : VARIABLE ASSIGNMENT expression'
    names[p[1]] = p[3]


def p_statement_expr(p):
    'statement : expression'
    print(p[1])


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
    elif p[2] == '%':
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
    "number : INTEGER"
    p[0] = p[1]

def p_expression_name(p):
    "expression : VARIABLE"
    try:
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

yacc.yacc()

while 1:
    try:
        s = input('calc > ')
    except EOFError:
        break
    if not s:
        continue
    yacc.parse(s)