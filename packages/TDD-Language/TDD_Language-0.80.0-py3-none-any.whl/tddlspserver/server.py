"""tddlspserver package."""

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
from .cst.calculate_complexity_visitor import CalculateComplexityVisitor
from .cst.cmake_file_generator_visitor import CMakeFileGeneratorVisitor
from .cst.f90_file_generator_visitor import F90FileGeneratorVisitor
from .cst.diagnostic_listener import DiagnosticListener
from .cst.pf_file_generator_visitor import PFFileGeneratorVisitor
from .cst.system_file_visitor import SystemFileVisitor
from .cst.symbol_table_visitor import SymbolTableVisitor
from .gen.python.TestSuite.TestSuiteLexer import TestSuiteLexer
from .gen.python.TestSuite.TestSuiteParser import TestSuiteParser
from .symboltable.symbol_table import MetricSymbol, ModuleSymbol, PathSymbol, RoutineSymbol, Symbol, VariableSymbol
from .utils.compute_token_index import CaretPosition, TokenPosition, compute_token_position
from .utils.suggest_variables import suggest_symbols
from .utils.tdd_errors_strategy import TDDErrorStrategy


class TDDLSPServer(LanguageServer):
    CMD_REGISTER_COMPLETIONS = "registerCompletions"
    CMD_UNREGISTER_COMPLETIONS = "unregisterCompletions"
    CMD_RECOMMEND_SUT_BLOCKING = "recommendSUT"

    CONFIGURATION_SECTION = "ODsl-TDD-DSL-Server"

    top_level_context = TestSuiteParser.Test_suiteContext
    parseTree: top_level_context
    # Recommendation metric
    sort_metric : str

    # Debug flag
    debug = False

    def __init__(self, *args):
        super().__init__(*args)
        # Set error listener
        self.error_listener: DiagnosticListener = DiagnosticListener()
        # Set empty input stream
        input_stream: InputStream = InputStream(str())

        # Set lexer
        self.lexer: TestSuiteLexer = TestSuiteLexer(input_stream)
        # Set error listener for diagnostics
        self.lexer.removeErrorListeners()
        self.lexer.addErrorListener(self.error_listener)

        # Set token stream pipe between lexer and parser
        self.token_stream: CommonTokenStream = CommonTokenStream(self.lexer)

        # Set parser
        self.parser: TestSuiteParser = TestSuiteParser(self.token_stream)
        # Set error listener for diagnostics
        self.parser.removeErrorListeners()
        self.parser.addErrorListener(self.error_listener)

        self.parser._errHandler=TDDErrorStrategy()

        # Attributes of generated files
        self.files: dict[str, Tuple[float, str, str]] = {}

        # Fxtran system file path
        self.fxtran_path = "fxtran"

        # Number of SuT to return
        self.show_n_metrics = 2


tdd_server = TDDLSPServer("pygls-odsl-tdd-prototype", "v0.8")

logger = logging.getLogger(__name__)


def _validate(params):

    # Get file content for lexer input stream
    text_doc: Document = tdd_server.workspace.get_text_document(params.text_document.uri)
    source: str = text_doc.source
    # Validate format if source is determined
    diagnostics: List[Diagnostic] = _validate_format(tdd_server, source) if source is not None else []
    # Return diagnostics
    tdd_server.publish_diagnostics(text_doc.uri, diagnostics)


def _validate_format(server: TDDLSPServer, source: str):
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
        top_level_context = TestSuiteParser.Test_suiteContext
        parse_tree: Optional[top_level_context] = server.parser.test_suite()

        if not tdd_server.token_stream.fetchedEOF:
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


