"""computeTokenIndex module."""

__author__ = "sgu"

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

# utils
import asyncio
import threading
from typing import List, ParamSpec, Type

# antlr4
from antlr4 import ParserRuleContext

# user relative imports
from ..symboltable.symbol_table import MetricSymbol, ModuleSymbol, PathSymbol, RoutineSymbol, SymbolTable, Symbol, ScopedSymbol, VariableSymbol
from .compute_token_index import TokenPosition

from ..gen.python.TestSuite.TestSuiteParser import TestSuiteParser
Top_levelContext = TestSuiteParser.Test_suiteContext
del TestSuiteParser

P = ParamSpec("P")


class RunThread(threading.Thread):
    def __init__(self, func, *args: P.args or None, **kwargs: P.kwargs or None):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.result = None
        super().__init__()

    def run(self):
        self.result = asyncio.run(self.func(*self.args, **self.kwargs))


def run_async(func, *args: P.args or None, **kwargs: P.kwargs or None):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:  # RuntimeError: There is no current event loop...
        loop = None
    if loop and loop.is_running():
        thread = RunThread(func, *args, **kwargs)
        thread.start()
        thread.join()
        return thread.result

        # print("Async event loop already running. Adding coroutine to the event loop.")
        # tsk = loop.create_task(symbolTable.symbolWithContext( context ))
        # ^-- https://docs.python.org/3/library/asyncio-task.html#task-object
        # Optionally, a callback function can be executed when the coroutine completes
        # tsk.add_done_callback( lambda t: print(f"Task done with result={t.result()}  << return val of main()"))
    else:
        return asyncio.run(func(*args, **kwargs))


def get_scope(context: ParserRuleContext, symbolTable: SymbolTable):
    if context is None:
        return None

    scope = run_async(symbolTable.symbol_with_context, context)

    if scope is not None:
        return scope
    else:
        return get_scope(context.parentCtx, symbolTable)


def get_all_symbols_of_type(scope: ScopedSymbol, symbol_type: type):
    symbols: List[Symbol] = run_async(scope.get_symbols_of_type, symbol_type, False)
    parent = scope.parent()
    broken_chain: bool = False
    while parent is not None and not isinstance(parent, ScopedSymbol):
        parent = parent.parent()
        broken_chain = True
    if parent is not None and broken_chain:
        symbols.extend(get_all_symbols_of_type(parent, symbol_type))
    return symbols


def suggest_symbols(symbol_table: SymbolTable, position: TokenPosition, symbol_type: Type = VariableSymbol) -> List[str]:
    if position:
        context = position.context
        scope = get_scope(context, symbol_table)
        symbols: List[Symbol]
        if isinstance(scope, ScopedSymbol):  # Local scope
            symbols = get_all_symbols_of_type(scope, symbol_type)
        else:  # Global scope
            symbols = run_async(symbol_table.get_symbols_of_type, symbol_type, False)

        text: str = position.text

        # TODO deprecated if not in preferred rule
        # variable = position.context
        # while not isinstance( variable, Top_levelContext ) and variable.parentCtx is not None:
        #     variable = variable.parentCtx
        #
        # return filterSymbols( position.text if variable is not None else "", symbols, symbolType )
    else:
        symbols = run_async(symbol_table.get_nested_symbols_of_type, symbol_type)
        text = ""
    return filter_symbols(text, symbols, symbol_type)


def filter_symbols(text: str, symbols: List[Symbol], symbol_type: Type = VariableSymbol) -> List[str]:
    match symbol_type:
        case symbol_type if issubclass(symbol_type, PathSymbol):
            candidates = list(map(lambda s: s.value, symbols))

            return candidates

        case symbol_type if issubclass(symbol_type, MetricSymbol):
            scopes: List = list(map(lambda s: s.value, symbols))
            # TODO recommendation order: False - low first, high last; True - high first, low last
            scopes.sort(reverse=False)
            candidates: List[str] = list(map(lambda scope: str(scope), scopes))

            return candidates

        case symbol_type if any(map(lambda sType: issubclass(symbol_type, sType), [VariableSymbol, ModuleSymbol, RoutineSymbol])):
            candidates = list(map(lambda s: s.name, symbols))
            if len(text.strip()) == 0:
                return candidates
            else:
                return list(filter(lambda c: c.lower().startswith(text), candidates))

        case _:
            return []
