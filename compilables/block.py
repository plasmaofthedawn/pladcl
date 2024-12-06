from .compilable import Compilable, register_class, join_compilables

class Block(Compilable):
    def __init__(self):
        self.name = "invalid"
        self.type = "invalid"
        self.lines = []

    @classmethod
    def from_tree(cls, tree):
        
        block = cls()
        block.tree = tree

        parsed = cls.parse_tree(tree)

        if 'STATE' in parsed:
            block.type = "state"
        elif 'FUNCTION' in parsed:
            block.type = "function"
        elif 'INTERRUPT' in parsed:
            block.type = "interrupt"

        block.name = parsed['IDENTIFIER'][0].value
        block.lines = parsed['line']

        #from pprint import pprint
        #pprint(dict(parsed))

        return block

    def __str__(self):
        return self.type + " " + self.name + "\n--" + "\n--".join(str(x) for x in self.lines)

    def compile(self, globals):

        globals["loop_depth"] = 0

        if self.type == "function":
            globals["can_return"] = True
            globals["depth"] = 1
        elif self.type == "state":
            globals["can_return"] = True
            globals["depth"] = 1
        elif self.type == "interrupt":
            globals["can_return"] = False
            globals["depth"] = 0

        
        return join_compilables(self.lines, globals)

register_class(Block, "state_declaration")
register_class(Block, "function_declaration")
register_class(Block, "interrupt_declaration")


