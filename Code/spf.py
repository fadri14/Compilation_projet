import sys
import argparse
import re
from lark import Lark, Token
from lark.visitors import Interpreter
import modules.exception as error
import modules.backend as back

# Transforme une liste à plusieurs dimensions en une dimension
def flattenList(l):
    resultat = []
    for element in l:
        if isinstance(element, list):
            resultat.extend(flattenList(element))
        else:
            resultat.append(element)
    return resultat

class MyInterpreter(Interpreter):
    def start(self, tree):
        print(tree)
        print()
        print()
        print()
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
                case "RES":
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
        return self.visit_children(tree)

    def ajout(self, tree):
        return self.visit_children(tree)

    def si(self, tree):
        return self.visit_children(tree)

    def sisinon(self, tree):
        return self.visit_children(tree)

    def tantque(self, tree):
        return self.visit_children(tree)

    def pourchaque(self, tree):
        return self.visit_children(tree)

    def exp(self, tree):
        """
        print("3-------")
        print(tree)
        for token in tree.scan_values(lambda x: isinstance(x, Token)):
            print(token.line)
            print(token.value)
        """
        return self.visit_children(tree)

    def parenthese(self, tree):
        return self.visit_children(tree)

    def literal(self, tree):
        for token in tree.scan_values(lambda x: isinstance(x, Token)):
            match token.type:
                case "sequence":
                    pass # utiliser range
                case default:
                    return Token("RES", token.value)

        #return self.visit_children(tree)

    def liste(self, tree):
        return self.visit_children(tree)

    def sequence(self, tree):
        return self.visit_children(tree)

    def egalite(self, tree):
        res = self.visit_children(tree)
        return res[0][0] and res[1][0]

    def nonegalite(self, tree):
        return self.visit_children(tree)

    def pluspetit(self, tree):
        return self.visit_children(tree)

    def plusgrand(self, tree):
        return self.visit_children(tree)

    def pluspetitouegal(self, tree):
        return self.visit_children(tree)

    def plusgrandouegal(self, tree):
        return self.visit_children(tree)

    def et(self, tree):
        return self.visit_children(tree)

    def ou(self, tree):
        return self.visit_children(tree)

    def non(self, tree):
        return self.visit_children(tree)

    def negation(self, tree):
        return self.visit_children(tree)

    def addition(self, tree):
        return self.visit_children(tree)

    def soustraction(self, tree):
        return self.visit_children(tree)

    def multiplication(self, tree):
        return self.visit_children(tree)

    def division(self, tree):
        return self.visit_children(tree)

    def indice(self, tree):
        return self.visit_children(tree)

    def taille(self, tree):
        return self.visit_children(tree)

parser = Lark.open("spf.lark", parser='lalr')
interpreter = MyInterpreter()

if __name__ == '__main__':
    parser_argument = argparse.ArgumentParser(description="Simple Programme en Français")
    parser_argument.add_argument("file", help="Le fichier a exécuter", type=str)
    parser_argument.add_argument("-m", "--memory", action="store_true", help="Affiche la mémoire du programme à l'issue de son exécution")
    parser_argument.add_argument("-d", "--debug", action="store_true", help="Affiche les variables lors de leur déclaration, utilisation ou modification")
    args = parser_argument.parse_args()

    memo = back.Memory(args.debug)

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

