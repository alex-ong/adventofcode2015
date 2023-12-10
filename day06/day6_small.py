"""
day6 solution
https://adventofcode.com/2015/day/6
"""


def split_instruction_type(line):
    if line.startswith("toggle"):
        return "toggle", line[len("toggle") :]
    elif line.startswith("turn on"):
        return "turn on", line[len("turn on") :]
    else:
        return "turn off", line[len("turn off") :]


def follow_instructions():
    size = 1000
    grid = [[0 for _ in range(size)] for _ in range(size)]
    """grabs the input"""
    with open("input.txt", "r", encoding="utf8") as file:
        for line in file:
            command, coords = split_instruction_type(line)
            left, right = coords.split("through")
            from_row, from_col = left.strip().split(",")
            to_row, to_col = right.strip().split(",")
            for row in range(int(from_row), int(to_row) + 1):
                for col in range(int(from_col), int(to_col) + 1):
                    old_value = grid[row][col]
                    if command == "toggle":
                        grid[row][col] = 0 if old_value else 1
                    elif command == "turn on":
                        grid[row][col] = 1
                    else:  # command == "turn off"
                        grid[row][col] = 0
    print(sum(sum(row for row in rows) for rows in grid))


if __name__ == "__main__":
    follow_instructions()
