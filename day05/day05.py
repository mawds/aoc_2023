import re
import sys
from math import floor

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


def get_target_location(s, maps):
    source = "seed"
    while source != "location":
        # map = [m for m in maps if m.get_source() == source][0]
        map = maps[source]
        target_value = map.get_target(s)
        next_target_type = map.get_target_map()
        source = next_target_type
        s = target_value

    return target_value


locations = []

for s in seeds:
    target_value = get_target_location(s, maps)
    locations.append(target_value)

print(f"Part 1: {min(locations)}")


min_location = sys.maxsize

# This is horrendously slow
# for start_of_range, length_of_range in zip(seeds[::2], seeds[1::2]):
#     print(start_of_range, length_of_range)
#     for s in range(start_of_range, start_of_range + length_of_range + 1):
#         locations_2.append(get_target_location(s, maps))


def get_min_in_span(start_of_range, end_of_range, maps, min_location):
    # Need to keep splitting the range until we get the difference in
    # location equal to span
    # Then return minimum in that span (which will be the answer for the first
    # element).
    # Then work on remaining part of span

    if start_of_range > end_of_range:
        raise ValueError("start range after end range")

    span = end_of_range - start_of_range
    start_target = get_target_location(start_of_range, maps)
    end_target = get_target_location(end_of_range, maps)
    difference = end_target - start_target

    # print(
    #     f"Going from {start_of_range} to {end_of_range}, span: {span}, diff: {difference}"
    # )

    if difference == span:
        min_location = min(min_location, start_target)
        return min_location
    elif span <= 1:
        return min(start_target, end_target, min_location)
    else:
        new_end = start_of_range + floor(span / 2)
        
        min_location = get_min_in_span(start_of_range, new_end, maps, min_location)
        min_location2 = get_min_in_span(new_end, end_of_range, maps, min_location)
        return min(min_location, min_location2)

for start_of_range, length_of_range in zip(seeds[::2], seeds[1::2]):
    end_of_range = start_of_range + length_of_range + 1
    # print(
    #     f"Working on: Start: {start_of_range}, End: {end_of_range}, length: {length_of_range}"
    # )
    min_location = get_min_in_span(start_of_range, end_of_range, maps, min_location)

    # break  # for debug - just first pair

print(f"Part 2: {min_location}")
