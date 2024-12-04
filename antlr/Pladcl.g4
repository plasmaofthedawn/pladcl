grammar Pladcl;

parameter : DC_LITERAL | STRING_LITERAL | INTEGER_LITERAL | IDENTIFIER;
parameter_list : (parameter WHITESPACE? ',' WHITESPACE?)* parameter ;
function: IDENTIFIER WHITESPACE? '(' WHITESPACE? parameter_list? WHITESPACE? ')';

empty_line: WHITESPACE? NEWLINE;
line: WHITESPACE? (DC_LITERAL | function) WHITESPACE? NEWLINE
    | empty_line;

end: WHITESPACE? END WHITESPACE? NEWLINE;
state_declaration : 
STATE WHITESPACE? IDENTIFIER WHITESPACE? NEWLINE line* end;
function_declaration : 
FUNCTION WHITESPACE? IDENTIFIER WHITESPACE? NEWLINE line* end;
interrupt_declaration : 
INTERRUPT WHITESPACE? IDENTIFIER WHITESPACE? NEWLINE line* end;

program: (empty_line | state_declaration | function_declaration | interrupt_declaration)+;


WHITESPACE: (' ' | '\t')+ ;
NEWLINE: ('\r'? '\n' | '\r')+ ;

STRING_LITERAL: '"' ~["]+ '"' ;
DC_LITERAL: '`' ~[`]+ '`';

/* Keywords */
END: 'end';
FUNCTION: 'function';
STATE: 'state';
INTERRUPT: 'interrupt';

COMMENT: '#'~[\r\n]* ->skip;

INTEGER_LITERAL: '-'?WHITESPACE?[0-9]+;
IDENTIFIER: ([a-z] | [A-Z] | '_')+;
