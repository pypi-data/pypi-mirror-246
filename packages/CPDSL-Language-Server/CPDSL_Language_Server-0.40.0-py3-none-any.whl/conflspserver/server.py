"""cpdslLSPServer package."""

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
from typing import List, Optional, Union

# antlr4
from antlr4 import CommonTokenStream, InputStream, Token
from antlr4.IntervalSet import IntervalSet


# antlr4-c3
from .cst.code_completion_core import CodeCompletionCore, CandidatesCollection

# pygls
from lsprotocol.types import (
    CompletionItem, CompletionItemKind, CompletionList, CompletionOptions, CompletionParams, Diagnostic, DidChangeTextDocumentParams, DidCloseTextDocumentParams,
    DidOpenTextDocumentParams, DidSaveTextDocumentParams, DocumentSymbol, DocumentSymbolParams, Location, MessageType, Position, Range, Registration, RegistrationParams, SemanticTokens, SemanticTokensLegend,
    SemanticTokensParams, SymbolInformation, TEXT_DOCUMENT_COMPLETION, TEXT_DOCUMENT_DID_CHANGE, TEXT_DOCUMENT_DID_CLOSE, TEXT_DOCUMENT_DID_OPEN, TEXT_DOCUMENT_DID_SAVE,
    TEXT_DOCUMENT_DOCUMENT_SYMBOL, TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL, Unregistration, UnregistrationParams
)
from pygls.server import LanguageServer
from pygls.workspace import Document

# user relative imports
from .utils.compute_token_index import compute_token_position, CaretPosition, TokenPosition
from .utils.suggest_variables import suggest_symbols
from .utils.conf_errors_strategy import CONFErrorStrategy

from .cst.symbol_table_visitor import SymbolTableVisitor
from .cst.diagnostic_listener import DiagnosticListener

from .gen.python.Configuration.ConfigurationLexer import ConfigurationLexer
from .gen.python.Configuration.ConfigurationParser import ConfigurationParser


from pygls.capabilities import get_capability

COUNT_DOWN_START_IN_SECONDS = 10
COUNT_DOWN_SLEEP_IN_SECONDS = 1


class confLSPServer( LanguageServer ):
    CMD_REGISTER_COMPLETIONS = 'registerCompletions'
    CMD_UNREGISTER_COMPLETIONS = 'unregisterCompletions'

    CONFIGURATION_SECTION = 'ODslCONFServer'

    def __init__(self, *args):
        super().__init__( *args )
        # set ErrorListener
        self.error_listener: DiagnosticListener = DiagnosticListener()
        # set empty input stream
        input_stream: InputStream = InputStream( str() )

        # set lexer
        self.lexer: ConfigurationLexer = ConfigurationLexer( input_stream )
        # set ErrorListener for diagnostics
        self.lexer.removeErrorListeners()
        self.lexer.addErrorListener( self.error_listener )

        # set token stream pipe between lexer and parser
        self.tokenStream: CommonTokenStream = CommonTokenStream( self.lexer )

        # set parser
        self.parser: ConfigurationParser = ConfigurationParser( self.tokenStream )
        # set ErrorListener for diagnostics
        self.parser.removeErrorListeners()
        self.parser.addErrorListener( self.error_listener )

        self.parser._errHandler=CONFErrorStrategy()

conf_server = confLSPServer( 'pygls-odsl-conf-prototype', 'v0.4' )

logger = logging.getLogger( __name__ )

def _validate(params):

    # Get file content for lexer input stream
    text_doc: Document = conf_server.workspace.get_text_document(params.text_document.uri)
    source: str = text_doc.source
    # Validate format if source is determined
    diagnostics: List[Diagnostic] = _validate_format(conf_server, source) if source is not None else []
    # Return diagnostics
    conf_server.publish_diagnostics(text_doc.uri, diagnostics)


def _validate_format(server: confLSPServer, source: str):
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
        top_level_context = ConfigurationParser.ConfigurationModelContext
        parse_tree: Optional[top_level_context] = server.parser.configurationModel()

        if not conf_server.token_stream.fetchedEOF:
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



