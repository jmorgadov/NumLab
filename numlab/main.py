import logging
import sys

from numlab.compiler import Grammar, LR1Parser, ParserManager
from numlab.lang.context import Context
from numlab.nl_builders import builders
from numlab.nl_tokenizer import tknz
from numlab.visitors.eval_visitor import EvalVisitor

# Set logging level to DEBUG
# logging.basicConfig(level=logging.DEBUG)


def main():
    # Load grammar
    gm = Grammar.open("numlab/nl_grammar.gm")
    gm.assign_builders(builders)

    # Create LR1Parser
    parser = LR1Parser(gm, "numlab/nl_lr1_table")

    # Create parser
    parser_man = ParserManager(gm, tknz, parser)

    # Parse file
    if len(sys.argv) < 2:
        raise Exception("Missing script file")

    file_path = sys.argv[1]
    program = parser_man.parse_file(file_path)

    # Evaluate
    evaluator = EvalVisitor(Context())
    evaluator.eval(program)


if __name__ == "__main__":
    main()
