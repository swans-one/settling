"""Board types are mappings between a hexagonal coordinate system and
ordinal numbers.

This mapping allows for different board sizes to be defined, and a
simple list of tiles/numbers/ports to be passed in for the
construction.

Currently the only board type defined is the standard 3-4 player
board.

"""

from abc import ABCMeta, abstractmethod

class BoardType(metaclass=ABCMeta):
    @abstractmethod
    def hexagon_from_ordinal(self, ordinal):
        """Return a class defined hexagon coordinate given an ordinal.
        """
        pass

    @abstractmethod
    def ordinal_from_hexagon(self, hexagon_coords):
        """Return a class defined ordinal given a hexagon coordinate.
        """
        pass

class StandardBoardType(BoardType):
    """The standard 3-4 player catan board.
    """
    def __init__(self):
        """Create caches for the mapping between ordinal and hexagon values.

        Since the computation in either direction can take a fair
        amount of time, we cache the values to create amoritized
        constant time lookups.

        We do not use fancy methods such as decorators to populate
        these caches, but rather code in the methods themselves.
        """
        self.cached_ordinal_from_hexagon = {}
        self.cached_hexagon_from_ordinal = {}

    def ordinal_from_hexagon(self, hex_coords):
        """Give the ordinal location of a tile given its hexagon coordinates.
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

    def hexagon_from_ordinal(self, ordinal):
        # Check the cache before computing
        if ordinal in self.cached_hexagon_from_ordinal:
            return self.cached_hexagon_from_ordinal[ordinal]

        # If the value is not in the cache, compute it explicitly
        ring, spine, offset = self.ring_spine_offset_from_ordinal(ordinal)
        hexagon_coords = self.hexagon_from_ring_spine_offset(ring, spine, offset)

        #cache computed value
        self.cached_hexagon_from_ordinal[ordinal] = hexagon_coords
        return hexagon_coords

    def ring_spine_offset_from_ordinal(self, ordinal):
        ring = self._find_ring(ordinal)
        spine = self._find_spine(ordinal, ring)
        offset = self._find_offset(ordinal, ring)
        return ring, spine, offset

    def _find_ring(self, ordinal, ring_so_far=0):
        """Recursively traverses triangular numbers.
        """
        check = ordinal - (6 * ring_so_far)
        if check <= 0:
            return ring_so_far
        else:
            return self._find_ring(check, ring_so_far + 1)

    def _find_spine(self, ordinal, ring):
        if ordinal == 0:
            return 0
        tiles_before_ring = sum(self._tiles_in_ring(r) for r in range(ring))
        ordinal_in_ring = ordinal - tiles_before_ring
        tiles_per_spine = self._tiles_in_ring(ring) // 6
        spine = ordinal_in_ring // tiles_per_spine
        return spine

    def _find_offset(self, ordinal, ring):
        if ordinal == 0:
            return 0
        tiles_before_ring = sum(self._tiles_in_ring(r) for r in range(ring))
        ordinal_in_ring = ordinal - tiles_before_ring
        tiles_per_spine = self._tiles_in_ring(ring) // 6
        offset = ordinal_in_ring % tiles_per_spine
        return offset

    def _tiles_in_ring(self, ring):
        return 1 if ring == 0 else ring * 6

    def hexagon_from_ring_spine_offset(self, ring, spine, offset):
        """Converts from a ring, spine and offset into hexagon coords.

        - ring is the number of tiles to the center along the shortest path.

        - spine is the nearest counter-clockwise "spoke" from the center.

        - offset is the number of tiles clockwise from the spine.

        This method is a helper method to make the implementation of
        hexagon_from_ordinal clearer.
        """
        ring_1 = [(1,0,-1), (0,1,-1), (-1,1,0), (-1,0,1), (0,-1,1), (1,-1,0)]
        if ring == 0 and spine == 0 and offset == 0:
            # We're in the center
            return (0, 0, 0)
        elif ring == 1 and offset == 0:
            # We're in the first ring
            return ring_1[spine]
        elif ring > 1 and offset == 0:
            # We're on a spine
            return tuple(ring * i for i in ring_1[spine])
        elif ring > 1 and offset != 0:
            # We move along the spine until we hit the next spine.
            move = ring_1[spine]
            next_loc = self.hexagon_from_ring_spine_offset(
                ring = ring - 1,
                spine = spine if offset < (ring - 1) else (spine + 1) % 6,
                offset = offset if offset < (ring - 1) else 0,
            )
            return tuple(m + l for m, l in zip(move, next_loc))
        else:
            err_msg = "{r}, {s}, {o} is not a valid ring, spine, offset."
            raise ValueError(err_msg.format(r=ring, s=spine, o=offset))

