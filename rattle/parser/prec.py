import enum as _

__all__ = "P", "Precedence"


class Precedence(_.IntEnum):
    # All none-expr related tokens have this by default
    # Hence will not be taken as valid expression tokens
    # therefore no errors should occur, except if they
    # were unexpected
    NONE = _.auto()

    # Sentinel that marks the lowest precedence
    # Also used to parse the group expression: (expr)
    LOWEST_PRECEDENCE = _.auto()

    # Assignment has the lowest precedence: =
    ASSIGNMENT = _.auto()

    # Or operator: ||
    OR = _.auto()

    # And operator: &&
    AND = _.auto()

    # Comparissons that always return true/false: == !=
    COMPARISSON = _.auto()

    # Relational operators: >= <= > <
    RELATIONAL = _.auto()

    # Arithmetic operators: + - * /
    PLUS = _.auto()
    MINUS = _.auto()
    MULTIPLY = _.auto()
    DIVIDE = _.auto()

    # All general unary operators use this: +, -
    # They have to have high precedence than binary
    # operators except if explicitly specified
    UNARY = _.auto()

    # Call expressions of the form `expr(args)`: ()
    # This is an infix operator if you think about it.
    # I mean look at the opening paren, goes between
    # the invoked expression and a comma separated arg list
    CALL = _.auto()

    # Member access operator: .
    DOT = _.auto()

    # number, string, variable, true, false, nil
    # We can say all litaral values are in this level
    PRIMARY = _.auto()


    # To make sure `Prec(prec + 1)` is always valid
    # NOTE: Do not use this to mark any precedence since if prec
    #      is equal to this then `Prec(prec + 1)` might fail.
    HIGHEST_PRECEDENCE = _.auto()


# Precedence is a very long word.
P = Precedence
