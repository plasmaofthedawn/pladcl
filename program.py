from compilables import *
from globalfuncs import *

class Program(Compilable):

    VALID_INTERRUPTS = ["program_start", "loop", "newline", "program_end"]
    VALID_STATELESS_INTERRUPTS = ["program_start", "loop", "newline", "program_end"]

    def __init__(self):
        self.states = []
        self.functions = []
        self.interrupts = []


    @classmethod
    def from_tree(cls, tree):
        program = cls()
        program.tree = tree
        parse = cls.parse_tree(tree)

        program.states = parse['state_declaration']
        program.functions = parse['function_declaration']
        program.interrupts = {
            block.name: block for block in parse['interrupt_declaration']
        }

        return program

    def compile(self, debug=False, progress=None):
        if len(self.states) == 0:
            if progress:
                raise CompileError("progress option is not supported on stateless programs")
            return self.compile_without_states(debug=debug)
        else:
            return self.compile_with_states(debug=debug, progress=progress)



    def compile_without_states(self, debug=False):

        user_func_to_ind = {
            block.name: count for count, block in enumerate(self.functions)
        }

        globals = {
            "localfuncid": user_func_to_ind,
            "globalfunc": global_functions(),
            "debug": debug,
        }

        # needed macros
        output = "[q]sq"

        for count, func in enumerate(self.functions):
            output += f"[{func.compile(globals)}]{count}:F"

        if debug:
            output += "[Loaded functions]n10an"

        if "program_start" in self.interrupts:
            output += self.interrupts["program_start"].compile(globals)

        if "program_end" in self.interrupts:
            output += self.interrupts["program_end"].compile(globals)

        return output





    def compile_with_states(self, debug=False, progress=None):

        

        states_to_ind = {
            block.name: count for count, block in enumerate(self.states)
        }

        user_func_to_ind = {
            block.name: count for count, block in enumerate(self.functions)
        }

        globals = {
            "localfuncid": user_func_to_ind,
            "stateid": states_to_ind,
            "globalfunc": global_functions(),
            "debug": debug,
        }

        # needed macros
        output = "[q]sq"

        for count, state in enumerate(self.states):
            output += f"[{state.compile(globals)}]{count}:S"

        if debug:
            output += "[Loaded states]n10an"

        for count, func in enumerate(self.functions):
            output += f"[{func.compile(globals)}]{count}:F"

        if debug:
            output += "[Loaded functions]n10an"

        # load input onto stack
        output += "?_1[z1-:Iz0<l]dslx"
        # start things
        output += "0si0ss"

        if debug:
            output += "[Loaded input]n10an"

        if "program_start" in self.interrupts:
            output += self.interrupts["program_start"].compile(globals)

        # start of loop
        output += "[li;Idsn"
        # quit if n = -1 or 0
        output += "dr_1=q0=q"

        if progress:
            output += f"[li{progress}%0!=q[.]n]x"


        if "loop" in self.interrupts:
            output += self.interrupts["loop"].compile(globals)

        if "newline" in self.interrupts:
            output += f"[ln10!=q{self.interrupts["newline"].compile(globals)}]x"
        
        # debug
        if debug:
            output += "lsn[: ]nlnn[ ]nlnan10an"

        if debug:
            output += "[z0=q[Extra stuff on stack after interrupt:]n10anfq]x"

        # execute state
        output += "ls;Sx"
        if debug:
            output += "[z0=q[Extra stuff on stack:]n10anfq]x"

        # increment input index
        output += "li1+si"
        # loop
        output += "llx"
        output += "]dslx"

        if debug:
            output += "[Loop end]n10an"

        if progress:
            output += "10an"

        if "program_end" in self.interrupts:
            output += "st"
            output += self.interrupts["program_end"].compile(globals)

        return output



