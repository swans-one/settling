import random
import itertools

import networkx as nx

from board_geometry import StandardBoard

DEFAULT_TILE_ORDER = ("wheat", "sheep", "wheat",
                      "sheep", "brick", "wood", "ore",
                      "wood", "ore", "wheat", "sheep", "wood",
                      "brick", "wood", "sheep", "wheat",
                      "desert", "brick", "ore")

DEFAULT_NUMBER_ORDER = (9, 10, 8, 12, 5, 4, 3, 11, 6,
                        11, 9, 6, 4, 3, 10, 2, 8, 5)

DEFAULT_PORT_ORDER = ("3:1 port", "3:1 port", "brick port", "wood port",
                      "3:1 port", "wheat port", "ore port", "3:1 port",
                      "sheep port")

TILES = list(itertools.chain(
    ["wood"] * 4,
    ["brick"] * 3,
    ["wheat"] * 4,
    ["sheep"] * 4,
    ["ore"] * 3,
    ["desert"]
))

NUMBERS = [2, 12] + list(range(3, 12)) * 2

PORTS = ["wood port", "brick port", "wheat port", "sheep port", "ore port",
         "3:1 port", "3:1 port", "3:1 port", "3:1 port"]


def random_board():
    # shuffled copies of the three lists
    tile_order = random.sample(TILES, len(TILES))
    port_order = random.sample(PORTS, len(PORTS))
    number_order = random.sample(NUMBERS, len(NUMBERS))
    return Board(tile_order, number_order, port_order)


class Board:
    def __init__(self, tile_order, number_order, port_order,
                 board_geometry=StandardBoard):
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
        self.tile_order = list(tile_order)
        self.port_order = list(port_order)
        self.number_order = list(number_order)
        self.graph = self._set_up(
            self.tile_order, self.port_order, self.number_order
        )

    def _set_up(self, tile_order, port_order, number_order):
        board_graph = nx.Graph()

        desert_index = tile_order.index("desert")
        number_order.insert(desert_index, None)
        resource_tiles = [Tile(t, n) for t, n in zip(tile_order, number_order)]
        water_tiles = [Tile("water", None) for _ in range(18)]
        tiles = resource_tiles + water_tiles

        board_graph.add_nodes_from(tiles)

        return board_graph

    def add_road(self):
        pass

    def add_settlement(self):
        pass

    def upgrade_settlement(self):
        pass

    def coord_to_node(self):
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
