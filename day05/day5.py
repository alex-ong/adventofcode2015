"""day5 solution"""

"""
A nice string is one with all of the following properties:

It contains at least three vowels (aeiou only), like aei, xazegov, or aeiouaeiouaeiou.
It contains at least one letter that appears twice in a row, like xx, abcdde (dd), or aabbccdd (aa, bb, cc, or dd).
It does not contain the strings ab, cd, pq, or xy, even if they are part of one of the other requirements.
"""
VOWELS = "aeiou"
NAUGHTY_PAIRS = ["ab", "cd", "pq", "xy"]


def count_vowels(string: str):
    """Counts vowels in string"""
    return sum(1 if letter in VOWELS else 0 for letter in string)


def is_nice(string: str):
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


def parse_input():
    """gets the lines"""
    with open("input.txt", "r", encoding="utf8") as file:
        return list(file)


def main():
    lines = parse_input()

    # q1
    nice_lines = sum(1 if is_nice(line) else 0 for line in lines)
    print(nice_lines)


if __name__ == "__main__":
    main()
