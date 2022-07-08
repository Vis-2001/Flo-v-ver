import ply.yacc as yacc
from lexrorg import tokens

start = 'translation_unit'
def p_primexpr(p):
    '''primary_expression : ID
	| CONSTANT
	| STRING
	| LPAREN expression RPAREN
    '''

def p_postfix(p):
    '''postfix_expression : primary_expression
	| postfix_expression LBRACKET expression RBRACKET
	| postfix_expression LPAREN RPAREN
	| postfix_expression LPAREN argument_expression_list RPAREN
	| postfix_expression PERIOD ID
	| postfix_expression ARROW ID
	| postfix_expression PLUSPLUS
	| postfix_expression MINUSMINUS
    '''

def p_argexpr(p):
    '''argument_expression_list : assignment_expression
	| argument_expression_list COMMA assignment_expression
    '''

def p_unary(p):
    '''unary_expression : postfix_expression
	| PLUSPLUS unary_expression
	| MINUSMINUS unary_expression
	| unary_operator cast_expression
	| SIZEOF unary_expression
	| SIZEOF LPAREN type_name RPAREN
    '''

def p_unop(p):
    '''unary_operator : AND
	| TIMES
	| PLUS
	| MINUS
	| NOT
	| LNOT
    '''

def p_cast_expr(p):
    '''cast_expression : unary_expression
	| LPAREN type_name RPAREN cast_expression
    '''

def p_mul_expr(p):
    '''multiplicative_expression : cast_expression
	| multiplicative_expression TIMES cast_expression
	| multiplicative_expression DIVIDE cast_expression
	| multiplicative_expression MOD cast_expression
    '''

def p_add_expr(p):
    '''additive_expression : multiplicative_expression
	| additive_expression PLUS multiplicative_expression
	| additive_expression MINUS multiplicative_expression
    '''

def p_shiftexpr(p):
    '''shift_expression : additive_expression
	| shift_expression LSHIFT additive_expression
	| shift_expression RSHIFT additive_expression
    '''

def p_relexpr(p):
    '''relational_expression : shift_expression
	| relational_expression LT shift_expression
	| relational_expression GT shift_expression
	| relational_expression LE shift_expression
	| relational_expression GE shift_expression
    '''

def p_eqexpr(p):
    '''equality_expression : relational_expression
	| equality_expression EQ relational_expression
	| equality_expression NE relational_expression
    '''

def p_andexpr(p):
    '''and_expression : equality_expression
	| and_expression AND equality_expression
    '''

def p_xorexpr(p):
    '''exclusive_or_expression : and_expression
	| exclusive_or_expression XOR and_expression
    '''

def p_eorexpr(p):
    '''inclusive_or_expression : exclusive_or_expression
	| inclusive_or_expression OR exclusive_or_expression
    '''

def p_landexpr(p):
    '''logical_and_expression : inclusive_or_expression
	| logical_and_expression LAND inclusive_or_expression
    '''

def p_lorexpr(p):
    '''logical_or_expression : logical_and_expression
	| logical_or_expression LOR logical_and_expression
    '''

def p_ternary(p):
    '''conditional_expression : logical_or_expression
	| logical_or_expression CONDOP expression COLON conditional_expression
    '''

def p_assign(p):
    '''assignment_expression : conditional_expression
	| unary_expression assignment_operator assignment_expression
    '''

def p_assignop(p):
    '''assignment_operator : EQUALS
	| TIMESEQUAL
	| DIVEQUAL
	| MODEQUAL
	| PLUSEQUAL
	| MINUSEQUAL
	| LSHIFTEQUAL
	| RSHIFTEQUAL
	| ANDEQUAL
	| XOREQUAL
	| OREQUAL
    '''

def p_expression(p):
    '''expression : assignment_expression
	| expression COMMA assignment_expression
    '''

def p_constexpr(p):
    '''constant_expression : conditional_expression
    '''

def p_declaration(p):
    '''declaration : declaration_specifiers SEMI
	| declaration_specifiers init_declarator_list SEMI
    '''

def p_dspec(p):
    '''declaration_specifiers : storage_class_specifier
	| storage_class_specifier declaration_specifiers
	| type_specifier
	| type_specifier declaration_specifiers
	| type_qualifier
	| type_qualifier declaration_specifiers
    '''

def p_idlst(p):
    '''init_declarator_list : init_declarator
	| init_declarator_list COMMA init_declarator
    '''

def p_idl(p):
    '''init_declarator : declarator
	| declarator EQUALS initializer
    '''

def p_scspec(p):
    '''storage_class_specifier : TYPEDEF
	| EXTERN
	| STATIC
	| AUTO
	| REGISTER
	'''

def p_typespec(p):
    '''type_specifier : VOID
	| CHAR
	| SHORT
	| INT
	| LONG
	| FLOAT
	| DOUBLE
	| SIGNED
	| UNSIGNED
	| struct_or_union_specifier
    '''

def p_structunionspec(p):
    '''struct_or_union_specifier : struct_or_union ID LBRACE struct_declaration_list RBRACE
	| struct_or_union LBRACE struct_declaration_list RBRACE
	| struct_or_union ID
    '''

def p_structunion(p):
    '''struct_or_union : STRUCT
	| UNION
    '''

