import os

import ply.yacc as yacc

from translator.scanner import tokens, lexer
from translator.tree import Node

precedence = (
    ('nonassoc', 'IFX'),
    ('nonassoc', 'ELSE'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQ', 'NE'),
    ('left', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
    ('right', 'NOT', 'UMINUS'),
)


def p_program(p):
    'program : using func_list'
    p[0] = Node('program', children=p[2])


def p_using(p):
    '''using : USING NAMESPACE ID SEMI
             | empty'''


def p_func_list(p):
    '''func_list : func_list func
                 | func'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_func(p):
    'func : type ID LPAREN params RPAREN block'
    p[0] = Node('func', (p[1], p[2]), [Node('params', children=p[4]), p[6]])


def p_type(p):
    '''type : INT
            | DOUBLE
            | BOOL
            | VOID'''
    p[0] = p[1]


def p_params(p):
    '''params : param_list
              | empty'''
    p[0] = p[1] if p[1] else []


def p_param_list(p):
    '''param_list : param_list COMMA type ID
                  | type ID'''
    if len(p) == 5:
        p[0] = p[1] + [Node('param', (p[3], p[4]))]
    else:
        p[0] = [Node('param', (p[1], p[2]))]


def p_block(p):
    'block : LBRACE stmt_list RBRACE'
    p[0] = Node('block', children=p[2])


def p_stmt_list(p):
    '''stmt_list : stmt_list stmt
                 | empty'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []


def p_stmt(p):
    '''stmt : decl SEMI
            | assign SEMI
            | expr SEMI
            | if_stmt
            | while_stmt
            | for_stmt
            | return_stmt
            | cout_stmt
            | block'''
    p[0] = p[1]


def p_decl(p):
    '''decl : type ID
            | type ID ASSIGN expr'''
    if len(p) == 5:
        p[0] = Node('decl', (p[1], p[2]), [p[4]])
    else:
        p[0] = Node('decl', (p[1], p[2]))


def p_assign(p):
    'assign : ID ASSIGN expr'
    p[0] = Node('assign', p[1], [p[3]], p.lineno(1))


def p_assign_inc(p):
    '''assign : ID INC
              | ID DEC'''
    p[0] = Node(p[2], p[1], line=p.lineno(1))


def p_if(p):
    'if_stmt : IF LPAREN expr RPAREN stmt %prec IFX'
    p[0] = Node('if', children=[p[3], p[5]])


def p_if_else(p):
    'if_stmt : IF LPAREN expr RPAREN stmt ELSE stmt'
    p[0] = Node('if', children=[p[3], p[5], p[7]])


def p_while(p):
    'while_stmt : WHILE LPAREN expr RPAREN stmt'
    p[0] = Node('while', children=[p[3], p[5]])


def p_for(p):
    '''for_stmt : FOR LPAREN decl SEMI expr SEMI assign RPAREN stmt
                | FOR LPAREN assign SEMI expr SEMI assign RPAREN stmt'''
    p[0] = Node('for', children=[p[3], p[5], p[7], p[9]])


def p_return(p):
    '''return_stmt : RETURN expr SEMI
                   | RETURN SEMI'''
    if len(p) == 4:
        p[0] = Node('return', children=[p[2]])
    else:
        p[0] = Node('return')


def p_cout(p):
    'cout_stmt : COUT out_list SEMI'
    p[0] = Node('cout', children=p[2])


def p_out_list(p):
    '''out_list : out_list SHL out_item
                | SHL out_item'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[2]]


def p_out_item_expr(p):
    'out_item : expr'
    p[0] = p[1]


def p_out_item_str(p):
    'out_item : STRING'
    p[0] = Node('str', p[1])


def p_out_item_endl(p):
    'out_item : ENDL'
    p[0] = Node('endl')


def p_expr_binop(p):
    '''expr : expr PLUS expr
            | expr MINUS expr
            | expr TIMES expr
            | expr DIVIDE expr
            | expr MOD expr
            | expr LT expr
            | expr LE expr
            | expr GT expr
            | expr GE expr
            | expr EQ expr
            | expr NE expr
            | expr AND expr
            | expr OR expr'''
    p[0] = Node('binop', p[2], [p[1], p[3]], p.lineno(2))


def p_expr_not(p):
    'expr : NOT expr'
    p[0] = Node('not', children=[p[2]])


def p_expr_minus(p):
    'expr : MINUS expr %prec UMINUS'
    p[0] = Node('neg', children=[p[2]])


def p_expr_paren(p):
    'expr : LPAREN expr RPAREN'
    p[0] = p[2]


def p_expr_num(p):
    '''expr : INT_NUM
            | DOUBLE_NUM'''
    p[0] = Node('num', p[1])


def p_expr_bool(p):
    '''expr : TRUE
            | FALSE'''
    p[0] = Node('bool', p[1])


def p_expr_var(p):
    'expr : ID'
    p[0] = Node('var', p[1], line=p.lineno(1))


def p_expr_call(p):
    '''expr : ID LPAREN RPAREN
            | ID LPAREN arg_list RPAREN'''
    if len(p) == 5:
        p[0] = Node('call', p[1], p[3], p.lineno(1))
    else:
        p[0] = Node('call', p[1], [], p.lineno(1))


def p_arg_list(p):
    '''arg_list : arg_list COMMA expr
                | expr'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_empty(p):
    'empty :'
    p[0] = None


def p_error(p):
    if p is None:
        raise Exception('Синтаксична помилка: неочікуваний кінець файлу')
    raise Exception("Синтаксична помилка: неочікуваний токен '" + str(p.value) + "' у рядку " + str(p.lineno))


parser = yacc.yacc(debug=True, write_tables=False, outputdir=os.path.dirname(__file__))


def parse(code):
    lexer.lineno = 1
    return parser.parse(code, lexer=lexer)
