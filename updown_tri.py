# UpDown Triangle Co-ordinates
# This module provides sample code for working with equilateral triangles in an up-down configuration, i.e.
#        ____________
#       /\    /\    /
#      /  \  /  \  /
#     /____\/____\/
#    /\    /\    /
#   /  \  /  \  /
#  /____\/____\/

# Each triangle is defined by three co-ordinates, x, y, z.
# y determines which row the triangle is in, and x and z the two diagonals.
# x + y + z always sums to either 1 or 2.
# There are many other possible co-ordinate schemes, but this one seems to have the simplest maths.

# Thus, the origin is a vertex, and it has 6 triangles around it:
# (1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 1, 1), (0, 0, 1), (1, 0, 1)

# To find the neighbous of a down triangle, add 1 to a co-ordinate, and subtract one for up neighbours.



# This is the side length of the triangle
edge_length = 1

sqrt3 = sqrt(3)

def tri_center(x, y, z):
    """Returns the center of a given triangle in cartesian co-ordinates"""
    # Each unit of x, y, z moves you in the direction of one of the edges of a
    # down triangle, in linear combination.
    # Or equivalently, this function multiplies by the inverse matrix to pick_tri
    #
    # NB: This function has the nice property that if you pass in x,y,z values that
    # sum to zero (not a valid triangle), it'll return co-ordinates for the vertices of the
    # triangles.
    return [(       0.5 * x +                      -0.5 * z) * edge_length,
            (-sqrt3 / 6 * x + sqrt3 / 3 * y - sqrt3 / 6 * z) * edge_length]

def points_up(x, y, z):
    """Returns True if this is an upwards pointing triangle, otherwise False"""
    return x + y + z == 2

def tri_corners(x, y, z):
    """Returns the three corners of a given triangle in cartesian co-ordinates"""
    if points_up(x, y, z):
        return [
            tri_center(1 + x, y, z),
            tri_center(x, y, 1 + z),
            tri_center(x, 1 + y, z),
        ]
    else:
        return [
            tri_center(-1 + x, y, z),
            tri_center(x, y, -1 + z),
            tri_center(x, -1 + y, z),
        ]

def pick_tri(x, y):
    """Returns the triangle that contains a given cartesian co-ordinate point"""
    # Using dot product, measures which row and diagonals a given point occupies.
    # Or equivalently, multiply by the inverse matrix to tri_center
    # Note we have to break symmetry, using floor(...)+1 instead of ceil, in order
    # to deal with corner vertices like (0, 0) correctly.
    return [
        ceil(( 1 * x - sqrt3 / 3 * y) / edge_length),
        floor((    sqrt3 * 2 / 3 * y) / edge_length) + 1,
        ceil((-1 * x - sqrt3 / 3 * y) / edge_length),
    ]

def hex_neighbours(x, y, z):
    """Returns the tris that share an edge with the given tri"""
    if points_up(x, y, z):
        return [
            [x - 1, y    , z    ],
            [x    , y - 1, z    ],
            [x    , y    , z - 1],
        ]
    else:
        return [
            [x + 1, y    , z    ],
            [x    , y + 1, z    ],
            [x    , y    , z + 1],
        ]