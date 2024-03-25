import typing as ty

if ty.TYPE_CHECKING:
    from .token import Token
else:
    Token = object

TokenStream = ty.Generator[Token, None, None]
