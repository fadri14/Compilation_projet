import sys
from enum import Enum
from copy import deepcopy
from modules.exception import SPFUnknownVariable, SPFAlreadyDefined

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
        self.tmp = {}
        #new traceback
        self.variableLine = []
        self.keyword = ["booléen", "entier", "texte", "liste", "afficher", "ajouter", "dans", "si", "alors", "sinon", "tant", "que", "faire", "pour", "chaque", "ne", "vaut", "pas", "et", "ou", "non", "taille"]

    # on force quand on crée la variable d'une boucle
    def declare(self, var, force, line = -1):
        #new SPFAlreadyDefined
        if not force and var.name in self.dico.keys():
            #new traceback
            index = []
            for key in self.dico:
                if key == var.name:
                    index.append(list(self.dico.keys()).index(key)) 
                    #Récupérer tous les indices où le mot apparaît dans le dico
                    #car on peut s'arrêter sur un nom créé dans une boucle ie line = -1 

            for i in index:
                if(index != -1):
                    index = list(self.dico.keys()).index(var.name)

            raise SPFAlreadyDefined(var.name, 0, self.variableLine[index])

        if var.name in self.keyword:
            pass #erreur

        if self.flag_debug:
            print("déclaration:".ljust(15), var, file=sys.stderr)

        if force and var.name in self.dico.keys():
            t = self.dico.get(var.name)
            self.tmp[t.name] = t
            del self.dico[var.name]

        global max
        if len(var.name) > max:
            max = len(var.name)

        self.dico[var.name] = var
        self.variableLine.append(line) #traceback

    def get(self, name):
        if not name in self.dico.keys():
            #new SPFUnknownVariable
            raise SPFUnknownVariable(name, 0)

        var = deepcopy(self.dico.get(name))

        if var.value == None:
            pass #erreur

        if self.flag_debug:
            print("accès:".ljust(15), var, file=sys.stderr)

        '''
        match var.typeof:
            case "booléen":
                var.typeof = "BOOLEEN"
            case "entier":
                var.typeof = "ENTIER"
            case "texte":
                var.typeof = "TEXTE"
        '''
        if var.typeof == "booléen":
            var.typeof = "BOOLEEN"
        elif var.typeof == "entier":
            var.typeof = "ENTIER"
        elif var.typeof == "texte":
            var.typeof = "TEXTE"

        return var

    def set(self, name, value):
        if not name in self.dico.keys():
            #new SPFUnknownVariable
            raise SPFUnknownVariable(name, 0)

        self.dico.get(name).value = value

        if self.flag_debug:
            print("modification:".ljust(15), self.dico.get(name), file=sys.stderr)

    def delete(self, name):
        del self.dico[name]
        if name in self.tmp.keys(): # en théorie dans notre cas toujours vrai
            d = self.tmp.get(name)
            self.dico[d.name] = d
            del self.tmp[name]

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
        res = self.value
        if isinstance(res, list) and len(res) != 0 and isinstance(res[0], tuple): #new (gestion types liste)
                l = "["
                for i in range(len(res)):
                    #new Le soucis de ' ds la liste pour les booléens A revoir ???
                    if res[i][1] == "BOOLEEN" or res[i][1] == "ENTIER":
                        l +=  str(res[i][0]) 

                    else:
                        l += "'" + str(res[i][0]) + "'"

                    if(i != len(res)-1):
                        l += ", "

                res = l + "]"
            
        return f"| nom: {self.name.ljust(max)} | type: {self.typeof.ljust(7)} | valeur: {res}"

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

