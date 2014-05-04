import unittest

from settling.board_geometry import StandardBoard
from settling.exceptions import GameRuleViolation
from settling import board
from settling import game_constants


class Test_random_standard_board(unittest.TestCase):
    def test_returns_board(self):
        """We just check that a board object is returned
        """
        random_standard_board = board.random_standard_board()
        self.assertIsInstance(random_standard_board, board.Board)


class Test_Board__set_up(unittest.TestCase):
    def setUp(self):
        self.tiles = game_constants.STANDARD_TILE_ORDER
        self.numbers = game_constants.STANDARD_NUMBER_ORDER
        self.ports = game_constants.STANDARD_PORT_MAP
        self.board_geom = StandardBoard()

    def test_creates_tiles(self):
        b = board.Board(self.tiles, self.numbers, self.ports, self.board_geom)
        self.assertTrue(b._tiles)

    def test_creates_ports(self):
        b = board.Board(self.tiles, self.numbers, self.ports, self.board_geom)
        self.assertTrue(b._ports)

    def test_adds_one_robber(self):
        b = board.Board(self.tiles, self.numbers, self.ports, self.board_geom)
        robber_count = sum([1 for t in b._tiles if t.has_robber])
        self.assertEqual(robber_count, 1)


class Test_Board_tile(unittest.TestCase):
    def setUp(self):
        tiles = game_constants.STANDARD_TILE_ORDER
        numbers = game_constants.STANDARD_NUMBER_ORDER
        ports = game_constants.STANDARD_PORT_MAP
        board_geom = StandardBoard()
        self.board = board.Board(tiles, numbers, ports, board_geom)

    def test_tile_water_boundary(self):
        """Test where there is no water, then water.
        """
        not_water = self.board.tile((2, 0, -2))
        water = self.board.tile((3, 0, -3))
        self.assertNotEqual(not_water.tile_type, 'water')
        self.assertEqual(water.tile_type, 'water')


class Test_Board_port(unittest.TestCase):
    def setUp(self):
        tiles = game_constants.STANDARD_TILE_ORDER
        numbers = game_constants.STANDARD_NUMBER_ORDER
        ports = game_constants.STANDARD_PORT_MAP
        board_geom = StandardBoard()
        self.board = board.Board(tiles, numbers, ports, board_geom)

    def test_no_port(self):
        port_output = self.board.port((0, 0, 0), 0)
        expected_output = None
        self.assertEqual(port_output, expected_output)

    def test_port_on_vetex(self):
        port_output = self.board.port((1, 1, -2), 2)
        expected_output = 'brick port'
        self.assertEqual(port_output, expected_output)

    def test_port_on_unnamed_vertex(self):
        """Return port for a synonym rather than name in port map.
        """
        port_output = self.board.port((0, 2, -2), 0)
        expected_output = 'brick port'
        self.assertEqual(port_output, expected_output)


class Test_Board_move_robber(unittest.TestCase):
    def setUp(self):
        tiles = game_constants.STANDARD_TILE_ORDER
        numbers = game_constants.STANDARD_NUMBER_ORDER
        ports = game_constants.STANDARD_PORT_MAP
        board_geom = StandardBoard()
        self.board = board.Board(tiles, numbers, ports, board_geom)

    def test_robber_in_new_location(self):
        new_location = (0, 0, 0)
        self.board.move_robber(to_coord=new_location)
        self.assertTrue(self.board.tile(new_location).has_robber)

    def test_only_one_robber_after_move(self):
        self.board.move_robber(to_coord=(0, 0, 0))
        robber_count = sum([1 for t in self.board._tiles if t.has_robber])
        self.assertEqual(robber_count, 1)


