"""Board types are mappings between a hexagonal coordinate system and
ordinal numbers.

This mapping allows for different board sizes to be defined, and a
simple list of tiles/numbers/ports to be passed in for the
construction.

Currently the only board type defined is the standard 3-4 player
board.

"""

from abc import ABCMeta, abstractmethod

import hex_utils

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

    def ordinal_from_hexagon(self, hexagon_coord):
        """Give the ordinal location of a tile given its hexagon coordinates.
        """
        # Go to the cache before calling the library function.
        if hexagon_coord in self.cached_ordinal_from_hexagon:
            ordinal_coord = self.cached_ordinal_from_hexagon[hexagon_coord]
        # If missing, compute it and  cache the value.
        else:
            ordinal_coord = hex_utils.ordinal_from_hexagon(hexagon_coord)
            self.cached_ordinal_from_hexagon[hexagon_coord] = ordinal_coord
        return ordinal_coord

    def hexagon_from_ordinal(self, ordinal_coord):
        # Go to the cache before calling the library function.
        if ordinal_coord in self.cached_hexagon_from_ordinal:
            hexagon_coord = self.cached_hexagon_from_ordinal[ordinal_coord]
        # If missing, compute it and  cache the value.
        else:
            hexagon_coord = hex_utils.hexagon_from_ordinal(ordinal_coord)
            self.cached_hexagon_from_ordinal[ordinal_coord] = hexagon_coord
        return hexagon_coord

