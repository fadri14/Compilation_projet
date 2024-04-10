import linecache as lc 

def setFile(f):
    global file
    file = f

class SPFException(Exception):
    def __init__(self, error, info): # info = (variable, line_error, column)
        global file
        line_code = lc.getline(file, info[1]) 
        surligne = " " * (info[2]-1) + "^" + "~" * (len(str(info[0]))-1)
        show = f"{line_code[:-1]}\n{surligne}\n"
        self.error = show + error

    def __str__(self):
        return self.error
    
class SPFSyntaxError(SPFException):
    def __init__(self, info, expected = None):
        sufix = ""
        if expected != None:
            tmp = ""
            for e in expected:
                tmp += ("  " + e + ",\n")
            expected = "\n" + tmp
            sufix = f"\n\nUn des tokens suivants étaient attendus:\n{expected}"
        super().__init__(f"SPFSyntaxError : il y a une erreur de syntaxe à la ligne {info[1]} par rapport au terme '{info[0]}'.{sufix}", info)

class SPFUninitializedVariable(SPFException):
    def __init__(self, info, line_declare):
        super().__init__(f"SPFUninitializedVariable : la variable '{info[0]}' est utilisé à la ligne {info[1]} mais n'a pas été initialisée ! Elle a été déclarée à la ligne {line_declare}.", info)

class SPFUnknownVariable(SPFException):
    def __init__(self, info):
        super().__init__(f"SPFUnknownVariable : la variable '{info[0]}' à la ligne {info[1]} n'est pas déclarée !", info)

class SPFAlreadyDefined(SPFException):
    def __init__(self, info, line_declare):
        super().__init__(f"SPFAlreadyDefined : la variable '{info[0]}' à la ligne {info[1]} a déjà été déclarée à la ligne {line_declare} !", info)

class SPFIncompatibleType(SPFException):
    def __init__(self, info, types):
        for i in range(len(types)):
            if types[i] == "BOOLEEN":
                types[i] = "booléen"
            elif types[i] == "ENTIER":
                types[i] = "entier"
            elif types[i] == "TEXTE":
                types[i] = "texte"

        super().__init__(f"SPFIncompatibleType : le terme '{info[0]}' à la ligne {info[1]} est de type {types[1]}, ce qui est incompatible avec le type {types[0]} !", info)

class SPFIndexError(SPFException):
    def __init__(self, info):
        super().__init__(f"SPFIndexError : La position {info[0]} que vous utilisez à la ligne {info[1]} est invalide, il doit être compris entre 1 et la taille du terme !", info)

