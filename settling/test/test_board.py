import unittest

import networkx as nx

import board


class Test_random_board(unittest.TestCase):
    def test_returns_board(self):
        """We just check that a board object is returned
        """
        random_board = board.random_board()
        self.assertIsInstance(random_board, board.Board)


class Test_Board__set_up(unittest.TestCase):
    def setUp(self):
        self.tiles = board.DEFAULT_TILE_ORDER
        self.numbers = board.DEFAULT_NUMBER_ORDER
        self.ports = board.DEFAULT_PORT_ORDER

    def test_returns_graph_object(self):
        b = board.Board(self.tiles, self.numbers, self.ports)
        self.assertIsInstance(b.graph, nx.Graph)
