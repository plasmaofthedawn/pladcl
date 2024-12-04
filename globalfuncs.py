from basetypes import *
from util import *


class GlobalFunc:
    def __init__(self, param_types, generation):
        self.param_types = param_types
        self.generation = generation
    

    def compile(self, params, globals):

        if len(params) != len(self.param_types):
            raise CompileError(f"Got {len(params)} parameters, expected {len(self.param_types)}")

        for p, t in zip(params, self.param_types):
            if not isinstance(p, t):
                raise CompileError(f"Bad type {type(p).__name__}, expected type {t.__name__}")

        return self.generation(
                [p.value for p in params], globals
        )
        
def setstate_generator(params, globals):
    if params[0] not in globals['stateid']:
        raise CompileError(f"Invalid state {params[0]}")

    return f"{globals['stateid'][params[0]]}ss"

def global_functions():

    return {
        "set_state": GlobalFunc([Identifier], setstate_generator),
        "streq": GlobalFunc([IntegerLiteral, StringLiteral], 
                            lambda params, globals: "[0" + "".join(f"li{(str(params[0] + count) + '+') if (params[0] + count > 0) else ""};I{ord(c)}!=q" for count, c in enumerate(params[1]))  + "1+]x"),
        "debug": GlobalFunc([DcLiteral], 
                            lambda params, globals: params[0] if globals["debug"] else ""),
        "debug_print": GlobalFunc([StringLiteral], 
                            lambda params, globals: ("[" + params[0] + "]n10an") if globals["debug"] else ""),
        "adjust_index": GlobalFunc([IntegerLiteral],
                                    lambda params, globals: f"li{params[0].compile(globals)}+dsi;Isn"),
        "set_index": GlobalFunc([IntegerLiteral],
                                lambda params, globals: f"{params[0].compile(globals)}dsi;Isn"),
        "rewind": GlobalFunc([], lambda params, globals: f"_1si")

    }
