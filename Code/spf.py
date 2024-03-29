import sys
from lark import Lark, Token
from lark.visitors import Interpreter

class MyInterpreter(Interpreter):
    def start(self, tree):
        return self.visit_children(tree)

    def programme(self, tree):
        return self.visit_children(tree)

    def expressions(self, tree):
        return self.visit_children(tree)

    def exp(self, tree):
        children = self.visit_children(tree)

    def literal(self, tree):
        pass

    def BOOLEEN(self, tree):
        pass

    def ENTIER(self, tree):
        pass

    def TEXTE(self, tree):
        pass

    def leslistes(self, tree):
        pass

    def liste(self, tree):
        pass

    def sequence(self, tree):
        pass

    def operation(self, tree):
        pass

    def egalite(self, tree):
        children0 = self.visit_children(tree[0])
        children1 = self.visit_children(tree[1])

        if not isinstance(children0, booleen) or not isinstance(children0, booleen):
            return #erreur
        return children0 == children1

    def nonegalite(self, tree):
        pass

    def negation(self, tree):
        pass

    def et(self, tree):
        pass

    def ou(self, tree):
        pass

    def addition(self, tree):
        pass

    def soustraction(self, tree):
        pass

    def tmp(self, tree):
        pass

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
