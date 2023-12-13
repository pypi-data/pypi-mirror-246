"""unittest example for CodeCompletionCore"""

__author__ = 'sgu'

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

# util imports
from unittest import TestCase

# antlr4
from antlr4 import InputStream, CommonTokenStream, DiagnosticErrorListener

# antlr4-c3
from codeCompletionCore.CodeCompletionCore import CodeCompletionCore

# grammar imports (example-DSL module dependency)
from examplelspserver.gen.python.TestExprCore.TestExprCoreLexer import TestExprCoreLexer
from examplelspserver.gen.python.TestExprCore.TestExprCoreParser import TestExprCoreParser


class TestCodeCompletionCore( TestCase ):

    def setUp( self ) -> None:
        # create input stream of characters for lexer
        # most simple setup
        self.input_stream = InputStream( "var c = a + b()" )

        # create lexer and parser objects and token stream pipe between them
        self.lexer = TestExprCoreLexer( self.input_stream )
        self.tokenStream = CommonTokenStream( self.lexer )

        self.parser = TestExprCoreParser( self.tokenStream )
        self.parser.addErrorListener( DiagnosticErrorListener )

        # launch parser by invoking rule 'expression'
        self.ast = self.parser.expression( )

        # launch c3 core with parser
        self.core = CodeCompletionCore( self.parser )

    # 1) At the input start.
    def test_inputStart( self ):
        candidates = self.core.collectCandidates( 0 )
        self.assertEqual( 3, len( candidates.tokens ) )
        self.assertIn( TestExprCoreLexer.VAR, candidates.tokens )
        self.assertIn( TestExprCoreLexer.LET, candidates.tokens )
        self.assertIn( TestExprCoreLexer.ID, candidates.tokens )
        self.assertEqual(
                [ TestExprCoreLexer.ID, TestExprCoreLexer.EQUAL ],
                candidates.tokens.get( TestExprCoreLexer.VAR )
        )
        self.assertEqual(
                [ TestExprCoreLexer.ID, TestExprCoreLexer.EQUAL ],
                candidates.tokens.get( TestExprCoreLexer.LET )
        )
        self.assertEqual( [ ], candidates.tokens.get( TestExprCoreLexer.ID ) )

    # 2) On the first whitespace. In real implementations you would do some additional checks where in the whitespace the caret is, as the outcome is different depending on that position.
    def test_first_whitespace( self ):
        candidates = self.core.collectCandidates( 1 )
        self.assertEqual( 1, len( candidates.tokens ) )
        self.assertIn( TestExprCoreLexer.ID, candidates.tokens )

    # 3) On the variable name ('c').
    def test_variable_name( self ):
        candidates = self.core.collectCandidates( 2 )
        self.assertEqual( 1, len( candidates.tokens ) )
        self.assertIn( TestExprCoreLexer.ID, candidates.tokens )

    # 4) On the equal sign (ignoring whitespace positions from now on).
    def test_equal_sign( self ):
        candidates = self.core.collectCandidates( 4 )
        self.assertEqual( 1, len( candidates.tokens ) )
        self.assertIn( TestExprCoreLexer.EQUAL, candidates.tokens )

    # 5) On the variable reference 'a'. But since we have not configured the c3 engine to return us var refs (or function refs for that matter) we only get an ID here.
    def test_variable_reference( self ):
        candidates = self.core.collectCandidates( 6 )
        self.assertEqual( 1, len( candidates.tokens ) )
        self.assertIn( TestExprCoreLexer.ID, candidates.tokens )

    # 6) On the '+' operator. Usually you would not show operators as candidates, but we have not set up the c3 engine yet to not return them.
    def test_plus_operator( self ):
        candidates = self.core.collectCandidates( 8 )
        self.assertEqual( 5, len( candidates.tokens ) )
        self.assertIn( TestExprCoreLexer.PLUS, candidates.tokens )
        self.assertIn( TestExprCoreLexer.MINUS, candidates.tokens )
        self.assertIn( TestExprCoreLexer.MULTIPLY, candidates.tokens )
        self.assertIn( TestExprCoreLexer.DIVIDE, candidates.tokens )
        self.assertIn( TestExprCoreLexer.OPEN_PAR, candidates.tokens )
