import functools
import itertools
from enum import Enum
import copy


infile = "day08/data/example_1.txt"
# infile = "day08/data/example_2.txt"
# infile = "day08/data/data.txt"

with open(infile) as f:
    indata = f.readlines()

indata = [i.strip() for i in indata]
indata = [i for i in indata if len(i) > 0]
