
NumLabError = type('NumLabError', (Exception,), {})

CompilationError = type('CompilationError', (Exception))

Tokenizer = type('Tokenizer',CompilationError)

class ParserError (CompilationError):

  def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

