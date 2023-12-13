"""computeTokenIndex module."""

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

# utils
import logging

from dataclasses import dataclass
from typing import Any, List, Optional

# antlr4
from antlr4 import BufferedTokenStream, TerminalNode, Token
from antlr4.ParserRuleContext import ParserRuleContext
from antlr4.tree.Tree import ErrorNodeImpl, TerminalNodeImpl

# debug
logger = logging.getLogger(__name__)
logger.disabled = True


@dataclass
class CaretPosition:
    line: int
    column: int


@dataclass
class TokenPosition:
    index: int
    context: ParserRuleContext
    text: str


def compute_token_index_of_terminal_node(terminal_node: TerminalNode, caret_position: CaretPosition) -> Optional[Any]:
    if isinstance(terminal_node, TerminalNodeImpl):
        start = terminal_node.symbol.column
        stop = terminal_node.symbol.column + len(terminal_node.getText())
        if terminal_node.symbol.line == caret_position.line and start <= caret_position.column <= stop:
            return terminal_node.symbol.tokenIndex
    return None


def compute_token_index_of_child_node(parser_rule_context: ParserRuleContext, caret_position: CaretPosition) -> Optional[int]:
    i = 0
    while i < parser_rule_context.getChildCount():
        index = compute_token_index(parser_rule_context.getChild(i), caret_position)
        if index is not None:
            return index
        i += 1
    return None


def compute_token_index(parser_rule_context: ParserRuleContext, caret_position: CaretPosition) -> int:
    if isinstance(parser_rule_context, TerminalNode):
        return compute_token_index_of_terminal_node(parser_rule_context, caret_position)
    else:
        return compute_token_index_of_child_node(parser_rule_context, caret_position)


def position_of_token(
        token: Token, text: str, caret_position: CaretPosition, identifier_token_types: List[int], parser_rule_context: ParserRuleContext | TerminalNode
):
    if token:
        start = token.column
        stop = token.column + len(text)
        if token.line == caret_position.line and start <= caret_position.column <= stop and 0 <= token.tokenIndex:
            index = token.tokenIndex
            if token.type in identifier_token_types:
                index -= 1

            text = text[0: caret_position.column - start] if not isinstance(parser_rule_context, ErrorNodeImpl) else ""
            result: TokenPosition = TokenPosition(index, parser_rule_context, text)

            return result

    return None


def compute_token_position_of_terminal(
        terminal_node: TerminalNode, token_stream: BufferedTokenStream, caret_position: CaretPosition, identifier_token_types: List[int]
):
    token: Token = terminal_node.symbol if isinstance(terminal_node, TerminalNodeImpl) else None
    text: str = terminal_node.getText() if isinstance(terminal_node, TerminalNodeImpl) else None
    return position_of_token(token, text, caret_position, identifier_token_types, terminal_node)


def compute_token_position_of_child_node(
        parser_rule_context: ParserRuleContext, tokens: BufferedTokenStream, caret_position: CaretPosition, identifier_token_types: List[int]
):
    # Return None if no context exists or caret is outside of context
    start_line: Optional[int] = None
    end_line: Optional[int] = None
    start_Index: Optional[int] = None
    stop_Index: Optional[int] = None
    if parser_rule_context and parser_rule_context.start:
        start_line = parser_rule_context.start.line
        start_Index = parser_rule_context.start.tokenIndex

        # Check tokens after parser error
        stop_Index = len(tokens.tokens)
        if parser_rule_context.stop:
            if parser_rule_context.stop.line != stop_Index:
                end_line = parser_rule_context.stop.line + 1
            else:
                end_line = parser_rule_context.stop.line
        else:
            end_line = start_line

        if start_line > caret_position.line or end_line < caret_position.line:
            return None

        # Check nested elements
        for i in range(0, parser_rule_context.getChildCount()):
            pos = compute_token_position(parser_rule_context.getChild(i), tokens, caret_position, identifier_token_types)
            if pos:
                return pos

        # Check elements in range of context
        for i in range(start_Index, stop_Index):
            pos = position_of_token(
                tokens.tokens[i], tokens.tokens[i].text, caret_position, identifier_token_types, parser_rule_context
            )
            if pos:
                return pos

    return None


def compute_token_position(
        parser_rule_context: ParserRuleContext, tokens: BufferedTokenStream, caret_position: CaretPosition, identifier_token_types=None
) -> Optional[TokenPosition]:
    if identifier_token_types is None:
        identifier_token_types = []
    if isinstance(parser_rule_context, TerminalNode):
        return compute_token_position_of_terminal(parser_rule_context, tokens, caret_position, identifier_token_types)
    else:
        return compute_token_position_of_child_node(parser_rule_context, tokens, caret_position, identifier_token_types)
