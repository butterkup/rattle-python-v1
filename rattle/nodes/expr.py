from .abc import Node, Visitor
from ..token import Token
import abc, typing


class ExpressionVisitor(Visitor, abc.ABC):
    @abc.abstractmethod
    def accept_plus(self, expr: "Plus") -> typing.Any: ...
    @abc.abstractmethod
    def accept_minus(self, expr: "Minus") -> typing.Any: ...
    @abc.abstractmethod
    def accept_multiply(self, expr: "Multiply") -> typing.Any: ...
    @abc.abstractmethod
    def accept_divide(self, expr: "Divide") -> typing.Any: ...
    @abc.abstractmethod
    def accept_unaryminus(self, expr: "UnaryMinus") -> typing.Any: ...
    @abc.abstractmethod
    def accept_unaryplus(self, expr: "UnaryPlus") -> typing.Any: ...
    @abc.abstractmethod
    def accept_equal(self, expr: "Equal") -> typing.Any: ...
    @abc.abstractmethod
    def accept_notequal(self, expr: "NotEqual") -> typing.Any: ...
    @abc.abstractmethod
    def accept_assign(self, expr: "Assign") -> typing.Any: ...
    @abc.abstractmethod
    def accept_less(self, expr: "Less") -> typing.Any: ...
    @abc.abstractmethod
    def accept_greater(self, expr: "Greater") -> typing.Any: ...
    @abc.abstractmethod
    def accept_lessthan(self, expr: "LessThan") -> typing.Any: ...
    @abc.abstractmethod
    def accept_greaterthan(self, expr: "GreaterThan") -> typing.Any: ...
    @abc.abstractmethod
    def accept_variable(self, expr: "Variable") -> typing.Any: ...
    @abc.abstractmethod
    def accept_number(self, expr: "Number") -> typing.Any: ...
    @abc.abstractmethod
    def accept_booltrue(self, expr: "BoolTrue") -> typing.Any: ...
    @abc.abstractmethod
    def accept_boolfalse(self, expr: "BoolFalse") -> typing.Any: ...
    @abc.abstractmethod
    def accept_string(self, expr: "String") -> typing.Any: ...
    @abc.abstractmethod
    def accept_not(self, expr: "Not") -> typing.Any: ...
    @abc.abstractmethod
    def accept_nil(self, expr: "Nil") -> typing.Any: ...
    @abc.abstractmethod
    def accept_call(self, expr: "Call") -> typing.Any: ...


class Expression(Node):
    assignable: bool = False

    def accept(self, visitor: ExpressionVisitor) -> typing.Any:
        target = f"accept_{self.__class__.__name__.lower()}"
        dispatch = getattr(visitor, target, None)
        if dispatch is None:
            raise NotImplementedError(self, target, visitor)
        return dispatch(self)


class Literal:
    def __init__(self, value: Token) -> None:
        self.value = value


class Binary:
    def __init__(self, op: Token, left: Expression, right: Expression) -> None:
        self.left = left
        self.operator = op
        self.right = right


class Unary:
    def __init__(self, op: Token, operand: Expression) -> None:
        self.operator = op
        self.operand = operand


class LitaralExpr(Literal, Expression): ...


class BinaryExpr(Binary, Expression): ...


class UnaryExpr(Unary, Expression): ...


class Plus(BinaryExpr): ...


class Minus(BinaryExpr): ...


class Multiply(BinaryExpr): ...


class Divide(BinaryExpr): ...


class UnaryMinus(UnaryExpr): ...


class UnaryPlus(UnaryExpr): ...


class Equal(BinaryExpr): ...


class NotEqual(BinaryExpr): ...


class Not(UnaryExpr): ...


class Assign(BinaryExpr): ...


class Less(BinaryExpr): ...


class Greater(BinaryExpr): ...


class LessThan(BinaryExpr): ...


class GreaterThan(BinaryExpr): ...


class Variable(LitaralExpr):
    assignable = True


class Number(LitaralExpr): ...


class BoolExpr(LitaralExpr): ...


class BoolTrue(BoolExpr): ...


class BoolFalse(BoolExpr): ...


class String(LitaralExpr): ...


class Nil(LitaralExpr): ...


class Call(Expression):
    def __init__(
        self, op: Token, expr: Expression, arguments: list[Expression]
    ) -> None:
        self.operator = op
        self.expression = expr
        self.arguments = arguments
