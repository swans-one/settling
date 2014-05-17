from copy import deepcopy

from settling.hand import Hand
import settling.player_actions as player_action


def game_loop(board, roll, player1, player2, player3, player4=None):
    # Create players list and hand mapping
    players = [player1, player2, player3] + ([player4] if player4 else [])
    hands = {player.name: Hand() for player in players}

    # start by placing tiles.
    # players in order, then reverse order.
    for player in players:
        player_board = deepcopy(board)
        hexagon_coord, vertex = player.starting_town(player_board)
        board.add_town(hexagon_coord, vertex, player.name)
    for player in reversed(players):
        player_board = deepcopy(board)
        hexagon_coord, vertex = player.starting_town(player_board)
        board.add_town(hexagon_coord, vertex, player.name)
        resources = initial_resources(hexagon_coord, vertex)
        hands[player.name].add_resources(resources)

    # Do normal turns:
    winner = None
    while winner is None:
        for player in players:
            # Roll, draw cards, move robber.
            number = roll()
            player_board = deepcopy(board)
            player_hand = deepcopy(hands[player.name])
            if number == 7:
                action = player.play_action_card(player_board, player_hand)
                if isinstance(action, player_action.PlayActionCard):
                    apply_action(action, board, players, hands)
                move_robber(player, board)
            else:
                for player in players:
                    resources = draw_player_resources(board, player, number)
                    hands[player.name].add_resources(resources)

            # Start regular turn
            player_board = deepcopy(board)
            player_hand = deepcopy(hands[player.name])
            action = player_action.StartTurn()
            while not isinstance(action, player_action.EndTurn):
                action = player.act(player_board, player_hand)
                if action:
                    apply_action(action, board, players, hands)
            winner = who_won(board)
            if winner:
                break
    return winner


def who_won(board):
    pass


def apply_action(action, board):
    pass


def draw_player_resources(board, player, number):
    pass


def initial_resources(hex_coord, vertex):
    pass


def move_robber(player, board):
    pass
