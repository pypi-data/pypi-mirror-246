"""this main is just for testing"""

__author__ = 'stu90642'

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

from os import getcwd
from antlr4 import *
from ..bgclspserver.gen.python.BgcDsl.BgcDslLexer import BgcDslLexer
from ..bgclspserver.gen.python.BgcDsl.BgcDslParser import BgcDslParser
from ..bgclspserver.cst.symbol_table_visitor import SymbolTableVisitor
from ..bgclspserver.symbolTable.symbol_table import ScopedSymbol, SymbolTable, P, T, VariableSymbol, Symbol, RoutineSymbol, SymbolTableOptions
import unittest

def main():
    input_stream = FileStream('input/example1.bgc')
    lexer = BgcDslLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = BgcDslParser(stream)     # returns object of class "Parser"
    tree = parser.bgcModel()  # tree ist ein ctx-objekt; bgcModel is the first rule

    symbolTable = SymbolTableVisitor('SymbolTableVisitor_1').visit(tree)

    # # shows the SymbolTable contents
    # for e in symbolTable.getAllSymbolsSync(Symbol):
    #     print(e.name)
    #     # unit = ''.join(list(map(lambda x: x.getText(), e.value.unit().elements)))
    #     # unit = ' '.join(e.value.unit().elements)
    #     # while len(unit) != 0 and unit[0] == ':':
    #     #     unit = unit[1:]
    #     # print(unit, e.value.type_.getText())


    self = unittest.TestCase()

    symbol = symbolTable.resolveSync('aggregation from Phy to Det')
    self.assertIsNotNone(symbol)
    self.assertEqual(symbol.value.expression.getText(), 'Phy.Phi*Phy.N+Det.Phi*Det.N')

    symbol = symbolTable.resolveSync('assimilation from Nutrients to Nif')
    self.assertIsNotNone(symbol)
    self.assertEqual(list(map(lambda x: x.text, symbol.value.substances)), ['N', 'C'])
    self.assertEqual(symbol.value.substanceExpressions[0].getText(), 'N=Nif.assim_DIP*Nif.N')

    print('all good')

if __name__ == '__main__':
    main()
