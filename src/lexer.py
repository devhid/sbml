# system imports
import sys

# internal imports
from utils import *

# external imports
import ply.lex as lex

reserved = {
    'mod': 'MODULUS',
    'div': 'INTEGER_DIVISION',
    'orelse': 'DISJUNCTION',
    'andalso': 'CONJUNCTION',
    'not': 'NEGATION',
    'False': 'BOOLEAN_FALSE',
    'True': 'BOOLEAN_TRUE',
    'in': 'MEMBERSHIP',
    'print': 'PRINT',
    'if' : 'IF',
    'else' : 'ELSE',
    'while': 'WHILE'
}

tokens = [
    'LBRACE', 'RBRACE',
    'LBRACKET', 'RBRACKET',
    'LPAREN','RPAREN',
    'VARIABLE', 
    'ADDITION', 'SUBTRACTION', 
    'MULTIPLICATION', 'DIVISION',
    'EXPONENTIATION',
    'ASSIGNMENT',
    'STRING', 'REAL', 'INTEGER',
    'LESS_THAN', 'LESS_THAN_EQUAL', 'GREATER_THAN', 'GREATER_THAN_EQUAL', 'EQUAL_TO', 'NOT_EQUAL_TO',
    'CONS',
    'COMMA', 'HASHTAG',
    'SEMICOLON'
] + list(reserved.values())

### Token Definitions ###

# general
t_ASSIGNMENT = r'='
t_SEMICOLON = r';'

# for blocks
t_LBRACE = r'{'
t_RBRACE = r'}'

# for lists
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r','
t_CONS = r'\:\:'

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

# printing
t_PRINT = r'print'

# control flow
t_IF = r'if'
t_ELSE = r'else'

# looping
t_WHILE = r'while'

def t_STRING(t):
    r'"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\''
    t.value = t.value
    return t

# rule for reals
def t_REAL(t):
    r'(\d*\.\d+|\d+\.\d*)(e-?\d+)?'
    t.value = eval(t.value)
    return t

def t_VARIABLE(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'VARIABLE') # check for reserved words
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_BOOLEAN_FALSE(t):
    r'False'
    t.value = False
    return t

def t_BOOLEAN_TRUE(t):
    r'True'
    t.value = True
    return t

t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    # print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

def main(args):
    if len(args) == 2:
        with open(sys.argv[1]) as fd:
            lexer.input(fd.read())

        while True:
            tok = lexer.token()
            if not tok:
                break
            print(tok)
        
    elif len(sys.argv) == 1:
        while True:
            lexer.input(input())
            tok = lexer.token()
            if not tok:
                break
            print(tok) 
    else:
        print("Invalid arguments. Proper usage: python3 lexer.py [input_file]")
        exit(1)

if __name__ == "__main__":
    main(sys.argv)
