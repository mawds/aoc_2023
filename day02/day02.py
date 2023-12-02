import re

infile = "day02/data/day_02.txt"
# infile = "day02/data/example_01.txt"

with open(infile) as f:
    indata = f.readlines()

indata = [i.strip() for i in indata]
indata = [i for i in indata if len(i) > 0]


class Draw:
    colours = {}

    def __init__(self, colours):
        self.colours = colours


class Game:
    id = 0
    draws = []

    def __init__(self, id):
        self.id = id
        self.draws = []

    def add(self, draw):
        self.draws.append(draw)

    def test_possible(self, max_cubes):
        for d in self.draws:
            for key, value in max_cubes.items():
                if d[key] > value:
                    return False

        return True

    def get_power(self):
        min_cubes = {"red": 0, "green": 0, "blue": 0}

        for d in self.draws:
            for key, value in min_cubes.items():
                if d[key] > value:
                    min_cubes[key] = d[key]

        return min_cubes["red"] * min_cubes["green"] * min_cubes["blue"]

games = []

game_regex = r"^Game (\d+): (.+)$"
colour_regex = r"\s?(\d+) (red|green|blue)"
for line in indata:
    matched = re.match(game_regex, line)
    if matched:
        game_id = int(matched[1])
        this_game = Game(game_id)

        draws = matched[2].split(";")
        for d in draws:
            colour_string = d.split(",")
            colours = {"red": 0, "green": 0, "blue": 0}
            for c in colour_string:
                colour_match = re.match(colour_regex, c)
                if colour_match:
                    colours[colour_match[2]] = int(colour_match[1])

            this_game.add(colours)

        games.append(this_game)

max_cubes = {"red": 12, "green": 13, "blue": 14}

id_total = 0
for g in games:
    if g.test_possible(max_cubes):
        id_total += g.id
        
print("Part 1")
print(id_total)

powers = [g.get_power() for g in games]

result = 0
for p in powers:
    result += p
    
print("Part 2")
print(result)
