# This module produces svg diagrams, to assist with testing
# There's no interesting code here

from flat_topped_hex import *
from flat_topped_trihex import *
from updown_tri import *
from square import *
import flat_topped_hex
import updown_tri

poly_style="fill: rgb(244, 244, 241); stroke: rgb(51, 51, 51); stroke-width: 0.1"
stroke_text_style = "fill: rgb(51, 51, 51); font-size: 0.3px;stroke: white; stroke-width: 0.05"
text_style = "fill: rgb(51, 51, 51); font-size: 0.3px;"
xs = """style="fill: hsl( 90, 100%, 35%); font-weight: bold" """
ys = """style="fill: hsl(300, 80%, 50%); font-weight: bold" """
zs = """style="fill: hsl(200, 100%, 45%); font-weight: bold" """

def flip(v):
    return [v[0], -v[1]]

def poly(corners):
    #corners = [corners[2], corners[0]]
    points = " ".join(map(lambda p: ",".join(map(str,flip(p))), corners))
    return f"""<polygon points="{points}" style="{poly_style}" />\n"""

def cell_text(p, x, y, z=None, scale=1):
    text = ""
    text += f"""<g transform="translate({p[0]},{p[1] + 0.08}) scale({scale})">"""
    text += f"""<text text-anchor="middle" alignment-baseline="middle" style="{stroke_text_style}">"""
    text += f"""<tspan {xs}>{x}</tspan>, <tspan {ys}>{y}</tspan>"""
    if z is not None:
        text += f""", <tspan {zs}>{z}</tspan>"""
    text += f"""</text>\n"""
    text += f"""<text text-anchor="middle" alignment-baseline="middle" style="{text_style}">"""
    text += f"""<tspan {xs}>{x}</tspan>, <tspan {ys}>{y}</tspan>"""
    if z is not None:
        text += f""", <tspan {zs}>{z}</tspan>"""
    text += f"""</text>\n"""
    text += "</g>"
    return text

def hex_grid_svg():
    svg = ""
    svg += """<svg viewBox="-3 -3 6 6" width="300px" height="300px" xmlns="http://www.w3.org/2000/svg">\n"""
    flat_topped_hex.edge_length = 0.75
    for x, y, z in hex_disc(0, 0, 0, 4):
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
    svg += """<svg viewBox="-3 -3 6 6" width="300px" height="300px" xmlns="http://www.w3.org/2000/svg">\n"""
    for x, y, z in tri_disc(0, 0, 0, 5):
        center = flip(tri_center(x, y, z))
        svg += poly(tri_corners(x, y, z))
        svg += cell_text(center, x, y, z)
    svg += "</svg>"

    with open("svg/tri_grid.svg", "w") as f:
        f.write(svg)

def tri_neighbours_svg():
    svg = ""
    svg += """<svg viewBox="-10 -10 20 20" xmlns="http://www.w3.org/2000/svg">\n"""
    def off(c, v1, v2): 
        n = v2 - v1
        if n == 0:
            return c
        if n == -1:
            return f"{c} - 1"
        if n == 1:
            return f"{c} + 1"
        assert False
    
    for tri in [[0,1,0],[2,-2,2]]:
        center = flip(tri_center(*tri))
        svg += poly(tri_corners(*tri))
        svg += cell_text(center, "a", "b", "c")
        for (x, y, z) in tri_neighbours(*tri):
            center = flip(tri_center(x, y, z))
            svg += cell_text([center[0], center[1]], off("a", tri[0], x), off("b", tri[1], y), off("c", tri[2], z))

    svg += "</svg>"

    with open("svg/tri_neighbours.svg", "w") as f:
        f.write(svg)

def square_grid_svg():
    svg = ""
    svg += """<svg viewBox="-3 -3 6 6" width="300px" height="300px" xmlns="http://www.w3.org/2000/svg">\n"""
    for x, y in square_disc(0, 0, 6):
        center = flip(square_center(x, y))
        svg += poly(square_corners(x, y))
        svg += cell_text(center, x, y)
    svg += "</svg>"

    with open("svg/square_grid.svg", "w") as f:
        f.write(svg)

def trihex_grid_svg():
    svg = ""
    svg += """<svg viewBox="-3 -3 6 6" width="300px" height="300px" xmlns="http://www.w3.org/2000/svg">\n"""
    for a, b, c in trihex_disc(0, 0, 0, 6):
        center = flip(trihex_center(a, b, c))
        svg += poly(trihex_corners(a, b, c))
    for a, b, c in trihex_disc(0, 0, 0, 6):
        center = flip(trihex_center(a, b, c))
        is_hex = trihex_cell_type(a, b, c) == "hex"
        svg += cell_text(center, a, b, c, 1 if is_hex else 0.8)
    svg += "</svg>"

    with open("svg/trihex_grid.svg", "w") as f:
        f.write(svg)

hex_grid_svg()
hex_neighbours_svg()
tri_grid_svg()
tri_neighbours_svg()
square_grid_svg()
trihex_grid_svg()