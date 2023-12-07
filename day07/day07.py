import re
import sys
from math import floor
import functools

infile = "day07/data/example.txt"
# infile = "day07/data/day07.txt"

with open(infile) as f:
    indata = f.readlines()

indata = [i.strip() for i in indata]
indata = [i for i in indata if len(i)>0]

# Set up card ordering so we can use it for sorting
card_order_ascending = "23456789TJQKA"
CARD_VALUES = {}
for v, c in enumerate(card_order_ascending):
    CARD_VALUES[c] = v

print(CARD_VALUES)


@functools.total_ordering
class Card:
    def __init__(self, card):
        self.c = card
        self.value = CARD_VALUES[self.c]

    def __str__(self):
        return c

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value


# assert Card("2") == Card("2")
# assert Card("T") > Card("9")
# assert Card("K") < Card("A")
# assert Card("6") >= Card("6")


class Hand:
    def __init__(self, cards, bid):
        if len(cards) != 5:
            raise ValueError("A hand has 5 cards")

        self.cards = []
        for c in cards:
            self.cards.append(Card(c))

        self.bid = bid

    def __str__(self):
        return f"{','.join([c.c for c in self.cards])}, bid: {self.bid}"


hands = []
for i in indata:
    cards, bid = i.split()
    hands.append(Hand(cards, bid))

for h in hands:
    print(h)