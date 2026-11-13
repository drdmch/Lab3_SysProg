HEADER = '''def div(a, b):
    if type(a) == int and type(b) == int:
        return int(a / b)
    return a / b


def mod(a, b):
    return a - int(a / b) * b


def to_str(v):
    if v is True:
        return '1'
    if v is False:
        return '0'
    if type(v) == float:
        return '%g' % v
    return str(v)

'''


def generate(tree):
    code = HEADER
    for func in tree.children:
        code += '\n' + gen_func(func) + '\n'
    code += "\nif __name__ == '__main__':\n    main()\n"
    return code


def gen_func(func):
    name = func.value[1]
    params = []
    for p in func.children[0].children:
        params.append(p.value[1])
    code = 'def ' + name + '(' + ', '.join(params) + '):\n'
    code += gen_body(func.children[1], 1)
    return code


def gen_body(node, level):
    code = gen_stmt(node, level)
    if code == '':
        code = '    ' * level + 'pass\n'
    return code


def gen_stmt(node, level):
    tab = '    ' * level
    t = node.type

    if t == 'block':
        code = ''
        for stmt in node.children:
            code += gen_stmt(stmt, level)
        return code

    if t == 'decl':
        var_type, name = node.value
        if not node.children:
            return tab + name + ' = 0\n'
        value = gen_expr(node.children[0])
        if var_type == 'int':
            value = 'int(' + value + ')'
        elif var_type == 'double':
            value = 'float(' + value + ')'
        return tab + name + ' = ' + value + '\n'

    if t == 'assign':
        return tab + node.value + ' = ' + gen_expr(node.children[0]) + '\n'

    if t == '++':
        return tab + node.value + ' += 1\n'

    if t == '--':
        return tab + node.value + ' -= 1\n'

    if t == 'if':
        code = tab + 'if ' + gen_expr(node.children[0]) + ':\n'
        code += gen_body(node.children[1], level + 1)
        if len(node.children) == 3:
            code += tab + 'else:\n'
            code += gen_body(node.children[2], level + 1)
        return code

    if t == 'while':
        code = tab + 'while ' + gen_expr(node.children[0]) + ':\n'
        code += gen_body(node.children[1], level + 1)
        return code

    if t == 'for':
        code = gen_stmt(node.children[0], level)
        code += tab + 'while ' + gen_expr(node.children[1]) + ':\n'
        code += gen_body(node.children[3], level + 1)
        code += gen_stmt(node.children[2], level + 1)
        return code

    if t == 'return':
        if node.children:
            return tab + 'return ' + gen_expr(node.children[0]) + '\n'
        return tab + 'return\n'

    if t == 'cout':
        parts = []
        for item in node.children:
            if item.type == 'endl':
                parts.append("'\\n'")
            elif item.type == 'str':
                parts.append(repr(item.value))
            else:
                parts.append('to_str(' + gen_expr(item) + ')')
        return tab + 'print(' + ' + '.join(parts) + ", end='')\n"

    return tab + gen_expr(node) + '\n'


def gen_expr(node):
    t = node.type

    if t == 'num':
        return str(node.value)
    if t == 'bool':
        if node.value == 'true':
            return 'True'
        return 'False'
    if t == 'var':
        return node.value
    if t == 'neg':
        return '(-' + gen_expr(node.children[0]) + ')'
    if t == 'not':
        return '(not ' + gen_expr(node.children[0]) + ')'
    if t == 'call':
        args = []
        for a in node.children:
            args.append(gen_expr(a))
        return node.value + '(' + ', '.join(args) + ')'

    a = gen_expr(node.children[0])
    b = gen_expr(node.children[1])
    op = node.value
    if op == '/':
        return 'div(' + a + ', ' + b + ')'
    if op == '%':
        return 'mod(' + a + ', ' + b + ')'
    if op == '&&':
        return 'bool(' + a + ' and ' + b + ')'
    if op == '||':
        return 'bool(' + a + ' or ' + b + ')'
    return '(' + a + ' ' + op + ' ' + b + ')'
