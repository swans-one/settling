import random

import networkx as nx

from board_geometry import StandardBoard
import game_constants


def random_standard_board():
    # shuffled copies of the three lists
    tile_order = random.sample(
        game_constants.STANDARD_LAND_TILE_ORDER,
        len(game_constants.STANDARD_LAND_TILE_ORDER)
    )
    number_order = random.sample(
        game_constants.STANDARD_NUMBER_ORDER,
        len(game_constants.STANDARD_NUMBER_ORDER)
    )
    port_order = game_constants.STANDARD_PORT_MAP
    return Board(tile_order, number_order, port_order, StandardBoard)


class Board:
    def __init__(self, tile_order, number_order, port_map, board_geometry):
        """Set up a board from order of tiles/numbers/port.

        Since a board is completely determined by the arrangement of
        tiles, numbers, and ports we only require that these be passed
        in as lists.

        Tile order is defined to be five rows of tiles, where the i'th
        row has [3, 4, 5, 4, 3] tiles in it respectively. Flattening
        this left to right, top to bottom gives the one dimensional
        tile order.

        Number order is defined in the same way as tile order, but the
        list is shorter in length by one, since the desert, wherever
        it is, is ommitted from the list of numbers.

        Port order is defined clockwise from the top-left port. This
        port is on the third connection from the
        top-left-vertex. Proceeding from this edge there are two blank
        connections and then a connection with a port.
        """
        self._tile_order = tile_order
        self._port_map = port_map
        self._number_order = number_order
        self._graph = self._set_up(
            self._tile_order, self._port_map, self._number_order
        )

    def _set_up(self, tile_order, port_order, number_order):
        board_graph = nx.Graph()
        number_index = 0
        tiles = []
        for tile in tile_order:
            if tile in game_constants.RESOURCE_TILE_TYPES:
                print(tile, number_index, number_order[number_index])
                # Resource tiles have a number
                tiles.append(Tile(tile, number_order[number_index]))
                number_index += 1
            else:
                # Non-resource tiles have no number.
                tiles.append(Tile(tile, None))
        board_graph.add_nodes_from(tiles)
        return board_graph

    def add_road(self):
        pass

    def add_settlement(self):
        pass

    def upgrade_settlement(self):
        pass

class Tile:
    """
    Possible Tile Types:
       ["water", "wood", "brick", "wheat", "sheep", "ore", "desert"]

    Possible Numbers:
       1-6, 8-12
    """
    def __init__(self, tile_type, number, has_robber=False):
        self.tile_type = tile_type
        self.number = number
        self.has_robber = has_robber


class Vertex:
    def __init__(self, settlement=None):
        self.settlement = settlement


class Connection:
    def __init__(self, road=None):
        self.road = road


class Port:
    def __init__(self, port_type):
        self.port_type = port_type
