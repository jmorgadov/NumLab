"""
This module contains the exceptions used on the project.
"""

class NumlabError(Exception):
    
    def __init__(self, message):
        super.__init__(message)
        self.message = message

    def __str__(self) -> str:
        return super().__str__()


class TokenError(NumlabError):
    def __init__(self, message, token: str):
        super.__init__(message)
        self.message = message
        self.token = token
    
    def __str__(self) -> str:
        return "Invalid token: {}\n{}".format(self.message, self.token)


class ParsingError(NumlabError):
    """
    This class represents an error that occurs during the parsing of a
    program.
    """
    def __init__(self, message, token):

        super().__init__(message)
        self.message = message
        self.token = token
        self.line = token.line
        self.column = token.col

    def __str__(self):
        return "Parsing error: {} at line {} column {}\n{}".format(
            self.message, self.line, self.column, self.token)


class RuntimeError(NumlabError):
    def __init__(self, message):
        super.__init__(message)
        self.message = message
    
    def __str__(self) -> str:
        return "Runtime Error: {}".format(self.message)


class ValueError(RuntimeError):
    def __init__(self, message):
        super.__init__(message)
        self.message = message
    
    def __str__(self) -> str:
        return "Value Error: {}".format(self.message)


class InvalidTypeError(RuntimeError):
    def __init__(self, message):
        super.__init__(message)
        self.message = message
    
    def __str__(self) -> str:
        return "Invalid Type Error: {}".format(self.message)


class InvalidConfigError(RuntimeError):
    def __init__(self, message):
        super.__init__(message)
        self.message = message
    
    def __str__(self) -> str:
        return "Invalid Configuration Options: {}".format(self.message)


class SimulationError(RuntimeError):
    def __init__(self, message):
        super.__init__(message)
        self.message = message
    
    def __str__(self) -> str:
        return "Simulation Error: {}".format(self.message)








