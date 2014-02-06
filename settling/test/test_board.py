import unittest
from board import Board, make_random_board

class Test_Board__set_up(unittest.TestCase):
    def setUp(self):
        self.board = Board(["desert"],[],[])

    def test_returns_graph_object(self):
        Board._set_up(None, ["wood", "desert"], [8], [])
