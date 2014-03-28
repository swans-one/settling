"""Utilities for dealing with hex grids.

This file establishes three hex grid coordinate systems.

1) Ordinal -- A system of numbering a grid of hexagons starting at 0
   and extending to +Inf.

2) Hexagon -- A system in in N3, where coordinates are 3-tuples
   representing coordinates in the three directions naturally
   associated with the six sides of a hexagon.

3) RSP (Ring Spline Offset -- A system in N3, where coordinates are
   3-tuples of a ring coordinate, a spline coordinate, and an offset
   coordinate.

"""

def neighbors(hex_coord):
    deltas = [(1,0,-1), (0,1,-1), (-1,1,0), 
              (-1,0,1), (0,-1,1), (1,-1,0)]
    neighbors = []
    for delta in deltas:
        neighbors.append(tuple(coord + d for coord, d in zip(hex_coord, delta)))
    return neighbors
