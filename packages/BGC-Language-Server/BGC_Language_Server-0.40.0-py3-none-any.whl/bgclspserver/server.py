"""bgcLSPServer package."""

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
import logging
import re
import uuid
import os.path
from typing import List, Optional, Tuple

# antlr4
from antlr4 import CommonTokenStream, InputStream, Token
from antlr4.IntervalSet import IntervalSet

# pygls
from lsprotocol.types import (
    CompletionItem, CompletionList, CompletionOptions, CompletionParams, Diagnostic, DidChangeTextDocumentParams, DidCloseTextDocumentParams,
    DidOpenTextDocumentParams, DidSaveTextDocumentParams, MessageType, Position, Range, Registration, RegistrationParams, SemanticTokens, SemanticTokensLegend,
    SemanticTokensParams, TEXT_DOCUMENT_COMPLETION, TEXT_DOCUMENT_DID_CHANGE, TEXT_DOCUMENT_DID_CLOSE, TEXT_DOCUMENT_DID_OPEN, TEXT_DOCUMENT_DID_SAVE,
    TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL, Unregistration, UnregistrationParams
)
from pygls.server import LanguageServer
from pygls.workspace import Document

# antlr4-c3
from codeCompletionCore.CodeCompletionCore import CandidatesCollection, CodeCompletionCore

# user relative imports
from .utils.compute_token_index import compute_token_position, compute_token_index, CaretPosition, TokenPosition
from .utils.suggest_variables import suggest_symbols
from utils.bgc_errors_strategy import BGCErrorStrategy

from .cst.symbol_table_visitor import SymbolTableVisitor
from .cst.diagnostic_listener import DiagnosticListener

from .gen.python.BgcDsl.BgcDslLexer import BgcDslLexer
from .gen.python.BgcDsl.BgcDslParser import BgcDslParser
from .gen.python.BgcDsl.BgcDslVisitor import BgcDslVisitor

class bgcLSPServer( LanguageServer ):
    CMD_REGISTER_COMPLETIONS = 'registerCompletions'
    CMD_UNREGISTER_COMPLETIONS = 'unregisterCompletions'

    CONFIGURATION_SECTION = 'ODslBGCServer'

    def __init__(self, *args):
        super().__init__(*args)
        # Set error listener
        self.error_listener: DiagnosticListener = DiagnosticListener()
        # Set empty input stream
        input_stream: InputStream = InputStream(str())

        # Set lexer
        self.lexer: BgcDslLexer = BgcDslLexer(input_stream)
        # Set error listener for diagnostics
        self.lexer.removeErrorListeners()
        self.lexer.addErrorListener(self.error_listener)

        # Set token stream pipe between lexer and parser
        self.token_stream: CommonTokenStream = CommonTokenStream(self.lexer)

        # Set parser
        self.parser: BgcDslParser = BgcDslParser(self.token_stream)
        # Set error listener for diagnostics
        self.parser.removeErrorListeners()
        self.parser.addErrorListener(self.error_listener)

        self.parser._errHandler=BGCErrorStrategy()

bgc_server = bgcLSPServer( 'pygls-odsl-bgc-prototype', 'v0.4' )

logger = logging.getLogger( __name__ )

def _validate(params):

    # Get file content for lexer input stream
    text_doc: Document = bgc_server.workspace.get_text_document(params.text_document.uri)
    source: str = text_doc.source
    # Validate format if source is determined
    diagnostics: List[Diagnostic] = _validate_format(bgc_server, source) if source is not None else []
    # Return diagnostics
    bgc_server.publish_diagnostics(text_doc.uri, diagnostics)


def _validate_format(server: bgcLSPServer, source: str):
    """Validates file format."""

    # Get input stream of characters for lexer
    input_stream: InputStream = InputStream(source)

    # set the input stream and reset the lexer/parser/listener
    server.error_listener.reset()
    server.lexer.inputStream = input_stream
    server.token_stream = CommonTokenStream(server.lexer)
    server.parser.setInputStream(server.token_stream)

    try:
        # Launch parser by invoking top-level rule
        top_level_context = BgcDslParser.BgcModelContext
        parse_tree: Optional[top_level_context] = server.parser.bgcModel()

        if not bgc_server.token_stream.fetchedEOF:
            end: Position = Position(parse_tree.stop.line, parse_tree.stop.column)
            eof_range: Range = Range(start=end, end=end)
            eof_msg = Diagnostic(message="Parser stopped before end of file.", range=eof_range)
            server.error_listener.diagnostics.append(eof_msg)

    except OSError as err:
        msg = err.filename.msg

        server.error_listener.diagnostics.append(msg)

    # return diagnostics
    return server.error_listener.diagnostics


def get_symbol_name_at_position(uri, position):
    logger.info("uri: %s\n", uri, "position: %s\n", position)


def lookup_symbol(uri, name):
    logger.info("uri: %s\n", uri, "name: %s\n", name)


