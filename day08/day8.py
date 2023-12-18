"""day8 solution"""


def main() -> None:
    part1()
    part2()


def part1() -> None:
    with open("input.txt") as file:
        result: int = 0
        for line in file:
            line = line.strip()
            result += len(line) - len(eval(line))
    print(result)


def process_line(line: str) -> int:
    index: int = 0
    result: int = 0
    while index < len(line):
        if line[index] == '"':
            result += 2
            index += 1
        elif line[index] == "\\":
            if line[index + 1] == "\\" or line[index + 1] == '"':
                result += 4
                index += 2
            else:  # line[index + 1] == "x":
                result += 2
                index += 1
        else:
            result += 1
            index += 1
    result += 2
    return result


def part2() -> None:
    with open("input.txt") as file:
        result: int = 0
        for line in file:
            line = line.strip()
            length = process_line(line)
            result += length - len(line)
    print(result)


if __name__ == "__main__":
    main()
