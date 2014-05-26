import unittest

import settling.cli_player as cli_player


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
