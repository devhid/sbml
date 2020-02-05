# Name: Mankirat Gulati
# ID: 111161128

# system imports
import sys

# internal imports
from lexer import tokens
from utils import print_semantic_err, print_syntax_err
from ast import *

# external imports
import ply.yacc as yacc

# precedence for rules
precedence = (
    ('left', 'STRING', 'INTEGER', 'REAL'),
    ('left', 'DISJUNCTION'),
    ('left', 'CONJUNCTION'),
    ('left', 'NEGATION'),
    ('left', 'LESS_THAN', 'LESS_THAN_EQUAL', 'GREATER_THAN', 'GREATER_THAN_EQUAL', 'EQUAL_TO', 'NOT_EQUAL_TO'),
    ('right', 'CONS'),
    ('left', 'MEMBERSHIP'),
    ('left', 'ADDITION', 'SUBTRACTION'),
    ('left', 'MULTIPLICATION', 'DIVISION', 'MODULUS', 'INTEGER_DIVISION'),
    ('right', 'EXPONENTIATION'),
    ('right', 'UMINUS'),
    ('left', 'LBRACKET', 'RBRACKET'),
    ('left', 'HASHTAG'),
    ('left', 'LPAREN', 'RPAREN')
)

# to handle list operations
lst = []

# to handle tuple operations
tup = tuple()

# to hold the statements contained within a block
block_statements = []

def p_start(p):
    "start : block"
    p[1].parse()

def p_block(p):
    """
    block : LBRACE RBRACE
          | LBRACE statement RBRACE
          | LBRACE statement block_tail RBRACE
    """

    global block_statements

    if p[1] == '{' and p[2] == '}':
        # nothing happens
        pass
    elif len(p) > 3:
        p[0] = [p[2]]

        if len(p) > 4:
            p[0] += p[3]
    
    p[0] = Block(statements=p[0])
    
    block_statements = []

def p_block_tail(p):
    """
    block_tail : statement block_tail
               | empty
    """

    global block_statements

    if len(p) > 1 and p[1] != None:
        block_statements = [p[1]] + block_statements
        
        if len(p) > 2:
            for i in range(3, len(p) - 1):
                block_statements = p[i] + block_statements
    
    p[0] = block_statements

def p_statement(p):
    """
    statement : single_statement SEMICOLON
              | conditional_statement
              | loop_statement
              | block
    """
    p[0] = p[1]

def p_single_statement(p):
    """
    single_statement : statement_assignable
                     | statement_print
    """
    p[0] = p[1]

def p_conditional_statement(p):
    """
    conditional_statement : statement_if
                          | statement_if_else
    """
    p[0] = p[1]

def p_loop_statement(p):
    "loop_statement : loop_statement_while"
    p[0] = p[1]

def p_conditional_statement_if(p):
    "statement_if : IF LPAREN boolean_argument RPAREN block"
    p[0] = IfStatement(condition=p[3], block=p[5])

def p_conditional_statement_if_else(p):
    "statement_if_else : IF LPAREN boolean_argument RPAREN block ELSE block"
    p[0] = IfElseStatement(condition=p[3], if_block=p[5], else_block=p[7])

def p_loop_statement_while(p):
    "loop_statement_while : WHILE LPAREN boolean_argument RPAREN block"
    p[0] = WhileStatement(condition=p[3], block=p[5])

def p_statement_assignable(p):
    "statement_assignable : lvalue ASSIGNMENT rvalue"
    p[0] = AssignStatement(lvalue=p[1], rvalue=p[3])

def p_statement_print(p):
    "statement_print : PRINT LPAREN rvalue RPAREN" 
    p[0] = PrintStatement(expr=p[3])

def p_lvalue(p):
    """
    lvalue : variable
           | indexing_other
    """
    p[0] = p[1]

def p_rvalue(p):
    """
    rvalue : expression
           | boolean_expression
           | boolean_comparison
    """
    p[0] = p[1]

def p_boolean_expression(p):
    """
    boolean_expression : boolean_conjunction
                       | boolean_disjunction
                       | boolean_negation
                       | boolean_membership
                       | LPAREN boolean_expression RPAREN
    """
    if p[1] == '(' and p[3] == ')':
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_boolean_conjunction(p):
    "boolean_conjunction : boolean_argument CONJUNCTION boolean_argument"
    p[0] = Conjunction(left=p[1], right=p[3])

def p_boolean_disjunction(p):
    "boolean_disjunction : boolean_argument DISJUNCTION boolean_argument"
    p[0] = Disjunction(left=p[1], right=p[3])

def p_boolean_negation(p):
    "boolean_negation : NEGATION boolean_argument"
    p[0] = Negation(expr=p[2])

