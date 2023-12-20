import sys
import os

os.environ["TQDM_COLOUR"] = "#33ffaa"
from tqdm import tqdm, trange

DAY = 13

ASCII_OFFSET = 32
ROW_FACTOR = 100
COL_FACTOR = 1
ENCODE_BASE = 16


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
    num_patterns = 1
    for i in range(len(input)):
        if input[i] == "":
            num_patterns += 1
    patterns_rows = [[] for _ in range(num_patterns)]
    patterns_columns = [[] for _ in range(num_patterns)]
    p = 0
    # add all patterns in separate lists
    # each pattern represented by a list of strings (rows)
    for i in range(len(input)):
        if input[i] == "":
            p += 1
            continue
        patterns_rows[p].append(input[i])
    # add all patterns read vertically in separate lists
    # each pattern represented by a list of strings (columns)
    for p in range(num_patterns):
        assert len(max(patterns_rows[p])) == len(min(patterns_rows[p]))
        pattern_width = len(patterns_rows[p][0])
        pattern_height = len(patterns_rows[p])
        patterns_columns[p] = ['' for _ in range(pattern_width)]
        for j in range(pattern_width):
            for i in range(pattern_height):
                patterns_columns[p][j] += patterns_rows[p][i][j]

    for p in range(num_patterns):
        pattern_width = len(patterns_columns[p])
        pattern_height = len(patterns_rows[p])
        # for every row, encode it as a sum based on its ASCII representation
        for y in range(pattern_height):
            pattern_row = patterns_rows[p][y]
            patterns_rows[p][y] = 0
            # convert each character to an ASCII int and add to the row sum
            # offset ASCII values to get a smaller base
            # use column index x as exponent of 16 for base16-encoded columns
            for x in range(pattern_width):
                patterns_rows[p][y] += (ord(pattern_row[x]) - ASCII_OFFSET) * ENCODE_BASE ** x

        # for every column, encode it as a sum based on its ASCII representation
        for x in range(pattern_width):
            pattern_col = patterns_columns[p][x]
            patterns_columns[p][x] = 0
            # convert each character to an ASCII int and add to the column sum
            for y in range(pattern_height):
                patterns_columns[p][x] += (ord(pattern_col[y]) - ASCII_OFFSET) * ENCODE_BASE ** y

    return patterns_rows, patterns_columns


def get_pattern_reflections(pattern_axis, part, transposed_length):
    reflection_skips = 0
    axis_length = len(pattern_axis)
    smudge_offset = 0
    for offset in range(1, axis_length):
        reflection_length = offset if offset < (axis_length + 1) // 2 else axis_length - offset
        k1 = offset - 1
        k2 = offset
        has_reflection = True
        has_one_smudge = False
        for k in range(reflection_length):
            # for part 1 -
            # check that each pair of vectors at equal distance from
            # the reference line between k1 and k2 are identical
            if part == 1:
                if pattern_axis[k1 - k] != pattern_axis[k2 + k]:
                    has_reflection = False
                    break
            # for part 2 -
            # check that each pair of vectors at equal distance from
            # the reference line between k1 and k2 has exactly one symbol that is different
            else:  # part == 2
                i1 = k1 - k
                i2 = k2 + k
                # if exactly one symbol differs, the encoded sum will differ by exactly
                # the difference between a '.' and a '#' in one of their offset base16-encoded form
                vector_distance = abs(pattern_axis[i1] - pattern_axis[i2])
                dot_hex = ord('.') - ASCII_OFFSET
                pound_hex = ord('#') - ASCII_OFFSET
                dot_diffs = [dot_hex * ENCODE_BASE ** i for i in range(transposed_length)]
                pound_diffs = [pound_hex * ENCODE_BASE ** i for i in range(transposed_length)]
                smudge_diffs = [abs(pound_diffs[i] - dot_diffs[i]) for i in range(transposed_length)]
                if vector_distance in smudge_diffs:
                    # smudge found
                    smudge_offset = offset
                    if has_one_smudge:
                        has_reflection = False
                        break
                    else:
                        has_one_smudge = True
                # when smudge isn't found, invalidate the reflection if one pair does not match
                elif pattern_axis[i1] != pattern_axis[i2]:
                    has_reflection = False
        if has_reflection and part == 1:
            reflection_skips = offset
            break
        if has_reflection and has_one_smudge and part == 2:
            reflection_skips = smudge_offset

    return reflection_skips


def get_reflection_values(patterns_rows, patterns_columns, part):
    assert len(patterns_rows) == len(patterns_columns)
    num_patterns = len(patterns_rows)
    reflection_values = [0] * num_patterns

    for p in range(num_patterns):
        pattern_columns = patterns_columns[p]
        pattern_rows = patterns_rows[p]
        row_length = len(pattern_columns)  # rows are as long as there are number of columns
        col_length = len(pattern_rows)  # columns are as long as there are number of rows
        reflection_rows = get_pattern_reflections(pattern_rows, part, row_length)
        reflection_cols = get_pattern_reflections(pattern_columns, part, col_length)
        reflection_values[p] = reflection_rows * ROW_FACTOR + reflection_cols * COL_FACTOR

    return reflection_values


def solve(input, part):
    patterns_rows, patterns_columns = preprocess_input(input)
    reflection_values = get_reflection_values(patterns_rows, patterns_columns, part)
    print(reflection_values)
    reflection_sum = sum(reflection_values)

    return reflection_sum


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
