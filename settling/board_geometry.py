"""Board types are mappings between a hexagonal coordinate system and
ordinal numbers.

This mapping allows for different board sizes to be defined, and a
simple list of tiles/numbers/ports to be passed in for the
construction.

Currently the only board type defined is the standard 3-4 player
board.
"""

from abc import ABCMeta, abstractmethod

import hexagon_utils as hx


class BoardGeometry(metaclass=ABCMeta):
    @abstractmethod
    def hexagon_from_ordinal(self, ordinal):
        """Return a class defined hexagon coordinate given an ordinal.
        """
        pass

    @abstractmethod
    def ordinal_from_hexagon(self, hexagon_coord):
        """Return a class defined ordinal given a hexagon coordinate.
        """
        pass

    @abstractmethod
    def hexagon_neighbors(self, hexagon_coord):
        """Return the coordinates of any existing neighbors.
        """
        pass

    @abstractmethod
    def vertex_synonyms(self, hexagon_coord, vertex):
        """Return any other ways of addressing a given vertex.
        """
        pass

class StandardBoard(BoardGeometry):
    """The standard 3-4 player catan board.

    There are only 37 tiles in the standard board.
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
        self.max_ordinal = 36 # 36 is max ordinal for 37 tiles

    def ordinal_from_hexagon(self, hexagon_coord):
        """Give the ordinal location of a tile given its hexagon coordinates.
        """
        # Go to the cache before calling the library function.
        if hexagon_coord in self.cached_ordinal_from_hexagon:
            ordinal_coord = self.cached_ordinal_from_hexagon[hexagon_coord]
        # If missing, compute it and  cache the value.
        else:
            ordinal_coord = hx.ordinal_from_hexagon(hexagon_coord)
            self.cached_ordinal_from_hexagon[hexagon_coord] = ordinal_coord
        return ordinal_coord

    def hexagon_from_ordinal(self, ordinal_coord):
        # Go to the cache before calling the library function.
        if ordinal_coord in self.cached_hexagon_from_ordinal:
            hexagon_coord = self.cached_hexagon_from_ordinal[ordinal_coord]
        # If missing, compute it and  cache the value.
        else:
            hexagon_coord = hx.hexagon_from_ordinal(ordinal_coord)
            self.cached_hexagon_from_ordinal[ordinal_coord] = hexagon_coord
        return hexagon_coord

    def hexagon_neighbors(self, hexagon_coord):
        all_neighbors = hx.neighbors(hexagon_coord)
        existing_neighbors = []
        for neighbor in all_neighbors:
            if self.ordinal_from_hexagon(neighbor) <= self.max_ordinal:
                existing_neighbors.append(neighbor)
        return existing_neighbors

    def vertex_synonyms(self, hexagon_coord, vertex):
        all_neighbors = hx.neighbors(hexagon_coord)
        first = all_neighbors[vertex - 1]
        second = all_neighbors[vertex]
        other_names = []
        if hx.ordinal_from_hexagon(first) <= self.max_ordinal:
            other_names.append((first, (vertex + 2) % 6))
        if hx.ordinal_from_hexagon(second) <= self.max_ordinal:
            other_names.append((second, (vertex + 4) % 6))
        return other_names
