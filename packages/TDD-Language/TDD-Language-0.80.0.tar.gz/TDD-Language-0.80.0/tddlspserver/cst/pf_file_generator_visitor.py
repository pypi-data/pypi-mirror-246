"""FileGeneratorVisitor module for pFunit pf files."""

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

# util
import os
from typing import Dict, List, Tuple

# jinja2
from jinja2 import Environment, FileSystemLoader

# user relative imports
from ..symboltable.symbol_table import SymbolTable
from ..filewriter.file_writer import write_file
from ..gen.python.TestSuite.TestSuiteParser import TestSuiteParser
from ..gen.python.TestSuite.TestSuiteVisitor import TestSuiteVisitor
from ..utils.suggest_variables import get_scope


class PFFileGeneratorVisitor(TestSuiteVisitor):
    file_templates: Dict[int, str]
    template_path: str
    test_folder: str
    test_file_predicate: str
    environment: Environment
    file_suffix: str
    found_ref: bool
    found_par: bool
    symbol_table: SymbolTable

    # TODO hc
    def __init__(
            self, template_path: str = "tdd-dsl/tddlspserver/filewriter/jinjatemplates/pf", files: Dict[str, Tuple[float, str, str]] = {},
            symbol_table: SymbolTable = None, work_path: str = "tdd-dsl/output", test_folder: str = "tests", file_suffix: str = "pf", rel_file_path=None
    ):
        """
        pfUnit test file generator. Builds template file dictionary from TestSuiteParser.ruleNames.

        Write/merge pFUnit-file to :work_path:/:test_folder:/:filename:.pf

        :param rel_file_path: rel path to source file
        :param template_path: absolute filepath for jinja templates
        :param work_path: path to generate test suite
        :param test_folder: relative path under :testWorkPath: to save pfUnit tests
        """
        super().__init__()

        self.overwrite = False
        self.overwrite_files: List[str] = []
        self.files: dict[str, Tuple[float, str, str]] = files

        self.symbol_table = symbol_table

        self.template_path = template_path
        self.rel_file_path = rel_file_path
        self.work_path = work_path
        self.cwd = work_path
        # TODO add test directory option
        self.test_folder = test_folder
        self.file_suffix = file_suffix

        # Load Jinja2 templates
        self.environment = Environment(loader=FileSystemLoader(template_path), trim_blocks=True, lstrip_blocks=True, keep_trailing_newline=False)

        # variable flags
        self.found_ref = False
        self.found_par = False

        self.file_templates = {}
        # Get template file names from grammar
        i: int = 0
        for rule in TestSuiteParser.ruleNames:
            self.file_templates[i] = f"{rule}_template.txt"
            i += 1

    # Visit a parse tree produced by TestSuiteParser#test_suite.
    def visitTest_suite(self, ctx:TestSuiteParser.Test_suiteContext):
        self.visitChildren(ctx)
        return self.files

    # Visit a parse tree produced by TestSuiteParser#test_case.
    def visitTest_case(self, ctx: TestSuiteParser.Test_caseContext) -> dict[str, Tuple[float, str, str]]:

        # Load Jinja2 template
        template = self.environment.get_template(self.file_templates[ctx.getRuleIndex()])
        # Render template
        name = ctx.name.text
        scope = self.visit(ctx.modules) if ctx.modules else None
        vars_ = self.visit(ctx.vars_) if ctx.vars_ else None
        assertions = []
        for assertion in ctx.assertions:
            assertions.append(self.visit(assertion))
        content = template.render(name=name, scope=scope, vars_=vars_, assertions=assertions)

        # Check test flags. E.g. overwrite flag
        self.overwrite = False
        if ctx.test_flags:
            self.visit(ctx.test_flags)
        # Get user path
        self.visit(ctx.src_path())
        # Write pf file
        abs_path: str = os.path.join(self.work_path, self.test_folder, f"{name}.{self.file_suffix}")
        file_attr = self.files.get(abs_path) # TODO None
        if self.overwrite:
            # Merge all files that should overwrite other files
            if abs_path in self.overwrite_files:
                self.overwrite = False
            else:
                self.overwrite_files.append(abs_path)
        self.files[abs_path] = write_file(abs_path, content, file_attr, insert=not self.overwrite)

        # Update test case symbol
        test_case_symbol = get_scope(ctx, self.symbol_table)
        if test_case_symbol:
            test_case_symbol.test_file_path = abs_path
        # TODO else error

        # Return list of generated files
        return self.files

    # Visit a parse tree produced by TestSuiteParser#src_path.
    def visitSrc_path(self, ctx: TestSuiteParser.Src_pathContext):
        # Strip string terminals
        user_path: str = ctx.path.text.strip("\'")
        # TODO document
        # If the given path is an absolute path, then self.testPath is ignored and the joining is only the given path
        self.work_path = os.path.join(self.cwd, user_path)

    # Get rendered list of used modules
    def visitUse_modules(self, ctx: TestSuiteParser.Use_modulesContext):
        template = self.environment.get_template(self.file_templates[ctx.getRuleIndex()])
        return template.render(modules=ctx.modules)

    # Visit a parse tree produced by TestSuiteParser#test_vars.
    def visitTest_vars(self, ctx: TestSuiteParser.Test_varsContext):
        template = self.environment.get_template(self.file_templates[ctx.getRuleIndex()])

        parm = []
        decl = []
        vars = []
        for var in ctx.vars_:
            templates: List[str] = self.visit(var)
            # Is the variable initialized with a reference?
            match (self.found_par, self.found_ref):
                case [True, _]:
                    # Add parameter to top of declaration
                    parm.append(templates[0])
                case [_, False]:
                    # Append declaration with constant expression as normal
                    vars.append(templates[0])
                case [False, True]:
                    # Split declaration and initialization separately
                    vars.append(templates[0])
                    decl.append(templates[1])

                    # Reset found flags
                    self.found_ref = False
                    self.found_par = False
                case _:
                    # TODO error
                    pass

        # set declaration list to None if empty
        # decl = decl if decl else None

        return template.render(parm=parm, decl=decl, vars=vars)

    # Visit a parse tree produced by TestSuiteParser#test_vars.
    def visitTest_var(self, ctx: TestSuiteParser.Test_varContext):
        template = self.environment.get_template(self.file_templates[ctx.getRuleIndex()])
        comment = self.visit(ctx.optionalDesc())

        # reset foundPar flag for left side
        self.found_par = False
        decl = self.visit(ctx.varDeclaration())
        name = ctx.decl.name.text

        self.found_ref = False
        # reset foundRef flag for right side
        value = self.visit(ctx.expr())

        templates: List[str] = []

        # TODO deprecated
        # if self.foundRef:
        #     templates.extend( [ decl, template.render( decl = None, name = name, value = value, comment = comment ) ] )
        # else:
        #     templates.extend( [ None, template.render( decl = decl, name = None, value = value, comment = comment ) ] )

        match (self.found_par, self.found_ref):
            case [True, _] | [_, False]:
                # TODO put parameters at the top
                # Found Parameter no reference on right side: Add declaration with constant expression
                templates.extend([template.render(decl=decl, name=None, value=value, comment=comment), None])
            case [False, True]:
                # Found reference on right side: Separate declaration and initialization
                templates.extend([template.render(decl=None, name=name, value=value, comment=comment), decl])
            case _:
                # TODO error
                pass

        return templates

    # Visit a parse tree produced by TestSuiteParser#varDeclaration.
    def visitVarDeclaration(self, ctx: TestSuiteParser.VarDeclarationContext):
        template = self.environment.get_template(self.file_templates[ctx.getRuleIndex()])
        name = ctx.ID().getText()
        type = self.visit(ctx.type_)
        keys = []
        for key in ctx.keys:
            # TODO check for parameter
            key_text: str = key.keyword.text
            # flag parameter
            if key_text.lower() == "parameter":
                self.found_par = True
            keys.append(key_text)
        # match keys:
        #     case []:
        #         return template.render( name=name, type=type )
        #     case _:
        #         return template.render( name=name, type=type, keys=keys )

        return template.render(name=name, type=type, keys=keys)

        # if keys:  #     return template.render( name = name, type = type, keys = keys )  # else:  #     return template.render( name = name, type = type )

    # Visit a parse tree produced by TestSuiteParser#funRef.
    def visitFunRef(self, ctx: TestSuiteParser.FunRefContext):
        self.found_ref = True
        template = self.environment.get_template(self.file_templates[ctx.getRuleIndex()])
        name = ctx.ID().getText()
        args = []
        for arg in ctx.args:
            args.append(self.visit(arg))
        return template.render(name=name, args=args)

    # Visit a parse tree produced by TestSuiteParser#varRef.
    def visitVarRef(self, ctx: TestSuiteParser.VarRefContext):
        self.found_ref = True
        template = self.environment.get_template(self.file_templates[ctx.getRuleIndex()])
        name = ctx.ID().getText()
        return template.render(name=name)

    # Visit a parse tree produced by TestSuiteParser#enm.
    def visitEnm(self, ctx: TestSuiteParser.EnmContext):
        # TODO type ENUM
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TestSuiteParser#array.
    def visitArray(self, ctx: TestSuiteParser.ArrayContext):
        # TODO type ARRAY
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TestSuiteParser#parensExpr.
    def visitParensExpr(self, ctx: TestSuiteParser.ParensExprContext):
        template = self.environment.get_template(self.file_templates[ctx.getRuleIndex()])
        inner = self.visit(ctx.inner)
        return template.render(inner=inner)

    # Visit a parse tree produced by TestSuiteParser#mulDivExpr.
    def visitMulDivExpr(self, ctx: TestSuiteParser.MulDivExprContext):
        template = self.environment.get_template(self.file_templates[ctx.getRuleIndex()])
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)
        op = ctx.op.text
        return template.render(left=left, right=right, op=op)

    # Visit a parse tree produced by TestSuiteParser#addSubExpr.
    def visitAddSubExpr(self, ctx: TestSuiteParser.AddSubExprContext):
        template = self.environment.get_template(self.file_templates[ctx.getRuleIndex()])
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)
        op = ctx.op.text
        return template.render(left=left, right=right, op=op)

    # Visit a parse tree produced by TestSuiteParser#signExpr.
    def visitSignExpr(self, ctx: TestSuiteParser.SignExprContext):
        template = self.environment.get_template(self.file_templates[ctx.getRuleIndex()])
        inner = self.visit(ctx.inner)
        op = ctx.op.text
        return template.render(inner=inner, op=op)

    # Visit a parse tree produced by TestSuiteParser#numberExpr.
    def visitNumberExpr(self, ctx: TestSuiteParser.NumberExprContext):
        template = self.environment.get_template(self.file_templates[ctx.getRuleIndex()])
        value = ctx.value.text
        return template.render(value=value)

    # Visit a parse tree produced by TestSuiteParser#strExpr.
    def visitStrExpr(self, ctx: TestSuiteParser.StrExprContext):
        template = self.environment.get_template(self.file_templates[ctx.getRuleIndex()])
        value = ctx.value.text
        return template.render(value=value)

    # Visit a parse tree produced by TestSuiteParser#intExpr.
    def visitIntExpr(self, ctx: TestSuiteParser.IntExprContext):
        template = self.environment.get_template(self.file_templates[ctx.getRuleIndex()])
        value = ctx.value.text
        return template.render(value=value)

    # Visit a parse tree produced by TestSuiteParser#refExpr.
    def visitRefExpr(self, ctx: TestSuiteParser.RefExprContext):
        template = self.environment.get_template(self.file_templates[ctx.getRuleIndex()])
        value = self.visit(ctx.value)
        return template.render(value=value)

    # Visit a parse tree produced by TestSuiteParser#emptyDesc.
    def visitEmptyDesc(self, ctx: TestSuiteParser.EmptyDescContext):
        return None

    # Visit a parse tree produced by TestSuiteParser#specDesc.
    def visitSpecDesc(self, ctx: TestSuiteParser.SpecDescContext):
        template = self.environment.get_template(self.file_templates[ctx.getRuleIndex()])
        type = self.visit(ctx.value)
        comment = self.visit(ctx.value)
        return template.render(type=type, comment=comment)

    # Visit a parse tree produced by TestSuiteParser#emptyComment.
    def visitEmptyComment(self, ctx: TestSuiteParser.EmptyCommentContext):
        return None

    # Visit a parse tree produced by TestSuiteParser#specComment.
    def visitSpecComment(self, ctx: TestSuiteParser.SpecCommentContext):
        template = self.environment.get_template(self.file_templates[ctx.getRuleIndex()])
        comment = ctx.comment.text
        return template.render(comment=comment)

    # Visit a parse tree produced by TestSuiteParser#test_assertion.
    def visitTest_assertion(self, ctx: TestSuiteParser.Test_assertionContext):
        template = self.environment.get_template(self.file_templates[ctx.getRuleIndex()])
        directive = self.visit(ctx.directive)
        input_ = self.visit(ctx.input_)
        output = self.visit(ctx.output)
        pub_attributes = self.visit(ctx.attr)
        # Remove leading whitespaces and hashtags as well as trailing linebreaks
        comment = ctx.comment.text.rstrip("\n").lstrip("# ") if ctx.comment is not None else None

        # Extract assertion line start/end
        start_stop: str
        if ctx.start is not None and ctx.stop is not None:
            start: str = "".join([str(ctx.start.line), ":", str(ctx.start.column)])
            stop: str = "".join([str(ctx.stop.line), ":", str(ctx.stop.column)])
            start_stop = "-".join([start, stop])
        else:
            start_stop = None

        tag_source: str = ", ".join([self.rel_file_path, start_stop]) if self.rel_file_path is not None and start_stop is not None else None
        tag: str = "auto-generated, src: " + tag_source if tag_source is not None else "auto-generated, src: unknown"

        # Render template
        return template.render(directive=directive, input_=input_, output=output, pub_attributes=pub_attributes, comment=comment, tag=tag)

    # Visit a parse tree produced by TestSuiteParser#test_directive.
    def visitTest_directive(self, ctx: TestSuiteParser.Test_directiveContext):
        template = self.environment.get_template(self.file_templates[ctx.getRuleIndex()])
        pp_directive = ctx.ppDirective.text
        return template.render(ppDirective=pp_directive)

    # Visit a parse tree produced by TestSuiteParser#test_parameter.
    def visitTest_parameter(self, ctx: TestSuiteParser.Test_parameterContext):
        template = self.environment.get_template(self.file_templates[ctx.getRuleIndex()])
        # TODO use decl and comment in upper template
        value = self.visit(ctx.value)
        return template.render(value=value)

    # Visit a parse tree produced by TestSuiteParser#pubAttributes.
    def visitPubAttributes(self, ctx: TestSuiteParser.PubAttributesContext):
        template = self.environment.get_template(self.file_templates[ctx.getRuleIndex()])
        msg = ctx.msg.text if ctx.msg is not None else None
        tol = self.visit(ctx.tol) if ctx.tol is not None else None
        match (msg, tol):
            case [None, None]:
                return None
            case [None, _]:
                return template.render(tol=tol)
            case [_, None]:
                return template.render(msg=msg)
            case _:
                return template.render(msg=msg, tol=tol)

    # Visit a parse tree produced by TestSuiteParser#overwritePF.
    def visitOverwritePF(self, ctx: TestSuiteParser.OverwritePFContext):
        self.overwrite = True

    def writefile(self, path=None, filename=None):
        path = os.path.join(os.getcwd(), path, filename)
        if not os.path.exists(path):
            # Write rendered and optional merged content to file
            with open(path, mode="w", encoding="utf-8") as f:
                f.write()
                # TODO add to debug info
                print(f"... wrote {path}")
