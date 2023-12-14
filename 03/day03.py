import sys
import os
import re
import numpy as np

os.environ["TQDM_COLOUR"] = "#33ffaa"
from tqdm import tqdm

DAY = 3

# Part 1 constants
SYMBOL_PATTERN = r"[^0-9\.]"
PART_NUMBER_PATTERN = r"([0-9]+)"
# Part 2 constants
GEAR_PATTERN = r"(\*)"


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


def preprocess_input(input):
    engine_map = np.array([[c for c in line] for line in input])
    return engine_map


def mark_valid_area(is_part_number_map, r, c):
    # traverse surrounding rows
    for i in range(-1, 2):
        row = r + i
        if row < 0 or row >= is_part_number_map.shape[0]:
            # skip wrap-arounds
            continue
        # traverse surrounding columns (of the number)
        for j in range(-1, 2):
            col = c + j
            if col < 0 or col >= is_part_number_map.shape[1]:
                # skip wrap-arounds
                continue
            is_part_number_map[row, col] = True
    return is_part_number_map


def mark_part_areas(engine_map, is_part_number_map):
    r = 0
    for row in engine_map:
        c = 0
        for col in row:
            is_symbol = bool(re.search(SYMBOL_PATTERN, col))
            if is_symbol:
                is_part_number_map = mark_valid_area(is_part_number_map, r, c)
            c += 1
        r += 1

    return is_part_number_map


# Part 1
def get_part_num_sum(input, engine_map):
    # boolean map for valid part number positions
    is_part_number_map = np.zeros(engine_map.shape, dtype=bool)

    # mark all areas valid as part numbers
    is_part_number_map = mark_part_areas(engine_map, is_part_number_map)
    # sum of all engine part numbers
    part_num_sum = 0
    r = 0
    for row in tqdm(input):
        for number_match in re.finditer(PART_NUMBER_PATTERN, row):
            c_start, c_end = number_match.span()
            if np.any(is_part_number_map[r, c_start:c_end]):
                part_num_sum += int(number_match.group())
        r += 1

    return part_num_sum


# Part 2
def mark_neighbor_nums(gear_neighbor_map, r, c_start, num):
    num_length = len(num)
    # traverse surrounding rows
    for i in range(-1, 2):
        row = r + i
        if row < 0 or row >= gear_neighbor_map.shape[0]:
            # skip wrap-arounds
            continue
        # traverse surrounding columns (of the number)
        for j in range(-1, num_length + 1):
            col = c_start + j
            if col < 0 or col >= gear_neighbor_map.shape[1]:
                # skip wrap-arounds
                continue
            # add number as a neighbor to the current cell
            gear_neighbor_map[row, col].append(int(num))

    return gear_neighbor_map


def mark_gear_areas(input, engine_map):
    # NxNx1 array keeping track of which numbers are neighboring each cell
    gear_neighbor_map = np.empty(engine_map.shape, dtype=object)
    # each cell is represented by a list containing neighboring numbers
    for i in np.ndindex(gear_neighbor_map.shape): gear_neighbor_map[i] = []

    r = 0
    for row in input:
        for number_match in re.finditer(PART_NUMBER_PATTERN, row):
            c_start, c_end = number_match.span()
            num = number_match.group()
            # mark all neighboring cells by appending the number found to their lists
            gear_neighbor_map = mark_neighbor_nums(gear_neighbor_map, r, c_start, num)

        r += 1
    return gear_neighbor_map


def get_gear_ratio_sum(input, engine_map):
    gear_neighbor_map = mark_gear_areas(input, engine_map)
    gear_ratio_sum = 0

    r = 0
    for row in tqdm(input):
        for gear_match in re.finditer(GEAR_PATTERN, row):
            c = gear_match.start()
            # the gear is valid if surrounded by exactly 2 part numbers
            if len(gear_neighbor_map[r, c]) == 2:
                # add its gear ratio to the total sum
                num1 = gear_neighbor_map[r, c][0]
                num2 = gear_neighbor_map[r, c][1]
                gear_ratio = num1 * num2
                gear_ratio_sum += gear_ratio
        r += 1

    return gear_ratio_sum


def solve(input, part):
    # NxNx1 string array of the engine map
    engine_map = preprocess_input(input)
    # Part 1: Find the sum of all the valid part numbers
    # Part 2: Find the sum of all gear ratios, i.e. '*'-symbols with exactly 2 neighboring part numbers
    solution = get_part_num_sum(input, engine_map) if part == 1 else get_gear_ratio_sum(input, engine_map)
    return solution


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
