import sys
import os
from functools import reduce
from math import inf

os.environ["TQDM_COLOUR"] = "#33ffaa"
from tqdm import trange

DAY = 6


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
def preprocess_input_part1(input):
    times = [int(x) for x in input[0].split()[1:]]
    distances = [int(x) for x in input[1].split()[1:]]
    return times, distances


def get_num_ways_to_win(time, distance):
    win_min = inf
    win_max = 0
    for t in trange(time):
        speed = t
        d = speed * (time - t)
        if d > distance:
            win_min = t
            break
    for t in trange(time, -1, -1):
        speed = t
        d = speed * (time - t)
        if d > distance:
            win_max = t
            break
    n = win_max - win_min + 1
    return n


def get_total_num_ways_to_win(times, distances):
    races = [0] * len(times)
    margin_product = 1
    for race in range(len(races)):
        num_winning_ways = get_num_ways_to_win(times[race], distances[race])
        races[race] = num_winning_ways
        margin_product *= num_winning_ways
    return margin_product


# Part 2
def preprocess_input_part2(input):
    time = int(reduce(lambda t, s: t + s, input[0].split()[1:], ""))
    distance = int(reduce(lambda t, s: t + s, input[1].split()[1:], ""))
    return time, distance


def solve(input, part):
    if part == 1:
        times, distances = preprocess_input_part1(input)
        solution = get_total_num_ways_to_win(times, distances)
    else:
        time, distance = preprocess_input_part2(input)
        solution = get_num_ways_to_win(time, distance)

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
