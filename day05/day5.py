"""
day5 solution
https://adventofcode.com/2015/day/5
"""


VOWELS = "aeiou"
NAUGHTY_PAIRS = ["ab", "cd", "pq", "xy"]


def count_vowels(string: str):
    """Counts vowels in string"""
    return sum(1 if letter in VOWELS else 0 for letter in string)


def one_letter_gap(string: str):
    """returns true if there's a substring like x_x"""
    for index in range(len(string) - 2):
        substring = string[index : index + 3]
        if substring[0] == substring[2]:
            return True
    return False


def is_nice(string: str):
    """part1"""
    vowel_count = count_vowels(string)

    if vowel_count < 3:
        return False

    has_pair = False
    for index in range(len(string) - 1):
        pair = string[index : index + 2]
        if pair in NAUGHTY_PAIRS:
            return False
        if pair[0] == pair[1]:
            has_pair = True

    return has_pair


def is_nice2(string: str):
    """part 2"""
    if not one_letter_gap(string):
        return False

    for index in range(len(string) - 1):
        sub_string = string[index : index + 2]
        start_of_string = string[:index]
        end_of_string = string[index + 2 :]

        if sub_string in start_of_string or sub_string in end_of_string:
            return True
    return False


def parse_input():
    """gets the lines"""
    with open("input.txt", "r", encoding="utf8") as file:
        return list(file)


def main():
    lines: list[str] = parse_input()

    # q1
    nice_lines = sum(1 if is_nice(line) else 0 for line in lines)
    print(nice_lines)

    # q2
    nice_lines = sum(1 if is_nice2(line) else 0 for line in lines)
    print(nice_lines)


if __name__ == "__main__":
    main()
