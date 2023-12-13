"""Port of antlr-c3 typescript library to python"""

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

# !!!!!ONLY HERE CAUSED TO PYTHON -> fast upload to pypi to not redudance code!!!!!

__author__ = 'sgu'

# TODO license

#
#  The c3 engine is able to provide code completion candidates useful for
#  editors with ANTLR generated parsers, independent of the actual
#  language/grammar used for the generation.
#

# TODO configure module
# package: com.vmware.antlr4c3

# utils
import logging
from dataclasses import dataclass, field
from typing import Dict, Set, List

# antlr imports
# TODO check range structure
#  https://stackoverflow.com/q/57356723/
from antlr4.IntervalSet import IntervalSet
from antlr4.Parser import Parser
from antlr4.Token import Token
from antlr4.BufferedTokenStream import TokenStream
from antlr4.ParserRuleContext import ParserRuleContext
from antlr4.atn.ATN import ATN
from antlr4.atn.ATNState import ATNState, RuleStartState
from antlr4.atn.Transition import Transition, PredicateTransition, RuleTransition, PrecedencePredicateTransition, WildcardTransition

# debug
logging.basicConfig( level=logging.DEBUG )

TokenList = List[int]
RuleList = List[int]


@dataclass
class CandidateRule:
    startTokenIndex: int
    ruleList: RuleList


@dataclass
class RuleWithStartToken:
    startTokenIndex: int
    ruleIndex: int


RuleWithStartTokenList = List[RuleWithStartToken]


@dataclass
class CandidatesCollection:
    """
    JDO returning information about matching tokens and rules

    All the candidates which have been found. Tokens and rules are separated. Token entries include a list of tokens
    that directly follow them (see also the "following" member in the FollowSetWithPath class). Rule entries include the
    index of the starting token within the evaluated rule, along with a call stack of rules found during evaluation.
    """

    # Collection of Token ID candidates, each with a follow-on List of subsequent tokens
    tokens: dict[int, TokenList] = field( default_factory=dict )
    # Collection of Rule candidates, each with the callstack of rules to reach the candidate
    rules: dict[int, CandidateRule] = field( default_factory=dict )

    def __str__(self):
        return str( 'CandidatesCollection{' + str( self.__dict__ ) + '}' )


@dataclass
class FollowSetWithPath:
    """
    A record for a follow set along with the path at which this set was found. If there is only a single symbol in the
    interval set then we also collect and store tokens which follow this symbol directly in its rule (i.e. there is no
    intermediate rule transition). Only single label transitions are considered. This is useful if you have a chain of
    tokens which can be suggested as a whole, because there is a fixed sequence in the grammar.
    """
    intervals: IntervalSet = field( default_factory=IntervalSet )
    path: RuleList = field( default_factory=list )
    following: TokenList = field( default_factory=list )


@dataclass
class FollowSetsHolder:
    """
    A list of follow sets (for a given state number) + all of them combined for quick hit tests. This data is static in
    nature (because the used ATN states are part of a static struct: the ATN). Hence, it can be shared between all C3
    instances, however it depends on the actual parser class (type).
    """
    sets: Set[FollowSetWithPath] = field( default_factory=set )
    combined: IntervalSet = IntervalSet()


FollowSetsPerState = Dict[int, FollowSetsHolder]

# Token stream position info after a rule was processed.
RuleEndStatus = Set[int]


@dataclass
class IPipelineEntry:
    state: ATNState
    tokenListIndex: int


def intervalSetToList(intervalSet: IntervalSet) -> List[int]:
    """
    Return an array containing the elements represented by the current set. The array is returned in ascending numerical
    order.
    """
    values: List = []
    for interval in intervalSet.intervals:
        start: int = interval.start
        stop: int = interval.stop

        # range upper limit is exclusive
        while start < stop:
            values.append( start )
            start += 1

    return values