@bgc_server.feature( TEXT_DOCUMENT_COMPLETION, CompletionOptions( trigger_characters=[','] ) )
def completions(params: Optional[CompletionParams] = None) -> CompletionList:
    """Returns completion items."""

    # Set input stream of characters for lexer
    text_doc: Document = bgc_server.workspace.get_text_document(params.text_document.uri)
    source: str = text_doc.source
    input_stream: InputStream = InputStream(source)

    # Reset the lexer/parser
    bgc_server.error_listener.reset()
    bgc_server.lexer.inputStream = input_stream
    bgc_server.token_stream = CommonTokenStream(bgc_server.lexer)
    bgc_server.parser.setTokenStream(bgc_server.token_stream)

    # Launches parser by invoking top-level rule
    top_level_context = BgcDslParser.BgcModelContext
    parse_tree: Optional[top_level_context] = None

    token_index: Optional[TokenPosition] = None

    # Parse until fetched
    while not bgc_server.token_stream.fetchedEOF:
        parse_tree = bgc_server.parser.bgcModel()

        # Get token index under caret position
        # params.position.line + 1 as lsp line counts from 0 and antlr4 line counts from 1
        if token_index is None:
            token_index = compute_token_position(
                parse_tree, bgc_server.token_stream, CaretPosition(
                    params.position.line + 1, params.position.character
                )
            )

    # Init emtpy return list
    completion_list: CompletionList = CompletionList(is_incomplete=False, items=[])

    # Return if no index could be determined
    if token_index is None:
        # TODO add warning
        return completion_list

    # Launch c3 core with parser
    core: CodeCompletionCore = CodeCompletionCore(bgc_server.parser)

    core.ignoredTokens = {Token.EPSILON}
    core.preferredRules = {BgcDslParser, BgcDslParser}

    # get completion candidates
    candidates: CandidatesCollection = core.collectCandidates( token_index.index )

    # TODO add interesting rules
    if any( rule in candidates.rules for rule in [None] ):

        symbolTableVisitor: SymbolTableVisitor = SymbolTableVisitor( 'completions' )

        symbolTable = symbolTableVisitor.visit( parse_tree )

        variables = suggest_symbols( symbolTable, token_index )

        for variable in variables:
            completion_list.items.append( CompletionItem( label=variable ) )

    # get labels of completion candidates to return
    labels_list: List[str] = []
    for key, valueList in candidates.tokens.items():
        completion_list.items.append( CompletionItem(
            label=IntervalSet.elementName( IntervalSet, bgc_server.parser.literalNames,
                                           bgc_server.parser.symbolicNames, key ) ) )

    # return completion candidates labels
    return completion_list


@bgc_server.feature( TEXT_DOCUMENT_DID_CHANGE )
def did_change(ls, params: DidChangeTextDocumentParams):
    """Text document did change notification."""
    _validate( ls, params )


@bgc_server.feature( TEXT_DOCUMENT_DID_CLOSE )
def did_close(server: bgcLSPServer, params: DidCloseTextDocumentParams):
    """Text document did close notification."""
    server.show_message( 'Text Document Did Close' )


@bgc_server.feature( TEXT_DOCUMENT_DID_SAVE )
def did_save(server: bgcLSPServer, params: DidSaveTextDocumentParams):
    """Text document did save notification."""

    # set input stream of characters for lexer
    text_doc: Document = bgc_server.workspace.get_document( params.text_document.uri )
    source: str = text_doc.source
    input_stream: InputStream = InputStream( source )

    # reset the lexer/parser
    bgc_server.error_listener.reset()
    bgc_server.lexer.inputStream = input_stream
    bgc_server.tokenStream = CommonTokenStream( bgc_server.lexer )
    bgc_server.parser.setInputStream( bgc_server.tokenStream )

    Top_levelContext = BgcDslParser.BgcModelContext
    parse_tree: Top_levelContext = bgc_server.parser.bgcModel()

    # TODO

    server.show_message( 'Text Document Did Save' )


@bgc_server.feature( TEXT_DOCUMENT_DID_OPEN )
async def did_open(ls, params: DidOpenTextDocumentParams):
    """Text document did open notification."""
    ls.show_message( 'Text Document Did Open' )
    _validate( ls, params )


@bgc_server.feature( TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL,
                     SemanticTokensLegend( token_types=["operator"], token_modifiers=[] ) )
def semantic_tokens(ls: bgcLSPServer, params: SemanticTokensParams):
    """See https://microsoft.github.io/language-server-protocol/specification#textDocument_semanticTokens
    for details on how semantic tokens are encoded."""

    TOKENS = re.compile( '".*"(?=:)' )

    uri = params.text_document.uri
    doc = ls.workspace.get_document( uri )

    last_line = 0
    last_start = 0

    data = []

    for lineno, line in enumerate( doc.lines ):
        last_start = 0

        for match in TOKENS.finditer( line ):
            start, end = match.span()
            data += [(lineno - last_line), (start - last_start), (end - start), 0, 0]

            last_line = lineno
            last_start = start

    return SemanticTokens( data=data )

@bgc_server.command( bgcLSPServer.CMD_REGISTER_COMPLETIONS )
async def register_completions(ls: bgcLSPServer, *args):
    """Register completions method on the client."""
    params = RegistrationParams( registrations=[Registration( id=str( uuid.uuid4() ), method=TEXT_DOCUMENT_COMPLETION,
                                                              register_options={"triggerCharacters": "[':']"} )] )
    response = await ls.register_capability_async( params )
    if response is None:
        ls.show_message( 'Successfully registered completions method' )
    else:
        ls.show_message( 'Error happened during completions registration.', MessageType.Error )


@bgc_server.command( bgcLSPServer.CMD_UNREGISTER_COMPLETIONS )
async def unregister_completions(ls: bgcLSPServer, *args):
    """Unregister completions method on the client."""
    params = UnregistrationParams(
        unregisterations=[Unregistration( id=str( uuid.uuid4() ), method=TEXT_DOCUMENT_COMPLETION )] )
    response = await ls.unregister_capability_async( params )
    if response is None:
        ls.show_message( 'Successfully unregistered completions method' )
    else:
        ls.show_message( 'Error happened during completions unregistration.', MessageType.Error )
