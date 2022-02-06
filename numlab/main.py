import logging

import typer

import numlab
from numlab.compiler import Grammar, LR1Parser, ParserManager
from numlab.lang.context import Context
from numlab.nl_builders import builders
from numlab.nl_optimizer import CodeOptimizer
from numlab.nl_tokenizer import tknz
from numlab.visitors.eval_visitor import EvalVisitor
from numlab.visitors.opt_visitor import OptVisitor

# Set logging level to DEBUG
# logging.basicConfig(level=logging.DEBUG)

app = typer.Typer(add_completion=False)


def echo(msg, verbose):
    if verbose:
        typer.echo(msg)


def get_ast(file_path: str, verbose: bool = False):
    # Load grammar
    echo("Loading grammar", verbose)
    grammar = Grammar.open("numlab/nl_grammar.gm")
    echo("Assigning builders", verbose)
    grammar.assign_builders(builders)

    # Create LR1Parser
    echo("Loading parser table", verbose)
    parser = LR1Parser(grammar, "numlab/nl_lr1_table")

    # Create parser
    parser_man = ParserManager(grammar, tknz, parser)

    # Parse file
    echo("Parsing script", verbose)
    program = parser_man.parse_file(file_path)
    return program


@app.command("optimize")
def optimize(
    input_file: str = typer.Argument(..., help="Input file"),
    dump: bool = typer.Option(False, "--dump", "-d", help="Dump AST"),
):
    """
    Optimize a program given in the input file
    """
    program = get_ast(input_file)
    typer.echo("Output (before optimizing):")
    evaluator = EvalVisitor(Context())
    evaluator.eval(program)
    opt = OptVisitor()
    opt.check(program)
    changes = opt.changes
    if dump:
        program.dump()
    if changes:
        typer.echo("Optimizing program")
        optimizer = CodeOptimizer(program, changes)
        optimizer.run()
        program.dump()
        typer.echo("Output (after optimizing):")
        evaluator = EvalVisitor(Context())
        evaluator.eval(program)


@app.command("run")
def run(
    input_path: str = typer.Argument(..., help="Input file"),
    dump: bool = typer.Option(False, "--dump", "-d", help="Dump AST"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose mode"),
):
    """Run the program given in the input file"""

    program = get_ast(input_path, verbose)
    if dump:
        program.dump()

    # Evaluate
    echo("Program output:", verbose)
    evaluator = EvalVisitor(Context())
    evaluator.eval(program)


@app.command("version", help="Print the version number")
def version():
    typer.echo(f"NumLab v{numlab.__version__}")


if __name__ == "__main__":
    app()
