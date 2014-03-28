"""Utilities for dealing with hex grids.
"""

def neighbors(hex_coord):
    deltas = [(1,0,-1), (0,1,-1), (-1,1,0), 
              (-1,0,1), (0,-1,1), (1,-1,0)]
    neighbors = []
    for delta in deltas:
        neighbors.append(tuple(coord + d for coord, d in zip(hex_coord, delta)))
    return neighbors
