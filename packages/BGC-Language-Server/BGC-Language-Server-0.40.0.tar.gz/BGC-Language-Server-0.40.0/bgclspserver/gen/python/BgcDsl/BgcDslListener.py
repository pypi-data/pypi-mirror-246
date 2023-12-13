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

# This class defines a complete listener for a parse tree produced by BgcDslParser.
class BgcDslListener(ParseTreeListener):

    # Enter a parse tree produced by BgcDslParser#bgcModel.
    def enterBgcModel(self, ctx:BgcDslParser.BgcModelContext):
        pass

    # Exit a parse tree produced by BgcDslParser#bgcModel.
    def exitBgcModel(self, ctx:BgcDslParser.BgcModelContext):
        pass


    # Enter a parse tree produced by BgcDslParser#substanceDeclaration.
    def enterSubstanceDeclaration(self, ctx:BgcDslParser.SubstanceDeclarationContext):
        pass

    # Exit a parse tree produced by BgcDslParser#substanceDeclaration.
    def exitSubstanceDeclaration(self, ctx:BgcDslParser.SubstanceDeclarationContext):
        pass


    # Enter a parse tree produced by BgcDslParser#parameterDeclaration.
    def enterParameterDeclaration(self, ctx:BgcDslParser.ParameterDeclarationContext):
        pass

    # Exit a parse tree produced by BgcDslParser#parameterDeclaration.
    def exitParameterDeclaration(self, ctx:BgcDslParser.ParameterDeclarationContext):
        pass


    # Enter a parse tree produced by BgcDslParser#environmentVariableDeclaration.
    def enterEnvironmentVariableDeclaration(self, ctx:BgcDslParser.EnvironmentVariableDeclarationContext):
        pass

    # Exit a parse tree produced by BgcDslParser#environmentVariableDeclaration.
    def exitEnvironmentVariableDeclaration(self, ctx:BgcDslParser.EnvironmentVariableDeclarationContext):
        pass


    # Enter a parse tree produced by BgcDslParser#primitiveTypes.
    def enterPrimitiveTypes(self, ctx:BgcDslParser.PrimitiveTypesContext):
        pass

    # Exit a parse tree produced by BgcDslParser#primitiveTypes.
    def exitPrimitiveTypes(self, ctx:BgcDslParser.PrimitiveTypesContext):
        pass


    # Enter a parse tree produced by BgcDslParser#compartment.
    def enterCompartment(self, ctx:BgcDslParser.CompartmentContext):
        pass

    # Exit a parse tree produced by BgcDslParser#compartment.
    def exitCompartment(self, ctx:BgcDslParser.CompartmentContext):
        pass


    # Enter a parse tree produced by BgcDslParser#substanceState.
    def enterSubstanceState(self, ctx:BgcDslParser.SubstanceStateContext):
        pass

    # Exit a parse tree produced by BgcDslParser#substanceState.
    def exitSubstanceState(self, ctx:BgcDslParser.SubstanceStateContext):
        pass


    # Enter a parse tree produced by BgcDslParser#updateState.
    def enterUpdateState(self, ctx:BgcDslParser.UpdateStateContext):
        pass

    # Exit a parse tree produced by BgcDslParser#updateState.
    def exitUpdateState(self, ctx:BgcDslParser.UpdateStateContext):
        pass


    # Enter a parse tree produced by BgcDslParser#connection.
    def enterConnection(self, ctx:BgcDslParser.ConnectionContext):
        pass

    # Exit a parse tree produced by BgcDslParser#connection.
    def exitConnection(self, ctx:BgcDslParser.ConnectionContext):
        pass


    # Enter a parse tree produced by BgcDslParser#substanceExpression.
    def enterSubstanceExpression(self, ctx:BgcDslParser.SubstanceExpressionContext):
        pass

    # Exit a parse tree produced by BgcDslParser#substanceExpression.
    def exitSubstanceExpression(self, ctx:BgcDslParser.SubstanceExpressionContext):
        pass


    # Enter a parse tree produced by BgcDslParser#calculation.
    def enterCalculation(self, ctx:BgcDslParser.CalculationContext):
        pass

    # Exit a parse tree produced by BgcDslParser#calculation.
    def exitCalculation(self, ctx:BgcDslParser.CalculationContext):
        pass


    # Enter a parse tree produced by BgcDslParser#basicCalculation.
    def enterBasicCalculation(self, ctx:BgcDslParser.BasicCalculationContext):
        pass

    # Exit a parse tree produced by BgcDslParser#basicCalculation.
    def exitBasicCalculation(self, ctx:BgcDslParser.BasicCalculationContext):
        pass


    # Enter a parse tree produced by BgcDslParser#alternativeCalculation.
    def enterAlternativeCalculation(self, ctx:BgcDslParser.AlternativeCalculationContext):
        pass

    # Exit a parse tree produced by BgcDslParser#alternativeCalculation.
    def exitAlternativeCalculation(self, ctx:BgcDslParser.AlternativeCalculationContext):
        pass


    # Enter a parse tree produced by BgcDslParser#caseCalculation.
    def enterCaseCalculation(self, ctx:BgcDslParser.CaseCalculationContext):
        pass

    # Exit a parse tree produced by BgcDslParser#caseCalculation.
    def exitCaseCalculation(self, ctx:BgcDslParser.CaseCalculationContext):
        pass


    # Enter a parse tree produced by BgcDslParser#unit.
    def enterUnit(self, ctx:BgcDslParser.UnitContext):
        pass

    # Exit a parse tree produced by BgcDslParser#unit.
    def exitUnit(self, ctx:BgcDslParser.UnitContext):
        pass


    # Enter a parse tree produced by BgcDslParser#unitElement.
    def enterUnitElement(self, ctx:BgcDslParser.UnitElementContext):
        pass

    # Exit a parse tree produced by BgcDslParser#unitElement.
    def exitUnitElement(self, ctx:BgcDslParser.UnitElementContext):
        pass


    # Enter a parse tree produced by BgcDslParser#groupUnit.
    def enterGroupUnit(self, ctx:BgcDslParser.GroupUnitContext):
        pass

    # Exit a parse tree produced by BgcDslParser#groupUnit.
    def exitGroupUnit(self, ctx:BgcDslParser.GroupUnitContext):
        pass


    # Enter a parse tree produced by BgcDslParser#prefixUnit.
    def enterPrefixUnit(self, ctx:BgcDslParser.PrefixUnitContext):
        pass

    # Exit a parse tree produced by BgcDslParser#prefixUnit.
    def exitPrefixUnit(self, ctx:BgcDslParser.PrefixUnitContext):
        pass


    # Enter a parse tree produced by BgcDslParser#arithmeticExpression.
    def enterArithmeticExpression(self, ctx:BgcDslParser.ArithmeticExpressionContext):
        pass

    # Exit a parse tree produced by BgcDslParser#arithmeticExpression.
    def exitArithmeticExpression(self, ctx:BgcDslParser.ArithmeticExpressionContext):
        pass


    # Enter a parse tree produced by BgcDslParser#eAdditionOperator.
    def enterEAdditionOperator(self, ctx:BgcDslParser.EAdditionOperatorContext):
        pass

    # Exit a parse tree produced by BgcDslParser#eAdditionOperator.
    def exitEAdditionOperator(self, ctx:BgcDslParser.EAdditionOperatorContext):
        pass


    # Enter a parse tree produced by BgcDslParser#multiplicationExpression.
    def enterMultiplicationExpression(self, ctx:BgcDslParser.MultiplicationExpressionContext):
        pass

    # Exit a parse tree produced by BgcDslParser#multiplicationExpression.
    def exitMultiplicationExpression(self, ctx:BgcDslParser.MultiplicationExpressionContext):
        pass


    # Enter a parse tree produced by BgcDslParser#eMultiplicationOperator.
    def enterEMultiplicationOperator(self, ctx:BgcDslParser.EMultiplicationOperatorContext):
        pass

    # Exit a parse tree produced by BgcDslParser#eMultiplicationOperator.
    def exitEMultiplicationOperator(self, ctx:BgcDslParser.EMultiplicationOperatorContext):
        pass


    # Enter a parse tree produced by BgcDslParser#powerExpression.
    def enterPowerExpression(self, ctx:BgcDslParser.PowerExpressionContext):
        pass

    # Exit a parse tree produced by BgcDslParser#powerExpression.
    def exitPowerExpression(self, ctx:BgcDslParser.PowerExpressionContext):
        pass


    # Enter a parse tree produced by BgcDslParser#valueExpression.
    def enterValueExpression(self, ctx:BgcDslParser.ValueExpressionContext):
        pass

    # Exit a parse tree produced by BgcDslParser#valueExpression.
    def exitValueExpression(self, ctx:BgcDslParser.ValueExpressionContext):
        pass


    # Enter a parse tree produced by BgcDslParser#arrayExpression.
    def enterArrayExpression(self, ctx:BgcDslParser.ArrayExpressionContext):
        pass

    # Exit a parse tree produced by BgcDslParser#arrayExpression.
    def exitArrayExpression(self, ctx:BgcDslParser.ArrayExpressionContext):
        pass


    # Enter a parse tree produced by BgcDslParser#functionCallingExpression.
    def enterFunctionCallingExpression(self, ctx:BgcDslParser.FunctionCallingExpressionContext):
        pass

    # Exit a parse tree produced by BgcDslParser#functionCallingExpression.
    def exitFunctionCallingExpression(self, ctx:BgcDslParser.FunctionCallingExpressionContext):
        pass


    # Enter a parse tree produced by BgcDslParser#function.
    def enterFunction(self, ctx:BgcDslParser.FunctionContext):
        pass

    # Exit a parse tree produced by BgcDslParser#function.
    def exitFunction(self, ctx:BgcDslParser.FunctionContext):
        pass


    # Enter a parse tree produced by BgcDslParser#literalExpression.
    def enterLiteralExpression(self, ctx:BgcDslParser.LiteralExpressionContext):
        pass

    # Exit a parse tree produced by BgcDslParser#literalExpression.
    def exitLiteralExpression(self, ctx:BgcDslParser.LiteralExpressionContext):
        pass


    # Enter a parse tree produced by BgcDslParser#literal.
    def enterLiteral(self, ctx:BgcDslParser.LiteralContext):
        pass

    # Exit a parse tree produced by BgcDslParser#literal.
    def exitLiteral(self, ctx:BgcDslParser.LiteralContext):
        pass


    # Enter a parse tree produced by BgcDslParser#numberLiteral.
    def enterNumberLiteral(self, ctx:BgcDslParser.NumberLiteralContext):
        pass

    # Exit a parse tree produced by BgcDslParser#numberLiteral.
    def exitNumberLiteral(self, ctx:BgcDslParser.NumberLiteralContext):
        pass


    # Enter a parse tree produced by BgcDslParser#stringLiteral.
    def enterStringLiteral(self, ctx:BgcDslParser.StringLiteralContext):
        pass

    # Exit a parse tree produced by BgcDslParser#stringLiteral.
    def exitStringLiteral(self, ctx:BgcDslParser.StringLiteralContext):
        pass


    # Enter a parse tree produced by BgcDslParser#parenthesisExpression.
    def enterParenthesisExpression(self, ctx:BgcDslParser.ParenthesisExpressionContext):
        pass

    # Exit a parse tree produced by BgcDslParser#parenthesisExpression.
    def exitParenthesisExpression(self, ctx:BgcDslParser.ParenthesisExpressionContext):
        pass


    # Enter a parse tree produced by BgcDslParser#termReference.
    def enterTermReference(self, ctx:BgcDslParser.TermReferenceContext):
        pass

    # Exit a parse tree produced by BgcDslParser#termReference.
    def exitTermReference(self, ctx:BgcDslParser.TermReferenceContext):
        pass


    # Enter a parse tree produced by BgcDslParser#subterm.
    def enterSubterm(self, ctx:BgcDslParser.SubtermContext):
        pass

    # Exit a parse tree produced by BgcDslParser#subterm.
    def exitSubterm(self, ctx:BgcDslParser.SubtermContext):
        pass


    # Enter a parse tree produced by BgcDslParser#qualifiedName.
    def enterQualifiedName(self, ctx:BgcDslParser.QualifiedNameContext):
        pass

    # Exit a parse tree produced by BgcDslParser#qualifiedName.
    def exitQualifiedName(self, ctx:BgcDslParser.QualifiedNameContext):
        pass



del BgcDslParser