"""
This module contains the exceptions used on the project.
"""


class NumlabError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class TokenizationError(NumlabError):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


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
        return "{} at line {} column {}\n{}".format(
            self.message, self.line, self.column, self.token
        )


class RuntimeError(NumlabError):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class ValueError(RuntimeError):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class InvalidTypeError(RuntimeError):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class InvalidConfigError(RuntimeError):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class SimulationError(RuntimeError):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
