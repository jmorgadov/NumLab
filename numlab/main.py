import logging
import sys

from numlab.compiler import Grammar, LR1Parser, ParserManager
from numlab.lang.context import Context
from numlab.nl_builders import builders
from numlab.nl_tokenizer import tknz
from numlab.visitors.eval_visitor import EvalVisitor
from numlab.visitors.opt_visitor import OptVisitor
from numlab.nl_optimizer import CodeOptimizer

# Set logging level to DEBUG
# logging.basicConfig(level=logging.DEBUG)

def main():
    if len(sys.argv) < 2:
        raise Exception("Missing script file")
    file_path = sys.argv[1]

    run_logger = logging.getLogger('run')
    run_logger.setLevel(logging.INFO)

    # Load grammar
    run_logger.info('Loading grammar')
    gm = Grammar.open("numlab/nl_grammar.gm")
    run_logger.info('Assigning builders')
    gm.assign_builders(builders)

    # Create LR1Parser
    run_logger.info('Loading parser table')
    parser = LR1Parser(gm, "numlab/nl_lr1_table")

    # Create parser
    parser_man = ParserManager(gm, tknz, parser)

    # Parse file
    run_logger.info("Parsing script")
    program = parser_man.parse_file(file_path)
    if "-d" in sys.argv:
        program.dump()


    if "-o" in sys.argv:
        run_logger.info("Output (with out optimizing):")
        evaluator = EvalVisitor(Context())
        evaluator.eval(program)
        opt = OptVisitor()
        opt.check(program)
        changes = opt.changes
        program.dump()
        if changes:
            run_logger.info("Optimizing program")
            optimizer = CodeOptimizer(program, changes)
            optimizer.run()
            program.dump()
            run_logger.info("Output (with optimizing):")
            evaluator = EvalVisitor(Context())
            evaluator.eval(program)
        return


    # Evaluate
    run_logger.info("Executing. Output:")
    evaluator = EvalVisitor(Context())
    evaluator.eval(program)


if __name__ == "__main__":
    main()
