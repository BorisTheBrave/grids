# UpDown Triangle Co-ordinates
# This module provides sample code for working with equilateral triangles in an up-down configuration, i.e.
#        ____________
#       /\    /\    /
#      /  \  /  \  /
#     /____\/____\/
#    /\    /\    /
#   /  \  /  \  /
#  /____\/____\/

# Each triangle is defined by three co-ordinates, a, b, c.
# b determines which row the triangle is in, and a and c the two diagonals.
# a + b + c always sums to either 1 or 2.
# There are many other possible co-ordinate schemes, but this one seems to have the simplest maths.

# Thus, the origin is a vertex, and it has 6 triangles around it:
# (1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 1, 1), (0, 0, 1), (1, 0, 1)

# To find the neighbours of a down triangle, add 1 to a co-ordinate, and subtract one for neighbours of an up triangle.

from math import floor, ceil, sqrt
from settings import edge_length

sqrt3 = sqrt(3)

# Basics #######################################################################

def tri_center(a, b, c):
    """Returns the center of a given triangle in cartesian co-ordinates"""
    # Each unit of a, b, c moves you in the direction of one of the edges of a
    # down triangle, in linear combination.
    # Or equivalently, this function multiplies by the inverse matrix to pick_tri
    #
    # NB: This function has the nice property that if you pass in x,y,z values that
    # sum to zero (not a valid triangle), it'll return co-ordinates for the vertices of the
    # triangles.
    return ((       0.5 * a +                      -0.5 * c) * edge_length,
            (-sqrt3 / 6 * a + sqrt3 / 3 * b - sqrt3 / 6 * c) * edge_length)

def points_up(a, b, c):
    """Returns True if this is an upwards pointing triangle, otherwise False"""
    return a + b + c == 2

def tri_corners(a, b, c):
    """Returns the three corners of a given triangle in cartesian co-ordinates"""
    if points_up(a, b, c):
        return [
            tri_center(1 + a, b, c),
            tri_center(a, b, 1 + c),
            tri_center(a, 1 + b, c),
        ]
    else:
        return [
            tri_center(-1 + a, b, c),
            tri_center(a, b, -1 + c),
            tri_center(a, -1 + b, c),
        ]

def pick_tri(x, y):
    """Returns the triangle that contains a given cartesian co-ordinate point"""
    # Using dot product, measures which row and diagonals a given point occupies.
    # Or equivalently, multiply by the inverse matrix to tri_center
    # Note we have to break symmetry, using floor(...)+1 instead of ceil, in order
    # to deal with corner vertices like (0, 0) correctly.
    return (
        ceil(( 1 * x - sqrt3 / 3 * y) / edge_length),
        floor((    sqrt3 * 2 / 3 * y) / edge_length) + 1,
        ceil((-1 * x - sqrt3 / 3 * y) / edge_length),
    )

def tri_neighbours(a, b, c):
    """Returns the tris that share an edge with the given tri"""
    if points_up(a, b, c):
        return [
            (a - 1, b    , c    ),
            (a    , b - 1, c    ),
            (a    , b    , c - 1),
        ]
    else:
        return [
            (a + 1, b    , c    ),
            (a    , b + 1, c    ),
            (a    , b    , c + 1),
        ]

def tri_dist(a1, b1, c1, a2, b2, c2):
    """Returns how many steps one tri is from another"""
    return abs(a1 - a2) + abs(b1 - b2) + abs(c1 - c2)

def tri_disc(a, b, c, r):
    """Returns the tris that are at most distance r from the given tri"""
    # This could probably be optimized more
    for da in range(-r, r + 1):
        for db in range(-r, r + 1):
            dc = 1 - (a + b + c + da + db)
            if abs(da) + abs(db) + abs(dc) <= r:
                yield (a + da, b + db, c + dc)
            dc += 1
            if abs(da) + abs(db) + abs(dc) <= r:
                yield (a + da, b + db, c + dc)

# Symmetry #####################################################################

def tri_rotate_60(a, b, c, n = 1):
    """Rotates the given triangle n * 60 degrees counter clockwise around the origin,
    and returns the co-ordinates of the new triangle."""
    n = n % 6 if n >= 0 else n % 6 + 6
    if n == 0:
        return (a, b, c)
    if n == 1:
        return (1 - b, 1 - c, 1 - a)
    if n == 2:
        return (c, a, b)
    if n == 3:
        return (1 - a, 1 - b, 1 - c)
    if n == 4:
        return (b, c, a)
    if n == 5:
        return (1 - c, 1 - a, 1 - b)

