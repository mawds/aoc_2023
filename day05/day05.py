import re
from itertools import tee
from collections import deque

# infile = "day05/data/example.txt"
infile = "day05/data/day05.txt"

with open(infile) as f:
    indata = f.readlines()

indata = [i.strip() for i in indata]

seeds = [int(i) for i in re.match("seeds: (.+)", indata[0])[1].split(" ")]


class XtoYMap:
    def __init__(self, map_data):
        header_data = re.match(r"(\w+)-to-(\w+) map", map_data[0])
        self.x = header_data[1]
        self.y = header_data[2]

        self.mapping = []
        for m in map_data[1:]:
            if m == "":
                break
            target, source, span = [int(i) for i in m.split(" ")]

            map = {"source_min": source, "source_max": source + span, "target": target}

            self.mapping.append(map)

    def __str__(self):
        return f"{self.x} to {self.y}:"

    def get_target(self, s):
        t = s
        for m in self.mapping:
            if m["source_min"] <= s < m["source_max"]:
                offset = s - m["source_min"]
                t = m["target"] + offset

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
            this_map_data = []

maps = {m.get_source(): m for m in maps}

cache = {}


def get_target_location(s, maps, cache):
    try:
        target_value = cache[s]

    except KeyError:
        source = "seed"
        original_s = s
        while source != "location":
            # map = [m for m in maps if m.get_source() == source][0]
            map = maps[source]
            target_value = map.get_target(s)
            next_target_type = map.get_target_map()
            source = next_target_type
            s = target_value

        cache[original_s] = target_value

    return target_value


locations = []

for s in seeds:
    target_value = get_target_location(s, maps, cache)
    locations.append(target_value)

print(f"Part 1: {min(locations)}")


locations_2 = []

for start_of_range, length_of_range in zip(seeds[::2], seeds[1::2]):
    print(start_of_range, length_of_range)
    for s in range(start_of_range, start_of_range + length_of_range + 1):
        locations_2.append(get_target_location(s, maps, cache))

print(f"Part 2: {min(locations_2)}")
