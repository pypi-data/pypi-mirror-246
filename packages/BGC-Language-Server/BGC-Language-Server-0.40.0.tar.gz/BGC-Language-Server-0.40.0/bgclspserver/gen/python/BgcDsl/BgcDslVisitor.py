#  Copyright (c) 2023.  OceanDSL (https://oceandsl.uni-kiel.de)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

# Generated from BgcDsl.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .BgcDslParser import BgcDslParser
else:
    from BgcDslParser import BgcDslParser

# This class defines a complete generic visitor for a parse tree produced by BgcDslParser.

class BgcDslVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by BgcDslParser#bgcModel.
    def visitBgcModel(self, ctx:BgcDslParser.BgcModelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BgcDslParser#substanceDeclaration.
    def visitSubstanceDeclaration(self, ctx:BgcDslParser.SubstanceDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BgcDslParser#parameterDeclaration.
    def visitParameterDeclaration(self, ctx:BgcDslParser.ParameterDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BgcDslParser#environmentVariableDeclaration.
    def visitEnvironmentVariableDeclaration(self, ctx:BgcDslParser.EnvironmentVariableDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BgcDslParser#primitiveTypes.
    def visitPrimitiveTypes(self, ctx:BgcDslParser.PrimitiveTypesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BgcDslParser#compartment.
    def visitCompartment(self, ctx:BgcDslParser.CompartmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BgcDslParser#substanceState.
    def visitSubstanceState(self, ctx:BgcDslParser.SubstanceStateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BgcDslParser#updateState.
    def visitUpdateState(self, ctx:BgcDslParser.UpdateStateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BgcDslParser#connection.
    def visitConnection(self, ctx:BgcDslParser.ConnectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BgcDslParser#substanceExpression.
    def visitSubstanceExpression(self, ctx:BgcDslParser.SubstanceExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BgcDslParser#calculation.
    def visitCalculation(self, ctx:BgcDslParser.CalculationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BgcDslParser#basicCalculation.
    def visitBasicCalculation(self, ctx:BgcDslParser.BasicCalculationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BgcDslParser#alternativeCalculation.
    def visitAlternativeCalculation(self, ctx:BgcDslParser.AlternativeCalculationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BgcDslParser#caseCalculation.
    def visitCaseCalculation(self, ctx:BgcDslParser.CaseCalculationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BgcDslParser#unit.
    def visitUnit(self, ctx:BgcDslParser.UnitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BgcDslParser#unitElement.
    def visitUnitElement(self, ctx:BgcDslParser.UnitElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BgcDslParser#groupUnit.
    def visitGroupUnit(self, ctx:BgcDslParser.GroupUnitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BgcDslParser#prefixUnit.
    def visitPrefixUnit(self, ctx:BgcDslParser.PrefixUnitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BgcDslParser#arithmeticExpression.
    def visitArithmeticExpression(self, ctx:BgcDslParser.ArithmeticExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BgcDslParser#eAdditionOperator.
    def visitEAdditionOperator(self, ctx:BgcDslParser.EAdditionOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BgcDslParser#multiplicationExpression.
    def visitMultiplicationExpression(self, ctx:BgcDslParser.MultiplicationExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BgcDslParser#eMultiplicationOperator.
    def visitEMultiplicationOperator(self, ctx:BgcDslParser.EMultiplicationOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BgcDslParser#powerExpression.
    def visitPowerExpression(self, ctx:BgcDslParser.PowerExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BgcDslParser#valueExpression.
    def visitValueExpression(self, ctx:BgcDslParser.ValueExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BgcDslParser#arrayExpression.
    def visitArrayExpression(self, ctx:BgcDslParser.ArrayExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BgcDslParser#functionCallingExpression.
    def visitFunctionCallingExpression(self, ctx:BgcDslParser.FunctionCallingExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BgcDslParser#function.
    def visitFunction(self, ctx:BgcDslParser.FunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BgcDslParser#literalExpression.
    def visitLiteralExpression(self, ctx:BgcDslParser.LiteralExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BgcDslParser#literal.
    def visitLiteral(self, ctx:BgcDslParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BgcDslParser#numberLiteral.
    def visitNumberLiteral(self, ctx:BgcDslParser.NumberLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BgcDslParser#stringLiteral.
    def visitStringLiteral(self, ctx:BgcDslParser.StringLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BgcDslParser#parenthesisExpression.
    def visitParenthesisExpression(self, ctx:BgcDslParser.ParenthesisExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BgcDslParser#termReference.
    def visitTermReference(self, ctx:BgcDslParser.TermReferenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BgcDslParser#subterm.
    def visitSubterm(self, ctx:BgcDslParser.SubtermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BgcDslParser#qualifiedName.
    def visitQualifiedName(self, ctx:BgcDslParser.QualifiedNameContext):
        return self.visitChildren(ctx)



del BgcDslParser