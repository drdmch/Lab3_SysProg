class Node:
    def __init__(self, type, value=None, children=None, line=0):
        self.type = type
        self.value = value
        self.children = children if children else []
        self.line = line

    def label(self):
        if self.value is None:
            return self.type
        if isinstance(self.value, tuple):
            return self.type + ' ' + ' '.join(self.value)
        if self.type == 'str':
            return '"' + self.value.replace('\n', '\\n') + '"'
        return self.type + ' ' + str(self.value)


def print_tree(node, level=0):
    print('  ' * level + node.label())
    for child in node.children:
        print_tree(child, level + 1)
