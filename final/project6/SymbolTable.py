"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""


class SymbolTable:
    """
    A symbol table that keeps a correspondence between symbolic labels and 
    numeric addresses.
    """

    def __init__(self) -> None:
        """Creates a new symbol table initialized with all the predefined symbols
        and their pre-allocated RAM addresses, according to section 6.2.3 of the
        book.
        """
        # Your code goes here!
        self.n = 16
        self.symbolTable = {"SCREEN" : "16384", "KBD" : "24576", "SP" : "0", "LCL" : "1", "ARG" : "2", "THIS": "3",
                            "THAT" : "4", "LOOP" : "4", "STOP" : "18", "END" : "22"}
        for i in range(0, 16):
            symbol = "R"
            symbol += str(i)
            self.symbolTable[symbol] = i

    def add_entry(self, symbol: str, address: int) -> None:
        """Adds the pair (symbol, address) to the table.

        Args:
            symbol (str): the symbol to add.
            address (int): the address corresponding to the symbol.
        """
        # Your code goes here!
        self.symbolTable[symbol] = address

    def contains(self, symbol: str) -> bool:
        """Does the symbol table contain the given symbol?

        Args:
            symbol (str): a symbol.

        Returns:
            bool: True if the symbol is contained, False otherwise.
        """
        # Your code goes here!
        return self.symbolTable.get(symbol) is not None

    def get_address(self, symbol: str) -> int:
        """Returns the address associated with the symbol.

        Args:
            symbol (str): a symbol.

        Returns:
            int: the address associated with the symbol.
        """
        # Your code goes here!
        return self.symbolTable[symbol]
