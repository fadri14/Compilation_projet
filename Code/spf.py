import sys
import argparse
from lark import Lark, Token
from lark.visitors import Interpreter
import modules.backend as back
from copy import deepcopy
from modules.exception import SPFException, SPFUnknownVariable, SPFAlreadyDefined, SPFIndexError, SPFIncompatibleType

#todo:
# changer toutes types dans les messages d'erreurs pour les mettres en minuscule
# régler l'exemple de boucle pour chaque donné dans le pdf
# réessayer plusieurs composanstes
# faire les priorités des opérations
# chercher toutes les erreurs de types incompatibles
# faire la gestion d'erreur pour la syntaxe

# Transforme une liste à plusieurs dimensions en une dimension
def flattenList(l):
    resultat = []
    for element in l:
        if isinstance(element, list):
            resultat.extend(flattenList(element))
        else:
            resultat.append(element)
    return resultat

# Sépare les valeurs des types dans un liste du genre [(1, 'ENTIER'), ('yo', 'TEXTE')]
def decomposeList(l, d = 0):
    v = []
    t = []
    for element in l:
        if isinstance(element, list) or isinstance(element, tuple) and isinstance(element[0], list):
            resV, resT = decomposeList(element, d +1)
            if d%2 == 0: # quand c'est une profondeur impaire, cela signifie que c'est un tuple superflux qui dit que c'est une liste donc il ne faut pas rajouter une profondeur
                v.append(resV)
                t.append(resT)
            else:
                v.extend(resV)
                t.extend(resT)
        elif element[0] != 'l':
            v.append(element[0])
            t.append(element[1])
    return v, t

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
        var.line = tokens[1].line
        if len(tokens) == 3:
            if isinstance(var.typeof, tuple):
                var.listType = tokens[2].type[1]
            var.value = tokens[2].value

        try:
            memo.declare(var)
        except SPFException as e:
                print(e)
                sys.exit(0)

    def assignation(self, tree):
        token = self.visit_children(tree)
        token = flattenList(token)
        
        try:
            if isinstance(token[1].type , tuple):
                memo.set(token[0].value, (token[1].value, token[1].type[1]), token[1].type, token[0].line)
            else:
                memo.set(token[0].value, token[1].value, token[1].type, token[0].line)
        except SPFException as e:
                print(e)
                sys.exit(0)

    def afficher(self, tree):
        tokens = self.visit_children(tree)
        tokens = flattenList(tokens)

        res = ""
        for i in range(len(tokens)):
            res += str(tokens[i].value.__str__().replace("'", ""))

            if i != len(tokens) -1:
                res += " "

        print(res)

    def ajout(self, tree):
        tokens = self.visit_children(tree)
        tokens = flattenList(tokens)

        try:
            var = memo.get(tokens[1].value, tokens[1].line)

            if isinstance(var.typeof, tuple) and var.typeof[0] != "liste":
                raise SPFIncompatibleType(var.value, var.typeof, "BOOLEEN", tokens[1].line)

            values = var.value
            values.append(tokens[0].value)
            types = var.listType
            types.append(tokens[0].type)

            memo.set(var.name, (values, types), tokens[0].type, tokens[0].line)
        except SPFException as e:
                print(e)
                sys.exit(0)

        return Token(("liste", types), values)

    def si(self, tree):
        test = self.visit(tree.children[0])
        test = flattenList(test)[0]

        try:
            if test.type != "BOOLEEN":
                raise SPFIncompatibleType(test.value, test.type, "BOOLEEN", test.line)
        except SPFException as e:
            print(e)
            sys.exit(0)

        if test.value == "vrai":
            for i in tree.children[1:]:
                self.visit(i)
        return test.value

    def sisinon(self, tree):
        test = self.visit(tree.children[0])

        if test == "faux":
            for c in tree.children[1:]:
                self.visit(c)

    def tantque(self, tree):
        tree_copy = deepcopy(tree)
        while True:
            test = self.visit(tree.children[0])
            test = flattenList(test)[0]
            try:
                if test.type != "BOOLEEN":
                    raise SPFIncompatibleType(test.value, test.type, "BOOLEEN", test.line)
            except SPFException as e:
                print(e)
                sys.exit(0)

            if test.value == "vrai":
                for i in tree.children[1:]:
                    self.visit(i)
                tree = deepcopy(tree_copy)
            else:
                break

    def pourchaque(self, tree):
        tree_copy = deepcopy(tree)

        var = back.Variable()
        var.typeof = tree.children[0].value
        var.name = tree.children[1].value
        var.line = tree.children[1].line

        memo.declare(var, True)

        iter = self.visit(tree.children[2])
        iter = flattenList(iter)[0].value

        for t in iter:
            memo.set(var.name, t, tree.children[1].type, tree.children[1].line)
            for i in tree.children[3:]:
                self.visit(i)
            tree = deepcopy(tree_copy)
        memo.delete(var.name)

    def exp(self, tree):
        for token in tree.scan_values(lambda x: isinstance(x, Token)):
            if token.type == "VARIABLE":
                try:
                    var = memo.get(token.value, token.line)
                except SPFException as e:
                        print(e)
                        sys.exit(0)
                
                token.type, token.value = var.typeof, var.value
        return self.visit_children(tree)

    def parenthese(self, tree):
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
            elem = (t.value, t.type)
            l.append(elem)

        l, t = decomposeList(l)
        return Token(("liste", t), l)

    def sequence(self, tree):
        tokens = self.visit_children(tree)
        tokens = flattenList(tokens)
        step = 1
        if(tokens[0].value - tokens[1].value > 0):
            step = -1
        t = ("liste", ["ENTIER"]+["ENTIER"]*((tokens[1].value - tokens[0].value)*step))
        return Token(t, [_ for _ in range(tokens[0].value, tokens[1].value + step, step)])

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
        tokens = self.visit_children(tree)
        tokens = flattenList(tokens)

        try:
            if tokens[0].type != tokens[1].type or not (isinstance(tokens[0].type, tuple) and isinstance(tokens[1].type, tuple)):
                raise SPFIncompatibleType(tokens[0].value, tokens[0].type, tokens[1].type, tokens[0].line)

            if isinstance(tokens[0].type, tuple):
                res = tokens[0].value
                res.extend(tokens[1].value)
                t = tokens[0].type[1]
                t.extend(tokens[1].type[1])
                return Token(("liste", t), res)
            elif tokens[0].type == "TEXTE":
                return Token("TEXTE", tokens[0].value + tokens[1].value)
            else:
                return Token(tokens[0].type, value.calcul(tokens, lambda n1, n2: n1 + n2))
        except SPFException as e:
            print(e)
            sys.exit(0)

    def soustraction(self, tree):
        return self.deco(tree, "ENTIER", lambda tokens: value.calcul(tokens, lambda n1, n2: n1 - n2))

    def multiplication(self, tree):
        return self.deco(tree, "ENTIER", lambda tokens: value.calcul(tokens, lambda n1, n2: n1 * n2))

    def division(self, tree):
        return self.deco(tree, "ENTIER", lambda tokens: value.calcul(tokens, lambda n1, n2: n1 / n2))

    def indice(self, tree):
        tokens = self.visit_children(tree)
        tokens = flattenList(tokens)

        try: 
            if tokens[1].type == "ENTIER":
                if tokens[0].type == "TEXTE" or isinstance(tokens[0].type, tuple):
                    if tokens[1].value <= 0 or len(tokens[0].value) < tokens[1].value:
                        raise SPFIndexError(tokens[0].line, tokens[1].value)                    
                    else:
                        if tokens[0].type[0] == "liste" :
                            return Token(tokens[0].type[1][tokens[1].value-1], tokens[0].value[tokens[1].value-1])

                        return Token("TEXTE", tokens[0].value[tokens[1].value-1])
                else:
                    raise SPFIncompatibleType(tokens[0].value, tokens[0].type, "TEXTE ou liste", tokens[0].line)
            else:
                raise SPFIncompatibleType(tokens[1].value, tokens[1].type, "ENTIER", tokens[1].line)
        except SPFException as e:
            print(e)
            sys.exit(0)

    def taille(self, tree):
        return self.deco(tree, "ENTIER", lambda tokens: len(tokens[0].value))

parser = Lark.open("spf.lark", parser='lalr')
interpreter = MyInterpreter()

if __name__ == '__main__':
    parser_argument = argparse.ArgumentParser(description="Simple Programme en Français")
    parser_argument.add_argument("file", help="Le fichier a exécuter", type=str)
    parser_argument.add_argument("-m", "--memory", action="store_true", help="Affiche la mémoire du programme à l'issue de son exécution")
    parser_argument.add_argument("-d", "--debug", action="store_true", help="Affiche les variables lors de leur déclaration, utilisation ou modification")
    parser_argument.add_argument("-t", "--tableau", action="store_true", help="Affiche un tableau pour illustrer la mémoire")
    args = parser_argument.parse_args()

    memo = back.Memory(args.debug, args.tableau)
    
    value = back.Value()

    with open(args.file) as f:
        tree = parser.parse(f.read())
    interpreter.visit(tree)
    
    if args.memory:
        print("\n--- Mémoire final ---\n", file=sys.stderr)
        print(memo, file=sys.stderr)

