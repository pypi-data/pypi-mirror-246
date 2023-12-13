"""Port of antlr-c3 typescript symbol table implementation to python"""

from __future__ import annotations

__author__ = "stu222808"

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

# TODO license

# utils import
import asyncio
from enum import Enum
from dataclasses import dataclass
from typing import Coroutine, List, Optional, ParamSpec, Set, TypeVar

# antlr4
from antlr4.tree.Tree import ParseTree


class DuplicateSymbolError(Exception):
    pass


class MemberVisibility(Enum):
    # Not specified, default depends on the language and type.
    Unknown = 0
    # Used in Swift, member can be accessed outside of the defining module and extended.
    Open = 1
    # Like Open, but in Swift such a type cannot be extended.
    Public = 2
    # Member is only accessible in the defining class and any derived class.
    Protected = 3
    # Member can only be accessed from the defining class.
    Private = 4
    # Used in Swift, member can be accessed from everywhere in a defining module, not outside however.
    FilePrivate = 5
    # Custom enum for special usage.
    Library = 6


class Modifier( Enum ):
    Static = 0
    Final = 1
    Sealed = 2
    Abstract = 3
    Deprecated = 4
    Virtual = 5
    Const = 6
    Overwritten = 7


class TypeKind(Enum):
    """
    Rough categorization of a type.
    """
    Unknown = 0
    Integer = 1
    Float = 2
    Number = 3
    String = 4
    Char = 5
    Boolean = 6
    Class = 7
    Interface = 8
    Array = 9
    Map = 10
    Enum = 11
    Alias = 12


# class ReferenceKind(Enum):
#     Irrelevant = 0
#     # Default for most languages for dynamically allocated memory ("Type*" in C++).
#     Pointer = 1
#     # "Type&" in C++
#     Reference = 2
#     # "Type" as such and default for all value types.
#     Instance = 3


class UnitKind(Enum):
    """
    Rough categorization of a unit from SI units.
    """
    Unknown = 0
    Second = 1
    Metre = 2
    # TODO si unit is kilogram | added to FundamentalUnit
    Gram = 3
    Ampere = 4
    Kelvin = 5
    Mole = 6
    Candela = 7
    # TODO add non si units?
    Pascal = 8
    Joule = 9
    ton = 10


class UnitPrefix:
    """
    Rough categorization of a unit from SI prefixes.
    """
    NoP = 0
    Quetta = 1
    Ronna = 2
    Yotta = 3
    Zetta = 4
    Exa = 5
    Peta = 6
    Tera = 7
    Giga = 8
    Mega = 9
    Kilo = 10
    Hecto = 11
    Deca = 12
    Deci = 13
    Centi = 14
    Mili = 15
    Micro = 16
    Nano = 17
    Pico = 18
    Femto = 19
    Atto = 20
    Zepto = 21
    Yocto = 22
    Ronto = 23
    Quecto = 24

@dataclass
class Unit:
    """
    The root unit. Used for unit symbols
    """
    name: str

    # The super unit of this unit or empty if this is a SI unit such as second.
    # TODO add units
    # TODO add aliases?
    base_types: List[Unit]
    prefix: UnitPrefix
    kind: UnitKind
    # reference: ReferenceKind

class ComposedUnit():
    """The composed Unit Representation of the Declaration-DSL"""
    numerator : FundamentalUnit
    denominator : FundamentalUnit
    exponent : FundamentalUnit
    basicUnit : FundamentalUnit

    def __init__(self, basicUnit : FundamentalUnit = None, numerator : FundamentalUnit = None, denominator : FundamentalUnit = None, exponent : FundamentalUnit = None) -> None:
        self.basicUnit = basicUnit
        self.numerator = numerator
        self.denominator = denominator
        self.exponent = exponent

class UnitSpecification():
    """CP-DSL Declaration UnitSpecification Representation Class"""
    prefix : UnitPrefix
    def __init__(self) -> None:
        self.composedUnitList = []
        self.prefix = None
    
    def add(self, unit : ComposedUnit):
        self.composedUnitList.append(unit)

    def getUnits(self):
        return self.composedUnitList

@dataclass
class Type:
    """
    The root type. Used for typed symbols and type aliases.
    """
    name: str

    # The super type of this type or empty if this is a fundamental type.
    # Also used as the target type for type aliases.
    base_types: Optional[List[Type]]
    kind: Optional[TypeKind]
    # reference: Optional[ReferenceKind]


@dataclass
class SymbolTableOptions:
    allow_duplicate_symbols: Optional[bool] = None


class classproperty(property):
    # TODO use metaclass factory https://stackoverflow.com/q/6760685/
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()


