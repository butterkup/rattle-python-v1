import enum, typing


class Tktype(enum.StrEnum):
    ERROR = enum.auto()
    SEMICOLON = enum.auto()

    STRING = enum.auto()
    NUMBER = enum.auto()
    TRUE = enum.auto()
    FALSE = enum.auto()
    NIL = enum.auto()
    IDENTIFIER = enum.auto()

    DOT = enum.auto()
    COMMA = enum.auto()
    GREATER = enum.auto()
    GREATER_THAN = enum.auto()
    LESS = enum.auto()
    LESS_THAN = enum.auto()
    BANG = enum.auto()
    BANG_EQUAL = enum.auto()
    EQUAL = enum.auto()
    EQUAL_EQUAL = enum.auto()
    PLUS = enum.auto()
    MINUS = enum.auto()
    STAR = enum.auto()
    SLASH = enum.auto()

    AND = enum.auto()
    OR = enum.auto()
    VERTBAR = enum.auto()
    AMPERSAND = enum.auto()
    OPEN_PAREN = enum.auto()
    CLOSE_PAREN = enum.auto()
    OPEN_BRACE = enum.auto()
    CLOSE_BRACE = enum.auto()
    OPEN_SQBKT = enum.auto()
    CLOSE_SQBKT = enum.auto()

    IF = enum.auto()
    WHILE = enum.auto()
    ELSE = enum.auto()
    FN = enum.auto()
    LET = enum.auto()
    FOR = enum.auto()
    RETURN = enum.auto()
    CONTINUE = enum.auto()
    BREAK = enum.auto()
    # CLASS = enum.auto()
    # THIS = enum.auto()
    THROW = enum.auto()
    CATCH = enum.auto()


class Location(typing.NamedTuple):
    line: int
    column: int
    position: int


class Token:
    def __init__(
        self, tktype: Tktype, lexeme: str, location: Location, error: str | None = None
    ) -> None:
        self.type = tktype
        self.lexeme = lexeme
        self.location = location
        self.error = error

    def __str__(self) -> str:
        return f"Token({self.type!s}, {self.lexeme!r}, line={self.location.line}, column={self.location.column})"


keywords: typing.Final[dict[str, Tktype]] = {
    "while": Tktype.WHILE,
    "for": Tktype.FOR,
    "fn": Tktype.FN,
    "let": Tktype.LET,
    "if": Tktype.IF,
    "else": Tktype.ELSE,
    "return": Tktype.RETURN,
    "true": Tktype.TRUE,
    "false": Tktype.FALSE,
    "nil": Tktype.NIL,
    "break": Tktype.BREAK,
    "continue": Tktype.CONTINUE,
    "throw": Tktype.THROW,
    "catch": Tktype.CATCH,
    # "class": Tktype.CLASS,
    # "this": Tktype.THIS,
}
