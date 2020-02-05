import sys
sys.path.append("..")

from src.sbml_ast import *
# from src.sbml import *

p = parser.parse

def t(expr):
    return p(expr).parse()

def sem(expr):
    try:
        p(expr)
    except SyntaxError as err:
        assert err == "SEMANTIC ERROR"

    return "No Error"

def syn(expr):
    try:
        p(expr)
    except SyntaxError as err:
        assert err == "invalid syntax"

    return "No Error"

#=== SEMANTIC ERROR CHECKING ===#
sem('1 + "abc";') 
sem('"abc" + ["c", "d", "e"];') 
sem('1 - [1, 2, 3];') 
sem('True andalso 5.0;') 
sem('False orelse "Abc";') 
sem('not (3+7);') 
sem('[1, 2, 3, 4][5];') 
sem('#7(1, 2, 3);') 
sem('[1, 2, 3, 4][3 < 4];') 
sem('"abc" < [1, 2, 3];')
sem('("test", "tuple") + ("another", "test");')
sem('["random"] + ("tuple", "stuff");')
sem('"dog" + ("cat", "mouse");')
sem('["dog"] + "cat";')
sem('3 + "dog";')
sem('3 + dog;')
sem('12 mod 7.0;')
sem('12 div 6.0;')
sem('1 div 0;')
sem('1 / 0;')

#=== SYNTAX ERROR CHECKING ===#
syn('1 + 2')
syn(';')
syn('1 2;')
syn("'b;")
syn('"a\';')
syn('[1, 2 3];')
syn('[1, 2,;')
syn('#"a"(1, 2, 3);')
syn('(2 + 3;')
syn('2 + ;')
syn('1 + 2')
syn('1 2 - 5')

#=== BASIC TEST CASES ==#
assert t('10101;') == 10101
assert t('-8759;') == -8759
assert t('2.718281828;') == 2.718281828
assert t('-0.0002;') == -0.0002
assert t('57.;') == 57.0
assert t('.7729;') == 0.7729
assert t('-.8394;') == -0.8394
assert t('6.02e-23;') == 6.02e-23
assert t('9.11e17;') == 9.11e+17
assert t('.188e86;') == 1.88e+85
assert t('17.e2;') == 1700.0
assert t('17.e-2;') == 0.17
assert t('True;') == True
assert t('False;') == False
assert t('"";') == ''
assert t('"A";') == 'A'
assert t('"ABCDEFGHIJKLMNOPQRSTUVWXYZ";') == 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
assert t("'';") == '' 
assert t("'B';") == 'B'
assert t("'Hello World';") == 'Hello World'
assert t('"legend         ary";') == 'legend         ary'
assert t('"!@#$%^&*()";') == '!@#$%^&*()'
assert t("'1234567890';") == '1234567890'
assert t('[];') == []
assert t("['a'];") == ['a']
assert t('[1, 2, 3, 4];') == [1, 2, 3, 4]
assert t("['zzzz', 817, \"ARG!\", 100.012, 17.0e-4];") == ['zzzz', 817, 'ARG!', 100.012, 0.0017]
assert t('True orelse False;') == True
assert t('False orelse False;') == False
assert t('False andalso True;') == False
assert t('True andalso True;') == True
assert t('not False;') == True
assert t('not True;') == False
assert t('"a" < \'z\';') == True
assert t('17 <= 16;') == False
assert t('"abc" == \'abc\';') == True
assert t('10.0 <> 10;') == False
assert t('11.9 >= 11.9;') == True
assert t('11.9 > 11.9;') == False
assert t("'a'::[];") == ['a']
assert t('17::[1, 2, 3, 4];') == [17, 1, 2, 3, 4]
assert t('\'z\' in "abzcdef";') == True
assert t('5 in [1, 2, 3, 4];') == False
assert t('5 - 3;') == 2
assert t('17.0 + 10.0;') == 27.0
assert t('"Hello" + " " + "World";') == 'Hello World'
assert t('[1, 2, 3] + ["a", \'b\', "c"];') == [1, 2, 3, 'a', 'b', 'c']
assert t('17 mod 6;') == 5
assert t('17 div 6;') == 2
assert t('17 / 6;') == 2.8333333333333335
assert t('17.0 / 6.0;') == 2.8333333333333335
assert t('10 * 10;') == 100
assert t('10.0 * 10.0;') == 100.0
assert t('10 * 10.0;') == 100.0
assert t('2 ** 10;') == 1024
assert t('[1, 2, 3, 4][0];') == 1
assert t('(1, 2, 3, 4);') == (1, 2, 3, 4)
assert t('#1(1, 2, 3, 4);') == 1
assert t('("abc");') == 'abc'
assert t('(2 + 5);') == 7

# custom test cases
assert t('1 + 2;') == 3 # valid
assert t('1 - 2;') == -1 # valid
assert t('-1 - -2;') == 1 # valid
assert t('1 / 4;') == 0.25 # valid
assert t('-1 / 4;') == -0.25 # valid
assert t('5 * 4;') == 20 # valid
assert t('5 * 4.20;') == 21.0 # valid
assert t('12 div 6;') == 2 # valid
assert t('12 mod 7;') == 5 # valid
assert t('2 ** 3;') == 8 # valid 
assert t('2 ** 2 ** 3;') == 256 # valid (testing exponentiation associativity)
assert t('(2 + 5) * 4 - 5;') == 23 # valid (testing parantheses)
assert t('2 + 5 * 4 - 5;') == 17 # valid (testing operator precedence)
assert t('10 + 9 - 8 / 4 div 6 mod 5 * 4 ** 3;') == 19 # valid
assert t('"cat" + "dog";') == "catdog" # string concatenation

#=== TRICKY TEST CASES ===#
assert t('1+2*3/4-7;') == -4.5
assert t('(1+2)*(3/(4-7));') == -3.0
assert t('(not (False orelse False)) andalso (not False andalso not False);') == True
assert t('[[1, 2, 3], ["a", "b", "c"], [4.0, 5.0, 6.0]][1];') == ['a', 'b', 'c']
assert t('[[1, 2, 3], ["a", "b", "c"], [4.0, 5.0, 6.0]][2][1];') == 5.0
assert t("'a' in (\"bce\" + \"def\" + \"ghi\" + \"yza\");") == True
assert t('#2(7, 8, 9) == [9, 8, 7][1];') == True
assert t('[1, 2, 3][1 + 1] > [4, 5, 6][1 - 1] orelse "abc"[2] < "xyz"[0];') == True
assert t('[1, 2, 3][1 * 2] * [4, 5, 6][2 div 1] - [7, 8, 9][17 mod 3];') == 9
assert t('([1, 2, 3][1 + 1] > [4, 5, 6][1 - 1] orelse "abc"[2] < "xyz"[0]) andalso (#2(7, 8, 9) == [9, 8, 7][1]);') == True
assert t('#3#2#1(("3", (3,8,10)), (10, "dad"));') == 10
