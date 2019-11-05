import ply.lex as lex

reserved = {
    'mod': 'MODULUS',
    'div': 'INTEGER_DIVISION',
    'orelse': 'DISJUNCTION',
    'andalso': 'CONJUNCTION',
    'not': 'NEGATION',
    'False': 'BOOLEAN_FALSE',
    'True': 'BOOLEAN_TRUE',
    'in': 'MEMBERSHIP'
}

tokens = [
    'LBRACKET', 'RBRACKET',
    'LPAREN','RPAREN',
    'VARIABLE', 
    'ADDITION', 'SUBTRACTION', 
    'MULTIPLICATION', 'DIVISION',
    'EXPONENTIATION',
    'ASSIGNMENT',
    'STRING','REAL', 'INTEGER',
    'LESS_THAN', 'LESS_THAN_EQUAL', 'GREATER_THAN', 'GREATER_THAN_EQUAL', 'EQUAL_TO', 'NOT_EQUAL_TO',
    'COMMA', 'HASHTAG'
] + list(reserved.values())

### Token Definitions ###

# general
t_ASSIGNMENT = r'='

# for lists
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r','

# for tuple
t_HASHTAG = r'\#'

# for arithmetic
t_ADDITION = r'\+'
t_SUBTRACTION = r'-'
t_MULTIPLICATION = r'\*'
t_DIVISION = r'/'
t_EXPONENTIATION = r'\*\*'
t_MODULUS = r'mod'
t_INTEGER_DIVISION = r'div'
t_LPAREN = r'\('
t_RPAREN = r'\)'

# comparison
t_LESS_THAN = r'<'
t_LESS_THAN_EQUAL = r'<='
t_GREATER_THAN = r'>'
t_GREATER_THAN_EQUAL = r'>='
t_EQUAL_TO = r'=='
t_NOT_EQUAL_TO =r'<>'

# boolean logic
t_CONJUNCTION = r'andalso'
t_DISJUNCTION = r'orelse'
t_NEGATION = r'not'
t_MEMBERSHIP = r'in'

def t_STRING(t):
    r'(\'[\w\W]*\'|\"[\w\W]*\")'
    t.value = t.value
    return t

# rule for reals
def t_REAL(t):
    r'(\d*\.\d+|\d+\.\d*)(e-?\d+)?'
    t.value = eval(t.value)
    return t

def t_VARIABLE(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'VARIABLE') # check for reserved words
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_BOOLEAN_FALSE(t):
    r'False'
    t.value = bool(t.value)
    return t

def t_BOOLEAN_TRUE(t):
    r'True'
    t.value = bool(t.value)
    return t

t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# while True:
#     lexer.input(input())
#     tok = lexer.token()
#     if not tok:
#         break
#     print(tok) 