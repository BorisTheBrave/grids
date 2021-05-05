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
    text = f"{x}, {y}, {z}"
    return f"""<text x="{p[0]}" y="{p[1]}" text-anchor="middle" alignment-baseline="middle" style="{text_style}">{text}</text>\n"""

def hex_grid_svg():
    svg = ""
    svg += """<svg viewBox="-10 -10 20 20" xmlns="http://www.w3.org/2000/svg">\n"""
    svg += """<rect x="-10" y="-10" width="20" height="20" style="fill: none; stroke: blue"/>\n"""
    for x, y, z in hex_disc(0, 0, 0, 2):
        center = flip(hex_center(x, y, z))
        svg += poly(hex_corners(x, y, z))
        svg += cell_text(center, x, y, z)
    svg += "</svg>"

    with open("svg/hex_grid.svg", "w") as f:
        f.write(svg)

def hex_neighbours_svg():
    svg = ""
    svg += """<svg viewBox="-10 -10 20 20" xmlns="http://www.w3.org/2000/svg">\n"""
    svg += """<rect x="-10" y="-10" width="20" height="20" style="fill: none; stroke: blue"/>\n"""
    center = flip(hex_center(0, 0, 0))
    svg += poly(hex_corners(0, 0, 0))
    def pm(n): 
        return "0" if n == 0 else f"+{n}" if n > 0 else f"{n}"
    for (x, y, z) in hex_neighbours(0, 0, 0):
        center = flip(hex_center(x, y, z))
        f = 0.8
        svg += cell_text([center[0] * 0.85, center[1] * 0.7], pm(x), pm(y), pm(z))
    svg += "</svg>"

    with open("svg/hex_neighbours.svg", "w") as f:
        f.write(svg)

def tri_grid_svg():
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

def tri_neighbours_svg():
    svg = ""
    svg += """<svg viewBox="-10 -10 20 20" xmlns="http://www.w3.org/2000/svg">\n"""
    svg += """<rect x="-10" y="-10" width="20" height="20" style="fill: none; stroke: blue"/>\n"""
    def pm(n): 
        return "0" if n == 0 else f"+{n}" if n > 0 else f"{n}"
    
    for tri in [[0,1,0],[2,-2,2]]:
        center = flip(tri_center(*tri))
        svg += poly(tri_corners(*tri))
        for (x, y, z) in tri_neighbours(*tri):
            center = flip(tri_center(x, y, z))
            f = 0.8
            svg += cell_text([center[0] * 1, center[1] * 1], pm(x - tri[0]), pm(y - tri[1]), pm(z - tri[2]))

    svg += "</svg>"

    with open("svg/tri_neighbours.svg", "w") as f:
        f.write(svg)

hex_grid_svg()
hex_neighbours_svg()
tri_grid_svg()
tri_neighbours_svg()