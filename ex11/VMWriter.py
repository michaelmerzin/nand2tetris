"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class VMWriter:
    """
    Writes VM commands into a file. Encapsulates the VM command syntax.
    """
    CONST = "constant"
    ARG = "argument"
    LOCAL = "local"
    STATIC = "static"
    THIS = "this"
    THAT = "that"
    POINTER = "pointer"
    TEMP = "temp"

    ADD = {"+": "ADD"}
    SUB = {"-": "SUB"}
    NEG = {"-": "NEG"}
    NEG_IF = {"~": "NOT"}
    EQ = {"=": "EQ"}
    GT = {">": "GT"}
    LT = {"<": "LT"}
    #   TODO
    AND = {"&": "AND"}
    OR = {"|": "OR"}
    NOT = {"-": "NOT"}

    SHIFTLEFT = {'^': "SHIFTLEFT"}
    SHIFTRIGHT = {'#': "SHIFTRIGHT"}

    MULT = {"*": ("Math.multiply", 2)}
    DIVIDE = {"/": ("Math.divide", 2)}

    VOID_SEGMENT = TEMP
    VOID_INDEX = 0

    ONE_VARS = [NEG_IF, NEG, NOT, SHIFTLEFT, SHIFTRIGHT]
    TWO_VARS = [ADD, SUB, EQ, GT, LT, AND, OR, MULT, DIVIDE]
    MATH = [MULT, DIVIDE]
    SEGMENTS = [CONST, ARG, LOCAL, STATIC, THIS, THAT, TEMP]
    ARITHMETIC = [ADD, SUB, NEG, EQ, GT, LT, AND, OR, NOT, SHIFTLEFT, SHIFTRIGHT]

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Creates a new file and prepares it for writing VM commands."""
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.output_stream = output_stream

    def write_push(self, segment: str, index: int) -> None:
        """Writes a VM push command.

        Args:
            segment (str): the segment to push to, can be "CONST", "ARG", 
            "LOCAL", "STATIC", "THIS", "THAT", "POINTER", "TEMP"
            index (int): the index to push to.
        """
        # Your code goes here!
        output = f"push {segment.lower()} {index}\n"
        self.output_stream.write(output)

    def write_pop(self, segment: str, index: int) -> None:
        """Writes a VM pop command.

        Args:
            segment (str): the segment to pop from, can be "CONST", "ARG", 
            "LOCAL", "STATIC", "THIS", "THAT", "POINTER", "TEMP".
            index (int): the index to pop from.
        """
        # Your code goes here!
        output = f"pop {segment.lower()} {index}\n"
        self.output_stream.write(output)

    def write_arithmetic(self, command: str) -> None:
        """Writes a VM arithmetic command.

        Args:
            command (str): the command to write, can be "ADD", "SUB", "NEG", 
            "EQ", "GT", "LT", "AND", "OR", "NOT", "SHIFTLEFT", "SHIFTRIGHT".
        """
        # Your code goes here!

        output = f"{command.lower()}\n"
        self.output_stream.write(output)

    def write_label(self, label: str) -> None:
        """Writes a VM label command.

        Args:
            label (str): the label to write.
        """
        # Your code goes here!
        output = f"label {label.lower()}\n"
        self.output_stream.write(output)

    def write_goto(self, label: str) -> None:
        """Writes a VM goto command.

        Args:
            label (str): the label to go to.
        """
        # Your code goes here!
        output = f"goto {label.lower()}\n"
        self.output_stream.write(output)

    def write_if(self, label: str) -> None:
        """Writes a VM if-goto command.

        Args:
            label (str): the label to go to.
        """
        # Your code goes here!
        output = f"if-goto {label.lower()}\n"
        self.output_stream.write(output)

    def write_call(self, name: str, n_args: int) -> None:
        """Writes a VM call command.

        Args:
            name (str): the name of the function to call.
            n_args (int): the number of arguments the function receives.
        """
        # Your code goes here!
        output = f"call {name} {n_args}\n"
        self.output_stream.write(output)

    def write_function(self, name: str, n_locals: int) -> None:
        """Writes a VM function command.

        Args:
            name (str): the name of the function.
            n_locals (int): the number of local variables the function uses.
        """
        # Your code goes here!
        output = f"function {name} {n_locals}\n"
        self.output_stream.write(output)

    def write_return(self) -> None:
        """Writes a VM return command."""
        # Your code goes here!
        output = f"return\n"
        self.output_stream.write(output)
