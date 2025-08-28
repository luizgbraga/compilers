ID = 1
NUMERAL = 2
CHARACTER = 3
STRING = 4
EOF = 5
UNKNOWN = 6

COLON = 7
PLUS = 8
MINUS = 9
SEMI_COLON = 10
COMMA = 11
LEFT_SQUARE = 12
RIGHT_SQUARE = 13
LEFT_BRACES = 14
RIGHT_BRACES = 15
LEFT_PARENTHESIS = 16
RIGHT_PARENTHESIS = 17
TIMES = 18
DOT = 19
DIVIDE = 20

PLUS_PLUS = 21
MINUS_MINUS = 22
EQUAL_EQUAL = 23
EQUALS = 24
AND = 25
OR = 26
LESS_OR_EQUAL = 27
LESS_THAN = 28
GREATER_OR_EQUAL = 29
GREATER_THAN = 30
NOT_EQUAL = 31
NOT = 32

KEYWORDS = {
    "array": 100,
    "boolean": 101,
    "break": 102,
    "char": 103,
    "continue": 104,
    "do": 105,
    "else": 106,
    "false": 107,
    "function": 108,
    "if": 109,
    "integer": 110,
    "of": 111,
    "string": 112,
    "struct": 113,
    "true": 114,
    "type": 115,
    "var": 116,
    "while": 117,
}

SYMBOLS = {
    ":": COLON,
    "+": PLUS,
    "-": MINUS,
    ";": SEMI_COLON,
    ",": COMMA,
    "[": LEFT_SQUARE,
    "]": RIGHT_SQUARE,
    "{": LEFT_BRACES,
    "}": RIGHT_BRACES,
    "(": LEFT_PARENTHESIS,
    ")": RIGHT_PARENTHESIS,
    "*": TIMES,
    ".": DOT,
    "/": DIVIDE,
}
