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
        self.stack = []

    def declare(self, var):
        if self.flag_debug:
            print("déclaration:".ljust(15), var)

        global max
        if len(var.name) > max:
            max = len(var.name)
        self.stack.append(var)

    def get(self, var):
        if self.flag_debug:
            print("accès:".ljust(15), var)

        return self.stack.get(var)

    def set(self, name, value):
        for var in self.stack:
            if var.name == name:
                var.value = value
                break

        if self.flag_debug:
            print("modification:".ljust(15), var)

    def typeof(self, var):
        return (memo.get(var)).typeof

    def __str__(self):
        res = ""
        for var in self.stack:
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
    def __init__(self):
        pass

    def egalite(self, tokens):
        vars = []
        flag = []

        for t in tokens:
            match t.type:
                case "BOOLEEN":
                    vars.append(t.value)
                    flag.append("BOOLEEN")
                case "ENTIER":
                    vars.append(t.value)
                    flag.append("ENTIER")
                case "TEXTE":
                    vars.append(t.value)
                    flag.append("TEXTE")
                case "LISTE":
                    vars.append(t.value)
                    flag.append("LISTE")

        if flag[0] != flag[1]:
            pass #erreur

        if vars[0] == vars[1]:
            return "vrai"
        return "faux"

    def nonegalite(self, tokens):
        if self.egalite(tokens) == "vrai":
            return "faux"
        return "vrai"

    def pluspetit(self, tokens):
        for t in tokens:
            if t.type != "ENTIER":
                    pass #erreur

        if int(tokens[0].value) < int(tokens[1].value):
            return "vrai"
        return "faux"

    def plusgrand(self, tokens):
        if self.pluspetit(tokens) == "vrai":
            return "faux"
        return "vrai"

    def pluspetitouegal(self, tokens):
        for t in tokens:
            if t.type != "ENTIER":
                    pass #erreur

        if int(tokens[0].value) <= int(tokens[1].value):
            return "vrai"
        return "faux"

    def plusgrandouegal(self, tokens):
        if self.pluspetitouegal(tokens) == "vrai":
            return "faux"
        return "vrai"

    def et(self, tokens):
        for t in tokens:
            if t.type != "BOOLEEN":
                    pass #erreur

        if tokens[0].value == "vrai" and tokens[1].value == "vrai":
            return "vrai"
        return "faux"

    def ou(self, tokens):
        for t in tokens:
            if t.type != "BOOLEEN":
                    pass #erreur

        if tokens[0].value == "vrai" or tokens[1].value == "vrai":
            return "vrai"
        return "faux"

    def non(self, token):
        if token.type != "BOOLEEN":
                    pass #erreur

        if token.value == "vrai":
            return "faux"
        return "vrai"

    def negation(self, token):
        if token.type != "ENTIER":
                    pass #erreur

        return - int(token)

    def addition(self, tokens):
        for t in tokens:
            if t.type != "ENTIER":
                    pass #erreur

        return int(tokens[0].value) + int(tokens[1].value)

    def soustraction(self, tokens):
        pass

    def multiplication(self, tokens):
        pass

    def division(self, tokens):
        pass

