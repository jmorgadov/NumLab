import logging
import sys
import typer

from numlab.compiler import Grammar, LR1Parser, ParserManager
from numlab.lang.context import Context
from numlab.nl_builders import builders
from numlab.nl_tokenizer import tknz
from numlab.visitors.eval_visitor import EvalVisitor
from numlab.visitors.opt_visitor import OptVisitor
from numlab.nl_optimizer import CodeOptimizer

# Set logging level to DEBUG
# logging.basicConfig(level=logging.DEBUG)

app = typer.Typer(add_completion=False)

@app.command()
def main(file_path: str,
         optmize: bool = typer.Options(
             False, "--optimize", "-o"
         ),
         dump: bool = typer.Options(
             False, "--dump", "-d"
         )):

    # Load grammar
    typer.echo('Loading grammar')
    gm = Grammar.open("numlab/nl_grammar.gm")
    typer.echo('Assigning builders')
    gm.assign_builders(builders)

    # Create LR1Parser
    typer.echo('Loading parser table')
    parser = LR1Parser(gm, "numlab/nl_lr1_table")

    # Create parser
    parser_man = ParserManager(gm, tknz, parser)

    # Parse file
    typer.echo("Parsing script")
    program = parser_man.parse_file(file_path)
    
    if dump:
        program.dump()


    if optmize:
        typer.echo("Output (with out optimizing):")
        evaluator = EvalVisitor(Context())
        evaluator.eval(program)
        opt = OptVisitor()
        opt.check(program)
        changes = opt.changes
        program.dump()
        if changes:
            typer.echo("Optimizing program")
            optimizer = CodeOptimizer(program, changes)
            optimizer.run()
            program.dump()
            typer.echo("Output (with optimizing):")
            evaluator = EvalVisitor(Context())
            evaluator.eval(program)
        return


    # Evaluate
    typer.echo("Executing. Output:")
    evaluator = EvalVisitor(Context())
    evaluator.eval(program)


if __name__ == "__main__":
    app()
