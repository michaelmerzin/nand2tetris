"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""

import typing
from typing import Tuple, Any

from SymbolTable import SymbolTable
from JackTokenizer import JackTokenizer
from VMWriter import VMWriter


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    XML_SPECIAL = {"<": "&lt;", ">": "&gt;", "&": "&amp;"}
    SPECIAL_GRAMMAR_LET = "50006"
    SPECIAL_GRAMMAR_IF = "50005"
    SPECIAL_GRAMMAR_WHILE = "50004"
    SPECIAL_GRAMMAR_DO = "50003"
    SPECIAL_GRAMMAR_RETURN = "50002"
    SPECIAL_GRAMMAR_IDENTIFIER = "50001"
    SPECIAL_GRAMMAR_TYPE = "50000"
    BAD_ERROR_MSG = "DEAD ERRORRRRRRRRRR"
    ERROR_MSG = "its my error :) invalid syntax :) go fix it :("
    cond_index = 0
    LABEL = lambda i: f"L{i}"

    def __init__(self, input_stream: JackTokenizer, output_stream_vm: typing.TextIO,
                 output_stream_xml: typing.TextIO) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.input_stream = input_stream
        self.output_stream = output_stream_xml
        self.count_tabs = 0
        self.cur_class_name = ""
        self.subroutine_name = ""
        self.class_name = ""
        self.cur_subroutine_name = ""
        self.function_type = ""
        self.is_class_name = True
        self.is_subroutine_name = False
        self.symbol_table = SymbolTable()
        self.vm_writer = VMWriter(output_stream_vm)
        self.cur_type = ""
        self.function_return_type = ""
        self.count_pushed = 0
        self.compile_class()

    def compile_class(self) -> None:
        """Compiles a complete class."""
        # Your code goes here!
        word = "class"
        output = word
        output = self.write_to_file(output, True)
        self.count_tabs += 1
        output += self.handle_words(["class"], True)
        self.cur_class_name = self.typed_lexical_element(self.input_stream.token_type())
        output += self.compile_identifier(class_name=True)
        output += self.handle_words(["{"])

        self.output_stream.write(output)
        output = ""

        tabs = self.count_tabs
        while True:
            try:
                self.compile_class_var_dec()
            except TypeError:
                break
        self.count_tabs = tabs

        tabs = self.count_tabs
        while True:
            try:
                self.compile_subroutine()
            except TypeError:
                break
        self.count_tabs = tabs

        output += self.handle_words(["}"])
        self.count_tabs -= 1
        output += self.write_to_file(word, False)
        self.output_stream.write(output)

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        # Your code goes here!
        word = "classVarDec"
        output = word
        output = self.write_to_file(output, True)
        self.count_tabs += 1

        kind = self.typed_lexical_element(self.input_stream.token_type()).upper()
        output += self.handle_words(["static", "field"], True)

        output += self.compile_type()
        output += self.compile_identifier(kind=kind, type=self.cur_type, class_name=self.is_class_name)
        tabs = self.count_tabs
        while True:
            try:
                output += self.handle_words([","], True)
            except TypeError:
                break

            output += self.compile_identifier(kind=kind, type=self.cur_type, class_name=self.is_class_name)

        self.count_tabs = tabs
        output += self.handle_words([";"])
        self.count_tabs -= 1
        output += self.write_to_file(word, False)
        self.output_stream.write(output)
        return

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        # Your code goes here!
        word = "subroutineDec"
        output = word
        output = self.write_to_file(output, True)
        self.count_tabs += 1

        self.symbol_table.start_subroutine()

        self.function_type = self.typed_lexical_element(self.input_stream.token_type())
        output += self.handle_words(["constructor", "function", "method"], True)

        if self.function_type == "constructor" or self.function_type == "method":
            self.symbol_table.define("this", self.cur_class_name, SymbolTable.ARGUMENT)

        self.function_return_type = self.typed_lexical_element(self.input_stream.token_type())
        output += self.handle_either(["void"], [CompilationEngine.SPECIAL_GRAMMAR_TYPE])

        function_name = self.typed_lexical_element(self.input_stream.token_type())
        self.cur_subroutine_name = f"{self.cur_class_name}.{function_name}"

        output += self.compile_identifier(subroutine_name=True)
        output += self.handle_words(["("])
        self.output_stream.write(output)
        output = ""
        self.compile_parameter_list()
        output += self.handle_words([")"])

        self.output_stream.write(output)
        output = ""
        output += self.compile_subroutine_body()

        self.count_tabs -= 1
        output += self.write_to_file(word, False)
        self.output_stream.write(output)

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        # Your code goes here!
        word = "parameterList"
        output = word
        output = self.write_to_file(output, True)
        self.count_tabs += 1

        tabs = self.count_tabs
        for i in range(1):
            try:
                output += self.compile_type(True)
            except TypeError:
                break

            self.count_tabs = tabs
            output += self.compile_identifier(kind=SymbolTable.ARGUMENT, type=self.cur_type,
                                              class_name=self.is_class_name)
            tabs = self.count_tabs


            while True:
                try:
                    output += self.handle_words([","], True)
                except TypeError:
                    break
                output += self.compile_type()

                output += self.compile_identifier(kind=SymbolTable.ARGUMENT, type=self.cur_type,
                                                  class_name=self.is_class_name)

        self.count_tabs = tabs
        self.count_tabs -= 1
        output += self.write_to_file(word, False)
        self.output_stream.write(output)

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        # Your code goes here!
        word = "varDec"
        output = word
        output = self.write_to_file(output, True)
        self.count_tabs += 1
        output += self.handle_words(["var"], True)
        output += self.compile_type()
        output += self.compile_identifier(kind=SymbolTable.VAR, type=self.cur_type, class_name=self.is_class_name)

        tabs = self.count_tabs
        while True:
            try:
                tabs = self.count_tabs
                output += self.handle_words([","], True)
            except TypeError:
                break
            output += self.compile_identifier(kind=SymbolTable.VAR, type=self.cur_type, class_name=self.is_class_name)

        self.count_tabs = tabs
        output += self.handle_words([";"])
        self.count_tabs -= 1
        output += self.write_to_file(word, False)
        self.output_stream.write(output)

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        # Your code goes here!
        word = "statements"
        output = word
        output = self.write_to_file(output, True)
        self.count_tabs += 1

        tabs = self.count_tabs
        while True:
            try:
                self.output_stream.write(output)
                output = ""
                self.compile_statement(True)
            except TypeError:
                break
        self.count_tabs = tabs


        self.count_tabs -= 1
        output += self.write_to_file(word, False)
        self.output_stream.write(output)

    def compile_do(self) -> None:
        """Compiles a do statement."""
        # Your code goes here!
        word = "doStatement"
        output = word
        output = self.write_to_file(output, True)
        self.count_tabs += 1

        output += self.handle_words(["do"], True)
        self.output_stream.write(output)
        output = ""
        output += self.compile_subroutine_call(False)
        output += self.handle_words([";"])

        segment = VMWriter.VOID_SEGMENT
        index = VMWriter.VOID_INDEX
        self.vm_writer.write_pop(segment, index)

        self.count_tabs -= 1
        output += self.write_to_file(word, False)
        self.output_stream.write(output)

    def compile_let(self) -> None:
        """Compiles a let statement."""
        # Your code goes here!
        word = "letStatement"
        output = word
        output = self.write_to_file(output, True)
        self.count_tabs += 1

        output += self.handle_words(["let"], True)
        name = self.typed_lexical_element(self.input_stream.token_type())
        output += self.compile_identifier()
        is_arr = False
        if self.typed_lexical_element(self.input_stream.token_type()) == "[":
            is_arr = True
            segment = self.symbol_table.kind_of(name)
            index = self.symbol_table.index_of(name)
            self.vm_writer.write_push(self.kind_to_segment(segment), index)

        tabs = self.count_tabs
        for i in range(1):
            if self.typed_lexical_element(self.input_stream.token_type()) == "=":
                break
            try:
                output += self.handle_words(["["], True)
            except TypeError:
                break
            self.output_stream.write(output)
            output = ""
            self.compile_expression()
            output += self.handle_words(["]"])
            self.vm_writer.write_arithmetic("ADD")


        self.count_tabs = tabs

        output += self.handle_words(["="])
        self.output_stream.write(output)
        output = ""
        self.compile_expression()
        output += self.handle_words([";"])

        if is_arr:
            self.vm_writer.write_pop(VMWriter.TEMP,  0)
            self.vm_writer.write_pop(VMWriter.POINTER, 1)
            self.vm_writer.write_push(VMWriter.TEMP, 0)
            self.vm_writer.write_pop(VMWriter.THAT, 0)

        else:
            segment = self.symbol_table.kind_of(name)
            index = self.symbol_table.index_of(name)
            if segment:
                self.vm_writer.write_pop(self.kind_to_segment(segment), index)

        self.count_tabs -= 1
        output += self.write_to_file(word, False)
        self.output_stream.write(output)

    def compile_while(self) -> None:
        """Compiles a while statement."""
        # Your code goes here!
        word = "whileStatement"
        output = word
        output = self.write_to_file(output, True)
        self.count_tabs += 1

        output += self.handle_words(["while"], True)
        output += self.handle_words(["("])
        self.output_stream.write(output)
        output = ""

        l1 = self.cond_index
        self.vm_writer.write_label(CompilationEngine.LABEL(l1))
        self.cond_index += 1

        self.compile_expression()

        self.vm_writer.write_arithmetic("NOT")
        l2 = self.cond_index
        self.vm_writer.write_if(CompilationEngine.LABEL(l2))
        self.cond_index += 1

        output += self.handle_words([")"])
        output += self.handle_words(["{"])
        self.output_stream.write(output)
        output = ""
        self.compile_statements()
        output += self.handle_words(["}"])

        self.vm_writer.write_goto(CompilationEngine.LABEL(l1))
        self.vm_writer.write_label(CompilationEngine.LABEL(l2))

        self.count_tabs -= 1
        output += self.write_to_file(word, False)
        self.output_stream.write(output)

    def compile_return(self) -> None:
        """Compiles a return statement."""
        # Your code goes here!
        word = "returnStatement"
        output = word
        output = self.write_to_file(output, True)
        self.count_tabs += 1
        output += self.handle_words(["return"], True)

        tabs = self.count_tabs


        for i in range(1):
            try:
                self.output_stream.write(output)
                output = ""
                if not self.typed_lexical_element(self.input_stream.token_type()) == ";":
                    self.compile_expression()
            except TypeError:
                break
        self.count_tabs = tabs

        if self.function_return_type == "void":
            self.vm_writer.write_push(VMWriter.CONST, 0)
        self.vm_writer.write_return()

        output += self.handle_words([";"])
        self.count_tabs -= 1
        output += self.write_to_file(word, False)
        self.output_stream.write(output)

    def compile_if(self) -> None:
        """Compiles an if statement, possibly with a trailing else clause."""
        # Your code goes here!
        word = "ifStatement"
        output = word
        output = self.write_to_file(output, True)
        self.count_tabs += 1

        output += self.handle_words(["if"], True)
        output += self.handle_words(["("])
        self.output_stream.write(output)
        output = ""
        self.compile_expression()

        self.vm_writer.write_arithmetic("NOT")
        l1 = self.cond_index
        self.vm_writer.write_if(CompilationEngine.LABEL(l1))
        self.cond_index += 1

        output += self.handle_words([")"])
        output += self.handle_words(["{"])
        self.output_stream.write(output)
        output = ""
        self.compile_statements()
        output += self.handle_words(["}"])

        l2 = self.cond_index
        self.vm_writer.write_goto(CompilationEngine.LABEL(l2))
        self.cond_index += 1
        self.vm_writer.write_label(CompilationEngine.LABEL(l1))

        tabs = self.count_tabs
        for i in range(1):
            try:
                if not self.typed_lexical_element(self.input_stream.token_type()) == "else":
                    break
                output += self.handle_words(["else"], True)
            except TypeError:
                break
            output += self.handle_words(["{"])
            self.output_stream.write(output)
            output = ""
            self.compile_statements()
            output += self.handle_words(["}"])

        self.vm_writer.write_label(CompilationEngine.LABEL(l2))
        self.count_tabs = tabs

        self.count_tabs -= 1
        output += self.write_to_file(word, False)
        self.output_stream.write(output)

    def compile_expression(self) -> None:
        """Compiles an expression."""
        # Your code goes here!
        word = "expression"
        output = word
        output = self.write_to_file(output, True)
        self.count_tabs += 1

        self.output_stream.write(output)
        output = ""
        self.compile_term()
        tabs = self.count_tabs
        while True:
            try:

                str_output, arithmetic_commend = self.compile_op(True)
                output += str_output

            except TypeError:
                break
            self.output_stream.write(output)
            output = ""
            self.compile_term()

            if isinstance(arithmetic_commend, str):
                self.vm_writer.write_arithmetic(arithmetic_commend)

            else:
                self.vm_writer.write_call(arithmetic_commend[0], arithmetic_commend[1])

        self.count_tabs = tabs

        self.count_tabs -= 1
        output += self.write_to_file(word, False)
        self.output_stream.write(output)

    def compile_term(self) -> None:
        """Compiles a term. 
        This routine is faced with a slight difficulty when
        trying to decide between some alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        # Your code goes here!
        word = "term"
        output = word
        output = self.write_to_file(output, True)
        self.count_tabs += 1

        tabs = self.count_tabs

        if self.input_stream.token_type() == "IDENTIFIER":
            name = self.typed_lexical_element(self.input_stream.token_type())
            if self.symbol_table.type_of(name) == "":
                if self.input_stream.has_more_tokens():
                    self.input_stream.advance()

                if self.typed_lexical_element(self.input_stream.token_type()) == ".":
                    output += self.compile_identifier(class_name=True, given_name=name)

                elif self.typed_lexical_element(self.input_stream.token_type()) == "(":
                    output += self.compile_identifier(subroutine_name=True, given_name=name)

                else:
                    output += self.compile_identifier(given_name=name)

            else:
                output += self.compile_identifier()
                segment = self.symbol_table.kind_of(name)
                index = self.symbol_table.index_of(name)
                self.vm_writer.write_push(self.kind_to_segment(segment), index)

                if not self.typed_lexical_element(self.input_stream.token_type()) == "[":
                    self.count_pushed += 1


            try:
                self.output_stream.write(output)
                output = ""
                output += self.compile_array()
            except:
                try:
                    self.output_stream.write(output)
                    output = ""
                    output += self.compile_subroutine_call(True, name=name)
                except:
                    x=1


        else:
            try:
                self.output_stream.write(output)
                output = ""
                output += self.compile_bracket_expression()
            except:
                try:
                    self.output_stream.write(output)
                    output = ""
                    output += self.compile_condition()

                except:
                        try:
                            const_output, int_const = self.compile_integer_const(True)
                            output += const_output
                            self.vm_writer.write_push(VMWriter.CONST, int_const)
                            self.count_pushed += 1

                        except TypeError:
                            try:
                                output += self.compile_string_const(True)
                                self.count_pushed += 1

                            except TypeError:
                                try:
                                    keyword_output, keyword = self.compile_keyword_const(True)
                                    self.switch_case_keyword(keyword)
                                    output += keyword_output

                                except TypeError:
                                    try:
                                        output += self.compile_identifier(True)
                                    except:
                                        x = 1
        self.count_tabs = tabs

        self.count_tabs -= 1
        output += self.write_to_file(word, False)
        self.output_stream.write(output)

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # Your code goes here!
        word = "expressionList"
        output = word
        output = self.write_to_file(output, True)
        self.count_tabs += 1
        tabs = self.count_tabs

        self.count_pushed = 0

        for i in range(1):
            try:
                self.output_stream.write(output)
                output = ""
                if not self.typed_lexical_element(self.input_stream.token_type()) == ")":
                    self.compile_expression()
            except TypeError:
                break

            self.count_tabs = tabs
            tabs = self.count_tabs
            while True:
                try:
                    output += self.handle_words([","], True)
                except TypeError:
                    break
                self.output_stream.write(output)
                output = ""
                self.compile_expression()

        self.count_tabs = tabs
        self.count_tabs -= 1
        output += self.write_to_file(word, False)
        self.output_stream.write(output)

    def compile_subroutine_call(self, is_identifier_compiled, name="") -> str:
        tabs = self.count_tabs

        output = ""
        if not is_identifier_compiled:
            name = self.typed_lexical_element(self.input_stream.token_type())
            if self.symbol_table.type_of(name) == "":
                if self.input_stream.has_more_tokens():
                    self.input_stream.advance()

                if self.typed_lexical_element(self.input_stream.token_type()) == ".":
                    output += self.compile_identifier(class_name=True, given_name=name)

                elif self.typed_lexical_element(self.input_stream.token_type()) == "(":
                    output += self.compile_identifier(subroutine_name=True, given_name=name)

                elif self.typed_lexical_element(self.input_stream.token_type()) == "[":
                    output += self.compile_identifier(given_name=name)

            else:
                output += self.compile_identifier()

        try:
            output = self.compile_class_function(output, name=name)

        except:
            output = self.compile_function(output, func_name=name)

        self.count_tabs = tabs

        return output

    def compile_class_function(self, base_output, name="") -> str:
        output = base_output
        output += self.handle_words(["."])
        func_name = self.typed_lexical_element(self.input_stream.token_type())
        output += self.compile_identifier(subroutine_name=True)
        output += self.handle_words(["("])
        self.output_stream.write(output)
        output = ""
        self.compile_expression_list()
        output += self.handle_words([")"])

        if self.symbol_table.type_of(name):
            segment = self.symbol_table.kind_of(name)
            index = self.symbol_table.index_of(name)
            self.vm_writer.write_push(self.kind_to_segment(segment), index)
            final_name = f"{func_name}"
        else:
            final_name = f"{name}.{func_name}"

        self.vm_writer.write_call(final_name, self.count_pushed)

        return output

    def compile_function(self, base_output, func_name="") -> str:
        output = base_output
        output += self.handle_words(["("])
        self.output_stream.write(output)
        output = ""
        self.compile_expression_list()
        output += self.handle_words([")"])

        self.vm_writer.write_call(func_name, self.count_pushed)
        return output

    def compile_condition(self) -> str:
        output, arithmetic_commend = self.compile_unary_op()
        self.output_stream.write(output)
        output = ""
        self.compile_term()
        self.vm_writer.write_arithmetic(arithmetic_commend)
        return output

    def compile_bracket_expression(self) -> str:
        output = self.handle_words(["("])
        self.output_stream.write(output)
        output = ""
        self.compile_expression()
        output += self.handle_words([")"])
        return output

    def compile_array(self) -> str:
        output = self.handle_words(["["])
        self.output_stream.write(output)
        output = ""
        self.compile_expression()
        output += self.handle_words(["]"])
        self.vm_writer.write_arithmetic("ADD")
        self.vm_writer.write_pop(VMWriter.POINTER, 1)
        self.vm_writer.write_push(VMWriter.THAT, 0)
        return output

    def compile_keyword_const(self, first_word=False) -> tuple[str, str]:
        keyword = self.typed_lexical_element(self.input_stream.token_type())
        output = self.handle_words(["true", "false", "null", "this"], first_word)
        return output, keyword

    def compile_op(self, first_word=False):
        op_symbol = self.typed_lexical_element(self.input_stream.token_type())
        arithmetic_commend = self.switch_case_op(op_symbol)
        if not arithmetic_commend:
            arithmetic_commend = self.switch_math_function(op_symbol)

        output = self.handle_words(["+", "-", "*", "/", "&", "|", "<", ">", "="], first_word)

        self.count_pushed = self.count_pushed - 1

        return output, arithmetic_commend

    def compile_unary_op(self, first_word=False) -> tuple[str, str]:
        op_symbol = self.typed_lexical_element(self.input_stream.token_type())
        arithmetic_commend = self.switch_case_unaryop(op_symbol)
        output = self.handle_words(["-", "~"], first_word)
        return output, arithmetic_commend

    def compile_statement(self, first_word=False) -> None:
        self.handle_either([], [CompilationEngine.SPECIAL_GRAMMAR_LET,
                                         CompilationEngine.SPECIAL_GRAMMAR_IF,
                                         CompilationEngine.SPECIAL_GRAMMAR_WHILE,
                                         CompilationEngine.SPECIAL_GRAMMAR_DO,
                                         CompilationEngine.SPECIAL_GRAMMAR_RETURN], first_word)

    def compile_type(self, first_word=False) -> str:
        words = ["int", "char", "boolean"]
        for word in words:
            type = self.typed_lexical_element(self.input_stream.token_type())
            if word == type:
                self.cur_type = word

        if self.input_stream.token_type() == "IDENTIFIER":
            self.is_class_name = True
            self.cur_type = self.typed_lexical_element(self.input_stream.token_type())

        else:
            self.is_class_name = False

        output = self.handle_either(["int", "char", "boolean"], [CompilationEngine.SPECIAL_GRAMMAR_IDENTIFIER],
                                    first_word)

        self.is_class_name = False
        return output

    def compile_identifier(self, first_word=False, class_name=False, subroutine_name=False, kind="",
                           type="", given_name="") -> str:

        # return self.old_identifier_print(first_word=first_word, given_name=given_name)

        if not self.input_stream.token_type() == "IDENTIFIER" and not given_name:
            if first_word:
                raise TypeError(CompilationEngine.ERROR_MSG)
            raise ValueError(CompilationEngine.BAD_ERROR_MSG)

        if class_name and not given_name:
            self.class_name = class_name

        if subroutine_name and not given_name:
            self.subroutine_name = subroutine_name
            
        word = "identifier"
        output = word
        output = self.write_to_file(output, True)
        self.count_tabs += 1

        tabs = "  " * self.count_tabs

        name = given_name
        if not given_name:
            name = self.typed_lexical_element(self.input_stream.token_type())

        output += tabs + f"<name> {name} </name>\n"

        if not class_name and not subroutine_name:
            if kind and type:
                self.symbol_table.define(name, type, kind)

            else:
                kind = self.symbol_table.kind_of(name)

            category = kind
            output += tabs + f"<category> {category} </category>\n"
            index = self.symbol_table.index_of(name)
            output += tabs + f"<index> {index} </index>\n"
            output += tabs + f"<isDefined> {bool(kind and type)} </isDefined>\n"

        elif class_name:
            category = "class"
            output += tabs + f"<category> {category} </category>\n"

        else:
            category = "subroutine"
            output += tabs + f"<category> {category} </category>\n"

        self.count_tabs -= 1
        output += self.write_to_file(word, False)

        if not given_name:
            if self.input_stream.has_more_tokens():
                self.input_stream.advance()

        return output

    def compile_integer_const(self, first_word=False) -> tuple[str, int]:
        if not (self.input_stream.token_type() == "INTEGER_CONST"):
            if first_word:
                raise TypeError(CompilationEngine.ERROR_MSG)
            raise ValueError(CompilationEngine.BAD_ERROR_MSG)

        tabs = "  " * self.count_tabs
        name = self.typed_lexical_element(self.input_stream.token_type())

        output = tabs + f"<integerConstant> " \
                        f"{name} " \
                        f"</integerConstant>\n"

        if self.input_stream.has_more_tokens():
            self.input_stream.advance()

        return output, int(name)

    def compile_string_const(self, first_word=False) -> str:
        if not (self.input_stream.token_type() == "STRING_CONST"):
            if first_word:
                raise TypeError(CompilationEngine.ERROR_MSG)
            raise ValueError(CompilationEngine.BAD_ERROR_MSG)


        tabs = "  " * self.count_tabs
        remove = '"'
        name = self.typed_lexical_element(self.input_stream.token_type()).strip(remove)
        output = tabs + f"<stringConstant> " \
                        f"{name} " \
                        f"</stringConstant>\n"

        self.write_string_vm(name)

        if self.input_stream.has_more_tokens():
            self.input_stream.advance()

        return output

    def compile_subroutine_body(self, first_word=False) -> str:
        word = "subroutineBody"
        output = word
        output = self.write_to_file(output, True)
        self.count_tabs += 1

        output += self.handle_words(["{"], first_word)
        self.output_stream.write(output)
        output = ""
        tabs = self.count_tabs
        while True:
            try:
                self.compile_var_dec()
            except TypeError:
                break
        self.count_tabs = tabs

        vars_count = self.symbol_table.var_count(self.symbol_table.VAR)
        self.vm_writer.write_function(self.cur_subroutine_name, vars_count)

        if self.function_type == "constructor":
            self.write_constructor_start()

        elif self.function_type == "method":
            self.write_method_start()

        self.compile_statements()
        output += self.handle_words(["}"])

        self.count_tabs -= 1
        output += self.write_to_file(word, False)
        return output

    def handle_either(self, words, special_grammar, first_word=False):
        tabs = self.count_tabs
        try:
            return self.handle_words(words, first_word)

        except:
            self.count_tabs = tabs
            return self.handle_special_grammar(special_grammar, first_word)

    def handle_words(self, words, first_word=False) -> str:
        for word in words:
            valid, output = self.handle_word(word)
            if valid:
                return output

        if first_word:
            raise TypeError(CompilationEngine.ERROR_MSG)
        raise ValueError(CompilationEngine.BAD_ERROR_MSG)

    def handle_special_grammar(self, special_grammar, first_word=False) -> str:
        if not special_grammar:
            if first_word:
                raise TypeError(CompilationEngine.ERROR_MSG)
            raise ValueError(CompilationEngine.BAD_ERROR_MSG)

        try:
            func, is_args_needed = self.switch_case_grammar(special_grammar[-1])
            if is_args_needed:
                return func(first_word)
            else:
                func()

        except:
            self.count_tabs -= 1
            special_grammar.pop()
            return self.handle_special_grammar(special_grammar, first_word)

    def switch_case_grammar(self, grammar):
        if grammar == CompilationEngine.SPECIAL_GRAMMAR_TYPE:
            return self.compile_type, True

        elif grammar == CompilationEngine.SPECIAL_GRAMMAR_IDENTIFIER:
            return self.compile_identifier, True

        elif grammar == CompilationEngine.SPECIAL_GRAMMAR_LET:
            return self.compile_let, False

        elif grammar == CompilationEngine.SPECIAL_GRAMMAR_IF:
            return self.compile_if, False

        elif grammar == CompilationEngine.SPECIAL_GRAMMAR_WHILE:
            return self.compile_while, False

        elif grammar == CompilationEngine.SPECIAL_GRAMMAR_DO:
            return self.compile_do, False

        elif grammar == CompilationEngine.SPECIAL_GRAMMAR_RETURN:
            return self.compile_return, False

    def handle_word(self, word: str) -> tuple[bool, str]:
        token_type = JackTokenizer.lexical_element(word)
        if not (self.input_stream.token_type() == token_type and
                self.typed_lexical_element(token_type) == word):
            return False, ""

        if self.input_stream.has_more_tokens():
            self.input_stream.advance()

        tabs = "  " * self.count_tabs

        word = self.parse_xml_special(word)
        output = tabs + f"<{token_type.lower()}> {word} </{token_type.lower()}>\n"
        return True, output

    def write_arguments_vm(self, name: str):

        if self.function_type == "constructor":
            segment = self.symbol_table.kind_of(name)
            index = self.symbol_table.index_of(name)
            self.vm_writer.write_push(self.kind_to_segment(segment), index)
            self.vm_writer.write_pop(VMWriter.THIS, index)

        elif self.function_type == "function":
            x = 1

        elif self.function_type == "method":
            x = 1

    def write_constructor_start(self):
        field_count = self.symbol_table.var_count(SymbolTable.FIELD)

        self.vm_writer.write_push(VMWriter.CONST, field_count)
        self.vm_writer.write_call("Memory.alloc", 1)
        self.vm_writer.write_pop(VMWriter.POINTER, 0)

    def write_method_start(self):
        self.vm_writer.write_push(VMWriter.ARG, 0)
        self.vm_writer.write_pop(VMWriter.POINTER, 0)

    def write_string_vm(self, word: str):
        length = len(word)
        self.vm_writer.write_push(VMWriter.CONST, length)
        self.vm_writer.write_call("String.new", 1)
        for i in range(length):
            c = ord(word[i])
            self.vm_writer.write_push(VMWriter.CONST, c)
            self.vm_writer.write_call("String.appendChar", 2)

    def parse_xml_special(self, word):
        if word in CompilationEngine.XML_SPECIAL:
            return CompilationEngine.XML_SPECIAL[word]

        return word

    def typed_lexical_element(self, token_type: str):
        if token_type == "KEYWORD":
            return self.input_stream.keyword().lower()

        elif token_type == "IDENTIFIER":
            return self.input_stream.identifier()

        elif token_type == "SYMBOL":
            return self.input_stream.symbol()

        elif token_type == "INTEGER_CONST":
            return self.input_stream.int_val()

        elif token_type == "STRING_CONST":
            return self.input_stream.string_val()

    def write_to_file(self, word: str, is_open: bool) -> str:
        tabs = "  " * self.count_tabs
        if is_open:
            output = tabs + f"<{word}>\n"

        else:
            output = tabs + f"</{word}>\n"

        return output

    def old_identifier_print(self, first_word=False, given_name="") -> str:
        if not self.input_stream.token_type() == "IDENTIFIER" and not given_name:
            if first_word:
                raise TypeError(CompilationEngine.ERROR_MSG)
            raise ValueError(CompilationEngine.BAD_ERROR_MSG)

        name = given_name
        type = "IDENTIFIER".lower()
        if not given_name:
            name = self.typed_lexical_element(self.input_stream.token_type())
            type = self.input_stream.token_type().lower()

        tabs = "  " * self.count_tabs
        output = tabs + f"<{type}> " \
                        f"{name} " \
                        f"</{type}>\n"

        if not given_name:
            if self.input_stream.has_more_tokens():
                self.input_stream.advance()

        return output

    def switch_math_function(self, op_symbol) -> tuple[str, int]:
        for math_function_dict in VMWriter.MATH:
            if op_symbol in math_function_dict.keys():
                return math_function_dict[op_symbol]

    def switch_case_op(self, op_symbol) -> str:
        for arithmetic_dict in VMWriter.TWO_VARS:
            if op_symbol in arithmetic_dict.keys():
                return arithmetic_dict[op_symbol]

    def switch_case_unaryop(self, op_symbol) -> str:
        for arithmetic_dict in VMWriter.ONE_VARS:
            if op_symbol in arithmetic_dict.keys():
                return arithmetic_dict[op_symbol]

    def switch_case_keyword(self, keyword: str):
        # "true", "false", "null", "this"

        if keyword == "true":
            self.vm_writer.write_push(VMWriter.CONST, 0)
            self.vm_writer.write_arithmetic("NOT")

        elif keyword == "false" or keyword == "null":
            self.vm_writer.write_push(VMWriter.CONST, 0)

    def kind_to_segment(self, kind) -> str:
        if kind == SymbolTable.VAR:
            return VMWriter.LOCAL

        if kind == SymbolTable.ARGUMENT:
            return VMWriter.ARG

        if kind == SymbolTable.FIELD:
            return VMWriter.THIS

        if kind == SymbolTable.STATIC:
            return VMWriter.STATIC

        return ""