import sys
import argparse
import re
from lark import Lark, Token
from lark.visitors import Interpreter
import modules.exception as error
import modules.backend as back
import math

# Transforme une liste à plusieurs dimensions en une dimension
def flattenList(l):
    resultat = []
    for element in l:
        if isinstance(element, list):
            resultat.extend(flattenList(element))
        else:
            resultat.append(element)
    return resultat

# Apparement si on met juste return self.visit_children(tree) dans une fonction
# on peut la retirer
class MyInterpreter(Interpreter):
    def start(self, tree):
        return self.visit_children(tree)

    def instruction(self, tree):
        return self.visit_children(tree)

    def declaration(self, tree):
        var = back.Variable()
        res = self.visit_children(tree)
        res = flattenList(res)

        for token in res:
            match token.type:
                case "TYPE":
                    var.typeof = token.value
                case "VARIABLE":
                    var.name = token.value
                case default:
                    var.value = token.value

        memo.declare(var)

    def assignation(self, tree):
        for token in tree.scan_values(lambda x: isinstance(x, Token)):
            match token.type:
                case "VARIABLE":
                    name = token.value

        new_value = self.visit_children(tree)[1][0]

        memo.set(name, new_value)

    def afficher(self, tree):
        tokens = self.visit_children(tree)
        tokens = flattenList(tokens)
        res = ""
        for i in range(len(tokens)):
            if tokens[i].type == "TEXTE":
                res += str(tokens[i].value)[1:-1]
            else:
                res += str(tokens[i].value)
            if i != len(tokens) -1:
                res += " "

        print(res)

    def ajout(self, tree): # est-ce que ajout est une expression ?
        tokens = self.visit_children(tree)
        tokens = flattenList(tokens)

        if tokens[1].type == "TEXTE":
            return Token("TEXTE", tokens[1].value[:-1] + tokens[0].value[1:])
        res = tokens[1].value
        res.append(tokens[0].value)
        return Token("leslistes", res)

    def si(self, tree): #todo
        return self.visit_children(tree)

    def sisinon(self, tree): #todo
        return self.visit_children(tree)

    def tantque(self, tree): #todo
        return self.visit_children(tree)

    def pourchaque(self, tree): #todo
        return self.visit_children(tree)

    def exp(self, tree):
        return self.visit_children(tree)

    def parenthese(self, tree): #todo
        return self.visit_children(tree)

    def literal(self, tree):
        for token in tree.scan_values(lambda x: isinstance(x, Token)):
            if token.type == "ENTIER":
                token.value = int(token.value)

        return self.visit_children(tree)

    def leslistes(self, tree):
        return self.visit_children(tree)

    def liste(self, tree):
        tokens = self.visit_children(tree)
        tokens = flattenList(tokens)
        l = []
        for t in tokens:
            l.append(t.value)

        return Token("liste", l)

    def sequence(self, tree):
        tokens = self.visit_children(tree)
        tokens = flattenList(tokens)
        vars = []
        return Token("liste", [i for i in range(tokens[0].value, tokens[1].value + 1)])

    def operation(self, tree):
        return self.visit_children(tree)

    def egalite(self, tree):
        res = self.visit_children(tree)
        res = flattenList(res)
        return Token("BOOLEEN", value.egalite(res))

    def nonegalite(self, tree):
        res = self.visit_children(tree)
        res = flattenList(res)
        return Token("BOOLEEN", value.nonegalite(res))

    def pluspetit(self, tree):
        res = self.visit_children(tree)
        res = flattenList(res)
        return Token("BOOLEEN", value.pluspetit(res))

    def plusgrand(self, tree):
        res = self.visit_children(tree)
        res = flattenList(res)
        return Token("BOOLEEN", value.plusgrand(res))

    def pluspetitouegal(self, tree):
        res = self.visit_children(tree)
        res = flattenList(res)
        return Token("BOOLEEN", value.pluspetitouegal(res))

    def plusgrandouegal(self, tree):
        res = self.visit_children(tree)
        res = flattenList(res)
        return Token("BOOLEEN", value.plusgrandouegal(res))

    def et(self, tree):
        res = self.visit_children(tree)
        res = flattenList(res)
        return Token("BOOLEEN", value.et(res))

    def ou(self, tree):
        res = self.visit_children(tree)
        res = flattenList(res)
        return Token("BOOLEEN", value.ou(res))

    def non(self, tree):
        res = self.visit_children(tree)
        res = flattenList(res)
        return Token("BOOLEEN", value.non(res[0]))

    def negation(self, tree):
        res = self.visit_children(tree)
        res = flattenList(res)
        return Token("ENTIER", value.negation(res[0]))

    def addition(self, tree):
        res = self.visit_children(tree)
        res = flattenList(res)
        return Token("ENTIER", value.calcul(res, lambda n1, n2: n1 + n2))

    def soustraction(self, tree):
        res = self.visit_children(tree)
        res = flattenList(res)
        return Token("ENTIER", value.calcul(res, lambda n1, n2: n1 - n2))

    def multiplication(self, tree):
        res = self.visit_children(tree)
        res = flattenList(res)
        return Token("ENTIER", value.calcul(res, lambda n1, n2: n1 * n2))

    def division(self, tree):
        res = self.visit_children(tree)
        res = flattenList(res)
        return Token("ENTIER", value.calcul(res, lambda n1, n2: n1 / n2))

    def indice(self, tree):
        res = self.visit_children(tree)
        res = flattenList(res)

        flag = True
        s = ""
        l = []
        index = 0

        for token in res:
            match token.type:
                case "TEXTE":
                    s= token.value[1:-1]
                    flag = True
                case "liste":
                    l = token.value
                    flag = False
                case "ENTIER":
                    index = token.value


        if flag:
            if index <= 0 or len(s) > abs(index):
                pass #erreur
            return Token("TEXTE", s[index-1])
        
        if index <= 0 or len(l) >= abs(index):
            pass #erreur
        return Token("liste", l[index-1])

    def taille(self, tree):
        res = self.visit_children(tree)
        res = flattenList(res)
        return Token("ENTIER", len(res[0].value))

parser = Lark.open("spf.lark", parser='lalr')
interpreter = MyInterpreter()

if __name__ == '__main__':
    parser_argument = argparse.ArgumentParser(description="Simple Programme en Français")
    parser_argument.add_argument("file", help="Le fichier a exécuter", type=str)
    parser_argument.add_argument("-m", "--memory", action="store_true", help="Affiche la mémoire du programme à l'issue de son exécution")
    parser_argument.add_argument("-d", "--debug", action="store_true", help="Affiche les variables lors de leur déclaration, utilisation ou modification")
    args = parser_argument.parse_args()

    memo = back.Memory(args.debug)
    value = back.Value()

    with open(args.file) as f:
        tree = parser.parse(f.read())
    interpreter.visit(tree)

    if args.memory:
        print("\n--- Mémoire final ---\n")
        print(memo)

    """
    try:
        raise error.SPFSyntaxError("l'erreur")
    except error.SPFSyntaxError as e:
        print(e)
    """

