import unittest
import board

class Test_random_board():
    def test_returns_board(self):
        """We just check that a board object is returned
        """
        random_board = board.random_board
        self.assertIsInstance(random_board, Board)

class Test_Board__set_up(unittest.TestCase):
    def setUp(self):
        self.numbers = [2] + [12] + list(range(3,12)) + list(range(3,12))
        self.tiles = 
        self.tiles = DEFAULT_PORT_ORDER

    def test_returns_graph_object(self):
        board.Board._set_up(None, ["wood", "desert"], [8], [])
