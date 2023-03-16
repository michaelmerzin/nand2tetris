"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import typing


class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    TEMP_START_ADDRESS = "@5\n"

    DE_REFERENCE_ADDRESS = \
        "@address\n" + \
        "A=M;\n" + \
        "D=M;\n" + \
        "@address_value\n" + \
        "M=D;\n"

    DE_REFERENCE_STATIC_I = lambda file_name, i:\
        f"@{file_name}.{i}\n" + \
        "D=M;\n" + \
        "@address_value\n" + \
        "M=D;\n"

    DE_REFERENCE_SP = \
        "@SP\n" + \
        "A=M;\n" + \
        "D=M;\n" + \
        "@sp_value\n" + \
        "M=D;\n"

    ADDRESS_EQUAL = \
        "@sp_value\n" + \
        "D=M;\n" + \
        "@address\n" + \
        "A=M;\n" + \
        "M=D;\n"

    STATIC_EQUAL_I = lambda file_name, i: \
        "@sp_value\n" + \
        "D=M;\n" + \
        f"@{file_name}.{i}\n" + \
        "M=D;\n"

    SP_EQUAL = \
        "@address_value\n" + \
        "D=M;\n" + \
        "@SP\n" + \
        "A=M;\n" + \
        "M=D;\n"

    SP_PLUS = \
        "@SP\n" + \
        "M=M+1;\n"

    SP_MINUS = \
        "@SP\n" + \
        "M=M-1;\n"

    POP_VALUE_X = \
            "@SP\n" + \
            "M=M-1;\n" + \
            "@SP\n" + \
            "A=M;\n" + \
            "D=M;\n" + \
            "@x\n" + \
            "M=D;\n"

    POP_VALUE_Y = \
        "@SP\n" + \
        "M=M-1;\n" + \
        "@SP\n" + \
        "A=M;\n" + \
        "D=M;\n" + \
        "@y\n" + \
        "M=D;\n"

    PUSH_D = \
        "@SP\n" + \
        "A=M;\n" + \
        "M=D;\n" + \
        SP_PLUS

    PUSH_D_I = lambda i: \
        f"(PUSH{i})\n" + \
        f"@SP\n" + \
        f"A=M;\n" + \
        f"M=D;\n" + \
        CodeWriter.SP_PLUS

    GOOD_CONDITION_I = lambda i: f"(GOOD{i})\n" \
                                 f"D=-1;\n"

    BAD_CONDITION_I = lambda i: f"(BAD{i})\n" \
                              f"D=0;\n" \
                              f"@PUSH{i}\n" \
                              f"0;JMP\n"

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.output_stream = output_stream
        self.cond_index = 0

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is 
        started.

        Args:
            filename (str): The name of the VM file.
        """
        # Your code goes here!
        # This function is useful when translating code that handles the
        # static segment. For example, in order to prevent collisions between two
        # .vm files which push/pop to the static segment, one can use the current
        # file's name in the assembly variable's name and thus differentiate between
        # static variables belonging to different files.
        # To avoid problems with Linux/Windows/MacOS differences with regards
        # to filenames and paths, you are advised to parse the filename in
        # the function "translate_file" in Main.py using python's os library,
        # For example, using code similar to:
        # input_filename, input_extension = os.path.splitext(os.path.basename(input_file.name))

    def write_arithmetic(self, command: str) -> None:
        """Writes assembly code that is the translation of the given 
        arithmetic command. For the commands eq, lt, gt, you should correctly
        compare between all numbers our computer supports, and we define the
        value "true" to be -1, and "false" to be 0.

        Args:
            command (str): an arithmetic command.
        """
        # Your code goes here!

        output = ""
        if command== "add":
            output = CodeWriter.add_arithmetic(self)

        elif command == "sub":
            output = CodeWriter.sub_arithmetic(self)

        elif command == "neg":
            output = CodeWriter.neg_arithmetic(self)

        elif command == "eq":
            output = CodeWriter.eq_arithmetic(self)
            self.cond_index += 1

        elif command == "gt":
            output = CodeWriter.gt_arithmetic(self)
            self.cond_index += 1

        elif command == "lt":
            output = CodeWriter.lt_arithmetic(self)
            self.cond_index += 1

        elif command == "and":
            output = CodeWriter.and_arithmetic(self)

        elif command == "or":
            output = CodeWriter.or_arithmetic(self)

        elif command == "not":
            output = CodeWriter.not_arithmetic(self)

        self.output_stream.write(output)

    @staticmethod
    def add_arithmetic(self) -> str:
        add = \
            "@x\n" + \
            "D=M;\n" + \
            "@y\n" + \
            "D=D+M;\n"

        return "// add ///////////////////////\n" + CodeWriter.POP_VALUE_Y + CodeWriter.POP_VALUE_X + add + CodeWriter.PUSH_D

    @staticmethod
    def sub_arithmetic(self) -> str:
        sub = \
            "@x\n" + \
            "D=M;\n" + \
            "@y\n" + \
            "D=D-M;\n"

        return "// sub ///////////////////////\n" + CodeWriter.POP_VALUE_Y + CodeWriter.POP_VALUE_X + sub + CodeWriter.PUSH_D

    @staticmethod
    def neg_arithmetic(self) -> str:
        neg = \
            "@x\n" + \
            "D=M;\n" + \
            "D=-D;\n"

        return "// neg ///////////////////////\n" + CodeWriter.POP_VALUE_X + neg + CodeWriter.PUSH_D

    @staticmethod
    def eq_arithmetic(self) -> str:
        eq_check = \
            "@x\n" + \
            "D=M;\n" + \
            "@y\n" + \
            "D=D-M;\n" + \
            "@GOOD" + str(self.cond_index) + "\n" + \
            "D;JEQ\n"

        return "// eq ///////////////////////\n" + CodeWriter.POP_VALUE_Y + CodeWriter.POP_VALUE_X + eq_check + \
               CodeWriter.BAD_CONDITION_I(self.cond_index) + CodeWriter.GOOD_CONDITION_I(self.cond_index) + CodeWriter.PUSH_D_I(self.cond_index)

    @staticmethod
    def gt_arithmetic(self) -> str:
        gt_check = \
            "@x\n" + \
            "D=M;\n" + \
            "@y\n" + \
            "D=D-M;\n" + \
            "@GOOD" + str(self.cond_index) + "\n" + \
            "D;JGT\n"

        return "// gt ///////////////////////\n" + CodeWriter.POP_VALUE_Y + CodeWriter.POP_VALUE_X + gt_check + \
               CodeWriter.BAD_CONDITION_I(self.cond_index) + CodeWriter.GOOD_CONDITION_I(self.cond_index) + CodeWriter.PUSH_D_I(self.cond_index)

    @staticmethod
    def lt_arithmetic(self) -> str:
        lt_check = \
            "@x\n" + \
            "D=M;\n" + \
            "@y\n" + \
            "D=D-M;\n" + \
            "@GOOD" + str(self.cond_index) + "\n" + \
            "D;JLT\n" \

        return "// lt  ///////////////////////\n" + CodeWriter.POP_VALUE_Y + CodeWriter.POP_VALUE_X + lt_check + \
               CodeWriter.BAD_CONDITION_I(self.cond_index) + CodeWriter.GOOD_CONDITION_I(self.cond_index) + CodeWriter.PUSH_D_I(self.cond_index)

    @staticmethod
    def and_arithmetic(self) -> str:
        and_arith = \
            "@x\n" + \
            "D=M;\n" + \
            "@y\n" + \
            "D=D&M;\n"

        return "// and ///////////////////////\n" + CodeWriter.POP_VALUE_Y + CodeWriter.POP_VALUE_X + and_arith + CodeWriter.PUSH_D

    @staticmethod
    def or_arithmetic(self) -> str:
        or_arith = \
            "@x\n" + \
            "D=M;\n" + \
            "@y\n" + \
            "D=D|M;\n"

        return "// or ///////////////////////\n" + CodeWriter.POP_VALUE_Y + CodeWriter.POP_VALUE_X + or_arith + CodeWriter.PUSH_D

    @staticmethod
    def not_arithmetic(self) -> str:
        not_arith = \
            "@x\n" + \
            "D=M;\n" + \
            "D=!D;\n"

        return "// not ///////////////////////\n" + CodeWriter.POP_VALUE_X + not_arith + CodeWriter.PUSH_D

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes assembly code that is the translation of the given 
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        # Your code goes here!
        # Note: each reference to "static i" appearing in the file Xxx.vm should
        # be translated to the assembly symbol "Xxx.i". In the subsequent
        # assembly process, the Hack assembler will allocate these symbolic
        # variables to the RAM, starting at address 16.

        if segment == "local" or segment == "argument" or segment == "this" or segment == "that":
            output = CodeWriter.base_segments(command, segment, index)

        elif segment == "constant":
            output = CodeWriter.constant_segments(command, segment, index)

        elif segment == "static":
            output = CodeWriter.static_segments(command, segment, index)

        elif segment == "temp":
            output = CodeWriter.temp_segments(command, segment, index)

        else:
            output = CodeWriter.pointer_segments(command, segment, index)

        if command == "C_PUSH":
            self.output_stream.write(f"// push {segment} {str(index)}\n")
        else:
            self.output_stream.write(f"// pop {segment} {str(index)}\n")

        self.output_stream.write(output)

    @staticmethod
    def pointer_segments(command: str, segment: str, index: int) -> str:
        if index == 1:
            segment_pointer = "@THAT\n"

        else:
            segment_pointer = "@THIS\n"

        address = \
            segment_pointer + \
            "D=A;\n" + \
            "@address\n" + \
            "M=D;\n"

        if command == "C_PUSH":
            output = address + CodeWriter.DE_REFERENCE_ADDRESS + CodeWriter.SP_EQUAL + CodeWriter.SP_PLUS
        else:
            output = address + CodeWriter.SP_MINUS + CodeWriter.DE_REFERENCE_SP + CodeWriter.ADDRESS_EQUAL
        return output

    @staticmethod
    def temp_segments(command: str, segment: str, index: int) -> str:
        address = \
            CodeWriter.TEMP_START_ADDRESS + \
            "D=A;\n" + \
            "@" + str(index) + "\n" + \
            "D=D+A;\n" + \
            "@address\n" + \
            "M=D;\n"

        if command == "C_PUSH":
            output = address + CodeWriter.DE_REFERENCE_ADDRESS + CodeWriter.SP_EQUAL + CodeWriter.SP_PLUS
        else:
            output = address + CodeWriter.SP_MINUS + CodeWriter.DE_REFERENCE_SP + CodeWriter.ADDRESS_EQUAL

        return output

    @staticmethod
    def static_segments(command: str, segment: str, index: int) -> str:
        file_name = "Foo"

        if command == "C_PUSH":
            output = CodeWriter.DE_REFERENCE_STATIC_I(file_name, index) + CodeWriter.SP_EQUAL + CodeWriter.SP_PLUS
        else:
            output = CodeWriter.SP_MINUS + CodeWriter.DE_REFERENCE_SP + CodeWriter.STATIC_EQUAL_I(file_name, index)

        return output

    @staticmethod
    def constant_segments(command: str, segment: str, index: int) -> str:
        de_reference_sp = \
            "@" + str(index) + "\n" + \
            "D=A;\n" + \
            "@SP\n" + \
            "A=M;\n" + \
            "M=D;\n"

        constant_output = de_reference_sp + CodeWriter.SP_PLUS
        return constant_output

    @staticmethod
    def base_segments(command: str, segment: str, index: int) -> str:
        segment_pointer = ""
        if segment == "local":
            segment_pointer = "@LCL\n"
        elif segment == "argument":
            segment_pointer = "@ARG\n"
        elif segment == "this":
            segment_pointer = "@THIS\n"
        elif segment == "that":
            segment_pointer = "@THAT\n"

        address = \
            segment_pointer + \
            "A=M;\n" + \
            "D=A;\n" + \
            "@" + str(index) + "\n" + \
            "D=D+A;\n" + \
            "@address\n" + \
            "M=D;\n"

        if command == "C_PUSH":
            output = address + CodeWriter.DE_REFERENCE_ADDRESS + CodeWriter.SP_EQUAL + CodeWriter.SP_PLUS
        else:
            output = address + CodeWriter.SP_MINUS + CodeWriter.DE_REFERENCE_SP + CodeWriter.ADDRESS_EQUAL

        return output


    def write_label(self, label: str) -> None:
        """Writes assembly code that affects the label command. 
        Let "Xxx.foo" be a function within the file Xxx.vm. The handling of
        each "label bar" command within "Xxx.foo" generates and injects the symbol
        "Xxx.foo$bar" into the assembly code stream.
        When translating "goto bar" and "if-goto bar" commands within "foo",
        the label "Xxx.foo$bar" must be used instead of "bar".

        Args:
            label (str): the label to write.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass

    def write_goto(self, label: str) -> None:
        """Writes assembly code that affects the goto command.

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass

    def write_if(self, label: str) -> None:
        """Writes assembly code that affects the if-goto command. 

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass

    def write_function(self, function_name: str, n_vars: int) -> None:
        """Writes assembly code that affects the function command. 
        The handling of each "function Xxx.foo" command within the file Xxx.vm
        generates and injects a symbol "Xxx.foo" into the assembly code stream,
        that labels the entry-point to the function's code.
        In the subsequent assembly process, the assembler translates this 
        symbol into the physical address where the function code starts.

        Args:
            function_name (str): the name of the function.
            n_vars (int): the number of local variables of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "function function_name n_vars" is:
        # (function_name)       // injects a function entry label into the code
        # repeat n_vars times:  // n_vars = number of local variables
        #   push constant 0     // initializes the local variables to 0
        pass

    def write_call(self, function_name: str, n_args: int) -> None:
        """Writes assembly code that affects the call command. 
        Let "Xxx.foo" be a function within the file Xxx.vm.
        The handling of each "call" command within Xxx.foo's code generates and
        injects a symbol "Xxx.foo$ret.i" into the assembly code stream, where
        "i" is a running integer (one such symbol is generated for each "call"
        command within "Xxx.foo").
        This symbol is used to mark the return address within the caller's 
        code. In the subsequent assembly process, the assembler translates this
        symbol into the physical memory address of the command immediately
        following the "call" command.

        Args:
            function_name (str): the name of the function to call.
            n_args (int): the number of arguments of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "call function_name n_args" is:
        # push return_address   // generates a label and pushes it to the stack
        # push LCL              // saves LCL of the caller
        # push ARG              // saves ARG of the caller
        # push THIS             // saves THIS of the caller
        # push THAT             // saves THAT of the caller
        # ARG = SP-5-n_args     // repositions ARG
        # LCL = SP              // repositions LCL
        # goto function_name    // transfers control to the callee
        # (return_address)      // injects the return address label into the code
        pass

    def write_return(self) -> None:
        """Writes assembly code that affects the return command."""
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "return" is:
        # frame = LCL                   // frame is a temporary variable
        # return_address = *(frame-5)   // puts the return address in a temp var
        # *ARG = pop()                  // repositions the return value for the caller
        # SP = ARG + 1                  // repositions SP for the caller
        # THAT = *(frame-1)             // restores THAT for the caller
        # THIS = *(frame-2)             // restores THIS for the caller
        # ARG = *(frame-3)              // restores ARG for the caller
        # LCL = *(frame-4)              // restores LCL for the caller
        # goto return_address           // go to the return address
        pass
