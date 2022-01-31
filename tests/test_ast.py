from numlab.compiler import Grammar, LR1Parser, ParserManager
from numlab.nl_builders import builders
from numlab.nl_tokenizer import tknz
from numlab.compiler.generic_ast import AST

import os

def test_ast():
    #Get current directory
    directory = os.getcwd()

    #Load scripts in folder
    astTests = os.listdir(directory + "\\tests\\astTests")

    #Load grammar files
    gm = Grammar.open("numlab/nl_grammar.gm")
    gm.assign_builders(builders)

    #Create LR1Parser
    parser = LR1Parser(gm, "numlab/nl_lr1_table")

    #Create parser
    parser_man = ParserManager(gm, tknz, parser)

    for t in astTests:
        try:
            program = parser_man.parse_file("tests/astTests/" + str(t))    
            assert isinstance(program, AST)
        except Exception as e:
            raise e