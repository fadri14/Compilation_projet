import sys
from lark import Lark, Transformer

grammar = """
    start: expr

    ?expr: sum

    ?sum: product
        | sum "+" product   -> add
        | sum "-" product   -> sub

    ?product: atom
        | product "*" atom   -> mul
        | product "/" atom   -> div

    ?atom: NUMBER           -> number
         | "-" atom         -> neg
         | "(" expr ")"

    %import common.NUMBER
    %import common.WS
    %ignore WS
"""

class CalcTransformer(Transformer):
    def add(self, args):
        return args[0] + args[1]

    def sub(self, args):
        return args[0] - args[1]

    def mul(self, args):
        return args[0] * args[1]

    def div(self, args):
        return args[0] / args[1]

    def neg(self, args):
        return -args[0]

    def number(self, args):
        return float(args[0])

parser = Lark.open("gram.lark", start='start', parser='lalr', transformer=CalcTransformer())

if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        print(parser.parse(f.read()))

