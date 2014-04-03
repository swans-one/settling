import unittest

import hex_utils

class Test_neighbors(unittest.TestCase):
    def test_origin_neighbors(self):
        """The neighbors of the origin should be equal to the delta.
        """
        deltas = [(1,0,-1), (0,1,-1), (-1,1,0),
                  (-1,0,1), (0,-1,1), (1,-1,0)]
        neighbors = hex_utils.neighbors((0, 0, 0))
        self.assertEqual(neighbors, deltas)

    def test_a_couple(self):
        """Test that a couple points are in the neighbors.
        """
        neighbors = hex_utils.neighbors((1,1,-2))
        self.assertIn((2,1,-3), neighbors)
        self.assertIn((1,2,-3), neighbors)
        self.assertIn((1,0,-1), neighbors)

class Test_hexagon_from_ordinal(unittest.TestCase):
    def test_works(self):
        """A few assertions to test that this works.

        Since the underlying componenets of this are thoroughly
        tested, this amounts to an integration test.
        """
        self.assertEqual(hex_utils.hexagon_from_ordinal(22), (0, 3, -3))
        self.assertEqual(hex_utils.hexagon_from_ordinal(11), (-2, 2, 0))
        self.assertEqual(hex_utils.hexagon_from_ordinal(32), (1, -3, 2))
        self.assertEqual(hex_utils.hexagon_from_ordinal(36), (3, -1, -2))

    def test_repeated_calculations(self):
        """Check that cache returns the same values.

        Since values, are cached, we want to make sure the lookup
        returns the same value as the calculation.
        """
        self.assertEqual(hex_utils.hexagon_from_ordinal(36), (3, -1, -2))
        self.assertEqual(hex_utils.hexagon_from_ordinal(36), (3, -1, -2))

class Test_hexagon_from_rso(unittest.TestCase):
    def test_center(self):
        """Should return (0,0,0)
        """
        hex_coord = hex_utils.hexagon_from_rso((0, 0, 0))
        self.assertEqual(hex_coord, (0,0,0))

    def test_ring_one(self):
        """If we're on the first ring, return the correct value.
        """
        hex_coord = hex_utils.hexagon_from_rso((1, 3, 0))
        self.assertEqual(hex_coord, (-1,0,1))

    def test_on_spine(self):
        """Offset == 0, (on spine) should return correctly
        """
        hex_coord = hex_utils.hexagon_from_rso((3, 4, 0))
        self.assertEqual(hex_coord, (0,-3,3))

    def test_with_offset(self):
        """Offset > 0 (off spine) should return correctly
        """
        hex_coord = hex_utils.hexagon_from_rso((3, 0, 1))
        self.assertEqual(hex_coord, (2,1,-3))

    def test_wrap_splines(self):
        """Spine of 5, should be handled correctly.

        This could potentially be an issue because there is no spine 6.
        """
        hex_coord = hex_utils.hexagon_from_rso((3, 5, 2))
        self.assertEqual(hex_coord, (3,-1,-2))


class Test_ordinal_from_hexagon(unittest.TestCase):
    def test_works(self):
        """A simple test that the correct ordinal is returned.
        """
        self.assertEqual(hex_utils.ordinal_from_hexagon((3, -1, -2)), 36)

    def test_round_trip(self):
        """Test that going through a round trip works.

        We send a value first through hexagon_from_ordinal, then
        through ordinal_from_hexagon, and compare to the original.
        """
        start_ordinal = 77
        end_hexagon = hex_utils.hexagon_from_ordinal(start_ordinal)
        end_ordinal = hex_utils.ordinal_from_hexagon(end_hexagon)
        self.assertEqual(start_ordinal, end_ordinal)

    def test_repeated_calculations(self):
        """Check that cache returns the same values.

        Since values, are cached, we want to make sure the lookup
        returns the same value as the calculation.
        """
        self.assertEqual(hex_utils.ordinal_from_hexagon((3, -1, -2)), 36)
        self.assertEqual(hex_utils.ordinal_from_hexagon((3, -1, -2)), 36)

class Test_ordinal_from_rso(unittest.TestCase):
    pass

class Test_rso_from_hexagon(unittest.TestCase):
    pass

class Test_rso_from_ordinal(unittest.TestCase):
    def test_returns_triple(self):
        """A simple test that (ring, spine, offset) is returned.

        The helper functions that go into this are more thoroughly
        unit tested.
        """
        expected = (3, 1, 1)
        rso = hex_utils.rso_from_ordinal(23)
        self.assertEqual(rso, expected)

class Test__find_ring(unittest.TestCase):
    pass

class Test__find_spine(unittest.TestCase):
    pass

class Test__find_offset(unittest.TestCase):
    pass

class Test__tiles_in_ring(unittest.TestCase):
    pass
