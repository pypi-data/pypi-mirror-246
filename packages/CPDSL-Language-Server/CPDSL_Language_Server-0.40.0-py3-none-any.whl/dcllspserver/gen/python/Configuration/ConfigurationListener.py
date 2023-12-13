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

# Generated from Configuration.g4 by ANTLR 4.12.0
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .ConfigurationParser import ConfigurationParser
else:
    from ConfigurationParser import ConfigurationParser

# This class defines a complete listener for a parse tree produced by ConfigurationParser.
class ConfigurationListener(ParseTreeListener):

    # Enter a parse tree produced by ConfigurationParser#configurationModel.
    def enterConfigurationModel(self, ctx:ConfigurationParser.ConfigurationModelContext):
        pass

    # Exit a parse tree produced by ConfigurationParser#configurationModel.
    def exitConfigurationModel(self, ctx:ConfigurationParser.ConfigurationModelContext):
        pass


    # Enter a parse tree produced by ConfigurationParser#include.
    def enterInclude(self, ctx:ConfigurationParser.IncludeContext):
        pass

    # Exit a parse tree produced by ConfigurationParser#include.
    def exitInclude(self, ctx:ConfigurationParser.IncludeContext):
        pass


    # Enter a parse tree produced by ConfigurationParser#featureActivation.
    def enterFeatureActivation(self, ctx:ConfigurationParser.FeatureActivationContext):
        pass

    # Exit a parse tree produced by ConfigurationParser#featureActivation.
    def exitFeatureActivation(self, ctx:ConfigurationParser.FeatureActivationContext):
        pass


    # Enter a parse tree produced by ConfigurationParser#featureConfiguration.
    def enterFeatureConfiguration(self, ctx:ConfigurationParser.FeatureConfigurationContext):
        pass

    # Exit a parse tree produced by ConfigurationParser#featureConfiguration.
    def exitFeatureConfiguration(self, ctx:ConfigurationParser.FeatureConfigurationContext):
        pass


    # Enter a parse tree produced by ConfigurationParser#parameterGroup.
    def enterParameterGroup(self, ctx:ConfigurationParser.ParameterGroupContext):
        pass

    # Exit a parse tree produced by ConfigurationParser#parameterGroup.
    def exitParameterGroup(self, ctx:ConfigurationParser.ParameterGroupContext):
        pass


    # Enter a parse tree produced by ConfigurationParser#parameterAssignment.
    def enterParameterAssignment(self, ctx:ConfigurationParser.ParameterAssignmentContext):
        pass

    # Exit a parse tree produced by ConfigurationParser#parameterAssignment.
    def exitParameterAssignment(self, ctx:ConfigurationParser.ParameterAssignmentContext):
        pass


    # Enter a parse tree produced by ConfigurationParser#selector.
    def enterSelector(self, ctx:ConfigurationParser.SelectorContext):
        pass

    # Exit a parse tree produced by ConfigurationParser#selector.
    def exitSelector(self, ctx:ConfigurationParser.SelectorContext):
        pass


    # Enter a parse tree produced by ConfigurationParser#elementSelector.
    def enterElementSelector(self, ctx:ConfigurationParser.ElementSelectorContext):
        pass

    # Exit a parse tree produced by ConfigurationParser#elementSelector.
    def exitElementSelector(self, ctx:ConfigurationParser.ElementSelectorContext):
        pass


    # Enter a parse tree produced by ConfigurationParser#rangeSelector.
    def enterRangeSelector(self, ctx:ConfigurationParser.RangeSelectorContext):
        pass

    # Exit a parse tree produced by ConfigurationParser#rangeSelector.
    def exitRangeSelector(self, ctx:ConfigurationParser.RangeSelectorContext):
        pass


    # Enter a parse tree produced by ConfigurationParser#unitSpecification.
    def enterUnitSpecification(self, ctx:ConfigurationParser.UnitSpecificationContext):
        pass

    # Exit a parse tree produced by ConfigurationParser#unitSpecification.
    def exitUnitSpecification(self, ctx:ConfigurationParser.UnitSpecificationContext):
        pass


    # Enter a parse tree produced by ConfigurationParser#arithmeticExpression.
    def enterArithmeticExpression(self, ctx:ConfigurationParser.ArithmeticExpressionContext):
        pass

    # Exit a parse tree produced by ConfigurationParser#arithmeticExpression.
    def exitArithmeticExpression(self, ctx:ConfigurationParser.ArithmeticExpressionContext):
        pass


    # Enter a parse tree produced by ConfigurationParser#eAdditionOperator.
    def enterEAdditionOperator(self, ctx:ConfigurationParser.EAdditionOperatorContext):
        pass

    # Exit a parse tree produced by ConfigurationParser#eAdditionOperator.
    def exitEAdditionOperator(self, ctx:ConfigurationParser.EAdditionOperatorContext):
        pass


    # Enter a parse tree produced by ConfigurationParser#multiplicationExpression.
    def enterMultiplicationExpression(self, ctx:ConfigurationParser.MultiplicationExpressionContext):
        pass

    # Exit a parse tree produced by ConfigurationParser#multiplicationExpression.
    def exitMultiplicationExpression(self, ctx:ConfigurationParser.MultiplicationExpressionContext):
        pass


    # Enter a parse tree produced by ConfigurationParser#eMultiplicationOperator.
    def enterEMultiplicationOperator(self, ctx:ConfigurationParser.EMultiplicationOperatorContext):
        pass

    # Exit a parse tree produced by ConfigurationParser#eMultiplicationOperator.
    def exitEMultiplicationOperator(self, ctx:ConfigurationParser.EMultiplicationOperatorContext):
        pass


    # Enter a parse tree produced by ConfigurationParser#valueExpression.
    def enterValueExpression(self, ctx:ConfigurationParser.ValueExpressionContext):
        pass

    # Exit a parse tree produced by ConfigurationParser#valueExpression.
    def exitValueExpression(self, ctx:ConfigurationParser.ValueExpressionContext):
        pass


    # Enter a parse tree produced by ConfigurationParser#literalExpression.
    def enterLiteralExpression(self, ctx:ConfigurationParser.LiteralExpressionContext):
        pass

    # Exit a parse tree produced by ConfigurationParser#literalExpression.
    def exitLiteralExpression(self, ctx:ConfigurationParser.LiteralExpressionContext):
        pass


    # Enter a parse tree produced by ConfigurationParser#literal.
    def enterLiteral(self, ctx:ConfigurationParser.LiteralContext):
        pass

    # Exit a parse tree produced by ConfigurationParser#literal.
    def exitLiteral(self, ctx:ConfigurationParser.LiteralContext):
        pass


    # Enter a parse tree produced by ConfigurationParser#parenthesisExpression.
    def enterParenthesisExpression(self, ctx:ConfigurationParser.ParenthesisExpressionContext):
        pass

    # Exit a parse tree produced by ConfigurationParser#parenthesisExpression.
    def exitParenthesisExpression(self, ctx:ConfigurationParser.ParenthesisExpressionContext):
        pass


    # Enter a parse tree produced by ConfigurationParser#arrayExpression.
    def enterArrayExpression(self, ctx:ConfigurationParser.ArrayExpressionContext):
        pass

    # Exit a parse tree produced by ConfigurationParser#arrayExpression.
    def exitArrayExpression(self, ctx:ConfigurationParser.ArrayExpressionContext):
        pass


    # Enter a parse tree produced by ConfigurationParser#namedElementReference.
    def enterNamedElementReference(self, ctx:ConfigurationParser.NamedElementReferenceContext):
        pass

    # Exit a parse tree produced by ConfigurationParser#namedElementReference.
    def exitNamedElementReference(self, ctx:ConfigurationParser.NamedElementReferenceContext):
        pass


    # Enter a parse tree produced by ConfigurationParser#stringValue.
    def enterStringValue(self, ctx:ConfigurationParser.StringValueContext):
        pass

    # Exit a parse tree produced by ConfigurationParser#stringValue.
    def exitStringValue(self, ctx:ConfigurationParser.StringValueContext):
        pass


    # Enter a parse tree produced by ConfigurationParser#longValue.
    def enterLongValue(self, ctx:ConfigurationParser.LongValueContext):
        pass

    # Exit a parse tree produced by ConfigurationParser#longValue.
    def exitLongValue(self, ctx:ConfigurationParser.LongValueContext):
        pass


    # Enter a parse tree produced by ConfigurationParser#doubleValue.
    def enterDoubleValue(self, ctx:ConfigurationParser.DoubleValueContext):
        pass

    # Exit a parse tree produced by ConfigurationParser#doubleValue.
    def exitDoubleValue(self, ctx:ConfigurationParser.DoubleValueContext):
        pass


    # Enter a parse tree produced by ConfigurationParser#booleanValue.
    def enterBooleanValue(self, ctx:ConfigurationParser.BooleanValueContext):
        pass

    # Exit a parse tree produced by ConfigurationParser#booleanValue.
    def exitBooleanValue(self, ctx:ConfigurationParser.BooleanValueContext):
        pass



del ConfigurationParser