"""
day6 solution
https://adventofcode.com/2015/day/6
"""

from dataclasses import dataclass
from enum import StrEnum


PART_1 = True


class Command(StrEnum):
    TOGGLE = "toggle"
    ON = "turn on"
    OFF = "turn off"

    def get_value(self, old_value):
        if PART_1:
            if self == Command.TOGGLE:
                return 0 if old_value else 1
            if self == Command.OFF:
                return 0
            return 1
        else:
            if self == Command.TOGGLE:
                return old_value + 2
            elif self == Command.ON:
                return old_value + 1
            elif self == Command.OFF:
                old_value -= 1
                old_value = max(0, old_value)
                return old_value


@dataclass
class Position:
    row: int
    col: int

    def __str__(self):
        return f"{self.row}, {self.col}"


@dataclass
class Instruction:
    command: Command
    range_from: Position
    range_to: Position

    @property
    def row_range(self):
        """row range inclusive"""
        if self.range_to.row < self.range_from.row:
            print(self.range_from, self.range_to)
        return self.range_from.row, self.range_to.row + 1

    @property
    def col_range(self):
        if self.range_to.col < self.range_from.col:
            print(self.range_from, self.range_to)
        return self.range_from.col, self.range_to.col + 1

    def __str__(self):
        return f"{str(self.command)}: {self.range_from} to {self.range_to}"


class Grid:
    lights: list[list[bool]]

    def __init__(self, size):
        self.lights = [[0 for _ in range(size)] for _ in range(size)]

    def execute(self, instruction):
        """executes an instruction"""
        row_range = instruction.row_range
        col_range = instruction.col_range
        command = instruction.command
        for row in range(*row_range):
            for col in range(*col_range):
                old_value = self.lights[row][col]
                self.lights[row][col] = command.get_value(old_value)

    def num_on(self):
        """returns how many are on"""
        return sum(sum(row) for row in self.lights)

    def __str__(self):
        return "\n" + "\n".join(
            "".join("1" if value else "0" for value in row) for row in self.lights
        )


def split_instruction_type(line):
    """returns instruction type and rest of line"""
    for command in list(Command):
        if line.startswith(str(command)):
            remainder = line[len(command) :]
            return command, remainder
    raise ValueError(f"unknown instruction type: {line}")


def split_position(string):
    """convert position string to well formed data type"""
    row, col = string.strip().split(",")
    return Position(int(row), int(col))


def parse_instruction(line):
    """parses a single line of input"""
    command, string = split_instruction_type(line)
    range_from_str, range_to_str = string.split("through")
    range_from = split_position(range_from_str)
    range_to = split_position(range_to_str)
    return Instruction(command, range_from, range_to)


def get_instructions():
    """grabs the input"""
    with open("input.txt", "r", encoding="utf8") as file:
        return [parse_instruction(line) for line in file]


def main():
    grid = Grid(1000)

    instructions = get_instructions()

    for instruction in instructions:
        grid.execute(instruction)

    print(grid.num_on())


if __name__ == "__main__":
    main()
