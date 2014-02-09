import unittest

import board_types

class Test_StandardBoardType_hexagon_from_ring_spine_offset(unittest.TestCase):
    def setUp(self):
        """Create an instance of the standard board type.
        """
        self.bt = board_types.StandardBoardType()

    def test_center(self):
        """Should return (0,0,0)
        """
        hex_coord = self.bt.hexagon_from_ring_spine_offset(ring=0, spine=0, offset=0)
        self.assertEqual(hex_coord, (0,0,0))

    def test_ring_one(self):
        """If we're on the first ring, return the correct value.
        """
        hex_coord = self.bt.hexagon_from_ring_spine_offset(ring=1, spine=3, offset=0)
        self.assertEqual(hex_coord, (-1,0,1))

    def test_on_spine(self):
        """Offset == 0, (on spine) should return correctly
        """
        hex_coord = self.bt.hexagon_from_ring_spine_offset(ring=3, spine=4, offset=0)
        self.assertEqual(hex_coord, (0,-3,3))

    def test_with_offset(self):
        """Offset > 0 (off spine) should return correctly
        """
        hex_coord = self.bt.hexagon_from_ring_spine_offset(ring=3, spine=0, offset=1)
        self.assertEqual(hex_coord, (2,1,-3))

    def test_wrap_splines(self):
        """Spine of 5, should be handled correctly.

        This could potentially be an issue because there is no spine 6.
        """
        hex_coord = self.bt.hexagon_from_ring_spine_offset(ring=3, spine=5, offset=2)
        self.assertEqual(hex_coord, (3,-1,-2))

