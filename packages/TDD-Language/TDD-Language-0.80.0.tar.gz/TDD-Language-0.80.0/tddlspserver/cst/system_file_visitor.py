"""Visitor extracting system file information from the cst"""

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

import os
# util imports
from typing import Callable, Generic

# antlr4
from antlr4.tree.Tree import ParseTree

# user relative imports
from ..fxca.util.fxtran_utils import get_subdirectories_gen
from ..gen.python.TestSuite.TestSuiteParser import TestSuiteParser
from ..gen.python.TestSuite.TestSuiteVisitor import TestSuiteVisitor
from ..symboltable.symbol_table import SymbolTable, PathSymbol, SymbolTableOptions, P, T, TestCaseSymbol


class SystemFileVisitor(TestSuiteVisitor, Generic[T]):
    _symbol_table: SymbolTable
    _test_path: str

    def __init__(self, name: str = "", test_work_path: str = "tdd-dsl/output", get_sub_directories: bool = True):
        super().__init__()
        self._symbol_table = SymbolTable(name, SymbolTableOptions(False))
        self._scope = None
        self._test_path = test_work_path
        self.get_sub_directories: bool = get_sub_directories

    @property
    def test_path(self) -> str:
        return self._test_path

    # Visit a parse tree produced by TestSuiteParser#test_suite.
    def visitTest_suite(self, ctx:TestSuiteParser.Test_suiteContext):
        self.visitChildren(ctx)
        return self._symbol_table

    # Visit a parse tree produced by TestSuiteParser#test_case.
    def visitTest_case(self, ctx: TestSuiteParser.Test_caseContext):
        return self.with_scope(ctx, TestCaseSymbol, lambda: self.visitChildren(ctx), ctx.ID().getText())

    # Return subdirectories under working path or user entered path
    def visitSrc_path(self, ctx: TestSuiteParser.Src_pathContext):
        # Strip string terminals
        user_path: str = ctx.path.text.strip("\'") if ctx.path else ''
        # candidates = list( map( lambda c: f"{os.sep}{c}" , candidates ) )

        # Remove incomplete basename from path
        if not user_path.endswith(os.sep):
            user_path = user_path.rpartition("/")[0]

        # TODO document
        # Update source directory
        # If the given path is an absolute path, then self._testPath is ignored and the joining is only the given path
        self._test_path: str = os.path.join(self._test_path, user_path)

        if self.get_sub_directories:

            # TODO document
            # get direct subdirectories without following symlinks or directories starting with "."
            sub_directories = get_subdirectories_gen(self._test_path, False, False)

            # Add subdirectories under current scope to symboltable
            for sub_directory in sub_directories:
                # Filter subdirectory path to be relative to user path
                rel_sub_user_path = os.path.relpath(sub_directory.path, user_path)
                self._symbol_table.add_new_symbol_of_type(PathSymbol, self._scope, sub_directory.name, rel_sub_user_path)

        else:
            self._symbol_table.add_new_symbol_of_type(PathSymbol, self._scope, "user_path", self._test_path)

    def with_scope(self, tree: ParseTree, t: type, action: Callable, *my_args: P.args or None, **my_kwargs: P.kwargs or None) -> T:
        scope = self._symbol_table.add_new_symbol_of_type(t, self._scope, *my_args, **my_kwargs)
        scope.context = tree
        self._scope = scope
        try:
            return action()
        finally:
            self._scope = scope.parent()
