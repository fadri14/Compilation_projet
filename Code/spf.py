import sys
import argparse
import re
from lark import Lark, Token
from lark.visitors import Interpreter
import modules.exception as error
import modules.backend as back
from copy import deepcopy

#todo:
# comment afficher les booléens sans ' : [Token('BOOLEEN', 'vrai')]
#   quand c'est uniquement un booléen, c'est correct. le problème est dans une liste
# faire la gestion d'erreur
# corriger les problèmes de calculs
# gérer l'addition pour les textes et les listes

#note:
# peut-on avoir des " dans une chaine de caractère
# est-ce que ajout est une expression ?

# Transforme une liste à plusieurs dimensions en une dimension
def flattenList(l):
    resultat = []
    for element in l:
        if isinstance(element, list):
            resultat.extend(flattenList(element))
        else:
            resultat.append(element)
    return resultat

# Apparement si on met juste return self.visit_children(tree) dans une fonction on peut la retirer
class MyInterpreter(Interpreter):
    def deco(self, tree, type_res, func):
        tokens = self.visit_children(tree)
        tokens = flattenList(tokens)
        return Token(type_res, func(tokens))

    def start(self, tree):
        return self.visit_children(tree)

    def instruction(self, tree):
        return self.visit_children(tree)

    def declaration(self, tree):
        var = back.Variable()
        tokens = self.visit_children(tree)
        tokens = flattenList(tokens)

        var.typeof = tokens[0].value
        var.name = tokens[1].value
        if len(tokens) == 3:
            var.value = tokens[2].value

        memo.declare(var)

    def assignation(self, tree):
        token = self.visit_children(tree)
        token = flattenList(token)
        memo.set(token[0].value, token[1].value)

    def afficher(self, tree):
        tokens = self.visit_children(tree)
        tokens = flattenList(tokens)
        res = ""
        for i in range(len(tokens)):
            if tokens[i].type == "TEXTE":
                res += str(tokens[i].value)
            else:
                res += str(tokens[i].value)
            if i != len(tokens) -1:
                res += " "

        print(res)

    def ajout(self, tree):
        tokens = self.visit_children(tree)
        tokens = flattenList(tokens)

        if tokens[1].type == "TEXTE":
            return Token("TEXTE", tokens[1].value[:-1] + tokens[0].value[1:])
        res = tokens[1].value
        res.append(tokens[0].value)
        return Token("leslistes", res)

    def si(self, tree):
        test = self.visit(tree.children[0])
        test = flattenList(test)[0]
        #todo régler le problème de type
        if test.type != "BOOLEEN":
            pass #erreur

        if test.value == "vrai":
            for i in tree.children[1:]:
                self.visit(i)
        return test.value

    def sisinon(self, tree):
        test = self.visit(tree.children[0])

        if test == "faux":
            for c in tree.children[1:]:
                self.visit(c)

    def tantque(self, tree): #todo
        tree_copy = deepcopy(tree)
        while True:
            test = self.visit(tree.children[0])
            test = flattenList(test)[0]
            #todo régler le problème de type
            if test.type != "BOOLEEN":
                pass #erreur

            if test.value == "vrai":
                for i in tree.children[1:]:
                    self.visit(i)
                tree = deepcopy(tree_copy)
            else:
                break

    def pourchaque(self, tree): #todo
        return self.visit_children(tree)

    def exp(self, tree):
        for token in tree.scan_values(lambda x: isinstance(x, Token)):
            if token.type == "VARIABLE":
                var = memo.get(token.value)
                token.type, token.value = var.typeof, var.value
        return self.visit_children(tree)

    def parenthese(self, tree): #todo
        return self.visit_children(tree)

    def literal(self, tree):
        for token in tree.scan_values(lambda x: isinstance(x, Token)):
            if token.type == "ENTIER":
                token.value = int(token.value)
            if token.type == "TEXTE" and token.value[0] == '"' and token.value[-1] == '"':
                token.value = token.value[1:-1]

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
        return Token("liste", [_ for _ in range(tokens[0].value, tokens[1].value + 1)])

    def operation(self, tree):
        return self.visit_children(tree)

    def egalite(self, tree):
        return self.deco(tree, "BOOLEEN", lambda tokens: value.egalite(tokens))

    def nonegalite(self, tree):
        return self.deco(tree, "BOOLEEN", lambda tokens: value.nonegalite(tokens))

    def pluspetit(self, tree):
        return self.deco(tree, "BOOLEEN", lambda tokens: value.pluspetit(tokens))

    def plusgrand(self, tree):
        return self.deco(tree, "BOOLEEN", lambda tokens: value.plusgrand(tokens))

    def pluspetitouegal(self, tree):
        return self.deco(tree, "BOOLEEN", lambda tokens: value.pluspetitouegal(tokens))

    def plusgrandouegal(self, tree):
        return self.deco(tree, "BOOLEEN", lambda tokens: value.plusgrandouegal(tokens))

    def et(self, tree):
        return self.deco(tree, "BOOLEEN", lambda tokens: value.et(tokens))

    def ou(self, tree):
        return self.deco(tree, "BOOLEEN", lambda tokens: value.ou(tokens))

    def non(self, tree):
        return self.deco(tree, "BOOLEEN", lambda tokens: value.non(tokens))

    def negation(self, tree):
        return self.deco(tree, "ENTIER", lambda tokens: value.negation(tokens))

    def addition(self, tree):
        return self.deco(tree, "ENTIER", lambda tokens: value.calcul(tokens, lambda n1, n2: n1 + n2))

    def soustraction(self, tree):
        return self.deco(tree, "ENTIER", lambda tokens: value.calcul(tokens, lambda n1, n2: n1 - n2))

    def multiplication(self, tree):
        return self.deco(tree, "ENTIER", lambda tokens: value.calcul(tokens, lambda n1, n2: n1 * n2))

    def division(self, tree):
        return self.deco(tree, "ENTIER", lambda tokens: value.calcul(tokens, lambda n1, n2: n1 / n2))

    def indice(self, tree):
        tokens = self.visit_children(tree)
        tokens = flattenList(tokens)

        if tokens[1].type == "ENTIER":
            if tokens[0].type == "TEXTE" or tokens[0].type == "liste":
                if tokens[1].value <= 0 or len(tokens[0].value) < tokens[1].value:
                    pass #erreur
                else:
                    #todo ca peut être tous les types, que faire ?
                    return Token("TEXTE", tokens[0].value[tokens[1].value-1])
            else:
                pass #erreur
        else:
            pass #erreur

    def taille(self, tree):
        return self.deco(tree, "ENTIER", lambda tokens: len(tokens[0].value))

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

