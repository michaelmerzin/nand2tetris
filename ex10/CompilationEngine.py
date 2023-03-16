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

    SPECIAL_GRAMMAR_TYPE = "50000"
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
        self.write_to_file(word, True)
        self.count_tabs += 1
        self.handle_words(["class"])
        self.compile_identifier()
        self.handle_words(["{"])

        # TODO *
        self.compile_class_var_dec()
        self.compile_subroutine()

        self.handle_words(["}"])
        self.count_tabs -= 1
        self.write_to_file(word, False)

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        # Your code goes here!
        word = "classVarDec"
        self.write_to_file(word, True)
        self.count_tabs += 1
        self.handle_words(["static", "field"])
        self.compile_type()

        # TODO *
        self.handle_words([","])
        self.compile_identifier()

        self.handle_words([";"])
        self.count_tabs -= 1
        self.write_to_file(word, False)

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        # Your code goes here!
        word = "subroutineDec"
        self.write_to_file(word, True)
        self.count_tabs += 1

        self.handle_words(["constructor", "function", "method"])
        self.handle_either(["void"], [CompilationEngine.SPECIAL_GRAMMAR_TYPE])

        self.compile_identifier()
        self.handle_words(["("])
        self.compile_parameter_list()
        self.handle_words([")"])

        self.compile_subroutine_body()

        self.count_tabs -= 1
        self.write_to_file(word, False)

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        # Your code goes here!
        word = "parameterList"
        self.write_to_file(word, True)
        self.count_tabs += 1

        self.count_tabs -= 1
        self.write_to_file(word, False)

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        # Your code goes here!
        word = "varDec"
        self.write_to_file(word, True)
        self.count_tabs += 1
        self.handle_words(["var"])
        self.compile_type()
        self.compile_identifier()

        # TODO *
        self.handle_words([","])
        self.compile_identifier()

        self.handle_words([";"])
        self.count_tabs -= 1
        self.write_to_file(word, False)

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        # Your code goes here!
        #TODO is write to file needed

    def compile_do(self) -> None:
        """Compiles a do statement."""
        # Your code goes here!
        word = "doStatement"
        self.write_to_file(word, True)
        self.count_tabs += 1

        self.count_tabs -= 1
        self.write_to_file(word, False)

    def compile_let(self) -> None:
        """Compiles a let statement."""
        # Your code goes here!
        word = "letStatement"
        self.write_to_file(word, True)
        self.count_tabs += 1

        self.count_tabs -= 1
        self.write_to_file(word, False)

    def compile_while(self) -> None:
        """Compiles a while statement."""
        # Your code goes here!
        word = "whileStatement"
        self.write_to_file(word, True)
        self.count_tabs += 1

        self.count_tabs -= 1
        self.write_to_file(word, False)

    def compile_return(self) -> None:
        """Compiles a return statement."""
        # Your code goes here!
        word = "returnStatement"
        self.write_to_file(word, True)
        self.count_tabs += 1

        self.count_tabs -= 1
        self.write_to_file(word, False)

    def compile_if(self) -> None:
        """Compiles an if statement, possibly with a trailing else clause."""
        # Your code goes here!
        word = "ifStatement"
        self.write_to_file(word, True)
        self.count_tabs += 1

        self.count_tabs -= 1
        self.write_to_file(word, False)

    def compile_expression(self) -> None:
        """Compiles an expression."""
        # Your code goes here!
        word = "expression"
        self.write_to_file(word, True)
        self.count_tabs += 1

        self.count_tabs -= 1
        self.write_to_file(word, False)

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
        self.write_to_file(word, True)
        self.count_tabs += 1

        self.count_tabs -= 1
        self.write_to_file(word, False)

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # Your code goes here!
        word = "expressionList"
        self.write_to_file(word, True)
        self.count_tabs += 1

        self.count_tabs -= 1
        self.write_to_file(word, False)


    def compile_type(self) -> None:
        self.handle_words(["int", "char", "boolean"])
        self.compile_identifier()

    def compile_identifier(self) -> None:
        if not (self.input_stream.token_type() == "IDENTIFIER"):
            raise Exception(CompilationEngine.ERROR_MSG)

        tabs = "\t" * self.count_tabs
        output = tabs + f"<{self.input_stream.token_type().lower()}> " \
                        f"{self.typed_lexical_element(self.input_stream.token_type())} " \
                        f"</{self.input_stream.token_type().lower()}>\n"
        self.output_stream.write(output)

        if self.input_stream.has_more_tokens():
            self.input_stream.advance()

    def compile_subroutine_body(self) -> None:
        self.handle_words(["{"])

        # TODO *
        self.compile_var_dec()

        self.compile_statements()
        self.handle_words(["}"])

    def handle_either(self, words, special_grammar):
        try:
            self.handle_words(words)

        except:
            self.handle_special_grammar(special_grammar)

    def handle_words(self, words) -> None:
        for word in words:
            if self.handle_word(word):
                return

        # TODO
        raise Exception(CompilationEngine.ERROR_MSG)

    def handle_special_grammar(self, special_grammar):
        try:
            if not special_grammar:
                raise Exception(CompilationEngine.ERROR_MSG)

            if special_grammar[-1] == CompilationEngine.SPECIAL_GRAMMAR_TYPE:
                self.compile_type()
        except:
            special_grammar.pop()
            self.handle_special_grammar(special_grammar)

    def handle_word(self, word: str) -> bool:
        token_type = JackTokenizer.lexical_element(word)
        if not (self.input_stream.token_type() == token_type and
                self.typed_lexical_element(token_type) == word):
            return False

        if self.input_stream.has_more_tokens():
            self.input_stream.advance()

        tabs = "\t" * self.count_tabs
        output = tabs + f"<{token_type.lower()}> {word} </{token_type.lower()}>\n"
        self.output_stream.write(output)
        return True

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

    def write_to_file(self, word: str, is_open: bool) -> None:
        tabs = "\t" * self.count_tabs
        if is_open:
            output = tabs + f"<{word}>\n"

        else:
            output = tabs + f"</{word}>\n"

        self.output_stream.write(output)
