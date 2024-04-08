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
        super().__init__(f"SPFUninitializedVariable : la variable '{variable}' est utilisé à la ligne {line_error} mais n'a pas été initialisée ! Voir ligne {line_declare}.")

class SPFUnknownVariable(SPFException):
    def __init__(self, variable, line_error):
        super().__init__(f"SPFUnknownVariable : la variable '{variable}' à la ligne {line_error} n'est pas déclarée !")

class SPFAlreadyDefined(SPFException):
    def __init__(self, variable, line_error, line_declare):
        super().__init__(f"SPFAlreadyDefined : la variable '{variable}' à la ligne {line_error} a déjà été déclarée à la ligne {line_declare} !")

#todo revoir l'explitacion de l'erreur
class SPFIncompatibleType(SPFException):
    def __init__(self, variable, type1, type2, line_error):
        super().__init__(f"SPFIncompatibleType : la variable '{variable}' à la ligne {line_error} possède un type {type1}, ce qui est incompatible avec le type {type2} !")

#todo revoir l'explitacion de l'erreur ( indice entre 1 et n)
class SPFIndexError(SPFException):
    def __init__(self, line_error, position):
        super().__init__(f"SPFIndexError : La position {position} que vous utilisez à la ligne {line_error} n'existe pas !")

