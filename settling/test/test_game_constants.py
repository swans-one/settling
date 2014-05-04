import unittest

from settling import game_constants


class Test_Standards(unittest.TestCase):
    """Do a double check that the game rules are reflected in the constant
    objects.

    This class only tests the standard game mode objects.
    """

    def test_land_tile_count(self):
        """19 land tiles.
        """
        self.assertEqual(len(game_constants.STANDARD_LAND_TILE_ORDER), 19)

    def test_total_tile_count(self):
        """37 total tiles.
        """
        self.assertEqual(len(game_constants.STANDARD_TILE_ORDER), 37)

    def test_total_number_count(self):
        """18 numbers, to correspond with resource tiles.
        """
        self.assertEqual(len(game_constants.STANDARD_NUMBER_ORDER), 18)
