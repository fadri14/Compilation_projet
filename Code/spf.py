import sys
from lark import Lark, Token
from lark.visitors import Interpreter

class MyInterpreter(Interpreter):
    def start(self, tree):
        return self.visit_children(tree)

parser = Lark.open("spf.lark", parser='lalr')
interpreter = MyInterpreter()

if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        tree = parser.parse(f.read())
        interpreter.visit(tree)
