"""Utilities for dealing with hex grids.

This file establishes three hex grid coordinate systems.

1) Ordinal -- A system of numbering a grid of hexagons starting at 0
   and extending to +Inf.

2) Hexagon -- A system in in N3, where coordinates are 3-tuples
   representing coordinates in the three directions naturally
   associated with the six sides of a hexagon.

3) RSO (Ring Spline Offset -- A system in N3, where coordinates are
   3-tuples of a ring coordinate, a spline coordinate, and an offset
   coordinate.

These three coordinate systems are each useful for different purposes,
and being able to convert between them compound their usefullness.

1) An ordinal system is useful as a storage medium, since python has a
   native list type, but not a native hexagonal type.

2) Hexagon coordinates are useful for finding neighboring coordinates,
   and traveling along the hex grid.

3) RSO coordinates are useful for determining how far from center, and
   how far around the ring you are.

This library provides utilities for converting between these
coordinate systems, as well as some other useful tools for working
with the coordinate systems.

The following graph, and table gives a number of examples of the
mapping between ring, spline and offset, and attempts to graphically
show how they are calculated and related.


                 spl 5
            -y     _    +x
              \  /17 \  /      _
               \ \ _ / /   _ /19 \ spline 0
      spline 4 _\/ 6 \/_ / 7 \ _ /
             / 5 \ _ / 1 \ _ /
       +z____\ _ / 0 \ _ / 8 \ _ ____-z
             / 4 \ _ / 2 \ _ /21 \
    spline 3 \ _ / 3 \ _ / 9 \ _ /
                /\ _ /\  \ _ /
               /       \     spline 1
              /  spl 2  \
            -x          +y

    |-----+-----------+--------------|
    | Ord | RSO       | Hexagon      |
    |-----+-----------+--------------|
    |   0 | (0, 0, 0) | ( 0,  0,  0) |
    |   1 | (1, 0, 0) | ( 1,  0, -1) |
    |   2 | (1, 1, 0) | ( 0,  1, -1) |
    |   3 | (1, 2, 0) | (-1,  1,  0) |
    |   4 | (1, 3, 0) | (-1,  0,  1) |
    |   5 | (1, 4, 0) | ( 0, -1,  1) |
    |   6 | (1, 5, 0) | ( 1, -1,  0) |
    |   7 | (2, 0, 0) | ( 2,  0, -2) |
    |   8 | (2, 0, 1) | ( 1,  1, -2) |
    |   9 | (2, 1, 0) | ( 0,  2, -2) |
    |  17 | (2, 5, 0) | ( 2, -2,  0) |
    |  19 | (3, 0, 0) | ( 3,  0, -3) |
    |  21 | (3, 0, 2) | ( 1,  2, -3) |
    |-----+-----------+--------------|
"""

def neighbors(hex_coord):
    deltas = [(1,0,-1), (0,1,-1), (-1,1,0), 
              (-1,0,1), (0,-1,1), (1,-1,0)]
    neighbors = []
    for delta in deltas:
        neighbors.append(tuple(coord + d for coord, d in zip(hex_coord, delta)))
    return neighbors
