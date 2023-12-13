''' Tests if a certain Symbol was inserted into the SymbolTable '''

__author__ = "stu90642"

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

from antlr4 import *
from ..bgclspserver.gen.python.BgcDsl.BgcDslLexer import BgcDslLexer
from ..bgclspserver.gen.python.BgcDsl.BgcDslParser import BgcDslParser
from ..bgclspserver.cst.symbol_table_visitor import SymbolTableVisitor
from SymbolTable_copy import ScopedSymbol, SymbolTable, P, T, VariableSymbol, Symbol, RoutineSymbol, SymbolTableOptions
import unittest

# tests SymbolTableVisitor
def prepare():
    # write_tdd()
    input_stream = FileStream('input/example1.bgc')
    # path = write_tdd()
    # input_stream = FileStream(path)
    lexer = BgcDslLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = BgcDslParser(stream)     # returns object of class "Parser"

    tree = parser.bgcModel()  # tree ist ein ctx-objekt
    my_SymbolTableVisitor = SymbolTableVisitor('SymbolTableVisitor_1')  # parse tree an SymbolTableVisitor übergeben
    symbolTable = my_SymbolTableVisitor.visit(tree)
    return symbolTable


class TestSTVisitor(unittest.TestCase):    # wenn ich eine klasse verwende, dann muss ihr name mit "Test" beginnen.

    # tests whether this variable is in the ST
    def test_substance_1(self):
        symbolTable = prepare()
        symbol = symbolTable.resolveSync('N')   # returnt das symbol-object, das Name N hat.
        self.assertIsNotNone(symbol)  # resolveSync returns a VariableSymbol object
        unit = ''.join(list(map(lambda x: x.getText(), symbol.value.unit().elements)))
        self.assertEqual(unit, 'mmol')
        self.assertEqual(symbol.value.type_.getText(), 'float')

    def test_substance_2(self):
        symbolTable = prepare()
        symbol = symbolTable.resolveSync('DIN')
        self.assertIsNotNone(symbol)  # resolveSync returns a VariableSymbol object
        unit = ''.join(list(map(lambda x: x.getText(), symbol.value.unit().elements)))
        self.assertEqual(unit, 'mmolNm^-3')
        self.assertEqual(symbol.value.type_.getText(), 'float')

    def test_parameter(self):
        symbolTable = prepare()
        symbol = symbolTable.resolveSync('Q_r_C_N')
        self.assertIsNotNone(symbol)  # resolveSync returns a VariableSymbol object
        unit = ''.join(list(map(lambda x: x.getText(), symbol.value.unit().elements)))
        self.assertEqual(unit, 'mmolC(mmolN)^-1')
        self.assertEqual(symbol.value.type_.getText(), 'float')

    def test_compartment(self):
        symbolTable = prepare()
        symbol = symbolTable.resolveSync('Nif')   # compartment
        # checks whether the compartment exists
        self.assertIsNotNone(symbol)
        # checks compartment contents
        states = list(map(lambda x: x.getText(), symbol.value.states))
        self.assertEqual(len(states), 4)
        self.assertEqual(states[0], 'Chl=0')
        parameters = symbol.value.constants   # parameters are in grammar as "constants"
        self.assertEqual(len(parameters), 2)
        self.assertEqual(parameters[0].name.text, 'Q_u2_N_C')
        self.assertEqual(parameters[0].type_.getText(), 'float')
        environments = symbol.value.evnironments
        self.assertEqual(len(environments), 2)
        self.assertEqual(environments[0].name.text, 'theta_C')
        calculations = symbol.value.calculations
        self.assertEqual(len(calculations), 14)
        self.assertEqual(calculations[0].getText(), 'calcPsi=max(0,Psi_max*(1-q_N_C/Q_2_N_C))')
        updateStates = symbol.value.updateStates
        self.assertEqual(len(updateStates), 4)
        self.assertEqual(updateStates[0].getText(), 'updateC=phot_DIC*C-(respiration+gamma+aggregation)*C')

    def test_connection_1(self):
        symbolTable = prepare()
        symbol = symbolTable.resolveSync('aggregation from Phy to Det')
        self.assertIsNotNone(symbol)
        self.assertEqual(symbol.value.expression.getText(), 'Phy.Phi*Phy.N+Det.Phi*Det.N')

    def test_connection_2(self):
        symbolTable = prepare()
        symbol = symbolTable.resolveSync('assimilation from Nutrients to Nif')
        self.assertIsNotNone(symbol)
        self.assertEqual(list(map(lambda x: x.text, symbol.value.substances)), ['N', 'C'])
        self.assertEqual(symbol.value.substanceExpressions[0].getText(), 'N=Nif.assim_DIP*Nif.N')


    # def test_amount(self):   # namen von test-funktionen müssen mit "test_" beginnen, oder auf "_test" enden.
    #     symbolTable = prepare()
    #     self.assertEqual(len(symbolTable.getAllSymbolsSync(Symbol)), 2)
