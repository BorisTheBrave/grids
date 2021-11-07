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
from settings import edge_length
from common import mod
from updown_tri import pick_tri, tri_line_intersect, tri_rect_intersect

sqrt3 = sqrt(3)

# Basics #######################################################################

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
    # Thanks to https://justinpombrio.net/programming/2020/04/28/pixel-to-hex.html
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

# Symmetry #####################################################################

def hex_rotate_60(x, y, z, n = 1):
    """Rotates the given hex n * 60 degrees counter clockwise around the origin,
    and returns the co-ordinates of the new hex."""
    n = mod(n, 6)
    if n == 0:
        return (x, y, z)
    if n == 1:
        return (-y, -z, -x)
    if n == 2:
        return (z, x, y)
    if n == 3:
        return (-x, -y, -z)
    if n == 4:
        return (y, z, x)
    if n == 5:
        return (-z, -x, -y)

def hex_rotate_about_60(x, y, z, about_x, about_y, about_z, n = 1):
    """Rotates the given hex n* 60 degress counter clockwise about the given hex
    and return the co-ordinates of the new hex."""
    (a, b, c) = hex_rotate_60(x - about_x, y - about_y, z - about_z, n)
    return (a + about_x, b + about_y, c + about_z)

def hex_reflect_y(x, y, z):
    """Reflects the given hex through the x-axis
    and returns the co-ordinates of the new hex"""
    return (x, z, y)

def hex_reflect_x(x, y, z):
    """Reflects the given hex through the y-axis
    and returns the co-ordinates of the new hex"""
    return (-x, -z, -y)

def hex_reflect_by(x, y, z, n = 0):
    """Reflects the given hex through the x-axis rotated counter clockwise by n * 30 degrees
    and returns the co-ordinates of the new hex"""
    (a, b, c) = hex_reflect_y(x, y, z)
    return hex_rotate_60(a, b, c, n)

# Shapes #######################################################################

def hex_disc(x, y, z, r):
    """Returns the hexes that are at most distance r from the given hex"""
    for dx in range(-r, r + 1):
        for dy in range(max(-r, -dx - r), min(r, -dx + r) + 1):
            dz = -dx - dy
            yield (x + dx, y + dy, z + dz)

def hex_line_intersect(x1, y1, x2, y2):
    """Returns hexes that intersect the line specified in cartesian co-ordinates"""
    prev = None
    for (a, b, c) in tri_line_intersect(x1, y1, x2, y2):
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

def hex_rect_intersect(x, y, width, height):
    """Returns the hexes that intersect the rectangle specified in cartesian co-ordinates"""
    prev = None
    first_b = None
    for (a, b, c) in tri_rect_intersect(x, y, width, height):
        if first_b is None: first_b = b
        hex = tri_to_hex(a, b, c)
        # Tri must be in the bottom half of the hex, except the first row
        # This stops double counting
        if first_b == b or hex[1] - hex[2] == b:
            if hex != prev:
                yield hex
                prev = hex

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

def hex_rect_knoll(x, y, z, rect_x, rect_y, rect_z, width, height, inc_bottom=False, inc_top=False):
    """Given a hex and a rectangle, gives a pair of integer cartesian co-ordinates that identify the square in the rectangle"""
    dx = x - rect_x
    if dx < 0 or dx >= width:
        return None
    odd_height = int(inc_bottom) + int(inc_top) - 1
    # y value of hex at bottom of the column that the searched hex is in
    base_dy = rect_y - (dx // 2) - (dx % 2) * int(inc_bottom)
    dy = y - base_dy
    return (dx, dy)

def hex_rect_unknoll(dx, dy, rect_x, rect_y, rect_z, width, height, inc_bottom=False, inc_top=False):
    """Given a co-ordinate pair and a rectangle, reverses hex_rect_knoll"""
    oy = - (dx // 2) - (dx % 2) * int(inc_bottom)
    return (rect_x + dx, rect_y + oy + dy, rect_z - dx - oy - dy)

def hex_rect_index(x, y, z, rect_x, rect_y, rect_z, width, height, inc_bottom=False, inc_top=False):
    """Given a hex and a rectangle, gives a linear position of the hex.
    The index is an integer between zero and hex_rect_size - 1.
    This is useful for array storage of rectangles.
    Returns None if the hex is not in the rectangle.
    Equivalent to list(hex_rect(...)).index((x, y, z))"""
    (dx, dy) = hex_rect_knoll(x, y, z, rect_x, rect_y, rect_z, width, height, inc_bottom, inc_top)
    if dx < 0 or dx >= width:
        return None
    odd_height = int(inc_bottom) + int(inc_top) - 1
    # Number of hexes in rect with x value smaller than searched hex.
    left_count = height * dx + odd_height * (dx // 2)
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
    return hex_rect_unknoll(dx, dy, rect_x, rect_y, rect_z, width, height, inc_bottom, inc_top)

def hex_rect_size(rect_x, rect_y, rect_z, width, height, inc_bottom=False, inc_top=False):
    """Returns the number of hexes in a given rectangle.
    Equivalent to len(list(hex_rect(...)))"""
    odd_height = int(inc_bottom) + int(inc_top) - 1
    return height * width + odd_height * (width // 2)

# Nesting ## ###################################################################
 
# Based on work in https://observablehq.com/@sanderevers/hexagon-tiling-of-an-hexagonal-grid
# Groups hexes into larger shapes that is each a disc around a given center hex
# These parent discs are themselves roughly hexagon shaped and roughly laid out like a pointy topped hexagon grid.

parent_radius = 2
parent_area = 3 * parent_radius * parent_radius + 3 * parent_radius + 1
parent_shift = 3 * parent_radius + 2

def hex_parent(x, y, z):
    """Returns the parent hex containing the given hex."""
    a = (z + y * parent_shift) // parent_area
    b = (x + z * parent_shift) // parent_area
    c = (y + x * parent_shift) // parent_area
    return (
        (1 + c - b) // 3,
        (1 + a - c) // 3,
        (1 + b - a) // 3,
    )

def hex_parent_center_child(x, y, z):
    """Returns the central hex of a given parent hex."""
    a = y - z
    b = z - x
    c = x - y
    return (
        (parent_shift * c + b) // 3,
        (parent_shift * a + c) // 3,
        (parent_shift * b + a) // 3,
    )

def hex_parent_children(x, y, z):
    """Returns all children hex of a given parent hex"""
    cx, cy, cz = hex_parent_center_child(x, y, z)
    return hex_disc(cx, cy, cz, parent_radius)