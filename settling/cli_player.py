from settling.player import Player


class CliPlayer(Player):
    def __init__(self, name):
        self.name = name

    def name(self):
        return self.name

    def starting_town(self, board):
        validated = False
        hexagon_prompt = "Place Town on tile: "
        vertex_prompt = "Place Town which vertext of {tile}"
        while invalidated:
            hexagon_string = input(hexagon_prompt)
            vertex_string = input(vertex_prompt.format(tile=hexagon_string))
            try:
                hexagon_coord = hexagon_coord_fro
            except ValueError:
                continue
        return

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
       ValueError if the string is bad
    """
    coords = (int(c.strip()) for c in hexagon_string.strip(' ()').split(','))
    return tuple(coords)