class FundamentalUnit(Unit):
    """
    A single class for all fundamental units which are mostly SI units. They are distinguished via the kind field.
    """

    def __init__(self, name: str, base_types=[], unit_prefix=UnitPrefix.NoP, unit_kind=UnitKind.Unknown):
        super().__init__(name=name, base_types=base_types, kind=unit_kind, prefix=unit_prefix)

    @classproperty
    def second_unit(self) -> FundamentalUnit:
        return FundamentalUnit(name="second", unit_kind=UnitKind.Second)

    @classproperty
    def metre_unit(self) -> FundamentalUnit:
        return FundamentalUnit(name="metre", unit_kind=UnitKind.Metre)

    # TODO si unit is kilogram but unitKind has gram
    @classproperty
    def gram_unit(self) -> FundamentalUnit:
        return FundamentalUnit(name="gram", unit_kind=UnitKind.Gram)

    # TODO si unit is kilogram but unitKind has gram
    @classproperty
    def kilogram_unit(self) -> FundamentalUnit:
        return FundamentalUnit(name="kilogram", unit_prefix=UnitPrefix.Kilo, unit_kind=UnitKind.Gram)

    @classproperty
    def ampere_unit(self) -> FundamentalUnit:
        return FundamentalUnit(name="ampere", unit_kind=UnitKind.Ampere)

    @classproperty
    def kelvin_unit(self) -> FundamentalUnit:
        return FundamentalUnit(name="Kelvin", unit_kind=UnitKind.Kelvin)

    @classproperty
    def mole_unit(self) -> FundamentalUnit:
        return FundamentalUnit(name="Mole", unit_kind=UnitKind.Mole)

    @classproperty
    def candela_unit(self) -> FundamentalUnit:
        return FundamentalUnit(name="Candela", unit_kind=UnitKind.Candela)

    @classproperty
    def pascal_unit(self) -> FundamentalUnit:
        return FundamentalUnit(name="Pascal", unit_kind=UnitKind.Pascal)

    @classproperty
    def joule_unit(self) -> FundamentalUnit:
        return FundamentalUnit(name="Joule", unit_kind=UnitKind.Joule)

    # TODO si unit is kilogram. unitKind has gram but could include ton
    @classproperty
    def ton_unit(self) -> FundamentalUnit:
        return FundamentalUnit(name="Ton", unit_prefix=UnitPrefix.Mega, unit_kind=UnitKind.Gram)


class FundamentalType(Type):
    """
    A single class for all fundamental types. They are distinguished via the kind field.
    """

    # , reference_kind=ReferenceKind.Irrelevant
    def __init__(self, name: str, base_types=[], type_kind=TypeKind.Unknown):
        # , reference=reference_kind
        super().__init__(name=name, base_types=base_types, kind=type_kind)

    @classproperty
    def integer_type(self) -> FundamentalType:
        return FundamentalType(name="integer", type_kind=TypeKind.Integer)

    @classproperty
    def real_type(self) -> FundamentalType:
        return FundamentalType(name="real", type_kind=TypeKind.Float)

    @classproperty
    def float_type(self) -> FundamentalType:
        return FundamentalType(name="float", type_kind=TypeKind.Float)

    @classproperty
    def string_type(self) -> FundamentalType:
        return FundamentalType(name="string", type_kind=TypeKind.String)

    @classproperty
    def bool_type(self) -> FundamentalType:
        return FundamentalType(name="bool", type_kind=TypeKind.Boolean)


def get_fundamental_type(type: str = "") -> Type | FundamentalType:
    """
    Return FundamentalType of type or, if non-existent, new Type of type
    :param type: type name to return
    :return: FundamentalType of type or, if non-existent, new Type of type
    """
    for key in FundamentalType.__dict__.keys():
        if type:
            if key == type.lower() + "_type":
                return getattr(FundamentalType, key)

            return Type(name=type.lower(), base_types=None, kind=None)
        else :
            return None



