from typing import List

from numlab.compiler import Token, Tokenizer

tknz = Tokenizer()
tknz.add_pattern("NEWLINE", r"\n")
tknz.add_pattern("SPACE", r"( |\t)( |\t)*", lambda l: None)

tknz.add_pattern("COMMENT", r"#.*\n", lambda t: None)

# Augassing
tknz.add_pattern("+=", r"+=")
tknz.add_pattern("-=", r"-=")
tknz.add_pattern("*=", r"\*=")
tknz.add_pattern("@=", r"@=")
tknz.add_pattern("/=", r"/=")
tknz.add_pattern("%=", r"%=")
tknz.add_pattern("&=", r"&=")
tknz.add_pattern("|=", r"\|=")
tknz.add_pattern("^=", r"\^=")
tknz.add_pattern("<<=", r"<<=")
tknz.add_pattern(">>=", r">>=")
tknz.add_pattern("**=", r"\*\*=")
tknz.add_pattern("//=", r"//=")

# Operators
tknz.add_pattern("==", r"==")
tknz.add_pattern(">=", r">=")
tknz.add_pattern("<=", r"<=")
tknz.add_pattern("!=", r"!=")
tknz.add_pattern("**", r"\*\*")
tknz.add_pattern("<<", r"<<")
tknz.add_pattern(">>", r">>")
tknz.add_pattern("*", r"\*")
tknz.add_pattern("=", r"=")
tknz.add_pattern("|", r"\|")
tknz.add_pattern("^", r"\^")
tknz.add_pattern("&", r"&")
tknz.add_pattern("+", r"+")
tknz.add_pattern("-", r"-")
tknz.add_pattern("@", r"@")
tknz.add_pattern("/", r"/")
tknz.add_pattern("%", r"%")
tknz.add_pattern("//", r"//")
tknz.add_pattern("~", r"~")
tknz.add_pattern("<", r"<")
tknz.add_pattern(">", r">")

# Punctuation
tknz.add_pattern("(", r"\(")
tknz.add_pattern(")", r"\)")
tknz.add_pattern("{", r"{")
tknz.add_pattern("}", r"}")
tknz.add_pattern("[", r"[")
tknz.add_pattern("]", r"]")
tknz.add_pattern(";", r";")
tknz.add_pattern(",", r",")
tknz.add_pattern(".", r"\.")
tknz.add_pattern(":", r":")


# Keywords
tknz.add_keywords(
    "True",
    "False",
    "None",
    "and",
    "or",
    "not",
    "if",
    "else",
    "elif",
    "while",
    "for",
    "in",
    "break",
    "continue",
    "return",
    "def",
    "class",
    "try",
    "except",
    "finally",
    "raise",
    "import",
    "from",
    "as",
    "is",
    "del",
    "pass",
    "yield",
    "assert",
    "with",
    "global",
    "nonlocal",
    "lambda",
    "conf",
    "begsim",
    "endsim",
    "resetstats",
)

# Special terminals
tknz.add_pattern("NAME", r"(\a|\A|_)(\a|\A|\d|_)*")
tknz.add_pattern("NUMBER", r"\d\d*|\d\d*\.\d\d*")
tknz.add_pattern(
    "STRING", r"'((^')|(\\'))*(^\\)'|\"((^\")|(\\\"))*(^\\)\"", lambda t: t[1:-1]
)


@tknz.process_tokens
def process_tokens(tokens: List[Token]):
    indent_tok = Token("INDENT", "INDENT")
    dedent_tok = Token("DEDENT", "DEDENT")
    indentations = [0]
    new_tokens = []
    check_indent = 0
    for tok in tokens:
        if tok.NEWLINE and check_indent == 0:
            check_indent = 1
        if not tok.NEWLINE and check_indent == 1:
            check_indent = 2
        if check_indent == 2:
            new_indentation_size = tok.col
            while new_indentation_size < indentations[-1]:
                new_tokens.append(dedent_tok)
                indentations.pop()
            if new_indentation_size > indentations[-1]:
                indentations.append(new_indentation_size)
                new_tokens.append(indent_tok)
            check_indent = 0
        if not tok.NEWLINE or (new_tokens and not new_tokens[-1].NEWLINE):
            new_tokens.append(tok)

    if len(indentations) > 1:
        for _ in range(len(indentations) - 1):
            new_tokens.append(dedent_tok)

    new_tokens.append(Token("NEWLINE", "\n"))
    return new_tokens
