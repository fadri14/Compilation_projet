class SPFException(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return self.error

class SPFSyntaxError(SPFException):
    def __init__(self, error):
        self.error = error

class SPFUninitializedVariable(SPFException):
    def __init__(self, variable, line_error, line_declare):
        super().__init__(f"SPFUninitializedVariable : la variable '{variable}' est utilisé à la ligne {line_error} mais n'a pas été initialisée ! Elle a été déclarée à la ligne {line_declare}.")

class SPFUnknownVariable(SPFException):
    def __init__(self, variable, line_error):
        super().__init__(f"SPFUnknownVariable : la variable '{variable}' à la ligne {line_error} n'est pas déclarée !")

class SPFAlreadyDefined(SPFException):
    def __init__(self, variable, line_error, line_declare):
        super().__init__(f"SPFAlreadyDefined : la variable '{variable}' à la ligne {line_error} a déjà été déclarée à la ligne {line_declare} !")

#todo revoir l'explitacion de l'erreur, ca peut-être autre chose qu'une variable
class SPFIncompatibleType(SPFException):
    def __init__(self, variable, types, line_error):
        for i in range(len(types)):
            if types[i] == "BOOLEEN":
                types[i] = "booléen"
            elif types[i] == "ENTIER":
                types[i] = "entier"
            elif types[i] == "TEXTE":
                types[i] = "texte"

        super().__init__(f"SPFIncompatibleType : la variable '{variable}' à la ligne {line_error} possède un type {types[0]}, ce qui est incompatible avec le type {types[0]} !")

#todo revoir l'explitacion de l'erreur ( indice entre 1 et n)
class SPFIndexError(SPFException):
    def __init__(self, line_error, position):
        super().__init__(f"SPFIndexError : La position {position} que vous utilisez à la ligne {line_error} n'existe pas !")

