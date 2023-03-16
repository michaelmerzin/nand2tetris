"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class SymbolTable:
    """A symbol table that associates names with information needed for Jack
    compilation: type, kind and running index. The symbol table has two nested
    scopes (class/subroutine).
    """
    STATIC = "STATIC"
    FIELD = "FIELD"
    VAR = "VAR"
    ARGUMENT = "ARG"

    SUBROUTINE_KINDS = [VAR, ARGUMENT]
    CLASS_KINDS = [FIELD, STATIC]
    KINDS = [VAR, ARGUMENT, FIELD, STATIC]

    def __init__(self) -> None:
        """Creates a new empty symbol table."""
        # Your code goes here!
        self.subroutine_table = {SymbolTable.ARGUMENT: [], SymbolTable.VAR: []}
        self.class_table = {SymbolTable.STATIC: [], SymbolTable.FIELD: []}

    def start_subroutine(self) -> None:
        """Starts a new subroutine scope (i.e., resets the subroutine's 
        symbol table).
        """
        # Your code goes here!
        self.subroutine_table = {SymbolTable.ARGUMENT: [], SymbolTable.VAR: []}

    def define(self, name: str, type: str, kind: str) -> None:
        """Defines a new identifier of a given name, type and kind and assigns 
        it a running index. "STATIC" and "FIELD" identifiers have a class scope, 
        while "ARG" and "VAR" identifiers have a subroutine scope.

        Args:
            name (str): the name of the new identifier.
            type (str): the type of the new identifier.
            kind (str): the kind of the new identifier, can be:
            "STATIC", "FIELD", "ARG", "VAR".
        """
        # Your code goes here!

        if kind in SymbolTable.SUBROUTINE_KINDS:
            self.subroutine_table[kind].append((name, type))

        elif kind in SymbolTable.CLASS_KINDS:
            self.class_table[kind].append((name, type))

    def var_count(self, kind: str) -> int:
        """
        Args:
            kind (str): can be "STATIC", "FIELD", "ARG", "VAR".

        Returns:
            int: the number of variables of the given kind already defined in 
            the current scope.
        """
        # Your code goes here!
        if kind in SymbolTable.SUBROUTINE_KINDS:
            return len(self.subroutine_table[kind])

        if kind in SymbolTable.CLASS_KINDS:
            return len(self.class_table[kind])

        return 0

    def kind_of(self, name: str) -> str:
        """
        Args:
            name (str): name of an identifier.

        Returns:
            str: the kind of the named identifier in the current scope, or None
            if the identifier is unknown in the current scope.
        """
        # Your code goes here!

        for kind in SymbolTable.SUBROUTINE_KINDS:
            for (cur_name, cur_type) in self.subroutine_table[kind]:
                if name == cur_name:
                    return kind

        for kind in SymbolTable.CLASS_KINDS:
            for (cur_name, cur_type) in self.class_table[kind]:
                if name == cur_name:
                    return kind

        return ""

    def type_of(self, name: str) -> str:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            str: the type of the named identifier in the current scope.
        """
        # Your code goes here!
        for kind in SymbolTable.SUBROUTINE_KINDS:
            for (cur_name, cur_type) in self.subroutine_table[kind]:
                if name == cur_name:
                    return cur_type

        for kind in SymbolTable.CLASS_KINDS:
            for (cur_name, cur_type) in self.class_table[kind]:
                if name == cur_name:
                    return cur_type

        return ""

    def index_of(self, name: str) -> int:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            int: the index assigned to the named identifier.
        """
        # Your code goes here!
        for kind in SymbolTable.SUBROUTINE_KINDS:
            for index, (cur_name, cur_type) in enumerate(self.subroutine_table[kind]):
                if name == cur_name:
                    return index

        for kind in SymbolTable.CLASS_KINDS:
            for index, (cur_name, cur_type) in enumerate(self.class_table[kind]):
                if name == cur_name:
                    return index

        return -1


