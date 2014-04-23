import random

import networkx as nx

from exceptions import GameRuleViolation
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
    return Board(tile_order, number_order, port_order, StandardBoard())


class Board:
    def __init__(self, tile_order, number_order, port_map, board_geometry):
        """Set up a board from order of tiles/numbers/port/geometry.

        Since a board is completely determined by the arrangement of
        tiles, numbers, ports and the shape of the board, these
        are the requirements to initialize a board.

        The layout of the board is handled by the board_geometry
        methods. The role of this class is to provide simple views
        into the board and to support the addition of roads and
        settlements/cities.
        """
        self._tile_order = tile_order
        self._number_order = number_order
        self._port_map = port_map
        self._board_geometry = board_geometry
        self._graph = self._set_up(
            self._tile_order, self._port_map, self._number_order
        )
        self._vertices = {}

    def _set_up(self, tile_order, port_order, number_order):
        """Create a graph based on tiles, ports, and numbers.

        Used to set up an initial self._graph object.
        """
        board_graph = nx.Graph()
        number_index = 0
        tiles = []
        for tile in tile_order:
            if tile in game_constants.RESOURCE_TILE_TYPES:
                # Resource tiles have a number
                tiles.append(Tile(tile, number_order[number_index]))
                number_index += 1
            else:
                # Non-resource tiles have no number.
                tiles.append(Tile(tile, None))
        board_graph = self._connect_tiles(tiles, board_graph)
        return board_graph

    def _connect_tiles(self, tiles, graph):
        """Create an connection between each tile  and its neighbors.

        For each of the tiles in the `tiles` argument, this method
        finds its neighbors based on the board geometry and adds an
        edge in the graph, connecting the tile and each neighbor.
        """
        graph.add_nodes_from(tiles)
        for i, tile in enumerate(tiles):
            board_geo = self._board_geometry
            hexagon_coord = board_geo.hexagon_from_ordinal(i)
            tile_neighbors = board_geo.hexagon_neighbors(hexagon_coord)
            connected = zip([tile] * len(tile_neighbors), tile_neighbors)
            graph.add_edges_from(connected)
        return graph

    def add_road(self, tile_1, tile_2, player):
        """Add a road on the edge between two tiles.

        It does not matter which tile is passed in as `tile_1` and
        which is passed in as `tile_2`
        """
        self._graph[tile_1][tile_2]['road'] = player

    def add_town(self, hexagon_coord, vertex, player):
        """Add a town to a tile's vertex for a give player.

        A vertex can be specified by any of the three possible
        tile/vertex combinations with the exact same effect.
        """
        self._vertices[(hexagon_coord, vertex)] = (player, 'town')

    def has_road(self, tile_1, tile_2, player=None):
        """Return True if there is a road.

        If the optional player argument is passed in, only return True
        if there is a road owned by that player.
        """
        pass

    def has_town(self, hexagon_coord, vertex, player=None):
        """Return True if there is a town.

        If the optional player argument is passed in, only return True
        if there is a town owned by that player.
        """
        pass

    def has_city(self, hexagon_coord, vertex, player=None):
        """Return True if there is a city.

        If the optional player argument is passed in, only return True
        if there is a city owned by that player.
        """
        pass

    def upgrade_town(self):
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


class Port:
    def __init__(self, port_type):
        self.port_type = port_type
