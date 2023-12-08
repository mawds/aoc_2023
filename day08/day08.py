import re
from itertools import cycle

# infile = "day08/data/example_1.txt"
# infile = "day08/data/example_2.txt"
infile = "day08/data/data.txt"

with open(infile) as f:
    indata = f.readlines()

indata = [i.strip() for i in indata]
# indata = [i for i in indata if len(i) > 0]


class Node:
    def __init__(self, indata):
        in_split = re.match(r"(\w{3}) = \((\w{3}), (\w{3})\)", indata)
        self.name = in_split[1]
        self.left = in_split[2]
        self.right = in_split[3]

    def __repr__(self):
        return f"{self.name}: ({self.left},{self.right})"


directions = list(indata[0])

nodes = {}
firstnode = None
for i in indata[2:]:
    if len(i) > 0:
        thisnode = Node(i)
        nodes[thisnode.name] = thisnode
        if firstnode is None:
            firstnode = thisnode.name

# print("Firstnode", firstnode)
print(f"{len(nodes)} nodes, {len(directions)} directions")


node = nodes["AAA"]
steps = 0
for d in cycle(directions):
    # print(steps, d, node)
    match d:
        case "L":
            node = nodes[nodes[node.name].left]
        case "R":
            node = nodes[nodes[node.name].right]
        case _:
            raise ValueError("Unknown direction")
    steps += 1
    if node.name == "ZZZ":
        break
print("Part 1", steps)
