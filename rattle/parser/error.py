from ..error import RattleError
from ..token import Token


class RattleParserError(RattleError):
    "All errors that involve parsing."

    def __init__(self, token: Token) -> None:
        # Token where the error occurred.
        self.error_token = token


class ExpectedToken(RattleParserError):
    def __init__(self, token: Token, *expected: str) -> None:
        super().__init__(token)
        self.expected = expected

    def __str__(self) -> str:
        return f"Expected one of {self.expected} but got {self.error_token}"


class UnexpectedEndOfProgram(RattleParserError): ...


class ExpressionError(RattleParserError):
    "Errors that involve expression parsing."

    def __str__(self) -> str:
        return f"Malformed expression at {self.error_token}"


class UnExpectedToken(ExpressionError):
    def __init__(self, token: Token, expected: str) -> None:
        super().__init__(token)
        self.expected = expected

    def __str__(self) -> str:
        return f"Expected token {self.expected!r} but got {self.error_token}"


class UnclosedCallExpr(UnExpectedToken):
    def __str__(self) -> str:
        return f"Call expression was not closed, expected {self.expected!r} got {self.error_token}"


class UnclosedGroupExpr(UnExpectedToken):
    def __str__(self) -> str:
        return f"Group expression was not closed, expected {self.expected!r} got {self.error_token}"


class UnknownOperator(ExpressionError):
    "Unknown operator tokens."

    def __str__(self) -> str:
        return f"Unknown operator at {self.error_token}"


class UnknownUnaryOperator(UnknownOperator):
    "Unknown unary operator"

    def __str__(self) -> str:
        return f"Expected a unary operator but got {self.error_token}"


class UnknownBinaryOperator(UnknownOperator):
    "Unknown binary operator"

    def __str__(self) -> str:
        return f"Expected a binary operator but got {self.error_token}"


class UnknownPrimary(UnknownOperator):
    "Unknown primary values."

    def __str__(self) -> str:
        return f"Expected a primary value like numbers, strings and boolean but got {self.error_token}"


class MissingExpression(ExpressionError):
    "Errors that involve a lack of expression where one is expected."

    def __str__(self) -> str:
        return f"Expected an expression but got {self.error_token}"


class StatementError(RattleParserError):
    "Errors that involve statement parsing."
