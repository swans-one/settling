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