@tdd_server.feature(TEXT_DOCUMENT_COMPLETION, CompletionOptions(trigger_characters=[","]))
def completions(params: Optional[CompletionParams] = None) -> CompletionList:
    """Returns completion items."""

    # Set input stream of characters for lexer
    text_doc: Document = tdd_server.workspace.get_text_document(params.text_document.uri)
    source: str = text_doc.source
    input_stream: InputStream = InputStream(source)

    # Reset the lexer/parser
    tdd_server.error_listener.reset()
    tdd_server.lexer.inputStream = input_stream
    tdd_server.token_stream = CommonTokenStream(tdd_server.lexer)
    tdd_server.parser.setTokenStream(tdd_server.token_stream)

    # Launches parser by invoking top-level rule
    top_level_context = TestSuiteParser.Test_suiteContext
    parse_tree: Optional[top_level_context] = None

    token_index: Optional[TokenPosition] = None

    # Parse until fetched
    while not tdd_server.token_stream.fetchedEOF:
        parse_tree = tdd_server.parser.test_suite()

        # Get token index under caret position
        # params.position.line + 1 as lsp line counts from 0 and antlr4 line counts from 1
        if token_index is None:
            token_index = compute_token_position(
                parse_tree, tdd_server.token_stream, CaretPosition(
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
    core: CodeCompletionCore = CodeCompletionCore(tdd_server.parser)

    core.ignoredTokens = {Token.EPSILON}
    core.preferredRules = {TestSuiteParser.RULE_reference, TestSuiteParser.RULE_src_path, TestSuiteParser.RULE_test_module}

    # Get completion candidates
    candidates: CandidatesCollection = core.collectCandidates(token_index.index)

    # Resolve candidates for preferred rules
    if len(candidates.rules) != 0:

        symbol_types: List[Symbol] = []

        if any(rule in candidates.rules for rule in [TestSuiteParser.RULE_reference]):

            symbol_table_visitor: SymbolTableVisitor = SymbolTableVisitor("completions", os.getcwd(), tdd_server.fxtran_path)
            symbol_table = symbol_table_visitor.visit(parse_tree)
            # FunctionSymbol is derived from RoutineSymbol
            symbol_types.extend([VariableSymbol, RoutineSymbol])

        elif any(rule in candidates.rules for rule in [TestSuiteParser.RULE_test_module]):

            symbol_table_visitor: SymbolTableVisitor = SymbolTableVisitor("completions", os.getcwd(), tdd_server.fxtran_path)
            symbol_table = symbol_table_visitor.visit(parse_tree)
            symbol_types.append(ModuleSymbol)

        elif any(rule in candidates.rules for rule in [TestSuiteParser.RULE_src_path]):

            symbol_table_visitor: SystemFileVisitor = SystemFileVisitor("paths", os.getcwd())
            symbol_table = symbol_table_visitor.visit(parse_tree)
            symbol_types.append(PathSymbol)

        symbols: List[str] = []
        for symbol_type in symbol_types:
            symbols.extend(suggest_symbols(symbol_table=symbol_table, position=token_index, symbol_type=symbol_type))

        for symbol in symbols:
            completion_list.items.append(CompletionItem(label=symbol))

    # TODO modules, type check, asserts, functions, subroutines

    # Add tokens to completion candidates
    # Strip ' from terminals
    stripped_literal_names: list = stripTerminals(elements=tdd_server.parser.literalNames, terminal="\'")
    symbolic_names: list = tdd_server.parser.symbolicNames
    for key, valueList in candidates.tokens.items():
        label = IntervalSet.elementName(IntervalSet, stripped_literal_names, symbolic_names, key)
        # Replace newline with os.newline token
        if label == "NEWLINE":
            label = os.linesep
        # Remove symbolic names or unknown tokens from completions
        if label == "<UNKNOWN>" or label in symbolic_names:
            label = None
        if label:
            completion_list.items.append(CompletionItem(label=label))

    if not completion_list.items:
        # VSCode empty list workaround
        completion_list.items.append(CompletionItem(label=""))
    if tdd_server.debug:
        for entry in completion_list.items:
            print(f"{entry}")
    # Return completion candidates labels
    return completion_list


def stripTerminals(elements: List[str] = None, terminal: str = "\'") -> List[str]:
    """
     Strip string terminals from list elements.

    :param elements: List of elements
    :return: List of striped elements
    """
    return [e.strip(terminal) for e in elements]


@tdd_server.feature(TEXT_DOCUMENT_DID_CHANGE)
def did_change(server: TDDLSPServer, params: DidChangeTextDocumentParams):
    """Text document did change notification."""
    server.parseTree = parse_document(params)
    _validate(params)


@tdd_server.feature(TEXT_DOCUMENT_DID_CLOSE)
def did_close(server: TDDLSPServer, params: DidCloseTextDocumentParams):
    """Text document did close notification."""
    server.show_message("Text Document Did Close")


@tdd_server.feature(TEXT_DOCUMENT_DID_SAVE)
def did_save(server: TDDLSPServer, params: DidSaveTextDocumentParams):
    """Text document did save notification."""

    # Get Path
    text_doc: Document = tdd_server.workspace.get_text_document(params.text_document.uri)
    file_path: str = os.path.abspath(text_doc.path)
    rel_file_path: str = os.path.relpath(file_path, os.getcwd())

    server.parseTree = parse_document(params)

    # Get symboltable for f90 generator
    symbol_table_visitor: SymbolTableVisitor = SymbolTableVisitor("variables", os.getcwd(), tdd_server.fxtran_path)
    symbol_table = symbol_table_visitor.visit(server.parseTree)

    # Generate pf files
    pf_file_generator_visitor: PFFileGeneratorVisitor = PFFileGeneratorVisitor(
        work_path=os.getcwd(), files=tdd_server.files, symbol_table=symbol_table, rel_file_path=rel_file_path)
    # write pf files and save generated files
    tdd_server.files = pf_file_generator_visitor.visit(server.parseTree)

    # Generate F90 files
    f90_file_generator_visitor: F90FileGeneratorVisitor = F90FileGeneratorVisitor(
        work_path=os.getcwd(), files=tdd_server.files, symbol_table=symbol_table, rel_file_path=rel_file_path)
    # update fortran file and save generated files
    tdd_server.files = f90_file_generator_visitor.visit(server.parseTree)

    # Generate CMake files
    cmake_file_generator_visitor: CMakeFileGeneratorVisitor = CMakeFileGeneratorVisitor(
        work_path=os.getcwd(), files=tdd_server.files, symbol_table=symbol_table
    )
    # update CMake files and save generated files
    tdd_server.files = cmake_file_generator_visitor.visit(server.parseTree)

    server.show_message("Text Document Did Save")


@tdd_server.feature(TEXT_DOCUMENT_DID_OPEN)
async def did_open(server: TDDLSPServer, params: DidOpenTextDocumentParams):
    """Text document did open notification."""
    server.show_message("Text Document Did Open")
    server.parseTree = parse_document(params)

    _validate(params)


def parse_document(params) -> TestSuiteParser.Test_suiteContext:
    # Set input stream of characters for lexer
    text_doc: Document = tdd_server.workspace.get_text_document(params.text_document.uri)
    source: str = text_doc.source
    input_stream: InputStream = InputStream(source)

    # Reset the lexer/parser
    tdd_server.error_listener.reset()
    tdd_server.lexer.inputStream = input_stream
    tdd_server.token_stream = CommonTokenStream(tdd_server.lexer)
    tdd_server.parser.setInputStream(tdd_server.token_stream)

    # Return launched parser by invoking top-level rule
    return tdd_server.parser.test_suite()


@tdd_server.feature(
    TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL, SemanticTokensLegend(token_types=["operator"], token_modifiers=[])
)
def semantic_tokens(server: TDDLSPServer, params: SemanticTokensParams):
    """See https://microsoft.github.io/language-server-protocol/specification#textDocument_semanticTokens
    for details on how semantic tokens are encoded."""

    TOKENS = re.compile("\".*\"(?=:)")

    uri = params.text_document.uri
    doc = server.workspace.get_document(uri)

    last_line = 0
    last_start = 0

    data = []

    for lineno, line in enumerate(doc.lines):
        last_start = 0

        for match in TOKENS.finditer(line):
            start, end = match.span()
            data += [(lineno - last_line), (start - last_start), (end - start), 0, 0]

            last_line = lineno
            last_start = start

    return SemanticTokens(data=data)


@tdd_server.command(TDDLSPServer.CMD_RECOMMEND_SUT_BLOCKING)
def recommend_SUT(server: TDDLSPServer, *args):
    """Calculates the complexity of the SuTs in the path and returns test recommendations."""

    calculate_complexity_visitor: CalculateComplexityVisitor = CalculateComplexityVisitor(
        name="paths", test_work_path=os.getcwd(), fxtran_path=tdd_server.fxtran_path, sort_metric=tdd_server.sort_metric)
    symbol_table = calculate_complexity_visitor.visit(server.parseTree)

    metric_list: List[str] = suggest_symbols(symbol_table, position=None, symbol_type=MetricSymbol)

    for metric in metric_list[:tdd_server.show_n_metrics]:
        server.show_message(metric)

    if tdd_server.debug:
        debug_file_write(os.path.join(os.getcwd(),tdd_server.sort_metric) , "\n".join(metric_list))

    server.show_message(f"Recommend SuT by {tdd_server.sort_metric}...")

def debug_file_write( file_path : str = None, content : str = None ):
    with open(file_path, mode="w", encoding="utf-8") as f:
        f.write(content)


@tdd_server.command(TDDLSPServer.CMD_REGISTER_COMPLETIONS)
async def register_completions(server: TDDLSPServer, *args):
    """Register completions method on the client."""
    params = RegistrationParams(
        registrations=[Registration(
            id=str(uuid.uuid4()), method=TEXT_DOCUMENT_COMPLETION, register_options={"triggerCharacters": ","}
        )]
    )
    response = await server.register_capability_async(params)
    if response is None:
        server.show_message("Successfully registered completions method")
    else:
        server.show_message("Error happened during completions registration.", MessageType.Error)


@tdd_server.command(TDDLSPServer.CMD_UNREGISTER_COMPLETIONS)
async def unregister_completions(server: TDDLSPServer, *args):
    """Unregister completions method on the client."""
    params = UnregistrationParams(
        unregisterations=[Unregistration(id=str(uuid.uuid4()), method=TEXT_DOCUMENT_COMPLETION)]
    )
    response = await server.unregister_capability_async(params)
    if response is None:
        server.show_message("Successfully unregistered completions method")
    else:
        server.show_message("Error happened during completions unregistration.", MessageType.Error)
