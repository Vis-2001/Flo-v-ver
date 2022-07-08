import ply.lex as lex
import re

tokens = [ 'ID' , 'CONSTANT',
#arithmetic operators
'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',
#increment/decrement operators
'PLUSPLUS', 'MINUSMINUS',
#assigment operators
'EQUALS','TIMESEQUAL','DIVEQUAL','MODEQUAL',
'PLUSEQUAL', 'MINUSEQUAL',
'LSHIFTEQUAL','RSHIFTEQUAL', 'ANDEQUAL', 'XOREQUAL',
'OREQUAL',
#logical operations
'OR', 'AND', 'NOT', 'XOR', 'LSHIFT', 'RSHIFT',
'LOR', 'LAND', 'LNOT',
'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',
#brackets
'LPAREN', 'RPAREN',
'LBRACKET', 'RBRACKET',
'LBRACE', 'RBRACE',
'COMMA', 'PERIOD',
'SEMI', 'COLON',
# Structure dereference
'ARROW',
# Conditional operator
'CONDOP',
 # Ellipsis (...)
'ELLIPSIS',
#others
'STRING','PREPROCESSOR_TOKEN',


]

reserved={
    'auto' : 'AUTO',
    'break' : 'BREAK',
    'case' : 'CASE',
    'char' : 'CHAR',
    'const' : 'CONST',
    'continue': 'CONTINUE',
    'default' : 'DEFAULT',
    'do' : 'DO',
    'double' : 'DOUBLE',
    'else' : 'ELSE',
    'enum' : 'ENUM',
    'extern' : 'EXTERN',
    'float' : 'FLOAT',
    'for' : 'FOR',
    'goto': 'GOTO',
    'if' : 'IF',
    'inline' : 'INLINE',
    'int' : 'INT',
    'long' : 'LONG',
    'register' : 'REGISTER',
    'restrict' : 'RESTRICT',
    'return' : 'RETURN',
    'short' : 'SHORT',
    'signed' : 'SIGNED',
    'sizeof' : 'SIZEOF',
    'static' : 'STATIC',
    'struct' : 'STRUCT',
    'switch':'SWITCH',
    'typedef' : 'TYPEDEF',
    'union' : 'UNION',
    'unsigned' : 'UNSIGNED',
    'void' : 'VOID',
    'volatile' : 'VOLATILE',
    'while' : 'WHILE',
    '_Bool' : 'BOOL',
    '_Complex' : 'CMPLX',
    '_Imaginary' : 'IMGRY',

}

tokens += reserved.values()
t_PLUS              = r'\+'
t_MINUS             = r'-'
t_TIMES             = r'\*'
t_DIVIDE            = r'/'
t_MOD               = r'%'
t_OR                = r'\|'
t_AND               = r'&'
t_NOT               = r'~'
t_XOR               = r'\^'
t_LSHIFT            = r'<<'
t_RSHIFT            = r'>>'
t_LOR               = r'\|\|'
t_LAND              = r'&&'
t_LNOT              = r'!'
t_LT                = r'<'
t_GT                = r'>'
t_LE                = r'<='
t_GE                = r'>='
t_EQ                = r'=='
t_NE                = r'!='
t_EQUALS            = r'='
t_TIMESEQUAL        = r'\*='
t_DIVEQUAL          = r'/='
t_MODEQUAL          = r'%='
t_PLUSEQUAL         = r'\+='
t_MINUSEQUAL        = r'-='
t_LSHIFTEQUAL       = r'<<='
t_RSHIFTEQUAL       = r'>>='
t_ANDEQUAL          = r'&='
t_OREQUAL           = r'\|='
t_XOREQUAL          = r'\^='
t_PLUSPLUS          = r'\+\+'
t_MINUSMINUS        = r'--'
t_ARROW             = r'->'
t_CONDOP            = r'\?'
t_LPAREN            = r'\('
t_RPAREN            = r'\)'
t_LBRACKET          = r'\[|<:'
t_RBRACKET          = r'\]|:>'
t_COMMA             = r','
t_PERIOD            = r'\.'
t_SEMI              = r';'
t_COLON             = r':'
t_ELLIPSIS          = r'\.\.\.'
t_LBRACE            = r'\{|<%'
t_RBRACE            = r'\}|%>'


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[ t.value ]
    return t

def t_PREPROCESSOR_TOKEN(t):
    r'\#.*\n'
    pass

def t_CONSTANT(t):
    r'[0-9]*\.[0-9]*|\d*\d|\'.\''
    if t.value[0] == '\'':
        t.value = ord(t.value.replace("'", ""))
    else:
        t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)

def t_STRING(t):
    r'".*"'
    return t

t_ignore  = ' \t'

def t_error(t):
  print ("Illegal character" , t.value[0])
  t.lexer.skip(1)

def t_COMMENT(t):
    r'//.*(\n|\*/)|/\*(.|\n)*\*/'
    pass

lexer=lex.lex()
