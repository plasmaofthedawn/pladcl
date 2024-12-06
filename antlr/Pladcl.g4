
grammar Pladcl;

/* end */
end: WHITESPACE? END WHITESPACE? NEWLINE;

/* parameter: anything that can go into a macro call*/
parameter : DC_LITERAL | STRING_LITERAL | INTEGER_LITERAL | IDENTIFIER 
                | predicate | CHAR_LITERAL;

/* line: any line of code */
line: WHITESPACE? (expression | return_line | BREAK) WHITESPACE? NEWLINE
      | empty_line 
      | WHITESPACE? (if_line | while_line | for_in_line | for_stack_line);

/* expression: any expression (thing that returns a value) */
expression : DC_LITERAL | function | INTEGER_LITERAL | CHAR_LITERAL | STRING_LITERAL;

/* predicate: a boolean conditional (0 == 1 ot smth */
predicate : WHITESPACE? expression WHITESPACE? COMPARISONS WHITESPACE? expression WHITESPACE? ;

empty_line: WHITESPACE? NEWLINE;

/* basic lines */
function: IDENTIFIER WHITESPACE? '(' WHITESPACE? ((parameter WHITESPACE? ',' WHITESPACE?)* parameter)? WHITESPACE? ')';
return_line : RETURN WHITESPACE? expression? ;

/* complex lines */
if_line : IF WHITESPACE? predicate WHITESPACE? THEN WHITESPACE? NEWLINE line* end ;
/* loops */
while_line: WHILE WHITESPACE? predicate WHITESPACE? DO WHITESPACE? NEWLINE line* end ;
for_in_line: FOR WHITESPACE? CHAR_LITERAL WHITESPACE? 
             IN WHITESPACE? expression WHITESPACE? TO WHITESPACE? expression WHITESPACE?
             (STEP WHITESPACE? expression WHITESPACE?)?
             DO WHITESPACE? NEWLINE line* end;
for_stack_line: FOR WHITESPACE? CHAR_LITERAL WHITESPACE? 
                IN WHITESPACE? STACK WHITESPACE? CHAR_LITERAL WHITESPACE?
                DO WHITESPACE? NEWLINE line* end;


/* primary program blocks */
state_declaration : 
STATE WHITESPACE? IDENTIFIER WHITESPACE? NEWLINE line* end;
function_declaration : 
FUNCTION WHITESPACE? IDENTIFIER WHITESPACE? NEWLINE line* end;
interrupt_declaration : 
INTERRUPT WHITESPACE? IDENTIFIER WHITESPACE? NEWLINE line* end;

/* program itself */
program: (empty_line | state_declaration | function_declaration | interrupt_declaration)+;


/* whitespace */
WHITESPACE: (' ' | '\t')+ ;
NEWLINE: ('\r'? '\n' | '\r')+ ;

/* literals */
STRING_LITERAL: '"' ~["]+ '"' ;
DC_LITERAL: '`' ~[`]+ '`';
CHAR_LITERAL: '\'' . '\'' ;
INTEGER_LITERAL: '-'?WHITESPACE?[0-9]+;

/* operators */
COMPARISONS: '==' | '!=' | '>' | '<' | '>=' | '<=' | '!>' | '!<';

/* Keywords */
END: 'end';
FUNCTION: 'function';
STATE: 'state';
INTERRUPT: 'interrupt';
IF: 'if';
THEN: 'then';
RETURN: 'return';
WHILE: 'while';
DO: 'do';
BREAK: 'break';
FOR: 'for';
IN: 'in';
TO: 'to';
STEP: 'step';
STACK: 'stack';

/* identifier */
IDENTIFIER: ([a-z] | [A-Z] | '_')+;

/* comment */
COMMENT: '#'~[\r\n]* ->skip;




