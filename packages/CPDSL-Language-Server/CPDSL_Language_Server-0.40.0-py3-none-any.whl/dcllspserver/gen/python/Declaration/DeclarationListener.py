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

# Generated from Declaration.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .DeclarationParser import DeclarationParser
else:
    from DeclarationParser import DeclarationParser

# This class defines a complete listener for a parse tree produced by DeclarationParser.
class DeclarationListener(ParseTreeListener):

    # Enter a parse tree produced by DeclarationParser#declarationModel.
    def enterDeclarationModel(self, ctx:DeclarationParser.DeclarationModelContext):
        pass

    # Exit a parse tree produced by DeclarationParser#declarationModel.
    def exitDeclarationModel(self, ctx:DeclarationParser.DeclarationModelContext):
        pass


    # Enter a parse tree produced by DeclarationParser#namedElement.
    def enterNamedElement(self, ctx:DeclarationParser.NamedElementContext):
        pass

    # Exit a parse tree produced by DeclarationParser#namedElement.
    def exitNamedElement(self, ctx:DeclarationParser.NamedElementContext):
        pass


    # Enter a parse tree produced by DeclarationParser#paramGroupAssignStat.
    def enterParamGroupAssignStat(self, ctx:DeclarationParser.ParamGroupAssignStatContext):
        pass

    # Exit a parse tree produced by DeclarationParser#paramGroupAssignStat.
    def exitParamGroupAssignStat(self, ctx:DeclarationParser.ParamGroupAssignStatContext):
        pass


    # Enter a parse tree produced by DeclarationParser#paramAssignStat.
    def enterParamAssignStat(self, ctx:DeclarationParser.ParamAssignStatContext):
        pass

    # Exit a parse tree produced by DeclarationParser#paramAssignStat.
    def exitParamAssignStat(self, ctx:DeclarationParser.ParamAssignStatContext):
        pass


    # Enter a parse tree produced by DeclarationParser#featureAssignStat.
    def enterFeatureAssignStat(self, ctx:DeclarationParser.FeatureAssignStatContext):
        pass

    # Exit a parse tree produced by DeclarationParser#featureAssignStat.
    def exitFeatureAssignStat(self, ctx:DeclarationParser.FeatureAssignStatContext):
        pass


    # Enter a parse tree produced by DeclarationParser#featureGroupAssignStat.
    def enterFeatureGroupAssignStat(self, ctx:DeclarationParser.FeatureGroupAssignStatContext):
        pass

    # Exit a parse tree produced by DeclarationParser#featureGroupAssignStat.
    def exitFeatureGroupAssignStat(self, ctx:DeclarationParser.FeatureGroupAssignStatContext):
        pass


    # Enter a parse tree produced by DeclarationParser#eKind.
    def enterEKind(self, ctx:DeclarationParser.EKindContext):
        pass

    # Exit a parse tree produced by DeclarationParser#eKind.
    def exitEKind(self, ctx:DeclarationParser.EKindContext):
        pass


    # Enter a parse tree produced by DeclarationParser#paramType.
    def enterParamType(self, ctx:DeclarationParser.ParamTypeContext):
        pass

    # Exit a parse tree produced by DeclarationParser#paramType.
    def exitParamType(self, ctx:DeclarationParser.ParamTypeContext):
        pass


    # Enter a parse tree produced by DeclarationParser#inlineEnumerationType.
    def enterInlineEnumerationType(self, ctx:DeclarationParser.InlineEnumerationTypeContext):
        pass

    # Exit a parse tree produced by DeclarationParser#inlineEnumerationType.
    def exitInlineEnumerationType(self, ctx:DeclarationParser.InlineEnumerationTypeContext):
        pass


    # Enter a parse tree produced by DeclarationParser#typeReference.
    def enterTypeReference(self, ctx:DeclarationParser.TypeReferenceContext):
        pass

    # Exit a parse tree produced by DeclarationParser#typeReference.
    def exitTypeReference(self, ctx:DeclarationParser.TypeReferenceContext):
        pass


    # Enter a parse tree produced by DeclarationParser#arrayType.
    def enterArrayType(self, ctx:DeclarationParser.ArrayTypeContext):
        pass

    # Exit a parse tree produced by DeclarationParser#arrayType.
    def exitArrayType(self, ctx:DeclarationParser.ArrayTypeContext):
        pass


    # Enter a parse tree produced by DeclarationParser#dimension.
    def enterDimension(self, ctx:DeclarationParser.DimensionContext):
        pass

    # Exit a parse tree produced by DeclarationParser#dimension.
    def exitDimension(self, ctx:DeclarationParser.DimensionContext):
        pass


    # Enter a parse tree produced by DeclarationParser#sizeDimension.
    def enterSizeDimension(self, ctx:DeclarationParser.SizeDimensionContext):
        pass

    # Exit a parse tree produced by DeclarationParser#sizeDimension.
    def exitSizeDimension(self, ctx:DeclarationParser.SizeDimensionContext):
        pass


    # Enter a parse tree produced by DeclarationParser#rangeDimension.
    def enterRangeDimension(self, ctx:DeclarationParser.RangeDimensionContext):
        pass

    # Exit a parse tree produced by DeclarationParser#rangeDimension.
    def exitRangeDimension(self, ctx:DeclarationParser.RangeDimensionContext):
        pass


    # Enter a parse tree produced by DeclarationParser#declaredType.
    def enterDeclaredType(self, ctx:DeclarationParser.DeclaredTypeContext):
        pass

    # Exit a parse tree produced by DeclarationParser#declaredType.
    def exitDeclaredType(self, ctx:DeclarationParser.DeclaredTypeContext):
        pass


    # Enter a parse tree produced by DeclarationParser#rangeType.
    def enterRangeType(self, ctx:DeclarationParser.RangeTypeContext):
        pass

    # Exit a parse tree produced by DeclarationParser#rangeType.
    def exitRangeType(self, ctx:DeclarationParser.RangeTypeContext):
        pass


    # Enter a parse tree produced by DeclarationParser#enumerationType.
    def enterEnumerationType(self, ctx:DeclarationParser.EnumerationTypeContext):
        pass

    # Exit a parse tree produced by DeclarationParser#enumerationType.
    def exitEnumerationType(self, ctx:DeclarationParser.EnumerationTypeContext):
        pass


    # Enter a parse tree produced by DeclarationParser#enumeral.
    def enterEnumeral(self, ctx:DeclarationParser.EnumeralContext):
        pass

    # Exit a parse tree produced by DeclarationParser#enumeral.
    def exitEnumeral(self, ctx:DeclarationParser.EnumeralContext):
        pass


    # Enter a parse tree produced by DeclarationParser#unitSpecification.
    def enterUnitSpecification(self, ctx:DeclarationParser.UnitSpecificationContext):
        pass

    # Exit a parse tree produced by DeclarationParser#unitSpecification.
    def exitUnitSpecification(self, ctx:DeclarationParser.UnitSpecificationContext):
        pass


    # Enter a parse tree produced by DeclarationParser#basicUnit.
    def enterBasicUnit(self, ctx:DeclarationParser.BasicUnitContext):
        pass

    # Exit a parse tree produced by DeclarationParser#basicUnit.
    def exitBasicUnit(self, ctx:DeclarationParser.BasicUnitContext):
        pass


    # Enter a parse tree produced by DeclarationParser#siunit.
    def enterSiunit(self, ctx:DeclarationParser.SiunitContext):
        pass

    # Exit a parse tree produced by DeclarationParser#siunit.
    def exitSiunit(self, ctx:DeclarationParser.SiunitContext):
        pass


    # Enter a parse tree produced by DeclarationParser#customunit.
    def enterCustomunit(self, ctx:DeclarationParser.CustomunitContext):
        pass

    # Exit a parse tree produced by DeclarationParser#customunit.
    def exitCustomunit(self, ctx:DeclarationParser.CustomunitContext):
        pass


    # Enter a parse tree produced by DeclarationParser#composedUnit.
    def enterComposedUnit(self, ctx:DeclarationParser.ComposedUnitContext):
        pass

    # Exit a parse tree produced by DeclarationParser#composedUnit.
    def exitComposedUnit(self, ctx:DeclarationParser.ComposedUnitContext):
        pass


    # Enter a parse tree produced by DeclarationParser#ePrefix.
    def enterEPrefix(self, ctx:DeclarationParser.EPrefixContext):
        pass

    # Exit a parse tree produced by DeclarationParser#ePrefix.
    def exitEPrefix(self, ctx:DeclarationParser.EPrefixContext):
        pass


    # Enter a parse tree produced by DeclarationParser#eSIUnitType.
    def enterESIUnitType(self, ctx:DeclarationParser.ESIUnitTypeContext):
        pass

    # Exit a parse tree produced by DeclarationParser#eSIUnitType.
    def exitESIUnitType(self, ctx:DeclarationParser.ESIUnitTypeContext):
        pass


    # Enter a parse tree produced by DeclarationParser#arithmeticExpression.
    def enterArithmeticExpression(self, ctx:DeclarationParser.ArithmeticExpressionContext):
        pass

    # Exit a parse tree produced by DeclarationParser#arithmeticExpression.
    def exitArithmeticExpression(self, ctx:DeclarationParser.ArithmeticExpressionContext):
        pass


    # Enter a parse tree produced by DeclarationParser#eAdditionOperator.
    def enterEAdditionOperator(self, ctx:DeclarationParser.EAdditionOperatorContext):
        pass

    # Exit a parse tree produced by DeclarationParser#eAdditionOperator.
    def exitEAdditionOperator(self, ctx:DeclarationParser.EAdditionOperatorContext):
        pass


    # Enter a parse tree produced by DeclarationParser#multiplicationExpression.
    def enterMultiplicationExpression(self, ctx:DeclarationParser.MultiplicationExpressionContext):
        pass

    # Exit a parse tree produced by DeclarationParser#multiplicationExpression.
    def exitMultiplicationExpression(self, ctx:DeclarationParser.MultiplicationExpressionContext):
        pass


    # Enter a parse tree produced by DeclarationParser#eMultiplicationOperator.
    def enterEMultiplicationOperator(self, ctx:DeclarationParser.EMultiplicationOperatorContext):
        pass

    # Exit a parse tree produced by DeclarationParser#eMultiplicationOperator.
    def exitEMultiplicationOperator(self, ctx:DeclarationParser.EMultiplicationOperatorContext):
        pass


    # Enter a parse tree produced by DeclarationParser#valueExpression.
    def enterValueExpression(self, ctx:DeclarationParser.ValueExpressionContext):
        pass

    # Exit a parse tree produced by DeclarationParser#valueExpression.
    def exitValueExpression(self, ctx:DeclarationParser.ValueExpressionContext):
        pass


    # Enter a parse tree produced by DeclarationParser#literalExpression.
    def enterLiteralExpression(self, ctx:DeclarationParser.LiteralExpressionContext):
        pass

    # Exit a parse tree produced by DeclarationParser#literalExpression.
    def exitLiteralExpression(self, ctx:DeclarationParser.LiteralExpressionContext):
        pass


    # Enter a parse tree produced by DeclarationParser#literal.
    def enterLiteral(self, ctx:DeclarationParser.LiteralContext):
        pass

    # Exit a parse tree produced by DeclarationParser#literal.
    def exitLiteral(self, ctx:DeclarationParser.LiteralContext):
        pass


    # Enter a parse tree produced by DeclarationParser#parenthesisExpression.
    def enterParenthesisExpression(self, ctx:DeclarationParser.ParenthesisExpressionContext):
        pass

    # Exit a parse tree produced by DeclarationParser#parenthesisExpression.
    def exitParenthesisExpression(self, ctx:DeclarationParser.ParenthesisExpressionContext):
        pass


    # Enter a parse tree produced by DeclarationParser#arrayExpression.
    def enterArrayExpression(self, ctx:DeclarationParser.ArrayExpressionContext):
        pass

    # Exit a parse tree produced by DeclarationParser#arrayExpression.
    def exitArrayExpression(self, ctx:DeclarationParser.ArrayExpressionContext):
        pass


    # Enter a parse tree produced by DeclarationParser#namedElementReference.
    def enterNamedElementReference(self, ctx:DeclarationParser.NamedElementReferenceContext):
        pass

    # Exit a parse tree produced by DeclarationParser#namedElementReference.
    def exitNamedElementReference(self, ctx:DeclarationParser.NamedElementReferenceContext):
        pass


    # Enter a parse tree produced by DeclarationParser#stringValue.
    def enterStringValue(self, ctx:DeclarationParser.StringValueContext):
        pass

    # Exit a parse tree produced by DeclarationParser#stringValue.
    def exitStringValue(self, ctx:DeclarationParser.StringValueContext):
        pass


    # Enter a parse tree produced by DeclarationParser#longValue.
    def enterLongValue(self, ctx:DeclarationParser.LongValueContext):
        pass

    # Exit a parse tree produced by DeclarationParser#longValue.
    def exitLongValue(self, ctx:DeclarationParser.LongValueContext):
        pass


    # Enter a parse tree produced by DeclarationParser#doubleValue.
    def enterDoubleValue(self, ctx:DeclarationParser.DoubleValueContext):
        pass

    # Exit a parse tree produced by DeclarationParser#doubleValue.
    def exitDoubleValue(self, ctx:DeclarationParser.DoubleValueContext):
        pass


    # Enter a parse tree produced by DeclarationParser#booleanValue.
    def enterBooleanValue(self, ctx:DeclarationParser.BooleanValueContext):
        pass

    # Exit a parse tree produced by DeclarationParser#booleanValue.
    def exitBooleanValue(self, ctx:DeclarationParser.BooleanValueContext):
        pass



del DeclarationParser