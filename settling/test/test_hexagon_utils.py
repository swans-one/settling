import unittest

import hexagon_utils as hx


class Test_neighbors(unittest.TestCase):
    def test_origin_neighbors(self):
        """The neighbors of the origin should be equal to the delta.
        """
        deltas = [(1, 0, -1), (0, 1, -1), (-1, 1, 0),
                  (-1, 0, 1), (0, -1, 1), (1, -1, 0)]
        neighbors = hx.neighbors((0, 0, 0))
        self.assertEqual(neighbors, deltas)

    def test_a_couple(self):
        """Test that a couple points are in the neighbors.
        """
        neighbors = hx.neighbors((1, 1, -2))
        self.assertIn((2, 1, -3), neighbors)
        self.assertIn((1, 2, -3), neighbors)
        self.assertIn((1, 0, -1), neighbors)


class Test_hexagon_from_ordinal(unittest.TestCase):
    def test_works(self):
        """A few assertions to test that this works.

        Since the underlying componenets of this are thoroughly
        tested, this amounts to an integration test.
        """
        self.assertEqual(hx.hexagon_from_ordinal(22), (0, 3, -3))
        self.assertEqual(hx.hexagon_from_ordinal(11), (-2, 2, 0))
        self.assertEqual(hx.hexagon_from_ordinal(32), (1, -3, 2))
        self.assertEqual(hx.hexagon_from_ordinal(36), (3, -1, -2))

    def test_repeated_calculations(self):
        """Check that cache returns the same values.

        Since values, are cached, we want to make sure the lookup
        returns the same value as the calculation.
        """
        self.assertEqual(hx.hexagon_from_ordinal(36), (3, -1, -2))
        self.assertEqual(hx.hexagon_from_ordinal(36), (3, -1, -2))


class Test_hexagon_from_rso(unittest.TestCase):
    def test_center(self):
        """Should return (0,0,0)
        """
        hex_coord = hx.hexagon_from_rso((0, 0, 0))
        self.assertEqual(hex_coord, (0, 0, 0))

    def test_ring_one(self):
        """If we're on the first ring, return the correct value.
        """
        hex_coord = hx.hexagon_from_rso((1, 3, 0))
        self.assertEqual(hex_coord, (-1, 0, 1))

    def test_on_spine(self):
        """Offset == 0, (on spine) should return correctly
        """
        hex_coord = hx.hexagon_from_rso((3, 4, 0))
        self.assertEqual(hex_coord, (0, -3, 3))

    def test_with_offset(self):
        """Offset > 0 (off spine) should return correctly
        """
        hex_coord = hx.hexagon_from_rso((3, 0, 1))
        self.assertEqual(hex_coord, (2, 1, -3))

    def test_wrap_splines(self):
        """Spine of 5, should be handled correctly.

        This could potentially be an issue because there is no spine 6.
        """
        hex_coord = hx.hexagon_from_rso((3, 5, 2))
        self.assertEqual(hex_coord, (3, -1, -2))


class Test_ordinal_from_hexagon(unittest.TestCase):
    def test_works(self):
        """A simple test that the correct ordinal is returned.
        """
        self.assertEqual(hx.ordinal_from_hexagon((3, -1, -2)), 36)

    def test_round_trip(self):
        """Test that going through a round trip works.

        We send a value first through hexagon_from_ordinal, then
        through ordinal_from_hexagon, and compare to the original.
        """
        start_ordinal = 77
        end_hexagon = hx.hexagon_from_ordinal(start_ordinal)
        end_ordinal = hx.ordinal_from_hexagon(end_hexagon)
        self.assertEqual(start_ordinal, end_ordinal)

    def test_repeated_calculations(self):
        """Check that cache returns the same values.

        Since values, are cached, we want to make sure the lookup
        returns the same value as the calculation.
        """
        self.assertEqual(hx.ordinal_from_hexagon((3, -1, -2)), 36)
        self.assertEqual(hx.ordinal_from_hexagon((3, -1, -2)), 36)


class Test_ordinal_from_rso(unittest.TestCase):
    def test_works(self):
        """Test that the correct ordinal is returned from the rso.
        """
        start_rso = (3, 0, 2)
        expected_ordinal = 21
        result_ordinal = hx.ordinal_from_rso(start_rso)
        self.assertEqual(result_ordinal, expected_ordinal)


class Test_rso_from_hexagon(unittest.TestCase):
    def test_works(self):
        """Test that the correct rso is returned from the hexagon.
        """
        start_hexagon = (0, -1, 1)
        expected_rso = (1, 4, 0)
        result_rso = hx.rso_from_hexagon(start_hexagon)
        self.assertEqual(result_rso, expected_rso)


class Test_rso_from_ordinal(unittest.TestCase):
    def test_returns_triple(self):
        """A simple test that (ring, spine, offset) is returned.

        The helper functions that go into this are more thoroughly
        unit tested.
        """
        expected = (3, 1, 1)
        rso = hx.rso_from_ordinal(23)
        self.assertEqual(rso, expected)


class Test__find_ring(unittest.TestCase):
    """Test the recursive traversal of the triangular numbers.
    """
    def test_ring_zero(self):
        """Ordinal 0 -> ring 0.
        """
        expected_ring = 0
        ring = hx._find_ring(0)
        self.assertEqual(ring, expected_ring)

    def test_ring_one(self):
        """Ordinal 6 -> ring 1.
        """
        expected_ring = 1
        ring = hx._find_ring(6)
        self.assertEqual(ring, expected_ring)

    def test_ring_four(self):
        """Ordinal 43 -> ring 4.
        """
        expected_ring = 4
        ring = hx._find_ring(43)
        self.assertEqual(ring, expected_ring)


class Test__find_spine(unittest.TestCase):
    def test_ring_zero(self):
        """Spine should be zero on ordinal zero, ring zero.
        """
        expected_spine = 0
        spine = hx._find_spine(0, 0)
        self.assertEqual(spine, expected_spine)

    def test_ring_one(self):
        expected_spine = 2
        spine = hx._find_spine(3, 1)
        self.assertEqual(spine, expected_spine)

    def test_ring_three(self):
        expected_spine = 0
        spine = hx._find_spine(19, 3)
        self.assertEqual(spine, expected_spine)

    def test_ring_four(self):
        expected_spine = 5
        spine = hx._find_spine(60, 4)
        self.assertEqual(spine, expected_spine)


class Test__find_offset(unittest.TestCase):
    def test_ring_zero(self):
        expected_offset = 0
        offset = hx._find_offset(0, 0)
        self.assertEqual(offset, expected_offset)

    def test_ring_4_offset_zero(self):
        expected_offset = 0
        offset = hx._find_offset(37, 4)
        self.assertEqual(offset, expected_offset)

    def test_ring_4_offset_three(self):
        expected_offset = 3
        offset = hx._find_offset(60, 4)
        self.assertEqual(offset, expected_offset)


class Test__tiles_in_ring(unittest.TestCase):
    def test_ring_zero(self):
        tiles = hx._tiles_in_ring(0)
        self.assertEqual(tiles, 1)

    def test_ring_five(self):
        tiles = hx._tiles_in_ring(5)
        self.assertEqual(tiles, 30)
