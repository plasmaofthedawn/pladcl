from .compilable import Compilable, register_class, join_compilables
from .expressions import Predicate
from .literals import IntegerLiteral, DcLiteral, CharLiteral

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


class ForIn(Compilable):

    var: CharLiteral

    start: Compilable
    end: Compilable
    step: Compilable

    lines: list[Compilable]


    def __init__(self):
        self.step = IntegerLiteral()
        self.step.value = 1

    @classmethod
    def from_tree(cls, tree):
        c = super().from_tree(tree)

        parse = cls.parse_tree(tree)

        c.lines = parse["line"]

        c.var = parse["CHAR_LITERAL"][0]

        c.start = parse["expression"][0]
        c.end = parse["expression"][1]

        if "STEP" in parse:
            c.step = parse["expression"][2]

        return c

    def compile(self, globals):
        
        # first load line
        set_line = DcLiteral.from_kwargs(value=self.start.compile(globals) + "s" + self.var.value)

        # predicate
        pred = Predicate.from_kwargs(
            arg_1 = DcLiteral.from_kwargs(value="l" + self.var.value),
            arg_2 = self.end,
            comparison = "!=",
        )

        # loop
        loop = While.from_kwargs(
            lines = self.lines,
            predicate = pred,
        )

        # inc line
        loop.lines.extend([
                DcLiteral.from_kwargs(value=f"l{self.var.value}"),
                self.step,
                DcLiteral.from_kwargs(value=f"+s{self.var.value}"),
        ])

        return join_compilables([set_line, loop], globals)


register_class(ForIn, "for_in_line")


class ForStack(Compilable):

    var: CharLiteral
    stack: CharLiteral

    lines: list[Compilable]

    @classmethod
    def from_tree(cls, tree):
        c = super().from_tree(tree)

        parse = cls.parse_tree(tree)

        c.var = parse["CHAR_LITERAL"][0]
        c.stack = parse["CHAR_LITERAL"][1]

        c.lines = parse["line"]

        return c

    def compile(self, globals: dict) -> str:
        
        loop = While.from_kwargs(
            lines = self.lines,
            predicate = Predicate.from_kwargs(
                arg_1 = DcLiteral.from_kwargs(value=f"L{self.stack.value}ds{self.var.value}"),
                arg_2 = IntegerLiteral.from_kwargs(value=-1),
                comparison = "!="
            )
        )

        # to put back on the end of stack thing if we popped it off
        if_eos = If.from_kwargs(
            lines = [DcLiteral.from_kwargs(value=f"_1S1")],
            predicate = Predicate.from_kwargs(
                arg_1 = DcLiteral.from_kwargs(value="l" + self.var.value),
                arg_2 = IntegerLiteral.from_kwargs(value=-1),
                comparison = "=="
            )
        )

        return join_compilables([loop, if_eos], globals)

register_class(ForStack, "for_stack_line")