class Symbol:
    """
    The root of the symbol table class hierarchy: a symbol can be any manageable entity (like a block), not only things
    like variables or classes. We are using a class hierarchy here, instead of an enum or similar, to allow for easy
    extension and certain symbols can so provide additional APIs for simpler access to their sub elements, if needed.
    """
    # The name of the scope or empty if anonymous.
    name: str

    #The configuration Trees
    configuration = []

    # Reference to the parse tree which contains this symbol.
    context: Optional[ParseTree]

    @property
    def modifiers(self) -> Set[int]:
        return set()

    visibility: MemberVisibility = MemberVisibility.Unknown

    __the_parent: Optional[ScopedSymbol] = None

    def __init__(self, name: str = ""):
        self.name = name
        self.context = None
        self.configuration = []

    def parent(self) -> Optional[ScopedSymbol]:
        return self.__the_parent

    def first_sibling(self) -> Symbol:
        if isinstance(self.__the_parent, ScopedSymbol):
            # expect not to be None
            return self.__the_parent.first_child()

        return self

    def previous_sibling(self) -> Optional[Symbol]:
        """
        :return: the symbol before this symbol in its scope.
        """
        if not isinstance(self.__the_parent, ScopedSymbol):
            return self

        return self.__the_parent.previous_sibling_of(self)

    def next_sibling(self) -> Optional[Symbol]:
        """
        :return: the symbol following this symbol in its scope.
        """
        if not isinstance(self.__the_parent, ScopedSymbol):
            return self

        return self.__the_parent.next_sibling_of(self)

    def last_sibling(self) -> Symbol:
        if isinstance(self.__the_parent, ScopedSymbol):
            # expect not to be None
            return self.__the_parent.last_child()

        return self

    def next(self) -> Optional[Symbol]:
        """
        :return: the next symbol in definition order, regardless of the scope.
        """
        if isinstance(self.__the_parent, ScopedSymbol):
            return self.__the_parent.next_of(self)

        return None

    def root(self) -> Optional[Symbol]:
        """
        :return: the outermost entity (below the symbol table) that holds us.
        """
        run: Optional[Symbol] = self.__the_parent
        while run is not None:
            if run.parent() is None or isinstance(run.parent(), SymbolTable):
                return run
            run = run.parent()

        return run

    def symbol_table(self) -> Optional[SymbolTable]:
        """
        :return: the symbol table we belong too or undefined if we are not yet assigned.
        """
        if isinstance(self, SymbolTable):
            return self

        run: Optional[Symbol] = self.__the_parent
        while run is not None:
            if isinstance(run, SymbolTable):
                return run
            run = run.parent()

        return None

    def symbol_path(self) -> List[Symbol]:
        """
        :return: the list of symbols from this one up to root.
        """
        result: List[Symbol] = []

        run: Symbol = self
        while run is not None:
            result.append(run)
            if run.parent() is None:
                break
            run = run.parent()

        return result

    def set_parent(self, parent: Optional[Symbol]) -> None:
        """
        The parent is usually a scoped symbol as only those can have children, but we allow any symbol here for special
        scenarios. This is rather an internal method and should rarely be used by external code.

        :param parent: The new parent to use.
        :return:
        """
        self.__the_parent = parent

    def remove_from_parent(self) -> None:
        if isinstance(self.__the_parent, ScopedSymbol):
            self.__the_parent.remove_symbol(self)
            self.__the_parent = None

    async def resolve(self, name: str, local_only: bool = False) -> Optional[Symbol]:
        """
        Asynchronously looks up a symbol with a given name, in a bottom-up manner.

        :param name: The name of the symbol to find.
        :param local_only: If true only child symbols are returned, otherwise also symbols from the parent of this symbol
        (recursively).
        :return: A promise resolving to the first symbol with a given name, in the order of appearance in this scope or
        any of the parent scopes (conditionally).
        """

        if isinstance(self.__the_parent, ScopedSymbol):
            return await self.__the_parent.resolve(name, local_only)

        return None

    def resolve_sync(self, name: str, local_only: bool = False) -> Optional[Symbol]:
        """
        Synchronously looks up a symbol with a given name, in a bottom-up manner.

        :param name: The name of the symbol to find.
        :param local_only: If true only child symbols are returned, otherwise also symbols from the parent of this symbol
        (recursively).
        :return: the first symbol with a given name, in the order of appearance in this scope or any of the parent
        scopes (conditionally).
        """
        if isinstance(self.__the_parent, ScopedSymbol):
            return self.__the_parent.resolve_sync(name, local_only)

        return None

    def get_parent_of_type(self, t: type) -> Optional[T]:
        """
        :param t: The type of objects to return.
        :return: the next enclosing parent of the given type.
        """
        run = self.__the_parent
        while run is not None:
            if isinstance(run, t):
                return run
            run = run.__the_parent

        return None

    # TODO <anonymous> special string for empty scope names
    def qualified_name(self, separator=".", full=False, include_anonymous=False) -> str:
        """
        Creates a qualified identifier from this symbol and its parent. If `full` is true then all parents are traversed
        in addition to this instance.

        :param separator: The string to be used between the parts.
        :param full: A flag indicating if the full path is to be returned.
        :param include_anonymous: Use a special string for empty scope names.
        :return: the constructed qualified identifier.
        """
        if not include_anonymous and len(self.name) == 0:
            return ""

        result: str = "<anonymous>" if len(self.name) == 0 else self.name
        run = self.__the_parent
        while run:
            if include_anonymous or len(run.name) > 0:
                result = ("<anonymous>" if len(run.name) == 0 else run.name) + separator + result

            if not full or run.__the_parent is None:
                break

            run = run.__the_parent

        return result


P = ParamSpec("P")
T = TypeVar("T", bound=Symbol)


class TypedSymbol(Symbol):
    """
    A symbol with an attached type (variables, fields etc.).
    """

    # Type such as int
    attached_type: Optional[Type]

    def __init__(self, name: str, attached_type: Type = None):
        super().__init__(name)
        self.attached_type = attached_type


class UnitSymbol(TypedSymbol):
    """
    A symbol with an attached unit (physical units such as second, metre, gram etc.).
    """
    attached_unit: Optional[Unit]
    attached_description: Optional[str]

    def __init__(self, name: str, attached_description: str, attached_unit: Unit, attached_type: Type = None):
        super().__init__(name, attached_type)
        self.attached_unit = attached_unit
        self.attached_description = attached_description

