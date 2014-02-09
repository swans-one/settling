import unittest

import board_types


class Test_StandardBoardType_ring_spine_offset_from_ordinal(unittest.TestCase):
    def setUp(self):
        """Create an instance of the standard board type.
        """
        self.bt = board_types.StandardBoardType()

    def test_returns_triple(self):
        """A simple test that (ring, spine, offset) is returned.

        The helper functions that go into this are more thoroughly
        unit tested.
        """
        expected = (3, 1, 1)
        ring, spine, offset = self.bt.ring_spine_offset_from_ordinal(23)
        self.assertEqual((ring, spine, offset), expected)


class Test_StandardBoardType__find_ring(unittest.TestCase):
    """Test the recursive traversal of the triangular numbers.
    """
    def setUp(self):
        """Create an instance of the standard board type.
        """
        self.bt = board_types.StandardBoardType()

    def test_ring_zero(self):
        """Ordinal 0 -> ring 0.
        """
        expected_ring = 0
        ring = self.bt._find_ring(0)
        self.assertEqual(ring, expected_ring)

    def test_ring_one(self):
        """Ordinal 6 -> ring 1.
        """
        expected_ring = 1
        ring = self.bt._find_ring(6)
        self.assertEqual(ring, expected_ring)

    def test_ring_four(self):
        """Ordinal 43 -> ring 4.
        """
        expected_ring = 4
        ring = self.bt._find_ring(43)
        self.assertEqual(ring, expected_ring)


class Test_StandardBoardType__find_spine(unittest.TestCase):
    def setUp(self):
        """Create an instance of the standard board type.
        """
        self.bt = board_types.StandardBoardType()

    def test_ring_zero(self):
        """Spine should be zero on ordinal zero, ring zero.
        """
        expected_spine = 0
        spine = self.bt._find_spine(0, 0)
        self.assertEqual(spine, expected_spine)

    def test_ring_one(self):
        expected_spine = 2
        spine = self.bt._find_spine(3, 1)
        self.assertEqual(spine, expected_spine)

    def test_ring_three(self):
        expected_spine = 0
        spine = self.bt._find_spine(19, 3)
        self.assertEqual(spine, expected_spine)

    def test_ring_four(self):
        expected_spine = 5
        spine = self.bt._find_spine(60, 4)
        self.assertEqual(spine, expected_spine)

class Test_StandardBoardType__find_offset(unittest.TestCase):
    def setUp(self):
        """Create an instance of the standard board type.
        """
        self.bt = board_types.StandardBoardType()

    def test_ring_zero(self):
        expected_offset = 0
        offset = self.bt._find_offset(0, 0)
        self.assertEqual(offset, expected_offset)

    def test_ring_4_offset_zero(self):
        expected_offset = 0
        offset = self.bt._find_offset(37, 4)
        self.assertEqual(offset, expected_offset)

    def test_ring_4_offset_three(self):
        expected_offset = 3
        offset = self.bt._find_offset(60, 4)
        self.assertEqual(offset, expected_offset)


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

