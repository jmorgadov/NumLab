"""
This module contains the exceptions used on the project.
"""


NumLabError = type("NumLabError", (Exception,), {})

CompilationError = type("CompilationError", (NumLabError,), {})

TokenizationError = type("TokenizationError", (CompilationError,), {})

class ParsingError(CompilationError):
    """
    This class represents an error that occurs during the parsing of a
    program.
    """
    def __init__(self, message, line, column):
        super().__init__(message)
        self.message = message
        self.line = line
        self.column = column

    def __str__(self):
        return "Parsing error: {} at line {} column {}".format(
            self.message, self.line, self.column)
