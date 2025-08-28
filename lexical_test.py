import io
import unittest

from lexical import LexicalAnalyzer
from tokens import (
    CHARACTER,
    EOF,
    EQUALS,
    GREATER_THAN,
    ID,
    LEFT_PARENTHESIS,
    NUMERAL,
    PLUS,
    RIGHT_PARENTHESIS,
    SEMI_COLON,
    STRING,
    UNKNOWN,
)


class TestLexicalAnalyzer(unittest.TestCase):
    def _create_analyzer(self, code: str) -> LexicalAnalyzer:
        file_like = io.StringIO(code)
        return LexicalAnalyzer(file_like)

    def test_mixed_tokens(self):
        analyzer = self._create_analyzer("x = 123 + \"hello\" 'a';")

        self.assertEqual(analyzer.next_token(), ID)
        self.assertEqual(analyzer.next_token(), EQUALS)
        self.assertEqual(analyzer.next_token(), NUMERAL)
        self.assertEqual(analyzer.next_token(), PLUS)
        self.assertEqual(analyzer.next_token(), STRING)
        self.assertEqual(analyzer.next_token(), CHARACTER)
        self.assertEqual(analyzer.next_token(), SEMI_COLON)
        self.assertEqual(analyzer.next_token(), EOF)

    def test_numbers(self):
        analyzer = self._create_analyzer("123 456 0")

        token = analyzer.next_token()
        self.assertEqual(token, NUMERAL)
        self.assertEqual(
            analyzer.symbol_table.constants[analyzer.secondary_token], "123"
        )

        token = analyzer.next_token()
        self.assertEqual(token, NUMERAL)
        self.assertEqual(
            analyzer.symbol_table.constants[analyzer.secondary_token], "456"
        )

        token = analyzer.next_token()
        self.assertEqual(token, NUMERAL)
        self.assertEqual(analyzer.symbol_table.constants[analyzer.secondary_token], "0")

    def test_strings(self):
        analyzer = self._create_analyzer('"hello" "world" "test string"')

        token = analyzer.next_token()
        self.assertEqual(token, STRING)
        self.assertEqual(
            analyzer.symbol_table.constants[analyzer.secondary_token], '"hello"'
        )

        token = analyzer.next_token()
        self.assertEqual(token, STRING)
        self.assertEqual(
            analyzer.symbol_table.constants[analyzer.secondary_token], '"world"'
        )

        token = analyzer.next_token()
        self.assertEqual(token, STRING)
        self.assertEqual(
            analyzer.symbol_table.constants[analyzer.secondary_token], '"test string"'
        )

    def test_characters(self):
        analyzer = self._create_analyzer("'a' 'b' '1'")

        token = analyzer.next_token()
        self.assertEqual(token, CHARACTER)
        self.assertEqual(analyzer.symbol_table.constants[analyzer.secondary_token], "a")

        token = analyzer.next_token()
        self.assertEqual(token, CHARACTER)
        self.assertEqual(analyzer.symbol_table.constants[analyzer.secondary_token], "b")

        token = analyzer.next_token()
        self.assertEqual(token, CHARACTER)
        self.assertEqual(analyzer.symbol_table.constants[analyzer.secondary_token], "1")

    def test_symbol_table_reuse(self):
        analyzer = self._create_analyzer("var1 var2 var1")

        analyzer.next_token()
        first_index = analyzer.secondary_token

        analyzer.next_token()
        second_index = analyzer.secondary_token

        analyzer.next_token()
        third_index = analyzer.secondary_token

        self.assertEqual(first_index, third_index)
        self.assertNotEqual(first_index, second_index)

    def test_unknown_character(self):
        analyzer = self._create_analyzer("@")
        self.assertEqual(analyzer.next_token(), UNKNOWN)

    def test_complex_expression(self):
        analyzer = self._create_analyzer("if (x > 0) { x = 1; }")

        tokens = []
        token = analyzer.next_token()
        while token != EOF:
            tokens.append(token)
            token = analyzer.next_token()

        self.assertGreater(len(tokens), 5)
        self.assertEqual(tokens[1], LEFT_PARENTHESIS)
        self.assertEqual(tokens[3], GREATER_THAN)
        self.assertEqual(tokens[5], RIGHT_PARENTHESIS)


if __name__ == "__main__":
    unittest.main()