class Test_Board_add_road(unittest.TestCase):
    def setUp(self):
        tiles = game_constants.STANDARD_TILE_ORDER
        numbers = game_constants.STANDARD_NUMBER_ORDER
        ports = game_constants.STANDARD_PORT_MAP
        board_geom = StandardBoard()
        self.board = board.Board(tiles, numbers, ports, board_geom)

    def test_road_added(self):
        """Adding a town should increase `_edges` by one.
        """
        self.board.add_road((0, 0, 0), 0, 'player1')
        self.assertEqual(len(self.board._edges), 1)

    def test_existing_road_raises(self):
        """Existing road -> GameRuleViolation.
        """
        self.board.add_road((0, 0, 0), 0, 'player1')
        with self.assertRaises(GameRuleViolation):
            self.board.add_road((0, 0, 0), 0, 'player1')

    def test_between_water_raises(self):
        """Trying to place a road between two water tiles -> GameRuleViolation
        """
        with self.assertRaises(GameRuleViolation):
            self.board.add_road((3, 0, -3), 2, 'player1')


class Test_Board_add_town(unittest.TestCase):
    def setUp(self):
        tiles = game_constants.STANDARD_TILE_ORDER
        numbers = game_constants.STANDARD_NUMBER_ORDER
        ports = game_constants.STANDARD_PORT_MAP
        board_geom = StandardBoard()
        self.board = board.Board(tiles, numbers, ports, board_geom)

    def test_town_added(self):
        """Adding a town should increase `_vertices` by one.
        """
        self.board.add_town((0, 0, 0), 0, 'player1')
        self.assertEqual(len(self.board._vertices), 1)

    def test_existing_town_raises(self):
        self.board.add_town((0, 0, 0), 0, 'player1')
        with self.assertRaises(GameRuleViolation):
            self.board.add_town((0, 0, 0), 0, 'player1')

    def test_only_on_water_raises(self):
        with self.assertRaises(GameRuleViolation):
            self.board.add_town((3, 0, -3), 0, 'player1')


class Test_Board_has_road(unittest.TestCase):
    def setUp(self):
        tiles = game_constants.STANDARD_TILE_ORDER
        numbers = game_constants.STANDARD_NUMBER_ORDER
        ports = game_constants.STANDARD_PORT_MAP
        board_geom = StandardBoard()
        self.board = board.Board(tiles, numbers, ports, board_geom)

    def test_same_hexagon_edge(self):
        """Add the road, then it should be there.
        """
        self.board.add_road((1, 0, -1), 3, 'player1')
        has_road = self.board.has_road((1, 0, -1), 3, 'player1')
        self.assertTrue(has_road)

    def test_alternate_hexagon_edge(self):
        """Add the road, then checking a synonym should return true.
        """
        self.board.add_road((1, 0, -1), 3, 'player1')
        has_road = self.board.has_road((0, 0, 0), 0, 'player1')
        self.assertTrue(has_road)

    def test_no_player(self):
        """Test the case where we only care if there is a road there or not.
        """
        self.board.add_road((1, 0, -1), 3, 'player1')
        has_road = self.board.has_road((0, 0, 0), 0)
        self.assertTrue(has_road)

    def test_no_road_no_player(self):
        """Return False when there is no road and no player given.
        """
        has_road = self.board.has_road((0, 0, 0), 0)
        self.assertFalse(has_road)

    def test_no_road_with_player(self):
        """Return False when there is no road but there is a player given.
        """
        has_road = self.board.has_road((0, 0, 0), 0, 'player1')
        self.assertFalse(has_road)


