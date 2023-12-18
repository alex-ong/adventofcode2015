"""day8 solution"""


def main() -> None:
    with open("input.txt") as file:
        result: int = 0
        for line in file:
            line = line.strip()
            result += len(line) - len(eval(line))
    print(result)


if __name__ == "__main__":
    main()
