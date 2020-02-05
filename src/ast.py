# internal imports
from utils import *

# dictionary of names
names = {}

class Node():
    def __init__(self, parent = None, children = []):
        self.parent = parent
        self.children = children

class Block(Node):
    def __init__(self, parent = None, children = [], statements = []):
        self.parent = parent
        self.children = children
        self.statements = statements
    
    def parse(self):
        if self.statements:
            for statement in self.statements:
                statement.parse()

class WhileStatement(Node):
    def __init__(self, parent = None, children = [], condition = None, block = None):
        self.parent = parent
        self.children = children
        self.condition = condition
        self.block = block
    
    def parse(self):
        while self.condition.parse():
            self.block.parse()
            
    def __str__(self):
        return "while {}".format(self.condition)

class IfStatement(Node):
    def __init__(self, parent = None, children = [], condition = None, block = None):
        self.parent = parent
        self.children = children
        self.condition = condition
        self.block = block
    
    def parse(self):
        if self.condition.parse():
            return self.block.parse()

class IfElseStatement(Node):
    def __init__(self, parent = None, children = [], condition = None, if_block = None, else_block = None):
        self.parent = parent
        self.children = children
        self.condition = condition
        self.if_block = if_block
        self.else_block = else_block
    
    def parse(self):
        if self.condition.parse():
            return self.if_block.parse()
        else:
            return self.else_block.parse()
    
    def __str__(self):
        return 'if {}'.format(self.condition)

class AssignStatement(Node):
    def __init__(self, parent = None, children = [], lvalue = None, rvalue = None):
        self.parent = parent
        self.children = children
        self.lvalue = lvalue
        self.rvalue = rvalue

        self.parse()

    def parse(self):
        if type(self.lvalue).__name__ == 'ListStringIndexing':
            self.lvalue.expr.parse()[self.lvalue.index.parse()] = self.rvalue.parse()
        if type(self.lvalue).__name__ == 'Variable':
            names[self.lvalue.name] = self.rvalue.parse()

    def __str__(self):
        return 'Assign: {}={}'.format(self.lvalue, self.rvalue)

class PrintStatement(Node):
    def __init__(self, parent = None, children = [], expr = None):
        self.parent = parent
        self.children = children
        self.expr = expr
    
    def parse(self):
        print(self.expr.parse())
    
    def __str__(self):
        return 'print({})'.format(self.expr)
        

class Variable(Node):
    def __init__(self, parent = None, children = [], name = None):
        super().__init__(parent, children)
        self.name = name
    
    def parse(self):
        return names[self.name]

    def __str__(self):
        return '(Variable: {})'.format(self.name)

class BooleanExpression(Node):
    def __init__(self, parent = None, children = [], expr = None):
        super().__init__(parent, children)
        self.expr = expr

    def parse(self):
        return self.expr.parse()

class Negation(Node):
    def __init__(self, parent = None, children = [], expr = None):
        super().__init__(parent, children)
        self.expr = expr
    
    def parse(self):
        return not self.expr.parse()
    
    def __str__(self):
        return 'Negation: not expr={}'.format(self.expr)

class Conjunction(Node):
    def __init__(self, parent = None, children = [], left = None, right = None):
        super().__init__(parent, children)
        self.left = left
        self.right = right

    def parse(self):
        return self.left.parse() and self.right.parse()
    
    def __str__(self):
        return 'Conjunction: left={} andalso right={}'.format(self.left, self.right)

class Disjunction(Node):
    def __init__(self, parent = None, children = [], left = None, right = None):
        super().__init__(parent, children)
        self.left = left
        self.right = right
    
    def parse(self):
        return self.left.parse() or self.right.parse()
    
    def __str__(self):
        return 'Disjunction: left={} orelse right={}'.format(self.left, self.right)

class Comparison(Node):
    def __init__(self, parent = None, children = [], left = None, right = None, operation = None):
        super().__init__(parent, children)
        self.left = left
        self.right = right
        self.operation = operation
    
    def parse(self):
        result = None

        try: 
            if self.operation == '<':
                result = self.left.parse() < self.right.parse()
            elif self.operation == '<=':
                result = self.left.parse() <= self.right.parse()
            elif self.operation == '>':
                result = self.left.parse() > self.right.parse()
            elif self.operation == '>=':
                result = self.left.parse() >= self.right.parse()
            elif self.operation == '==':
                result = self.left.parse() == self.right.parse()
            elif self.operation == '<>':
                result = self.left.parse() != self.right.parse()
        except TypeError:
            print_semantic_err()
            exit(1)
        
        return result
    
    def __str__(self):
        return 'Comparison: left={}, operation={}, right={}'.format(self.left, self.operation, self.right)


