from .typedef import InfixParser, PrefixParser, ExprParser
from ..token import Tktype as Tk
import typing as ty, enum as _
from ..nodes import expr as e
from .prec import Precedence
from . import error

if ty.TYPE_CHECKING:
    from ..lexer import Stream
else:
    Stream = type


class Associativity(_.StrEnum):
    "A way to deal with operator associativity."
    RIGHT = _.auto()
    LEFT = _.auto()


class Rule:
    "Bundle up an operators parsing infomation."

    def __init__(
        self,
        pre_prec: Precedence,
        in_prec: Precedence,
        prefix: PrefixParser | None = None,
        infix: InfixParser | None = None,
        assoc: Associativity | None = None,
    ) -> None:
        self.assoc = assoc or A.LEFT
        self.pre_prec = pre_prec
        self.in_prec = in_prec
        self.prefix = prefix
        self.infix = infix


class Info:
    "Hold parsing related information."

    def __init__(self, stream: Stream, parser: ExprParser) -> None:
        self.stream = stream
        self.parser = parser


# Associativity is a very long word
A = Associativity


def primary_expr(info: Info, _: Precedence) -> e.PrimaryExpr:
    tk = info.stream.peek()
    info.stream.pop()
    Klass: type[e.PrimaryExpr]
    match tk.type:
        case Tk.NUMBER:
            Klass = e.Number
        case Tk.NIL:
            Klass = e.Nil
        case Tk.STRING:
            Klass = e.String
        case Tk.TRUE:
            Klass = e.BoolTrue
        case Tk.FALSE:
            Klass = e.BoolFalse
        case Tk.IDENTIFIER:
            Klass = e.Variable
        case _:
            raise error.UnknownPrimary(tk)
    return Klass(tk)


def group_expr(info: Info, prec: Precedence) -> e.Group:
    tk = info.stream.peek()
    info.stream.pop()
    expr = info.parser(info, None)
    tk = info.stream.peek()
    if tk.type != Tk.CLOSE_PAREN:
        raise error.UnclosedGroupExpr(tk, ")")
    # Own the close paren
    info.stream.pop()
    return e.Group(tk, expr)


def unary_expr(info: Info, prec: Precedence) -> e.UnaryExpr:
    tk = info.stream.peek()
    info.stream.pop()
    operand = info.parser(info, prec)
    Klass: type[e.UnaryExpr]
    match tk.type:
        case Tk.PLUS:
            Klass = e.UnaryPlus
        case Tk.MINUS:
            Klass = e.UnaryMinus
        case Tk.BANG:
            Klass = e.Not
        case _:
            raise error.UnknownUnaryOperator(tk)
    return Klass(tk, operand)


def associate(prec: Precedence, assoc: A) -> Precedence:
    match assoc:
        case A.LEFT:
            prec = Precedence(prec + 1)
        case A.RIGHT:
            prec = prec
    return prec


def binary_expr(
    info: Info, prec: Precedence, assoc: Associativity, left: e.Expression
) -> e.BinaryExpr:
    tk = info.stream.peek()
    info.stream.pop()
    prec = associate(prec, assoc)
    right = info.parser(info, prec)
    Klass: type[e.BinaryExpr]

    match tk.type:
        case Tk.PLUS:
            Klass = e.Plus
        case Tk.MINUS:
            Klass = e.Minus
        case Tk.STAR:
            Klass = e.Multiply
        case Tk.SLASH:
            Klass = e.Divide
        case Tk.EQUAL:
            Klass = e.Assign
        case Tk.EQUAL_EQUAL:
            Klass = e.Equal
        case Tk.BANG_EQUAL:
            Klass = e.NotEqual
        case Tk.GREATER:
            Klass = e.Greater
        case Tk.GREATER_THAN:
            Klass = e.GreaterThan
        case Tk.LESS:
            Klass = e.Less
        case Tk.LESS_THAN:
            Klass = e.LessThan
        case Tk.AND:
            Klass = e.And
        case Tk.OR:
            Klass = e.Or
        case Tk.PLUS_EQUAL:
            right = e.Plus(tk, left, right)
            Klass = e.Assign
        case Tk.MINUS_EQUAL:
            right = e.Minus(tk, left, right)
            Klass = e.Assign
        case Tk.STAR_EQUAL:
            right = e.Multiply(tk, left, right)
            Klass = e.Assign
        case Tk.SLASH_EQUAL:
            right = e.Divide(tk, left, right)
            Klass = e.Assign
        case _:
            raise error.UnknownBinaryOperator(tk)
    return Klass(tk, left, right)


def call_expr(
    info: Info, prec: Precedence, assoc: Associativity, left: e.Expression
) -> e.Call:
    tk = info.stream.peek()
    info.stream.pop()
    args: list[e.Expression] = []
    while True:
        args.append(info.parser(info, None))
        cc = info.stream.pop()
        if cc is None:
            raise error.UnexpectedEndOfProgram(tk)
        match cc.type:
            case Tk.COMMA:
                continue
            case Tk.CLOSE_PAREN:
                break
            case _:
                raise error.ExpectedToken(cc, ",", ")")
    return e.Call(tk, left, args)


def dot_expr(
    info: Info, prec: Precedence, assoc: Associativity, left: e.Expression
) -> e.Dot:
    tk = info.stream.peek()
    info.stream.pop()
    member = info.stream.pop()
    if member is None or member.type != Tk.IDENTIFIER:
        raise error.ExpectedToken(member, "IDENTIFIER")
    member = e.Member(member)
    return e.Dot(tk, left, member)
