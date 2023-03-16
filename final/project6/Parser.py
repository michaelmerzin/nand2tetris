"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
from curses.ascii import NUL
import typing



class Parser:
    """Encapsulates access to the input code. Reads an assembly program
    by reading each command line-by-line, parses the current command,
    and provides convenient access to the commands components (fields
    and symbols). In addition, removes all white space and comments.
    """

    COMMENT_SYNTAX = "//"

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
            input_file (typing.TextIO): input file.
        """
        # Your code goes here!
        # A good place to start is to read all the lines of the input:
        # input_lines = input_file.read().splitlines()
        self.lines = []
        self.index = 0
        for line in input_file:
            no_comment = line.split(Parser.COMMENT_SYNTAX)[0]
            valid_code = no_comment.strip(" \n")
            if valid_code:
                self.lines.append(valid_code)

    def reset(self) -> None:
        self.index = 0

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        # Your code goes here!
        return self.index < len(self.lines)

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
        # Your code goes here!

        if self.has_more_commands():
            self.index += 1

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        # Your code goes here!
        line = self.lines[self.index]
        if not line:
            return ""
        if line.startswith("@"):
            return "A_COMMAND"
        elif line.startswith("("):
            return "L_COMMAND"
        return "C_COMMAND"

    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or 
            "L_COMMAND".
        """
        # Your code goes here!
        line = self.lines[self.index]
        value = line.strip("@()")
        value = value.replace(" ", "")
        return value

    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!
        line = self.lines[self.index]
        values = line.split("=")
        if len(values) < 2:
            return ""
        dest = values[0]
        dest = dest.replace(" ", "")
        return dest

    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!
        line = self.lines[self.index]
        values = line.split("=")
        if len(values) < 2:
            comp_and_jmp = line
        else:
            comp_and_jmp = values[1]

        values = comp_and_jmp.split(";")
        comp = values[0]
        comp = comp.replace(" ", "")
        return comp

    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!
        line = self.lines[self.index]
        values = line.split("=")
        if len(values) < 2:
            comp_and_jmp = line
        else:
            comp_and_jmp = values[1]
        values = comp_and_jmp.split(";")
        if len(values) < 2:
            return ""
        jmp = values[1]
        jmp = jmp.replace(" ", "")
        return jmp

