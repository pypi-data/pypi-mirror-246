"""pytest example for CodeCompletionCore"""

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
import pytest
from typing import List, Set

# antlr4
from antlr4 import CommonTokenStream, DiagnosticErrorListener, InputStream

# antlr4-c3
from codeCompletionCore.CodeCompletionCore import CandidatesCollection, CodeCompletionCore

# grammar imports (example-DSL module dependency)
from examplelspserver.gen.python.TestExprCore.TestExprCoreLexer import TestExprCoreLexer
from examplelspserver.gen.python.TestExprCore.TestExprCoreParser import TestExprCoreParser

# tokenIndexes for collect_candidates test parameterization
inputTokenIndex: Set[ int ] = {0, 1, 2, 4, 6, 8}
# input stream for core
inputStream: List[ str ] = [ "var c = a + b()" ]


# Core set up
@pytest.fixture( scope = "function" )
def core( request ) -> CodeCompletionCore:
    # create input stream of characters for lexer
    # most simple setup
    input_stream = InputStream( request.param )

    # create lexer and parser objects and token stream pipe between them
    lexer = TestExprCoreLexer( input_stream )
    tokenStream = CommonTokenStream( lexer )

    parser = TestExprCoreParser( tokenStream )
    parser.addErrorListener( DiagnosticErrorListener )

    # launch parser by invoking rule 'expression'
    parser.expression( )

    # launch c3 core with parser
    return CodeCompletionCore( parser )


class TestCodeCompletionCore:
    @pytest.mark.parametrize( "core", inputStream, indirect = [ "core" ] )
    @pytest.mark.parametrize( "tokenIndex", inputTokenIndex )
    def test_collect_candidates( self, core, tokenIndex ) -> None:
        """
        Test collected candidates for 'var c = a + b()' at tokenIndex

        :param core: test fixture to set up the core
        :param tokenIndex: tokenIndex from caret
        :return:
        """
        candidates: CandidatesCollection = core.collectCandidates( tokenIndex )
        match tokenIndex:
            # At the input start.
            case 0:
                assert 3 == len( candidates.tokens )
                assert TestExprCoreLexer.VAR in candidates.tokens
                assert TestExprCoreLexer.LET in candidates.tokens
                assert TestExprCoreLexer.ID in candidates.tokens
                assert [ TestExprCoreLexer.ID, TestExprCoreLexer.EQUAL ] == candidates.tokens.get( TestExprCoreLexer.VAR )
                assert [ TestExprCoreLexer.ID, TestExprCoreLexer.EQUAL ] == candidates.tokens.get( TestExprCoreLexer.LET )
                assert [ ] == candidates.tokens.get( TestExprCoreLexer.ID )
            # On the first whitespace. In real implementations you would do some additional checks where in the whitespace
            # the caret is, as the outcome is different depending on that position.
            case 1:
                assert 1 == len( candidates.tokens )
                assert TestExprCoreLexer.ID in candidates.tokens
            # On the variable name ('c').
            case 2:
                assert 1 == len( candidates.tokens )
                assert TestExprCoreLexer.ID in candidates.tokens
            # On the equal sign (ignoring whitespace positions from now on).
            case 4:
                assert 1 == len( candidates.tokens )
                assert TestExprCoreLexer.EQUAL in candidates.tokens
            # On the variable reference 'a'. But since we have not configured the c3 engine to return us var refs (or
            # function refs for that matter) we only get an ID here.
            case 6:
                assert 1 == len( candidates.tokens )
                assert TestExprCoreLexer.ID in candidates.tokens
            # On the '+' operator. Usually you would not show operators as candidates, but we have not set up the c3 engine
            # yet to not return them.
            case 8:
                assert 5 == len( candidates.tokens )
                assert TestExprCoreLexer.PLUS in candidates.tokens
                assert TestExprCoreLexer.MINUS in candidates.tokens
                assert TestExprCoreLexer.MULTIPLY in candidates.tokens
                assert TestExprCoreLexer.DIVIDE in candidates.tokens
                assert TestExprCoreLexer.OPEN_PAR in candidates.tokens
