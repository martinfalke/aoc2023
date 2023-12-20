import sys
import os
import re
os.environ["TQDM_COLOUR"] = "#33ffaa"
from tqdm import tqdm, trange

DAY = 15

NUM_BOXES = 256
PUT_OP = '='
REMOVE_OP = '-'

LABEL_KEY = 'label'
OP_KEY = 'op'
BOX_KEY = 'box'
FOCAL_LENGTH_KEY = 'focal_length'
ORDER_KEY = 'order'


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
    sequence = input[0].split(',')
    return sequence


def preprocess_input_part2(input):
    sequence = input[0].split(',')
    steps = [dict() for _ in range(len(sequence))]
    boxes = [dict() for _ in range(NUM_BOXES)]
    for i, subsequence in enumerate(sequence):
        label = re.search("[A-Za-z]+", subsequence).group()
        op = re.search("-|=",subsequence).group()
        step = {LABEL_KEY: label, OP_KEY: op}
        focal_length = re.search("\d+", subsequence)
        if focal_length:
            step[FOCAL_LENGTH_KEY] = int(focal_length.group())

        steps[i] = step
    return steps, boxes


# Part 1
def hash_algo(subsequence, current_value):
    if len(subsequence) == 0:
        return current_value
    next_char = subsequence[0]
    current_value += ord(next_char)
    current_value *= 17
    current_value = current_value % 256
    return hash_algo(subsequence[1:], current_value)


def calc_sequence_hashes(sequence):
    hash_results = [0]*len(sequence)
    for i, subsequence in enumerate(sequence):
        hash_results[i] = hash_algo(subsequence, 0)
    return hash_results


# Part 2
def add_box_numbers(steps, label_hashes):
    for i in range(len(steps)):
        steps[i][BOX_KEY] = label_hashes[i]
    return steps


def set_boxes_lens_config(steps, boxes):
    for s in range(len(steps)):
        step = steps[s]
        op = step[OP_KEY]
        box = boxes[step[BOX_KEY]]
        label = step[LABEL_KEY]
        if op == PUT_OP:
            if label in box:
                order = box[label][ORDER_KEY]
            else:
                order = s
            box[label] = {FOCAL_LENGTH_KEY: step[FOCAL_LENGTH_KEY], ORDER_KEY: order}
        elif op == REMOVE_OP:
            try:
                del box[label]
            except KeyError:
                continue
        else:
            raise KeyError


def calc_focusing_power(boxes):
    focusing_power = 0
    for b in range(len(boxes)):
        box = boxes[b]
        box_power = 0
        box_num = b + 1
        sorted_box = sorted(list(zip(box.keys(), box.values())), key=lambda x: x[1][ORDER_KEY])
        for i in range(len(sorted_box)):
            lens_power = box_num * (i+1) * sorted_box[i][1][FOCAL_LENGTH_KEY]
            box_power += lens_power
        focusing_power += box_power
    return focusing_power


def solve(input, part):
    if part == 1:
        sequence = preprocess_input(input)
        hash_results = calc_sequence_hashes(sequence)
        verification_sum = sum(hash_results)
        solution = verification_sum
    else:
        steps, boxes = preprocess_input_part2(input)
        step_labels = list(map(lambda step: step[LABEL_KEY], steps))
        label_hashes = calc_sequence_hashes(step_labels)
        add_box_numbers(steps, label_hashes)
        set_boxes_lens_config(steps, boxes)
        focusing_power = calc_focusing_power(boxes)
        solution = focusing_power
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
