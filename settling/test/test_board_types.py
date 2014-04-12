import unittest

import board_types


class Test_StandardBoardType_ordinal_from_hexagon(unittest.TestCase):
    def setUp(self):
        """Create an instance of the standard board type.
        """
        self.bt = board_types.StandardBoardType()

    def test_works(self):
        """A simple test that the correct ordinal is returned.
        """
        self.assertEqual(self.bt.ordinal_from_hexagon((3, -1, -2)), 36)

    def test_round_trip(self):
        """Test that going through a round trip works.

        We send a value first through hexagon_from_ordinal, then
        through ordinal_from_hexagon, and compare to the original.
        """
        start_ordinal = 77
        end_hexagon = self.bt.hexagon_from_ordinal(start_ordinal)
        end_ordinal = self.bt.ordinal_from_hexagon(end_hexagon)
        self.assertEqual(start_ordinal, end_ordinal)

    def test_repeated_calculations(self):
        """Check that cache returns the same values.

        Since values, are cached, we want to make sure the lookup
        returns the same value as the calculation.
        """
        self.assertEqual(self.bt.ordinal_from_hexagon((3, -1, -2)), 36)
        self.assertEqual(self.bt.ordinal_from_hexagon((3, -1, -2)), 36)


class Test_StandardBoardType_hexagon_from_ordinal(unittest.TestCase):
    def setUp(self):
        """Create an instance of the standard board type.
        """
        self.bt = board_types.StandardBoardType()

    def test_works(self):
        """A few assertions to test that this works.

        Since the underlying componenets of this are thoroughly
        tested, this amounts to an integration test.
        """
        self.assertEqual(self.bt.hexagon_from_ordinal(22), (0, 3, -3))
        self.assertEqual(self.bt.hexagon_from_ordinal(11), (-2, 2, 0))
        self.assertEqual(self.bt.hexagon_from_ordinal(32), (1, -3, 2))
        self.assertEqual(self.bt.hexagon_from_ordinal(36), (3, -1, -2))

    def test_repeated_calculations(self):
        """Check that cache returns the same values.

        Since values, are cached, we want to make sure the lookup
        returns the same value as the calculation.
        """
        self.assertEqual(self.bt.hexagon_from_ordinal(36), (3, -1, -2))
        self.assertEqual(self.bt.hexagon_from_ordinal(36), (3, -1, -2))
