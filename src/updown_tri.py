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

# To find the neighbours of a down triangle, add 1 to a co-ordinate, and subtract one for neighbours of an up triangle.

from math import floor, ceil, sqrt
from settings import edge_length

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
    return ((       0.5 * x +                      -0.5 * z) * edge_length,
            (-sqrt3 / 6 * x + sqrt3 / 3 * y - sqrt3 / 6 * z) * edge_length)

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
    return (
        ceil(( 1 * x - sqrt3 / 3 * y) / edge_length),
        floor((    sqrt3 * 2 / 3 * y) / edge_length) + 1,
        ceil((-1 * x - sqrt3 / 3 * y) / edge_length),
    )

def tri_neighbours(x, y, z):
    """Returns the tris that share an edge with the given tri"""
    if points_up(x, y, z):
        return [
            (x - 1, y    , z    ),
            (x    , y - 1, z    ),
            (x    , y    , z - 1),
        ]
    else:
        return [
            (x + 1, y    , z    ),
            (x    , y + 1, z    ),
            (x    , y    , z + 1),
        ]

def tri_dist(x1, y1, z1, x2, y2, z2):
    """Returns how many steps one tri is from another"""
    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)

def tri_disc(x, y, z, r):
    """Returns the tris that are at most distance r from the given tri"""
    # This could probably be optimized more
    for dx in range(-r, r + 1):
        for dy in range(-r, r + 1):
            dz = 1 - (x + y + z + dx + dy)
            if abs(dx) + abs(dy) + abs(dz) <= r:
                yield (x + dx, y + dy, z + dz)
            dz += 1
            if abs(dx) + abs(dy) + abs(dz) <= r:
                yield (x + dx, y + dy, z + dz)

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

def tri_rect_intersect(x, y, width, height):
    """Returns the tris that intersect the rectangle specified in cartesian co-ordinates"""
    x /= edge_length
    y /= edge_length
    width /= edge_length
    height /= edge_length
    # Lower and upper bound by row
    fl = sqrt3 * 2 / 3 * y
    fu = sqrt3 * 2 / 3 * (y + height)
    # Loop over all rows that the rectangle is in
    for b in range(ceil(fl), ceil(fu) + 1):
        # Consider each row vs a trimmed rect
        minb = max(b - 1, fl)
        maxb = min(b, fu)
        # The smallest / largest values for the diagonals
        # can be read from the trimmed rect corners
        mina = ceil(x - maxb / 2)
        maxa = ceil(x + width - minb / 2)
        minc = ceil(-x - width - maxb / 2)
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