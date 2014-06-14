"""Board types are mappings between a hexagonal coordinate system and
ordinal numbers.

This mapping allows for different board sizes to be defined, and a
simple list of tiles/numbers/ports to be passed in for the
construction.

Currently the only board type defined is the standard 3-4 player
board.
"""

from abc import ABCMeta, abstractmethod

from settling import hexagon_utils as hx


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
    def edge_synonyms(self, hexagon_coord, edge):
        """Return all ways of addressing a given edge.
        """
        pass

    @abstractmethod
    def vertex_synonyms(self, hexagon_coord, vertex):
        """Return all ways of addressing a given vertex.
        """
        pass

    @abstractmethod
    def vertex_neighbors(self, hexagon_coord, vertex):
        """Return a cordinate for all the nearby vertices.
        """
        pass

    @abstractmethod
    def vertices_around_edge(self, hexagon_coord, edge):
        """Return the veticies around an edge.
        """
        pass

    @abstractmethod
    def edges_around_vertex(self, hexagon_coord, vertex):
        """Return the edges around a vertex.
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
        self.max_ordinal = 36     # 36 is max ordinal for 37 tiles

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

    def edge_synonyms(self, hexagon_coord, edge):
        all_neighbors = hx.neighbors(hexagon_coord)
        other = all_neighbors[edge]
        other_edge = (edge + 3) % 6
        if hx.ordinal_from_hexagon(other) <= self.max_ordinal:
            return [(hexagon_coord, edge), (other, other_edge)]
        else:
            return [(hexagon_coord, edge)]

    def vertex_synonyms(self, hexagon_coord, vertex):
        all_neighbors = hx.neighbors(hexagon_coord)
        first = all_neighbors[vertex - 1]
        second = all_neighbors[vertex]
        synonyms = [(hexagon_coord, vertex)]
        if hx.ordinal_from_hexagon(first) <= self.max_ordinal:
            synonyms.append((first, (vertex + 2) % 6))
        if hx.ordinal_from_hexagon(second) <= self.max_ordinal:
            synonyms.append((second, (vertex + 4) % 6))
        return synonyms

    def vertex_neighbors(self, hexagon_coord, vertex):
        synonyms = self.vertex_synonyms(hexagon_coord, vertex)
        if len(synonyms) == 3:
            neighbors = {(h, (v - 1) % 6) for h, v in synonyms}
        elif len(synonyms) == 2:
            neighbors = {(h, (v - 1) % 6) for h, v in synonyms}
            neighbors.add((synonyms[0][0], (synonyms[0][1] + 1) % 6))
        elif len(synonyms) == 1:
            neighbors = {
                (hexagon_coord, (vertex + 1) % 6),
                (hexagon_coord, (vertex - 1) % 6)
            }
        return neighbors

    def vertices_around_edge(self, hexagon_coord, edge):
        """Return the veticies around an edge.
        """
        pass

    def edges_around_vertex(self, hexagon_coord, vertex):
        """Return the edges around a vertex.
        """
        pass