class ScopedSymbol(Symbol):
    """
    A symbol with a scope (so it can have child symbols).
    """
    # All child symbols in definition order.
    __child_symbols: List[Symbol]

    def __init__(self, name: str = ""):
        super().__init__(name)
        self.__child_symbols = []

    def direct_scopes(self) -> Coroutine[List[ScopedSymbol]]:
        """
        :return: A promise resolving to all direct child symbols with a scope (e.g. classes in a module).
        """
        return self.get_symbols_of_type(ScopedSymbol)

    def children(self) -> List[Symbol]:
        return self.__child_symbols

    def parent(self) -> Optional[ScopedSymbol]:
        s_parent: Symbol = super().parent()
        if not isinstance(s_parent, SymbolTable):
            return s_parent
        else:
            return None

    def first_child(self) -> Optional[Symbol]:
        if len(self.children()) > 0:
            return self.children()[0]

        return None

    def last_child(self) -> Optional[Symbol]:
        if len(self.children()) > 0:
            return self.children()[len(self.children()) - 1]

        return None

    def clear(self) -> None:
        self.__child_symbols = []

    def add_symbol(self, symbol: Symbol) -> None:
        """
        Adds the given symbol to this scope. If it belongs already to a different scope it is removed from that before
        adding it here.

        :param symbol: The symbol to add as a child.
        :return:
        """
        symbol.remove_from_parent()

        # Check for duplicates first.
        symbol_table = self.symbol_table()
        if symbol_table is None or not symbol_table.options.allow_duplicate_symbols:
            for child in self.children():
                if child == symbol or (len(symbol.name) > 0 and child.name == symbol.name) and type(child) == type(symbol):
                    symbol_name = symbol.name if symbol.name else "<anonymous>"
                    scope_name = self.name if self.name else "<anonymous>"
                    msg: str = f"Attempt to add duplicate symbol \"{symbol_name}\" to \"{scope_name}\""

                    raise DuplicateSymbolError(msg)

        self.children().append(symbol)
        symbol.set_parent(self)

    def remove_symbol(self, symbol: Symbol) -> None:
        if symbol in self.children():
            self.children().remove(symbol)
            symbol.set_parent(None)

    async def get_nested_symbols_of_type(self, t: type) -> List[T]:
        """
        Asynchronously retrieves child symbols of a given type from this symbol.

        :param t: The type of the objects to return.
        :return: A promise resolving to all (nested) children of the given type.
        """
        result: List[T] = []

        child_promises: List[Coroutine[List[T]]] = []
        for child in self.children():
            if isinstance(child, t):
                result.append(child)

            if isinstance(child, ScopedSymbol):
                child_promises.append(child.get_nested_symbols_of_type(t))

        child_symbols = await asyncio.gather(*child_promises)
        for entry in child_symbols:
            result.extend(entry)

        return result

    def get_nested_symbols_of_type_and_name_sync(self, t: type, name: str = None) -> List[T]:
        """
        Synchronously retrieves child symbols of a given type and name from this symbol.

        :param t: The type of the objects to return.
        :param name: If given only returns symbols with that name.
        :return: A list of all (nested) children of the given type.
        """
        result: List[T] = []

        for child in self.children():
            if isinstance(child, t) and (name is None or child.name == name):
                result.append(child)

            if isinstance(child, ScopedSymbol):
                result.extend(child.get_nested_symbols_of_type_and_name_sync(t, name))

        return result

    def get_nested_symbols_of_type_sync(self, t: type) -> List[T]:
        """
        Synchronously retrieves child symbols of a given type from this symbol.

        :param t: The type of the objects to return.
        :return: A list of all (nested) children of the given type.
        """
        result: List[T] = []

        for child in self.children():
            if isinstance(child, t):
                result.append(child)

            if isinstance(child, ScopedSymbol):
                result.extend(child.get_nested_symbols_of_type_sync(t))

        return result

    async def get_all_nested_symbols(self, name: str = None) -> List[Symbol]:
        """
        :param name: If given only returns symbols with that name.
        :return: A promise resolving to symbols from this and all nested scopes in the order they were defined.
        """
        result: List[Symbol] = []

        child_promises: List[Coroutine[List[Symbol]]] = []
        for child in self.children():
            if name is None or child.name == name:
                result.append(child)

            if isinstance(child, ScopedSymbol):
                child_promises.append(child.get_all_nested_symbols(name))

        child_symbols = await asyncio.gather(*child_promises)
        for entry in child_symbols:
            result.extend(entry)

        return result

    def get_all_nested_symbols_sync(self, name: str = None) -> List[Symbol]:
        """
        :param name: If given only returns symbols with that name.
        :return: A list of all symbols from this and all nested scopes in the order they were defined.
        """
        result: List[Symbol] = []

        for child in self.children():
            if name is None or child.name == name:
                result.append(child)

            if isinstance(child, ScopedSymbol):
                result.extend(child.get_all_nested_symbols_sync(name))

        return result

    def get_symbols_of_type_sync(self, t: type, local_only: bool = True, callers: List[T] = [] ) -> List[T]:
        """
        :param callers: List of visited scopes, that should not be visited again
        :param local_only: If true only child symbols are returned, otherwise also symbols from the parent of this symbol
        (recursively).
        :param t: The type of the objects to return.
        :return: A promise resolving to direct children of a given type.
        """
        result: List[T] = []
        for child in self.children():
            if isinstance(child, t):
                result.append(child)

        # TODO check modded by sgu?
        if not local_only:
            # Call parent scope
            if isinstance(self.parent(), ScopedSymbol) and self.parent() not in callers:
                result.extend(self.parent().get_symbols_of_type_sync(t, local_only, callers + [self]))

        return result

    async def get_symbols_of_type(self, t: type, local_only: bool = True, callers: List[T] = [] ) -> List[T]:
        """
        :param callers: List of visited scopes, that should not be visited again
        :param local_only: If true only child symbols are returned, otherwise also symbols from the parent of this symbol
        (recursively).
        :param t: The type of the objects to return.
        :return: A promise resolving to direct children of a given type.
        """
        result: List[T] = []
        for child in self.children():
            if isinstance(child, t):
                result.append(child)

        # TODO check modded by sgu?
        if not local_only:
            # Call parent scope
            if isinstance(self.parent(), ScopedSymbol) and self.parent() not in callers:
                localList: List[T] = await self.parent().get_symbols_of_type(t, local_only, callers + [self])
                result.extend(localList)

        return result

    # TODO: add optional position dependency (only symbols defined before a given caret pos are viable).
    async def get_all_symbols(self, t: type, local_only: bool = False, callers: List[T] = []) -> List[T]:
        """
        :param callers: List of visited scopes, that should not be visited again
        :param t: The type of the objects to return.
        :param local_only: If true only child symbols are returned, otherwise also symbols from the parent of this symbol
        (recursively).
        :return: A promise resolving to all symbols of the given type, accessible from this scope (if local_only is
        false), within the owning symbol table.
        """
        result: List[T] = []

        # Special handling for namespaces, which act like grouping symbols in this scope, so we show them as available
        # in this scope.
        for child in self.children():
            if isinstance(child, t):
                result.append(child)

            # if isinstance(child, NamespaceSymbol) and child not in callers:
            #     child_symbols: List[T] = await child.get_all_symbols(t, True, callers + [self])
            #     result.extend(child_symbols)

            # recursively call children scopes, except for scopes that called us
            if isinstance(child, ScopedSymbol) and child not in callers:
                localList: List[T] = await child.get_all_symbols(t, True, callers + [self])
                result.extend(localList)

        # recursively call parent scopes, except for scopes that called us
        # TODO sgu fixed bug: no recursive call
        if not local_only:
            # Call parent scope
            if isinstance(self.parent(), ScopedSymbol) and self.parent() not in callers:
                localList: List[T] = await self.parent().get_all_symbols(t, local_only, callers + [self])
                result.extend(localList)

        return result

    def get_all_symbols_sync(self, t: type, local_only: bool = False, callers: List[T] = []) -> List[T]:
        """
        TODO: add optional position dependency (only symbols defined before a given caret pos are viable).

        :param callers: List of visited scopes, that should not be visited again
        :param t: The type of the objects to return.
        :param local_only: If true only child symbols are returned, otherwise also symbols from the parent of this symbol
        (recursively).
        :return: A list with all symbols of the the given type, accessible from this scope (if local_only is false),
        within the owning symbol table.
        """
        result: List[T] = []

        # Special handling for namespaces, which act like grouping symbols in this scope,
        # so we show them as available in this scope.
        for child in self.children():
            if isinstance(child, t):
                result.append(child)

            # if isinstance(child, NamespaceSymbol) and child not in callers:
            #     child_symbols: List[T] = child.get_all_symbols_sync(t, True, callers + [self])
            #     result.extend(child_symbols)

            # recursively call children scopes, except for scopes that called us
            if isinstance(child, ScopedSymbol) and child not in callers:
                result.extend(child.get_all_symbols_sync(t, True, callers + [self]))

        # recursively call parent scopes, except for scopes that called us
        # TODO sgu fixed bug: no recursive call
        if not local_only:
            # Call parent scope
            if isinstance(self.parent(), ScopedSymbol) and self.parent() not in callers:
                local_list: List[T] = self.parent().get_all_symbols_sync(t, local_only, callers + [self])
                result.extend(local_list)

        return result

    async def resolve(self, name: str, local_only: bool = False, callers: List[T] = [] ) -> Optional[Symbol]:
        """
        :param callers: List of visited scopes, that should not be visited again
        :param name: The name of the symbol to resolve.
        :param local_only: If true only child symbols are returned, otherwise also symbols from the parent of this symbol
        (recursively).
        :return: A promise resolving to the first symbol with a given name, in the order of appearance in this scope or
        any of the parent scopes (conditionally).
        """
        for child in self.children():
            if child.name == name:
                return child

        # Nothing found locally. Let the parent continue.
        if not local_only:
            # Call parent scope
            if isinstance(self.parent(), ScopedSymbol) and self.parent() not in callers:
                return await self.parent().resolve(name, local_only, callers + [self])

        return None

    def resolve_sync(self, name: str, local_only: bool = False, callers: List[T] = []) -> Optional[Symbol]:
        """
        :param name: The name of the symbol to resolve.
        :param local_only: If true only child symbols are returned, otherwise also symbols from the parent of this symbol
        (recursively).
        :param callers: List of visited scopes, that should not be visited again
        :return: the first symbol with a given name, in the order of appearance in this scope or any of the parent
        scopes (conditionally).
        """
        for child in self.children():
            if child.name == name:
                return child

        # Nothing found locally. the parent continues.
        if not local_only:
            # Call parent scope
            if isinstance(self.parent(), ScopedSymbol) and self.parent() not in callers:
                return self.parent().resolve_sync(name, local_only, callers + [self])

        return None

    def get_typed_symbols(self, local_only: bool = True, callers: List[T] = [] ) -> List[TypedSymbol]:
        """
        :param local_only: If true only child symbols are returned, otherwise also symbols from the parent of this symbol
        (recursively).
        :param callers: List of visited scopes, that should not be visited again
        :return: all accessible symbols that have a type assigned.
        """
        result: List[TypedSymbol] = []

        for child in self.children():
            if isinstance(child, TypedSymbol):
                result.append(child)

        if not local_only:
            # Call parent scope
            if isinstance(self.parent(), ScopedSymbol) and self.parent() not in callers:
                local_list = self.parent().get_typed_symbols(local_only, callers + [self])
                result.extend(local_list)

        return result

    def get_typed_symbol_names(self, local_only: bool = True, callers: List[T] = [] ) -> List[str]:
        """
        The names of all accessible symbols with a type.


        :param local_only: If true only child symbols are returned, otherwise also symbols from the parent of this symbol
        (recursively).
        :param callers: List of visited scopes, that should not be visited again
        :return: A list of names.
        :param callers:
        """
        result: List[str] = []
        for child in self.children():
            if isinstance(child, TypedSymbol):
                result.append(child.name)

        if not local_only:
            # Call parent scope
            if isinstance(self.parent(), ScopedSymbol) and self.parent() not in callers:
                local_list = self.parent().get_typed_symbol_names(local_only, callers + [self])
                result.extend(local_list)

        return result

    def symbol_from_path(self, path: str, separator=".") -> Optional[Symbol]:
        """
        :param path: The path consisting of symbol names separator by `separator`.
        :param separator: The character to separate path segments.
        :return: the symbol located at the given path through the symbol hierarchy.
        """
        elements = path.split(separator)
        index = 0
        if elements[0] == self.name or len(elements[0]) == 0:
            index += 1

        result: Symbol = self
        while index < len(elements):
            if not isinstance(result, ScopedSymbol):
                return None

            child: Optional[Symbol] = next(
                filter(lambda candidate: candidate.name == elements[index], result.children()), None
            )
            if child is None:
                return None

            result = child
            index += 1

        return result

    def index_of_child(self, child: Symbol) -> int:
        """
        :param child: The child to search for.
        :return: the index of the given child symbol in the child list or -1 if it couldn't be found.
        """
        # two pass org
        # return lambda child,self.children() : self.children().index(child) if child in self.children() else -1
        try:
            return self.children().index(child)
        except ValueError:
            return -1

    def next_sibling_of(self, child: Symbol) -> Optional[Symbol]:
        """
        :param child: The reference node.
        :return: the sibling symbol after the given child symbol, if one exists.
        """
        index = self.index_of_child(child)
        if index == -1 or index >= len(self.children()) - 1:
            return None

        return self.children()[index + 1]

    def previous_sibling_of(self, child: Symbol) -> Optional[Symbol]:
        """
        :param child: The reference node.
        :return: the sibling symbol before the given child symbol, if one exists.
        """
        index = self.index_of_child(child)
        if index < 1:
            return None

        return self.children()[index - 1]

    def next_of(self, child: Symbol) -> Optional[Symbol]:
        """
        :param child: The reference node.
        :return: the next symbol in definition order, regardless of the scope.
        """
        if not isinstance(child.parent(), ScopedSymbol):
            return None

        if child.parent() is not self:
            return child.parent().nextOf(child)

        if isinstance(child, ScopedSymbol) and len(child.children()) > 0:
            return child.children()[0]

        sibling = self.next_sibling_of(child)
        if sibling is not None:
            return sibling

        return self.parent().next_of(self)


