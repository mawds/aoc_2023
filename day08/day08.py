import re
import math
from itertools import cycle

# infile = "day08/data/example_1.txt"
# infile = "day08/data/example_2.txt"
infile = "day08/data/example_3.txt"
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

    def is_startnode(self):
        return self.name[-1] == "A"

    def is_endnode(self):
        return self.name[-1] == "Z"

    def __repr__(self):
        return f"{self.name}: ({self.left},{self.right})"


directions = list(indata[0])

map_nodes = {}
firstnode = None
for i in indata[2:]:
    if len(i) > 0:
        thisnode = Node(i)
        map_nodes[thisnode.name] = thisnode
        if firstnode is None:
            firstnode = thisnode.name

# print("Firstnode", firstnode)
print(f"{len(map_nodes)} nodes, {len(directions)} directions")


node = map_nodes["AAA"]
steps = 0
for d in cycle(directions):
    # print(steps, d, node)
    match d:
        case "L":
            node = map_nodes[node.left]
        case "R":
            node = map_nodes[node.right]
        case _:
            raise ValueError("Unknown direction")
    steps += 1
    if node.name == "ZZZ":
        break
print("Part 1", steps)


nodes = [map_nodes[n] for n in map_nodes if map_nodes[n].is_startnode()]


def solve_routes(nodes):
    steps = 0
    for d in cycle(directions):
        for i, n in enumerate(nodes):
            match d:
                case "L":
                    nodes[i] = map_nodes[n.left]
                case "R":
                    nodes[i] = map_nodes[n.right]
                case _:
                    raise ValueError("Unknown direction")
        steps += 1
        if not steps % 1000000:
            print(f"{steps/1000000} million iterations")
        if all([x.is_endnode() for x in nodes]):
            return steps


# Solve each route in series and use this to figure out when they'll be in sync
steps = [solve_routes([n]) for n in nodes]

# Lowest common multiple will be when they're all in sync
print("Part 2", math.lcm(*steps))
