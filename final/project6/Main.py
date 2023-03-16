"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from SymbolTable import SymbolTable
from Parser import Parser
from Code import Code

BINARY_LENGTH = 15

def assemble_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """
    # Your code goes here!
    # A good place to start is to initialize a new Parser object:
    # parser = Parser(input_file)
    # Note that you can write to output_file like so:
    # output_file.write("Hello world! \n")
    parser = Parser(input_file)
    symbol_table = SymbolTable()
    jmp_symbol_handler(parser, symbol_table)

    while parser.has_more_commands():
        output_line = ""
        if parser.command_type() == "A_COMMAND":
            symbol = parser.symbol()
            if symbol.isnumeric():
                address = symbol
            else:
                address = ver_symbol_handler(symbol, symbol_table)

            output_line = "0" + decimal_to_binary(address)

        elif parser.command_type() == "C_COMMAND":
            dest = parser.dest()
            dest_byte = Code.dest(dest)
            comp = parser.comp()
            comp_byte = Code.comp(comp)
            jump = parser.jump()
            jump_byte = Code.jump(jump)
            output_line = "1" + comp_byte + dest_byte + jump_byte

        if output_line:
            output_file.write(output_line + "\n")
        parser.advance()


def decimal_to_binary(str_num):

    num = int(str_num)
    binary_num = bin(num)[2:]
    ret = str(binary_num)
    while len(ret) < BINARY_LENGTH:
        ret = "0" + ret

    return ret


def ver_symbol_handler(symbol, symbol_table):
    if not symbol_table.contains(symbol):
        symbol_table.add_entry(symbol, symbol_table.n)
        symbol_table.n += 1

    return symbol_table.symbolTable[symbol]


def jmp_symbol_handler(parser, symbol_table):
    count_l_command = 0
    while parser.has_more_commands():
        if parser.command_type() == "L_COMMAND":
            symbol = parser.symbol()
            valid_line_index = parser.index - count_l_command
            symbol_table.add_entry(symbol, valid_line_index)
            count_l_command += 1
        parser.advance()

    parser.reset()


if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: Assembler <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".asm":
            continue
        output_path = filename + ".hack"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            assemble_file(input_file, output_file)
