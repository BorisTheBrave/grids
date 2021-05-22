# Square grid
# This is a standard square grid.

#   ___ ___ ___
#  |   |   |   |
#  |___|___|___|
#  |   |   |   |
#  |___|___|___|
#  |   |   |   |
#  |___|___|___|

# Each square is defined by two integer co-ordinates x and y. x is right, and y is up.
# Following standard conventions, the square with co-ordinate (0, 0) spans
# the cartesian x-axis and y-axis from 0 to 1.

from __future__ import division
from math import floor, ceil, sqrt
from settings import edge_length
from common import mod

# Basics #######################################################################


def square_center(x, y):
    """Returns the center of a given square in cartesian co-ordinates"""
    return (x * edge_length, y * edge_length)

def square_corners(x, y):
    """Returns the four corners of a given square in cartesian co-ordinates"""
    return [
        square_center(x - 0.5, y - 0.5),
        square_center(x + 0.5, y - 0.5),
        square_center(x + 0.5, y + 0.5),
        square_center(x - 0.5, y + 0.5),
    ]

def pick_square(x, y):
    """Returns the square that contains a given cartesian co-ordinate point"""
    return (
        floor(x / edge_length),
        floor(y / edge_length),
    )

def square_neighbours(x, y):
    """Returns the squares that share an edge with the given square"""
    return (
        (x + 1, y),
        (x, y + 1),
        (x - 1, y),
        (x, y - 1),
    )

def square_dist(x1, y1, x2, y2):
    """Returns how many steps one square is from another"""
    return abs(x1 - x2) + abs(y1 - y2)

# Symmetry #####################################################################

def square_rotate_90(x, y, n = 1):
    """Rotates the given square n * 90 degrees counter clockwise around the (0, 0) square,
    and returns the co-ordinates of the new square."""
    n = mod(n, 4)
    if n == 0:
        return (x, y)
    if n == 1:
        return (-y, x)
    if n == 2:
        return (-x, -y)
    if n == 3:
        return (y, -x)

def square_rotate_about_90(x, y, about_x, about_y, n = 1):
    """Rotates the given square n * 90 degress counter clockwise about the given square
    and return the co-ordinates of the new square."""
    x1, y2 = square_rotate_90(x - about_x, y - about_y)
    return (x2 + about_x, y2 + about_y)

def square_reflect_y(x, y):
    """Reflects the given square through the x-axis
    and returns the co-ordinates of the new square"""
    return (x, -y)

def square_reflect_x(x, y):
    """Reflects the given square through the y-axis
    and returns the co-ordinates of the new square"""
    return (-x, y)

def square_reflect_by(x, y, n = 0):
    """Reflects the given square through the x-axis rotated counter clockwise by n * 45 degrees
    and returns the co-ordinates of the new square"""
    (x2, y2) = square_reflect_y(x, y)
    return square_rotate_90(x2, y2, n)

# Shapes #######################################################################

def square_disc(x, y, r):
    """Returns the squares that are at most distance r from the given square"""
    for dx in range(-r, r + 1):
        for dy in range(-r + abs(dx), r - abs(dx) + 1):
            yield (x + dx, y + dy)

def square_line_intersect(x1, y1, x2, y2):
    """Returns squares that intersect the line specified in cartesian co-ordinates"""
    x1 /= edge_length
    y1 /= edge_length
    x2 /= edge_length
    y2 /= edge_length
    dx = x2 - x1
    dy = y2 - y1
    x = floor(x1)
    y = floor(x2)
    stepx = 1 if dx > 0 else -1
    stepy = 1 if dy > 0 else -1
    tx = (x - int(dx <= 0) - x1) / dx
    ty = (y - int(dy <= 0) - y2) / dy
    idx = abs(1 / dx)
    idy = abs(1 / dy)
    yield (x, y)
    while True:
        if tx <= ty:
            if tx > 1: return
            x += stepx
            tx += idx
        else:
            if ty > 1: return
            y += stepy
            ty += idy
        yield (tx, ty)

def square_line(x1, y1, x2, y2):
    """Returns the squares in a shortest path from one square to another, staying as close to the straight line as possible"""
    (fx1, fy1) = square_center(x1, y1)
    (fx2, fy2) = square_center(x2, y2)
    return square_line_intersect(fx1, fy1, fx2, fy2)

def square_rect_intersect(x, y, width, height):
    """Returns the square that intersect the rectangle specified in cartesian co-ordinates"""
    minx = floor(x / edge_length)
    maxx = ceil((x + width) / edge_length)
    miny = floor(y / edge_length)
    maxy = ceil((y + height) / edge_length)
    for x in range(minx, maxx + 1):
        for y  in range(miny, maxy + 1):
            yield (x, y)

def square_rect(rect_x, rect_y, width, height):
    """Returns the squares in a rectangle that includes the given sququre in the bottom left, 
    that extends `height` squares upwards, and `width` squares to the right."""
    for dx in range(width):
        for dy in range(height):
            yield (rect_x + x, rect_y + y)

def square_rect_index(x, y, rect_x, rect_y, width, height):
    """Given a square and a rectangle, gives a linear position of the square.
    The index is an integer between zero and square_rect_size - 1.
    This is useful for array storage of rectangles.
    Returns None if the square is not in the rectangle.
    Equivalent to list(square_rect(...)).index((x, y))"""
    dx = x - rect_x
    dy = y - rect_y
    if dx < 0 or dx >= width or dy < 0 or dy >= height:
        return None
    return dx + dy * width

def square_rect_deindex(index, rect_x, rect_y, width, height):
    """Performs the inverse of square_rect_index
    Equivalent to list(square_rect(...))[index]"""
    dx = index % width
    dy = index // width
    assert dx >= 0 and dy < height
    return (rect_x + dx, rect_y + dy)

def square_rect_size(rect_x, rect_y, width, height):
    """Returns the number of squares in a given rectangle.
    Equivalent to len(list(square_rect(...)))"""
    return width * height

# Nesting ## ###################################################################

parent_width = 3
parent_height = 2

def square_parent(x, y):
    """Returns the parent square containing the given square."""
    return (x // parent_width, y // parent_height)

def square_parent_rect(x, y):
    """Returns the left, bottom, width, height of th rect of a given parent square."""
    return (x * parent_width, y * parent_height, parent_width, parent_height)

def square_parent_children(x, y):
    """Returns all children squares of a given parent square"""
    (x, y, width, height) = square_parent_rect(x, y)
    return square_rect(x, y, width, height)