class ReturnValue(Exception):
    def __init__(self, value):
        self.value = value


def to_str(v):
    if v is True:
        return '1'
    if v is False:
        return '0'
    if type(v) == float:
        return '%g' % v
    return str(v)


class Interpreter:
    def __init__(self, tree):
        self.functions = {}
        for f in tree.children:
            self.functions[f.value[1]] = f
        self.vars = {}

    def run(self):
        if 'main' not in self.functions:
            raise Exception('Помилка: немає функції main')
        self.call('main', [], 0)

    def call(self, name, args, line):
        if name not in self.functions:
            raise Exception("Помилка: невідома функція '" + name + "' у рядку " + str(line))
        func = self.functions[name]
        params = func.children[0].children
        if len(params) != len(args):
            raise Exception("Помилка: неправильна кількість аргументів для '" + name + "' у рядку " + str(line))

        old_vars = self.vars
        self.vars = {}
        for i in range(len(params)):
            self.vars[params[i].value[1]] = args[i]

        result = None
        try:
            self.execute(func.children[1])
        except ReturnValue as r:
            result = r.value

        self.vars = old_vars
        return result

    def get_var(self, name, line):
        if name not in self.vars:
            raise Exception("Помилка: невідома змінна '" + name + "' у рядку " + str(line))
        return self.vars[name]

    def execute(self, node):
        t = node.type

        if t == 'block':
            for stmt in node.children:
                self.execute(stmt)

        elif t == 'decl':
            var_type, name = node.value
            value = 0
            if node.children:
                value = self.calc(node.children[0])
            if var_type == 'int':
                value = int(value)
            elif var_type == 'double':
                value = float(value)
            self.vars[name] = value

        elif t == 'assign':
            self.get_var(node.value, node.line)
            self.vars[node.value] = self.calc(node.children[0])

        elif t == '++':
            self.vars[node.value] = self.get_var(node.value, node.line) + 1

        elif t == '--':
            self.vars[node.value] = self.get_var(node.value, node.line) - 1

        elif t == 'if':
            if self.calc(node.children[0]):
                self.execute(node.children[1])
            elif len(node.children) == 3:
                self.execute(node.children[2])

        elif t == 'while':
            while self.calc(node.children[0]):
                self.execute(node.children[1])

        elif t == 'for':
            self.execute(node.children[0])
            while self.calc(node.children[1]):
                self.execute(node.children[3])
                self.execute(node.children[2])

        elif t == 'return':
            if node.children:
                raise ReturnValue(self.calc(node.children[0]))
            raise ReturnValue(None)

        elif t == 'cout':
            text = ''
            for item in node.children:
                if item.type == 'endl':
                    text += '\n'
                elif item.type == 'str':
                    text += item.value
                else:
                    text += to_str(self.calc(item))
            print(text, end='')

        else:
            self.calc(node)

    def calc(self, node):
        t = node.type

        if t == 'num':
            return node.value
        if t == 'bool':
            return node.value == 'true'
        if t == 'var':
            return self.get_var(node.value, node.line)
        if t == 'neg':
            return -self.calc(node.children[0])
        if t == 'not':
            return not self.calc(node.children[0])
        if t == 'call':
            args = []
            for a in node.children:
                args.append(self.calc(a))
            return self.call(node.value, args, node.line)

        op = node.value
        if op == '&&':
            return bool(self.calc(node.children[0])) and bool(self.calc(node.children[1]))
        if op == '||':
            return bool(self.calc(node.children[0])) or bool(self.calc(node.children[1]))

        a = self.calc(node.children[0])
        b = self.calc(node.children[1])

        if op == '+':
            return a + b
        if op == '-':
            return a - b
        if op == '*':
            return a * b
        if op == '/' or op == '%':
            if b == 0:
                raise Exception('Помилка виконання: ділення на нуль у рядку ' + str(node.line))
            if type(a) == int and type(b) == int:
                if op == '/':
                    return int(a / b)
                return a - int(a / b) * b
            return a / b
        if op == '<':
            return a < b
        if op == '<=':
            return a <= b
        if op == '>':
            return a > b
        if op == '>=':
            return a >= b
        if op == '==':
            return a == b
        if op == '!=':
            return a != b
