from basetypes import *
from globalfuncs import *


class Block:
    def __init__(self):
        self.name = "invalid"
        self.type = "invalid"
        self.lines = []

    def add_line(self, line: Line):
        self.lines.append(line)

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

class Program:

    VALID_INTERRUPTS = ["program_start", "loop", "newline", "program_end"]

    def __init__(self):
        self.states = []
        self.functions = []
        self.interrupts = {}

    def add_block(self, block):


        if block.type == "state":
            if block.name in [x.name for x in self.states]:
                raise CompileError(f"duplicate state {block.name}")
            
            self.states.append(block)

        elif block.type == "function":
            if block.name in [x.name for x in self.functions]:
                raise CompileError(f"duplicate function {block.name}")

            self.functions.append(block)

        elif block.type == "interrupt":
            if block.name not in self.VALID_INTERRUPTS:
                raise CompileError(f"{block.name} is not a valid interrupt")

            if block.name in self.interrupts:
                raise CompileError(f"duplicate interrupt {block.name}")

            self.interrupts[block.name] = block

    def compile(self, debug=False, progress=None):


        if len(self.states) == 0:
            raise CompileError("program must have at least one state")

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
            output += self.interrupts["program_end"].compile(globals)

        return output







