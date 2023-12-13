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

# This class defines a complete generic visitor for a parse tree produced by DeclarationParser.

class DeclarationVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by DeclarationParser#declarationModel.
    def visitDeclarationModel(self, ctx:DeclarationParser.DeclarationModelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeclarationParser#namedElement.
    def visitNamedElement(self, ctx:DeclarationParser.NamedElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeclarationParser#paramGroupAssignStat.
    def visitParamGroupAssignStat(self, ctx:DeclarationParser.ParamGroupAssignStatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeclarationParser#paramAssignStat.
    def visitParamAssignStat(self, ctx:DeclarationParser.ParamAssignStatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeclarationParser#featureAssignStat.
    def visitFeatureAssignStat(self, ctx:DeclarationParser.FeatureAssignStatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeclarationParser#featureGroupAssignStat.
    def visitFeatureGroupAssignStat(self, ctx:DeclarationParser.FeatureGroupAssignStatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeclarationParser#eKind.
    def visitEKind(self, ctx:DeclarationParser.EKindContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeclarationParser#paramType.
    def visitParamType(self, ctx:DeclarationParser.ParamTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeclarationParser#inlineEnumerationType.
    def visitInlineEnumerationType(self, ctx:DeclarationParser.InlineEnumerationTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeclarationParser#typeReference.
    def visitTypeReference(self, ctx:DeclarationParser.TypeReferenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeclarationParser#arrayType.
    def visitArrayType(self, ctx:DeclarationParser.ArrayTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeclarationParser#dimension.
    def visitDimension(self, ctx:DeclarationParser.DimensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeclarationParser#sizeDimension.
    def visitSizeDimension(self, ctx:DeclarationParser.SizeDimensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeclarationParser#rangeDimension.
    def visitRangeDimension(self, ctx:DeclarationParser.RangeDimensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeclarationParser#declaredType.
    def visitDeclaredType(self, ctx:DeclarationParser.DeclaredTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeclarationParser#rangeType.
    def visitRangeType(self, ctx:DeclarationParser.RangeTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeclarationParser#enumerationType.
    def visitEnumerationType(self, ctx:DeclarationParser.EnumerationTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeclarationParser#enumeral.
    def visitEnumeral(self, ctx:DeclarationParser.EnumeralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeclarationParser#unitSpecification.
    def visitUnitSpecification(self, ctx:DeclarationParser.UnitSpecificationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeclarationParser#basicUnit.
    def visitBasicUnit(self, ctx:DeclarationParser.BasicUnitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeclarationParser#siunit.
    def visitSiunit(self, ctx:DeclarationParser.SiunitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeclarationParser#customunit.
    def visitCustomunit(self, ctx:DeclarationParser.CustomunitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeclarationParser#composedUnit.
    def visitComposedUnit(self, ctx:DeclarationParser.ComposedUnitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeclarationParser#ePrefix.
    def visitEPrefix(self, ctx:DeclarationParser.EPrefixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeclarationParser#eSIUnitType.
    def visitESIUnitType(self, ctx:DeclarationParser.ESIUnitTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeclarationParser#arithmeticExpression.
    def visitArithmeticExpression(self, ctx:DeclarationParser.ArithmeticExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeclarationParser#eAdditionOperator.
    def visitEAdditionOperator(self, ctx:DeclarationParser.EAdditionOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeclarationParser#multiplicationExpression.
    def visitMultiplicationExpression(self, ctx:DeclarationParser.MultiplicationExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeclarationParser#eMultiplicationOperator.
    def visitEMultiplicationOperator(self, ctx:DeclarationParser.EMultiplicationOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeclarationParser#valueExpression.
    def visitValueExpression(self, ctx:DeclarationParser.ValueExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeclarationParser#literalExpression.
    def visitLiteralExpression(self, ctx:DeclarationParser.LiteralExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeclarationParser#literal.
    def visitLiteral(self, ctx:DeclarationParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeclarationParser#parenthesisExpression.
    def visitParenthesisExpression(self, ctx:DeclarationParser.ParenthesisExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeclarationParser#arrayExpression.
    def visitArrayExpression(self, ctx:DeclarationParser.ArrayExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeclarationParser#namedElementReference.
    def visitNamedElementReference(self, ctx:DeclarationParser.NamedElementReferenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeclarationParser#stringValue.
    def visitStringValue(self, ctx:DeclarationParser.StringValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeclarationParser#longValue.
    def visitLongValue(self, ctx:DeclarationParser.LongValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeclarationParser#doubleValue.
    def visitDoubleValue(self, ctx:DeclarationParser.DoubleValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeclarationParser#booleanValue.
    def visitBooleanValue(self, ctx:DeclarationParser.BooleanValueContext):
        return self.visitChildren(ctx)



del DeclarationParser