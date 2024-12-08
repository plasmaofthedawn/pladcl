from .compilable import Compilable, Expression, Parameter, register_class

class DcLiteral(Compilable, Expression, Parameter):

    def __init__(self):
        self.value = ""

    @classmethod
    def from_tree(cls, tree):
        c = super().from_tree(tree)

        c.value = tree.getText().strip("`")

        return c

    def compile(self, globals):
        return self.value

    def __str__(self):
        return '`' + str(self.value) + '`'

register_class(DcLiteral, "DC_LITERAL")

class IntegerLiteral(Compilable, Expression, Parameter):
    def __init__(self):
        self.value = 0

    @classmethod
    def from_tree(cls, tree):
        c = super().from_tree(tree)

        c.value = int(tree.getText())

        return c

    def __str__(self):
        return str(self.value)

    def compile(self, globals):
        return str(self.value) if self.value >= 0 else "_" + str(-self.value)

register_class(IntegerLiteral, "INTEGER_LITERAL")

class StringLiteral(Compilable, Parameter):
    def __init__(self):
        self.value = ""

    @classmethod
    def from_tree(cls, tree):
        c = super().from_tree(tree)
        c.value = tree.getText().strip('"')
        return c

    def compile(self, globals: dict) -> str:
        return "[" + self.value + "]"

    def __str__(self):
        return '"' + self.value + '"'

register_class(StringLiteral, "STRING_LITERAL")

class CharLiteral(Compilable, Expression, Parameter):

    def __init__(self):
        self.value = ""

    @classmethod
    def from_tree(cls, tree):
        c = super().from_tree(tree)
        c.value = tree.getText().strip("'")
        return c

    def compile(self, globals):
        return str(ord(self.value))

    def __str__(self):
        return "'" + self.value + "'"

register_class(CharLiteral, "CHAR_LITERAL")


class Identifier(Compilable, Parameter):
    def __init__(self):
        self.value = ""

    @classmethod
    def from_tree(cls, tree):
        c = cls()
        c.tree = tree

        c.value = tree.getText()

        return c

    def __str__(self):
        return self.value

register_class(Identifier, "IDENTIFIER")
