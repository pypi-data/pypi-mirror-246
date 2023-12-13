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
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,31,212,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,1,0,1,0,1,0,1,0,1,0,5,0,54,8,
        0,10,0,12,0,57,9,0,1,0,1,0,1,0,1,0,5,0,63,8,0,10,0,12,0,66,9,0,3,
        0,68,8,0,1,0,1,0,5,0,72,8,0,10,0,12,0,75,9,0,1,1,1,1,1,1,1,2,3,2,
        81,8,2,1,2,1,2,1,3,1,3,1,3,1,3,1,3,1,3,1,3,5,3,92,8,3,10,3,12,3,
        95,9,3,3,3,97,8,3,1,3,1,3,5,3,101,8,3,10,3,12,3,104,9,3,1,3,1,3,
        1,4,1,4,1,4,1,4,5,4,112,8,4,10,4,12,4,115,9,4,1,4,1,4,1,5,1,5,1,
        5,1,5,1,5,5,5,124,8,5,10,5,12,5,127,9,5,1,5,1,5,3,5,131,8,5,1,5,
        1,5,1,5,3,5,136,8,5,1,6,1,6,3,6,140,8,6,1,7,1,7,1,8,1,8,1,8,1,8,
        1,9,1,9,1,10,1,10,1,10,1,10,1,10,3,10,155,8,10,1,11,1,11,1,12,1,
        12,1,12,1,12,1,12,3,12,164,8,12,1,13,1,13,1,14,1,14,1,14,1,14,3,
        14,172,8,14,1,15,1,15,1,16,1,16,1,16,1,16,3,16,180,8,16,1,17,1,17,
        1,17,1,17,1,18,1,18,1,18,1,18,5,18,190,8,18,10,18,12,18,193,9,18,
        3,18,195,8,18,1,18,1,18,1,19,1,19,1,19,3,19,202,8,19,1,20,1,20,1,
        21,1,21,1,22,1,22,1,23,1,23,1,23,0,0,24,0,2,4,6,8,10,12,14,16,18,
        20,22,24,26,28,30,32,34,36,38,40,42,44,46,0,2,1,0,13,14,1,0,15,17,
        213,0,48,1,0,0,0,2,76,1,0,0,0,4,80,1,0,0,0,6,84,1,0,0,0,8,107,1,
        0,0,0,10,118,1,0,0,0,12,139,1,0,0,0,14,141,1,0,0,0,16,143,1,0,0,
        0,18,147,1,0,0,0,20,154,1,0,0,0,22,156,1,0,0,0,24,163,1,0,0,0,26,
        165,1,0,0,0,28,171,1,0,0,0,30,173,1,0,0,0,32,179,1,0,0,0,34,181,
        1,0,0,0,36,185,1,0,0,0,38,198,1,0,0,0,40,203,1,0,0,0,42,205,1,0,
        0,0,44,207,1,0,0,0,46,209,1,0,0,0,48,49,5,1,0,0,49,50,5,21,0,0,50,
        51,5,2,0,0,51,55,5,21,0,0,52,54,3,2,1,0,53,52,1,0,0,0,54,57,1,0,
        0,0,55,53,1,0,0,0,55,56,1,0,0,0,56,67,1,0,0,0,57,55,1,0,0,0,58,59,
        5,3,0,0,59,64,3,4,2,0,60,61,5,4,0,0,61,63,3,4,2,0,62,60,1,0,0,0,
        63,66,1,0,0,0,64,62,1,0,0,0,64,65,1,0,0,0,65,68,1,0,0,0,66,64,1,
        0,0,0,67,58,1,0,0,0,67,68,1,0,0,0,68,73,1,0,0,0,69,72,3,8,4,0,70,
        72,3,6,3,0,71,69,1,0,0,0,71,70,1,0,0,0,72,75,1,0,0,0,73,71,1,0,0,
        0,73,74,1,0,0,0,74,1,1,0,0,0,75,73,1,0,0,0,76,77,5,5,0,0,77,78,5,
        22,0,0,78,3,1,0,0,0,79,81,5,6,0,0,80,79,1,0,0,0,80,81,1,0,0,0,81,
        82,1,0,0,0,82,83,5,21,0,0,83,5,1,0,0,0,84,85,5,7,0,0,85,86,5,21,
        0,0,86,96,5,8,0,0,87,88,5,3,0,0,88,93,3,4,2,0,89,90,5,4,0,0,90,92,
        3,4,2,0,91,89,1,0,0,0,92,95,1,0,0,0,93,91,1,0,0,0,93,94,1,0,0,0,
        94,97,1,0,0,0,95,93,1,0,0,0,96,87,1,0,0,0,96,97,1,0,0,0,97,102,1,
        0,0,0,98,101,3,8,4,0,99,101,3,6,3,0,100,98,1,0,0,0,100,99,1,0,0,
        0,101,104,1,0,0,0,102,100,1,0,0,0,102,103,1,0,0,0,103,105,1,0,0,
        0,104,102,1,0,0,0,105,106,5,9,0,0,106,7,1,0,0,0,107,108,5,10,0,0,
        108,109,5,21,0,0,109,113,5,8,0,0,110,112,3,10,5,0,111,110,1,0,0,
        0,112,115,1,0,0,0,113,111,1,0,0,0,113,114,1,0,0,0,114,116,1,0,0,
        0,115,113,1,0,0,0,116,117,5,9,0,0,117,9,1,0,0,0,118,130,5,22,0,0,
        119,120,5,11,0,0,120,125,3,12,6,0,121,122,5,4,0,0,122,124,3,12,6,
        0,123,121,1,0,0,0,124,127,1,0,0,0,125,123,1,0,0,0,125,126,1,0,0,
        0,126,128,1,0,0,0,127,125,1,0,0,0,128,129,5,12,0,0,129,131,1,0,0,
        0,130,119,1,0,0,0,130,131,1,0,0,0,131,132,1,0,0,0,132,133,5,2,0,
        0,133,135,3,20,10,0,134,136,3,18,9,0,135,134,1,0,0,0,135,136,1,0,
        0,0,136,11,1,0,0,0,137,140,3,14,7,0,138,140,3,16,8,0,139,137,1,0,
        0,0,139,138,1,0,0,0,140,13,1,0,0,0,141,142,5,23,0,0,142,15,1,0,0,
        0,143,144,5,23,0,0,144,145,5,2,0,0,145,146,5,23,0,0,146,17,1,0,0,
        0,147,148,5,21,0,0,148,19,1,0,0,0,149,150,3,24,12,0,150,151,3,22,
        11,0,151,152,3,20,10,0,152,155,1,0,0,0,153,155,3,24,12,0,154,149,
        1,0,0,0,154,153,1,0,0,0,155,21,1,0,0,0,156,157,7,0,0,0,157,23,1,
        0,0,0,158,159,3,28,14,0,159,160,3,26,13,0,160,161,3,24,12,0,161,
        164,1,0,0,0,162,164,3,28,14,0,163,158,1,0,0,0,163,162,1,0,0,0,164,
        25,1,0,0,0,165,166,7,1,0,0,166,27,1,0,0,0,167,172,3,34,17,0,168,
        172,3,38,19,0,169,172,3,36,18,0,170,172,3,30,15,0,171,167,1,0,0,
        0,171,168,1,0,0,0,171,169,1,0,0,0,171,170,1,0,0,0,172,29,1,0,0,0,
        173,174,3,32,16,0,174,31,1,0,0,0,175,180,3,40,20,0,176,180,3,42,
        21,0,177,180,3,44,22,0,178,180,3,46,23,0,179,175,1,0,0,0,179,176,
        1,0,0,0,179,177,1,0,0,0,179,178,1,0,0,0,180,33,1,0,0,0,181,182,5,
        18,0,0,182,183,3,20,10,0,183,184,5,19,0,0,184,35,1,0,0,0,185,194,
        5,11,0,0,186,191,3,20,10,0,187,188,5,4,0,0,188,190,3,20,10,0,189,
        187,1,0,0,0,190,193,1,0,0,0,191,189,1,0,0,0,191,192,1,0,0,0,192,
        195,1,0,0,0,193,191,1,0,0,0,194,186,1,0,0,0,194,195,1,0,0,0,195,
        196,1,0,0,0,196,197,5,12,0,0,197,37,1,0,0,0,198,201,5,21,0,0,199,
        200,5,20,0,0,200,202,5,21,0,0,201,199,1,0,0,0,201,202,1,0,0,0,202,
        39,1,0,0,0,203,204,5,27,0,0,204,41,1,0,0,0,205,206,5,23,0,0,206,
        43,1,0,0,0,207,208,5,24,0,0,208,45,1,0,0,0,209,210,5,25,0,0,210,
        47,1,0,0,0,22,55,64,67,71,73,80,93,96,100,102,113,125,130,135,139,
        154,163,171,179,191,194,201
    ]

