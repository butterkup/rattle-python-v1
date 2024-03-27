"""
Handle all expression parsing.
Precedence, associativity and all
algorithms related.
"""

from ..token import Tktype as Tk
from ..nodes import expr as e
from .prec import P
import typing as ty
from .rules import (
    Rule,
    Info,
    A,
    dot_expr,
    primary_expr,
    group_expr,
    unary_expr,
    binary_expr,
    call_expr,
)

# Export only the parser; the expression parser.
__all__ = ("expression",)

if ty.TYPE_CHECKING:
    from ..lexer import Stream
else:
    Stream = type


def expression(stream: Stream) -> e.Expression:
    "Build info object and start parsing"
    info = Info(stream, expression_parser)
    return expression_parser(info)


def expression_parser(info: Info, prec: P | None = None) -> e.Expression:
    "Kick off expression parsing from the lowest level."
    return pratts_expr_parser(info, prec or P.LOWEST_PRECEDENCE)


# Represents no rule to parse a token as an expression or an operator
NoRule: ty.Final[Rule] = Rule(P.NONE, P.NONE)
_primary_rule = Rule(P.PRIMARY, P.NONE, primary_expr)
# Mapping of token type and parse rule
OpRules: ty.Final[dict[Tk, Rule]] = {
    Tk.NUMBER: _primary_rule,
    Tk.STRING: _primary_rule,
    Tk.NIL: _primary_rule,
    Tk.TRUE: _primary_rule,
    Tk.FALSE: _primary_rule,
    Tk.IDENTIFIER: _primary_rule,
    #
    Tk.BANG: Rule(P.UNARY, P.NONE, unary_expr),
    Tk.PLUS: Rule(P.UNARY, P.PLUS, unary_expr, binary_expr, A.LEFT),
    Tk.MINUS: Rule(P.UNARY, P.MINUS, unary_expr, binary_expr, A.LEFT),
    Tk.STAR: Rule(P.NONE, P.MULTIPLY, None, binary_expr, A.LEFT),
    Tk.SLASH: Rule(P.NONE, P.DIVIDE, None, binary_expr, A.RIGHT),
    #
    Tk.OPEN_PAREN: Rule(P.LOWEST_PRECEDENCE, P.CALL, group_expr, call_expr),
    Tk.DOT: Rule(P.NONE, P.DOT, None, dot_expr),
    #
    Tk.EQUAL: Rule(P.NONE, P.ASSIGNMENT, None, binary_expr, A.RIGHT),
    Tk.EQUAL_EQUAL: Rule(P.NONE, P.COMPARISSON, None, binary_expr),
    Tk.BANG_EQUAL: Rule(P.NONE, P.COMPARISSON, None, binary_expr),
    Tk.GREATER: Rule(P.NONE, P.RELATIONAL, None, binary_expr),
    Tk.GREATER_THAN: Rule(P.NONE, P.RELATIONAL, None, binary_expr),
    Tk.LESS: Rule(P.NONE, P.RELATIONAL, None, binary_expr),
    Tk.LESS_THAN: Rule(P.NONE, P.RELATIONAL, None, binary_expr),
    #
    Tk.AND: Rule(P.NONE, P.AND, None, binary_expr),
    Tk.OR: Rule(P.NONE, P.OR, None, binary_expr),
}


def pratts_expr_parser(info: Info, prec: P) -> e.Expression:
    "Pratts parsing algorithm"
    tk = info.stream.peek()
    if tk is None:
        raise
    rule = OpRules.get(tk.type, NoRule)
    if rule.prefix is None:
        raise
    if prec > rule.pre_prec:
        raise
    left = rule.prefix(info, rule.pre_prec)
    while True:
        tk = info.stream.peek()
        if tk is None:
            break
        rule = OpRules.get(tk.type, NoRule)
        if prec > rule.in_prec:
            break
        if rule.infix is None:
            break
        left = rule.infix(info, rule.in_prec, rule.assoc, left)
    return left
