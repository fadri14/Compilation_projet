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