class VariableSymbol( Symbol ):
    """a class for parameter of cp-dsl

    Args:
        Symbol (_type_): _description_

    Returns:
        _type_: _description_
    """

    def __init__(self, name: str, description: str = "", value = None, unitSpecification : UnitSpecification = None, type = None):
        super().__init__(name)
        self.description = description
        self.unit = unitSpecification
        self.is_tree = isinstance(value, ParseTree)
        self.val = value if value else None
        if type == "float":
            value = 0.0
        if type == "int":
            value = 0
        self.type = type
        self.is_array = False

    @property
    def value(self):
        return self.val

class EnumSymbol(Symbol):
    '''
    a class for enums of cp-dsl language
    '''
    def __init__(self, name: str = "", enums = None):
        super().__init__(name)
        self.enums = enums

class RangeSymbol(Symbol):
    '''
    a class for ranges in cp-dsl
    '''
    def __init__(self, name, type, minimum, maximum):
        super().__init__(name)
        self.type = type
        self.minimum = minimum
        self.maximum = maximum
        
class ArraySymbol(VariableSymbol):
    """
    a class representing a n-dimensional array
    Array Representation:
    i[2:7] = {0,1,2,3,4,5}
    => [2,3,4,5,6,7][0,1,2,3,4,5]
    i[5][9] = 8
    => [5][ArraySymbol([9][8])]
    """

    def __init__(self, name: str = "", upperBound = 0, lowerBound = 0):
        super().__init__(name)
        self.upperBound = upperBound
        self.lowerBound = lowerBound
        self.is_array = True
        self.vectors = []
        self.arrVal = []

    @property
    def value(self):
        return self.toNormalizedArray()

    #!!!!EXPERIMENTAL!!!!
    def add(self, vector, val) -> None:
        """
        adds a value in the array
        :vector: the index of the value
        :val: the value to save in the array
        """
        #n Dimension Support
        if len(vector) >= 2:
            if isinstance(self.get(vector[0]), ArraySymbol):
                newArray = self.get(vector[0])
            else:
                newArray = ArraySymbol()
            newArray.add(vector[1:], val)
            self.add([vector[0]], newArray)
        else:
            #check if vector already in array
            if vector[0] in self.vectors:
                i = self.vectors.index(vector[0])
                self.arrVal[i] = val
                return
            if self.upperBound == 0 and self.lowerBound == 0:
                self.vectors.append(vector[0])
                self.arrVal.append(val)
            else:
                #Check for the bounds
                if self.lowerBound <= vector[0] and self.upperBound >= vector[0] or self.upperBound == 0:
                    self.vectors.append(vector[0])
                    self.arrVal.append(val)
                else:
                    print("ERROR: Array", self.name,"out of bound error for index", vector)


    def get(self, index) -> T:
        """
        get a value out of the list, None if not available
        :index: the index of the value to return
        :return: the value on given index
        """
        try:
            if isinstance(index, list):
                return self.arrVal[self.vectors.index(index[0])]
            return self.arrVal[self.vectors.index(index)]
        except:
            return None
    
    def getVector(self, vector) -> T:
        """
        get a value out of the list recursive given by a vector
        :vector: the vector
        :return: the value on the vector
        """
        if len(vector) >= 2:
            currArray = self
            try:
                for i in vector:
                    index = self.vectors.index(i)
                    currArray = currArray.value[index]
                return currArray
            except:
                # return the last value reached
                return currArray
        else:
            return self.get(vector[0])
            
    
    def remove(self, index) -> T:
        """
        removes and returns the value places at index
        :index: the index of the value to remove
        :return: the value removed
        """
        i = self.vectors.index(index)
        self.vectors.pop(i)
        return self.arrVal.pop(i)
    
    def removeVal(self, val) -> None:
        """
        removes a given value from the array (first elem found)
        :val: the value to remove
        """
        i = self.arrVal.index(val)
        self.vectors.pop(i)
        self.arrVal.pop(i)

    def toArray(self, recursive = True) -> list:
        """
        converts the array in a pyton list
        :recursive: convert also arrays in arrays
        :return: the generated python list
        """
        returnVal = []
        for i in range(len(self)):
            if i in self.vectors:
                if not recursive:
                    returnVal.append(self.get(i))
                else:
                    elem = self.get(i)
                    if isinstance(elem, ArraySymbol):
                        returnVal.append(elem.toArray())
                    else:
                        returnVal.append(elem)
            else:
                returnVal.append(None)
        return returnVal
    
    def toNormalizedArray(self, recursive = True) -> list:
        """
        converts the array in a pyton list without nones
        :recursive: convert also arrays in arrays
        :return: the generated python list
        """
        returnVal = []
        for i in range(len(self)):
            if i in self.vectors:
                if not recursive:
                    returnVal.append(self.get(i[0])) if isinstance(self.get(i), tuple) else returnVal.append(self.get(i))
                else:
                    elem = self.get(i)
                    if isinstance(elem, ArraySymbol):
                        returnVal.append(elem.toNormalizedArray())
                    else:
                        returnVal.append(elem[0]) if isinstance(elem, tuple) else returnVal.append(elem)
        return returnVal        

    def clear(self) -> None:
        '''
        removes all values from the array
        '''
        self.vectors = []
        self.arrVal = []

    def __len__(self):
        if len(self.vectors) == 0:
            return 0
        return max(self.vectors) + 1
    
    def __str__(self):
        return str(self.toArray()).replace("None, ", "")


