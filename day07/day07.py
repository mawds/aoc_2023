import functools
from enum import Enum

#infile = "day07/data/example.txt"
#infile = "day07/data/testdata2.txt"
infile = "day07/data/day07.txt"

with open(infile) as f:
    indata = f.readlines()

indata = [i.strip() for i in indata]
indata = [i for i in indata if len(i) > 0]

# Set up card ordering so we can use it for sorting
card_order_ascending = "23456789TJQKA"
CARD_VALUES = {}
for v, c in enumerate(card_order_ascending):
    CARD_VALUES[c] = v


@functools.total_ordering
class Handtype(Enum):
    HIGHCARD = 1
    ONEPAIR = 2
    TWOPAIR = 3
    THREEKIND = 4
    FULLHOUSE = 5
    FOURKIND = 6
    FIVEKIND = 7

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value


@functools.total_ordering
class Card:
    def __init__(self, card):
        self.c = card
        self.value = CARD_VALUES[self.c]

    def __str__(self):
        return self.c

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value


# assert Card("2") == Card("2")
# assert Card("T") > Card("9")
# assert Card("K") < Card("A")
# assert Card("6") >= Card("6")


# @functools.total_ordering
class Hand:
    def __init__(self, cards, bid):
        if len(cards) != 5:
            raise ValueError("A hand has 5 cards")

        self.cards = []
        for c in cards:
            self.cards.append(Card(c))

        self.bid = int(bid)

    def __str__(self):
        return f"{','.join([c.c for c in self.cards])}, bid: {self.bid}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        for i, j in zip(self.cards, other.cards):
            if i.value != j.value:
                return False
        return True

    def get_type(self):
        if len(set([c.c for c in self.cards])) == 1:
            return Handtype.FIVEKIND
        else:
            cardtypes = [c.c for c in self.cards]
            cardcounts = {d: cardtypes.count(d) for d in cardtypes}
            cardtallys = list(cardcounts.values())
            cardtallys.sort()
            if cardtallys == [1, 4]:
                return Handtype.FOURKIND
            elif cardtallys == [2, 3]:
                return Handtype.FULLHOUSE
            elif cardtallys == [1, 1, 3]:
                return Handtype.THREEKIND
            elif cardtallys == [1, 2, 2]:
                return Handtype.TWOPAIR
            elif cardtallys == [1, 1, 1, 2]:
                return Handtype.ONEPAIR
            else:
                return Handtype.HIGHCARD

    def __gt__(self, other):
        if self.get_type() > other.get_type():
            return True
        elif self.get_type() == other.get_type():  # Test comparing first card
            for i in range(len(self.cards)):
                if self.cards[i] != other.cards[i]:
                    return self.cards[i] > other.cards[i]

        return False


hands = []
for i in indata:
    cards, bid = i.split()
    hands.append(Hand(cards, bid))

hands.sort()

rank = 1
total = 0
for h in hands:
    # print(h, h.get_type(), rank)
    total += rank * h.bid
    rank += 1

print("Part 1:", total)
#246795406