class Boolean(Node):
    def __init__(self, parent = None, children = [], value = None):
        super().__init__(parent, children)
        self.value = value
    
    def parse(self):
        if type(self.value).__name__ == 'Boolean':
            return self.value.parse()
        return eval(self.value)

class BinaryOperation(Node):
    def __init__(self, parent = None, children = [], left = None, right = None, operation = None):
        super().__init__(parent, children)
        self.left = left
        self.right = right
        self.operation = operation
    
    def parse(self):
        result = None

        try:
            if self.operation == '+':
                result = self.left.parse() + self.right.parse()
            elif self.operation == '-':
                result = self.left.parse() - self.right.parse()
            elif self.operation == '*':
                result = self.left.parse() * self.right.parse()
            elif self.operation in ['/', 'div', 'mod']:
                if self.right.parse() == 0:
                    print_semantic_err()
                    exit(1)
                else:
                    if self.operation == '/':
                        result = self.left.parse() / self.right.parse()
                    elif self.operation == 'div':
                        result = self.left.parse() // self.right.parse()
                    elif self.operation == 'mod':
                        result = self.left.parse() % self.right.parse()
            elif self.operation == '**':
                result = self.left.parse() ** self.right.parse()
        except TypeError:
            print_semantic_err()
            exit(1)
            
        return result
    
    def __str__(self):
        return 'BinaryOperation: {} {} {}'.format(self.left, self.operation, self.right)

class UnaryMinus(Node):
    def __init__(self, parent = None, children = [], expr = None):
        super().__init__(parent, children)
        self.expr = expr
    
    def parse(self):
        if type(self.expr).__name__ == 'Number':
            return -self.expr.parse()
        return -self.expr

class String(Node):
    def __init__(self, parent = None, children = [], value = None):
        super().__init__(parent, children)
        self.value = value
    
    def parse(self):
        return eval(self.value)
    
    def __str__(self):
        return 'String: value={}'.format(self.parse())

class ListConstruct(Node):
    def __init__(self, parent = None, children = [], left = None, right = None):
        super().__init__(parent, children)
        self.left = left
        self.right = right
    
    def parse(self):
        if type(self.right.parse()).__name__ != 'list':
            print_semantic_err()
            exit(1)
    
        return [self.left.parse()] + self.right.parse()

class Membership(Node):
    def __init__(self, parent = None, children = [], element = None, collection = None):
        super().__init__(parent, children)
        self.element = element
        self.collection = collection

    def parse(self):
        try:
            return self.element.parse() in self.collection.parse()
        except:
            print_semantic_err()
            exit(1)
        
    def __str__(self):
        return '{} in {}'.format(self.element.parse(), self.collection.parse())


class TupleIndexing(Node):
    def __init__(self, parent = None, children = [], index = None, expr = None):
        super().__init__(parent, children)
        self.index = index
        self.expr = expr

    def parse(self):
        if type(self.expr.parse()).__name__ != 'tuple':
            print_semantic_err()
            exit(1)

        if self.index.parse() - 1 < 0 or self.index.parse() - 1 >= len(self.expr.parse()):
            print_semantic_err()
            exit(1)
    
        return self.expr.parse()[self.index.parse() - 1]

class ListStringIndexing(Node):
    def __init__(self, parent = None, children = [], index = None, expr = None):
        super().__init__(parent, children)
        self.index = index
        self.expr = expr
    
    def parse(self):
        index_type = type(self.index.parse()).__name__

        if index_type != 'int': # make sure expression is not a string, can't index with that.
            print_semantic_err()
            exit(1)

        if self.index.parse() < 0 or self.index.parse() >= len(self.expr.parse()):
            print_semantic_err()
            exit(1)

        return self.expr.parse()[self.index.parse()]
    
    def __str__(self):
        return '{}[{}]'.format(self.expr.parse(), self.index.parse())

class Number(Node):
    def __init__(self, parent = None, children = [], value = None):
        super().__init__(parent, children)
        self.value = value
    
    def parse(self):
        return self.value
    
    def __str__(self):
        return 'Number: value={}'.format(self.value)

class List(Node):
    def __init__(self, parent = None, children = [], lst=[]):
        super().__init__(parent, children)
        self.lst = lst
    
    def parse(self):
        if len(self.lst) > 0:
            parsed = [element.parse() for element in self.lst]
            return parsed
        return self.lst
    
    def __str__(self):
        return '[{}]'.format(self.parse())

class Tuple(Node):
    def __init__(self, parent = None, children = [], tup=()):
        super().__init__(parent, children)
        self.tup = tup
    
    def parse(self):
        return (element.parse() for element in self.tup)