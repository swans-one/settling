"""The main game logic code.

The code in this module keeps track of:

  1) The global board state.
  2) The global state of players' hands.
  3) The progression of turns
  4) When a victory condition has been reached.

The code in this module is responsible for dispatching all actions to
the appropriate players. It is also responsible for modifying global
game state based on these actions.

As a design principle, a piece of mutable global state should never be
passed to players. Instead, copies of that state, that players can
modify locally should be passed in instead.
"""

from copy import deepcopy

from settling.hand import Hand
import settling.player_actions as player_action


class Game:
    def __init__(self, board, players, roll):
        self.board = board
        self.players = players
        self.roll = roll
        self.hands = {player.name: Hand() for player in players}

    def game_loop(self):
        """Perform the main game loop.
        """
        self._board_set_up()
        winner = None
        while winner is None:
            for player in self.players:
                self._player_turn(player)
                winner = who_won(self.board)
                if winner:
                    break
        return winner

    def _board_set_up(self):
        """Initial settlement placement. Initial resource distribtuion.
        """
        for player in self.players:
            player_board = deepcopy(self.board)
            hexagon_coord, vertex = player.starting_town(player_board)
            self.board.add_town(hexagon_coord, vertex, player.name)
        for player in reversed(self.players):
            player_board = deepcopy(self.board)
            hexagon_coord, vertex = player.starting_town(player_board)
            self.board.add_town(hexagon_coord, vertex, player.name)
            resources = initial_resources(hexagon_coord, vertex)
            self.hands[player.name].add_resources(resources)

    def _player_turn(self, player):
        # Turn set up:
        #   - Initial action card?
        #   - roll
        #   - Move robber or distribute resources
        player_board = deepcopy(self.board)
        player_hand = deepcopy(self.hands[player.name])
        action = player.play_action_card(player_board, player_hand)
        if isinstance(action, player_action.PlayActionCard):
            self._apply_action(action)
        number = self.roll()
        player_board = deepcopy(self.board)
        player_hand = deepcopy(self.hands[player.name])
        if number == 7:
            self._move_robber()
        else:
            self._distribute_resources(number)

        # Regular turn:
        player_board = deepcopy(self.board)
        player_hand = deepcopy(self.hands[player.name])
        action = player_action.StartTurn()
        while not isinstance(action, player_action.EndTurn):
            self._apply_action(action)
            action = player.act(player_board, player_hand)

    def _move_robber(self):
        pass

    def _distribute_resources(self, number):
        for player in self.players:
            resources = draw_player_resources(self.board, player, number)
            self.hands[player.name].add_resources(resources)

    def _apply_action(action):
        pass


def who_won(board):
    pass


def draw_player_resources(board, player, number):
    pass


def initial_resources(hex_coord, vertex):
    pass
