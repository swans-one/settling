import unittest

from settling import board_geometry


class Test_StandardBoard_ordinal_from_hexagon(unittest.TestCase):
    def setUp(self):
        """Create an instance of the standard board type.
        """
        self.geometry = board_geometry.StandardBoard()

    def test_works(self):
        """A simple test that the correct ordinal is returned.
        """
        self.assertEqual(self.geometry.ordinal_from_hexagon((3, -1, -2)), 36)

    def test_round_trip(self):
        """Test that going through a round trip works.

        We send a value first through hexagon_from_ordinal, then
        through ordinal_from_hexagon, and compare to the original.
        """
        start_ordinal = 77
        end_hexagon = self.geometry.hexagon_from_ordinal(start_ordinal)
        end_ordinal = self.geometry.ordinal_from_hexagon(end_hexagon)
        self.assertEqual(start_ordinal, end_ordinal)

    def test_repeated_calculations(self):
        """Check that cache returns the same values.

        Since values, are cached, we want to make sure the lookup
        returns the same value as the calculation.
        """
        self.assertEqual(self.geometry.ordinal_from_hexagon((3, -1, -2)), 36)
        self.assertEqual(self.geometry.ordinal_from_hexagon((3, -1, -2)), 36)


class Test_StandardBoard_hexagon_from_ordinal(unittest.TestCase):
    def setUp(self):
        """Create an instance of the standard board type.
        """
        self.geometry = board_geometry.StandardBoard()

    def test_works(self):
        """A few assertions to test that this works.

        Since the underlying componenets of this are thoroughly
        tested, this amounts to an integration test.
        """
        self.assertEqual(self.geometry.hexagon_from_ordinal(22), (0, 3, -3))
        self.assertEqual(self.geometry.hexagon_from_ordinal(11), (-2, 2, 0))
        self.assertEqual(self.geometry.hexagon_from_ordinal(32), (1, -3, 2))
        self.assertEqual(self.geometry.hexagon_from_ordinal(36), (3, -1, -2))

    def test_repeated_calculations(self):
        """Check that cache returns the same values.

        Since values, are cached, we want to make sure the lookup
        returns the same value as the calculation.
        """
        self.assertEqual(self.geometry.hexagon_from_ordinal(36), (3, -1, -2))
        self.assertEqual(self.geometry.hexagon_from_ordinal(36), (3, -1, -2))


class Test_StandardBoard_hexagon_neighbors(unittest.TestCase):
    def setUp(self):
        """Create an instance of the standard board type.
        """
        self.geometry = board_geometry.StandardBoard()

    def test_center_neighbors(self):
        """All surrounding neighbors should be included.
        """
        neighbors = self.geometry.hexagon_neighbors((0, 0, 0))
        expected_neighbors = [(1, 0, -1), (0, 1, -1), (-1, 1, 0),
                              (-1, 0, 1), (0, -1, 1), (1, -1, 0)]
        self.assertEqual(neighbors, expected_neighbors)

    def test_edge_neighbors(self):
        """Only the three nearby neighbors should be included.
        """
        neighbors = self.geometry.hexagon_neighbors((3, 0, -3))
        expected_neighbors = [(2, 1, -3), (2, 0, -2), (3, -1, -2)]
        self.assertEqual(neighbors, expected_neighbors)


class Test_StandardBoard_edge_synonyms(unittest.TestCase):
    def setUp(self):
        """Create an instance fo the standard board type.
        """
        self.geometry = board_geometry.StandardBoard()

    def test_center_zero(self):
        """Test edge_synonyms working as expected.
        """
        hexagon = (0, 0, 0)
        edge = 0
        synonyms = self.geometry.edge_synonyms(hexagon, edge)
        expected_synonyms = [((1, 0, -1), 3)]
        self.assertEqual(synonyms, expected_synonyms)

    def test_no_other_synonyms(self):
        """Test the case where there are no vertex_synonyms.
        """
        hexagon = (1, 2, -3)
        edge = 1
        synonyms = self.geometry.edge_synonyms(hexagon, edge)
        expected_synonyms = []
        self.assertEqual(synonyms, expected_synonyms)

    def test_wraps(self):
        """Test the case where the neighbors wraps around.
        """
        hexagon = (1, 0, -1)
        edge = 4
        synonyms = self.geometry.edge_synonyms(hexagon, edge)
        expected_synonyms = [((1, -1, 0), 1)]
        self.assertEqual(synonyms, expected_synonyms)


class Test_StandardBoard_vertex_synonyms(unittest.TestCase):
    def setUp(self):
        """Create an instance fo the standard board type.
        """
        self.geometry = board_geometry.StandardBoard()

    def test_center_zero(self):
        """Test vertex_synonyms working as expected.
        """
        hexagon = (0, 0, 0)
        vertex = 0
        synonyms = self.geometry.vertex_synonyms(hexagon, vertex)
        expected_synonyms = [((1, -1, 0), 2), ((1, 0, -1), 4)]
        self.assertEqual(synonyms, expected_synonyms)

    def test_outer_five(self):
        """Test vertex_synonyms moduluous wraps around as expected.
        """
        hexagon = (1, 1, -2)
        vertex = 5
        synonyms = self.geometry.vertex_synonyms(hexagon, vertex)
        expected_synonyms = [((1, 0, -1), 1), ((2, 0, -2), 3)]
        self.assertEqual(synonyms, expected_synonyms)

    def test_no_other_synonyms(self):
        """Test the case where there are no vertex_synonyms.
        """
        hexagon = (1, 2, -3)
        vertex = 1
        synonyms = self.geometry.vertex_synonyms(hexagon, vertex)
        expected_synonyms = []
        self.assertEqual(synonyms, expected_synonyms)
