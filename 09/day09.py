import sys
import os
import numpy as np

os.environ["TQDM_COLOUR"] = "#33ffaa"
from tqdm import tqdm, trange

DAY = 9


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
    num_histories = len(input)
    oasis_histories = [0] * num_histories
    for i in range(num_histories):
        oasis_histories[i] = [int(x) for x in input[i].split()]
    longest_sequence = max(oasis_histories, key=lambda h: len(h))
    histories = np.zeros((num_histories, 10 ** 4, len(longest_sequence)), dtype=int)
    for i in range(num_histories):
        histories[i, 0, :] = oasis_histories[i]
    return histories


def solve(input, part):
    histories = preprocess_input(input)
    extrapolated_vals = np.zeros(histories.shape[0], dtype=int)
    end_vals = [0] * histories.shape[1]
    # process one history at a time
    for h in trange(histories.shape[0]):
        is_all_zero = False
        i = 0
        h_length = histories.shape[2]
        h_offset = 0
        while not is_all_zero:
            should_look_back = i % 2 == 1
            for j in range(h_offset, h_length - 1):
                first_val = histories[h, i, j] if should_look_back else histories[h, i, j + 1]
                second_val = histories[h, i, j - 1] if should_look_back else histories[h, i, j]
                histories[h, i + 1, j] = first_val - second_val

            i += 1
            # save the last/first (part 1/2) value of the iteration for extrapolation
            end_val = histories[h, i, h_length - 2] if part == 1 else histories[h, i, h_offset]
            end_vals[i] = end_val
            # decrease the window size, every other time at front and back
            h_length = h_length - 1 if should_look_back else h_length
            h_offset = h_offset + 1 if not should_look_back else h_offset
            # no non-zero values => True
            is_all_zero = not np.any(histories[h, i, :])

        # find the next/previous value in the first iteration of the history
        if part == 1:
            diff_to_step = np.sum(end_vals[:i])
            extrapolated_vals[h] = histories[h, 0, -1] + diff_to_step
        if part == 2:
            end_vals[0] = histories[h, 0, 0]
            t2 = 0
            t1 = end_vals[i]
            for k in range(i, 0, -1):
                t3 = t1 - t2
                t2 = t3
                t1 = end_vals[k - 1]
            extrapolated_vals[h] = t1 - t2

    return np.sum(extrapolated_vals)


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
if __name__ == "__main__":
    part = 1
    use_example_input = False
    if len(sys.argv) > 1:
        part = int(sys.argv[1])
        if len(sys.argv) > 2:
            use_example_input = not int(sys.argv[2]) == 0
    input = read_input(use_example_input)
    solution = solve(input, part)
    print('Solution:')
    print(solution)
