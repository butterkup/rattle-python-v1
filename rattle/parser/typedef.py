import typing as ty


if ty.TYPE_CHECKING:
    from .rules import Info, Associativity
    from ..nodes.expr import Expression
    from .prec import Precedence
else:
    Expression = Associativity = Info = Precedence = type

__all__ = "InfixParser", "PrefixParser"

InfixParser = ty.Callable[[Info, Precedence, Associativity, Expression], Expression]
PrefixParser = ty.Callable[[Info, Precedence], Expression]
ExprParser = ty.Callable[[Info, Precedence | None], Expression]
