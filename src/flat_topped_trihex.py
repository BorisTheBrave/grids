# Trihex grid
#
# A trihexagonal grid, aka a Kagome lattice is a grid of alternating regular hexagons and triangles
# I don't know any games or uses for this tiling, but it's a simple variant of a triangle grid 
# so surprisingly easy to work with.
# 
# https://en.wikipedia.org/wiki/Trihexagonal_tiling
#
# __ ____ __ ____ __ ____
#\  /    \  /    \  /    \
# \/      \/      \/      \
#  \      /\      /\      /\
#   \____/__\____/__\____/__\
#    \  /    \  /    \  /    \
#     \/      \/      \/      \
#      \      /\      /\      /\
#       \____/__\____/__\____/__\
#        \  /    \  /    \  /    \
#         \/      \/      \/      \
#          \      /\      /\      /\
#           \____/__\____/__\____/__\

# Each cell, a trihex, is defined by three co-ordinates, a, b, c.
# b determines which row the trihex is in, and a and c the two diagonals.
# a + b + c always sums to either 0, -1, or 1, with the hexes being the zeros.

from __future__ import division
from math import floor, ceil, sqrt
from settings import edge_length
from common import mod
from updown_tri import pick_tri, tri_line_intersect, tri_rect_intersect

sqrt3 = sqrt(3)

# Basics #######################################################################

def trihex_cell_type(a, b, c):
    """Given a trihex returns what shape it specifically is."""
    n = a + b + c
    if n == 0:
        return "hex"
    if n == 1:
        return "tri_up"
    if n == -1:
        return "tri_down"

def trihex_center(a, b, c):
    """Returns the center of a given trihex in cartesian co-ordinates"""
    return ((             a +                                -c) * edge_length,
            (-sqrt3 / 3 * a + sqrt3 * 2 / 3 * b - sqrt3 / 3 * c) * edge_length)

def tri_to_trihex(a, b, c):
    """Given a triangle co-ordinate as specified in updown_tri, finds the trihex that contains it"""
    return (
        floor(a / 2),
        floor(b / 2),
        floor(c / 2),
    )

def trihex_to_tris(a, b, c):
    """Given a trihex, returns the co-ordinates of the 6 triangles it contains, using co-ordinates as described in updown_tri"""
    n = a + b + c
    if n == 0:
        return [
            (a * 2 + 1, b * 2, c * 2),
            (a * 2 + 1, b * 2 + 1, c * 2),
            (a * 2, b * 2 + 1, c * 2),
            (a * 2, b * 2 + 1, c * 2 + 1),
            (a * 2, b * 2, c * 2 + 1),
            (a * 2 + 1, b * 2, c * 2 + 1),
        ]
    if n == 1:
        return [(a * 2, b * 2, c * 2)]
    if n == -1:
        return [(a * 2, b * 2, c * 2)]

def trihex_corners(a, b, c):
    """Returns the three/six corners of a given trihex in cartesian co-ordinates"""
    n = a + b + c
    if n == 0:
        return [
            trihex_center(a + 0.5, b - 0.5, c      ),
            trihex_center(a,       b - 0.5, c + 0.5),
            trihex_center(a - 0.5, b,       c + 0.5),
            trihex_center(a - 0.5, b + 0.5, c      ),
            trihex_center(a,       b + 0.5, c - 0.5),
            trihex_center(a + 0.5, b,       c - 0.5),
        ]
    if n == 1:
        return [
            trihex_center(a + 0.5, b    , c    ),
            trihex_center(a    , b + 0.5, c    ),
            trihex_center(a    , b    , c + 0.5),
        ]
    if n == -1:
        return [
            trihex_center(a - 0.5, b    , c    ),
            trihex_center(a    , b - 0.5, c    ),
            trihex_center(a    , b    , c - 0.5),
        ]

def pick_trihex(x, y):
    """Returns the trihex that contains a given cartesian co-ordinate point"""
    (a, b, c) = pick_tri(x, y)
    return tri_to_trihex(a, b, c)

def trihex_neighbours(a, b, c):
    """Returns the three/six trihexes that share an edge with the given trihex"""
    n = a + b + c
    if n == 0:
        return [
            (a - 1, b    , c    ),
            (a    , b - 1, c    ),
            (a    , b    , c - 1),
            (a + 1, b    , c    ),
            (a    , b + 1, c    ),
            (a    , b    , c + 1),
        ]
    if n == 1:
        return [
            (a - 1, b    , c    ),
            (a    , b - 1, c    ),
            (a    , b    , c - 1),
        ]
    if n == -1:
        return [
            (a + 1, b    , c    ),
            (a    , b + 1, c    ),
            (a    , b    , c + 1),
        ]

def trihex_dist(a1, b1, c1, a2, b2, c2):
    """Returns how many steps one trihex is from another"""
    return abs(a1 - a2) + abs(b1 - b2) + abs(c1 - c2)

# Shapes #######################################################################

def trihex_disc(a, b, c, r):
    """Returns the trihexes that are at most distance r from the given trihex"""
    # This could probably be optimized more
    for da in range(-r, r + 1):
        for db in range(-r, r + 1):
            for t in (-1, 0, 1):
                dc = t - (a + b + c + da + db)
                if abs(da) + abs(db) + abs(dc) <= r:
                    yield (a + da, b + db, c + dc)

def trihex_line_intersect(x1, y1, x2, y2):
    """Returns trihexes that intersect the line specified in cartesian co-ordinates"""
    # We could implement this similar to tri_line_intersect
    # by raymarching through double sized lanes, but this is more code re-use
    prev = None
    for (a, b, c) in tri_line_intersect(x1, y1, x2, y2):
        trihex = tri_to_trihex(a, b, c)
        if trihex != prev:
            yield trihex
            prev = trihex