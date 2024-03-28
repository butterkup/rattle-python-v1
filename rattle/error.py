import typing as ty

if ty.TYPE_CHECKING:
    from .token import Token
else:
    Token = type


class RattleError(Exception):
    "All rattle errors derive from this."


class LexingError(RattleError):
    """
    There is only one kind of error that the
    lexer can throw and that occurs if it encounters
    an unrecognized character while traversing the
    program string.
    The invalid character will be sent to the parser
    wrapped in a token whose type is a special value
    TkType.ERROR and as usual the character will be
    stored in the token itself which will be used to
    raise this error, yes, the parser throws this error
    not the lexer; this is because the lexer is a token
    generator and as we know generators stop their
    iteration once an error is encountered which we
    don't want.
    After this, the parser will stop parsing and drain
    the lexer ignoring all non-error tokens so that the
    user can get a whole list of the invalid characters
    instead of notifying them one by one.
    """

    def __init__(self, token: Token) -> None:
        self.error_token = token

    def __str__(self) -> str:
        # The error message will be set in the token
        return f"{self.error_token.error}: {self.error_token.lexeme}"
