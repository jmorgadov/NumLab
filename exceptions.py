
NumLabError = type('NumLabError', (Exception,), {})

CompilationError = type('CompilationError', (Exception,), {})

TokenizerError = type('Tokenizer', (CompilationError,), {})

ParserError = type('ParserError', (CompilationError,), {})
        

