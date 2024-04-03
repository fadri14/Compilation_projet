from enum import Enum

class Type(Enum):
    ENTIER = 1
    BOOLEEN = 2
    TEXTE = 3
    LISTE = 4

max = 0

class Memory(): # Stocke les variables
    def __init__(self, flag_debug):
        self.flag_debug = flag_debug
        self.dico = {}

    def declare(self, var):
        # pour vérifier s'il n'existe pas déjà : dico.has_key(var.name)
        if self.flag_debug:
            print("déclaration:".ljust(15), var)

        global max
        if len(var.name) > max:
            max = len(var.name)

        self.dico[var.name] = var

    def get(self, name):
        var = self.dico.get(name)

        if var.value == None:
            pass #erreur

        if self.flag_debug:
            print("accès:".ljust(15), var)

        return var

    def set(self, name, value):
        self.dico.get(name).value = value

        if self.flag_debug:
            print("modification:".ljust(15), name)

    # ne sert à rien…
    def typeof(self, var):
        return (memo.get(var)).typeof

    def __str__(self):
        res = ""
        for var in self.dico.values():
            res += var.__str__()
            res += "\n"

        return res

class Variable(): # Représente une variable
    def __init__(self):
        self.typeof = None
        self.name = None
        self.value = None

    def __str__(self):
        return f"| nom: {self.name.ljust(max)} | type: {self.typeof.ljust(7)} | valeur: {self.value}"

class Value(): # Effectue les calcules
    def deco(self, tokens, type_tokens, func):
        for t in tokens:
            if t.type != type_tokens:
                    pass #erreur

        if func(tokens):
            return "vrai"
        return "faux"

    def egalite(self, tokens):
        if tokens[0].type != tokens[1].type:
            pass #erreur

        if tokens[0].value == tokens[1].value:
            return "vrai"
        return "faux"

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
        if token[0].type != "ENTIER":
                    pass #erreur

        return - token[0].value

    # operation est une fonction lambda effectuant une opération entre deux nombres
    def calcul(self, tokens, operation):
        for t in tokens:
            if t.type != "ENTIER":
                    pass #erreur

        return operation(tokens[0].value, tokens[1].value)

