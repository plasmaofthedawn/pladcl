from .compilable import Compilable, register_class, join_compilables

"""
    Function calls are in expressions.py
"""
def gen_quit_command(length: int):
    # bug in dc makes depth of 1 not work for some reason
    if length == 1:
        return f"lqx"
    elif length == 2:
        return f"q"
    else:
        return f"{length}Q"

class Break(Compilable):

    def compile(self, globals):

        if globals["loop_depth"] < 1:
            self.error(f"break outside of loop")

        return join_compilables([
                "LLst",
                "0",
                gen_quit_command(globals["depth"] - globals["cur_loop_depth"] + 1),
        ], globals)


register_class(Break, "BREAK")

class Return(Compilable):
    def __init__(self):
        self.retvalue = None

    @classmethod
    def from_tree(cls, tree):
        c = super().from_tree(tree)

        parse = cls.parse_tree(tree)

        if "expression" in parse:
            c.retvalue = parse["expression"][0]

        return c


    def compile(self, globals):
        if not globals["can_return"]:
            self.error(f"cannot return here")


        if globals["depth"] <= 0:
            self.error(f"return at depth {globals["depth"]} (compiler issue) ")
        
        # fix loop stack
        out = "LLst" * globals["loop_depth"]
        out += gen_quit_command(globals["depth"])
                
        if self.retvalue:
            return join_compilables([self.retvalue, out], globals)
        else:
            return out

register_class(Return, "return_line")

class EmptyLine(Compilable):
        
    def compile(self, globals):
        return ""

register_class(EmptyLine, "empty_line")
