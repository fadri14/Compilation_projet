import sys
from lark import Lark, Token
from lark.visitors import Interpreter

class MyInterpreter(Interpreter):
    def start(self, tree):
        return self.visit_children(tree)

    def egalite(self, tree):
        children0 = self.visit_children(tree[0])
        children1 = self.visit_children(tree[1])

        if not isinstance(children0, booleen) or not isinstance(children0, booleen):
            return #erreur
        return children0 == children1

        """
        tab = []
        for token in tree.scan_values(lambda x: isinstance(x, Token)):
            tab += token.value
        return tab[0] == tab[1]
        """

parser = Lark.open("spf.lark", parser='lalr')
interpreter = MyInterpreter()

if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        tree = parser.parse(f.read())
        interpreter.visit(tree)