class ConfigurationParser ( Parser ):

    grammarFileName = "Configuration.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'configuration'", "':'", "'activate'", 
                     "','", "'include'", "'!'", "'feature'", "'{'", "'}'", 
                     "'group'", "'['", "']'", "'+'", "'-'", "'*'", "'/'", 
                     "'%'", "'('", "')'", "'.'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "ID", "QualifiedName", "ELONG", "EDOUBLE", 
                      "EBoolean", "INT", "STRING", "WS", "ML_COMMENT", "SL_COMMENT", 
                      "ANY_OTHER" ]

    RULE_configurationModel = 0
    RULE_include = 1
    RULE_featureActivation = 2
    RULE_featureConfiguration = 3
    RULE_parameterGroup = 4
    RULE_parameterAssignment = 5
    RULE_selector = 6
    RULE_elementSelector = 7
    RULE_rangeSelector = 8
    RULE_unitSpecification = 9
    RULE_arithmeticExpression = 10
    RULE_eAdditionOperator = 11
    RULE_multiplicationExpression = 12
    RULE_eMultiplicationOperator = 13
    RULE_valueExpression = 14
    RULE_literalExpression = 15
    RULE_literal = 16
    RULE_parenthesisExpression = 17
    RULE_arrayExpression = 18
    RULE_namedElementReference = 19
    RULE_stringValue = 20
    RULE_longValue = 21
    RULE_doubleValue = 22
    RULE_booleanValue = 23

    ruleNames =  [ "configurationModel", "include", "featureActivation", 
                   "featureConfiguration", "parameterGroup", "parameterAssignment", 
                   "selector", "elementSelector", "rangeSelector", "unitSpecification", 
                   "arithmeticExpression", "eAdditionOperator", "multiplicationExpression", 
                   "eMultiplicationOperator", "valueExpression", "literalExpression", 
                   "literal", "parenthesisExpression", "arrayExpression", 
                   "namedElementReference", "stringValue", "longValue", 
                   "doubleValue", "booleanValue" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    T__11=12
    T__12=13
    T__13=14
    T__14=15
    T__15=16
    T__16=17
    T__17=18
    T__18=19
    T__19=20
    ID=21
    QualifiedName=22
    ELONG=23
    EDOUBLE=24
    EBoolean=25
    INT=26
    STRING=27
    WS=28
    ML_COMMENT=29
    SL_COMMENT=30
    ANY_OTHER=31

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.12.0")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ConfigurationModelContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.name = None # Token
            self.declarationModel = None # Token
            self._include = None # IncludeContext
            self.includes = list() # of IncludeContexts
            self._featureActivation = None # FeatureActivationContext
            self.featureActivations = list() # of FeatureActivationContexts
            self._parameterGroup = None # ParameterGroupContext
            self.parameterGroups = list() # of ParameterGroupContexts
            self._featureConfiguration = None # FeatureConfigurationContext
            self.featureConfigurations = list() # of FeatureConfigurationContexts

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(ConfigurationParser.ID)
            else:
                return self.getToken(ConfigurationParser.ID, i)

        def include(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ConfigurationParser.IncludeContext)
            else:
                return self.getTypedRuleContext(ConfigurationParser.IncludeContext,i)


        def featureActivation(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ConfigurationParser.FeatureActivationContext)
            else:
                return self.getTypedRuleContext(ConfigurationParser.FeatureActivationContext,i)


        def parameterGroup(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ConfigurationParser.ParameterGroupContext)
            else:
                return self.getTypedRuleContext(ConfigurationParser.ParameterGroupContext,i)


        def featureConfiguration(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ConfigurationParser.FeatureConfigurationContext)
            else:
                return self.getTypedRuleContext(ConfigurationParser.FeatureConfigurationContext,i)


        def getRuleIndex(self):
            return ConfigurationParser.RULE_configurationModel

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConfigurationModel" ):
                listener.enterConfigurationModel(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConfigurationModel" ):
                listener.exitConfigurationModel(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConfigurationModel" ):
                return visitor.visitConfigurationModel(self)
            else:
                return visitor.visitChildren(self)




    def configurationModel(self):

        localctx = ConfigurationParser.ConfigurationModelContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_configurationModel)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 48
            self.match(ConfigurationParser.T__0)
            self.state = 49
            localctx.name = self.match(ConfigurationParser.ID)
            self.state = 50
            self.match(ConfigurationParser.T__1)
            self.state = 51
            localctx.declarationModel = self.match(ConfigurationParser.ID)
            self.state = 55
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==5:
                self.state = 52
                localctx._include = self.include()
                localctx.includes.append(localctx._include)
                self.state = 57
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 67
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==3:
                self.state = 58
                self.match(ConfigurationParser.T__2)
                self.state = 59
                localctx._featureActivation = self.featureActivation()
                localctx.featureActivations.append(localctx._featureActivation)
                self.state = 64
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==4:
                    self.state = 60
                    self.match(ConfigurationParser.T__3)
                    self.state = 61
                    localctx._featureActivation = self.featureActivation()
                    localctx.featureActivations.append(localctx._featureActivation)
                    self.state = 66
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 73
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==7 or _la==10:
                self.state = 71
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [10]:
                    self.state = 69
                    localctx._parameterGroup = self.parameterGroup()
                    localctx.parameterGroups.append(localctx._parameterGroup)
                    pass
                elif token in [7]:
                    self.state = 70
                    localctx._featureConfiguration = self.featureConfiguration()
                    localctx.featureConfigurations.append(localctx._featureConfiguration)
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 75
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IncludeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.importedNamespace = None # Token

        def QualifiedName(self):
            return self.getToken(ConfigurationParser.QualifiedName, 0)

        def getRuleIndex(self):
            return ConfigurationParser.RULE_include

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInclude" ):
                listener.enterInclude(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInclude" ):
                listener.exitInclude(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInclude" ):
                return visitor.visitInclude(self)
            else:
                return visitor.visitChildren(self)




    def include(self):

        localctx = ConfigurationParser.IncludeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_include)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 76
            self.match(ConfigurationParser.T__4)
            self.state = 77
            localctx.importedNamespace = self.match(ConfigurationParser.QualifiedName)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FeatureActivationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.deactivated = None # Token
            self.declaration = None # Token

        def ID(self):
            return self.getToken(ConfigurationParser.ID, 0)

        def getRuleIndex(self):
            return ConfigurationParser.RULE_featureActivation

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFeatureActivation" ):
                listener.enterFeatureActivation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFeatureActivation" ):
                listener.exitFeatureActivation(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFeatureActivation" ):
                return visitor.visitFeatureActivation(self)
            else:
                return visitor.visitChildren(self)




    def featureActivation(self):

        localctx = ConfigurationParser.FeatureActivationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_featureActivation)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 80
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==6:
                self.state = 79
                localctx.deactivated = self.match(ConfigurationParser.T__5)


            self.state = 82
            localctx.declaration = self.match(ConfigurationParser.ID)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FeatureConfigurationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.declaration = None # Token
            self._featureActivation = None # FeatureActivationContext
            self.featureActivations = list() # of FeatureActivationContexts
            self._parameterGroup = None # ParameterGroupContext
            self.parameterGroups = list() # of ParameterGroupContexts
            self._featureConfiguration = None # FeatureConfigurationContext
            self.featureConfigurations = list() # of FeatureConfigurationContexts

        def ID(self):
            return self.getToken(ConfigurationParser.ID, 0)

        def featureActivation(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ConfigurationParser.FeatureActivationContext)
            else:
                return self.getTypedRuleContext(ConfigurationParser.FeatureActivationContext,i)


        def parameterGroup(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ConfigurationParser.ParameterGroupContext)
            else:
                return self.getTypedRuleContext(ConfigurationParser.ParameterGroupContext,i)


        def featureConfiguration(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ConfigurationParser.FeatureConfigurationContext)
            else:
                return self.getTypedRuleContext(ConfigurationParser.FeatureConfigurationContext,i)


        def getRuleIndex(self):
            return ConfigurationParser.RULE_featureConfiguration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFeatureConfiguration" ):
                listener.enterFeatureConfiguration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFeatureConfiguration" ):
                listener.exitFeatureConfiguration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFeatureConfiguration" ):
                return visitor.visitFeatureConfiguration(self)
            else:
                return visitor.visitChildren(self)




    def featureConfiguration(self):

        localctx = ConfigurationParser.FeatureConfigurationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_featureConfiguration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 84
            self.match(ConfigurationParser.T__6)
            self.state = 85
            localctx.declaration = self.match(ConfigurationParser.ID)
            self.state = 86
            self.match(ConfigurationParser.T__7)
            self.state = 96
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==3:
                self.state = 87
                self.match(ConfigurationParser.T__2)
                self.state = 88
                localctx._featureActivation = self.featureActivation()
                localctx.featureActivations.append(localctx._featureActivation)
                self.state = 93
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==4:
                    self.state = 89
                    self.match(ConfigurationParser.T__3)
                    self.state = 90
                    localctx._featureActivation = self.featureActivation()
                    localctx.featureActivations.append(localctx._featureActivation)
                    self.state = 95
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 102
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==7 or _la==10:
                self.state = 100
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [10]:
                    self.state = 98
                    localctx._parameterGroup = self.parameterGroup()
                    localctx.parameterGroups.append(localctx._parameterGroup)
                    pass
                elif token in [7]:
                    self.state = 99
                    localctx._featureConfiguration = self.featureConfiguration()
                    localctx.featureConfigurations.append(localctx._featureConfiguration)
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 104
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 105
            self.match(ConfigurationParser.T__8)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParameterGroupContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.declaration = None # Token
            self._parameterAssignment = None # ParameterAssignmentContext
            self.parameters = list() # of ParameterAssignmentContexts

        def ID(self):
            return self.getToken(ConfigurationParser.ID, 0)

        def parameterAssignment(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ConfigurationParser.ParameterAssignmentContext)
            else:
                return self.getTypedRuleContext(ConfigurationParser.ParameterAssignmentContext,i)


        def getRuleIndex(self):
            return ConfigurationParser.RULE_parameterGroup

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParameterGroup" ):
                listener.enterParameterGroup(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParameterGroup" ):
                listener.exitParameterGroup(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParameterGroup" ):
                return visitor.visitParameterGroup(self)
            else:
                return visitor.visitChildren(self)




    def parameterGroup(self):

        localctx = ConfigurationParser.ParameterGroupContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_parameterGroup)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 107
            self.match(ConfigurationParser.T__9)
            self.state = 108
            localctx.declaration = self.match(ConfigurationParser.ID)
            self.state = 109
            self.match(ConfigurationParser.T__7)
            self.state = 113
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==22:
                self.state = 110
                localctx._parameterAssignment = self.parameterAssignment()
                localctx.parameters.append(localctx._parameterAssignment)
                self.state = 115
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 116
            self.match(ConfigurationParser.T__8)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParameterAssignmentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.declaration = None # Token
            self._selector = None # SelectorContext
            self.selectors = list() # of SelectorContexts
            self.value = None # ArithmeticExpressionContext
            self.unit = None # UnitSpecificationContext

        def QualifiedName(self):
            return self.getToken(ConfigurationParser.QualifiedName, 0)

        def arithmeticExpression(self):
            return self.getTypedRuleContext(ConfigurationParser.ArithmeticExpressionContext,0)


        def selector(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ConfigurationParser.SelectorContext)
            else:
                return self.getTypedRuleContext(ConfigurationParser.SelectorContext,i)


        def unitSpecification(self):
            return self.getTypedRuleContext(ConfigurationParser.UnitSpecificationContext,0)


        def getRuleIndex(self):
            return ConfigurationParser.RULE_parameterAssignment

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParameterAssignment" ):
                listener.enterParameterAssignment(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParameterAssignment" ):
                listener.exitParameterAssignment(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParameterAssignment" ):
                return visitor.visitParameterAssignment(self)
            else:
                return visitor.visitChildren(self)




    def parameterAssignment(self):

        localctx = ConfigurationParser.ParameterAssignmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_parameterAssignment)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 118
            localctx.declaration = self.match(ConfigurationParser.QualifiedName)
            self.state = 130
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==11:
                self.state = 119
                self.match(ConfigurationParser.T__10)
                self.state = 120
                localctx._selector = self.selector()
                localctx.selectors.append(localctx._selector)
                self.state = 125
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==4:
                    self.state = 121
                    self.match(ConfigurationParser.T__3)
                    self.state = 122
                    localctx._selector = self.selector()
                    localctx.selectors.append(localctx._selector)
                    self.state = 127
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 128
                self.match(ConfigurationParser.T__11)


            self.state = 132
            self.match(ConfigurationParser.T__1)
            self.state = 133
            localctx.value = self.arithmeticExpression()
            self.state = 135
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==21:
                self.state = 134
                localctx.unit = self.unitSpecification()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SelectorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def elementSelector(self):
            return self.getTypedRuleContext(ConfigurationParser.ElementSelectorContext,0)


        def rangeSelector(self):
            return self.getTypedRuleContext(ConfigurationParser.RangeSelectorContext,0)


        def getRuleIndex(self):
            return ConfigurationParser.RULE_selector

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSelector" ):
                listener.enterSelector(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSelector" ):
                listener.exitSelector(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSelector" ):
                return visitor.visitSelector(self)
            else:
                return visitor.visitChildren(self)




    def selector(self):

        localctx = ConfigurationParser.SelectorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_selector)
        try:
            self.state = 139
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,14,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 137
                self.elementSelector()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 138
                self.rangeSelector()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ElementSelectorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.element = None # Token

        def ELONG(self):
            return self.getToken(ConfigurationParser.ELONG, 0)

        def getRuleIndex(self):
            return ConfigurationParser.RULE_elementSelector

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterElementSelector" ):
                listener.enterElementSelector(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitElementSelector" ):
                listener.exitElementSelector(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitElementSelector" ):
                return visitor.visitElementSelector(self)
            else:
                return visitor.visitChildren(self)




    def elementSelector(self):

        localctx = ConfigurationParser.ElementSelectorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_elementSelector)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 141
            localctx.element = self.match(ConfigurationParser.ELONG)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RangeSelectorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.lowerBound = None # Token
            self.upperBound = None # Token

        def ELONG(self, i:int=None):
            if i is None:
                return self.getTokens(ConfigurationParser.ELONG)
            else:
                return self.getToken(ConfigurationParser.ELONG, i)

        def getRuleIndex(self):
            return ConfigurationParser.RULE_rangeSelector

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRangeSelector" ):
                listener.enterRangeSelector(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRangeSelector" ):
                listener.exitRangeSelector(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRangeSelector" ):
                return visitor.visitRangeSelector(self)
            else:
                return visitor.visitChildren(self)




    def rangeSelector(self):

        localctx = ConfigurationParser.RangeSelectorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_rangeSelector)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 143
            localctx.lowerBound = self.match(ConfigurationParser.ELONG)
            self.state = 144
            self.match(ConfigurationParser.T__1)
            self.state = 145
            localctx.upperBound = self.match(ConfigurationParser.ELONG)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UnitSpecificationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.unit = None # Token

        def ID(self):
            return self.getToken(ConfigurationParser.ID, 0)

        def getRuleIndex(self):
            return ConfigurationParser.RULE_unitSpecification

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnitSpecification" ):
                listener.enterUnitSpecification(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnitSpecification" ):
                listener.exitUnitSpecification(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnitSpecification" ):
                return visitor.visitUnitSpecification(self)
            else:
                return visitor.visitChildren(self)




    def unitSpecification(self):

        localctx = ConfigurationParser.UnitSpecificationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_unitSpecification)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 147
            localctx.unit = self.match(ConfigurationParser.ID)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArithmeticExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.left = None # MultiplicationExpressionContext
            self.op = None # EAdditionOperatorContext
            self.right = None # ArithmeticExpressionContext

        def multiplicationExpression(self):
            return self.getTypedRuleContext(ConfigurationParser.MultiplicationExpressionContext,0)


        def eAdditionOperator(self):
            return self.getTypedRuleContext(ConfigurationParser.EAdditionOperatorContext,0)


        def arithmeticExpression(self):
            return self.getTypedRuleContext(ConfigurationParser.ArithmeticExpressionContext,0)


        def getRuleIndex(self):
            return ConfigurationParser.RULE_arithmeticExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArithmeticExpression" ):
                listener.enterArithmeticExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArithmeticExpression" ):
                listener.exitArithmeticExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArithmeticExpression" ):
                return visitor.visitArithmeticExpression(self)
            else:
                return visitor.visitChildren(self)




    def arithmeticExpression(self):

        localctx = ConfigurationParser.ArithmeticExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_arithmeticExpression)
        try:
            self.state = 154
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,15,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 149
                localctx.left = self.multiplicationExpression()
                self.state = 150
                localctx.op = self.eAdditionOperator()
                self.state = 151
                localctx.right = self.arithmeticExpression()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 153
                self.multiplicationExpression()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class EAdditionOperatorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return ConfigurationParser.RULE_eAdditionOperator

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEAdditionOperator" ):
                listener.enterEAdditionOperator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEAdditionOperator" ):
                listener.exitEAdditionOperator(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEAdditionOperator" ):
                return visitor.visitEAdditionOperator(self)
            else:
                return visitor.visitChildren(self)




    def eAdditionOperator(self):

        localctx = ConfigurationParser.EAdditionOperatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_eAdditionOperator)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 156
            _la = self._input.LA(1)
            if not(_la==13 or _la==14):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MultiplicationExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.left = None # ValueExpressionContext
            self.op = None # EMultiplicationOperatorContext
            self.right = None # MultiplicationExpressionContext

        def valueExpression(self):
            return self.getTypedRuleContext(ConfigurationParser.ValueExpressionContext,0)


        def eMultiplicationOperator(self):
            return self.getTypedRuleContext(ConfigurationParser.EMultiplicationOperatorContext,0)


        def multiplicationExpression(self):
            return self.getTypedRuleContext(ConfigurationParser.MultiplicationExpressionContext,0)


        def getRuleIndex(self):
            return ConfigurationParser.RULE_multiplicationExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMultiplicationExpression" ):
                listener.enterMultiplicationExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMultiplicationExpression" ):
                listener.exitMultiplicationExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMultiplicationExpression" ):
                return visitor.visitMultiplicationExpression(self)
            else:
                return visitor.visitChildren(self)




    def multiplicationExpression(self):

        localctx = ConfigurationParser.MultiplicationExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_multiplicationExpression)
        try:
            self.state = 163
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,16,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 158
                localctx.left = self.valueExpression()
                self.state = 159
                localctx.op = self.eMultiplicationOperator()
                self.state = 160
                localctx.right = self.multiplicationExpression()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 162
                self.valueExpression()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class EMultiplicationOperatorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return ConfigurationParser.RULE_eMultiplicationOperator

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEMultiplicationOperator" ):
                listener.enterEMultiplicationOperator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEMultiplicationOperator" ):
                listener.exitEMultiplicationOperator(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEMultiplicationOperator" ):
                return visitor.visitEMultiplicationOperator(self)
            else:
                return visitor.visitChildren(self)




    def eMultiplicationOperator(self):

        localctx = ConfigurationParser.EMultiplicationOperatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_eMultiplicationOperator)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 165
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 229376) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ValueExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def parenthesisExpression(self):
            return self.getTypedRuleContext(ConfigurationParser.ParenthesisExpressionContext,0)


        def namedElementReference(self):
            return self.getTypedRuleContext(ConfigurationParser.NamedElementReferenceContext,0)


        def arrayExpression(self):
            return self.getTypedRuleContext(ConfigurationParser.ArrayExpressionContext,0)


        def literalExpression(self):
            return self.getTypedRuleContext(ConfigurationParser.LiteralExpressionContext,0)


        def getRuleIndex(self):
            return ConfigurationParser.RULE_valueExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterValueExpression" ):
                listener.enterValueExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitValueExpression" ):
                listener.exitValueExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitValueExpression" ):
                return visitor.visitValueExpression(self)
            else:
                return visitor.visitChildren(self)




    def valueExpression(self):

        localctx = ConfigurationParser.ValueExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_valueExpression)
        try:
            self.state = 171
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [18]:
                self.enterOuterAlt(localctx, 1)
                self.state = 167
                self.parenthesisExpression()
                pass
            elif token in [21]:
                self.enterOuterAlt(localctx, 2)
                self.state = 168
                self.namedElementReference()
                pass
            elif token in [11]:
                self.enterOuterAlt(localctx, 3)
                self.state = 169
                self.arrayExpression()
                pass
            elif token in [23, 24, 25, 27]:
                self.enterOuterAlt(localctx, 4)
                self.state = 170
                self.literalExpression()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LiteralExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.value = None # LiteralContext

        def literal(self):
            return self.getTypedRuleContext(ConfigurationParser.LiteralContext,0)


        def getRuleIndex(self):
            return ConfigurationParser.RULE_literalExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLiteralExpression" ):
                listener.enterLiteralExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLiteralExpression" ):
                listener.exitLiteralExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLiteralExpression" ):
                return visitor.visitLiteralExpression(self)
            else:
                return visitor.visitChildren(self)




    def literalExpression(self):

        localctx = ConfigurationParser.LiteralExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_literalExpression)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 173
            localctx.value = self.literal()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def stringValue(self):
            return self.getTypedRuleContext(ConfigurationParser.StringValueContext,0)


        def longValue(self):
            return self.getTypedRuleContext(ConfigurationParser.LongValueContext,0)


        def doubleValue(self):
            return self.getTypedRuleContext(ConfigurationParser.DoubleValueContext,0)


        def booleanValue(self):
            return self.getTypedRuleContext(ConfigurationParser.BooleanValueContext,0)


        def getRuleIndex(self):
            return ConfigurationParser.RULE_literal

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLiteral" ):
                listener.enterLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLiteral" ):
                listener.exitLiteral(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLiteral" ):
                return visitor.visitLiteral(self)
            else:
                return visitor.visitChildren(self)




    def literal(self):

        localctx = ConfigurationParser.LiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_literal)
        try:
            self.state = 179
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [27]:
                self.enterOuterAlt(localctx, 1)
                self.state = 175
                self.stringValue()
                pass
            elif token in [23]:
                self.enterOuterAlt(localctx, 2)
                self.state = 176
                self.longValue()
                pass
            elif token in [24]:
                self.enterOuterAlt(localctx, 3)
                self.state = 177
                self.doubleValue()
                pass
            elif token in [25]:
                self.enterOuterAlt(localctx, 4)
                self.state = 178
                self.booleanValue()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParenthesisExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.expression = None # ArithmeticExpressionContext

        def arithmeticExpression(self):
            return self.getTypedRuleContext(ConfigurationParser.ArithmeticExpressionContext,0)


        def getRuleIndex(self):
            return ConfigurationParser.RULE_parenthesisExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParenthesisExpression" ):
                listener.enterParenthesisExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParenthesisExpression" ):
                listener.exitParenthesisExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParenthesisExpression" ):
                return visitor.visitParenthesisExpression(self)
            else:
                return visitor.visitChildren(self)




    def parenthesisExpression(self):

        localctx = ConfigurationParser.ParenthesisExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_parenthesisExpression)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 181
            self.match(ConfigurationParser.T__17)
            self.state = 182
            localctx.expression = self.arithmeticExpression()
            self.state = 183
            self.match(ConfigurationParser.T__18)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArrayExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self._arithmeticExpression = None # ArithmeticExpressionContext
            self.elements = list() # of ArithmeticExpressionContexts

        def arithmeticExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ConfigurationParser.ArithmeticExpressionContext)
            else:
                return self.getTypedRuleContext(ConfigurationParser.ArithmeticExpressionContext,i)


        def getRuleIndex(self):
            return ConfigurationParser.RULE_arrayExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArrayExpression" ):
                listener.enterArrayExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArrayExpression" ):
                listener.exitArrayExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArrayExpression" ):
                return visitor.visitArrayExpression(self)
            else:
                return visitor.visitChildren(self)




    def arrayExpression(self):

        localctx = ConfigurationParser.ArrayExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_arrayExpression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 185
            self.match(ConfigurationParser.T__10)
            self.state = 194
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 195299328) != 0):
                self.state = 186
                localctx._arithmeticExpression = self.arithmeticExpression()
                localctx.elements.append(localctx._arithmeticExpression)
                self.state = 191
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==4:
                    self.state = 187
                    self.match(ConfigurationParser.T__3)
                    self.state = 188
                    localctx._arithmeticExpression = self.arithmeticExpression()
                    localctx.elements.append(localctx._arithmeticExpression)
                    self.state = 193
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 196
            self.match(ConfigurationParser.T__11)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NamedElementReferenceContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.element = None # Token
            self.attribute = None # Token

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(ConfigurationParser.ID)
            else:
                return self.getToken(ConfigurationParser.ID, i)

        def getRuleIndex(self):
            return ConfigurationParser.RULE_namedElementReference

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNamedElementReference" ):
                listener.enterNamedElementReference(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNamedElementReference" ):
                listener.exitNamedElementReference(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNamedElementReference" ):
                return visitor.visitNamedElementReference(self)
            else:
                return visitor.visitChildren(self)




    def namedElementReference(self):

        localctx = ConfigurationParser.NamedElementReferenceContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_namedElementReference)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 198
            localctx.element = self.match(ConfigurationParser.ID)
            self.state = 201
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==20:
                self.state = 199
                self.match(ConfigurationParser.T__19)
                self.state = 200
                localctx.attribute = self.match(ConfigurationParser.ID)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StringValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.value = None # Token

        def STRING(self):
            return self.getToken(ConfigurationParser.STRING, 0)

        def getRuleIndex(self):
            return ConfigurationParser.RULE_stringValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStringValue" ):
                listener.enterStringValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStringValue" ):
                listener.exitStringValue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStringValue" ):
                return visitor.visitStringValue(self)
            else:
                return visitor.visitChildren(self)




    def stringValue(self):

        localctx = ConfigurationParser.StringValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_stringValue)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 203
            localctx.value = self.match(ConfigurationParser.STRING)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LongValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.value = None # Token

        def ELONG(self):
            return self.getToken(ConfigurationParser.ELONG, 0)

        def getRuleIndex(self):
            return ConfigurationParser.RULE_longValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLongValue" ):
                listener.enterLongValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLongValue" ):
                listener.exitLongValue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLongValue" ):
                return visitor.visitLongValue(self)
            else:
                return visitor.visitChildren(self)




    def longValue(self):

        localctx = ConfigurationParser.LongValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_longValue)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 205
            localctx.value = self.match(ConfigurationParser.ELONG)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DoubleValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.value = None # Token

        def EDOUBLE(self):
            return self.getToken(ConfigurationParser.EDOUBLE, 0)

        def getRuleIndex(self):
            return ConfigurationParser.RULE_doubleValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDoubleValue" ):
                listener.enterDoubleValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDoubleValue" ):
                listener.exitDoubleValue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDoubleValue" ):
                return visitor.visitDoubleValue(self)
            else:
                return visitor.visitChildren(self)




    def doubleValue(self):

        localctx = ConfigurationParser.DoubleValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_doubleValue)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 207
            localctx.value = self.match(ConfigurationParser.EDOUBLE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BooleanValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.value = None # Token

        def EBoolean(self):
            return self.getToken(ConfigurationParser.EBoolean, 0)

        def getRuleIndex(self):
            return ConfigurationParser.RULE_booleanValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBooleanValue" ):
                listener.enterBooleanValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBooleanValue" ):
                listener.exitBooleanValue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBooleanValue" ):
                return visitor.visitBooleanValue(self)
            else:
                return visitor.visitChildren(self)




    def booleanValue(self):

        localctx = ConfigurationParser.BooleanValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_booleanValue)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 209
            localctx.value = self.match(ConfigurationParser.EBoolean)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





