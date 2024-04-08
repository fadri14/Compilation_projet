import sys
from copy import deepcopy
from modules.exception import SPFException, SPFUnknownVariable, SPFAlreadyDefined, SPFIncompatibleType, SPFUninitializedVariable

max = 0

class Memory(): # Stocke les variables
    def __init__(self, flag_debug, flag_tableau):
        self.flag_debug = flag_debug
        self.flag_tableau = flag_tableau
        self.dico = {}
        self.tmp = {}
        self.keyword = ["booléen", "entier", "texte", "liste", "afficher", "ajouter", "dans", "si", "alors", "sinon", "tant", "que", "faire", "pour", "chaque", "ne", "vaut", "pas", "et", "ou", "non", "taille"]

    # on force quand on crée la variable d'une boucle
    def declare(self, var, force = False):
        if not force and var.name in self.dico.keys():
            var2 = self.dico.get(var.name)
            raise SPFAlreadyDefined(var.name, var.line, var2.line)

        if var.name in self.keyword:
            pass #erreur

        if self.flag_debug:
            print("(", var.line, ")", "déclaration:".ljust(15), var, file=sys.stderr)

        if force and var.name in self.dico.keys():
            t = self.dico.get(var.name)
            self.tmp[t.name] = t
            del self.dico[var.name]

        global max
        if len(var.name) > max:
            max = len(var.name)

        self.dico[var.name] = var

    def get(self, name, line):
        if not name in self.dico.keys():
            raise SPFUnknownVariable(name, line)

        var = deepcopy(self.dico.get(name))

        if var.value == None:
            raise SPFUninitializedVariable(name, line, var.line)

        if self.flag_debug:
            print("(", line, ")", "accès:".ljust(15), var, file=sys.stderr)

        if var.typeof == "booléen":
            var.typeof = "BOOLEEN"
        elif var.typeof == "entier":
            var.typeof = "ENTIER"
        elif var.typeof == "texte":
            var.typeof = "TEXTE"
        else:
            var.typeof = (var.typeof, var.listType)

        return var

    def set(self, name, value, typeof, line):
        if not name in self.dico.keys():
            raise SPFUnknownVariable(name, line)

        var = self.dico.get(name)
        if var.typeof != typeof:
            pass #erreur

        if var.typeof == 'liste':
            var.value = value[0]
            var.listType = value[1]
        else:
            var.value = value

        if self.flag_debug:
            print("(", line, ")", "modification:".ljust(15), self.dico.get(name), file=sys.stderr)

    def delete(self, name):
        del self.dico[name]
        if name in self.tmp.keys(): # en théorie dans notre cas toujours vrai
            d = self.tmp.get(name)
            self.dico[d.name] = d
            del self.tmp[name]

    def __str__(self):
        res = ""
        for var in self.dico.values():
            if self.flag_tableau:
                res += var.__str__()
            else:
                res += f"{var.typeof.ljust(7)} {var.name.ljust(max)} = {var.value}"
            res += "\n"

        return res

class Variable(): # Représente une variable
    def __init__(self):
        self.typeof = None
        self.name = None
        self.value = None
        self.line = None
        self.listType = None

    def __str__(self):
        res = self.value.__str__().replace("'", "")
        return f"| nom: {self.name.ljust(max)} | type: {self.typeof.ljust(7)} | valeur: {res}"

class Value(): # Effectue les calculs
    def deco(self, tokens, type_tokens, func):
        try:
            for t in tokens:
                if t.type != type_tokens:
                        raise SPFIncompatibleType(t.value, t.type, type_tokens, t.line)

            if func(tokens):
                return "vrai"
            return "faux"
        except SPFException as e:
            print(e.error)
            sys.exit(0)

    def egalite(self, tokens):
        try:
            if tokens[0].type != tokens[1].type:
                raise SPFIncompatibleType(tokens[0].value, tokens[0].type, tokens[1].type, tokens[0].line)

            if tokens[0].value == tokens[1].value:
                return "vrai"
            return "faux"
        except SPFException as e:
            print(e)
            sys.exit(0)

    def nonegalite(self, tokens):
        if self.egalite(tokens) == "vrai":
            return "faux"
        return "vrai"

    def pluspetit(self, tokens):
        return self.deco(tokens, "ENTIER", lambda args : args[0].value < args[1].value)

    def plusgrand(self, tokens):
        return self.deco(tokens, "ENTIER", lambda args : args[0].value > args[1].value)

    def pluspetitouegal(self, tokens):
        return self.deco(tokens, "ENTIER", lambda args : args[0].value <= args[1].value)

    def plusgrandouegal(self, tokens):
        return self.deco(tokens, "ENTIER", lambda args : args[0].value >= args[1].value)

    def et(self, tokens):
        return self.deco(tokens, "BOOLEEN", lambda args : args[0].value == "vrai" and args[1].value == "vrai")

    def ou(self, tokens):
        return self.deco(tokens, "BOOLEEN", lambda args : args[0].value == "vrai" or args[1].value == "vrai")

    def non(self, tokens):
        return self.deco(tokens, "BOOLEEN", lambda args : args[0].value != "vrai")

    def negation(self, token):
        try:
            if token[0].type != "ENTIER":
                raise SPFIncompatibleType(token[0].value, token[0].type, "ENTIER", token[0].line)

            return - token[0].value
        except SPFException as e:
            print(e.error)
            sys.exit(0)

    # operation est une fonction lambda effectuant une opération entre deux nombres
    def calcul(self, tokens, operation):
        try:
            for t in tokens:
                if t.type != "ENTIER":
                    raise SPFIncompatibleType(t.value, t.type, "ENTIER", t.line)

            return operation(tokens[0].value, tokens[1].value)
        except SPFException as e:
            print(e)
            sys.exit(0)

