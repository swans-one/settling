"""Utilities for dealing with hex grids.

This file establishes three hex grid coordinate systems.

1) Ordinal -- A system of numbering a grid of hexagons starting at 0
   and extending to +Inf.

2) Hexagon -- A system in in N3, where coordinates are 3-tuples
   representing coordinates in the three directions naturally
   associated with the six sides of a hexagon.

3) RSO (Ring Spine Offset -- A system in N3, where coordinates are
   3-tuples of a ring coordinate, a spine coordinate, and an offset
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
mapping between ring, spine and offset, and attempts to graphically
show how they are calculated and related.


                 spl 5
            -y     _    +x
              \  /17 \  /      _
               \ \ _ / /   _ /19 \ spine 0
       spine 4 _\/ 6 \/_ / 7 \ _ /
             / 5 \ _ / 1 \ _ /
       +z____\ _ / 0 \ _ / 8 \ _ ____-z
             / 4 \ _ / 2 \ _ /21 \
     spine 3 \ _ / 3 \ _ / 9 \ _ /
                /\ _ /\  \ _ /
               /       \     spine 1
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
        neighbor = tuple(coord + d for coord, d in zip(hex_coord, delta))
        neighbors.append(neighbor)
    return neighbors

def hexagon_from_ordinal(ordinal_coord):
    """Convert from an ordinal to a hexagon coordinate.
    """
    # If the value is not in the cache, compute it explicitly
    rso = rso_from_ordinal(ordinal_coord)
    hexagon_coords = hexagon_from_rso(rso)
    return hexagon_coords

def hexagon_from_rso(rso_coord):
    """Convert from a ring spine offset to a hexagon coordinate.
    """
    pass

def ordinal_from_hexagon(hexagon_coord):
    """Convert from a hexagon to an ordianl coordinate.
    """
    # First check that the coordinates are valid
    if sum(hexagon_coord) != 0:
        raise ValueError("{0} are not valid hexagon coordinates".format(hexagon_coord))
    # Iterate through all the ordinal numbers, comparing to their
    # hexagon coordinates to those given.
    #
    # This method ensures that the ordering is consistent in both
    # directions.
    MAX_SEARCH = 1000
    current_ordinal = 0
    while current_ordinal < MAX_SEARCH:
        hexagon = hexagon_from_ordinal(current_ordinal)
        if hexagon == hexagon_coord:
            return current_ordinal
        current_ordinal += 1
    err_msg = "Cannot find coordinates in first {0} ordinals"
    raise ValueError(err_msg.format(MAX_SEARCH))

def ordinal_from_rso(rso_coord):
    """Convert from a ring spine offset to an ordinal coordinate.
    """
    pass

def rso_from_hexagon(hexagon_coord):
    """Convert from a hexagon to ring spine offset coordinate.
    """
    pass

def rso_from_ordinal(ordinal_coord):
    """Convert from an ordinal to a ring spine offset coordinate.
    """
    ring = _find_ring(ordinal_coord)
    spine = _find_spine(ordinal_coord, ring)
    offset = _find_offset(ordinal_coord, ring)
    return ring, spine, offset


def _find_ring(ordinal, ring_so_far=0):
    """Recursively traverses triangular numbers.
    """
    check = ordinal - (6 * ring_so_far)
    if check <= 0:
        return ring_so_far
    else:
        return _find_ring(check, ring_so_far + 1)

def _find_spine(ordinal, ring):
    if ordinal == 0:
        return 0
    tiles_before_ring = sum(_tiles_in_ring(r) for r in range(ring))
    ordinal_in_ring = ordinal - tiles_before_ring
    tiles_per_spine = _tiles_in_ring(ring) // 6
    spine = ordinal_in_ring // tiles_per_spine
    return spine

def _find_offset(ordinal, ring):
    if ordinal == 0:
        return 0
    tiles_before_ring = sum(_tiles_in_ring(r) for r in range(ring))
    ordinal_in_ring = ordinal - tiles_before_ring
    tiles_per_spine = _tiles_in_ring(ring) // 6
    offset = ordinal_in_ring % tiles_per_spine
    return offset

def _tiles_in_ring(ring):
    return 1 if ring == 0 else ring * 6
