from antlr.PladclParser import PladclParser
from antlr4.tree.Tree import TerminalNodeImpl
from antlr4.tree.Trees import Trees

rule_names = PladclParser.ruleNames
token_names = PladclParser.symbolicNames
get_token_name = lambda x: token_names[x.getSymbol().type]
get_rule_name = lambda x: Trees.getNodeText(x, rule_names)
get_name = lambda x: get_token_name(x) if isinstance(x, TerminalNodeImpl) else get_rule_name(x)

ignore = ["WHITESPACE", "NEWLINE", "<INVALID>"]
ignore_pred = lambda x: get_name(x) not in ignore
get_children = lambda x: filter(ignore_pred, x.getChildren())

unwrap_singleton = lambda x: list(get_children(x))[0]

def get_line(x):

    while "getSymbol" not in dir(x):
        x = unwrap_singleton(x)

    return x.getSymbol().line

