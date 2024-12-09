from .compilable import Compilable, Expression, CompileError, Parameter, register_class

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
