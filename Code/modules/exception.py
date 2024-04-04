class SPFException(Exception):
    def __init__(self, error):
        self.error = error

class SPFSyntaxError(SPFException):
    def __init__(self, error):
        self.error = error

#new SPFUnknownVariable
class SPFUnknownVariable(SPFException):
    def __init__(self, variable, line):
        self.variable = variable
        self.line = line
        self.updateError()
    
    def updateError(self):
        error = f"SPFUnknownVariable : la variable  '{self.variable}' à la ligne {self.line} n'est pas déclarée !"
        super().__init__(error)

class SPFUninitializedVariable(SPFException):
    def __init__(self, error):
        self.error = error

class SPFAlreadyDefined(SPFException):
    def __init__(self, error):
        self.error = error

class SPFIncompatibleType(SPFException):
    def __init__(self, error):
        self.error = error

class SPFIndexError(SPFException):
    def __init__(self, error):
        self.error = error

