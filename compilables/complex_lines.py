from .compilable import Compilable, register_class, join_compilables
from .expressions import Predicate

class If(Compilable):
    
    predicate: Predicate
    
    def __init__(self):
        self.lines = []


    @classmethod
    def from_tree(cls, tree):
        c = super().from_tree(tree)

        parse = cls.parse_tree(tree)

        c.predicate = parse["predicate"][0]
        c.lines = parse["line"]

        return c

    def compile(self, globals):

        globals = globals.copy()
        globals["depth"] += 1

        return f"[{self.predicate.r_compile(globals)}q{join_compilables(self.lines, globals)}]x"

register_class(If, "if_line")

class While(Compilable):

    predicate: Predicate

    def __init__(self):
        self.lines = []

    @classmethod
    def from_tree(cls, tree):
        c = super().from_tree(tree)

        parse = cls.parse_tree(tree)

        c.predicate = parse["predicate"][0]
        c.lines = parse["line"]

        return c


    def compile(self, globals):
        globals = globals.copy()
        globals["depth"] += 1
        globals["loop_depth"] += 1
        globals["cur_loop_depth"] = globals["depth"]

        return f"[{self.predicate.r_compile(globals)}qSL{join_compilables(self.lines, globals)}LLdx]dxst"

register_class(While, "while_line")
