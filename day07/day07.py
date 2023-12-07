import functools
import itertools
from enum import Enum
import copy

# infile = "day07/data/example.txt"
# infile = "day07/data/testdata2.txt"
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

card_order_jacks_wild = "J23456789TQKA"
CARD_VALUES_JACKS_WILD = {}
for v, c in enumerate(card_order_jacks_wild):
    CARD_VALUES_JACKS_WILD[c] = v


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
    def __init__(self, card, *args, **kwargs):
        try:
            card_values = kwargs["card_values"]
        except KeyError:
            card_values = CARD_VALUES
        self.c = card
        self.value = card_values[self.c]

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
    def __init__(self, cards, bid, *args, **kwargs):
        if len(cards) != 5:
            raise ValueError("A hand has 5 cards")

        self.cards = []
        for c in cards:
            self.cards.append(Card(c, *args, **kwargs))

        self.bid = int(bid)

    def __str__(self):
        return f"{','.join([str(c.c + '(' + str(c.value) + ')') for c in self.cards])}, bid: {self.bid}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        for i, j in zip(self.cards, other.cards):
            if i.value != j.value:
                return False
        return True

    def has_jack(self):
        return "J" in set([c.c for c in self.cards])

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

    def maximise_type(self):
        """Change the hand type to the best possible using Jokers"""
        if not self.has_jack():
            return

        # All jokers is already a five of a kind
        # Don't bother testing this one as it slows things down a lot
        if [c.c for c in self.cards].count("J") == 5:
            return

        # We'll do this inefficiently and just loop over all possible hands
        # and set cards to the strongest
        best_hand = copy.deepcopy(self)
        test_hand = copy.deepcopy(self)
        # Get positions of Jacks
        j_positions = [i for i, x in enumerate(test_hand.cards) if x.c == "J"]
        # Generate a list of lists of all possible cards at each of the j_positions
        card_options = [list(card_order_jacks_wild)] * len(j_positions)

        # Test each of them
        for e in itertools.product(*card_options):
            for i, p in enumerate(j_positions):
                test_hand.cards[p].c = e[i]
                # Don't overwrite the value since we use the original values in comparison
                # test_hand.cards[p].value = CARD_VALUES_JACKS_WILD[e[i]]
                if test_hand > best_hand:
                    best_hand = copy.deepcopy(test_hand)

        self.cards = best_hand.cards.copy()


hands = []
for i in indata:
    cards, bid = i.split()
    hands.append(Hand(cards, bid))

hands.sort()

rank = 1
total = 0
for h in hands:
    total += rank * h.bid
    rank += 1

print("Part 1:", total)

# Part 2
wild_hands = []
for i in indata:
    cards, bid = i.split()
    wild_hands.append(Hand(cards, bid, card_values=CARD_VALUES_JACKS_WILD))

for h in wild_hands:
    h.maximise_type()

wild_hands.sort()

rank = 1
total = 0
for h in wild_hands:
    total += rank * h.bid
    rank += 1

print("Part 2:", total)
