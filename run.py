import sys

from translator.grammar import parse
from translator.tree import print_tree
from translator.evaluator import Interpreter
from translator.to_python import generate
from translator.tree_view import save_html

if len(sys.argv) < 2:
    print('запуск: python run.py programs/fibonacci.cpp')
    sys.exit()

path = sys.argv[1]

f = open(path, encoding='utf-8')
code = f.read()
f.close()

try:
    tree = parse(code)
    print('--- AST ---')
    print_tree(tree)

    save_html(tree, path, 'ast.html')
    print('\nдерево збережено в ast.html')

    f = open('output.py', 'w', encoding='utf-8')
    f.write(generate(tree))
    f.close()
    print('python код збережено в output.py')

    print('\n--- результат ---')
    Interpreter(tree).run()
except Exception as e:
    print(e)