class GroupSymbol(ScopedSymbol):
    """
    A Class for Group Declarations
    """
    description: Optional[str]
    groupType: Optional[T]
    
    def __init__(self, name: str, groupType: T, description: str = ""):
        super().__init__(name)
        self.description = description
        self.groupType = groupType
        
    def getGroupVars(self, localOnly=True) -> Coroutine[List[T]]:
        return self.getSymbolsOfType(self.groupType)

class NamespaceSymbol( ScopedSymbol ):
    pass

class FeatureSymbol( ScopedSymbol ):
    """
    A standalone function/procedure/rule.
    """
    returnType: Optional[Type]  # Can be null if result is void.
    is_activated: bool = False # set if the feature is activated

    def __init__(self, name: str, description : str = "", returnType: Type = None):
        super().__init__( name )
        self.returnType = returnType
        self.is_activated = False
        self.description = description

    def getVariables(self, localOnly=True) -> Coroutine[List[T]]:
        return self.getNestedSymbolsOfTypeSync( VariableSymbol )

    def getParameters(self, localOnly=True) -> Coroutine[List[T]]:
        return self.getNestedSymbolsOfTypeSync( VariableSymbol )

    def getUnits(self, localOnly=True) -> Coroutine[List[T]]:
        return self.getNestedSymbolsOfTypeSync(UnitSymbol)
    
    def getFeatures(self, localOnly=True) -> Coroutine[List[T]]:
        return self.getNestedSymbolsOfTypeSync(FeatureSymbol)


