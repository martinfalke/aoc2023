import sys
import os
import numpy as np

os.environ["TQDM_COLOUR"] = "#33ffaa"
from tqdm import tqdm, trange

DAY = 11


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


# Part 1
def preprocess_input(input):
    y_length = len(input)
    x_length = len(input[0])
    space_map = np.ndarray((y_length, x_length), dtype=object)
    for y in range(y_length):
        line = input[y]
        for x in range(x_length):
            space_map[y, x] = line[x]

    # double up every row with no galaxies
    new_y = y_length
    y = 0
    while y < new_y:
        row = space_map[y, :]
        has_no_galaxies = np.all(list(map(lambda p: 0 if p == '#' else 1, row)))
        if has_no_galaxies:
            new_y += 1
            space_map = np.insert(space_map, y, values=row.copy(), axis=0).reshape(new_y, x_length)
            y += 2
        else:
            y += 1

    # double up every column with no galaxies
    new_x = x_length
    x = 0
    while x < new_x:
        column = space_map[:, x]
        has_no_galaxies = np.all(list(map(lambda p: 0 if p == '#' else 1, column)))
        if has_no_galaxies:
            new_x += 1
            space_map = np.insert(space_map, x, values=column.copy(), axis=1).reshape(new_y, new_x)
            x += 2
        else:
            x += 1

    # get locations of galaxies
    galaxy_locs = []
    for y in range(new_y):
        for x in range(new_x):
            if space_map[y, x] == '#':
                galaxy_locs.append((y, x))
    num_galaxies = len(galaxy_locs)

    # create pairs of galaxies
    # i = current galaxy g1
    # j = current galaxy g2
    galaxy_pairs = []
    for i in range(num_galaxies):
        for j in range(i + 1, num_galaxies):
            galaxy_pairs.append((i, j))

    return space_map, galaxy_locs, galaxy_pairs


# Part 2
def preprocess_input_part2(input):
    y_length = len(input)
    x_length = len(input[0])
    space_map = np.ndarray((y_length, x_length), dtype=object)
    for y in range(y_length):
        line = input[y]
        for x in range(x_length):
            space_map[y, x] = line[x]

    # each non-galaxy row/column should count as 1 000 000 empty ones
    extra_spacing = 10 ** 6

    # add extra spacing for every row with no galaxies
    row_spacing = np.ones((y_length), dtype=int)
    y = 0
    while y < y_length:
        row = space_map[y, :]
        has_no_galaxies = np.all(list(map(lambda p: 0 if p == '#' else 1, row)))
        if has_no_galaxies:
            row_spacing[y] = extra_spacing
        y += 1

    # add extra spacing for every column with no galaxies
    x = 0
    column_spacing = np.ones(x_length, dtype=int)
    while x < x_length:
        column = space_map[:, x]
        has_no_galaxies = np.all(list(map(lambda p: 0 if p == '#' else 1, column)))
        if has_no_galaxies:
            column_spacing[x] = extra_spacing
        x += 1

    # get locations of galaxies
    galaxy_locs = []
    for y in range(y_length):
        for x in range(x_length):
            if space_map[y, x] == '#':
                galaxy_locs.append((y, x))
    num_galaxies = len(galaxy_locs)

    # create pairs of galaxies
    # i = current galaxy g1
    # j = current galaxy g2
    galaxy_pairs = []
    for i in range(num_galaxies):
        for j in range(i + 1, num_galaxies):
            galaxy_pairs.append((i, j))

    return space_map, galaxy_locs, galaxy_pairs, row_spacing, column_spacing


# Part 1
def get_shortest_galaxy_pair_path(g1_loc, g2_loc):
    return abs(g2_loc[0] - g1_loc[0]) + abs(g2_loc[1] - g1_loc[1])


def get_shortest_galaxy_paths(galaxy_locs, galaxy_pairs, row_spacing=None, column_spacing=None):
    shortest_paths = []
    for g1, g2 in galaxy_pairs:
        g1_loc = galaxy_locs[g1]
        g2_loc = galaxy_locs[g2]
        if row_spacing is None or column_spacing is None:
            # Part 1
            shortest_path = get_shortest_galaxy_pair_path(g1_loc, g2_loc)
        else:
            # Part 2
            shortest_path = get_shortest_galaxy_pair_path_part2(g1_loc, g2_loc, row_spacing, column_spacing)
        shortest_paths.append(shortest_path)
    return shortest_paths


# Part 2
def get_shortest_galaxy_pair_path_part2(g1_loc, g2_loc, row_spacing, column_spacing):
    y1, x1 = g1_loc
    y2, x2 = g2_loc
    traveled_rows = row_spacing[y1:y2] if y1 < y2 else row_spacing[y2:y1]
    traveled_columns = column_spacing[x1:x2] if x1 < x2 else column_spacing[x2:x1]
    # sum up the spacings between y1 -> y2 and x1 -> x2
    shortest_pair_path = np.sum(traveled_rows) + np.sum(traveled_columns)
    return shortest_pair_path


def solve(input, part):
    galaxy_paths = []
    if part == 1:
        space_map, galaxy_locs, galaxy_pairs = preprocess_input(input)
        galaxy_paths = get_shortest_galaxy_paths(galaxy_locs, galaxy_pairs)
    if part == 2:
        space_map, galaxy_locs, galaxy_pairs, row_spacing, column_spacing = preprocess_input_part2(input)
        galaxy_paths = get_shortest_galaxy_paths(galaxy_locs, galaxy_pairs, row_spacing, column_spacing)

    solution = np.sum(galaxy_paths)
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
