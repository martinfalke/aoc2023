import sys
import os
import re
from itertools import chain
from functools import lru_cache
from multiprocessing import Pool

os.environ["TQDM_COLOUR"] = "#33ffaa"
from tqdm import tqdm, trange

DAY = 12
DAMAGED_SPRING = '#'
OPERATIONAL_SPRING = '.'
UNKNOWN_SPRING = '?'
OPEN_BRACE_CHAR = '{'
CLOSE_BRACE_CHAR = '}'
pattern_memo = {}


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
    spring_rows = []
    damaged_counts = []
    for line in input:
        spring_row = re.search("([\?#\.]+)", line).group()
        spring_rows.append(spring_row)
        damaged_counts_row = re.search("(?<= )(\d.*)", line).group()
        damaged_counts_row = tuple([int(x) for x in damaged_counts_row.split(',')])
        damaged_counts.append(damaged_counts_row)

    return spring_rows, damaged_counts


# Part 1
def surpassed_counts(row, index, combination, counts, damaged_streak):
    all_damaged_groups = re.findall(f'(?<!{DAMAGED_SPRING}){DAMAGED_SPRING}+(?=[^{DAMAGED_SPRING}]|$)', combination)
    if len(all_damaged_groups) > len(counts):
        return True
    for i in range(len(all_damaged_groups)):
        if len(all_damaged_groups[i]) > counts[i]:
            return True
    return False


def get_all_possible_combinations(row, index, combination, counts, damaged_streak):
    # if we have already surpassed the allowed counts, prune the entire subtree of recursion
    if damaged_streak > 1 and surpassed_counts(row, index, combination, counts, damaged_streak):
        return []
    if index == len(row):
        return [combination]

    c = row[index]
    # if the next character is an unknown: recurse both options for it
    if c == UNKNOWN_SPRING:
        combinations_chain = chain(
            get_all_possible_combinations(row, index + 1, combination + OPERATIONAL_SPRING, counts, 0),
            get_all_possible_combinations(row, index + 1, combination + DAMAGED_SPRING, counts, damaged_streak + 1)
        )
    else:
        if c == DAMAGED_SPRING:
            combinations_chain = get_all_possible_combinations(row, index + 1, combination + c, counts,
                                                               damaged_streak + 1)
        else:
            if damaged_streak > 0 and surpassed_counts(row, index, combination, counts, damaged_streak):
                return []
            combinations_chain = get_all_possible_combinations(row, index + 1, combination + c, counts, 0)
    return combinations_chain


def is_valid_combination(combination, row_damaged_counts):
    patterns = {}
    for count in row_damaged_counts:
        if not count in patterns:
            pattern_string = f'^[^{DAMAGED_SPRING}]*[{DAMAGED_SPRING}]{OPEN_BRACE_CHAR}{count}{CLOSE_BRACE_CHAR}(?=[^{DAMAGED_SPRING}]|$)'
            patterns[count] = re.compile(pattern_string)
        match = re.search(patterns[count], combination)
        if not match:
            return False
        end = match.end()
        combination = combination[end:len(combination)]
    if re.search("#", combination):
        return False

    return True


def get_num_valid_combinations_row(combinations, row_damaged_counts):
    num_valid_combinations_row = 0
    for combination in combinations:
        if is_valid_combination(combination, row_damaged_counts):
            num_valid_combinations_row += 1
    return num_valid_combinations_row


# Part 1
def calculate_num_valid_arrangements_parallel_brute(worker_id, num_workers, spring_rows, damaged_counts):
    partial_num_valid_combinations = 0
    for i in range(worker_id, len(spring_rows), num_workers):
        row = spring_rows[i]
        counts = damaged_counts[i]
        possible_combinations = list(get_all_possible_combinations(row, 0, "", counts, 0))
        partial_num_valid_combinations += get_num_valid_combinations_row(possible_combinations, counts)
    return partial_num_valid_combinations


