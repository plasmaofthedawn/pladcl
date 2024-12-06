from util import get_name, get_children, unwrap_singleton, get_line
from collections import defaultdict

class CompileError(Exception):
    pass

class Compilable:

    name_to_type: dict[str, 'Compilable'] = dict()
    singleton_names: set[str] = set()

    def __init__(self):
        """Initialize all needed variables to default"""
        self.tree = None

    @classmethod
    def from_kwargs(cls, **kwargs):
        c = cls()

        for k, v in kwargs.items():
            c.__setattr__(k, v)

        return c

    @classmethod
    def from_tree(cls, tree):
        """Gathers all needed variables from the provided tree"""
        c = cls()
        c.tree = tree
        return c

    def compile(self, globals: dict) -> str:
        raise NotImplementedError

    @staticmethod
    def parse_tree(tree):
        out = defaultdict(list)

        for node in get_children(tree):

            name = get_name(node)
            #print(name)
            
            while get_name(node) in Compilable.singleton_names:
                node = unwrap_singleton(node)
                #print("\t", get_name(node))

            # if we have a type for this name
            if get_name(node) in Compilable.name_to_type:
                cls = Compilable.name_to_type[get_name(node)]
                value = cls.from_tree(node)
            else:
                value = node

            out[name].append(value)

        #print(out)

        return out

    def error(self, error: str):
        raise CompileError(error + f" on line {get_line(self.tree)}")


def register_class(cls, name):
    #Compilable.register(cls)
    Compilable.name_to_type[name] = cls
    
def register_singleton(name):
    Compilable.singleton_names.add(name)


# i'm not sure where to put these yet
register_singleton("line")
register_singleton("expression")
register_singleton("parameter")


# all this for like. 1 space
def needs_escaped(command):

    # if it is a digit this could be bad
    if command.isdigit():
        return True

    # if this is a 
    #if command[0] == "-" and command[1:].isdigit():
    #    return True

    # if the last thing is a digit and it's not being used as a register yikes
    if len(command) > 1 and command[-1].isdigit() and command[-2] not in "slSL><=;:":
        return True

    return False

def join_compilables(commands, globals):

    compiled = [x if type(x) is str else x.compile(globals) for x in commands]
    compiled = [x for x in compiled if x != ""]

    if len(compiled) == 0:
        return ""


    #print(compiled)

    out = ""
    for command, next_command in zip(compiled, compiled[1:]):

        if command == "":
            continue

        out += command

        if next_command != "" and needs_escaped(command) and next_command[0].isdigit():
            out += " "

    out += compiled[-1]
    #print(out)
    return out


