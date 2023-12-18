"""operator / operation classes"""
from dataclasses import dataclass
from enum import Enum, StrEnum
from typing import Optional


class Operator(StrEnum):
    """operator subclass"""

    __repr__ = Enum.__str__

    AND = "AND"
    OR = "OR"
    LSHIFT = "LSHIFT"
    RSHIFT = "RSHIFT"
    NOT = "NOT"
    LVAL = "LVAL"


OPERATORS = [o.name for o in Operator]


def try_int(value: str) -> int | str:
    try:
        return int(value)
    except ValueError:
        return value


def bit_not(n: int, num_bits: int = 16) -> int:
    return (1 << num_bits) - 1 - n


def non_null(item: Optional[int]) -> int:
    if item is None:
        raise ValueError(f"{item} is None!")
    return item


def operate(
    left_val: Optional[int], operator: Operator, right_val: Optional[int]
) -> int:
    # type: ignore[operator]
    if operator == Operator.AND:
        return non_null(left_val) & non_null(right_val)
    if operator == Operator.OR:
        return non_null(left_val) | non_null(right_val)
    if operator == Operator.LVAL:
        return non_null(left_val)
    if operator == Operator.LSHIFT:
        mask = 2**16 - 1
        return (non_null(left_val) << non_null(right_val)) & mask
    if operator == Operator.RSHIFT:
        mask = 2**16 - 1
        return (non_null(left_val) >> non_null(right_val)) & mask
    if operator == Operator.NOT and right_val is not None:
        return bit_not(non_null(right_val))

    raise ValueError(f"Unsupported Operator {operator}")


@dataclass(init=False)
class Operation:
    left_val: str | int | None
    operator: Operator
    right_val: str | int | None

    def __init__(self, args: list[str]) -> None:
        if len(args) == 1:
            self.left_val = try_int(args[0])
            self.operator = Operator.LVAL
            self.right_val = None
        if len(args) == 2:
            if args[0] in OPERATORS:
                self.left_val = None
                self.operator = Operator(args[0])
                self.right_val = try_int(args[1])
            else:
                raise ValueError(args)
        if len(args) == 3:
            self.left_val = try_int(args[0])
            self.operator = Operator(args[1])
            self.right_val = try_int(args[2])

    def __str__(self) -> str:
        return f"{self.left_val}, {self.operator}, {self.right_val}"

    def calculatable(self, pre_calculated_values: dict[str, int]) -> bool:
        if (
            isinstance(self.left_val, str)
            and self.left_val not in pre_calculated_values
        ):
            return False

        if (
            isinstance(self.right_val, str)
            and self.right_val not in pre_calculated_values
        ):
            return False
        return True

    def get_dependencies(self) -> list[str]:
        """returns dependencies of this operator"""
        result = []
        if isinstance(self.left_val, str):
            result.append(self.left_val)
        if isinstance(self.right_val, str):
            result.append(self.right_val)
        return result

    def solve(self, pre_calculated_values: dict[str, int]) -> int:
        left_val: int | None
        right_val: int | None
        if isinstance(self.left_val, str):
            left_val = pre_calculated_values[self.left_val]
        else:
            left_val = self.left_val
        if isinstance(self.right_val, str):
            right_val = pre_calculated_values[self.right_val]
        else:
            right_val = self.right_val
        return operate(left_val, self.operator, right_val)