# Part 2
# limit cache use to 1000 function calls - larger caches takes longer to confirm hits/misses
@lru_cache(maxsize=1000)
def get_num_valid_combinations_row_cache(remaining_row, counts):
    num_valid = 0

    # nothing more to process but there are damaged counts left unprocessed
    # meaning too few damaged springs - combination is invalid
    if len(remaining_row) == 0 and len(counts) > 0:
        return 0
    # there are no more counts, and there are no more damaged springs
    # remaining unknown springs will count as operational and any number
    # of operational springs yield a valid combination
    if len(counts) == 0 and DAMAGED_SPRING not in remaining_row:
        return 1
    # there are no more counts, but there are more damaged springs
    # that have not been processed - combination is invalid
    elif len(counts) == 0:
        return 0

    def unknown_next():
        # Sum valid combinations from both options
        return damaged_next() + operational_next()

    def damaged_next():
        # The following characters must be as many damaged as the next count
        # and all unknown springs can be replaced with damaged ones to match
        # the count that is sought
        current_chunk = remaining_row[:next_count]
        current_chunk = current_chunk.replace(UNKNOWN_SPRING, DAMAGED_SPRING)
        # Not all the characters in the current chunk are matching what is
        # required for the count to be valid - combination is invalid
        next_chunk = DAMAGED_SPRING * next_count
        if current_chunk != next_chunk:
            return 0

        # If the current chunk covers the entirety of the rest of the row,
        # the combination is valid if and only it is the last chunk, i.e. there
        # are no more counts. If there are more counts, there are no more springs
        # to create the remaining chunks - combination is invalid
        if len(remaining_row) == len(current_chunk):
            if len(counts) == 1:
                return 1
            else:
                return 0

        # The next spring that occurs after the current chunk needs to separate
        # the current chunk from the rest of the row, i.e. be unknown or operational
        # If the next spring is not damaged, the count is respected - combination still valid
        # To ensure the next spring acts as an operational, respecting the count, skip it for
        # the next recursion
        following_spring = remaining_row[next_count]
        if following_spring != DAMAGED_SPRING:
            return get_num_valid_combinations_row_cache(remaining_row[next_count + 1:], counts[1:])

        # Missed all validity checks - all remaining combinations are invalid
        return 0

    def operational_next():
        # Operational springs do not need to match any count and can be ignored
        return get_num_valid_combinations_row_cache(remaining_row[1:], counts)

    next_spring = remaining_row[0]
    next_count = counts[0]
    if next_spring == UNKNOWN_SPRING:
        num_valid += unknown_next()
    elif next_spring == DAMAGED_SPRING:
        num_valid += damaged_next()
    elif next_spring == OPERATIONAL_SPRING:
        num_valid += operational_next()
    else:
        raise KeyError
    return num_valid


def get_num_valid_arrangements_cache(spring_rows, damaged_counts):
    num_valid_combinations = 0
    for i in trange(len(spring_rows)):
        row = spring_rows[i]
        counts = damaged_counts[i]
        num_valid_combinations += get_num_valid_combinations_row_cache(row, counts)

    return [num_valid_combinations]


def get_num_valid_combinations(spring_rows, damaged_counts, part):
    num_workers = 8
    with Pool(processes=num_workers) as pool:
        args = []
        for i in range(num_workers):
            args.append((i, num_workers, spring_rows, damaged_counts))
        # split the workload into `num_workers` pieces
        # each worker reads different rows from the input and calculates their partial sum
        if part == 1:
            results = pool.starmap(calculate_num_valid_arrangements_parallel_brute, args)
        else:  # Part 2
            results = get_num_valid_arrangements_cache(spring_rows, damaged_counts)
    sum_num_valid_combinations = sum(results)
    return sum_num_valid_combinations


# Part 2
def unfold_input(spring_rows, damaged_counts, multiplier=5):
    for i in range(len(spring_rows)):
        spring_rows[i] = '?'.join([spring_rows[i]] * multiplier)
        damaged_counts[i] = damaged_counts[i] * multiplier
    return spring_rows, damaged_counts


def solve(input, part):
    spring_rows, damaged_counts = preprocess_input(input)
    if part == 2:
        spring_rows, damaged_counts = unfold_input(spring_rows, damaged_counts)
    # get the sum of the number of all valid arrangements for every row
    solution = get_num_valid_combinations(spring_rows, damaged_counts, part)

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
