"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """
    # Parser
    
    Handles the parsing of a single .vm file, and encapsulates access to the
    input code. It reads VM commands, parses them, and provides convenient 
    access to their components. 
    In addition, it removes all white space and comments.

    ## VM Language Specification

    A .vm file is a stream of characters. If the file represents a
    valid program, it can be translated into a stream of valid assembly 
    commands. VM commands may be separated by an arbitrary number of whitespace
    characters and comments, which are ignored. Comments begin with "//" and
    last until the line’s end.
    The different parts of each VM command may also be separated by an arbitrary
    number of non-newline whitespace characters.

    - Arithmetic commands:
      - add, sub, and, or, eq, gt, lt
      - neg, not, shiftleft, shiftright
    - Memory segment manipulation:
      - push <segment> <number>
      - pop <segment that is not constant> <number>
      - <segment> can be any of: argument, local, static, constant, this, that, 
                                 pointer, temp
    - Branching (only relevant for project 8):
      - label <label-name>
      - if-goto <label-name>
      - goto <label-name>
      - <label-name> can be any combination of non-whitespace characters.
    - Functions (only relevant for project 8):
      - call <function-name> <n-args>
      - function <function-name> <n-vars>
      - return
    """

    COMMENT_SYNTAX = "//"

    ARITHMETIC_CMD = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]
    MEMORY_CMD = ["pop", "push"]

    def __init__(self, input_file: typing.TextIO) -> None:
        """Gets ready to parse the input file.

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
            valid_code = no_comment.strip("\n")
            if valid_code:
                self.lines.append(valid_code)

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        # Your code goes here!
        return self.index < len(self.lines)

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current 
        command. Should be called only if has_more_commands() is true. Initially
        there is no current command.
        """
        # Your code goes here!
        if self.has_more_commands():
            self.index += 1


    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current VM command.
            "C_ARITHMETIC" is returned for all arithmetic commands.
            For other commands, can return:
            "C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION",
            "C_RETURN", "C_CALL".
        """
        # Your code goes here!
        line = self.lines[self.index]
        if not line:
            return ""

        for arithmetic in Parser.ARITHMETIC_CMD:
            if line.startswith(arithmetic):
                return "C_ARITHMETIC"

        if line.startswith("push"):
            return "C_PUSH"

        elif line.startswith("pop"):
            return "C_POP"

        elif line.startswith("label"):
            return "C_LABEL"

        elif line.startswith("goto"):
            return "C_GOTO"

        elif line.startswith("if-goto"):
            return "C_IF"

        elif line.startswith("function"):
            return "C_FUNCTION"

        elif line.startswith("call"):
            return "C_CALL"

        elif line.startswith("call"):
            return "C_RETURN"

    def arg1(self) -> str:
        """
        Returns:
            str: the first argument of the current command. In case of
            "C_ARITHMETIC", the command itself (add, sub, etc.) is returned.
            Should not be called if the current command is "C_RETURN".
        """
        # Your code goes here!
        line = self.lines[self.index]
        if self.command_type() == "C_RETURN":
            return ""

        if self.command_type() == "C_ARITHMETIC":
            return line.strip(" ")

        str_arr = line.split(" ")
        if len(str_arr) > 1:
            return str_arr[1]

        return ""

    def arg2(self) -> int:
        """
        Returns:
            int: the second argument of the current command. Should be
            called only if the current command is "C_PUSH", "C_POP", 
            "C_FUNCTION" or "C_CALL".
        """
        # Your code goes here!
        line = self.lines[self.index]

        str_arr = line.split(" ")
        if len(str_arr) > 2:
            return int(str_arr[2])

        return -1
