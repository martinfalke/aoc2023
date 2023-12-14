import sys
import re

DAY = 1


def read_input(part, use_example_input=False):
    global DAY
    if DAY < 10:
        DAY = "0" + str(DAY)
    example_filename = "example_input.txt" if part == 1 else "example_input2.txt"
    filename = example_filename if use_example_input else f'input{DAY}.txt'
    file = open(filename, mode='r')
    lines = file.read().splitlines()
    file.close()
    return lines


# define spelled digits for regex and adding
spelled_digits = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
digits_dict = {digit[:-1]: str(idx + 1) for idx, digit in enumerate(spelled_digits)}

# define patterns
spelled_digits_pattern = '|'.join([f'{digit[:-1]}(?={digit[-1]})' for digit in spelled_digits])

# Part 1
pattern_1 = re.compile("([0-9])")
# Part 2
pattern_2 = re.compile(r'([0-9]|{spelled_digits_pattern})'.format(spelled_digits_pattern=spelled_digits_pattern))


def solve(input, part):
    num_sum = 0
    line_num = 1  # debug
    for line in input:
        matches = re.findall(pattern_1, line) if part == 1 else re.findall(pattern_2, line)

        first = matches[0]
        if len(first) > 1:
            first = digits_dict[first]
        last = matches[-1]
        if len(last) > 1:
            last = digits_dict[last]

        num = int(first + last)

        # debug
        debug = False
        if line_num % 30 == 3 and debug:
            print(f'line num: {line_num}\nFull line:\n{line}')
            print(f'Matches: {matches}')
            print(f'First: {first}, Last: {last}')
            print(f'Num: {num}')
            print()
            line_num += 1

        num_sum += num
    return num_sum


if __name__ == "__main__":
    part = 1
    use_example_input = False
    if len(sys.argv) > 1:
        part = int(sys.argv[1])
        if len(sys.argv) > 2:
            use_example_input = not int(sys.argv[2]) == 0
    input = read_input(part, use_example_input)
    solution = solve(input, part)
    print('Solution:')
    print(solution)
