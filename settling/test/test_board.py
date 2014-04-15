import unittest

import networkx as nx

from board_geometry import StandardBoard
import board
import game_constants


class Test_random_standard_board(unittest.TestCase):
    def test_returns_board(self):
        """We just check that a board object is returned
        """
        random_standard_board = board.random_standard_board()
        self.assertIsInstance(random_standard_board, board.Board)


class Test_Board__set_up(unittest.TestCase):
    def setUp(self):
        self.tiles = game_constants.STANDARD_TILE_ORDER
        self.numbers = game_constants.STANDARD_NUMBER_ORDER
        self.ports = game_constants.STANDARD_PORT_MAP
        self.board_geom = StandardBoard()

    def test_returns_graph_object(self):
        b = board.Board(self.tiles, self.numbers, self.ports, self.board_geom)
        self.assertIsInstance(b._graph, nx.Graph)
