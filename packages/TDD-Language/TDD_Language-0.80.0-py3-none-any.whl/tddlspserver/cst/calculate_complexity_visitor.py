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
import re
# util imports
from typing import Callable, Generic

# antlr4
from antlr4.tree.Tree import ParseTree

# user relative imports
from ..fxca.util.fxtran_utils import get_files, write_decorate_src_xml
from ..gen.python.TestSuite.TestSuiteParser import TestSuiteParser
from ..gen.python.TestSuite.TestSuiteVisitor import TestSuiteVisitor
from ..utils.calculate_complexity import calculate_metrics
from ..symboltable.symbol_table import MetricSymbol, SymbolTable, PathSymbol, SymbolTableOptions, P, T, TestCaseSymbol


class CalculateComplexityVisitor(TestSuiteVisitor, Generic[T]):
    _symbol_table: SymbolTable
    _test_path: str

    def __init__(self, name: str = "", test_work_path: str = "tdd-dsl/output", fxtran_path: str = "fxtran", sort_metric=None):
        super().__init__()
        self.sort_metric = sort_metric
        self.fxtran_path = fxtran_path
        self._symbol_table = SymbolTable(name, SymbolTableOptions(False))
        self._scope = None
        self._test_work_path = test_work_path
        self._test_path = ""

    @property
    def work_path(self) -> str:
        return self._test_work_path

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

        # TODO document
        # Update source directory
        # If the given path is an absolute path, then self._testPath is ignored and the joining is only the given path
        self._test_path: str = os.path.join(self._test_work_path, user_path)

        # TODO hc
        xml_path = os.path.join(self._test_path, "tmp")
        # Write XML files
        write_decorate_src_xml(self._test_path, xml_path, fxtran_path=self.fxtran_path)

        # Get Fortran files
        xml_files = get_files(xml_path, "*.[fF]90.xml")

        for path, filename in xml_files:
            src_filename: str = filename.rsplit(".", 1)[0]
            rel_path = os.path.relpath(path, xml_path)
            if rel_path != ".":
                # Relative path exists
                src_path: str = os.path.join(self._test_path, rel_path, src_filename)
            else:
                # Relative path is current dir and omitted
                src_path: str = os.path.join(self._test_path, src_filename)
            scope_elements = calculate_metrics(xml_path=os.path.join(path, filename), src=src_path, sort_metric=self.sort_metric)

            for scope_name, scope in scope_elements.items():
                if scope.is_testable:
                    self._symbol_table.add_new_symbol_of_type(MetricSymbol, self._scope, scope_name, scope)

    def with_scope(self, tree: ParseTree, t: type, action: Callable, *my_args: P.args or None, **my_kwargs: P.kwargs or None) -> T:
        scope = self._symbol_table.add_new_symbol_of_type(t, self._scope, *my_args, **my_kwargs)
        scope.context = tree
        self._scope = scope
        try:
            return action()
        finally:
            self._scope = scope.parent()