@dataclass
class SymbolTableInfo:
    dependency_count: int
    symbol_count: int


class SymbolTable(ScopedSymbol):
    """
    The main class managing all the symbols for a top level entity like a file, library or similar.
    """
    #  Other symbol information available to this instance.
    dependencies: Set[SymbolTable]
    options: SymbolTableOptions

    def __init__(self, name: str, options: SymbolTableOptions):
        self.dependencies = set()
        self.options = options
        super().__init__(name)

    def info(self):
        """
        :return: instance information, mostly relevant for unit testing.
        """
        return SymbolTableInfo(len(self.dependencies), len(self.children()))

    def clear(self):
        super().clear()
        self.dependencies.clear()

    def add_dependencies(self, *tables: SymbolTable):
        for table in tables:
            self.dependencies.add(table)

    def remove_dependency(self, table: SymbolTable):
        if table in self.dependencies:
            self.dependencies.remove(table)

    def add_new_symbol_of_type(
            self, t: type, parent: Optional[ScopedSymbol] = None, *my_args: P.args or None, **my_kwargs: P.kwargs or None
    ) -> T:
        result = t(*my_args, **my_kwargs)
        if parent is None or parent is self:
            self.add_symbol(result)
        else:
            parent.add_symbol(result)

        return result

    async def addNewNamespaceFromPath(self, parent: Optional[ScopedSymbol], path: str,
                                      delimiter=".") -> NamespaceSymbol:
        """
        Asynchronously adds a new namespace to the symbol table or the given parent. The path parameter specifies a
        single namespace name or a chain of namespaces (which can be e.g. "outer.intermittent.inner.final"). If any of
        the parent namespaces is missing they are created implicitly. The final part must not exist however or you'll
        get a duplicate symbol error.

        :param parent: The parent to add the namespace to.
        :param path: The namespace path.
        :param delimiter: The delimiter used in the path.
        :return: The new symbol.
        """
        parts = path.split( delimiter )
        i = 0
        currentParent = self if parent is None else parent
        while i < len( parts ) - 1:
            namespace: NamespaceSymbol = await currentParent.resolve( parts[i], True )
            if namespace is None:
                namespace = self.addNewSymbolOfType( NamespaceSymbol, currentParent, parts[i] )

            currentParent = namespace
            i += 1

        return self.addNewSymbolOfType( NamespaceSymbol, currentParent, parts[len( parts ) - 1] )

    def addNewNamespaceFromPathSync(self, parent: Optional[ScopedSymbol], path: str, delimiter=".") -> NamespaceSymbol:
        """
        Synchronously adds a new namespace to the symbol table or the given parent. The path parameter specifies a
        single namespace name or a chain of namespaces (which can be e.g. "outer.intermittent.inner.final"). If any of
        the parent namespaces is missing they are created implicitly. The final part must not exist however or you'll
        get a duplicate symbol error.

        :param parent: The parent to add the namespace to.
        :param path: The namespace path.
        :param delimiter: The delimiter used in the path.
        :return: The new symbol.
        """
        parts = path.split( delimiter )
        i = 0
        currentParent = self if parent is None else parent

        while i < len( parts ) - 1:
            namespace: NamespaceSymbol = currentParent.resolveSync( parts[i], True )
            if namespace is None:
                namespace = self.addNewSymbolOfType( NamespaceSymbol, currentParent, parts[i] )

            currentParent = namespace
            i += 1

        return self.addNewSymbolOfType( NamespaceSymbol, currentParent, parts[len( parts ) - 1] )

    async def get_all_symbols(self, t: type, local_only: bool = False, callers: List[T] = []) -> List[T]:
        """
        Asynchronously returns all symbols from this scope (and optionally those from dependencies) of a specific type.

        :param t: The type of the symbols to return.
        :param local_only: If true do not search dependencies.
        :return: A promise which resolves when all symbols are collected.
        """
        result: List[T] = await super().get_all_symbols(t, local_only, callers)

        if not local_only and self.parent() not in callers:
            # TODO alternative
            # dependencyResults = await asyncio.gather(*[x.get_all_symbols(t, local_only) for x in self.dependencies])
            dependencyResults = await asyncio.gather(
                *(map((lambda x: x.get_all_symbols(t, local_only, callers + [self])), self.dependencies))
            )

            for value in dependencyResults:
                result.extend(value)

        return result

    def get_all_symbols_sync(self, t: type, local_only: bool = False) -> List[T]:
        """
        Synchronously returns all symbols from this scope (and optionally those from dependencies) of a specific type.

        :param t: The type of the symbols to return.
        :param local_only: If true do not search dependencies.
        :return: A list with all symbols.
        """
        result: List[T] = super().get_all_symbols_sync(t, local_only)

        if not local_only:
            for dependency in self.dependencies:
                result.extend(dependency.get_all_symbols_sync(t, local_only))

        return result

    async def symbol_with_context(self, context: ParseTree) -> Optional[Symbol]:
        """
        Asynchronously looks for a symbol which is connected with a given parse tree context.

        :param context: The context to search for.
        :return: A promise resolving to the found symbol or undefined.
        """

        def find_recursive(local_symbol: Symbol) -> Optional[Symbol]:
            """
            Local function to find a symbol recursively.

            :param local_symbol: The symbol to search through.
            :return: The symbol with the given context, if found.
            """
            if local_symbol.context == context:
                return local_symbol

            if isinstance(local_symbol, ScopedSymbol):
                for child in local_symbol.children():
                    local_result = find_recursive(child)
                    if local_result is not None:
                        return local_result

            return None

        symbols = await self.get_all_symbols(Symbol)
        for symbol in symbols:
            result = find_recursive(symbol)
            if result is not None:
                return result

        for dependency in self.dependencies:
            symbols = await dependency.get_all_symbols(Symbol)
            for symbol in symbols:
                result = find_recursive(symbol)
                if result is not None:
                    return result

        return None

    def symbol_with_context_sync(self, context: ParseTree) -> Optional[Symbol]:
        """
        Synchronously looks for a symbol which is connected with a given parse tree context.

        :param context: The context to search for.
        :return: The found symbol or undefined.
        """

        def find_recursive(local_symbol: Symbol) -> Optional[Symbol]:
            """
            Local function to find a symbol recursively.

            :param local_symbol: The symbol to search through.
            :return: The symbol with the given context, if found.
            """
            if local_symbol.context is context:
                return local_symbol

            if isinstance(local_symbol, ScopedSymbol):
                for child in local_symbol.children():
                    local_result = find_recursive(child)
                    if local_result is not None:
                        return local_result

            return None

        symbols = self.get_all_symbols_sync(Symbol)
        for symbol in symbols:
            result = find_recursive(symbol)
            if result is not None:
                return result

        for dependency in self.dependencies:
            symbols = dependency.get_all_symbols_sync(Symbol)
            for symbol in symbols:
                result = find_recursive(symbol)
                if result is not None:
                    return result

        return None

    async def resolve(self, name: str, local_only: bool = False) -> Optional[Symbol]:
        """
        Asynchronously resolves a name to a symbol.

        :param name: The name of the symbol to find.
        :param local_only: A flag indicating if only this symbol table should be used or also its dependencies.
        :return: A promise resolving to the found symbol or undefined.
        """
        result = await super().resolve(name, local_only)
        if result is None and not local_only:
            for dependency in self.dependencies:
                result = await dependency.resolve(name, False)
                if result is not None:
                    return result

        return result

    def resolve_sync(self, name: str, local_only: bool = False) -> Optional[Symbol]:
        """
        Synchronously resolves a name to a symbol.

        :param name: The name of the symbol to find.
        :param local_only: A flag indicating if only this symbol table should be used or also its dependencies.
        :return: The found symbol or undefined.
        """
        result = super().resolve_sync(name, local_only)
        if result is None and not local_only:
            for dependency in self.dependencies:
                result = dependency.resolve_sync(name, False)
                if result is not None:
                    return result

        return result