def tri_rotate_about_60(a, b, c, about_a, about_b, about_c, n = 1):
    """Rotates the given triangle n* 60 degress counter clockwise about the given tri
    and return the co-ordinates of the new triangle."""
    (a, b, c) = tri_rotate_60(a - about_a, b - about_b, c - about_c)
    return (a + about_a, b + about_b, c + about_c)

def tri_reflect_y(a, b, c):
    """Reflects the given triangle through the x-axis
    and returns the co-ordinates of the new triangle"""
    return (1 - c, 1 - b, 1 - a)

def tri_reflect_x(a, b, c):
    """Reflects the given triangle through the y-axis
    and returns the co-ordinates of the new triangle"""
    return (c, b, a)

def tri_reflect_by(a, b, c, n = 0):
    """Reflects the given triangle through the x-axis rotated counter clockwise by n * 30 degrees
    and returns the co-ordinates of the new triangle"""
    (a2, b2, c2) = tri_reflect_y(a, b, c)
    return tri_rotate_60(a2, b2, c2, n)

# Shapes #######################################################################

def tri_line_intersect(x1, y1, x2, y2):
    """Returns the triangles that intersect the line specified in cartesian co-ordinates"""
    x1 /= edge_length
    y1 /= edge_length
    x2 /= edge_length
    y2 /= edge_length
    dx = x2 - x1
    dy = y2 - y1
    # Convert from cartesian co-ordinates to the three triangle axes
    fa =  1 * x1 - sqrt3 / 3 * y1
    fb =       sqrt3 * 2 / 3 * y1
    fc = -1 * x1 - sqrt3 / 3 * y1
    da =  1 * dx - sqrt3 / 3 * dy
    db =       sqrt3 * 2 / 3 * dy
    dc = -1 * dx - sqrt3 / 3 * dy
    # Now do raycasting on a 3d cube grid, except we ensure
    # we step across cells in an order that alternates
    # up/down triangles
    a =  ceil(fa)
    b =  floor(fb) + 1
    c =  ceil(fc)
    isup = a + b + c == 2
    stepa = 1 if da > 0 else -1
    stepb = 1 if db > 0 else -1
    stepc = 1 if dc > 0 else -1
    ta = (a - int(da <= 0) - fa) / da
    tb = (b - int(db <= 0) - fb) / db
    tc = (c - int(dc <= 0) - fc) / dc
    ida = abs(1 / da)
    idb = abs(1 / db)
    idc = abs(1 / dc)
    yield (a, b, c)
    while True:
        if ta <= tb and ta <= tc and (stepa == 1) != isup:
            if ta > 1: return
            a += stepa
            ta += ida
        elif tb <= ta and tb <= tc and (stepb == 1) != isup:
            if tb > 1: return
            b += stepb
            tb += idb
        else:
            if tc > 1: return
            c += stepc
            tc += idc
        yield (a, b, c)
        isup = not isup

def tri_line(a1, b1, c1, a2, b2, c2):
    """Returns the tris in a shortest path from one tri to another, staying as close to the straight line as possible"""
    (x1, y1) = tri_center(a1, b1, c1)
    (x2, y2) = tri_center(a2, b2, c2)
    return tri_line_intersect(x1, y1, x2, y2)

def tri_rect_intersect(x, y, width, height):
    """Returns the tris that intersect the rectangle specified in cartesian co-ordinates"""
    assert width >= 0, "Rectangle should have non-negative width"
    assert height >= 0, "Rectangle should have non-negative height"
    # For consistency, we treat the triangles as exclusive of their border, and the rect as inclusive
    x /= edge_length
    y /= edge_length
    width /= edge_length
    height /= edge_length
    # Lower and upper bound by row
    fl = sqrt3 * 2 / 3 * y
    fu = sqrt3 * 2 / 3 * (y + height)
    # Loop over all rows that the rectangle is in
    for b in range(floor(fl) + 1, ceil(fu) + 1):
        # Consider each row vs a trimmed rect
        minb = max(b - 1, fl)
        maxb = min(b, fu)
        # The smallest / largest values for the diagonals
        # can be read from the trimmed rect corners
        mina = floor(x - maxb / 2) + 1
        maxa = ceil(x + width - minb / 2)
        minc = floor(-x - width - maxb / 2) + 1
        maxc = ceil(-x - minb / 2)
        # Walk along the row left to right
        a = mina
        c = maxc
        assert a + b + c == 1 or a + b + c == 2
        while a <= maxa and c >= minc:
            yield (a, b, c)
            if a + b + c == 1:
                a += 1
            else:
                c -= 1