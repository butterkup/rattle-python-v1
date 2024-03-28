from .abc import Node, Visitor
from .expr import Expression
from ..token import Token
import abc


class StatementVisitor(Visitor, abc.ABC):
    @abc.abstractmethod
    def accept_block(self, stmt: "Block"): ...
    @abc.abstractmethod
    def accept_if(self, stmt: "If"): ...
    @abc.abstractmethod
    def accept_while(self, stmt: "While"): ...
    @abc.abstractmethod
    def accept_for(self, stmt: "For"): ...
    @abc.abstractmethod
    def accept_break(self, stmt: "Break"): ...
    @abc.abstractmethod
    def accept_continue(self, stmt: "Continue"): ...
    @abc.abstractmethod
    def accept_function(self, stmt: "Function"): ...
    @abc.abstractmethod
    def accept_let(self, stmt: "Let"): ...
    @abc.abstractmethod
    def accept_try(self, stmt: "Try"): ...
    @abc.abstractmethod
    def accept_throw(self, stmt: "Throw"): ...


class Statement(Node):
    def accept(self, visitor: StatementVisitor):
        target = f"accept_{self.__class__.__name__.lower()}"
        dispatch = getattr(visitor, target, None)
        if dispatch is None:
            raise NotImplementedError(self, target, visitor)
        return dispatch(self)


class Loop(Statement): ...


class If(Statement):
    def __init__(self, expr: Expression, then_b: Statement, else_b: Statement) -> None:
        self.expression = expr
        self.then_body = then_b
        self.else_body = else_b


class For(Loop):
    def __init__(
        self,
        init: Expression | None,
        cond: Expression | None,
        incr: Expression | None,
        body: Statement,
    ) -> None:
        self.initializer = init
        self.condition = cond
        self.increment = incr
        self.for_body = body


class While(Loop):
    def __init__(self, expr: Expression, body: Statement) -> None:
        self.expression = expr
        self.while_body = body


class Throw(Statement):
    def __init__(self, expr: Expression) -> None:
        self.expression = expr


class Break(Statement): ...


class Continue(Statement): ...


class Let(Statement):
    def __init__(self, let: Token, expr: dict[str, Expression | None]) -> None:
        self.let = let
        self.defined = expr


class Block(Statement):
    def __init__(self, body: list[Statement]) -> None:
        self.body = body

    def __len__(self) -> int:
        return len(self.body)

    def __bool__(self) -> bool:
        return bool(self.body)


class Try(Statement):
    def __init__(self, try_b: Statement, catch_b: Statement) -> None:
        self.try_body = try_b
        self.catch_body = catch_b


class Function(Statement):
    def __init__(
        self, token: Token, name: Token, param: list[Token], body: Statement
    ) -> None:
        self.name = name
        self.token = token
        self.parameters = param
        self.function_body = body
