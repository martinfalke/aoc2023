import sys
import os
from math import inf

os.environ["TQDM_COLOUR"] = "#33ffaa"
from tqdm import tqdm

DAY = 5


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
    i = 3  # first mapping starts on line 3
    seeds = [int(x) for x in input[0].split()[1:]]
    seed2soil, i = parse_mapping_ranges(input[i:], i)
    soil2fert, i = parse_mapping_ranges(input[i:], i)
    fert2water, i = parse_mapping_ranges(input[i:], i)
    water2light, i = parse_mapping_ranges(input[i:], i)
    light2temp, i = parse_mapping_ranges(input[i:], i)
    temp2humidity, i = parse_mapping_ranges(input[i:], i)
    humidity2loc, i = parse_mapping_ranges(input[i:], i)

    return seeds, seed2soil, soil2fert, fert2water, water2light, light2temp, temp2humidity, humidity2loc


def parse_mapping_ranges(subinput, i):
    mapping = []
    for line in subinput:
        if line.strip() == "":
            # empty line, current mapping done
            break
        dest, src, l = tuple([int(x) for x in line.split()])
        mapping_range = {"src_min": src, "src_max": src + l - 1, "dest_min": dest}
        mapping.append(mapping_range)
        i += 1

    return mapping, i + 2


def get_tmp_min_location(seeds, mappings):
    min_loc = inf
    for seed in tqdm(seeds, desc="Seeds processed:"):
        tmp = seed  # value being mapped
        for mapping in mappings:
            for mapping_range in mapping:
                src_min = mapping_range["src_min"]
                src_max = mapping_range["src_max"]
                dest_min = mapping_range["dest_min"]
                offset = dest_min - src_min
                if src_min <= tmp <= src_max:
                    # translate to dest
                    tmp = tmp + offset
                    break
                # if the src value is not within a specific range, keep it as is
        if tmp < min_loc:
            min_loc = tmp

    return min_loc


# Part 2
def parse_seed_ranges(seed_pairs):
    assert len(seed_pairs) % 2 == 0  # seed ranges come in pairs of integers
    num_seed_pairs = len(seed_pairs) // 2
    seed_ranges = [{}] * num_seed_pairs
    i = 0
    for j in range(num_seed_pairs):
        assert i + 1 < len(seed_pairs)
        range_start = seed_pairs[i]
        range_length = seed_pairs[i + 1]
        range_end = range_start + range_length - 1
        seed_range = {"tmp_min": range_start, "tmp_max": range_end}
        seed_ranges[j] = seed_range
        assert isinstance(seed_ranges[j]["tmp_min"], int)
        assert isinstance(seed_ranges[j]["tmp_max"], int)
        i += 2
    return seed_ranges


def split_range_on_min(tmp_min, src_min):
    split_min = tmp_min
    split_max = src_min - 1
    split_range = {"tmp_min": split_min, "tmp_max": split_max}
    tmp_min = src_min
    return tmp_min, split_range


def split_range_on_max(tmp_max, src_max):
    split_min = src_max + 1
    split_max = tmp_max
    split_range = {"tmp_min": split_min, "tmp_max": split_max}
    tmp_max = src_max
    return tmp_max, split_range


def get_seed_ranges_min_location(seed_ranges, mappings):
    translated_ranges = seed_ranges.copy()
    for mapping in mappings:
        tmp_ranges = translated_ranges
        num_tmp_ranges = len(tmp_ranges)
        translated_ranges = []
        i = 0
        while i < num_tmp_ranges:
            tmp_range = tmp_ranges[i]
            tmp_min = tmp_range["tmp_min"]
            tmp_max = tmp_range["tmp_max"]

            for mapping_range in mapping:
                src_min = mapping_range["src_min"]
                src_max = mapping_range["src_max"]

                # Check for mapping range being too low
                if tmp_min > src_max or tmp_max < src_min:
                    # the translation range starts at a higher mapping range
                    # skip current mapping range
                    continue

                # Check for overlaps on low end of the mapping range
                overlaps_min = tmp_max >= src_min > tmp_min
                if overlaps_min:
                    # split the part that is less than the mapping into a separate range
                    # keep the part that fully overlaps with the mapping
                    tmp_min, split_range = split_range_on_min(tmp_min, src_min)
                    tmp_ranges[i]["tmp_min"] = tmp_min
                    tmp_ranges.append(split_range)
                    num_tmp_ranges += 1

                # Check for overlaps on high end of the mapping range
                overlaps_max = tmp_min <= src_max < tmp_max
                if overlaps_max:
                    # split the part greater than the mapping into a separate range
                    # keep the part that fully overlaps with the mapping
                    tmp_max, split_range = split_range_on_max(tmp_max, src_max)
                    tmp_ranges[i]["tmp_max"] = tmp_max
                    tmp_ranges.append(split_range)
                    num_tmp_ranges += 1

                is_contained = tmp_max <= src_max and tmp_min >= src_min
                if is_contained:
                    # Translation from src to dest using current mapping range
                    dest_min = mapping_range["dest_min"]
                    offset = dest_min - src_min
                    tmp_ranges[i]["tmp_min"] = tmp_min + offset
                    tmp_ranges[i]["tmp_max"] = tmp_max + offset
                    break

            # range was either translated or kept as is (not found within any mapping range)
            translated_ranges.append(tmp_ranges[i])
            i += 1
    min_loc = min(translated_ranges, key=lambda r: r["tmp_min"])["tmp_min"]
    return min_loc


def solve(input, part):
    seeds, seed2soil, soil2fert, fert2water, water2light, light2temp, temp2humidity, humidity2loc = preprocess_input(
        input)
    mappings = [seed2soil, soil2fert, fert2water, water2light, light2temp, temp2humidity, humidity2loc]
    if part == 1:
        min_loc = get_tmp_min_location(seeds, mappings)
    else:  # part 2
        seed_ranges = parse_seed_ranges(seeds)
        min_loc = get_seed_ranges_min_location(seed_ranges, mappings)
    return min_loc


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
