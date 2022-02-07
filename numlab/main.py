import json
import logging

import typer

import numlab
from numlab.compiler import Grammar, LR1Parser, ParserManager
from numlab.lang.context import Context
from numlab.nl_builders import builders
from numlab.nl_tokenizer import tknz
from numlab.optimization.optimizer import CodeOptimizer
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
    max_iter: int = typer.Option(
        5, "--max-iter", "-i", help="Maximum number of iterations"
    ),
    pop_size: int = typer.Option(10, "--pop-size", "-p", help="Population size"),
    mutation_prob: float = typer.Option(
        0.1, "--mutation-prob", "-m", help="Mutation probability"
    ),
    best_sel_count: int = typer.Option(
        3, "--best-sel-count", "-b", help="Number of best individuals to select"
    ),
    new_random_count: int = typer.Option(
        2, "--new-random-count", "-r", help="Number of new random individuals"
    ),
    config_file: str = typer.Option(
        None, "--config", "-c", help="Configuration file (JSON)"
    ),
):
    """
    Optimize a program given in the input file
    """

    if config_file is not None:
        if not config_file.endswith(".json"):
            raise typer.Exit(
                "Configuration file must be a JSON file. Got " + config_file
            )
        with open(config_file, "r") as conf_fd:
            config = json.load(conf_fd)
    else:
        config = {}

    pop_size = config["pop_size"] = config.get("pop_size", pop_size)
    max_iter = config["max_iter"] = config.get("max_iter", max_iter)
    mutation_prob = config["mutation_prob"] = config.get("mutation_prob", mutation_prob)
    best_sel_count = config["best_sel_count"] = config.get(
        "best_sel_count", best_sel_count
    )
    new_random_count = config["new_random_count"] = config.get(
        "new_random_count", new_random_count
    )

    # Validate parameters
    if not 0 <= mutation_prob <= 1:
        raise typer.Exit(
            f"Mutation probability must be between 0 and 1. Got {mutation_prob}"
        )

    if max_iter <= 0:
        raise typer.Exit(
            f"Maximum number of iterations must be greater than 0. Got {max_iter}"
        )

    if pop_size <= 0:
        raise typer.Exit(f"Population size must be greater than 0. Got {pop_size}")

    if not 0 <= best_sel_count <= pop_size:
        raise typer.Exit(
            "Number of best individuals to select must be between 0 and"
            f" population size. Got {best_sel_count}"
        )

    if not 0 <= new_random_count <= pop_size:
        raise typer.Exit(
            "Number of new random individuals must be between 0 and "
            f"population size. Got {new_random_count}"
        )

    if best_sel_count + new_random_count > pop_size:
        raise typer.Exit(
            "Number of best individuals to select and number of new random "
            "individuals must be less than population size. Got "
            f"{best_sel_count} and {new_random_count}"
        )

    max_lenght = max([len(str(item)) for item in config.values()]) + 2
    total_length = 42 + max_lenght

    typer.echo("\n")
    typer.echo(f" .{'=' * total_length}.")
    typer.echo(f" |{'Configuration':^{total_length}}|")
    typer.echo(f" |{'=' * total_length}|")
    typer.echo(f" | {'Parameter':<40}{'Value':>{max_lenght}} |")
    typer.echo(f" |{'-'*40:<40}--{'-'*max_lenght:>{max_lenght}}|")
    typer.echo(f" | {'Population size':<40}{pop_size:>{max_lenght}} |")
    typer.echo(f" | {'Maximum number of iterations':<40}{max_iter:>{max_lenght}} |")
    typer.echo(f" | {'Mutation probability':<40}{mutation_prob:>{max_lenght}} |")
    typer.echo(
        f" | {'Number of best individuals to select':<40}{best_sel_count:>{max_lenght}} |"
    )
    typer.echo(
        f" | {'Number of new random individuals':<40}{new_random_count:>{max_lenght}} |"
    )
    typer.echo(f" '{'=' * total_length}'")
    typer.echo("\n")

    program = get_ast(input_file)
    opt = OptVisitor()
    opt.check(program)
    changes = opt.changes
    if changes:
        opt_quality = opt.classifier.classify_optimization_quality()
        typer.echo(f"Estimated optimization quality: {opt_quality}")
        if not typer.confirm(
            "\nDo you want to proceed with the optimization?", default=True
        ):
            raise typer.Exit("Optimization aborted")
        if dump:
            program.dump()
        typer.echo("Output (before optimizing):")
        evaluator = EvalVisitor(Context())
        evaluator.eval(program)
        typer.echo("\nOptimizing program")
        optimizer = CodeOptimizer(
            program,
            changes,
            max_iter=max_iter,
            minimize=True,
            population_size=pop_size,
            mutation_prob=mutation_prob,
            best_selection_count=best_sel_count,
            generate_new_randoms=new_random_count,
        )
        optimizer.run()
        if dump:
            program.dump()
        typer.echo("\nOutput (after optimizing):")
        evaluator = EvalVisitor(Context())
        evaluator.eval(program)
    else:
        typer.echo("No changes were found for possible optimizations")


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
