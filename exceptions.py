"""
This module contains the exceptions used on the project.
"""


NumLabError = type("NumLabError", (Exception,), {})

CompilationError = type("CompilationError", (NumLabError,), {})

TokenizationError = type("TokenizationError", (CompilationError,), {})

ParsingError = type("ParsingError", (CompilationError,), {})