def p_sdl(p):
    '''struct_declaration_list : struct_declaration
	| struct_declaration_list struct_declaration
    '''

def p_structdecl(p):
    '''struct_declaration : specifier_qualifier_list struct_declarator_list SEMI
    '''

def p_specquall(p):
    '''specifier_qualifier_list : type_specifier specifier_qualifier_list
	| type_specifier
	| type_qualifier specifier_qualifier_list
	| type_qualifier
    '''

def p_structdecllst(p):
    '''struct_declarator_list : struct_declarator
	| struct_declarator_list COMMA struct_declarator
    '''

def p_structdecl1(p):
    '''struct_declarator : declarator
	| COLON constant_expression
	| declarator COLON constant_expression
    '''

def p_typequal(p):
    '''type_qualifier : CONST
	| VOLATILE
    '''

def p_decl(p):
    '''declarator : pointer direct_declarator
	| direct_declarator
    '''

def p_dirdecl(p):
    '''direct_declarator : ID
	| LPAREN declarator RPAREN
	| direct_declarator LBRACKET constant_expression RBRACKET
	| direct_declarator LBRACKET RBRACKET
	| direct_declarator LPAREN parameter_type_list RPAREN
	| direct_declarator LPAREN ID_list RPAREN
	| direct_declarator LPAREN RPAREN
    '''

def p_pointer(p):
    '''pointer : TIMES
	| TIMES type_qualifier_list
	| TIMES pointer
	| TIMES type_qualifier_list pointer
    '''

def p_typeqlist(p):
    '''type_qualifier_list : type_qualifier
	| type_qualifier_list type_qualifier
    '''

def p_paramtypelist(p):
    '''parameter_type_list : parameter_list
	| parameter_list COMMA ELLIPSIS
    '''

def p_param(p):
    '''parameter_list : parameter_declaration
	| parameter_list COMMA parameter_declaration
    '''

def p_paramdecl(p):
    '''parameter_declaration : declaration_specifiers declarator
	| declaration_specifiers abstract_declarator
	| declaration_specifiers
    '''

def p_idlist(p):
    '''ID_list : ID
	| ID_list COMMA ID
    '''

def p_typename(p):
    '''type_name : specifier_qualifier_list
	| specifier_qualifier_list abstract_declarator
    '''

def p_abstractdecl(p):
    '''abstract_declarator : pointer
	| direct_abstract_declarator
	| pointer direct_abstract_declarator
    '''

def p_directabdecl(p):
    '''direct_abstract_declarator : LPAREN abstract_declarator RPAREN
	| LBRACKET RBRACKET
	| LBRACKET constant_expression RBRACKET
	| direct_abstract_declarator LBRACKET RBRACKET
	| direct_abstract_declarator LBRACKET constant_expression RBRACKET
	| LPAREN RPAREN
	| LPAREN parameter_type_list RPAREN
	| direct_abstract_declarator LPAREN RPAREN
	| direct_abstract_declarator LPAREN parameter_type_list RPAREN
    '''

def p_initializer(p):
    '''initializer : assignment_expression
	| LBRACE initializer_list RBRACE
	| LBRACE initializer_list COMMA RBRACE
    '''

def p_initlist(p):
    '''initializer_list : initializer
	| initializer_list COMMA initializer
    '''

def p_statement(p):
    '''statement : labeled_statement
	| compound_statement
	| expression_statement
	| selection_statement
	| iteration_statement
	| jump_statement
    '''

def p_labstat(p):
    '''labeled_statement : ID COLON statement
	| CASE constant_expression COLON statement
	| DEFAULT COLON statement
    '''

def p_compoundstat(p):
    '''compound_statement : LBRACE RBRACE
	| LBRACE statement_list RBRACE
	| LBRACE declaration_list RBRACE
	| LBRACE declaration_list statement_list RBRACE
    '''
def p_declist(p):
    '''declaration_list : declaration
	| declaration_list declaration
	'''
def p_statlist(p):
    '''statement_list : statement
	| statement_list statement
    '''

def p_exprstat(p):
    '''expression_statement : SEMI
	| expression SEMI
    '''

def p_selectstat(p):
    '''selection_statement : IF LPAREN expression RPAREN statement
	| IF LPAREN expression RPAREN statement ELSE statement
	| SWITCH LPAREN expression RPAREN statement
    '''

def p_iterstat(p):
    '''iteration_statement : WHILE LPAREN expression RPAREN statement
	| DO statement WHILE LPAREN expression RPAREN SEMI
	| FOR LPAREN expression_statement expression_statement RPAREN statement
	| FOR LPAREN expression_statement expression_statement expression RPAREN statement
    '''

def p_jstat(p):
    '''jump_statement : GOTO ID SEMI
	| CONTINUE SEMI
	| BREAK SEMI
	| RETURN SEMI
	| RETURN expression SEMI
    '''

def p_translationunit(p):
    '''translation_unit : external_declaration
	| translation_unit external_declaration
    '''

def p_extdec(p):
    '''external_declaration : function_definition
	| declaration
    '''

def p_funcdef(p):
    '''function_definition : declaration_specifiers declarator declaration_list compound_statement
	| declaration_specifiers declarator compound_statement
	| declarator declaration_list compound_statement
	| declarator compound_statement
    '''


def p_error(p):
    print("Syntax error in input!")


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
