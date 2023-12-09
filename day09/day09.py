import re
import math
from itertools import cycle

infile = "day09/data/example.txt"
infile = "day09/data/data.txt"

with open(infile) as f:
    indata = f.readlines()

indata = [i.strip() for i in indata]
indata = [i for i in indata if len(i) > 0]


def get_differences_list(s):
    return [m - n for m, n in zip(s[1:], s)]


def get_next_value(s):
    s_stack = []
    seq = s.copy()
    s_stack.append(seq)
    while True:
        d = get_differences_list(seq)
        if len(set(d)) == 1 and d[0] == 0:
            d.append(0)
        s_stack.append(d)
        seq = d
        if len(set(d)) == 1 and d[0] == 0:
            break

    while len(s_stack) > 1:
        to_add = s_stack.pop()[-1]
        s_stack[-1].append(s_stack[-1][-1] + to_add)
    
    return s_stack[0]


readings = []
for i in indata:
    readings.append([int(r) for r in i.split()])

new_readings = []
for r in readings:
    new_readings.append(get_next_value(r))
    
total_last_values = 0
for n in new_readings:
    total_last_values += n[-1]
    
print("Part 1", total_last_values)
    