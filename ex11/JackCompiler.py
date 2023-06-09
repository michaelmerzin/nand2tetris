
import os
import sys
import typing
from CompilationEngine import CompilationEngine
from JackTokenizer import JackTokenizer
from SymbolTable import SymbolTable
from VMWriter import VMWriter


def compile_file(
        input_file: typing.TextIO, output_stream_vm: typing.TextIO, output_stream_xml: typing.TextIO) -> None:
    """Compiles a single file.

    Args:
        input_file (typing.TextIO): the file to compile.
        output_file (typing.TextIO): writes all output to this file.
    """
    # Your code goes here!
    # This function should be relatively similar to "analyze_file" in
    # JackAnalyzer.py from the previous project.
    tokenizer = JackTokenizer(input_file)
    engine = CompilationEngine(tokenizer, output_stream_vm, output_stream_xml)


if "__main__" == __name__:
    # Parses the input path and calls compile_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: JackCompiler <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".jack":
            continue

        #   TODO API change back
        output_path1 = filename + ".vm"
        output_path2 = filename + ".xml"
        with open(input_path, 'r') as input_file, \
                open(output_path1, 'w') as output_file1, open(output_path2, 'w') as output_file2:
                        compile_file(input_file, output_file1, output_file2)