@conf_server.feature( TEXT_DOCUMENT_COMPLETION, CompletionOptions( trigger_characters=[','] ) )
def completions(params: Optional[CompletionParams] = None) -> CompletionList:
    """Returns completion items."""

    # set input stream of characters for lexer
    text_doc: Document = conf_server.workspace.get_document( params.text_document.uri )
    source: str = text_doc.source
    input_stream: InputStream = InputStream( source )

    # reset the lexer/parser
    conf_server.error_listener.reset()
    conf_server.lexer.inputStream = input_stream
    conf_server.tokenStream = CommonTokenStream( conf_server.lexer )
    conf_server.parser.setInputStream( conf_server.tokenStream )


    # Launches parser by invoking top-level rule
    top_level_context = ConfigurationParser.ConfigurationModelContext
    parse_tree: Optional[top_level_context] = None

    token_index: Optional[TokenPosition] = None

    # Parse until fetched
    while not conf_server.token_stream.fetchedEOF:
        parse_tree = conf_server.parser.configurationModel()

        # Get token index under caret position
        # params.position.line + 1 as lsp line counts from 0 and antlr4 line counts from 1
        if token_index is None:
            token_index = compute_token_position(
                parse_tree, conf_server.token_stream, CaretPosition(
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
    core: CodeCompletionCore = CodeCompletionCore( conf_server.parser )

    core.ignoredTokens = {Token.EPSILON}
    core.preferredRules = {ConfigurationParser, ConfigurationParser}

    # get completion candidates
    candidates: CandidatesCollection = core.collectCandidates( token_index.index )

    calcVariables = False

    def calcLitAndSymbNames(literalNames):
        literalNames = []
        symbolic_names = []
        for i in literalNames:
            if i in conf_server.parser.literalNames:
                literalNames.append(i)
            else:
                symbolic_names.append(i)
        return (literalNames, symbolic_names)

    def addToCompletionList(literalNames):
        #get labels of completion candidates to return
        symbolic_names, literal_names = calcLitAndSymbNames(literalNames)
        for key, _ in candidates.tokens.items():
            completion_list.items.append(CompletionItem(
                label=IntervalSet.elementName(IntervalSet, literal_names,
                                           symbolic_names, key)))

    
    #TODO: Add Rules
    addToCompletionList(ConfigurationParser.literalNames)
    addToCompletionList(ConfigurationParser.symbolicNames)
    
    # Variables finding
    if any( rule in candidates.rules for rule in [ ConfigurationParser.configurationModel ] ):

        symbolTableVisitor: SymbolTableVisitor = SymbolTableVisitor( 'completions' )

        symbolTable = symbolTableVisitor.visit( parse_tree)

        variables = suggest_symbols( symbolTable, token_index )

        for variable in variables:
            completion_list.items.append( CompletionItem( label=variable, kind = CompletionItemKind.Variable ) )

    # return completion candidates labels
    return completion_list

def get_lsp_symbol_type(nameOfType : str):
    # predefine some module and function keywords
    #TODO: Edit for ConfigurationDSL
    module = ['include', 'configuration', 'group']
    function = ['feature', 'multiple', 'def', 'activate']
    # Define a regex pattern for literalNames of the parser
    # regex_pattern = DeclarationParser.literalNames
    # regex_pattern = '|'.join(regex_pattern)
    # regexReplaceChars = "()[]*/+."
    # ignoreToken = ["'", "<INVALID>|"]
    # for elem in ignoreToken:
    #     regex_pattern = regex_pattern.replace(elem, "")
    # for elem in regexReplaceChars:
    #     regex_pattern = regex_pattern.replace(elem, "\\" + elem)

    # TOKENS = re.compile(regex_pattern)

    if nameOfType in [x.replace("'", "") for x in ConfigurationParser.literalNames]:
        if nameOfType in module:
            return CompletionItemKind.Module
        if nameOfType in function:
            return CompletionItemKind.Function
        return CompletionItemKind.Keyword
    if nameOfType in ConfigurationParser.symbolicNames:
        return CompletionItemKind.Constructor
    if nameOfType.isdigit():
        return CompletionItemKind.Value
    return CompletionItemKind.Variable

def get_position_and_item_val(inp : str):
    from itertools import groupby

    ret_val = []

    for k, g in groupby(enumerate(inp), lambda x: not x[1].isspace() or x[1] in [",", ":"]):
        if k:
            pos, first_item = next(g)
            item = first_item + ''.join([x for _, x in g])
            ret_val.append([pos, pos + len(item) - 1, item])
    return ret_val


@conf_server.feature(TEXT_DOCUMENT_DOCUMENT_SYMBOL)
def document_symbol(
    server: confLSPServer, params: DocumentSymbolParams
) -> Optional[Union[List[DocumentSymbol], List[SymbolInformation]]]:
    # get the document
    uri = params.text_document.uri
    doc = server.workspace.get_document( uri )

    data = []

    #For capturing strings
    string_entity = False
    string_ident = ""
    start_string = (0,0) # tuple for (lineno, linepos)

    for lineno, line in enumerate( doc.lines ):
        for start, end, word in get_position_and_item_val(line):
            if str(word).startswith(("'", '"')):
                string_entity = True
                string_ident = word[0]
                if str(word).endswith(("'", '"')) and word[-1] == string_ident:
                    pos_range = Range(
                    start = Position(line=lineno, character=start),
                    end = Position(line=lineno, character=end) 
                    )
                    string_entity = False
                    data.append(SymbolInformation(
                        name = "STRING",
                        kind = CompletionItemKind.Text,
                        location = Location(uri=uri, range=pos_range)
                    ))
                start_string = (lineno, start)
            elif string_entity and str(word).endswith(("'", '"')) and word[-1] == string_ident:
                pos_range = Range(
                start = Position(line=start_string[0], character=start_string[1]),
                end = Position(line=lineno, character=end) 
                )
                string_entity = False
                data.append(SymbolInformation(
                    name = "STRING",
                    kind = CompletionItemKind.Text,
                    location = Location(uri=uri, range=pos_range)
                ))
            elif not string_entity:
                pos_range = Range(
                    start = Position(line=lineno, character=start),
                    end = Position(line=lineno, character=end) 
                )
                # for now its only covering keywords, no variables
                data.append(SymbolInformation(
                    name = word,
                    kind = get_lsp_symbol_type(word),
                    location = Location(uri=uri, range=pos_range)
                ))
                print("added SymbolItem:")
                print(str(word) + " " + str(get_lsp_symbol_type(word)))
            else:
                continue
    return data if data else None


@conf_server.feature( TEXT_DOCUMENT_DID_CHANGE )
def did_change(ls, params: DidChangeTextDocumentParams):
    """Text document did change notification."""
    _validate( ls, params )


@conf_server.feature( TEXT_DOCUMENT_DID_CLOSE )
def did_close(server: confLSPServer, params: DidCloseTextDocumentParams):
    """Text document did close notification."""
    server.show_message( 'Text Document Did Close' )


@conf_server.feature( TEXT_DOCUMENT_DID_SAVE )
def did_save(server: confLSPServer, params: DidSaveTextDocumentParams):
    """Text document did save notification."""

    # set input stream of characters for lexer
    text_doc: Document = conf_server.workspace.get_document( params.text_document.uri )
    source: str = text_doc.source
    input_stream: InputStream = InputStream( source )

    # reset the lexer/parser
    conf_server.error_listener.reset()
    conf_server.lexer.inputStream = input_stream
    conf_server.tokenStream = CommonTokenStream( conf_server.lexer )
    conf_server.parser.setInputStream( conf_server.tokenStream )

    Top_levelContext = ConfigurationParser.ConfigurationModelContext
    parseTree: Top_levelContext = conf_server.parser.configurationModel()

    # TODO

    server.show_message( 'Text Document Did Save' )


@conf_server.feature( TEXT_DOCUMENT_DID_OPEN )
async def did_open(ls, params: DidOpenTextDocumentParams):
    """Text document did open notification."""
    ls.show_message( 'Text Document Did Open' )
    _validate( ls, params )


@conf_server.feature( TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL,
                     SemanticTokensLegend( token_types=["operator"], token_modifiers=[] ) )
def semantic_tokens(ls: confLSPServer, params: SemanticTokensParams):
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

@conf_server.command( confLSPServer.CMD_REGISTER_COMPLETIONS )
async def register_completions(ls: confLSPServer, *args):
    """Register completions method on the client."""
    params = RegistrationParams( registrations=[Registration( id=str( uuid.uuid4() ), method=TEXT_DOCUMENT_COMPLETION,
                                                              register_options={"triggerCharacters": "[':']"} )] )
    response = await ls.register_capability_async( params )
    if response is None:
        ls.show_message( 'Successfully registered completions method' )
    else:
        ls.show_message( 'Error happened during completions registration.', MessageType.Error )


@conf_server.command( confLSPServer.CMD_UNREGISTER_COMPLETIONS )
async def unregister_completions(ls: confLSPServer, *args):
    """Unregister completions method on the client."""
    params = UnregistrationParams(
        unregisterations=[Unregistration( id=str( uuid.uuid4() ), method=TEXT_DOCUMENT_COMPLETION )] )
    response = await ls.unregister_capability_async( params )
    if response is None:
        ls.show_message( 'Successfully unregistered completions method' )
    else:
        ls.show_message( 'Error happened during completions unregistration.', MessageType.Error )
