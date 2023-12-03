import re

infile = "day03/data/example.txt"
# infile = "day02/data/example_01.txt"

with open(infile) as f:
    indata = f.readlines()

indata = [i.strip() for i in indata]
indata = [i for i in indata if len(i) > 0]


class Digit:
    def __init__(self, value, end_coordinate):
        self.value = int(value)
        self.end_coordinate = end_coordinate
        self.start_coordinate = (end_coordinate[0] - len(value), end_coordinate[1])

    def __str__(self):
        return f"{self.start_coordinate} to {self.end_coordinate}: {self.value}"


class Symbol:
    def __init__(self, coordinate):
        self.coordinate = coordinate

    def __str__(self):
        return f"{self.coordinate}"


digits = []
symbols = []

for ypos, value in enumerate(indata):
    print(value)
    digit_string = ""
    for xpos, character in enumerate(value):
        print(xpos, character)
        if character in [str(x) for x in range(0, 10)]:
            digit_string += character
        else:
            if character != ".":
                symbols.append(Symbol((xpos, ypos)))

            if digit_string != "":
                digits.append(Digit(digit_string, (xpos, ypos)))
                digit_string = ""


for d in digits:
    print(d)

for s in symbols:
    print(s)
