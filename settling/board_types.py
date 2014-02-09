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
    def hexagon_from_ordinal(self, ordinal):
        pass

    def ordinal_from_hexagon(self, hex_coords):
        pass
