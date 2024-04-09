import linecache as lc 

def setFile(f):
    global file
    file = f

class SPFException(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return self.error
    
class SPFSyntaxError(SPFException):
    def __init__(self, error):
        self.error = error

class SPFUninitializedVariable(SPFException):
    def __init__(self, variable, line_error, line_declare, column):
        global file
        line_code = lc.getline(file, line_error) 
        surligne = " " * (column-1) + "^" + "~" * (len(variable)-1)
        show = f"{line_code[:-1]}\n{surligne}\n\n"
        super().__init__(f"{show}SPFUninitializedVariable : la variable '{variable}' est utilisé à la ligne {line_error} mais n'a pas été initialisée ! Elle a été déclarée à la ligne {line_declare}.")

class SPFUnknownVariable(SPFException):
    def __init__(self, variable, line_error, column):
        global file
        line_code = lc.getline(file, line_error) 
        surligne = " " * (column-1) + "^" + "~" * (len(variable)-1)
        show = f"{line_code[:-1]}\n{surligne}\n\n"
        super().__init__(f"{show}SPFUnknownVariable : la variable '{variable}' à la ligne {line_error} n'est pas déclarée !")

class SPFAlreadyDefined(SPFException):
    def __init__(self, variable, line_error, line_declare, column):
        global file
        line_code = lc.getline(file, line_error) 
        surligne = " " * (column-1) + "^" + "~" * (len(variable)-1)
        show = f"{line_code[:-1]}\n{surligne}\n\n"
        super().__init__(f"{show}SPFAlreadyDefined : la variable '{variable}' à la ligne {line_error} a déjà été déclarée à la ligne {line_declare} !")

#todo revoir l'explitacion de l'erreur, ca peut-être autre chose qu'une variable
class SPFIncompatibleType(SPFException):
    def __init__(self, variable, types, line_error, column):
        for i in range(len(types)):
            if types[i] == "BOOLEEN":
                types[i] = "booléen"
            elif types[i] == "ENTIER":
                types[i] = "entier"
            elif types[i] == "TEXTE":
                types[i] = "texte"

        global file
        line_code = lc.getline(file, line_error) 
        surligne = " " * (column-1) + "^" + "~" * (len(variable)-1)
        show = f"{line_code[:-1]}\n{surligne}\n\n"
        super().__init__(f"{show}SPFIncompatibleType : le terme '{variable}' à la ligne {line_error} est de type {types[1]}, ce qui est incompatible avec le type {types[0]} !")

#todo revoir l'explitacion de l'erreur ( indice entre 1 et n)
class SPFIndexError(SPFException):
    def __init__(self, position, line_error, column):
        global file
        line_code = lc.getline(file, line_error) 
        surligne = " " * (column-1) + "^" + "~" * (len(str(position))-1)
        show = f"{line_code[:-1]}\n{surligne}\n\n"
        super().__init__(f"{show}SPFIndexError : La position {position} que vous utilisez à la ligne {line_error} n'existe pas !")

