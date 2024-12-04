from util import get_name, get_children, unwrap_singleton, get_line

class CompileError(Exception):
    pass

class Line:

    def __init__(self, Tree):
        raise NotImplementedError

    def compile(self, globals):
        raise NotImplementedError

    pass

class Parameter:
    def __init__(self, tree):
        pass

class DcLiteral(Line, Parameter):
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

class FunctionCall(Line):
    def __init__(self, tree):
        self.name = "invalid"
        self.parameters = []
        self.node = tree
        
        for i in get_children(tree):

            if get_name(i) == "IDENTIFIER":
                self.name = i.getText()

            elif get_name(i) == "parameter_list":

                for p in get_children(i):

                    param = unwrap_singleton(p)

                    self.parameters.append(
                            literal_types[get_name(param)](param)
                    )


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


line_types = {
    "DC_LITERAL": DcLiteral,
    "function": FunctionCall,
}

literal_types = {
    "DC_LITERAL": DcLiteral,
    "INTEGER_LITERAL": IntegerLiteral,
    "STRING_LITERAL": StringLiteral,
    "IDENTIFIER": Identifier,
}
