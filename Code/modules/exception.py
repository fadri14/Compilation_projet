class SPFException(Exception):
    def __init__(self, error):
        self.error = error

class SPFSyntaxError(SPFException):
    def __init__(self, error):
        self.error = error

class SPFUninitializedVariable(SPFException):
    def __init__(self, error):
        self.error = error

#new SPFUnknownVariable
class SPFUnknownVariable(SPFException):
    def __init__(self, variable, line):
        self.variable = variable
        self.line = line
        self.updateError()
    
    def updateError(self):
        error = f"SPFUnknownVariable : la variable '{self.variable}' à la ligne {self.line} n'est pas déclarée !"
        super().__init__(error)

#new SPFAlreadyDefined
class SPFAlreadyDefined(SPFException):
    def __init__(self, variable, line1, line2):
        self.variable = variable
        self.line1 = line1
        self.line2 = line2 #traceback
        self.updateError()

    def updateError(self):
        error = f"SPFAlreadyDefined : la variable '{self.variable}' à la ligne {self.line1} a déjà été déclarée à la ligne {self.line2} !"
        super().__init__(error)

#new SPFIncompatibleType
#A retester, encore une erreur voir la méthode calcul de backend.
class SPFIncompatibleType(SPFException):
    def __init__(self, variable, type1, type2, line):
        self.variable = variable
        self.type1 = type1
        self.type2 = type2
        self.line = line
        self.updateError()

    def updateError(self):
        error = f"SPFIncompatibleType : la variable '{self.variable}' à la ligne {self.line} possède un type {self.type1}, ce qui est incompatible avec le type {self.type2} !"
        super().__init__(error)

#new SPFIndexError
class SPFIndexError(SPFException):
    def __init__(self, variable, line, position):
        self.variable = variable
        self.line = line
        self.position = position
        self.updateError()
    
    def updateError(self):
        error = f"SPFIndexError : La position {self.position} que vous utilisez sur la variable '{self.variable}' à la ligne {self.line} n'existe pas !"
        super().__init__(error)

