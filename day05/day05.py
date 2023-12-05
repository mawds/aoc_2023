import re
import itertools
from collections import deque

infile = "day05/data/example.txt"
#infile = "day05/data/day05.txt"

with open(infile) as f:
    indata = f.readlines()

indata = [i.strip() for i in indata]

seeds = [int(i) for i in re.match("seeds: (.+)", indata[0])[1].split(" ")]


class XtoYMap:
    def __init__(self, map_data):
        header_data = re.match(r"(\w+)-to-(\w+) map", map_data[0])
        self.x = header_data[1]
        self.y = header_data[2]

        self.mapping = {}
        for m in map_data[1:]:
            if m == "":
                break
            target, source, span = [int(i) for i in m.split(" ")]
            span = span
            for r in range(span):
                self.mapping[source] = target
                target += 1
                source += 1

    def __str__(self):
        return f"{self.x} to {self.y}:"

    def get_target(self, s):
        try:
            t = self.mapping[s]
        except KeyError:
            t = s
        finally:
            return t

    def get_target_map(self):
        return self.y

    def get_source(self):
        return self.x

    def print_mapping(self):
        for i in range(100):
            print(i, self.get_target(i))
        


# Load in the maps
maps = []
this_map_data = []
for i in indata[2:]:
    this_map_data.append(i)
    if len(i) == 0:
        if len(this_map_data[0]) > 0:
            maps.append(XtoYMap(this_map_data))
            print(maps[-1])
            this_map_data = []

locations = []
for s in seeds:
    print(s, ": ", end="")
    source = "seed"
    while source != "location":
        map = [m for m in maps if m.get_source() == source][0]
        target_value = map.get_target(s)
        next_target_type = map.get_target_map()
        source = next_target_type
        s = target_value

    locations.append(target_value)
    print(target_value)

print(f"Part 1: {min(locations)}")