def p_boolean_argument(p):
    """
    boolean_argument : boolean_comparison
                     | boolean_membership
                     | boolean_conjunction
                     | boolean_disjunction
                     | boolean_negation
                     | expression
    """
    valid = ['Comparison', 'Membership', 'Conjunction', 'Disjunction', 'Negation', 'Variable']
    if type(p[1]).__name__ not in valid:
        print_semantic_err()
        exit(1)
    
    p[0] = p[1]

def p_grouped_boolean_argument(p):
    "boolean_argument : LPAREN boolean_argument RPAREN"
    p[0] = p[2]

def p_boolean_comparison(p):
    """
    boolean_comparison : boolean
                       | expression LESS_THAN expression
                       | expression LESS_THAN_EQUAL expression
                       | expression GREATER_THAN expression
                       | expression GREATER_THAN_EQUAL expression
                       | expression EQUAL_TO expression
                       | expression NOT_EQUAL_TO expression
                       | LPAREN boolean_comparison RPAREN
    """

    if len(p) == 2:
        p[0] = Boolean(value=p[1])
    
    elif p[1] == '(' and p[3] == ')':
        p[0] = p[2]

    else:
        p[0] = Comparison(left=p[1], right=p[3], operation=p[2])
    
def p_boolean(p):
    """
    boolean : BOOLEAN_TRUE
            | BOOLEAN_FALSE
    """
    p[0] = Boolean(value=p[1])

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
    
    p[0] = BinaryOperation(left=p[1], right=p[3], operation=p[2])

def p_expression_uminus(p):
    "expression : SUBTRACTION expression %prec UMINUS"
    p[0] = UnaryMinus(expr=p[2])

def p_expression_indexing(p):
    "expression : indexing"
    p[0] = p[1]

def p_expression_tuple(p):
    "expression : tuple"
    p[0] = p[1]

def p_expression_list(p):
    "expression : list"
    p[0] = p[1]

def p_expression_string(p):
    "expression : STRING"
    p[0] = String(value=p[1])

def p_expression_group(p):
    "expression : LPAREN expression RPAREN"
    p[0] = p[2]

def p_expression_number(p):
    "expression : number"
    p[0] = p[1]

def p_expression_name(p):
    "expression : variable" 
    if p[1].name not in names:
        print_semantic_err()
        exit(1)
    p[0] = p[1]
        
def p_expression_cons(p):
    "expression : list_cons"
    p[0] = p[1]

def p_list_cons(p):
    "list_cons : expression CONS expression"
    p[0] = ListConstruct(left=p[1], right=p[3])

def p_boolean_membership(p):
    "boolean_membership : expression MEMBERSHIP expression"
    p[0] = Membership(element=p[1], collection=p[3])

def p_indexing(p):
    """
    indexing : indexing_other
             | indexing_tuple
    """
    p[0] = p[1]

def p_indexing_tuple(p):
    "indexing_tuple : HASHTAG INTEGER expression"
    p[0] = TupleIndexing(index=p[2], expr=p[3])

# handles both lists and strings since they have the same signature
def p_indexing_other(p):
    """
    indexing_other : expression LBRACKET expression RBRACKET
                   | list LBRACKET expression RBRACKET
    """
    p[0] = ListStringIndexing(index=p[3], expr=p[1])

def p_list(p):
    """
    list : LBRACKET expression list_tail RBRACKET
         | LBRACKET RBRACKET
    """
    global lst

    if len(p) == 3:
        p[0] = []
    elif len(p) > 3:
        p[0] = [p[2]]

        if len(p) > 4:
            p[0] += p[3]
    
    p[0] = List(lst=p[0])
    
    lst = []

def p_list_tail(p):
    """
    list_tail : COMMA expression list_tail
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
    "tuple : LPAREN expression COMMA expression tuple_tail RPAREN"
    global tup

    p[0] = Tuple(tup=((p[2], p[4]) + p[5]))

    # clear the global tuple
    tup = list(tup)
    tup.clear()
    tup = tuple(tup)

def p_tuple_tail(p):
    """
    tuple_tail : COMMA expression tuple_tail
               | empty
    """
    global tup

    if len(p) > 2:
        tup = ((p[2],) + tup)
        
        if len(p) > 3:
            for i in range(4, len(p) - 1, 2):
                tup = p[i] + tup
    
    p[0] = tup

def p_variable(p):
    "variable : VARIABLE"
    p[0] = Variable(name=p[1])

def p_number(p):
    """
    number : INTEGER
           | REAL
    """
    p[0] = Number(value=p[1])

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    print_syntax_err()
    exit(1)

debug_output_dir = "../output" 
parser = yacc.yacc(outputdir=debug_output_dir, errorlog=yacc.NullLogger())

def main(args):
    if len(args) == 2:
        with open(sys.argv[1]) as fd:
            parser.parse(fd.read())
    else:
        print("Invalid arguments. Proper usage: python3 sbml.py <input_file>")
        exit(1)

if __name__ == "__main__":
    main(sys.argv)