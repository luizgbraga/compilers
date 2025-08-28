from typing import Dict, List, Optional

from input_stream import InputStream
from tokens import (
    AND,
    CHARACTER,
    EOF,
    EQUAL_EQUAL,
    EQUALS,
    GREATER_OR_EQUAL,
    GREATER_THAN,
    ID,
    KEYWORDS,
    LESS_OR_EQUAL,
    LESS_THAN,
    MINUS_MINUS,
    NOT,
    NOT_EQUAL,
    NUMERAL,
    OR,
    PLUS_PLUS,
    STRING,
    SYMBOLS,
    UNKNOWN,
)


class SymbolTable:
    def __init__(self):
        self.constants: List[str] = []
        self.identifiers: Dict[str, int] = {}
        self.identifier_count: int = 0

    def add_constant(self, value: str) -> int:
        self.constants.append(value)
        return len(self.constants) - 1

    def get_identifier(self, name: str) -> int:
        if name not in self.identifiers:
            self.identifiers[name] = self.identifier_count
            self.identifier_count += 1
        return self.identifiers[name]


class LexicalAnalyzer:
    def __init__(self, file) -> None:
        self.stream: InputStream = InputStream(file)
        self.lexical_error: bool = False
        self.symbol_table: SymbolTable = SymbolTable()
        self.secondary_token: Optional[int] = None

    def get_keyword_or_id(self, name: str) -> int:
        return KEYWORDS.get(name, ID)

    def next_token(self) -> int:
        self._skip_whitespace()

        if self.stream.eof():
            return EOF

        ch: str = self.stream.peek()

        if ch.isalpha():
            word: str = self._consume_identifier()
            token: int = self.get_keyword_or_id(word)
            if token == ID:
                self.secondary_token = self.symbol_table.get_identifier(word)

        elif ch.isdigit():
            number: str = self._consume_number()
            token = NUMERAL
            self.secondary_token = self.symbol_table.add_constant(number)

        elif ch == '"':
            string_val: str = self._consume_string()
            token = STRING
            self.secondary_token = self.symbol_table.add_constant(string_val)

        else:
            token = self._match_symbol_or_operator()

        return token

    def _skip_whitespace(self) -> None:
        while self.stream.peek().isspace():
            self.stream.advance()

    def _consume_identifier(self) -> str:
        chars: List[str] = []
        while self.stream.peek().isalnum() or self.stream.peek() == "_":
            chars.append(self.stream.peek())
            self.stream.advance()
        return "".join(chars)

    def _consume_number(self) -> str:
        digits: List[str] = []
        while self.stream.peek().isdigit():
            digits.append(self.stream.peek())
            self.stream.advance()
        return "".join(digits)

    def _consume_string(self) -> str:
        chars: List[str] = [self.stream.peek()]
        self.stream.advance()
        while not self.stream.eof() and self.stream.peek() != '"':
            chars.append(self.stream.peek())
            self.stream.advance()
        chars.append(self.stream.peek())
        self.stream.advance()
        return "".join(chars)

    def _match_symbol_or_operator(self) -> int:
        ch: str = self.stream.peek()
        self.stream.advance()

        if ch == "+" and self.stream.peek() == "+":
            token = PLUS_PLUS
            self.stream.advance()
        elif ch == "-" and self.stream.peek() == "-":
            token = MINUS_MINUS
            self.stream.advance()
        elif ch == "=" and self.stream.peek() == "=":
            token = EQUAL_EQUAL
            self.stream.advance()
        elif ch == "=":
            token = EQUALS
        elif ch == "&" and self.stream.peek() == "&":
            token = AND
            self.stream.advance()
        elif ch == "|" and self.stream.peek() == "|":
            token = OR
            self.stream.advance()
        elif ch == "<" and self.stream.peek() == "=":
            token = LESS_OR_EQUAL
            self.stream.advance()
        elif ch == "<":
            token = LESS_THAN
        elif ch == ">" and self.stream.peek() == "=":
            token = GREATER_OR_EQUAL
            self.stream.advance()
        elif ch == ">":
            token = GREATER_THAN
        elif ch == "!" and self.stream.peek() == "=":
            token = NOT_EQUAL
            self.stream.advance()
        elif ch == "!":
            token = NOT
        elif ch == "'":
            char_val: str = self.stream.advance()
            self.secondary_token = self.symbol_table.add_constant(char_val)
            self.stream.advance()
            token = CHARACTER
        else:
            token = SYMBOLS.get(ch, UNKNOWN)

        return token

    def report_error(self, token: int) -> None:
        if token == UNKNOWN:
            line, col = self.stream.position()
            self.lexical_error = True
            print(f"Character not expected at line {line}, column {col}")

    def run(self) -> None:
        token: int = self.next_token()
        while token != EOF:
            if token == UNKNOWN:
                self.report_error(token)
            token = self.next_token()
        if not self.lexical_error:
            print("Compiled successfully.")
