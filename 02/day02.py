import sys
import re
import numpy as np

DAY = 2

ROUNDS_KEY = 'rounds'
GAME_ID_KEY = 'game_id'

RED_MAX = 12
GREEN_MAX = 13
BLUE_MAX = 14


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


def preprocess_games(games):
    i = 0
    for g in games:
        g = g.split(': ')[1]
        g = g.split('; ')
        games[i] = format_rounds(g, i + 1)
        i += 1
    return games


def format_rounds(rounds, game_id):
    i = 0
    game = dict()
    for r in rounds:
        cubes = re.findall("([0-9]+) (g(?=reen)|r(?=ed)|b(?=lue))", r)
        colors = {c[1]: c[0] for c in cubes}
        rounds[i] = colors
        i += 1
    game[GAME_ID_KEY] = game_id
    game[ROUNDS_KEY] = rounds
    return game


def get_color_counts(r):
    try:
        red = int(r['r'])
    except KeyError:
        red = 0
    try:
        green = int(r['g'])
    except KeyError:
        green = 0
    try:
        blue = int(r['b'])
    except KeyError:
        blue = 0
    return red, green, blue


# Part 1
def get_valid_games_sum(games):
    valid_games = np.ones(len(games), dtype=bool)
    valid_id_sum = 0
    i = 0
    for g in games:
        rounds = g[ROUNDS_KEY]
        for r in rounds:
            red, green, blue = get_color_counts(r)
            if red > RED_MAX or green > GREEN_MAX or blue > BLUE_MAX:
                valid_games[i] = False  # hm?
        if valid_games[i]:
            valid_id_sum += g[GAME_ID_KEY]
        i += 1

    return valid_id_sum


# Part 2
def get_cubes_powersum(games):
    i = 0
    powers = np.zeros(len(games))
    for g in games:
        fewest = {'r': 0, 'g': 0, 'b': 0}
        rounds = g[ROUNDS_KEY]
        for r in rounds:
            red, green, blue = get_color_counts(r)
            fewest['r'] = max(fewest['r'], red)
            fewest['g'] = max(fewest['g'], green)
            fewest['b'] = max(fewest['b'], blue)
        powers[i] = fewest['r'] * fewest['g'] * fewest['b']
        i += 1

    return int(np.sum(powers))


def solve(input, part):
    games = preprocess_games(input)
    solution = get_valid_games_sum(games) if part == 1 else get_cubes_powersum(games)
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
