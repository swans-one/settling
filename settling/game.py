from copy import deepcopy


def game_loop(board, player1, player2, player3, player4=None):
    players = [player1, player2, player3] + ([player4] if player4 else [])

    # start by placing tiles.
    # plaers in order, then reverse order.
    for player in players + list(reversed(players)):
        player_board = deepcopy(board)
        hex_coord, vertex = player.starting_town(player_board)
        board.add_town(hex_coord, vertex, player.name)

    # Do normal turns:
    winner = None
    while winner is None:
        for player in players:
            player_board = deepcopy(board)
            action = StartAction()
            hand = None
            while action is not None:
                action = player.act(player_board, hand)
                if action:
                    apply_action(action, board)
            winner = who_won(board)
            if winner:
                break
    return winner


class StartAction:
    pass


def who_won(board):
    pass


def apply_action(action, board):
    pass