class CodeCompletionCore:
    """
    The main class for doing the collection process.
    """
    followSetsByATN: dict[str, FollowSetsPerState] = {}

    atnStateTypeMap: List[str] = ["invalid", "basic", "rule start", "block start", "plus block start",
                                  "star block start",
                                  "token start", "rule stop", "block end", "star loop back", "star loop entry",
                                  "plus loop back",
                                  "loop end"]

    # Debugging options. Print human-readable ATN state and other info.

    # Not dependent on showDebugOutput. Prints the collected rules + tokens to terminal.
    showResult: bool
    # Enables printing ATN state info to terminal.
    showDebugOutput: bool
    # Only relevant when showDebugOutput is true. Enables transition printing for a state.
    debugOutputWithTransitions: bool
    # Also depends on showDebugOutput. Enables call stack printing for each rule recursion.
    showRuleStack: bool

    # Tailoring of the result:
    # Tokens which should not appear in the candidates set.
    ignoredTokens: Set[int]

    # Rules which replace any candidate token they contain.
    # This allows to return descriptive rules (e.g. className, instead of ID/identifier).
    preferredRules: Set[int]

    # Specify if preferred rules should be translated top-down (higher index rule returns first) or
    # bottom-up (lower index rule returns first).
    translateRulesTopDown: bool

    parser: Parser
    atn: ATN
    ruleNames: List[str]
    tokens: List[Token]
    literalNames: List[str]
    symbolicNames: List[str]
    precedenceStack: List[int]
    tokenStartIndex: int
    statesProcessed: int

    # A mapping of rule index to token stream position to end token positions.
    # A rule which has been visited before with the same input position will always produce the same output positions.
    shortcutMap: dict[int, dict[int, RuleEndStatus]]

    # The collected candidates (rules and tokens).
    candidates: CandidatesCollection = CandidatesCollection()

    def __init__(self, parser: Parser):
        self.parser = parser
        self.atn = parser.atn
        self.literalNames = parser.literalNames
        self.symbolicNames = parser.symbolicNames
        self.ruleNames = parser.ruleNames
        self.ignoredTokens = set()
        self.preferredRules = set()

        self.showResult = False
        self.showDebugOutput = False
        self.debugOutputWithTransitions = False
        self.showRuleStack = False
        self.translateRulesTopDown = True

        self.tokenStartIndex = 0
        self.statesProcessed = 0

        self.shortcutMap = {}

    logger = logging.getLogger( __name__ )

    def collectCandidates(self, caretTokenIndex: int, context: ParserRuleContext = None) -> CandidatesCollection:
        """
        This is the main entry point. The caret token index specifies the token stream index for the token which
        currently covers the caret (or any other position you want to get code completion candidates for).

        Optionally you can pass in a parser rule context which limits the ATN walk to only that or called rules.
        This can significantly speed up the retrieval process but might miss some candidates (if they are outside the
        given context).
        """
        self.shortcutMap.clear()
        self.candidates.rules.clear()
        self.candidates.tokens.clear()
        self.statesProcessed = 0
        self.precedenceStack = []

        self.tokenStartIndex = context.start.tokenIndex if context is not None else 0
        tokenStream: TokenStream = self.parser.getInputStream()

        self.tokens = []
        offset: int = self.tokenStartIndex
        while True:
            token: Token = tokenStream.get( offset )
            offset += 1
            if token.channel == Token.DEFAULT_CHANNEL:
                self.tokens.append( token )

                if token.tokenIndex >= caretTokenIndex or token.type == Token.EOF:
                    break

            # Do not check for the token index here, as we want to end with the first unhidden token on or after the
            # caret.
            if token.type == Token.EOF:
                break

        callStack: RuleWithStartTokenList = []
        startRule: int = context.ruleIndex if context is not None else 0
        self.processRule( self.atn.ruleToStartState[startRule], 0, callStack, 0, 0 )

        if self.showResult and self.logger.isEnabledFor( logging.DEBUG ):
            logMessage_list: List[str] = ["States processed: ", str( self.statesProcessed ), "\n\n",
                                          "Collected rules:\n"]
            for key, value in self.candidates.rules.items():
                logMessage_list.extend( [" / ", self.ruleNames[key], ", path: "] )

                for token in value.ruleList:
                    logMessage_list.extend( [self.ruleNames[token], " "] )

            sortedTokens: Set[str] = set()
            for key, valueList in self.candidates.tokens.items():
                symbol: str = IntervalSet.elementName( IntervalSet, self.literalNames, self.symbolicNames, key )
                for following in valueList:
                    symbol += " " + IntervalSet.elementName( IntervalSet, self.literalNames, self.symbolicNames,
                                                             following )
                sortedTokens.add( symbol )

            logMessage_list.append( "\n\nCollected Tokens:\n" )
            for symbol in sortedTokens:
                logMessage_list.extend( [symbol, "\n"] )
            logMessage_list.append( "\n\n" )

            self.logger.debug( ''.join( logMessage_list ) )

        return self.candidates

    def checkPredicate(self, transition: PredicateTransition) -> bool:
        """
        Check if the predicate associated with the given transition evaluates to true.
        """
        return transition.getPredicate().eval( self.parser, ParserRuleContext.EMPTY )

    def translateStackToRuleIndex(self, ruleWithStartTokenList: RuleWithStartTokenList) -> bool:
        """
        Walks the rule chain upwards or downwards (depending on translateRulesTopDown) to see if that matches any of the
        preferred rules. If found, that rule is added to the collection candidates and true is returned.
        """

        if len( self.preferredRules ) == 0:
            return False

        # Change the direction we iterate over the rule stack
        if self.translateRulesTopDown:
            #  Loop over the rule stack from lowest to highest rule level. This will prioritize a lower preferred rule
            #  if it is a child of a higher one that is also a preferred rule.
            i = len( ruleWithStartTokenList ) - 1
            while i >= 0:
                if self.translateToRuleIndex( i, ruleWithStartTokenList ):
                    return True
                i -= 1
        else:
            #  Loop over the rule stack from highest to lowest rule level. This will prioritize a higher preferred rule
            #  if it contains a lower one that is also a preferred rule.
            i = 0
            while i < len( ruleWithStartTokenList ):
                if self.translateToRuleIndex( i, ruleWithStartTokenList ):
                    return True
                i += 1

        return False

    def translateToRuleIndex(self, i: int, ruleStack: RuleWithStartTokenList) -> bool:
        """
        Given the index of a rule from a rule chain, check if that matches any of the preferred rules. If it matches,
        that rule is added to the collection candidates and true is returned.
        """
        ruleIndex: int = ruleStack[i].ruleIndex
        startTokenIndex: int = ruleStack[i].startTokenIndex

        if ruleIndex in self.preferredRules:
            # Add the rule to our candidates list along with the current rule path,
            # but only if there isn't already an entry like that.
            path: List[int] = list( map( (lambda x: x.ruleIndex), ruleStack[0:i] ) )
            addNew: bool = True
            for key, value in self.candidates.rules.items():
                if key != ruleIndex or len( value.ruleList ) != len( path ):
                    continue

                # Found an entry for this rule. Same path? If so don't add a new (duplicate) entry.
                if path == value.ruleList[0:len( path )]:
                    addNew = False
                    break

            if addNew:
                self.candidates.rules[ruleIndex] = CandidateRule( startTokenIndex, path )
                if self.showDebugOutput and self.logger.isEnabledFor( logging.DEBUG ):
                    self.logger.debug( "=====> collected: ", self.ruleNames[ruleIndex] )

            return True

        return False

    def getFollowingTokens(self, transition: Transition) -> List[int]:
        """
        This method follows the given transition and collects all symbols within the same rule that directly follow it
        without intermediate transitions to other rules and only if there is a single symbol for a transition.
        """
        result: List[int] = []

        pipeline: List[ATNState] = [transition.target]

        # TODO check pipeline not empty via
        #  while pipeline:
        while len( pipeline ) > 0:

            state: ATNState = pipeline.pop()

            if state:
                for outgoing in state.transitions:
                    if outgoing.serializationType == Transition.ATOM:
                        if not outgoing.isEpsilon:
                            outgoingList: List[int] = intervalSetToList( outgoing.label )
                            if len( outgoingList ) == 1 and not outgoingList[0] in self.ignoredTokens:
                                result.append( outgoingList[0] )
                                pipeline.append( outgoing.target )
                        else:
                            pipeline.append( outgoing.target )

        return result

    def determineFollowSets(self, start: ATNState, stop: ATNState) -> List[FollowSetWithPath]:
        """
        Entry point for the recursive follow set collection function.
        """
        result: List[FollowSetWithPath] = []
        stateStack: List[ATNState] = []
        ruleStack: List[int] = []
        self.collectFollowSets( start, stop, result, stateStack, ruleStack )

        return result

    def collectFollowSets(self, s: ATNState, stopState: ATNState, followSets: List[FollowSetWithPath],
                          stateStack: List[ATNState], ruleStack: List[int]):
        """
        Collects possible tokens which could be matched following the given ATN state. This is essentially the same
        algorithm as used in the LL1Analyzer class, but here we consider predicates also and use no parser rule context.
        """
        # TODO check lambda function
        #  stateStack.find((x) => x === s)
        if s in stateStack:
            return

        stateStack.append( s )

        if s == stopState or s.stateType == ATNState.RULE_STOP:
            followSet: FollowSetWithPath = FollowSetWithPath()
            followSet.intervals = IntervalSet()
            followSet.intervals.addOne( Token.EPSILON )
            followSet.path = ruleStack[:]  # .copy()
            followSets.append( followSet )
            stateStack.pop()

            return

        for transition in s.transitions:
            if transition.serializationType == Transition.RULE:
                ruleTransition: RuleTransition = transition
                # TODO check semantic eg skip the current iteration
                #  if ruleStack.index(ruleTransition.target.ruleIndex) != -1:
                if ruleTransition.target.ruleIndex in ruleStack:
                    continue

                ruleStack.append( ruleTransition.target.ruleIndex )
                self.collectFollowSets( transition.target, stopState, followSets, stateStack, ruleStack )
                ruleStack.pop()

            elif transition.serializationType == Transition.PREDICATE:
                if self.checkPredicate( transition ):
                    self.collectFollowSets( transition.target, stopState, followSets, stateStack, ruleStack )
            elif transition.isEpsilon:
                self.collectFollowSets( transition.target, stopState, followSets, stateStack, ruleStack )
            elif transition.serializationType == Transition.WILDCARD:
                followSet: FollowSetWithPath = FollowSetWithPath()
                followSet.intervals.addRange(
                    range( Token.MIN_USER_TOKEN_TYPE, self.atn.maxTokenType + 1 ) )  # range upper limit is exclusive
                followSet.path = ruleStack[:]  # .copy()
                followSets.append( followSet )
            else:
                label: IntervalSet = transition.label
                if label is not None and len( label ) > 0:
                    if transition.serializationType == Transition.NOT_SET:
                        label = label.complement( Token.MIN_USER_TOKEN_TYPE, self.atn.maxTokenType )
                    followSet: FollowSetWithPath = FollowSetWithPath()
                    followSet.intervals = label
                    followSet.path = ruleStack[:]  # .copy()
                    followSet.following = self.getFollowingTokens( transition )
                    followSets.append( followSet )

        stateStack.pop()

    def processRule(self, startState: RuleStartState, tokenListIndex: int, callStack: RuleWithStartTokenList,
                    precedence: int, indentation: int) -> RuleEndStatus:
        """
        Walks the ATN for a single rule only. It returns the token stream position for each path that could be matched
        in this rule. The result can be empty in case we hit only non-epsilon transitions that didn't match the current
        input or if we hit the caret position.
        """

        # Start with rule specific handling before going into the ATN walk.

        # Check first if we've taken this path with the same input before.
        positionMap: dict[int, RuleEndStatus] = self.shortcutMap.get( startState.ruleIndex )
        if positionMap is None:
            positionMap = {}
            self.shortcutMap[startState.ruleIndex] = positionMap
        else:
            if tokenListIndex in positionMap:
                if self.showDebugOutput and self.logger.isEnabledFor( logging.DEBUG ):
                    self.logger.debug( "=====> shortcut" )
                return positionMap.get( tokenListIndex )

        result: RuleEndStatus = set()

        #  For rule start states we determine and cache the follow set, which gives us 3 advantages:
        #  1) We can quickly check if a symbol would be matched when we follow that rule. We can so check in advance
        #     and can save us all the intermediate steps if there is no match.
        #  2) We'll have all symbols that are collectable already together when we are at the caret on rule enter.
        #  3) We get this lookup for free with any 2nd or further visit of the same rule, which often happens
        #     in non-trivial grammars, especially with (recursive) expressions and of course when invoking code
        #     completion multiple times.
        # TODO check class attribute CodeCompletionCore.followSetsByATN vs self.followSetsByATN
        setsPerState: FollowSetsPerState = self.followSetsByATN.get( self.parser.__class__.__name__ )
        if setsPerState is None:
            setsPerState = {}
            self.followSetsByATN[self.parser.__class__.__name__] = setsPerState

        followSets: FollowSetsHolder = setsPerState.get( startState.stateNumber )
        if followSets is None:
            followSets = FollowSetsHolder()
            setsPerState[startState.stateNumber] = followSets
            stop: ATNState = self.atn.ruleToStopState[startState.ruleIndex]
            followSets.sets = self.determineFollowSets( startState, stop )

            # Sets are split by path to allow translating them to preferred rules. But for quick hit tests
            # it is also useful to have a set with all symbols combined.
            combined: IntervalSet = IntervalSet()
            for followSet in followSets.sets:
                combined.addSet( followSet.intervals )
            followSets.combined = combined

        # Get the token index where our rule starts from our (possibly filtered) token list
        startTokenIndex: int = self.tokens[tokenListIndex].tokenIndex

        callStack.append( RuleWithStartToken( startTokenIndex, startState.ruleIndex ) )

        if tokenListIndex >= len( self.tokens ) - 1:  # At caret?
            if startState.ruleIndex in self.preferredRules:
                # No need to go deeper when collecting entries and we reach a rule that we want to collect anyway.
                self.translateStackToRuleIndex( callStack )
            else:
                # Convert all follow sets to either single symbols or their associated preferred rule and add
                # the result to our candidates list.
                for followSet in followSets.sets:
                    fullPath: RuleWithStartTokenList = callStack[:]  # .copy()

                    # Rules derived from our followSet will always start at the same token as our current rule
                    #  alternative: lambda path: RuleWithStartToken(startTokenIndex,path) for path in followSet.path
                    followSetPath = list(
                        map( (lambda path: RuleWithStartToken( startTokenIndex, path )), followSet.path ) )

                    fullPath.extend( followSetPath )
                    if not self.translateStackToRuleIndex( fullPath ):
                        for symbol in intervalSetToList( followSet.intervals ):
                            if not symbol in self.ignoredTokens:
                                if self.showDebugOutput and self.logger.isEnabledFor( logging.DEBUG ):
                                    self.logger.debug(
                                        "=====> collected: " + IntervalSet.elementName( IntervalSet, self.literalNames,
                                                                                        self.symbolicNames, symbol ) )
                                if not symbol in self.candidates.tokens:
                                    # Following is empty if there is more than one entry in the set.
                                    self.candidates.tokens[symbol] = followSet.following
                                else:
                                    # More than one following list for the same symbol.
                                    if self.candidates.tokens[symbol] != followSet.following:
                                        self.candidates.tokens[symbol] = []

            callStack.pop()

            return result

        else:
            # Process the rule if we either could pass it without consuming anything (epsilon transition)
            # or if the current input symbol will be matched somewhere after this entry point.
            # Otherwise, stop here.
            currentSymbol: int = self.tokens[tokenListIndex].type
            if not Token.EPSILON in followSets.combined and not currentSymbol in followSets.combined:
                callStack.pop()

                return result

        if startState.isPrecedenceRule:
            self.precedenceStack.append( precedence )

        # The current state execution pipeline contains all yet-to-be-processed ATN states in this rule.
        # For each such state we store the token index + a list of rules that lead to it.
        statePipeline: List[IPipelineEntry] = []
        currentEntry: IPipelineEntry

        # Bootstrap the pipeline.
        statePipeline.append( IPipelineEntry( startState, tokenListIndex ) )

        while len( statePipeline ) > 0:
            currentEntry = statePipeline.pop()
            self.statesProcessed += 1

            currentSymbol: int = self.tokens[currentEntry.tokenListIndex].type

            atCaret: bool = currentEntry.tokenListIndex >= len( self.tokens ) - 1
            if self.showDebugOutput and self.logger.isEnabledFor( logging.DEBUG ):
                self.printDescription( indentation, currentEntry.state,
                                       self.generateBaseDescription( currentEntry.state ), currentEntry.tokenListIndex )
                if self.showRuleStack:
                    self.printRuleState( callStack )

            if currentEntry.state.stateType == ATNState.RULE_STOP:
                # Record the token index we are at, to report it to the caller.
                result.add( currentEntry.tokenListIndex )
                continue

            transitions: List[Transition] = currentEntry.state.transitions

            # We simulate here the same precedence handling as the parser does, which uses hard coded values.
            # For rules that are not left recursive this value is ignored (since there is no precedence transition).
            for transition in transitions:
                if type( transition ) == RuleTransition:
                    ruleTransition: RuleTransition = transition
                    endStatus: Set[int] = self.processRule( transition.target, currentEntry.tokenListIndex, callStack,
                                                            ruleTransition.precedence, indentation + 1 )
                    for position in endStatus:
                        statePipeline.append( IPipelineEntry( transition.followState, position ) )

                elif type( transition ) == PredicateTransition:
                    if self.checkPredicate( transition ):
                        statePipeline.append( IPipelineEntry( transition.target, currentEntry.tokenListIndex ) )

                elif type( transition ) == PrecedencePredicateTransition:
                    predTransition: PrecedencePredicateTransition = transition
                    if predTransition.precedence >= self.precedenceStack[len( self.precedenceStack ) - 1]:
                        statePipeline.append( IPipelineEntry( transition.target, currentEntry.tokenListIndex ) )

                elif type( transition ) == WildcardTransition:
                    if atCaret:
                        if not self.translateStackToRuleIndex( callStack ):
                            intern: IntervalSet = IntervalSet()
                            intern.addRange( range( Token.MIN_USER_TOKEN_TYPE,
                                                    self.atn.maxTokenType + 1 ) )  # range upper limit is exclusive
                            for token in intervalSetToList( intern ):
                                if not token in self.ignoredTokens:
                                    self.candidates.tokens[token] = []
                    else:
                        statePipeline.append( IPipelineEntry( transition.target, currentEntry.tokenListIndex + 1 ) )

                else:
                    if transition.isEpsilon:
                        # Jump over simple states with a single outgoing epsilon transition.
                        statePipeline.append( IPipelineEntry( transition.target, currentEntry.tokenListIndex ) )
                        continue

                    followSet: IntervalSet = transition.label
                    if followSet is not None and len( followSet ) > 0:
                        if transition.serializationType == Transition.NOT_SET:
                            followSet = followSet.complement( Token.MIN_USER_TOKEN_TYPE, self.atn.maxTokenType )
                        if atCaret:
                            if not self.translateStackToRuleIndex( callStack ):
                                followList: List[int] = intervalSetToList( followSet )
                                addFollowing: bool = len( followList ) == 1
                                for symbol in followList:
                                    if not symbol in self.ignoredTokens:
                                        if self.showDebugOutput and self.logger.isEnabledFor( logging.DEBUG ):
                                            self.logger.debug(
                                                "=====> collected: " + IntervalSet.elementName( IntervalSet,
                                                                                                self.literalNames,
                                                                                                self.symbolicNames,
                                                                                                symbol ) )

                                        if addFollowing:
                                            self.candidates.tokens[symbol] = self.getFollowingTokens( transition )
                                        else:
                                            self.candidates.tokens[symbol] = []
                                    else:
                                        self.logger.debug( "====> collected: Ignoring token: " + str( symbol ) )
                        else:
                            if currentSymbol in followSet:
                                if self.showDebugOutput and self.logger.isEnabledFor( logging.DEBUG ):
                                    self.logger.debug(
                                        "=====> consumed: " + IntervalSet.elementName( IntervalSet, self.literalNames,
                                                                                       self.symbolicNames,
                                                                                       currentSymbol ) )
                                statePipeline.append(
                                    IPipelineEntry( transition.target, currentEntry.tokenListIndex + 1 ) )

        callStack.pop()
        if startState.isPrecedenceRule:
            self.precedenceStack.pop()

        # Cache the result, for later lookup to avoid duplicate walks.
        positionMap[tokenListIndex] = result

        return result

    # TODO switch case
    def switchCase(self, serializationType: int):
        return {
            Transition.RULE: lambda: self.callRULE(),
            Transition.PREDICATE: lambda: self.callPREDICATE(),
            Transition.PRECEDENCE: lambda: self.callPRECEDENCE(),
            Transition.WILDCARD: lambda: self.callWILDCARD()
        }.get( serializationType,
               lambda: self.callDEFAULT() )  # callDEFAULT will be returned default if serializationType is not found
        # (https://docs.python.org/3/library/stdtypes.html#dict.get)

    def callRULE(self):
        pass

    def callPREDICATE(self):
        pass

    def callPRECEDENCE(self):
        pass

    def callWILDCARD(self):
        pass

    def callDEFAULT(self):
        pass

    def generateBaseDescription(self, state: ATNState) -> str:
        stateValue: str = "Invalid" if (state.stateNumber == ATNState.INVALID_STATE_NUMBER) else str(
            state.stateNumber )

        return "[" + stateValue + " " + self.atnStateTypeMap[state.stateType] + "] in " + self.ruleNames[
            state.ruleIndex]

    def printDescription(self, indentation: int, state: ATNState, baseDescription: str, tokenIndex: int):
        """
        self, currentIndent, state, baseDescription, tokenIndex
        """
        # TODO check log level
        #  FINER level
        #  logger.isLoggable(Level.FINER)

        indent: List[str] = ["  "] * indentation
        output_list: List[str] = indent.copy()

        transitionDescription_list = [""]
        if self.debugOutputWithTransitions and self.logger.isEnabledFor( logging.DEBUG ):
            for transition in state.transitions:
                labels_list: List[str] = []
                symbols: List[int] = intervalSetToList( transition.label ) if transition.label is not None else []
                if len( symbols ) > 2:
                    # Only print start and end symbols to avoid large lists in debug output.
                    labels_list.append(
                        IntervalSet.elementName( IntervalSet, self.literalNames, self.symbolicNames,
                                                 symbols[0] ) + " .. " +
                        IntervalSet.elementName( IntervalSet, self.literalNames, self.symbolicNames,
                                                 symbols[len( symbols ) - 1] )
                    )
                else:
                    for symbol in symbols:
                        if len( labels_list ) > 0:
                            labels_list.append( ", " )
                        labels_list.append(
                            IntervalSet.elementName( IntervalSet, self.literalNames, self.symbolicNames, symbol ) )
                if len( labels_list ) == 0:
                    labels_list.append( "ε" )
                transitionDescription_list.extend(
                    ["\n", ''.join( indent ), "\t(", ''.join( labels_list ), ") [",
                     str( transition.target.stateNumber ), " ",
                     self.atnStateTypeMap[transition.target.stateType], "] in ",
                     self.ruleNames[transition.target.ruleIndex]]
                )
            if tokenIndex >= len( self.tokens ) - 1:
                output_list.extend( ["<<", str( self.tokenStartIndex + tokenIndex ), ">> "] )
            else:
                output_list.extend( ["<", str( self.tokenStartIndex + tokenIndex ), "> "] )
            self.logger.debug(
                ''.join( output_list ) + "Current state: " + baseDescription + ''.join( transitionDescription_list ) )

    def printRuleState(self, stack: RuleWithStartTokenList):
        # TODO check log level
        #  FINER level
        #  logger.isLoggable(Level.FINER)

        if len( stack ) == 0:
            self.logger.debug( "<empty stack>" )

            return

        if self.logger.isEnabledFor( logging.DEBUG ):
            sb_list = []
            for rule in stack:
                sb_list.extend( ["  ", self.ruleNames[rule.ruleIndex], "\n"] )
            self.logger.debug( ''.join( sb_list ) )
