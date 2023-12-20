import sys
import os
import numpy as np
from functools import reduce
os.environ["TQDM_COLOUR"] = "#33ffaa"
from tqdm import tqdm, trange

DAY = 14

EMPTY_SPACE = b'.'
ROUND_ROCK = b'O'


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
    # create a map that keeps track of what exists at each spot in the map
    y_max = len(input)
    x_max = len(max(input, key=lambda r: len(r)))
    row_map = np.zeros((y_max, x_max), dtype='S1')
    for y in range(y_max):
        row_map[y, :] = list(input[y])
    return row_map


def get_total_load(row_map):
    total_load = 0
    for y in range(len(row_map)):
        row = row_map[y]
        row_magnitude = len(row_map) - y
        rock_row_count = 0
        # count the rocks in the row
        for x in range(len(row)):
            if row[x] == ROUND_ROCK:
                rock_row_count += 1

        row_load = row_magnitude * rock_row_count
        total_load += row_load
    return total_load


def tilt_north(row_map):
    for y in range(len(row_map)):
        for x in range(len(row_map[y])):
            spot = row_map[y, x]
            # skip empty spaces and non-round rocks
            if spot != ROUND_ROCK:
                continue
            row_map[y, x] = EMPTY_SPACE

            # find the next non-empty space
            i = 0
            while y-i >= 0 and row_map[y-i, x] == EMPTY_SPACE:
                i += 1
            new_y = y-i+1
            # move the round rock to new position
            row_map[new_y, x] = ROUND_ROCK


# Part 2
def tilt_west(row_map):
    for x in range(len(row_map[0])):
        for y in range(len(row_map)):
            spot = row_map[y, x]
            # skip empty spaces and non-round rocks
            if spot != ROUND_ROCK:
                continue
            row_map[y, x] = EMPTY_SPACE

            # find the next non-empty space
            i = 0
            while x-i >= 0 and row_map[y, x-i] == EMPTY_SPACE:
                i += 1
            new_x = x-i+1
            # move the round rock to new position
            row_map[y, new_x] = ROUND_ROCK


def tilt_south(row_map):
    for y in range(len(row_map)-1, -1, -1):
        for x in range(len(row_map[y])):
            spot = row_map[y, x]
            # skip empty spaces and non-round rocks
            if spot != ROUND_ROCK:
                continue

            # find the next non-empty space
            row_map[y, x] = EMPTY_SPACE
            i = 0
            while y+i < len(row_map[:, x]) and row_map[y+i, x] == EMPTY_SPACE:
                i += 1
            new_y = y+i-1
            # move the round rock to new position
            row_map[new_y, x] = ROUND_ROCK


def tilt_east(row_map):
    for x in range(len(row_map[0])-1, -1, -1):
        for y in range(len(row_map)):
            spot = row_map[y, x]
            # skip empty spaces and non-round rocks
            if spot != ROUND_ROCK:
                continue
            row_map[y, x] = EMPTY_SPACE

            # find the next non-empty space
            i = 0
            while x+i < len(row_map[y]) and row_map[y, x+i] == EMPTY_SPACE:
                i += 1
            new_x = x+i-1
            # move the round rock to new position
            row_map[y, new_x] = ROUND_ROCK
    return row_map


def get_cache_key(row_map):
    return reduce(lambda t, c: t + c, row_map.flat)


def cache_key_to_row_map(cache_key, shape):
    row_map = np.zeros(shape, dtype='S1')
    y_max = shape[0]
    x_max = shape[1]
    # split the byte-array from cache into rows
    for y in range(y_max):
        start = x_max*y
        end = start+x_max
        row = cache_key[start:end]
        if len(row) == 0:
            break
        row_map[y, :] = list(row.decode())
    return row_map


def solve(input, part):
    row_map = preprocess_input(input)
    if part == 1:
        tilt_north(row_map)
    else:
        # Part 2
        num_cycles = 10**9
        cycle_cache = dict()
        c = 0
        while c < num_cycles:
            cache_key = get_cache_key(row_map)
            if cache_key in cycle_cache:
                # cache hit - calculate how many cycles can be skipped with the periodicity
                # that forms with the previous cycle where the map had the same state
                cached_c = cycle_cache[cache_key]['c']
                periodicity = c - cached_c
                remaining_cycles = num_cycles - c
                new_c = num_cycles - (remaining_cycles % periodicity) + 1
                # restore the state of the map from after the cycle and move to the final identical cycle no.
                row_map = cache_key_to_row_map(cycle_cache[cache_key]['row_map'], row_map.shape)
                c = new_c
                continue

            # perform the tilt cycle
            tilt_north(row_map)
            tilt_west(row_map)
            tilt_south(row_map)
            tilt_east(row_map)
            # save this cycle's state to cache
            if cache_key not in cycle_cache:
                cycle_cache[cache_key] = dict()
            cycle_cache[cache_key]['c'] = c
            # save the state of the map after the cycle
            cycle_cache[cache_key]['row_map'] = get_cache_key(row_map)
            c += 1

    # calculate the load on the northern support beams after all tilting is completed
    load = get_total_load(row_map)
    return load


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
