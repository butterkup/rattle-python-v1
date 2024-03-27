import enum

__all__ = "I", "Instruction"


class Instruction(enum.StrEnum):
    ADD = enum.auto()
    NEGATE = enum.auto()
    DIVIDE = enum.auto()
    MULTIPLY = enum.auto()
    SUBTRACT = enum.auto()


I = Instruction
