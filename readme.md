# pladcl

pladcl (plasma's lazy ass dc language) is a language that i wrote that targets the dc program.
this was written purely for advent of code lol

`pladclc` is the compiler

`pladcl.vim` is a vim syntax highlighting file i wrote for vim

## syntax

the entire code is stuck into three types of blocks, `state`, `function`, and `interrupt`.

### states

states are the main entry point. the program takes in a file (turned into a stream of numbers) and for every character will call whatever state it's in (it always starts at the first state).
states can be swapped between using the global function `set_state`

### functions

function blocks are blocks of code that can be called from anywhere.
i could have inlined this but meh
no user functions cannot have parameters

### interrupts

interrupts are blocks of code that are run at certain points in the code
as of right now there are 4:
- `program_start` is run on program start, after everything is loaded
- `loop` is run once at the beginning of every loop
- `newline` is run once at the beginning of every loop (after `loop` interrupt, if any) if the current char is `\n`
- `program_end` is run on program end, after the loop is finished

### lines
all lines of code are either function calls or dc literals
dc literals are marked with backticks on either end of them, and are just inserted as is.


### global functions

i really should have called these macros as that's what they are
as of right now there are a few:
 - `set_state(identifier id)` sets the current state to the state provided
 - `streq(int offset, str)` returns 1 if the chars on the stack + offset match string, else 0
 - `debug(dcliteral)` adds code if debug flag
 - `debug_print(str)` prints str if debug flag
 - `adjust_index(int)` adjusts the index by the given number
 - `set_index(int)`    set the index to the given number. note that this will be incremented at end of loop
 - `rewind()` rewinds the index back to the beginning