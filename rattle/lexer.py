from typing import cast
from .typedef import TokenStream
from . import token as tk
from collections import deque

__all__ = "lex", "Stream"
Tk = tk.Tktype


class Stream:
    def __init__(self, src: TokenStream | str) -> None:
        self._source = lex(src) if isinstance(src, str) else src
        self._pending: deque[tk.Token] = deque()
        self._source_empty: bool = False

    def empty(self) -> bool:
        return self._source_empty and not self._pending

    __bool__ = empty

    def peek(self, throw: bool | None = None) -> tk.Token:
        token = self.pop(throw)
        if token is not None:
            self.pend(token)
        return token

    def pend(self, token: tk.Token):
        self._pending.append(token)

    def pop(self, throw: bool | None = None) -> tk.Token:
        if self._pending:
            return self._pending.popleft()
        try:
            return next(self._source)
        except StopIteration:
            self._source_empty = True
            if throw: raise
        return cast(tk.Token, None)

    def __iter__(self):
        return self

    def __next__(self):
        return self.pop(True)


def lex(src: str) -> TokenStream:
    yield from _Lexer_impl(src).scan()


def _isalnum(char: str) -> bool:
    return char.isalnum() or char == "_"


class _Lexer_impl:
    def __init__(self, source: str, /) -> None:
        self.stop: int = len(source)
        self.current: int = 0
        self.column: int = 1
        self.source = source
        self.line: int = 1
        self.start = 0
        # Must be set last in this function
        self.start_loc = self.capture_loc()

    def capture_loc(self) -> tk.Location:
        return tk.Location(self.line, self.column, self.current)

    def lexeme(self) -> str:
        return self.source[self.start : self.current]

    def empty(self) -> bool:
        return self.current >= self.stop

    def peek(self) -> str:
        if self.empty():
            return ""
        return self.source[self.current]

    def advance(self) -> str:
        char = self.peek()
        self.column += 1
        self.current += 1
        if char == "\n":
            self.line += 1
            self.column = 1
        return char

    def consume(self) -> tuple[str, tk.Location]:
        lexeme = self.lexeme()
        self.start = self.current
        last = self.start_loc
        self.start_loc = self.capture_loc()
        return lexeme, last

    def make_token(
        self,
        tktype: Tk,
        *,
        error: str | None = None,
        loc: tk.Location | None = None,
    ):
        lexeme, location = self.consume()
        if loc is not None:
            location = loc
        return tk.Token(tktype, lexeme, location, error)

    def match(self, char: str):
        if self.peek() == char:
            self.advance()
            return True

    def string(self) -> tk.Token:
        self.advance()  # Consume opening quote
        while self.peek() != '"':
            self.advance()
            if self.empty():
                return self.make_token(Tk.ERROR, error="String was never closed.")
        self.advance()  # Consume closing quote
        return self.make_token(Tk.STRING)

    def _number(self) -> str:
        digits = ''
        while not self.empty() and self.peek().isdigit():
            digits += self.advance()
        return digits

    def number(self) -> tk.Token:
        self._number()
        if self.peek() == '.':
            self.advance()
            if not (after := self._number()):
                err = 'Expected a number after the dot in %r' % after
                return self.make_token(Tk.ERROR, error=err)
        return self.make_token(Tk.NUMBER)

    def spaces(self):
        while not self.empty():
            match self.peek():
                case " " | "\t" | "\n":
                    self.advance()
                case _:
                    break
        self.consume()  # Ignore the spaces
        return self.empty()

    def identifier(self) -> tk.Token:
        while _isalnum(self.peek()) and not self.empty():
            self.advance()
        tktype = tk.keywords.get(self.lexeme(), Tk.IDENTIFIER)
        return self.make_token(tktype)

    def scomment(self):
        while self.peek() != "\n" and not self.empty():
            self.advance()

    def mcomment(self):
        self.advance()  # *
        while True:
            if self.empty():
                err = "Unterminated multiline comment"
                return self.make_token(Tk.ERROR, error=err)
            if self.advance() == "*":
                if self.match("/"):
                    break

    def make_ctoken(self, tktype: Tk, error: str | None = None):
        self.advance()
        return self.make_token(tktype, error=error)

    def scan(self) -> TokenStream:
        while not self.spaces():
            match self.peek():
                case '"':
                    yield self.string()
                case ">":
                    self.advance()
                    tktype = Tk.GREATER_THAN if self.match("=") else Tk.GREATER
                    yield self.make_token(tktype)
                case "<":
                    self.advance()
                    tktype = Tk.LESS_THAN if self.match("=") else Tk.LESS
                    yield self.make_token(tktype)
                case "!":
                    self.advance()
                    tktype = Tk.BANG_EQUAL if self.match("=") else Tk.BANG
                    yield self.make_token(tktype)
                case "=":
                    self.advance()
                    tktype = Tk.EQUAL_EQUAL if self.match("=") else Tk.EQUAL
                    yield self.make_token(tktype)
                case "/":
                    self.advance()
                    match self.peek():
                        case "/":
                            self.scomment()
                        case "*":
                            if (e := self.mcomment()) is not None:
                                yield e
                        case _:
                            yield self.make_token(Tk.SLASH)
                case ',':
                    yield self.make_ctoken(Tk.COMMA)
                case "+":
                    yield self.make_ctoken(Tk.PLUS)
                case "-":
                    yield self.make_ctoken(Tk.MINUS)
                case "*":
                    yield self.make_ctoken(Tk.STAR)
                case ";":
                    yield self.make_ctoken(Tk.SEMICOLON)
                case "{":
                    yield self.make_ctoken(Tk.OPEN_BRACE)
                case "}":
                    yield self.make_ctoken(Tk.CLOSE_BRACE)
                case "[":
                    yield self.make_ctoken(Tk.OPEN_SQBKT)
                case "]":
                    yield self.make_ctoken(Tk.CLOSE_SQBKT)
                case "(":
                    yield self.make_ctoken(Tk.OPEN_PAREN)
                case ")":
                    yield self.make_ctoken(Tk.CLOSE_PAREN)
                case "&":
                    self.advance()
                    tktype = Tk.AND if self.match("&") else Tk.AMPERSAND
                    yield self.make_token(tktype)
                case "|":
                    self.advance()
                    tktype = Tk.OR if self.match("|") else Tk.VERTBAR
                    yield self.make_token(tktype)
                case char:
                    if char.isdigit():
                        yield self.number()
                    elif _isalnum(char):
                        yield self.identifier()
                    else:
                        err = "Unexpected character %r." % char
                        yield self.make_ctoken(Tk.ERROR, err)
