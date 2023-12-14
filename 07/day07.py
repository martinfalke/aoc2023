import sys
from functools import reduce

DAY = 7


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
    # create instances of CardHand
    hands = []
    for hand_line in input:
        cl = hand_line.split()
        hand = cl[0]
        bid = int(cl[1])
        card_hand = CardHand(hand, bid)
        hands.append(card_hand)
    return hands


class CardHand:
    hand_types = [0, 1, 2, 3, 4, 5, 6]
    #                   high card   one pair     two pair   threekind  full house fourkind fivekind
    hand_types_counts = [[1, 1, 1, 1, 1], [2, 1, 1, 1], [2, 2, 1], [3, 1, 1], [3, 2], [4, 1], [5]]
    card_types = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    use_jokers = False

    def __init__(self, hand, bid):
        self.rank = None
        self.hand = hand
        self.bid = bid
        self.score = 0
        self.tiebreak_score = [0] * len(hand)
        self.set_score()

    def __str__(self):
        return f'{self.hand}\t{self.bid}\t{self.rank}\nScore:{self.score}\nTiebreaker: {self.tiebreak_score}\n'

    def __repr__(self):
        return f'{self.hand}\t{self.bid}\t{self.rank}'

    def set_rank(self, rank):
        self.rank = rank

    def set_score(self):
        # count the number of each card type
        card_counts = [0] * len(self.card_types)
        for i, card in enumerate(self.hand):
            card_type = self.card_types.index(card)
            card_counts[card_type] += 1
            self.tiebreak_score[i] = card_type

        # use the joker as the most frequently appearing other card
        if self.use_jokers:
            joker_count = card_counts[0]
            card_counts[0] = 0
            max_index = card_counts.index(max(card_counts))
            card_counts[max_index] += joker_count

        assert (sum(card_counts) == len(self.hand))
        # format the card_counts like defined in self.hand_type_counts
        type_counts = sorted([count for i, count in enumerate(card_counts) if count != 0], reverse=True)
        hand_type = self.hand_types_counts.index(type_counts)
        score = self.hand_types[hand_type]
        self.score = score

    def get_winnings(self):
        return self.rank * self.bid


def solve(input, part):
    if part == 2:
        # change 'J' to mean joker
        joker_index = CardHand.card_types.index('J')
        # move 'J' from current pos in types list to the start (lowest index = lowest value)
        CardHand.card_types.insert(0, CardHand.card_types.pop(joker_index))
        CardHand.use_jokers = True

    card_hands = preprocess_input(input)

    # sort the hands first on their score, second on tiebreak score (highest card left-to-right)
    card_hands = sorted(card_hands, key=lambda c: (c.score, c.tiebreak_score))
    # use sort ranking index to set game rank
    for i, hand in enumerate(card_hands):
        hand.set_rank(i + 1)

    # sum up winnings of each hand
    total_winnings = reduce(lambda tw, h: tw + h.get_winnings(), card_hands, 0)
    return total_winnings


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
