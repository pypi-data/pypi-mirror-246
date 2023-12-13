# Generated from TestSuite.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .TestSuiteParser import TestSuiteParser
else:
    from TestSuiteParser import TestSuiteParser

# This class defines a complete generic visitor for a parse tree produced by TestSuiteParser.

class TestSuiteVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by TestSuiteParser#test_suite.
    def visitTest_suite(self, ctx:TestSuiteParser.Test_suiteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#test_case.
    def visitTest_case(self, ctx:TestSuiteParser.Test_caseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#test_flag.
    def visitTest_flag(self, ctx:TestSuiteParser.Test_flagContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#overwritePF.
    def visitOverwritePF(self, ctx:TestSuiteParser.OverwritePFContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#overwriteCMake.
    def visitOverwriteCMake(self, ctx:TestSuiteParser.OverwriteCMakeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#overwriteF90.
    def visitOverwriteF90(self, ctx:TestSuiteParser.OverwriteF90Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#src_path.
    def visitSrc_path(self, ctx:TestSuiteParser.Src_pathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#test_vars.
    def visitTest_vars(self, ctx:TestSuiteParser.Test_varsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#test_var.
    def visitTest_var(self, ctx:TestSuiteParser.Test_varContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#varDeclaration.
    def visitVarDeclaration(self, ctx:TestSuiteParser.VarDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#use_modules.
    def visitUse_modules(self, ctx:TestSuiteParser.Use_modulesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#test_module.
    def visitTest_module(self, ctx:TestSuiteParser.Test_moduleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#test_assertion.
    def visitTest_assertion(self, ctx:TestSuiteParser.Test_assertionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#pubAttributes.
    def visitPubAttributes(self, ctx:TestSuiteParser.PubAttributesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#test_parameter.
    def visitTest_parameter(self, ctx:TestSuiteParser.Test_parameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#emptyDesc.
    def visitEmptyDesc(self, ctx:TestSuiteParser.EmptyDescContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#specDesc.
    def visitSpecDesc(self, ctx:TestSuiteParser.SpecDescContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#emptyComment.
    def visitEmptyComment(self, ctx:TestSuiteParser.EmptyCommentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#specComment.
    def visitSpecComment(self, ctx:TestSuiteParser.SpecCommentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#nameDecl.
    def visitNameDecl(self, ctx:TestSuiteParser.NameDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#typeDecl.
    def visitTypeDecl(self, ctx:TestSuiteParser.TypeDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#combinedDecl.
    def visitCombinedDecl(self, ctx:TestSuiteParser.CombinedDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#arraySpec.
    def visitArraySpec(self, ctx:TestSuiteParser.ArraySpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#argSpecInput.
    def visitArgSpecInput(self, ctx:TestSuiteParser.ArgSpecInputContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#argSpecInOutput.
    def visitArgSpecInOutput(self, ctx:TestSuiteParser.ArgSpecInOutputContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#argSpecOutput.
    def visitArgSpecOutput(self, ctx:TestSuiteParser.ArgSpecOutputContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#constantSpec.
    def visitConstantSpec(self, ctx:TestSuiteParser.ConstantSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#customKey.
    def visitCustomKey(self, ctx:TestSuiteParser.CustomKeyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#test_directive.
    def visitTest_directive(self, ctx:TestSuiteParser.Test_directiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#ref.
    def visitRef(self, ctx:TestSuiteParser.RefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#enm.
    def visitEnm(self, ctx:TestSuiteParser.EnmContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#array.
    def visitArray(self, ctx:TestSuiteParser.ArrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#typeRef.
    def visitTypeRef(self, ctx:TestSuiteParser.TypeRefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#enumType.
    def visitEnumType(self, ctx:TestSuiteParser.EnumTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#enum.
    def visitEnum(self, ctx:TestSuiteParser.EnumContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#arrayType.
    def visitArrayType(self, ctx:TestSuiteParser.ArrayTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#size.
    def visitSize(self, ctx:TestSuiteParser.SizeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#range.
    def visitRange(self, ctx:TestSuiteParser.RangeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#sizeDim.
    def visitSizeDim(self, ctx:TestSuiteParser.SizeDimContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#rangeDim.
    def visitRangeDim(self, ctx:TestSuiteParser.RangeDimContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#strExpr.
    def visitStrExpr(self, ctx:TestSuiteParser.StrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#intExpr.
    def visitIntExpr(self, ctx:TestSuiteParser.IntExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#addSubExpr.
    def visitAddSubExpr(self, ctx:TestSuiteParser.AddSubExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#signExpr.
    def visitSignExpr(self, ctx:TestSuiteParser.SignExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#refExpr.
    def visitRefExpr(self, ctx:TestSuiteParser.RefExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#numberExpr.
    def visitNumberExpr(self, ctx:TestSuiteParser.NumberExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#parensExpr.
    def visitParensExpr(self, ctx:TestSuiteParser.ParensExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#mulDivExpr.
    def visitMulDivExpr(self, ctx:TestSuiteParser.MulDivExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#funRef.
    def visitFunRef(self, ctx:TestSuiteParser.FunRefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#varRef.
    def visitVarRef(self, ctx:TestSuiteParser.VarRefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#parensUnit.
    def visitParensUnit(self, ctx:TestSuiteParser.ParensUnitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#mulDivUnit.
    def visitMulDivUnit(self, ctx:TestSuiteParser.MulDivUnitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#cstUnit.
    def visitCstUnit(self, ctx:TestSuiteParser.CstUnitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#expUnit.
    def visitExpUnit(self, ctx:TestSuiteParser.ExpUnitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#stdUnit.
    def visitStdUnit(self, ctx:TestSuiteParser.StdUnitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#siUnit.
    def visitSiUnit(self, ctx:TestSuiteParser.SiUnitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#customUnit.
    def visitCustomUnit(self, ctx:TestSuiteParser.CustomUnitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#noP.
    def visitNoP(self, ctx:TestSuiteParser.NoPContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#quetta.
    def visitQuetta(self, ctx:TestSuiteParser.QuettaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#ronna.
    def visitRonna(self, ctx:TestSuiteParser.RonnaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#yotta.
    def visitYotta(self, ctx:TestSuiteParser.YottaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#zetta.
    def visitZetta(self, ctx:TestSuiteParser.ZettaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#exa.
    def visitExa(self, ctx:TestSuiteParser.ExaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#peta.
    def visitPeta(self, ctx:TestSuiteParser.PetaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#tera.
    def visitTera(self, ctx:TestSuiteParser.TeraContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#giga.
    def visitGiga(self, ctx:TestSuiteParser.GigaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#mega.
    def visitMega(self, ctx:TestSuiteParser.MegaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#kilo.
    def visitKilo(self, ctx:TestSuiteParser.KiloContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#hecto.
    def visitHecto(self, ctx:TestSuiteParser.HectoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#deca.
    def visitDeca(self, ctx:TestSuiteParser.DecaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#deci.
    def visitDeci(self, ctx:TestSuiteParser.DeciContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#centi.
    def visitCenti(self, ctx:TestSuiteParser.CentiContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#mili.
    def visitMili(self, ctx:TestSuiteParser.MiliContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#micro.
    def visitMicro(self, ctx:TestSuiteParser.MicroContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#nano.
    def visitNano(self, ctx:TestSuiteParser.NanoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#pico.
    def visitPico(self, ctx:TestSuiteParser.PicoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#femto.
    def visitFemto(self, ctx:TestSuiteParser.FemtoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#atto.
    def visitAtto(self, ctx:TestSuiteParser.AttoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#zepto.
    def visitZepto(self, ctx:TestSuiteParser.ZeptoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#yocto.
    def visitYocto(self, ctx:TestSuiteParser.YoctoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#ronto.
    def visitRonto(self, ctx:TestSuiteParser.RontoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#quecto.
    def visitQuecto(self, ctx:TestSuiteParser.QuectoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#second.
    def visitSecond(self, ctx:TestSuiteParser.SecondContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#metre.
    def visitMetre(self, ctx:TestSuiteParser.MetreContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#gram.
    def visitGram(self, ctx:TestSuiteParser.GramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#ampere.
    def visitAmpere(self, ctx:TestSuiteParser.AmpereContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#kelvin.
    def visitKelvin(self, ctx:TestSuiteParser.KelvinContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#mole.
    def visitMole(self, ctx:TestSuiteParser.MoleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#candela.
    def visitCandela(self, ctx:TestSuiteParser.CandelaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#pascal.
    def visitPascal(self, ctx:TestSuiteParser.PascalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#joule.
    def visitJoule(self, ctx:TestSuiteParser.JouleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestSuiteParser#ton.
    def visitTon(self, ctx:TestSuiteParser.TonContext):
        return self.visitChildren(ctx)



del TestSuiteParser