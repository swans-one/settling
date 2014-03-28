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
        
        

