"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""

import typing
from JackTokenizer import JackTokenizer


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
    BAD_ERROR_MSG = "DEAD ERRORRR"
    ERROR_MSG = "its my error :) invalid syntax :) go fix it :("

    def __init__(self, input_stream: JackTokenizer, output_stream: typing.TextIO) -> None:
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
        self.output_stream = output_stream
        self.count_tabs = 0

        self.compile_class()

    def compile_class(self) -> None:
        """Compiles a complete class."""
        # Your code goes here!
        word = "class"
        output = word
        output = self.write_to_file(output, True)
        self.count_tabs += 1
        output += self.handle_words(["class"], True)
        output += self.compile_identifier()
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
        output += self.handle_words(["static", "field"], True)
        output += self.compile_type()
        output += self.compile_identifier()
        tabs = self.count_tabs
        while True:
            try:
                output += self.handle_words([","], True)
            except TypeError:
                break

            output += self.compile_identifier()

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

        output += self.handle_words(["constructor", "function", "method"], True)
        output += self.handle_either(["void"], [CompilationEngine.SPECIAL_GRAMMAR_TYPE])

        output += self.compile_identifier()
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
            output += self.compile_identifier()
            tabs = self.count_tabs
            while True:
                try:
                    output += self.handle_words([","], True)
                except TypeError:
                    break
                output += self.compile_type()
                output += self.compile_identifier()

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
        output += self.compile_identifier()

        tabs = self.count_tabs
        while True:
            try:
                tabs = self.count_tabs
                output += self.handle_words([","], True)
            except TypeError:
                break
            output += self.compile_identifier()

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
        output += self.compile_identifier()

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
        self.count_tabs = tabs

        output += self.handle_words(["="])
        self.output_stream.write(output)
        output = ""
        self.compile_expression()
        output += self.handle_words([";"])

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
        self.compile_expression()
        output += self.handle_words([")"])
        output += self.handle_words(["{"])
        self.output_stream.write(output)
        output = ""
        self.compile_statements()
        output += self.handle_words(["}"])

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
        output += self.handle_words([")"])
        output += self.handle_words(["{"])
        self.output_stream.write(output)
        output = ""
        self.compile_statements()
        output += self.handle_words(["}"])

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
                output += self.compile_op(True)
            except TypeError:
                break
            self.output_stream.write(output)
            output = ""
            self.compile_term()
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
            output += self.compile_identifier()
            try:
                self.output_stream.write(output)
                output = ""
                output += self.compile_array()
            except:
                try:
                    self.output_stream.write(output)
                    output = ""
                    output += self.compile_subroutine_call(True)
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
                            output += self.compile_integer_const(True)
                        except TypeError:
                            try:
                                output += self.compile_string_const(True)

                            except TypeError:
                                try:
                                    output += self.compile_keyword_const(True)

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

    def compile_subroutine_call(self, is_identifier_compiled) -> str:
        tabs = self.count_tabs

        output = ""
        if not is_identifier_compiled:
            output += self.compile_identifier()


        try:
            output = self.compile_method(output)

        except:
            output = self.compile_function(output)

        self.count_tabs = tabs

        return output

    def compile_method(self, base_output) -> str:
        output = base_output
        output += self.handle_words(["."])
        output += self.compile_identifier()
        output += self.handle_words(["("])
        self.output_stream.write(output)
        output = ""
        self.compile_expression_list()
        output += self.handle_words([")"])
        return output

    def compile_function(self, base_output) -> str:
        output = base_output
        output += self.handle_words(["("])
        self.output_stream.write(output)
        output = ""
        self.compile_expression_list()
        output += self.handle_words([")"])
        return output

    def compile_condition(self) -> str:
        output = self.compile_unary_op()
        self.output_stream.write(output)
        output = ""
        self.compile_term()
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
        return output

    def compile_keyword_const(self, first_word=False) -> str:
        output = self.handle_words(["true", "false", "null", "this"], first_word)
        return output

    def compile_op(self, first_word=False) -> str:
        output = self.handle_words(["+", "-", "*", "/", "&", "|", "<", ">", "="], first_word)
        return output

    def compile_unary_op(self, first_word=False) -> str:
        output = self.handle_words(["-", "~", "^", "#"], first_word)
        return output

    def compile_statement(self, first_word=False) -> None:
        self.handle_either([], [CompilationEngine.SPECIAL_GRAMMAR_LET,
                                         CompilationEngine.SPECIAL_GRAMMAR_IF,
                                         CompilationEngine.SPECIAL_GRAMMAR_WHILE,
                                         CompilationEngine.SPECIAL_GRAMMAR_DO,
                                         CompilationEngine.SPECIAL_GRAMMAR_RETURN], first_word)

    def compile_type(self, first_word=False) -> str:
        output = self.handle_either(["int", "char", "boolean"], [CompilationEngine.SPECIAL_GRAMMAR_IDENTIFIER], first_word)
        return output

    def compile_identifier(self, first_word=False) -> str:
        if not (self.input_stream.token_type() == "IDENTIFIER"):
            if first_word:
                raise TypeError(CompilationEngine.ERROR_MSG)
            raise ValueError(CompilationEngine.BAD_ERROR_MSG)

        tabs = "  " * self.count_tabs
        output = tabs + f"<{self.input_stream.token_type().lower()}> " \
                        f"{self.typed_lexical_element(self.input_stream.token_type())} " \
                        f"</{self.input_stream.token_type().lower()}>\n"

        if self.input_stream.has_more_tokens():
            self.input_stream.advance()

        return output

    def compile_integer_const(self, first_word=False) -> str:
        if not (self.input_stream.token_type() == "INTEGER_CONST"):
            if first_word:
                raise TypeError(CompilationEngine.ERROR_MSG)
            raise ValueError(CompilationEngine.BAD_ERROR_MSG)

        tabs = "  " * self.count_tabs
        output = tabs + f"<integerConstant> " \
                        f"{self.typed_lexical_element(self.input_stream.token_type())} " \
                        f"</integerConstant>\n"

        if self.input_stream.has_more_tokens():
            self.input_stream.advance()

        return output

    def compile_string_const(self, first_word=False) -> str:
        if not (self.input_stream.token_type() == "STRING_CONST"):
            if first_word:
                raise TypeError(CompilationEngine.ERROR_MSG)
            raise ValueError(CompilationEngine.BAD_ERROR_MSG)

        tabs = "  " * self.count_tabs
        remove = '"'
        output = tabs + f"<stringConstant> " \
                        f"{self.typed_lexical_element(self.input_stream.token_type()).strip(remove)} " \
                        f"</stringConstant>\n"

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

        self.compile_statements()
        output += self.handle_words(["}"])

        self.count_tabs -= 1
        output += self.write_to_file(word, False)
        return output

    def handle_either(self, words, special_grammar, first_word=False):
        try:
            tabs = self.count_tabs
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

