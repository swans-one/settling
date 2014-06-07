import unittest

from mock import patch

import settling.board as board
import settling.cli_player as cli_player


class Test_retry_input(unittest.TestCase):
    @patch('builtins.input', lambda x: 'four')
    def test_no_error_argument(self):
        # Since no error list, should not retry, just raise.
        @cli_player.retry_input()
        def get_three():
            three = input("Type 'three': ")
            if three not in ('3', 'three'):
                raise ValueError
            return 3
        with self.assertRaises(ValueError):
            get_three()

    @patch('builtins.input')
    def test_two_calls(self, input_mock):
        input_mock.side_effect = ['4', '3']

        @cli_player.retry_input(ValueError)
        def get_three():
            three = input("Type 'three': ")
            if three not in ('3', 'three'):
                raise ValueError
            return 3
        get_three()
        self.assertEqual(len(input_mock.mock_calls), 2)


class Test_CliPlayer_starting_town(unittest.TestCase):
    def setUp(self):
        self.player = cli_player.CliPlayer('test')
        self.board = board.standard_board()

    @patch('builtins.input')
    def test_working(self, input_mock):
        input_mock.side_effect = ['(0, 0, 0)', '0']
        hexagon_coord, vertex = self.player.starting_town(self.board)
        self.assertEqual(hexagon_coord, (0, 0, 0))
        self.assertEqual(vertex, 0)

    @patch('builtins.input')
    def test_game_rule_violation(self, input_mock):
        # Two sets of coord/vertex combos. One which is a violation,
        # and one which isn't.
        self.board.add_town((0, 0, 0), 1, 'test_b')
        input_mock.side_effect = [
            '(0, 0, 0)', '0',
            '(-1, 0, 1)', '3',
        ]
        output = self.player.starting_town(self.board)
        expected_output = ((-1, 0, 1), 3)
        self.assertEqual(output, expected_output)


class Test_hexagon_coords_from_string(unittest.TestCase):
    def test_different_input_formats(self):
        well_formed_inputs = [
            '(1, -1, 0)', '( 1, -1, 0 )', '1, -1, 0',
            ' 1 , -1 , 0 ', '( 1 , -1 , 0 )'
        ]
        expected_output = (1, -1, 0)
        for well_formed in well_formed_inputs:
            output = cli_player.hexagon_coord_from_string(well_formed)
            self.assertEqual(output, expected_output)

    def test_raises_value_error(self):
        poorly_formed = 'what'
        with self.assertRaises(ValueError):
            cli_player.hexagon_coord_from_string(poorly_formed)

    def test_illegal_coord(self):
        not_valid_coord = '(1, 2, 3)'
        with self.assertRaises(ValueError):
            cli_player.hexagon_coord_from_string(not_valid_coord)


class Test_vertex_from_string(unittest.TestCase):
    def test_just_integer_input(self):
        input_string = '4'
        output = cli_player.vertex_from_string(input_string)
        expected = 4
        self.assertEqual(output, expected)

    def test_spaces_around_input(self):
        input_string = ' 4	'
        output = cli_player.vertex_from_string(input_string)
        expected = 4
        self.assertEqual(output, expected)

    def test_poorly_formed_input(self):
        with self.assertRaises(ValueError):
            cli_player.vertex_from_string('what')

    def test_upper_out_of_bounds(self):
        with self.assertRaises(ValueError):
            cli_player.vertex_from_string('6')

    def test_lower_out_of_bounds(self):
        with self.assertRaises(ValueError):
            cli_player.vertex_from_string('-1')
