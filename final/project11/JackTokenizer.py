"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class JackTokenizer:
    """Removes all comments from the input stream and breaks it
    into Jack language tokens, as specified by the Jack grammar.
    
    # Jack Language Grammar

    A Jack file is a stream of characters. If the file represents a
    valid program, it can be tokenized into a stream of valid tokens. The
    tokens may be separated by an arbitrary number of whitespace characters, 
    and comments, which are ignored. There are three possible comment formats: 
    /* comment until closing */ , /** API comment until closing */ , and 
    // comment until the line’s end.

    - ‘xxx’: quotes are used for tokens that appear verbatim (‘terminals’).
    - xxx: regular typeface is used for names of language constructs 
           (‘non-terminals’).
    - (): parentheses are used for grouping of language constructs.
    - x | y: indicates that either x or y can appear.
    - x?: indicates that x appears 0 or 1 times.
    - x*: indicates that x appears 0 or more times.

    ## Lexical Elements

    The Jack language includes five types of terminal elements (tokens).

    - keyword: 'class' | 'constructor' | 'function' | 'method' | 'field' | 
               'static' | 'var' | 'int' | 'char' | 'boolean' | 'void' | 'true' |
               'false' | 'null' | 'this' | 'let' | 'do' | 'if' | 'else' | 
               'while' | 'return'
    - symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' | 
              '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
    - integerConstant: A decimal number in the range 0-32767.
    - StringConstant: '"' A sequence of Unicode characters not including 
                      double quote or newline '"'
    - identifier: A sequence of letters, digits, and underscore ('_') not 
                  starting with a digit. You can assume keywords cannot be
                  identifiers, so 'self' cannot be an identifier, etc'.

    ## Program Structure

    A Jack program is a collection of classes, each appearing in a separate 
    file. A compilation unit is a single class. A class is a sequence of tokens 
    structured according to the following context free syntax:
    
    - class: 'class' className '{' classVarDec* subroutineDec* '}'
    - classVarDec: ('static' | 'field') type varName (',' varName)* ';'
    - type: 'int' | 'char' | 'boolean' | className
    - subroutineDec: ('constructor' | 'function' | 'method') ('void' | type) 
    - subroutineName '(' parameterList ')' subroutineBody
    - parameterList: ((type varName) (',' type varName)*)?
    - subroutineBody: '{' varDec* statements '}'
    - varDec: 'var' type varName (',' varName)* ';'
    - className: identifier
    - subroutineName: identifier
    - varName: identifier

    ## Statements

    - statements: statement*
    - statement: letStatement | ifStatement | whileStatement | doStatement | 
                 returnStatement
    - letStatement: 'let' varName ('[' expression ']')? '=' expression ';'
    - ifStatement: 'if' '(' expression ')' '{' statements '}' ('else' '{' 
                   statements '}')?
    - whileStatement: 'while' '(' 'expression' ')' '{' statements '}'
    - doStatement: 'do' subroutineCall ';'
    - returnStatement: 'return' expression? ';'

    ## Expressions
    
    - expression: term (op term)*
    - term: integerConstant | stringConstant | keywordConstant | varName | 
            varName '['expression']' | subroutineCall | '(' expression ')' | 
            unaryOp term
    - subroutineCall: subroutineName '(' expressionList ')' | (className | 
                      varName) '.' subroutineName '(' expressionList ')'
    - expressionList: (expression (',' expression)* )?
    - op: '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
    - unaryOp: '-' | '~' | '^' | '#'
    - keywordConstant: 'true' | 'false' | 'null' | 'this'
    
    Note that ^, # correspond to shiftleft and shiftright, respectively.
    """

    MULTI_LINE_COMMENTS_SYNTAX = {"/**": "*/", "/*": "*/", "//": "\n"}
    LINE_COMMENT_SYNTAX = "//"

    KEYWORDS = ["class", "constructor", "function", "method", "field", "static", "var", "int", "char",
                "boolean", "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"]

    SYMBOLS = ["{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~", "^", "#"]

    KEYWORD = lambda word: word in JackTokenizer.KEYWORDS

    SYMBOL = lambda word: word in JackTokenizer.SYMBOLS

    INTEGER_CONST = lambda x: x.isdigit() and 0 <= int(x) <= 32767

    STRING_CONST = lambda word: word and word[0] == '"' and ("\n" not in word) and word[len(word) - 1] == '"'

    def __init__(self, input_stream: typing.TextIO) -> None:
        """Opens the input stream and gets ready to tokenize it.

        Args:
            input_stream (typing.TextIO): input stream.
        """
        # Your code goes here!
        # A good place to start is to read all the lines of the input:
        # input_lines = input_stream.read().splitlines()
        lines = JackTokenizer.get_valid_lines(input_stream)
        self.index = 0
        self.tokens = []
        for line in lines:

            const = ""
            if '"' in line:
                const = line.split('"', 1)[1]
                if const:
                    const = const.split('"')[0]
                    const = f'"{const}"'
                    line = line.replace(const, ' " ')

            words = line.split(" ")
            for word in words:
                if word == '"':
                    self.tokens_from_word(const)
                else:
                    self.tokens_from_word(word)

    @staticmethod
    def get_valid_lines(input_stream: typing.TextIO) -> [str]:
        lines = []
        comment_open = False
        current_comment = ""
        for line in input_stream:
            no_comment_line_arr, comment_open, current_comment = \
                JackTokenizer.comment_handler(line, comment_open, current_comment)
            for no_comment_line in no_comment_line_arr:
                no_comment_line = no_comment_line.strip("\n")
                no_comment_line = no_comment_line.replace("\t", " ")
                if no_comment_line.strip(" "):
                    lines.append(no_comment_line)

        return lines

    @staticmethod
    def comment_handler(line: str, comment_open: bool, current_comment) -> tuple[list[str], bool, str]:
        no_comment_line_arr = []
        if not comment_open:
            text = ""
            if '"' in line:
                text = line.split('"', 1)[1]
                if text:
                    text = text.split('"')[0]
                    text = f'"{text}"'

            comment_exists = True
            while comment_exists:
                comment_exists = False
                for comment in JackTokenizer.MULTI_LINE_COMMENTS_SYNTAX:
                    if (comment in text) and (comment not in line.replace(text, '')):
                        break

                    if comment in line:
                        comment_exists = True
                        current_comment = comment
                        line, no_comment, comment_open, current_comment \
                            = JackTokenizer.remove_comments(line, current_comment)

                        no_comment_line_arr.append(no_comment)

        if comment_open:
            line, no_comment, comment_open, current_comment = JackTokenizer.remove_comments(line, current_comment)

        elif not no_comment_line_arr:
            no_comment_line_arr.append(line)

        return no_comment_line_arr, comment_open, current_comment

    @staticmethod
    def remove_comments(line: str, comment: str) -> tuple[str, str, bool, str]:
        no_comment = ""
        new_line = ""
        comment_open = True

        if comment in line:
            no_comment = line.split(comment)[0]
            split_line = line.split(JackTokenizer.MULTI_LINE_COMMENTS_SYNTAX[comment])
            if len(split_line) > 1:
                new_line = split_line[1]

        if JackTokenizer.MULTI_LINE_COMMENTS_SYNTAX[comment] in line:
            comment_open = False
            comment = ""

        return new_line, no_comment, comment_open, comment

    @staticmethod
    def IDENTIFIER(word: str) -> bool:
        if not word:
            return False

        for symbol in JackTokenizer.SYMBOLS:
            if symbol in word:
                return False

        if word in JackTokenizer.KEYWORDS:
            return False

        if JackTokenizer.INTEGER_CONST(word[0]):
            return False

        if word[0] == '"':
            return False

        return True

    @staticmethod
    def lexical_element(word: str) -> str:
        if not word:
            return ""

        if JackTokenizer.KEYWORD(word):
            return "KEYWORD"

        elif JackTokenizer.IDENTIFIER(word):
            return "IDENTIFIER"

        elif JackTokenizer.SYMBOL(word):
            return "SYMBOL"

        elif JackTokenizer.STRING_CONST(word):
            return "STRING_CONST"

        elif JackTokenizer.INTEGER_CONST(word):
            return "INTEGER_CONST"

        return ""

    def tokens_from_word(self, word: str) -> None:
        lexical_element = JackTokenizer.lexical_element(word)
        if lexical_element:
            self.tokens.append((word, lexical_element))
            return

        token_type = ""
        current_token = ""
        for i, c in enumerate(word):
            current_token += c

            if JackTokenizer.KEYWORD(current_token):
                if i + 1 == len(word):
                    next_char = ""
                else:
                    next_char = word[i + 1]
                current_token, token_type = self.keyword_token_handler(current_token, token_type, next_char)

            elif JackTokenizer.STRING_CONST(current_token):
                current_token, token_type = self.string_token_handler(current_token, token_type)

            elif JackTokenizer.INTEGER_CONST(current_token):
                current_token, token_type = self.integer_token_handler(current_token, token_type)

            elif JackTokenizer.SYMBOL(current_token[-1]):
                if i + 1 == len(word):
                    next_char = ""
                else:
                    next_char = word[i + 1]

                current_token, token_type = self.symbol_token_handler(current_token, token_type, next_char)

            elif JackTokenizer.IDENTIFIER(current_token):
                current_token, token_type = self.identifier_token_handler(current_token, token_type)

        lexical_element = JackTokenizer.lexical_element(current_token)
        if lexical_element:
            self.tokens.append((current_token, lexical_element))

    def keyword_token_handler(self, token, token_type, next_char):
        if token_type != "KEYWORD" and not next_char:
            self.tokens.append((token, "KEYWORD"))
            token = ""

        if next_char and JackTokenizer.IDENTIFIER(token + next_char):
            token_type = "IDENTIFIER"
        else:
            token_type = "KEYWORD"
        return token, token_type

    def symbol_token_handler(self, token, token_type, next_char):
        if token_type != "SYMBOL":
            if len(token) == 1:
                self.tokens.append((token, "SYMBOL"))
                token = ""

            else:
                self.tokens.append((token[:-1], token_type))
                self.tokens.append((token[-1], "SYMBOL"))
                token = ""

        elif len(token) == 2 and JackTokenizer.SYMBOL(token[-2]):
            self.tokens.append((token[-2], token_type))
            token = token[-1]

        elif len(token) == 1 and JackTokenizer.SYMBOL(token):
            self.tokens.append((token, token_type))
            token = ""

        # token_type = "SYMBOL"

        token_type = JackTokenizer.lexical_element(next_char)

        return token, token_type

    def identifier_token_handler(self, token, token_type):
        if token_type != "IDENTIFIER" and token_type:
            self.tokens.append((token, token_type))
            token = token[-1]
        token_type = "IDENTIFIER"

        return token, token_type

    def string_token_handler(self, token, token_type):
        if token_type != "STRING_CONST" and token_type:
            self.tokens.append((token, token_type))
            token = token[-1]
        token_type = "STRING_CONST"
        return token, token_type

    def integer_token_handler(self, token, token_type):
        if token_type != "INTEGER_CONST" and token_type:
            self.tokens.append((token, token_type))
            token = token[-1]
        token_type = "INTEGER_CONST"
        return token, token_type

    def has_more_tokens(self) -> bool:
        """Do we have more tokens in the input?

        Returns:
            bool: True if there are more tokens, False otherwise.
        """
        # Your code goes here!
        return self.index < len(self.tokens)

    def advance(self) -> None:
        """Gets the next token from the input and makes it the current token. 
        This method should be called if has_more_tokens() is true. 
        Initially there is no current token.
        """
        # Your code goes here!
        self.index += 1

    def token_type(self) -> str:
        """
        Returns:
            str: the type of the current token, can be
            "KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"
        """
        # Your code goes here!

        token, token_type = self.tokens[self.index]
        return token_type

    def keyword(self) -> str:
        """
        Returns:
            str: the keyword which is the current token.
            Should be called only when token_type() is "KEYWORD".
            Can return "CLASS", "METHOD", "FUNCTION", "CONSTRUCTOR", "INT", 
            "BOOLEAN", "CHAR", "VOID", "VAR", "STATIC", "FIELD", "LET", "DO", 
            "IF", "ELSE", "WHILE", "RETURN", "TRUE", "FALSE", "NULL", "THIS"
        """
        # Your code goes here!
        token = self.tokens[self.index]
        return token[0].upper()

    def symbol(self) -> str:
        """
        Returns:
            str: the character which is the current token.
            Should be called only when token_type() is "SYMBOL".
            Recall that symbol was defined in the grammar like so:
            symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' | 
              '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
        """
        # Your code goes here!
        token = self.tokens[self.index]
        return token[0]

    def identifier(self) -> str:
        """
        Returns:
            str: the identifier which is the current token.
            Should be called only when token_type() is "IDENTIFIER".
            Recall that identifiers were defined in the grammar like so:
            identifier: A sequence of letters, digits, and underscore ('_') not 
                  starting with a digit. You can assume keywords cannot be
                  identifiers, so 'self' cannot be an identifier, etc'.
        """
        # Your code goes here!
        token = self.tokens[self.index]
        return token[0]

    def int_val(self) -> int:
        """
        Returns:
            str: the integer value of the current token.
            Should be called only when token_type() is "INT_CONST".
            Recall that integerConstant was defined in the grammar like so:
            integerConstant: A decimal number in the range 0-32767.
        """
        # Your code goes here!
        token = self.tokens[self.index]
        return int(token[0])

    def string_val(self) -> str:
        """
        Returns:
            str: the string value of the current token, without the double 
            quotes. Should be called only when token_type() is "STRING_CONST".
            Recall that StringConstant was defined in the grammar like so:
            StringConstant: '"' A sequence of Unicode characters not including 
                      double quote or newline '"'
        """
        # Your code goes here!
        token = self.tokens[self.index]
        return token[0]
