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
        neighbor = tuple(coord + d for coord, d in zip(hex_coord, delta))
        neighbors.append(neighbor)
    return neighbors

def hexagon_from_ordinal(ordinal_coord):
    """Convert from an ordinal to a hexagon coordinate.
    """
    # Check the cache before computing
    if ordinal in self.cached_hexagon_from_ordinal:
        return self.cached_hexagon_from_ordinal[ordinal]

    # If the value is not in the cache, compute it explicitly
    ring, spine, offset = self.ring_spine_offset_from_ordinal(ordinal)
    hexagon_coords = self.hexagon_from_ring_spine_offset(ring, spine, offset)

    #cache computed value
    self.cached_hexagon_from_ordinal[ordinal] = hexagon_coords
    return hexagon_coords

def hexagon_from_rso(rso_coord):
    """Convert from a ring spline offset to a hexagon coordinate.
    """
    pass

def ordinal_from_hexagon(hexagon_coord):
    """Convert from a hexagon to an ordianl coordinate.
    """
    # First check that the coordinates are valid
    if sum(hex_coords) != 0:
        raise ValueError("{0} are not valid hexagon coordinates".format(hex_coords))
     # Go to the cache before iterating
    if hex_coords in self.cached_ordinal_from_hexagon:
        return self.cached_ordinal_from_hexagon[hex_coords]

    # If the cache fails, iterate through all the ordinal numbers,
    # comparing to their hexagon coordinates to those given.
    #
    # This method ensures that the ordering is consistent in both
    # directions.
    MAX_SEARCH = 1000
    current_ordinal = 0
    while current_ordinal < MAX_SEARCH:
        hexagon = self.hexagon_from_ordinal(current_ordinal)
        if hexagon == hex_coords:
            # cache computed value
            self.cached_ordinal_from_hexagon[hex_coords] = current_ordinal
            return current_ordinal
        current_ordinal += 1
    err_msg = "Cannot find coordinates in first {0} ordinals"
    raise ValueError(err_msg.format(MAX_SEARCH))

def ordinal_from_rso(rso_coord):
    """Convert from a ring spline offset to an ordinal coordinate.
    """
    pass

def rso_from_hexagon(hexagon_coord):
    """Convert from a hexagon to ring spline offset coordinate.
    """
    pass

def rso_from_ordinal(ordinal_coord):
    """Convert from an ordinal to a ring spline offset coordinate.
    """
    ring = self._find_ring(ordinal)
    spine = self._find_spine(ordinal, ring)
    offset = self._find_offset(ordinal, ring)
    return ring, spine, offset


def _find_ring(ordinal, ring_so_far=0):
    """Recursively traverses triangular numbers.
    """
    check = ordinal - (6 * ring_so_far)
    if check <= 0:
        return ring_so_far
    else:
        return self._find_ring(check, ring_so_far + 1)

def _find_spine(ordinal, ring):
    if ordinal == 0:
        return 0
    tiles_before_ring = sum(self._tiles_in_ring(r) for r in range(ring))
    ordinal_in_ring = ordinal - tiles_before_ring
    tiles_per_spine = self._tiles_in_ring(ring) // 6
    spine = ordinal_in_ring // tiles_per_spine
    return spine

def _find_offset(ordinal, ring):
    if ordinal == 0:
        return 0
    tiles_before_ring = sum(self._tiles_in_ring(r) for r in range(ring))
    ordinal_in_ring = ordinal - tiles_before_ring
    tiles_per_spine = self._tiles_in_ring(ring) // 6
    offset = ordinal_in_ring % tiles_per_spine
    return offset

def _tiles_in_ring(ring):
    return 1 if ring == 0 else ring * 6
