import sys
import os
import re
from math import gcd

os.environ["TQDM_COLOUR"] = "#33ffaa"
from tqdm import trange

DAY = 8


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
    # encode direction L=0, R=1 to use as tuple indices
    directions = [0 if direction == 'L' else 1 for direction in input[0]]
    locations = {}
    for loc in input[2:]:
        start = re.search("^(\w+)", loc).group()
        left = re.search("(\w+)(?=, )", loc).group()
        right = re.search("(\w+)(?=\))", loc).group()
        locations[start] = (left, right)
    return directions, locations


# Part 2
def get_starts(locations):
    locations = " ".join(locations.keys())
    starts = re.findall("\w{2}A", locations)
    return starts


def is_destination(pos):
    return pos[-1] == 'Z'


def get_trips_lcm(trip_lengths):
    lcm = 1
    for tl in trip_lengths:
        lcm = lcm * tl // gcd(lcm, tl)
    return lcm


def solve(input, part):
    directions, locations = preprocess_input(input)
    direction_index = 0
    steps = 0
    if part == 1:
        start = "AAA"
        destination = "ZZZ"
        pos = start
        while pos != destination:
            direction = directions[direction_index]
            pos = locations[pos][direction]
            steps += 1
            direction_index = (direction_index + 1) % len(directions)
    else:  # Part 2
        starts = get_starts(locations)
        trip_lengths = [0] * len(starts)
        for i in trange(len(starts)):
            p = starts[i]
            direction_index = 0
            steps = 0
            # find the lengths of each starting point's
            # shortest trip to a valid destination
            while not is_destination(p):
                direction = directions[direction_index]
                p = locations[p][direction]
                steps += 1
                direction_index = (direction_index + 1) % len(directions)
            trip_lengths[i] = steps

        # find the least common multiple of all the trip lengths; at this point,
        # all parallel trips will have arrived at a valid destination simultaneously
        lcm = get_trips_lcm(trip_lengths)
        steps = lcm

    return steps


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
