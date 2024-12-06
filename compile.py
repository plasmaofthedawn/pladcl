import antlr4
from antlr.PladclParser import PladclParser
from antlr.PladclLexer import PladclLexer
import sys
import argparse

from util import get_name, get_children, unwrap_singleton

from program import *

filename = "input.pdl"


def parse_program(program, **kwargs):
    global rule_names, token_names

    char_stream = antlr4.InputStream(program)
    #char_stream = antlr4.FileStream(filename, encoding='utf-8')

    lexer = PladclLexer(char_stream)
    stream = antlr4.CommonTokenStream(lexer)
    parser = PladclParser(stream)
    tree = parser.program()

    if parser._syntaxErrors > 0:
        return

    program = Program.from_tree(tree)
    
    """
    for b in get_children(tree):

        if get_name(b) in ["empty_line"]:
            continue

        # for each block
        block = Block.from_tree(b)
        
        program.add_block(block)
    """

    try:
        return program.compile(**kwargs)
    except CompileError as e:
        sys.stderr.write("Compile error: " + str(e) + "\n")
        quit(1)

if __name__ == "__main__":

    parser = argparse.ArgumentParser("pladclc")
    parser.add_argument("-d", "--debug", help="debug flag", action='store_true')
    parser.add_argument("file", help="file to be compiled", type=argparse.FileType('r'),
                        default=sys.stdin)
    parser.add_argument("-p", "--progress", type=int, default=None,
                        help="show a progress bar while running\nhow many chars to show a dot")
    parser.add_argument("-o", "--output", type=argparse.FileType('w'), default=sys.stdout,
                        help="file to output, default is stdout")

    args = parser.parse_args(sys.argv[1:])

    progress = args.progress
    debug = args.debug
    
    if (compiled := parse_program(args.file.read(), debug=debug, progress=progress)):
        
        args.output.write(compiled)
        args.output.close()
