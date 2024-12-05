from util import get_name, get_children, unwrap_singleton, get_line

class CompileError(Exception):
    pass

class Line:

    def __init__(self, tree):
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
        return str(self.value) if self.value >= 0 else "_" + str(-self.value)

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


def gen_quit_command(length: int):
    # bug in dc makes depth of 1 not work for some reason
    if length == 1:
        return f"lqx"
    elif length == 2:
        return f"q"
    else:
        return f"{length}Q"

class Break:
    def __init__(self, tree):
        self.tree = tree

    def compile(self, globals):

        if globals["loop_depth"] < 1:
            raise CompileError(f"break outside of loop on line {get_line(self.tree)}")

        # fix loop stack
        out = "LLst"
        out += gen_quit_command(globals["depth"] - globals["cur_loop_depth"] + 1)

        return out


class Return:
    def __init__(self, tree):
        self.tree = tree
        self.retvalue = None

        for i in get_children(tree):
            if get_name(i) == "expression":
                self.retvalue = unwrap_expression(i)


    def compile(self, globals):
        if not globals["can_return"]:
            raise CompileError(f"cannot return on line {get_line(self.tree)}")


        if globals["depth"] <= 0:
            raise CompileError(f"return at depth {globals["depth"]} on line {get_line(self.tree)}. this is an issue with the compiler")
        
        # fix loop stack
        out = "LLst" * globals["loop_depth"]
        out += gen_quit_command(globals["loop_depth"])

                
        if self.retvalue:
            return join_compilables([self.retvalue, out], globals)
        else:
            return out

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


        return f"{join_compilables((self.arg_2, self.arg_1), globals)}{self.COMPARISON_INVERSE_MAP[self.comparison]}q"

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

        globals = globals.copy()
        globals["depth"] += 1

        return f"[{self.predicate.compile(globals)}{join_compilables(self.lines, globals)}]x"

class While(Line):

    def __init__(self, tree):
        self.predicate = None
        self.lines = []

        for i in get_children(tree):

            if get_name(i) == "predicate":
                self.predicate = Predicate(i)

            if get_name(i) == "line":
                self.lines.append(unwrap_line(i))

    def compile(self, globals):
        globals = globals.copy()
        globals["depth"] += 1
        globals["loop_depth"] += 1
        globals["cur_loop_depth"] = globals["depth"]

        return f"[{self.predicate.compile(globals)}SL{join_compilables(self.lines, globals)}LLdx]dx"

        

class EmptyLine(Line):

    def __init__(self, tree):
        pass
        
    def compile(self, globals):
        return ""



line_types = {
    "DC_LITERAL": DcLiteral,
    "function": FunctionCall,
    "if_line": If,
    "empty_line": EmptyLine,
    "return_line": Return,
    "INTEGER_LITERAL": IntegerLiteral,
    "while_line": While,
    "BREAK": Break,
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

# all this for like. 1 space
def needs_escaped(command):

    # if it is a digit this could be bad
    if command.isdigit():
        return True

    # if the last thing is a digit and it's not being used as a register yikes
    if len(command) > 1 and command[-1].isdigit() and command[-2] not in "slSL><=;:":
        return True

    return False

def join_compilables(commands, globals):

    if len(commands) == 0:
        return ""

    out = ""
    c1 = commands[0] if type(commands[0]) is str else commands[0].compile(globals) 
    for command, next_command in zip(commands, commands[1:]):

        #c1 = command.compile(globals)
        c2 = next_command if isinstance(next_command, str) else next_command.compile(globals)

        if needs_escaped(c1) and c2[0].isdigit():
            c1 += " "

        out += c1

        c1 = c2

    out += c1
    return out

