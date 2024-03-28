"""
Handle all expression parsing.
Precedence, associativity and all
algorithms related.
"""

from ..token import Tktype as Tk
from ..nodes import expr as E
from .prec import P
import typing as ty
from . import error
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


def expression(stream: Stream) -> E.Expression:
    "Build info object and start parsing"
    info = Info(stream, expression_parser)
    return expression_parser(info)


def expression_parser(info: Info, prec: P | None = None) -> E.Expression:
    "Kick off expression parsing from the lowest level."
    return pratts_expr_parser(info, prec or P.LOWEST_PRECEDENCE)


# Represents no rule to parse a token as an expression or an operator
NoRule: ty.Final[Rule] = Rule(P.NONE, P.NONE)
_primary_rule = Rule(P.PRIMARY, P.NONE, primary_expr)
# Mapping of token type and parse rule
OpRules: ty.Final[dict[Tk, Rule]] = {
    Tk.EQUAL: Rule(P.NONE, P.ASSIGNMENT, None, binary_expr, A.RIGHT),
    Tk.PLUS_EQUAL: Rule(P.NONE, P.OP_ASSIGNMENT, None, binary_expr, A.RIGHT),
    Tk.STAR_EQUAL: Rule(P.NONE, P.OP_ASSIGNMENT, None, binary_expr, A.RIGHT),
    Tk.SLASH_EQUAL: Rule(P.NONE, P.OP_ASSIGNMENT, None, binary_expr, A.RIGHT),
    Tk.MINUS_EQUAL: Rule(P.NONE, P.OP_ASSIGNMENT, None, binary_expr, A.RIGHT),
    #
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
    Tk.OPEN_PAREN: Rule(P.GROUP, P.CALL, group_expr, call_expr),
    Tk.DOT: Rule(P.NONE, P.DOT, None, dot_expr),
    #
    Tk.EQUAL_EQUAL: Rule(P.NONE, P.COMPARISSON, None, binary_expr),
    Tk.BANG_EQUAL: Rule(P.NONE, P.COMPARISSON, None, binary_expr),
    #
    Tk.GREATER: Rule(P.NONE, P.RELATIONAL, None, binary_expr),
    Tk.GREATER_THAN: Rule(P.NONE, P.RELATIONAL, None, binary_expr),
    Tk.LESS: Rule(P.NONE, P.RELATIONAL, None, binary_expr),
    Tk.LESS_THAN: Rule(P.NONE, P.RELATIONAL, None, binary_expr),
    #
    Tk.AND: Rule(P.NONE, P.AND, None, binary_expr),
    Tk.OR: Rule(P.NONE, P.OR, None, binary_expr),
}


def pratts_expr_parser(info: Info, prec: P) -> E.Expression:
    "Pratts parsing algorithm"
    tk = info.stream.peek()
    if tk is None:
        raise error.UnexpectedEndOfProgram(tk)
    rule = OpRules.get(tk.type, NoRule)
    if rule.prefix is None:
        raise error.MissingExpression(tk)
    if prec > rule.pre_prec:
        raise error.MissingExpression(tk)
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
