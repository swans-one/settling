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
