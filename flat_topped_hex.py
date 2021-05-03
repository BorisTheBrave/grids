# Flat-topped cube-cordinate hexes
# See https://www.redblobgames.com/grids/hexagons/ for an explnation of how this works.
# This module provides sample code for working with regular hexagons flat-topped configuration, i.e.

#            ___
#           /   \
#       ___/     \__
#      /   \     /   \
#     /     \___/     \
#     \     /   \     /
#      \___/     \___/
#          \     /
#           \___/

# Each hex is defined by three co-ordinates, x, y, z.
# x + y + z always sums to 0, so z is redundant and can be omitted when storing co-ordinates.
# There are many other possible co-ordinate schemes, but this one seems to have the simplest maths.

# To find the neighbours of a given hex, add one to one co-ordinate, and subtract one from another.
# (there's 6 different ways of choosing the two co-ordinates).


from math import floor, ceil, sqrt

# Aka outer_radius, this is the side length of the hex
edge_length = 1

sqrt3 = sqrt(3)

# See updown_tri.py for a commented explanation of this function
# These triangles pack 6 into a hexagon, so are useful for pick_hex
def pick_tri(x, y):
    return [
        ceil(( 1 * x - sqrt3 / 3 * y) / edge_length),
        floor((    sqrt3 * 2 / 3 * y) / edge_length) + 1,
        ceil((-1 * x - sqrt3 / 3 * y) / edge_length),
    ]

def hex_center(x, y, z):
    """Returns the center of a given hex in cartesian co-ordinates"""
    # Each unit of x, y, z moves you in the direction of one of the corners of
    # the hex, in linear combination.
    #
    # NB: This function has the nice property that if you pass in x,y,z values that
    # sum to 1 or -1 (not a valid hex), it'll return co-ordinates for the vertices of the
    # hexes.
    return [(1 * x      - 0.5 * y       - 0.5 * z) * edge_length,
            (       sqrt3 / 2 * y - sqrt3 / 2 * z) * edge_length]

def hex_corners(x, y, z):
    """Returns the six corners of a given hex in cartesian co-ordinates"""
    return [
        hex_center(x    , y    , z - 1),
        hex_center(x    , y + 1, z    ),
        hex_center(x - 1, y    , z    ),
        hex_center(x    , y    , z + 1),
        hex_center(x    , y - 1, z    ),
        hex_center(x + 1, y    , z    ),
    ]

def pick_hex(x, y):
    """Returns the hex that contains a given cartesian co-ordinate point"""
    # Find the triangle that the point is in
    (a, b, c) = pick_tri(x, y)
    # Rotate the co-ordinate system by 30 degrees, and discretize.
    # I'm not totally sure why this works.
    return [
        round((a - c) / 3),
        round((b - a) / 3),
        round((c - b) / 3),
    ]

def hex_neighbours(x, y, z):
    """Returns the hexes that share an edge with the given hex"""
    return [
        [x + 1, y    , z - 1],
        [x    , y + 1, z - 1],
        [x - 1, y + 1, z    ],
        [x - 1, y    , z + 1],
        [x    , y - 1, z + 1],
        [x + 1, y - 1, z    ],
    ]