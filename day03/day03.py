import re

#infile = "day03/data/example.txt"

infile = "day03/data/day03.txt"

with open(infile) as f:
    indata = f.readlines()

indata = [i.strip() for i in indata]
indata = [i for i in indata if len(i) > 0]


def adjacent_coordinates(coordinate):
    acs = []
    for x in range(coordinate[0] - 1, coordinate[0] + 2):
        for y in range(coordinate[1] - 1, coordinate[1] + 2):
            new_coordinate = (x, y)
            if new_coordinate != coordinate:
                acs.append(new_coordinate)

    return acs


class Part:
    def __init__(self, value, end_coordinate):
        self.value = int(value)
        self.end_coordinate = end_coordinate
        self.start_coordinate = (
            end_coordinate[0] - (len(value) - 1),
            end_coordinate[1],
        )
        self.coordinates = [
            (i, self.start_coordinate[1])
            for i in range(self.start_coordinate[0], self.end_coordinate[0] + 1)
        ]

    def is_part_number(self, symbols):
        for c in self.coordinates:
            acs = adjacent_coordinates(c)
            if len(set(acs) & {s.coordinate for s in symbols}) > 0:
                return True

        return False

    def __str__(self):
        return f"{self.start_coordinate} to {self.end_coordinate}: {self.value}"


class Symbol:
    def __init__(self, symb, coordinate):
        self.coordinate = coordinate
        self.symb = symb

    def __str__(self):
        return f"{self.coordinate}: {self.symb}"

    def adjacent_parts(self, parts):
        acs = adjacent_coordinates(self.coordinate)
        ap = []
        for p in parts:
            if set(p.coordinates) & set(acs):
                ap.append(p)
        
        return ap

    def get_gear_ratio(self, parts):
        if self.symb == "*":
            aps = self.adjacent_parts(parts)
            if len(aps) == 2:
                return aps[0].value * aps[1].value
        return 0


parts = []
symbols = []

digit_string = ""
for ypos, value in enumerate(indata):
    digit_string = ""
    for xpos, character in enumerate(value):
        if character in [str(x) for x in range(0, 10)]:
            digit_string += character
        else:
            if character != ".":
                symbols.append(Symbol(character, (xpos, ypos)))

            if digit_string != "":
                parts.append(Part(digit_string, (xpos - 1, ypos)))
                digit_string = ""
    # Add the part if it's the final entry on the line
    if digit_string != "":
        parts.append(Part(digit_string, (xpos - 1, ypos)))
        digit_string = ""


actual_parts = []
part_sum = 0
for p in parts:
    if p.is_part_number(symbols):
        actual_parts.append(p.value)
        part_sum += p.value

print("Part 1:", part_sum)

ratios = 0
for s in symbols:
    ratios += s.get_gear_ratio(parts)
    
print("Part 2", ratios)
