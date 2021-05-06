# Flat-topped cube-cordinate hexes
# See https://www.redblobgames.com/grids/hexagons/ for an extended explnation of how this works.
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


from __future__ import division
from math import floor, ceil, sqrt
from updown_tri import pick_tri, tri_line

# Aka outer_radius, this is the side length of the hex
edge_length = 1

sqrt3 = sqrt(3)

def hex_center(x, y, z):
    """Returns the center of a given hex in cartesian co-ordinates"""
    # Each unit of x, y, z moves you in the direction of one of the corners of
    # the hex, in linear combination.
    #
    # NB: This function has the nice property that if you pass in x,y,z values that
    # sum to 1 or -1 (not a valid hex), it'll return co-ordinates for the vertices of the
    # hexes.
    return ((1 * x      - 0.5 * y       - 0.5 * z) * edge_length,
            (       sqrt3 / 2 * y - sqrt3 / 2 * z) * edge_length)

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

def tri_to_hex(x, y, z):
    """Given a triangle co-ordinate as specified in updown_tri, finds the hex that contains it"""
    # Rotate the co-ordinate system by 30 degrees, and discretize.
    # I'm not totally sure why this works.
    return (
        round((x - z) / 3),
        round((y - x) / 3),
        round((z - y) / 3),
    )

def hex_to_tris(x, y, z):
    """Given a hex, returns the co-ordinates of the 6 triangles it contains, using co-ordinates as described in updown_tri"""
    a = x - y
    b = y - z
    c = z - x
    return [
        (a + 1, b    , c    ),
        (a + 1, b + 1, c    ),
        (a    , b + 1, c    ),
        (a    , b + 1, c + 1),
        (a    , b    , c + 1),
        (a + 1, b    , c + 1),
    ]

def pick_hex(x, y):
    """Returns the hex that contains a given cartesian co-ordinate point"""
    (a, b, c) = pick_tri(x, y)
    return tri_to_hex(a, b, c)
    

def hex_neighbours(x, y, z):
    """Returns the hexes that share an edge with the given hex"""
    return [
        (x + 1, y    , z - 1),
        (x    , y + 1, z - 1),
        (x - 1, y + 1, z    ),
        (x - 1, y    , z + 1),
        (x    , y - 1, z + 1),
        (x + 1, y - 1, z    ),
    ]

def hex_dist(x1, y1, z1, x2, y2, z2):
    """Returns how many steps one hex is from another"""
    return (abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)) // 2

def hex_disc(x, y, z, r):
    """Returns the hexes that are at most distance r from the given hex"""
    for dx in range(-r, r + 1):
        for dy in range(max(-r, -dx - r), min(r, -dx + r) + 1):
            dz = -dx - dy
            yield (x + dx, y + dy, z + dz)

def hex_line_intersect(x1, y1, x2, y2):
    """Returns hexes that intersect the line specified"""
    prev = None
    for (a, b, c) in tri_line(x1, y1, x2, y2):
        hex = tri_to_hex(a, b, c)
        if hex != prev:
            yield hex
            prev = hex

def hex_line(x1, y1, z1, x2, y2, z2):
    """Returns the hexes in a shortest path from one hex to another, staying as close to the straight line as possible"""
    # Note that drawing a straight line from one hex to another can touch hexes not returned by this method.
    n = hex_dist(x1, y1, z1, x2, y2, z2)
    c1 = hex_center(x1, y1, z1)
    c2 = hex_center(x2, y2, z2)
    for i in range(0, n + 1):
        t = i / n
        px = c1[0] + (c2[0] - c1[0]) * t
        py = c1[1] + (c2[1] - c1[1]) * t
        yield pick_hex(px, py)

def hex_rect(rect_x, rect_y, rect_z, width, height, inc_bottom=False, inc_top=False):
    """Returns the hexes in a rectangle that includes the given hex in the bottom left, 
    that extends `height` hexes upwards, and `width` hexes to the right.
    inc_bottom and inc_top increase the size of the rect in every other column"""
    odd_height = int(inc_bottom) + int(inc_top) - 1
    (x, y, z) = (rect_x, rect_y, rect_z)
    for dx in range(width):
        # yield a vertical column
        for dy in range(height + (dx % 2) * odd_height):
            yield (x, y + dy, z - dy)
        # Move one column along, staying at the bottom of the rect
        x += 1
        if dx % 2 == int(inc_bottom):
            z -= 1
        else:
            y -= 1

def hex_rect_index(x, y, z, rect_x, rect_y, rect_z, width, height, inc_bottom=False, inc_top=False):
    """Given a hex and a rectangle, gives a linear position of the hex.
    The index is an integer between zero and hex_rect_size - 1.
    This is useful for array storage of rectangles.
    Returns None if the hex is not in the rectangle.
    Equivalent to list(hex_rect(...)).index((x, y, z))"""
    dx = x - rect_x
    if dx < 0 or dx >= width:
        return None
    odd_height = int(inc_bottom) + int(inc_top) - 1
    # Number of hexes in rect with x value smaller than searched hex.
    left_count = height * dx + odd_height * (dx // 2)
    # y value of hex at bottom of the column that the searched hex is in
    base_dy = rect_y - (dx // 2) - (dx % 2) * int(inc_bottom)
    dy = y - base_dy
    if dy < 0 or dy >= height + (dx % 2) * odd_height:
        return None
    return left_count + dy

def hex_rect_deindex(index, rect_x, rect_y, rect_z, width, height, inc_bottom=False, inc_top=False):
    """Performs the inverse of hex_rect_index
    Equivalent to list(hex_rect(...))[index]"""
    odd_height = int(inc_bottom) + int(inc_top) - 1
    two_col = height + height + odd_height
    dx = 2 * (index // two_col)
    index -= dx // 2 * two_col
    if index >= height:
        dx += 1
        index -= height
    if dx < 0 or dx >= width:
        raise Exception("Hex is not inside rectangle")
    dy = index
    # y + oy is the value of hex at bottom of the column that the searched hex is in
    oy = - (dx // 2) - (dx % 2) * int(inc_bottom)
    return (rect_x + dx, rect_y + oy + dy, rect_z - dx - oy - dy)

def hex_rect_size(rect_x, rect_y, rect_z, width, height, inc_bottom=False, inc_top=False):
    """Returns the number of hexes in a given rectangle.
    Equivalent to len(list(hex_rect(...)))"""
    odd_height = int(inc_bottom) + int(inc_top) - 1
    return height * width + odd_height * (width // 2)
