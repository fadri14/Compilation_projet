from lark import Lark, Token
from lark.visitors import Interpreter

grammar = """
start: expr
expr: NUMBER "+" NUMBER  -> add
    | NUMBER "-" NUMBER  -> subtract
NUMBER: /\d+/
%ignore /\s+/
"""

class MyInterpreter(Interpreter):
    def start(self, tree):
        print(tree.data)
        print(tree.meta)
        return self.visit(tree.children[0])

    def expr(self, tree):
        # La méthode expr interprète une expression et retourne le résultat
        return self.visit_children(tree)

    def add(self, tree1):
        # La méthode add interprète une addition et retourne le résultat
        print(tree)
        res = 0
        for token in tree1.scan_values(lambda x: isinstance(x, Token)): #ou Number
            res += int(token.value)
            print(token.line)
            print(token.value)
        return res

parser = Lark(grammar, start='start')
interpreter = MyInterpreter()

tree = parser.parse("2 + 3")
result = interpreter.visit(tree)
print("Résultat de l'expression:", result)
