import typing, abc
T = typing.TypeVar("T")
T_co = typing.TypeVar("T_co", covariant=True)
T_con = typing.TypeVar("T_con", contravariant=True)


class Visitor(abc.ABC): ...


class Node(abc.ABC):
    @abc.abstractmethod
    def accept(self, visitor) -> typing.Any: ...
