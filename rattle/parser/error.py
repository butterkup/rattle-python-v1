from ..error import RattleError


class RattleParserError(RattleError):
    "All errors that involve parsing."


class ExpressionError(RattleParserError):
    "Errors that involve expression parsing."


class UnknownOperator(ExpressionError):
    "Unknown operator tokens."


class UnknownUnaryOperator(UnknownOperator):
    "Unknown unary operator"


class UnknownBinaryOperator(UnknownOperator):
    "Unknown binary operator"

class UnknownPrimary(UnknownOperator):
    "Unknown primary values."

class MissingExpression(ExpressionError):
    "Errors that involve a lack of expression where one is expected."


class StatementError(RattleParserError):
    "Errors that involve statement parsing."
