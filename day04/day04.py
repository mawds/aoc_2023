import re
import itertools
from collections import deque

infile = "day04/data/day04.txt"
# infile = "day04/data/example_01.txt"


class Card:
    def _process_numbers(self, number_string):
        split_numbers = [i for i in number_string.split(" ")]

        return [int(i) for i in split_numbers if i != ""]

    def __init__(self, card_data):
        card_parts = re.match(r"Card.+?(\d+): (.+)\|(.+)", card_data)

        self.card_number = int(card_parts[1])

        self.winning_numbers = self._process_numbers(card_parts[2])
        self.card_numbers = self._process_numbers(card_parts[3])
        self.copies = 1

    def number_of_matches(self):
        return len(set(self.card_numbers) & set(self.winning_numbers))

    def score(self):
        num_matches = self.number_of_matches()
        if num_matches == 0:
            return 0
        else:
            return 2 ** (num_matches - 1)

    def win_copy(self):
        self.copies += 1

    def __str__(self):
        return (
            f"Card: {self.card_number}\n"
            + f"Winning: {self.winning_numbers}\n"
            + f"On card: {self.card_numbers}\n"
        )


with open(infile) as f:
    indata = f.readlines()

indata = [i.strip() for i in indata]
indata = [i for i in indata if len(i) > 0]

cards = [Card(c) for c in indata]

total_score = 0
for c in cards:
    total_score += c.score()

print(f"Part 1: {total_score}")


def play_card(card, cards):
    number_of_cards_won = card.number_of_matches()
    new_cards_won = cards[card.card_number : card.card_number + number_of_cards_won]

    return new_cards_won


for c in cards:
    for copy in range(c.copies):
        won_cards = play_card(c, cards)
        [w.win_copy() for w in won_cards]

total_copies = 0
for c in cards:
    total_copies += c.copies

print(f"Part 2: {total_copies}")
