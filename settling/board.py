import random

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
        self._vertices = {}
        self._edges = {}

        # Take care of additional setup tasks
        self._set_up()

    def _set_up(self):
        number_index = 0
        tiles = []
        for tile in self._tile_order:
            if tile in game_constants.RESOURCE_TILE_TYPES:
                # Resource tiles have a number
                tiles.append(Tile(tile, self._number_order[number_index]))
                number_index += 1
            else:
                # Non-resource tiles have no number.
                tiles.append(Tile(tile, None))
        self._tiles = tiles

    def tile(self, hexagon_coord):
        ordinal = self._board_geometry.ordinal_from_hexagon(hexagon_coord)
        return self._tiles[ordinal]

    def add_road(self, hexagon_coord, edge, player):
        """Add a road on the edge between two tiles.

        It does not matter which tile is passed in as `tile_1` and
        which is passed in as `tile_2`
        """
        # Check a road doesn't already exist.
        if self.has_road(hexagon_coord, edge):
            msg = "Cannot build a road where a road already exists."
            raise GameRuleViolation(msg)

        # Check that road isn't between two water tiles.
        neighbors = self._board_geometry.hexagon_neighbors(hexagon_coord)
        current_tile_type = self.tile(hexagon_coord).tile_type
        opposite_tile_type = self.tile(neighbors[edge]).tile_type
        if current_tile_type == 'water' and opposite_tile_type == 'water':
            msg = "Road must be built adjacent to land."
            raise GameRuleViolation(msg)

        # If no error is thrown, Add the road.
        self._edges[(hexagon_coord,  edge)] = player

    def add_town(self, hexagon_coord, vertex, player):
        """Add a town to a tile's vertex for a give player.

        A vertex can be specified by any of the three possible
        tile/vertex combinations with the exact same effect.
        """
        # Check that a city or town doesn't already exist.
        h, v = hexagon_coord, vertex
        if self.has_town(h, v) or self.has_city(h, v):
            msg = "Cannot build a town where a town or city exists."
            raise GameRuleViolation(msg)

        # Check that there is at least one land tile.
        synonyms = self._board_geometry.vertex_synonyms(hexagon_coord, vertex)
        all_water = all(self.tile(h).tile_type == 'water' for h, v in synonyms)
        if all_water:
            msg = "Towns must be built near land"
            raise GameRuleViolation(msg)

        # If no error is thrown, add the city
        self._vertices[(hexagon_coord, vertex)] = (player, 'town')

    def has_road(self, hexagon_coord, edge, player=None):
        """Return True if there is a road.

        If the optional player argument is passed in, only return True
        if there is a road owned by that player.
        """
        road_coords = self._board_geometry.edge_synonyms(hexagon_coord, edge)
        road_coords.append((hexagon_coord, edge))
        if player:
            has_road = any(self._edges.get(road_coord) == player
                           for road_coord in road_coords)
        else:
            has_road = any(self._edges.get(road_coord) is not None
                           for road_coord in road_coords)
        return has_road

    def upgrade_town(self, hexagon_coord, vertex, player):
        if not self.has_town(hexagon_coord, vertex):
            msg = "Must build a town first."
            raise GameRuleViolation(msg)
        elif not self.has_town(hexagon_coord, vertex, player):
            msg = "Cannot upgrade a town you don't own"
            raise GameRuleViolation(msg)
        else:
            self._vertices[(hexagon_coord, vertex)] = (player, 'city')

    def has_town(self, hexagon_coord, vertex, player=None):
        """Return True if there is a town.

        If the optional player argument is passed in, only return True
        if there is a town owned by that player.
        """
        has_town = self._vertex_contains(
            hexagon_coord, vertex, player, 'town'
        )
        return has_town

    def has_city(self, hexagon_coord, vertex, player=None):
        """Return True if there is a city.

        If the optional player argument is passed in, only return True
        if there is a city owned by that player.
        """
        has_city = self._vertex_contains(
            hexagon_coord, vertex, player, 'city'
        )
        return has_city

    def _vertex_contains(self, hexagon_coord, vertex, player, town_or_city):
        """Does the vertex contain a given player's town/city?

        If player is None, return True for any town/city.
        """
        bg = self._board_geometry
        verts = self._vertices
        town_coords = bg.vertex_synonyms(hexagon_coord, vertex)
        town_coords.append((hexagon_coord, vertex))
        if player:
            has_town = any(verts.get(town_coord) == (player, town_or_city)
                           for town_coord in town_coords)
        else:
            has_town = any(town_or_city in verts.get(town_coord, (None, None))
                           for town_coord in town_coords)
        return has_town


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
