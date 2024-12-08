from .compilable import Compilable, Expression, CompileError, Parameter, register_class, join_compilables

class Predicate(Compilable, Expression, Parameter):

    COMPARISON_INVERSE_MAP = {
            "==": "!=",
            "!=": "=",
            ">": "!>",
            ">=": "<",
            "<": "!<",
            "<=": ">",
            "!<": "<",
            "!>": ">",
    }

    COMPARISON_MAP = {
        "==": "=",
        "!=": "!=",
        ">": ">",
        ">=": "!<",
        "<": "<",
        "<=": "!>",
        "!<": "!<",
        "!>": "!>",
    }

    def __init__(self):

        self.arg_1 = None
        self.arg_2 = None
        self.comparison = None
        

    @classmethod
    def from_tree(cls, tree):
        c = super().from_tree(tree)

        parse = cls.parse_tree(tree)

        c.arg_1 = parse["expression"][0]
        c.arg_2 = parse["expression"][1]
        c.comparison = parse["COMPARISONS"][0].getText()

        return c

    def compile(self, globals):

        if self.comparison not in self.COMPARISON_MAP:
            self.error(f"Unknown comparison {self.comparison}. This should have been caught by antlr what")


        return f"{join_compilables((self.arg_2, self.arg_1), globals)}{self.COMPARISON_MAP[self.comparison]}"

    def r_compile(self, globals):

        if self.comparison not in self.COMPARISON_INVERSE_MAP:
            self.error(f"Unknown comparison {self.comparison}. This should have been caught by antlr what")


        return f"{join_compilables((self.arg_2, self.arg_1), globals)}{self.COMPARISON_INVERSE_MAP[self.comparison]}"

register_class(Predicate, "predicate")


class FunctionCall(Compilable, Expression, Parameter):
    def __init__(self):
        self.name = "invalid"
        self.parameters = []        
        
    @classmethod
    def from_tree(cls, tree):

        c = super().from_tree(tree) 

        parse = cls.parse_tree(tree)

        c.name = parse['IDENTIFIER'][0].value
        c.parameters = parse['parameter']

        return c

    def __str__(self):
        return self.name + "(" + ", ".join([str(x) for x in self.parameters]) + ")"

    def compile(self, globals):

        if self.name in globals['globalfunc']:

            try:
                return globals['globalfunc'][self.name].compile(self.parameters, globals)
            except CompileError as e:
                self.error(f"{str(e)} in function {self.name}")

        if self.name in globals['localfuncid']:
            return f"{str(globals['localfuncid'][self.name])};Fx"

        raise self.error(f"Unknown function {self.name}")

register_class(FunctionCall, "function")
