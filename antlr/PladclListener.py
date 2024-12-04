# Generated from Pladcl.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .PladclParser import PladclParser
else:
    from PladclParser import PladclParser

# This class defines a complete listener for a parse tree produced by PladclParser.
class PladclListener(ParseTreeListener):

    # Enter a parse tree produced by PladclParser#parameter.
    def enterParameter(self, ctx:PladclParser.ParameterContext):
        pass

    # Exit a parse tree produced by PladclParser#parameter.
    def exitParameter(self, ctx:PladclParser.ParameterContext):
        pass


    # Enter a parse tree produced by PladclParser#parameter_list.
    def enterParameter_list(self, ctx:PladclParser.Parameter_listContext):
        pass

    # Exit a parse tree produced by PladclParser#parameter_list.
    def exitParameter_list(self, ctx:PladclParser.Parameter_listContext):
        pass


    # Enter a parse tree produced by PladclParser#function.
    def enterFunction(self, ctx:PladclParser.FunctionContext):
        pass

    # Exit a parse tree produced by PladclParser#function.
    def exitFunction(self, ctx:PladclParser.FunctionContext):
        pass


    # Enter a parse tree produced by PladclParser#empty_line.
    def enterEmpty_line(self, ctx:PladclParser.Empty_lineContext):
        pass

    # Exit a parse tree produced by PladclParser#empty_line.
    def exitEmpty_line(self, ctx:PladclParser.Empty_lineContext):
        pass


    # Enter a parse tree produced by PladclParser#line.
    def enterLine(self, ctx:PladclParser.LineContext):
        pass

    # Exit a parse tree produced by PladclParser#line.
    def exitLine(self, ctx:PladclParser.LineContext):
        pass


    # Enter a parse tree produced by PladclParser#end.
    def enterEnd(self, ctx:PladclParser.EndContext):
        pass

    # Exit a parse tree produced by PladclParser#end.
    def exitEnd(self, ctx:PladclParser.EndContext):
        pass


    # Enter a parse tree produced by PladclParser#state_declaration.
    def enterState_declaration(self, ctx:PladclParser.State_declarationContext):
        pass

    # Exit a parse tree produced by PladclParser#state_declaration.
    def exitState_declaration(self, ctx:PladclParser.State_declarationContext):
        pass


    # Enter a parse tree produced by PladclParser#function_declaration.
    def enterFunction_declaration(self, ctx:PladclParser.Function_declarationContext):
        pass

    # Exit a parse tree produced by PladclParser#function_declaration.
    def exitFunction_declaration(self, ctx:PladclParser.Function_declarationContext):
        pass


    # Enter a parse tree produced by PladclParser#interrupt_declaration.
    def enterInterrupt_declaration(self, ctx:PladclParser.Interrupt_declarationContext):
        pass

    # Exit a parse tree produced by PladclParser#interrupt_declaration.
    def exitInterrupt_declaration(self, ctx:PladclParser.Interrupt_declarationContext):
        pass


    # Enter a parse tree produced by PladclParser#expression.
    def enterExpression(self, ctx:PladclParser.ExpressionContext):
        pass

    # Exit a parse tree produced by PladclParser#expression.
    def exitExpression(self, ctx:PladclParser.ExpressionContext):
        pass


    # Enter a parse tree produced by PladclParser#predicate.
    def enterPredicate(self, ctx:PladclParser.PredicateContext):
        pass

    # Exit a parse tree produced by PladclParser#predicate.
    def exitPredicate(self, ctx:PladclParser.PredicateContext):
        pass


    # Enter a parse tree produced by PladclParser#if_line.
    def enterIf_line(self, ctx:PladclParser.If_lineContext):
        pass

    # Exit a parse tree produced by PladclParser#if_line.
    def exitIf_line(self, ctx:PladclParser.If_lineContext):
        pass


    # Enter a parse tree produced by PladclParser#program.
    def enterProgram(self, ctx:PladclParser.ProgramContext):
        pass

    # Exit a parse tree produced by PladclParser#program.
    def exitProgram(self, ctx:PladclParser.ProgramContext):
        pass



del PladclParser