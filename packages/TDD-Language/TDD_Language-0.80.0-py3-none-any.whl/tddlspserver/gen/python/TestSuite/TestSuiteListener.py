# Generated from TestSuite.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .TestSuiteParser import TestSuiteParser
else:
    from TestSuiteParser import TestSuiteParser

# This class defines a complete listener for a parse tree produced by TestSuiteParser.
class TestSuiteListener(ParseTreeListener):

    # Enter a parse tree produced by TestSuiteParser#test_suite.
    def enterTest_suite(self, ctx:TestSuiteParser.Test_suiteContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#test_suite.
    def exitTest_suite(self, ctx:TestSuiteParser.Test_suiteContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#test_case.
    def enterTest_case(self, ctx:TestSuiteParser.Test_caseContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#test_case.
    def exitTest_case(self, ctx:TestSuiteParser.Test_caseContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#test_flag.
    def enterTest_flag(self, ctx:TestSuiteParser.Test_flagContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#test_flag.
    def exitTest_flag(self, ctx:TestSuiteParser.Test_flagContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#overwritePF.
    def enterOverwritePF(self, ctx:TestSuiteParser.OverwritePFContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#overwritePF.
    def exitOverwritePF(self, ctx:TestSuiteParser.OverwritePFContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#overwriteCMake.
    def enterOverwriteCMake(self, ctx:TestSuiteParser.OverwriteCMakeContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#overwriteCMake.
    def exitOverwriteCMake(self, ctx:TestSuiteParser.OverwriteCMakeContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#overwriteF90.
    def enterOverwriteF90(self, ctx:TestSuiteParser.OverwriteF90Context):
        pass

    # Exit a parse tree produced by TestSuiteParser#overwriteF90.
    def exitOverwriteF90(self, ctx:TestSuiteParser.OverwriteF90Context):
        pass


    # Enter a parse tree produced by TestSuiteParser#src_path.
    def enterSrc_path(self, ctx:TestSuiteParser.Src_pathContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#src_path.
    def exitSrc_path(self, ctx:TestSuiteParser.Src_pathContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#test_vars.
    def enterTest_vars(self, ctx:TestSuiteParser.Test_varsContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#test_vars.
    def exitTest_vars(self, ctx:TestSuiteParser.Test_varsContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#test_var.
    def enterTest_var(self, ctx:TestSuiteParser.Test_varContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#test_var.
    def exitTest_var(self, ctx:TestSuiteParser.Test_varContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#varDeclaration.
    def enterVarDeclaration(self, ctx:TestSuiteParser.VarDeclarationContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#varDeclaration.
    def exitVarDeclaration(self, ctx:TestSuiteParser.VarDeclarationContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#use_modules.
    def enterUse_modules(self, ctx:TestSuiteParser.Use_modulesContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#use_modules.
    def exitUse_modules(self, ctx:TestSuiteParser.Use_modulesContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#test_module.
    def enterTest_module(self, ctx:TestSuiteParser.Test_moduleContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#test_module.
    def exitTest_module(self, ctx:TestSuiteParser.Test_moduleContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#test_assertion.
    def enterTest_assertion(self, ctx:TestSuiteParser.Test_assertionContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#test_assertion.
    def exitTest_assertion(self, ctx:TestSuiteParser.Test_assertionContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#pubAttributes.
    def enterPubAttributes(self, ctx:TestSuiteParser.PubAttributesContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#pubAttributes.
    def exitPubAttributes(self, ctx:TestSuiteParser.PubAttributesContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#test_parameter.
    def enterTest_parameter(self, ctx:TestSuiteParser.Test_parameterContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#test_parameter.
    def exitTest_parameter(self, ctx:TestSuiteParser.Test_parameterContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#emptyDesc.
    def enterEmptyDesc(self, ctx:TestSuiteParser.EmptyDescContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#emptyDesc.
    def exitEmptyDesc(self, ctx:TestSuiteParser.EmptyDescContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#specDesc.
    def enterSpecDesc(self, ctx:TestSuiteParser.SpecDescContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#specDesc.
    def exitSpecDesc(self, ctx:TestSuiteParser.SpecDescContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#emptyComment.
    def enterEmptyComment(self, ctx:TestSuiteParser.EmptyCommentContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#emptyComment.
    def exitEmptyComment(self, ctx:TestSuiteParser.EmptyCommentContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#specComment.
    def enterSpecComment(self, ctx:TestSuiteParser.SpecCommentContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#specComment.
    def exitSpecComment(self, ctx:TestSuiteParser.SpecCommentContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#nameDecl.
    def enterNameDecl(self, ctx:TestSuiteParser.NameDeclContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#nameDecl.
    def exitNameDecl(self, ctx:TestSuiteParser.NameDeclContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#typeDecl.
    def enterTypeDecl(self, ctx:TestSuiteParser.TypeDeclContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#typeDecl.
    def exitTypeDecl(self, ctx:TestSuiteParser.TypeDeclContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#combinedDecl.
    def enterCombinedDecl(self, ctx:TestSuiteParser.CombinedDeclContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#combinedDecl.
    def exitCombinedDecl(self, ctx:TestSuiteParser.CombinedDeclContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#arraySpec.
    def enterArraySpec(self, ctx:TestSuiteParser.ArraySpecContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#arraySpec.
    def exitArraySpec(self, ctx:TestSuiteParser.ArraySpecContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#argSpecInput.
    def enterArgSpecInput(self, ctx:TestSuiteParser.ArgSpecInputContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#argSpecInput.
    def exitArgSpecInput(self, ctx:TestSuiteParser.ArgSpecInputContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#argSpecInOutput.
    def enterArgSpecInOutput(self, ctx:TestSuiteParser.ArgSpecInOutputContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#argSpecInOutput.
    def exitArgSpecInOutput(self, ctx:TestSuiteParser.ArgSpecInOutputContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#argSpecOutput.
    def enterArgSpecOutput(self, ctx:TestSuiteParser.ArgSpecOutputContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#argSpecOutput.
    def exitArgSpecOutput(self, ctx:TestSuiteParser.ArgSpecOutputContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#constantSpec.
    def enterConstantSpec(self, ctx:TestSuiteParser.ConstantSpecContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#constantSpec.
    def exitConstantSpec(self, ctx:TestSuiteParser.ConstantSpecContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#customKey.
    def enterCustomKey(self, ctx:TestSuiteParser.CustomKeyContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#customKey.
    def exitCustomKey(self, ctx:TestSuiteParser.CustomKeyContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#test_directive.
    def enterTest_directive(self, ctx:TestSuiteParser.Test_directiveContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#test_directive.
    def exitTest_directive(self, ctx:TestSuiteParser.Test_directiveContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#ref.
    def enterRef(self, ctx:TestSuiteParser.RefContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#ref.
    def exitRef(self, ctx:TestSuiteParser.RefContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#enm.
    def enterEnm(self, ctx:TestSuiteParser.EnmContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#enm.
    def exitEnm(self, ctx:TestSuiteParser.EnmContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#array.
    def enterArray(self, ctx:TestSuiteParser.ArrayContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#array.
    def exitArray(self, ctx:TestSuiteParser.ArrayContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#typeRef.
    def enterTypeRef(self, ctx:TestSuiteParser.TypeRefContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#typeRef.
    def exitTypeRef(self, ctx:TestSuiteParser.TypeRefContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#enumType.
    def enterEnumType(self, ctx:TestSuiteParser.EnumTypeContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#enumType.
    def exitEnumType(self, ctx:TestSuiteParser.EnumTypeContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#enum.
    def enterEnum(self, ctx:TestSuiteParser.EnumContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#enum.
    def exitEnum(self, ctx:TestSuiteParser.EnumContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#arrayType.
    def enterArrayType(self, ctx:TestSuiteParser.ArrayTypeContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#arrayType.
    def exitArrayType(self, ctx:TestSuiteParser.ArrayTypeContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#size.
    def enterSize(self, ctx:TestSuiteParser.SizeContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#size.
    def exitSize(self, ctx:TestSuiteParser.SizeContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#range.
    def enterRange(self, ctx:TestSuiteParser.RangeContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#range.
    def exitRange(self, ctx:TestSuiteParser.RangeContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#sizeDim.
    def enterSizeDim(self, ctx:TestSuiteParser.SizeDimContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#sizeDim.
    def exitSizeDim(self, ctx:TestSuiteParser.SizeDimContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#rangeDim.
    def enterRangeDim(self, ctx:TestSuiteParser.RangeDimContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#rangeDim.
    def exitRangeDim(self, ctx:TestSuiteParser.RangeDimContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#strExpr.
    def enterStrExpr(self, ctx:TestSuiteParser.StrExprContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#strExpr.
    def exitStrExpr(self, ctx:TestSuiteParser.StrExprContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#intExpr.
    def enterIntExpr(self, ctx:TestSuiteParser.IntExprContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#intExpr.
    def exitIntExpr(self, ctx:TestSuiteParser.IntExprContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#addSubExpr.
    def enterAddSubExpr(self, ctx:TestSuiteParser.AddSubExprContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#addSubExpr.
    def exitAddSubExpr(self, ctx:TestSuiteParser.AddSubExprContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#signExpr.
    def enterSignExpr(self, ctx:TestSuiteParser.SignExprContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#signExpr.
    def exitSignExpr(self, ctx:TestSuiteParser.SignExprContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#refExpr.
    def enterRefExpr(self, ctx:TestSuiteParser.RefExprContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#refExpr.
    def exitRefExpr(self, ctx:TestSuiteParser.RefExprContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#numberExpr.
    def enterNumberExpr(self, ctx:TestSuiteParser.NumberExprContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#numberExpr.
    def exitNumberExpr(self, ctx:TestSuiteParser.NumberExprContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#parensExpr.
    def enterParensExpr(self, ctx:TestSuiteParser.ParensExprContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#parensExpr.
    def exitParensExpr(self, ctx:TestSuiteParser.ParensExprContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#mulDivExpr.
    def enterMulDivExpr(self, ctx:TestSuiteParser.MulDivExprContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#mulDivExpr.
    def exitMulDivExpr(self, ctx:TestSuiteParser.MulDivExprContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#funRef.
    def enterFunRef(self, ctx:TestSuiteParser.FunRefContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#funRef.
    def exitFunRef(self, ctx:TestSuiteParser.FunRefContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#varRef.
    def enterVarRef(self, ctx:TestSuiteParser.VarRefContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#varRef.
    def exitVarRef(self, ctx:TestSuiteParser.VarRefContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#parensUnit.
    def enterParensUnit(self, ctx:TestSuiteParser.ParensUnitContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#parensUnit.
    def exitParensUnit(self, ctx:TestSuiteParser.ParensUnitContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#mulDivUnit.
    def enterMulDivUnit(self, ctx:TestSuiteParser.MulDivUnitContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#mulDivUnit.
    def exitMulDivUnit(self, ctx:TestSuiteParser.MulDivUnitContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#cstUnit.
    def enterCstUnit(self, ctx:TestSuiteParser.CstUnitContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#cstUnit.
    def exitCstUnit(self, ctx:TestSuiteParser.CstUnitContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#expUnit.
    def enterExpUnit(self, ctx:TestSuiteParser.ExpUnitContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#expUnit.
    def exitExpUnit(self, ctx:TestSuiteParser.ExpUnitContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#stdUnit.
    def enterStdUnit(self, ctx:TestSuiteParser.StdUnitContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#stdUnit.
    def exitStdUnit(self, ctx:TestSuiteParser.StdUnitContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#siUnit.
    def enterSiUnit(self, ctx:TestSuiteParser.SiUnitContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#siUnit.
    def exitSiUnit(self, ctx:TestSuiteParser.SiUnitContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#customUnit.
    def enterCustomUnit(self, ctx:TestSuiteParser.CustomUnitContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#customUnit.
    def exitCustomUnit(self, ctx:TestSuiteParser.CustomUnitContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#noP.
    def enterNoP(self, ctx:TestSuiteParser.NoPContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#noP.
    def exitNoP(self, ctx:TestSuiteParser.NoPContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#quetta.
    def enterQuetta(self, ctx:TestSuiteParser.QuettaContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#quetta.
    def exitQuetta(self, ctx:TestSuiteParser.QuettaContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#ronna.
    def enterRonna(self, ctx:TestSuiteParser.RonnaContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#ronna.
    def exitRonna(self, ctx:TestSuiteParser.RonnaContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#yotta.
    def enterYotta(self, ctx:TestSuiteParser.YottaContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#yotta.
    def exitYotta(self, ctx:TestSuiteParser.YottaContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#zetta.
    def enterZetta(self, ctx:TestSuiteParser.ZettaContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#zetta.
    def exitZetta(self, ctx:TestSuiteParser.ZettaContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#exa.
    def enterExa(self, ctx:TestSuiteParser.ExaContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#exa.
    def exitExa(self, ctx:TestSuiteParser.ExaContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#peta.
    def enterPeta(self, ctx:TestSuiteParser.PetaContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#peta.
    def exitPeta(self, ctx:TestSuiteParser.PetaContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#tera.
    def enterTera(self, ctx:TestSuiteParser.TeraContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#tera.
    def exitTera(self, ctx:TestSuiteParser.TeraContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#giga.
    def enterGiga(self, ctx:TestSuiteParser.GigaContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#giga.
    def exitGiga(self, ctx:TestSuiteParser.GigaContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#mega.
    def enterMega(self, ctx:TestSuiteParser.MegaContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#mega.
    def exitMega(self, ctx:TestSuiteParser.MegaContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#kilo.
    def enterKilo(self, ctx:TestSuiteParser.KiloContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#kilo.
    def exitKilo(self, ctx:TestSuiteParser.KiloContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#hecto.
    def enterHecto(self, ctx:TestSuiteParser.HectoContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#hecto.
    def exitHecto(self, ctx:TestSuiteParser.HectoContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#deca.
    def enterDeca(self, ctx:TestSuiteParser.DecaContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#deca.
    def exitDeca(self, ctx:TestSuiteParser.DecaContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#deci.
    def enterDeci(self, ctx:TestSuiteParser.DeciContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#deci.
    def exitDeci(self, ctx:TestSuiteParser.DeciContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#centi.
    def enterCenti(self, ctx:TestSuiteParser.CentiContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#centi.
    def exitCenti(self, ctx:TestSuiteParser.CentiContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#mili.
    def enterMili(self, ctx:TestSuiteParser.MiliContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#mili.
    def exitMili(self, ctx:TestSuiteParser.MiliContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#micro.
    def enterMicro(self, ctx:TestSuiteParser.MicroContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#micro.
    def exitMicro(self, ctx:TestSuiteParser.MicroContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#nano.
    def enterNano(self, ctx:TestSuiteParser.NanoContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#nano.
    def exitNano(self, ctx:TestSuiteParser.NanoContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#pico.
    def enterPico(self, ctx:TestSuiteParser.PicoContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#pico.
    def exitPico(self, ctx:TestSuiteParser.PicoContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#femto.
    def enterFemto(self, ctx:TestSuiteParser.FemtoContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#femto.
    def exitFemto(self, ctx:TestSuiteParser.FemtoContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#atto.
    def enterAtto(self, ctx:TestSuiteParser.AttoContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#atto.
    def exitAtto(self, ctx:TestSuiteParser.AttoContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#zepto.
    def enterZepto(self, ctx:TestSuiteParser.ZeptoContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#zepto.
    def exitZepto(self, ctx:TestSuiteParser.ZeptoContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#yocto.
    def enterYocto(self, ctx:TestSuiteParser.YoctoContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#yocto.
    def exitYocto(self, ctx:TestSuiteParser.YoctoContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#ronto.
    def enterRonto(self, ctx:TestSuiteParser.RontoContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#ronto.
    def exitRonto(self, ctx:TestSuiteParser.RontoContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#quecto.
    def enterQuecto(self, ctx:TestSuiteParser.QuectoContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#quecto.
    def exitQuecto(self, ctx:TestSuiteParser.QuectoContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#second.
    def enterSecond(self, ctx:TestSuiteParser.SecondContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#second.
    def exitSecond(self, ctx:TestSuiteParser.SecondContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#metre.
    def enterMetre(self, ctx:TestSuiteParser.MetreContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#metre.
    def exitMetre(self, ctx:TestSuiteParser.MetreContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#gram.
    def enterGram(self, ctx:TestSuiteParser.GramContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#gram.
    def exitGram(self, ctx:TestSuiteParser.GramContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#ampere.
    def enterAmpere(self, ctx:TestSuiteParser.AmpereContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#ampere.
    def exitAmpere(self, ctx:TestSuiteParser.AmpereContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#kelvin.
    def enterKelvin(self, ctx:TestSuiteParser.KelvinContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#kelvin.
    def exitKelvin(self, ctx:TestSuiteParser.KelvinContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#mole.
    def enterMole(self, ctx:TestSuiteParser.MoleContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#mole.
    def exitMole(self, ctx:TestSuiteParser.MoleContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#candela.
    def enterCandela(self, ctx:TestSuiteParser.CandelaContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#candela.
    def exitCandela(self, ctx:TestSuiteParser.CandelaContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#pascal.
    def enterPascal(self, ctx:TestSuiteParser.PascalContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#pascal.
    def exitPascal(self, ctx:TestSuiteParser.PascalContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#joule.
    def enterJoule(self, ctx:TestSuiteParser.JouleContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#joule.
    def exitJoule(self, ctx:TestSuiteParser.JouleContext):
        pass


    # Enter a parse tree produced by TestSuiteParser#ton.
    def enterTon(self, ctx:TestSuiteParser.TonContext):
        pass

    # Exit a parse tree produced by TestSuiteParser#ton.
    def exitTon(self, ctx:TestSuiteParser.TonContext):
        pass



del TestSuiteParser