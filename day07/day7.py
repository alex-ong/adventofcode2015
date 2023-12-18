"""day7 solution"""
from collections import defaultdict
from dataclasses import dataclass

from operation import Operation


@dataclass
class Wire:
    name: str
    operation: Operation
    result: int | None = None

    def get_dependencies(self) -> list[str]:
        return self.operation.get_dependencies()

    def is_solvable(self, solutions: dict[str, int]) -> bool:
        return self.operation.calculatable(solutions)

    def solve(self, solutions: dict[str, int]) -> int:
        self.result = self.operation.solve(solutions)
        return self.result

    def __hash__(self) -> int:
        return hash(f"{self.name} | {self.operation}")


def get_input() -> list[Wire]:
    wires: list[Wire] = []
    with open("input.txt") as file:
        for line in file:
            operation_str, name = line.split("->")
            operation_args = operation_str.strip().split()
            wires.append(Wire(name.strip(), Operation(operation_args)))
    return wires


def check_wire(
    wire: Wire,
    solved_cache: dict[str, int],
    unsolved: set[Wire],
    wire_dependents: dict[str, list[Wire]],
):
    """Checks wire. If solvable, checks its dependents and solves more."""
    if wire.is_solvable(solved_cache) and wire in unsolved:
        solved_cache[wire.name] = wire.solve(solved_cache)
        unsolved.remove(wire)
        dependents: list[Wire] = wire_dependents[wire.name]
        for dependent in dependents:
            check_wire(dependent, solved_cache, unsolved, wire_dependents)


def main() -> None:
    wires = get_input()
    # mapping wire_name -> wire's that rely on this wire
    wire_dependents: dict[str, list[Wire]] = defaultdict(list)
    solved_cache: dict[str, int] = {}
    unsolved: set[Wire] = set(wires)

    for wire in wires:
        dependencies = wire.get_dependencies()
        for dependency in dependencies:
            wire_dependents[dependency].append(wire)

    # build dependency list
    while len(unsolved) > 0:
        num_unsolved = len(unsolved)
        for wire in wires:
            check_wire(wire, solved_cache, unsolved, wire_dependents)

        if len(unsolved) == num_unsolved:
            print("uh oh")
            break
    # done
    # print("\n".join(str(wire) for wire in sorted(wires, key=lambda x: x.name)))
    print(solved_cache["a"])


if __name__ == "__main__":
    main()
