import ply.lex as lex

reserved = {
    'int': 'INT',
    'double': 'DOUBLE',
    'bool': 'BOOL',
    'void': 'VOID',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'return': 'RETURN',
    'true': 'TRUE',
    'false': 'FALSE',
    'cout': 'COUT',
    'endl': 'ENDL',
    'using': 'USING',
    'namespace': 'NAMESPACE',
}

tokens = [
    'ID', 'INT_NUM', 'DOUBLE_NUM', 'STRING',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',
    'ASSIGN', 'EQ', 'NE', 'LT', 'LE', 'GT', 'GE',
    'AND', 'OR', 'NOT', 'SHL', 'INC', 'DEC',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'SEMI', 'COMMA',
] + list(reserved.values())

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'
t_ASSIGN = r'='
t_EQ = r'=='
t_NE = r'!='
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'
t_SHL = r'<<'
t_INC = r'\+\+'
t_DEC = r'--'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMI = r';'
t_COMMA = r','

t_ignore = ' \t\r'
t_ignore_include = r'\#.*'
t_ignore_comment = r'//.*'


def t_DOUBLE_NUM(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


def t_INT_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_STRING(t):
    r'"[^"\n]*"'
    t.value = t.value[1:-1].replace('\\n', '\n')
    return t


def t_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    raise Exception("Лексична помилка: невідомий символ '" + t.value[0] + "' у рядку " + str(t.lineno))


lexer = lex.lex()
