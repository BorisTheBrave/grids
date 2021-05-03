# This module produces svg diagrams, to assist with testing
from flat_topped_hex import *
from updown_tri import *
import updown_tri

poly_style="fill: rgb(244, 244, 241); stroke: rgb(51, 51, 51); stroke-width: 0.1"
text_style = "fill: rgb(51, 51, 51); font-size: 0.25px"

def flip(v):
    return [v[0], -v[1]]

def poly(corners):
    points = " ".join(map(lambda p: ",".join(map(str,flip(p))), corners))
    return f"""<polygon points="{points}" style="{poly_style}" />\n"""

def cell_text(p, x, y, z):
    text = f"({x}, {y}, {z})"
    return f"""<text x="{p[0]}" y="{p[1]}" text-anchor="middle" alignment-baseline="middle" style="{text_style}">{text}</text>\n"""

def hex_grid():
    svg = ""
    svg += """<svg viewBox="-10 -10 20 20" xmlns="http://www.w3.org/2000/svg">\n"""
    svg += """<rect x="-10" y="-10" width="20" height="20" style="fill: none; stroke: blue"/>\n"""
    for x in range(-5, 5):
        for y in range(-5, 5):
            z = - x - y
            center = flip(hex_center(x, y, z))
            svg += poly(hex_corners(x, y, z))
            svg += cell_text(center, x, y, z)
    svg += "</svg>"

    with open("svg/hex_grid.svg", "w") as f:
        f.write(svg)

def tri_grid():
    updown_tri.edge_length = 2
    svg = ""
    svg += """<svg viewBox="-10 -10 20 20" xmlns="http://www.w3.org/2000/svg">\n"""
    svg += """<rect x="-10" y="-10" width="20" height="20" style="fill: none; stroke: blue"/>\n"""
    for x in range(-5, 5):
        for y in range(-5, 5):
            for t in range(2):
                z = 2 - t - x - y
                center = flip(tri_center(x, y, z))
                svg += poly(tri_corners(x, y, z))
                svg += cell_text(center, x, y, z)
    svg += "</svg>"

    with open("svg/tri_grid.svg", "w") as f:
        f.write(svg)

hex_grid()
tri_grid()