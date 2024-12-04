from util import get_name, get_children, unwrap_singleton, get_line

class CompileError(Exception):
    pass

class Line:

    def __init__(self, Tree):
        raise NotImplementedError

    def compile(self, globals):
        raise NotImplementedError

class Parameter:
    def __init__(self, tree):
        raise NotImplementedError

    def compile(self, globals):
        raise NotImplementedError

class Expression:

    value = None
    def __init__(self, tree):
        raise NotImplementedError

class DcLiteral(Line, Parameter, Expression):
    def __init__(self, tree):
        self.value = tree.getText()[1: -1]

    def compile(self, globals):
        return self.value

    def __str__(self):
        return '`' + self.value + '`'

class IntegerLiteral(Parameter):
    def __init__(self, tree):
        self.value = int(tree.getText())

    def __str__(self):
        return str(self.value)

    def compile(self, _):
        return str(self.value) if self.value > 0 else "_" + str(-self.value)

class StringLiteral(Parameter):
    def __init__(self, tree):
        self.value = tree.getText()[1: -1]

    def __str__(self):
        return '"' + self.value + '"'

class Identifier(Parameter):
    def __init__(self, tree):
        self.value = tree.getText()

    def __str__(self):
        return self.value

class FunctionCall(Line, Expression):
    def __init__(self, tree):
        self.name = "invalid"
        self.parameters = []
        self.node = tree
        
        for i in get_children(tree):

            if get_name(i) == "IDENTIFIER":
                self.name = i.getText()

            elif get_name(i) == "parameter_list":

                for p in get_children(i):

                    self.parameters.append(unwrap_literal(p))

    def add_parameter(self, param):
        self.parameters.append(param)

    def __str__(self):
        return self.name + "(" + ", ".join([str(x) for x in self.parameters]) + ")"

    def compile(self, globals):

        if self.name in globals['globalfunc']:

            try:
                return globals['globalfunc'][self.name].compile(self.parameters, globals)
            except CompileError as e:
                raise CompileError(f"{str(e)} in function {self.name} on line {get_line(self.node)}")

        if self.name in globals['localfuncid']:
            return f"{str(globals['localfuncid'][self.name])};Fx"

        raise CompileError(f"Unknown function {self.name} on line {get_line(self.node)}")


class Predicate:

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

    def __init__(self, tree):

        self.arg_1 = None
        self.arg_2 = None
        self.comparison = None
        self.lines = None
        
        for i in get_children(tree):

            if get_name(i) == "expression":

                e = unwrap_singleton(i)
                e = expression_types[get_name(e)](e)

                if self.arg_1 is None:
                    self.arg_1 = e
                else:
                    self.arg_2 = e

            elif get_name(i) == "COMPARISONS":
                self.comparison = i.getText()

    def compile(self, globals):

        if self.comparison not in self.COMPARISON_INVERSE_MAP:
            raise CompileError(f"Unknown comparison {self.comparison}. This should have been caught by antlr what")

        compiled_1 = self.arg_1.compile(globals)
        compiled_2 = self.arg_2.compile(globals)

        # put a guard if needed
        if compiled_1.isdigit() and compiled_2[0].isdigit():
            compiled_1 += " "

        return f"{compiled_1}{compiled_2}{self.COMPARISON_INVERSE_MAP[self.comparison]}q"

class If(Line):
    
    def __init__(self, tree):
        self.predicate = None
        self.lines = []

        for i in get_children(tree):

            if get_name(i) == "predicate":
                self.predicate = Predicate(i)

            if get_name(i) == "line":
                self.lines.append(unwrap_line(i))

    def compile(self, globals):

        return f"[{self.predicate.compile(globals)}{"".join(x.compile(globals) for x in self.lines)}]x"
                

class EmptyLine(Line):

    def __init__(self, Tree):
        pass

    def compile(self, globals):
        return ""



line_types = {
    "DC_LITERAL": DcLiteral,
    "function": FunctionCall,
    "if_line": If,
    "empty_line": EmptyLine,
}

expression_types = {
    "DC_LITERAL": DcLiteral,
    "function": FunctionCall,
    "INTEGER_LITERAL": IntegerLiteral,
}

literal_types = {
    "DC_LITERAL": DcLiteral,
    "INTEGER_LITERAL": IntegerLiteral,
    "STRING_LITERAL": StringLiteral,
    "IDENTIFIER": Identifier,
}

def unwrap_line(tree):
    line = unwrap_singleton(tree)
    return line_types[get_name(line)](line)
    
def unwrap_expression(tree):
    exp = unwrap_singleton(tree)
    return expression_types[get_name(exp)](exp)

def unwrap_literal(tree):
    lit = unwrap_singleton(tree)
    return literal_types[get_name(lit)](lit)

