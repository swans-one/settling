from unittest.mock import MagicMock
import unittest

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

    def test_creates_tiles(self):
        b = board.Board(self.tiles, self.numbers, self.ports, self.board_geom)
        self.assertTrue(b._tiles)


class Test_Board_add_road(unittest.TestCase):
    def setUp(self):
        """Pin the method under test to a mock object.
        """
        self.board = MagicMock()
        self.board._edges = {}
        self.board.add_road = board.Board.add_road

    def test_road_added(self):
        """Adding a town should increase `_edges` by one.
        """
        self.board.add_road(self.board, (0, 0, 0), 0, 'player1')
        self.assertEqual(len(self.board._edges), 1)


class Test_Board_add_town(unittest.TestCase):
    def setUp(self):
        """Pin the method under test to a mock object.
        """
        self.board = MagicMock()
        self.board._vertices = {}
        self.board.add_town = board.Board.add_town

    def test_town_added(self):
        """Adding a town should increase `_vertices` by one.
        """
        self.board.add_town(self.board, (0, 0, 0), 0, 'player1')
        self.assertEqual(len(self.board._vertices), 1)


class Test_Board_has_road(unittest.TestCase):
    def setUp(self):
        """Pin the method under test to a mock object.
        """
        self.board = MagicMock()
        self.board._edges = {}
        self.board._board_geometry = StandardBoard()
        self.board.add_road = board.Board.add_road
        self.board.has_road = board.Board.has_road

    def test_same_hexagon_edge(self):
        """Add the road, then it should be there.
        """
        self.board.add_road(self.board, (1, 0, -1), 3, 'player1')
        has_road = self.board.has_road(self.board, (1, 0, -1), 3, 'player1')
        self.assertTrue(has_road)

    def test_alternate_hexagon_edge(self):
        """Add the road, then checking a synonym should return true.
        """
        self.board.add_road(self.board, (1, 0, -1), 3, 'player1')
        has_road = self.board.has_road(self.board, (0, 0, 0), 0, 'player1')
        self.assertTrue(has_road)
