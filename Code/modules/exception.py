class SPFException(Exception):
    def __init__(self, error):
        self.error = error

class SPFSyntaxError(SPFException):
    def __init__(self, error):
        self.error = error

class SPFUnknownVariable(SPFException):
    def __init__(self, error):
        self.error = error

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