class Test_Board_upgrade_town(unittest.TestCase):
    def setUp(self):
        tiles = game_constants.STANDARD_TILE_ORDER
        numbers = game_constants.STANDARD_NUMBER_ORDER
        ports = game_constants.STANDARD_PORT_MAP
        board_geom = StandardBoard()
        self.board = board.Board(tiles, numbers, ports, board_geom)

    def test_upgrade_works(self):
        """If conditions are right, upgrade.
        """
        self.board.add_town((1, 1, -2), 4, 'player1')
        self.board.upgrade_town((1, 1, -2), 4, 'player1')
        self.assertTrue(True)

    def test_raise_when_no_town(self):
        """Raise an error if there is no town.
        """
        with self.assertRaises(GameRuleViolation):
            self.board.upgrade_town((1, 1, -2), 4, 'player1')

    def test_raise_when_wrong_player(self):
        """Raise an error if there is another player's town.
        """
        self.board.add_town((1, 1, -2), 4, 'player1')
        with self.assertRaises(GameRuleViolation):
            self.board.upgrade_town((1, 1, -2), 4, 'player2')


class Test_Board_has_town(unittest.TestCase):
    def setUp(self):
        self.tiles = game_constants.STANDARD_TILE_ORDER
        self.numbers = game_constants.STANDARD_NUMBER_ORDER
        self.ports = game_constants.STANDARD_PORT_MAP
        self.board_geom = StandardBoard()
        self.board = board.Board(
            self.tiles, self.numbers, self.ports, self.board_geom
        )

    def test_same_vertex(self):
        """Adding a town should show up at the same location.
        """
        self.board.add_town((1, 1, -2), 4, 'player1')
        has_town = self.board.has_town((1, 1, -2), 4, 'player1')
        self.assertTrue(has_town)

    def test_other_vertex(self):
        """Adding a town should show up in synonymous locations.
        """
        self.board.add_town((1, 1, -2), 4, 'player1')
        has_town = self.board.has_town((0, 1, -1), 0, 'player1')
        self.assertTrue(has_town)

    def test_no_player(self):
        """Should return True no matter what the player is.
        """
        self.board.add_town((1, 1, -2), 4, 'player1')
        has_town = self.board.has_town((0, 1, -1), 0)
        self.assertTrue(has_town)

    def test_no_town_no_player(self):
        """Return False, no town, no player.
        """
        has_town = self.board.has_town((0, 1, -1), 0)
        self.assertFalse(has_town)

    def test_town_no_player(self):
        """Return False, no town, with player.
        """
        has_town = self.board.has_town((0, 1, -1), 0, 'player1')
        self.assertFalse(has_town)


class Test_Board_has_city(unittest.TestCase):
    def setUp(self):
        self.tiles = game_constants.STANDARD_TILE_ORDER
        self.numbers = game_constants.STANDARD_NUMBER_ORDER
        self.ports = game_constants.STANDARD_PORT_MAP
        self.board_geom = StandardBoard()
        self.board = board.Board(
            self.tiles, self.numbers, self.ports, self.board_geom
        )

    def test_same_vertex(self):
        """Adding a city should show up at the same location.
        """
        self.board.add_town((1, 1, -2), 4, 'player1')
        self.board.upgrade_town((1, 1, -2), 4, 'player1')
        has_city = self.board.has_city((1, 1, -2), 4, 'player1')
        self.assertTrue(has_city)

    def test_other_vertex(self):
        """Adding a city should show up in synonymous locations.
        """
        self.board.add_town((1, 1, -2), 4, 'player1')
        self.board.upgrade_town((1, 1, -2), 4, 'player1')
        has_city = self.board.has_city((0, 1, -1), 0, 'player1')
        self.assertTrue(has_city)

    def test_no_player(self):
        """Should return True no matter what the player is.
        """
        self.board.add_town((1, 1, -2), 4, 'player1')
        self.board.upgrade_town((1, 1, -2), 4, 'player1')
        has_city = self.board.has_city((0, 1, -1), 0)
        self.assertTrue(has_city)

    def test_no_city_no_player(self):
        """Return False, no city, no player.
        """
        has_city = self.board.has_city((0, 1, -1), 0)
        self.assertFalse(has_city)

    def test_city_no_player(self):
        """Return False, no city, with player.
        """
        has_city = self.board.has_city((0, 1, -1), 0, 'player1')
        self.assertFalse(has_city)
