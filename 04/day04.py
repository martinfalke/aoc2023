import sys
import os
import numpy as np

os.environ["TQDM_COLOUR"] = "#33ffaa"
from tqdm import trange

DAY = 4


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


def preprocess_cards(input):
    # set up lists of lists, containing the winning/own numbers
    winning_numbers = np.empty(len(input), dtype=object)
    for i in np.ndindex(winning_numbers.shape): winning_numbers[i] = []
    candidate_numbers = np.empty(len(input), dtype=object)
    for i in np.ndindex(candidate_numbers.shape): candidate_numbers[i] = []

    i = 0
    for card in input:
        card = card.split(': ')[1]
        card = card.split(' | ')
        # split numbers on whitespace, then convert to ints
        # place all winning/own numbers of each card into a sorted list
        winning_numbers[i] = list(map(lambda x: int(x), card[0].split()))
        winning_numbers[i].sort()
        candidate_numbers[i] = list(map(lambda x: int(x), card[1].split()))
        candidate_numbers[i].sort()
        i += 1
    return winning_numbers, candidate_numbers


def get_card_num_winners(card_winners, card_candidates):
    num_winners = 0  # winners on current card
    for j in range(len(card_candidates)):
        candidate_number = card_candidates[j]
        for k in range(len(card_winners)):
            winning_number = card_winners[k]
            if candidate_number < winning_number:
                # lists are sorted in ascending order, hence the number can't
                # be a winning if it's reached a winner that's greater than itself
                break
            if candidate_number == winning_number:
                num_winners += 1
    return num_winners


# Part 1
def get_total_cards_score(winning_numbers, candidate_numbers, num_cards):
    total_score = 0
    for i in trange(num_cards):
        card_winners = winning_numbers[i]
        card_candidates = candidate_numbers[i]
        num_winners = get_card_num_winners(card_winners, card_candidates)
        card_score = 2 ** (num_winners - 1) if num_winners > 0 else 0
        total_score += card_score

    return total_score


# Part 2
def get_num_cards_won(winning_numbers, candidate_numbers, start_num_cards):
    total_cards_won = 0
    card_multiplier = [1] * start_num_cards
    for i in trange(start_num_cards):
        card_winners = winning_numbers[i]
        card_candidates = candidate_numbers[i]
        num_winners = get_card_num_winners(card_winners, card_candidates)
        num_copies = card_multiplier[i]
        # add a copy for each card ahead for every winning number
        for k in range(1, num_winners + 1):
            # end of cards reached, prevent index error
            if i + k > start_num_cards:
                break
            card_multiplier[i + k] += num_copies
        total_cards_won += num_copies

    return total_cards_won


def solve(input, part):
    winning_numbers, candidate_numbers = preprocess_cards(input)
    assert len(winning_numbers) == len(candidate_numbers)
    num_cards = len(winning_numbers)
    if part == 1:
        solution = get_total_cards_score(winning_numbers, candidate_numbers, num_cards)
    else:
        solution = get_num_cards_won(winning_numbers, candidate_numbers, num_cards)
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
