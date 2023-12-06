import re
import sys
from math import floor

# infile = "day06/data/example.txt"
infile = "day06/data/day06.txt"

with open(infile) as f:
    indata = f.readlines()

indata = [i.strip() for i in indata]

times = indata[0].split()[1:]
distances = indata[1].split()[1:]


races = []
for t, d in zip(times, distances):
    races.append({"time": int(t), "distance": int(d)})


def calculate_winning_possibilities(race):
    """Calculate the number of winning possibilities in a race
    
    we use have_won to save testing the end of the range of times.
    Once we've stopped getting winning times, we know there can be 
    no more. In practice this didn't save much cpu time at all
    """
    winning = 0
    have_won = False 
    for x in range(race["time"]):
        speed = x
        time_remaining = race["time"] - speed
        distance_travelled = speed * time_remaining
        if distance_travelled > race["distance"]:
            winning += 1
            have_won = True
        elif have_won:
            return winning

    return winning


winning_product = 1
for r in races:
    winning_product *= calculate_winning_possibilities(r)

print("Part 1:", winning_product)

joined_race = {"time" : int("".join(times)),
               "distance" : int("".join(distances))}

joined_race_winning_possibilities = calculate_winning_possibilities(joined_race)

print("Part 2:", joined_race_winning_possibilities)
