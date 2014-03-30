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
    pass

class Test_hexagon_from_rso(unittest.TestCase):
    pass

class Test_ordinal_from_hexagon(unittest.TestCase):
    pass

class Test_ordinal_from_rso(unittest.TestCase):
    pass

class Test_rso_from_hexagon(unittest.TestCase):
    pass

class Test_rso_from_ordinal(unittest.TestCase):
    pass

class Test__find_ring(unittest.TestCase):
    pass

class Test__find_spine(unittest.TestCase):
    pass

class Test__find_offset(unittest.TestCase):
    pass

class Test__tiles_in_ring(unittest.TestCase):
    pass
