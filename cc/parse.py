import ply.yacc as yacc
from lexrorg import tokens

var_table = {}
symbol_table = {}

precedence = (
     ('left', 'LOR'),
     ('left', 'LAND'),
     ('left', 'OR'),
     ('left', 'XOR'),
     ('left', 'AND'),
     ('left', 'NE','EQ'),
     ('left', 'LT', 'LE', 'GE', 'GT'),
     ('left', 'LSHIFT', 'RSHIFT'),
     ('left', 'PLUS', 'MINUS'),
     ('left', 'TIMES', 'DIVIDE', 'MOD'),
     ('right', 'SIZEOF', 'LNOT', 'NOT'),
     ('right', 'MINUSMINUS', 'PLUSPLUS'),
    )


def p_main(p):
    '''main     : declaration main
                | expression SEMI main
                | assignment main
                | empty
    '''
    p[0]=p[1]



def p_declaration0(p):
    '''declaration  : INT ID EQUALS expression SEMI
                    | INT ID EQUALS expression COMMA declaration1
    '''
    var_table[p[2]]=p[4]
    p[0] = p[4]
def p_declaration1(p):
    '''declaration  : INT ID SEMI
                    | INT ID COMMA declaration1
    '''
    var_table[p[2]]='undef'
def p_declaration2(p):
    '''declaration1     : ID SEMI
                        | ID COMMA declaration1
    '''
    var_table[p[1]]='undef'
def p_declaration3(p):
    '''declaration1     : ID EQUALS expression SEMI
                        | ID EQUALS expression COMMA declaration1
    '''
    var_table[p[1]]=p[3]




def p_assign0(p):
    '''assignment   : ID EQUALS expression SEMI
    '''
    if p[1] in var_table:
        var_table[p[1]] = p[3]
        p[0] = p[3]
def p_assign1(p):
    '''assignment   : ID LSHIFTEQUAL expression SEMI
                    | ID RSHIFTEQUAL expression SEMI
                    | ID ANDEQUAL expression SEMI
                    | ID OREQUAL expression SEMI
                    | ID XOREQUAL expression SEMI
    '''
    if p[1] in var_table:
        if p[2] == '<<=':
            var_table[p[1]] = var_table[p[1]] << p[3]
            p[0] = var_table[p[1]]
        if p[2] == '>>=':
            var_table[p[1]] = var_table[p[1]] >> p[3]
            p[0] = var_table[p[1]]
        if p[2] == '&=':
            var_table[p[1]] &= p[3]
            p[0] = var_table[p[1]]
        if p[2] == '|=':
            var_table[p[1]] |= p[3]
            p[0] = var_table[p[1]]
        if p[2] == '^=':
            var_table[p[1]] ^= p[3]
            p[0] = var_table[p[1]]
def p_assign2(p):
    '''assignment   : ID TIMESEQUAL expression SEMI
                    | ID DIVEQUAL expression SEMI
                    | ID PLUSEQUAL expression SEMI
                    | ID MINUSEQUAL expression SEMI
                    | ID MODEQUAL expression SEMI
    '''
    if p[1] in var_table:
        if p[2] == '*=':
            var_table[p[1]] *= p[3]
            p[0] = var_table[p[1]]
        if p[2] == '/=':
            var_table[p[1]] /= p[3]
            p[0] = var_table[p[1]]
        if p[2] == '+=':
            var_table[p[1]] += p[3]
            p[0] = var_table[p[1]]
        if p[2] == '-=':
            var_table[p[1]] -= p[3]
            p[0] = var_table[p[1]]
        if p[2] == '%=':
            var_table[p[1]] %= p[3]
            p[0] = var_table[p[1]]




def p_ar_binary_operators(p):
    '''expression   : expression PLUS expression
                    | expression MINUS expression
                    | expression TIMES expression
                    | expression DIVIDE expression
                    | expression MOD expression
    '''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]
    elif p[2] == '%':
        p[0] = p[1] % p[3]

def p_bool_binary_operators(p):
    '''expression   : expression OR expression
                    | expression AND expression
                    | expression XOR expression
                    | expression LOR expression
                    | expression LAND expression
    '''
    if p[2] == '|':
        p[0] = p[1] | p[3]
    elif p[2] == '&':
        p[0] = p[1]&p[3]
    elif p[2] == '^':
        p[0] = p[1]^p[3]
    elif p[2] == '||':
        p[0] = p[1] or p[3]
    elif p[2] == '&&':
        p[0] = p[1] and p[3]
def p_bool_binary_operators1(p):
    '''expression   : expression LE expression
                    | expression GE expression
                    | expression EQ expression
                    | expression LT expression
                    | expression GT expression
    '''
    if p[2] == '<=':
        p[0] = p[1]<=p[3]
    elif p[2] == '>=':
        p[0] = p[1]>=[3]
    elif p[2] == '==':
        p[0] = p[1]==p[3]
    elif p[2] == '<':
        p[0] = p[1] < p[3]
    elif p[2] == '>':
        p[0] = p[1] > p[3]
def p_bool_binary_operators2(p):
    '''expression   : expression NE expression
                    | expression LSHIFT expression
                    | expression RSHIFT expression
    '''
    if p[2] == '!=':
        p[0] = p[1]!=p[3]
    elif p[2] == '>>':
        p[0] = p[1]>=[3]
    elif p[2] == '<<':
        p[0] = p[1]<<p[3]



def p_unary_operators1(p):
    '''expression   : expression PLUSPLUS
                    | expression MINUSMINUS
    '''
    if p[2] == '++':
        p[0] = p[1]+1
    elif p[2] == '--':
        p[0] = p[1]-1;
def p_unary_operators2(p):
    '''expression   : PLUSPLUS expression
                    | MINUSMINUS expression
                    | LNOT expression
                    | NOT expression
    '''
    if p[1] == '++':
        p[0] = p[2]+1
    elif p[1] == '--':
        p[0] = p[2]-1;
    elif p[1] == '~':
        p[0] = ~p[2];
    elif p[1] == '!':
        p[0] = not p[2];
def p_unary_operators3(p):
    '''expression   : PLUSPLUS ID
                    | MINUSMINUS ID
    '''
    if p[1] == '++':
        if p[2] in var_table.keys():
            p[0] = var_table[p[2]]+1
            var_table[p[2]]=p[0]
    elif p[1] == '--':
        if p[2] in var_table.keys():
            p[0] = var_table[p[2]]-1
            var_table[p[2]]=p[0]
def p_unary_operators4(p):
    '''expression   : ID PLUSPLUS
                    | ID MINUSMINUS
    '''
    if p[2] == '++':
        if p[1] in var_table.keys():
            p[0] = var_table[p[1]]
            var_table[p[1]]+=1
    elif p[2] == '--':
        if p[1] in var_table.keys():
            p[0] = var_table[p[1]]
            var_table[p[1]]-=1


def p_ternary(p):
    '''expression   : expression CONDOP expression COLON expression
    '''
    if p[1] == True:
        p[0] = p[3]
    else:
        p[0] = p[5]


def p_factor_num(p):
    'expression : CONSTANT'
    p[0] = p[1]

def p_factor_ID(p):
    'expression : ID'
    if p[1] in var_table:
        p[0] = var_table[p[1]]
    else:
        print('SyntaxError')

def p_factor_expr(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_error(p):
    print("Syntax error in input!")

def p_empty(p):
    'empty :'
    pass

 # Build the parser
parser = yacc.yacc()

while True:
    try:
        s = input('calc > ')
    except EOFError:
        break
    if not s: continue
    result = parser.parse(s)
    print(result)
    print(var_table)
