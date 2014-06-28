from functools import wraps

from settling.exceptions import GameRuleViolation
from settling.player import Player
from settling import player_action, game_constants


def retry_input(*errors):
    """A decorator that will retry the function until success.

    Args:
      *errors - a variable number of errors to retry on.
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            while True:
                try:
                    res = f(*args, **kwargs)
                    break
                except errors as err:
                    print(err)
                    pass
            return res
        return wrapper
    return decorator


class CliPlayer(Player):
    def __init__(self, name):
        self.name = name

    def name(self):
        return self.name

    @retry_input(ValueError, GameRuleViolation)
    def starting_town(self, board):
        hexagon_prompt = "Place Town on tile: "
        vertex_prompt = "Place Town which vertex of {tile}: "
        hexagon_string = input(hexagon_prompt)
        vertex_string = input(vertex_prompt.format(tile=hexagon_string))
        hexagon_coord = hexagon_coord_from_string(hexagon_string)
        vertex = vertex_from_string(vertex_string)
        board.add_town(hexagon_coord, vertex, self.name)
        return hexagon_coord, vertex

    @retry_input(ValueError, GameRuleViolation)
    def play_action_card(self, board, hand):
        print('You have the following action cards:')
        for card in hand:
            if card not in game_constants.RESOURCE_TILE_TYPES:
                print(card)
        to_play = input('Which to play? (Return for none):')
        while to_play != '':
            _play_action(to_play)

    def act(self, board, hand):
        pass


def hexagon_coord_from_string(hexagon_string):
    """Parse a user supplied hexagon coordinate.

    Args:
      A user input string representing a hexagon_coordinate.
      Should be able to handle any of the following formats:
         - '(1, -1, 0)'
         - '( 1, -1, 0 )'
         - '1, -1, 0'
         - ' 1 , -1 , 0 '
         - '( 1 , -1 , 0 )'

    Returns:
       A tuple of ints.

    Raises:
       ValueError if the string is poorly formed.
    """
    coord = (int(c.strip()) for c in hexagon_string.strip(' ()').split(','))
    coord = tuple(coord)
    if not sum(coord) == 0:
        err = 'Not a valid hexgon coord: sum({coord}) != 0'
        raise ValueError(err.format(coord=coord))
    return coord


def vertex_from_string(vertex_string):
    """Parse a user supplied vertex.

    Args:
      A user input string representing a vertex. Should be an
      integer between 0 and 5.

    Returns:
      An int, the vertex.

    Raises:
      ValueError if the string is poorly formed, or

    """
    vertex = int(vertex_string.strip())
    if not 0 <= vertex <= 5:
        err = 'Given vertex: {vertex} must be a whole numbers between 0 and 5.'
        raise ValueError(err.format(vertex=vertex))
    return vertex
