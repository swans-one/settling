from settling.player import Player


class CliPlayer(Player):
    def __init__(self, name):
        self.name = name

    def name(self):
        return self.name

    def starting_town(self, board):
        validated = False
        hexagon_prompt = "Place Town on tile: "
        vertex_prompt = "Place Town which vertex of {tile}: "
        while not validated:
            hexagon_string = input(hexagon_prompt)
            vertex_string = input(vertex_prompt.format(tile=hexagon_string))
            try:
                hexagon_coord = hexagon_coord_from_string(hexagon_string)
                vertex = vertex_from_string(vertex_string)
            except ValueError:
                continue
            validated = True
        return hexagon_coord, vertex

    def play_action_card(self, board, hand):
        pass

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
