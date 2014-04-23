import unittest
from unittest.mock import MagicMock

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


class Test_Board__connect_tiles(unittest.TestCase):
    def setUp(self):
        """Pin the method under test to a mock object.
        """
        self.board = MagicMock()
        self.board._connect_tiles = board.Board._connect_tiles

    def test_returns_graph(self):
        input_tiles = ['a', 'b', 'c']
        input_graph = nx.Graph()
        out_graph = self.board._connect_tiles(
            self.board, input_tiles, input_graph
        )
        self.assertIsInstance(out_graph, nx.Graph)

    def test_connects_three(self):
        """Test a simple set of neighbors.
        """
        input_tiles = ['a', 'b', 'c']
        self.board._board_geometry.hexagon_neighbors.return_value = ['d']
        input_graph = nx.Graph()
        out_graph = self.board._connect_tiles(
            self.board, input_tiles, input_graph
        )
        self.assertTrue(
            ('a', 'd') in out_graph.edges() or ('d', 'a') in out_graph.edges())
        self.assertTrue(
            ('b', 'd') in out_graph.edges() or ('d', 'b') in out_graph.edges())
        self.assertTrue(
            ('c', 'd') in out_graph.edges() or ('d', 'c') in out_graph.edges())

class Test_Board_add_road(unittest.TestCase):
    def setUp(self):
        """Pin the method under test to a mock object.
        """
        self.board = MagicMock()
        self.board._graph = nx.Graph()
        self.board._graph.add_edge('a', 'b')
        self.board.add_road = board.Board.add_road

    def test_adds_key_value(self):
        """Did the key and the value make it in?
        """
        self.board.add_road(self.board, 'a', 'b', 'player1')
        self.assertEqual(self.board._graph['b']['a']['road'], 'player1')

class Test_Board_add_town(unittest.TestCase):
    def setUp(self):
        """Pin the method under test to a mock object.
        """
        self.board = MagicMock()
        self.board._vertices = {}
        self.board.add_town = board.Board.add_town

    def test_town_added(self):
        self.board.add_town(self.board, (0, 0, 0), 0, 'player1')
        self.assertEqual(len(self.board._vertices), 1)
