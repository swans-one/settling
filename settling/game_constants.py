"""References for game rule constants.

This module provides a number of objects and collections that make it
easier to encode game rules. 

Any object or colleciton defined in this module should be immutable so
that a consumer of this module cannot affect game behavior by
modifying the objects.
"""

RESOURCE_TILE_TYPES = ("brick", "wood", "wheat", "sheep", "ore")

NON_RESOURCE_TILE_TYPES = ("water", "desert")

TILE_TYPES = RESOURCE_TILE_TYPES + NON_RESOURCE_TILE_TYPES

PORT_TYPES = ("3:1 port", "brick port", "wood port", "sheep port", "ore_port")

NUMBERS = (2, 3, 4, 5, 6, 8, 9, 10, 11, 12)

STANDARD_LAND_TILE_ORDER = (
    "wheat", "wood", "sheep", "sheep", "wood", "ore", "brick", "wheat", "ore",
    "wood", "wheat", "ore", "brick", "desert", "brick", "wood", "sheep",
    "wheat", "sheep"
)

STANDARD_TILE_ORDER = STANDARD_LAND_TILE_ORDER + ("water",) * 18

STANDARD_NUMBER_ORDER = (
    9, 10, 8, 12, 5, 4, 3, 11, 6, 11, 9, 6, 4, 3, 10, 2, 8, 5
)

STANDARD_PORT_MAP = ()

DEFAULT_PORT_ORDER = ("3:1 port", "3:1 port", "brick port", "wood port",
                      "3:1 port", "wheat port", "ore port", "3:1 port",
                      "sheep port")

PORTS = ["wood port", "brick port", "wheat port", "sheep port", "ore port",
         "3:1 port", "3:1 port", "3:1 port", "3:1 port"]
