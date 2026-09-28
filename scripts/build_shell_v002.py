"""Rea Farms II 3D - Building II geometry validation shell, v002 (refinement pass).

Builds on the approved v001 dimensional control: SAME origin, axes, datums, grids and
face-of-stud control lines. v001 files are not touched. New in v002: exterior wall
build-up (A003), openings checked against A811/A815/A816, CW3 door bay, louvered
sun-shade (A702), door/side canopies (A701), glass railings, terrace closet and the
utility yard screen walls (A012). Every number is documented in
notes/model_control_v002.md with a confidence code:
  W written dimension/datum, G grid position, M measured from exact-scale vector
  linework or elevation raster, A assumption.

Run (from the project root) with:
  "C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe" --background --python scripts/build_shell_v002.py
Optional:  -- --no-render     build and save the .blend only
           -- --out <folder>  write every output into <folder> instead (trial runs)

Units: DATA values are decimal feet; origin = grid 1' x grid K' at Level 01 finish
floor, +X project east, +Y project north, +Z up. Scene is metric at true scale.
The script refuses to overwrite any existing output file.
"""
from pathlib import Path
import json
import math
import sys
import time

import bpy
import bmesh
from mathutils import Vector

VERSION = "v002"
STEM = f"building_shell_{VERSION}"
ROOT = Path(__file__).resolve().parent.parent
BLEND = ROOT / "models" / f"{STEM}.blend"
REPORT = ROOT / "notes" / f"{STEM}_build_report.json"
RENDER_DIR = ROOT / "renders"
FT = 0.3048

# =============================== DATA (feet) ================================
# --- datums (W) - unchanged from v001 ---
AVG_GRADE = -1.8125
L1_FF = 0.0
TERRACE_FF = 15.0 + 2.0 / 12
L2_FF = 16.0
LOW_PARAPET_1 = 17.5
LOW_PARAPET_2 = 19.5
ROOF_STRUCT = 32.0
HIGH_PARAPET_1 = 34.0 + 11.0 / 12
PARAPET_CW2_BAY = 38.0 + 9.5 / 12
HIGH_PARAPET_2 = 42.0
HIGH_PARAPET_3 = 43.0 + 10.0 / 12

# --- grids (G/W) - unchanged from v001 ---
GX = {"1'": 0.0, "1": 1.5, "1.2'": 5.0, "2": 6.0, "3": 32.5, "3.1": 34.5, "4": 59.0,
      "5": 65.5, "6": 80.5, "6'": 82.875, "7": 92.5, "7'": 94.125, "7.1'": 94.375,
      "7.2": 95.5, "8'": 104.646, "8": 105.5, "8.3": 115.5, "8.4": 125.378, "9": 143.5,
      "9'": 144.5, "9.1": 145.125, "9.1'": 147.875, "10": 172.411, "11": 202.0,
      "11'": 203.0, "12": 203.5, "12'": 205.0}
GY = {"K'": 0.0, "K": 1.833, "J'": 2.0, "J": 3.833, "H'": 23.056, "H": 24.533,
      "G": 50.944, "F'": 57.604, "F": 58.789, "E.4": 65.944, "E": 71.833, "D": 77.378,
      "C": 83.789, "B": 96.833, "B'": 97.833, "A": 103.333, "A.1'": 104.917,
      "A'": 105.833, "XA": 113.311}

# --- face-of-stud control values - unchanged from v001 ---
CW2_BAY_Y = 104.417
PIER_W = 3.0 + 8.0 / 12
L2_WEST_X = GX["1.2'"] + 25.5
L2_EAST_X = 174.0
L2_SOUTH_Y = 22.95
L2_NE_Y = 78.961
LOBBY_SOUTH_Y = 48.789

# --- NEW: exterior build-up outside face of stud, A003 (W) ---
EW1 = 9.125 / 12      # EW1/EW3 brick veneer: 1/2 + 1 1/2 + 3 1/2 + 3 5/8
EW2 = 7.125 / 12      # EW2/EW4 "brick insert": 1/2 + 1 1/2 + 1 1/2 + 3 5/8
EW5 = 4.0 / 12        # EW5/EW6/EW7 architectural metal panel: 1/2 + 1 1/2 + 2
GLASS_SETBACK = 2.0 / 12   # A: glass plane 2" inside the face of stud

# --- Level 1 footprint on face of stud (CCW) + build-up + terrace parapet per edge ---
P1 = [(GX["1.2'"], 0.0), (GX["6'"], 0.0), (GX["6'"], GY["J'"]), (GX["7'"], GY["J'"]),
      (GX["7'"], 0.0), (GX["9.1'"], 0.0), (GX["9.1'"], GY["J'"]), (GX["11'"], GY["J'"]),
      (GX["11'"], GY["H'"]), (GX["12'"], GY["H'"]), (GX["12'"], GY["B'"]),
      (GX["9'"], GY["B'"]), (GX["9'"], GY["A'"]), (GX["8'"], GY["A'"]),
      (GX["8'"], CW2_BAY_Y), (GX["7.1'"], CW2_BAY_Y), (GX["7.1'"], GY["A.1'"]),
      (0.0, GY["A.1'"]), (0.0, GY["F'"]), (GX["1.2'"], GY["F'"])]
P1_OFFSET = [EW1, EW2, EW5, EW2, EW1, EW2, EW5, EW5, EW2, EW1,
             EW1, EW5, EW5, EW5, EW5, EW2, EW2, EW2, EW2, EW1]
P1_PARAPET = [LOW_PARAPET_2, LOW_PARAPET_2, LOW_PARAPET_1, LOW_PARAPET_2, LOW_PARAPET_2,
              LOW_PARAPET_2, LOW_PARAPET_1, LOW_PARAPET_1, LOW_PARAPET_2, LOW_PARAPET_2,
              LOW_PARAPET_2, None, None, None, None, None, None, None, None, LOW_PARAPET_2]
TERRACE_PARAPET_T = 1.5           # M (A132 linework, finish face to inside face)
RAIL_EDGES = [2, 6, 7]            # GR-1 on the 17'-6" parapets (A300/A301 raster, A302)
RAIL_TOP = LOW_PARAPET_2          # M: glass top aligns with 19'-6"
RAIL_T = 0.1                      # A

# --- Level 2 roof zones ---
ZONES = {
    "HighBlock": {
        "poly": [(0.0, GY["F'"]), (GX["8'"], GY["F'"]), (GX["8'"], CW2_BAY_Y),
                 (GX["7.1'"], CW2_BAY_Y), (GX["7.1'"], GY["A.1'"]), (0.0, GY["A.1'"])],
        "offset": [EW2, 0.0, EW5, EW2, EW2, EW2],
        "parapet": [HIGH_PARAPET_2, None, PARAPET_CW2_BAY, HIGH_PARAPET_2,
                    HIGH_PARAPET_2, HIGH_PARAPET_2],
        "parapet_t": 1.13,
        "source": "A132 Rev5 42'-0\" / 38'-9 1/2\"; EW2/EW4 tags A112/A122; A003"},
    "LobbyBlock": {
        "poly": [(GX["8'"], LOBBY_SOUTH_Y), (GX["9'"], LOBBY_SOUTH_Y),
                 (GX["9'"], GY["A'"]), (GX["8'"], GY["A'"])],
        "offset": [EW5, EW5, EW5, 0.0],
        "parapet": [HIGH_PARAPET_3] * 4,
        "parapet_t": 1.0,
        "source": "A132 Rev5 43'-10\"; ACM / EW5 A003"},
    "LowRoof": {
        "poly": [(L2_WEST_X, L2_SOUTH_Y), (L2_EAST_X, L2_SOUTH_Y), (L2_EAST_X, L2_NE_Y),
                 (GX["9'"], L2_NE_Y), (GX["9'"], LOBBY_SOUTH_Y), (GX["8'"], LOBBY_SOUTH_Y),
                 (GX["8'"], GY["F'"]), (L2_WEST_X, GY["F'"])],
        "offset": [EW5, EW5, EW5, 0.0, 0.0, 0.0, 0.0, EW5],
        "parapet": [HIGH_PARAPET_1, HIGH_PARAPET_1, HIGH_PARAPET_1, None, None, None,
                    None, HIGH_PARAPET_1],
        "parapet_t": 1.0,
        "source": "A122; A132 Rev5 34'-11\"; EW5 tags A122; A003"},
}

# --- NEW: Level 2 terrace closet (A122 linework M; top from A301 raster M) ---
CLOSET = {"x0": L2_WEST_X - EW5, "x1": 33.5, "y0": 10.378, "y1": L2_SOUTH_Y,
          "z1": HIGH_PARAPET_1}

# --- lobby recess between piers; curtain wall plane on grid A ---
CW_HEAD = 28.0 + 10.875 / 12      # 28'-10 7/8" (W, A815 CW1-CW4)
LOBBY_RECESS = {"x0": GX["8'"] + PIER_W, "x1": GX["9'"] - PIER_W,
                "y_back": GY["A"], "z0": AVG_GRADE, "z1": CW_HEAD}

# --- openings: (normal, stud plane, a0, a1, z0, z1, build-up, tag) ---
L1_SILL, L1_HEAD = 3.0, 13.0 + 11.625 / 12          # A811 SF1/SF3: 3'-0" + 10'-11 5/8"
L2_SILL, L2_HEAD = L2_FF + 3.0, L2_FF + 12.0 + 11.25 / 12   # A811 SF4-SF7
DOOR_BAY = (79.89, 89.85)                           # M; 9'-11 1/2" wide (W, A815)
DOOR_HEAD = 3.0 + 1 / 12 + 5.0 + 0.625 / 12 + 1.0 + 10.0 / 12   # 9'-11 5/8" (W, A815)
OPENINGS = [
    ("N", GY["A.1'"], -EW2, DOOR_BAY[0], 0.0, CW_HEAD, EW2, "CW3 main"),      # glazed NW corner
    ("N", GY["A.1'"], DOOR_BAY[0], DOOR_BAY[1], DOOR_HEAD + 2.0 + 2.75 / 12, CW_HEAD, EW2,
     "CW3 above door bay"),
    ("N", GY["A.1'"], DOOR_BAY[0] + 0.75, DOOR_BAY[1] - 0.5, 0.0, DOOR_HEAD, EW2, "Door 100A"),
    ("N", CW2_BAY_Y, 94.885, 104.135, 0.0, CW_HEAD, EW5, "CW2"),
    ("N", GY["A"], 108.655, 140.489, 0.0, DOOR_HEAD, 0.0, "CW1 lower / 101A"),
    ("N", GY["A"], 108.655, 140.489, 11.70, CW_HEAD, 0.0, "CW1 upper"),
    ("N", GY["B'"], 145.63, 170.63, L1_SILL, L1_HEAD, EW1, "SF3"),
    ("N", GY["B'"], 175.63, 200.63, L1_SILL, L1_HEAD, EW1, "SF3"),
    ("N", L2_NE_Y, 151.667, 173.5, L2_SILL, L2_HEAD, EW5, "SF5B"),
    ("N", L2_NE_Y, 146.875, 150.208, L2_FF, L2_HEAD, EW5, "SF5A"),
    ("E", GX["12'"], 33.70, 48.54, L1_SILL, 10.0, EW1, "SF2"),
    ("E", GX["12'"], 33.70, 36.95, 0.0, 10.0, EW1, "SF2 door"),
    ("E", GX["12'"], 53.5, 63.5, L1_SILL, L1_HEAD, EW1, "SF1"),
    ("E", GX["12'"], 68.5, 93.5, L1_SILL, L1_HEAD, EW1, "SF3"),
    ("E", GX["11'"], 7.08, 17.08, 0.0, 14.0, EW5, "CW6"),
    ("E", L2_EAST_X, 23.5, 48.5, L2_SILL, L2_HEAD, EW5, "SF6"),
    ("E", L2_EAST_X, 53.5, 78.5, L2_SILL, L2_HEAD, EW5, "SF6"),
    ("E", GX["9'"], 83.51, 96.93, L2_SILL, L2_HEAD, EW5, "SF7"),
    ("S", GY["J'"], 153.47, 198.47, 3.0, 14.0, EW5, "CW5"),
    ("W", GX["1.2'"], 4.19, 14.19, L1_SILL, L1_HEAD, EW1, "SF1"),
    ("W", L2_WEST_X, 25.41, 50.41, L2_SILL, L2_HEAD, EW5, "SF6"),
    ("W", 0.0, 74.01, GY["A.1'"] + EW2, 0.0, CW_HEAD, EW2, "CW4"),              # glazed NW corner
]
for x0 in (23.5, 38.5, 53.5, 68.5, 103.5, 118.5, 133.5):
    OPENINGS.append(("S", 0.0, x0, x0 + 10.0, L1_SILL, L1_HEAD, EW1, "SF1"))
for x0, x1 in ((38.5, 63.5), (68.5, 93.5), (98.5, 113.5), (118.5, 143.5), (148.5, 173.5)):
    OPENINGS.append(("S", L2_SOUTH_Y, x0, x1, L2_SILL, L2_HEAD, EW5,
                     "SF4" if x1 - x0 < 20 else "SF6"))

# --- drop-off canopy (A700) - unchanged, heights remain PROVISIONAL (M) ---
CANOPY = {"cols_x": [79.644, 108.233, 140.922], "end_overhang": 2.0 + 2.0 / 12,
          "y_gutter": GY["XA"], "south": 6.625, "north": 16.625,
          "z_gutter_top": 16.1, "slope": 1.5 / 12, "glass_t": 0.25,
          "col_top": 15.0, "col_size": 14.0 / 12}

# --- NEW: door / side canopies (A701; heights from A815/A811 stacks) ---
# (name, normal, wall plane, a0, a1, projection, z_bottom_at_wall, z_top_at_wall, soffit slope, top slope)
SMALL_CANOPIES = [
    ("MainEntry", "N", GY["A"], 108.655, 140.489, 9.0 + 0.125 / 12, DOOR_HEAD, 11.70,
     0.875 / 12, 0.25 / 12),
    ("Door100A", "N", GY["A.1'"], 79.84, 89.90, 7.0 + 5.125 / 12, DOOR_HEAD,
     DOOR_HEAD + 2.0 + 2.75 / 12, 0.875 / 12, 0.25 / 12),
    ("East", "E", GX["12'"], 33.70, 48.54, 3.0 + 11.125 / 12, 10.0, 11.5, 2.0 / 12, 0.25 / 12),
]

# --- NEW: louvered sun-shade (A702 W; TOS 32'-0" S133 W; 12" beam A340) ---
SS_D = 13.0 + 7.0 / 12
SUNSHADE = {
    "x_out": GX["10"] + SS_D, "y_south": GY["H"] - SS_D, "y_north": GY["D"] + SS_D,
    "x_south_start": CLOSET["x1"], "x_north_start": GX["9.1"] + 2.5 / 12,
    "top": ROOF_STRUCT, "depth": 1.0, "beam_w": 0.5,
    "south_beams_x": [44.354, 54.917, 65.5, 75.5, 85.5, 95.5, 105.5, 115.5, 125.375,
                      135.25, 145.125, 154.417, 163.417, 172.417],
    "east_beams_y": [24.533, 33.367, 42.117, 50.95, 59.783, 68.533, 77.367],
    "north_beams_x": [154.417, 163.417, 172.417],
    "louver_n": 12, "louver_oc": 11.0 / 12, "louver_w": 10.0 / 12, "louver_t": 1.0 / 12,
    "louver_angle": 40.0}

# --- NEW: utility yard screen walls (A012 heights W; plan positions M from A112) ---
YARD_WALLS = [  # (name, polygon, top)
    ("Gen_west", [(-20.22, 24.80), (-18.80, 24.80), (-18.80, 64.41), (-20.22, 64.41)], 14.0),
    ("Gen_north_a", [(-18.80, 62.98), (-10.60, 62.98), (-10.60, 64.41), (-18.80, 64.41)], 14.0),
    ("Gen_north_b", [(-6.26, 62.98), (-EW2, 62.98), (-EW2, 64.41), (-6.26, 64.41)], 14.0),
    ("Gen_south_a", [(-18.80, 24.80), (-14.42, 24.80), (-14.42, 26.24), (-18.80, 26.24)], 14.0),
    ("Gen_south_b", [(-11.09, 24.80), (5.0 - EW1, 24.80), (5.0 - EW1, 26.24), (-11.09, 26.24)], 14.0),
    ("Trans_north", [(-26.41, 90.64), (-10.65, 90.64), (-10.65, 91.91), (-26.41, 91.91)], 10.0 / 3),
    ("Trans_south", [(-26.41, 72.80), (-10.65, 72.80), (-10.65, 74.08), (-26.41, 74.08)], 10.0 / 3),
    ("Trans_east", [(-11.92, 74.08), (-10.65, 74.08), (-10.65, 90.64), (-11.92, 90.64)], 10.0 / 3),
    ("Trans_west_s", [(-26.41, 74.08), (-25.14, 74.08), (-25.14, 76.60), (-26.41, 76.60)], 10.0 / 3),
    ("Trans_west_n", [(-26.41, 88.08), (-25.14, 88.08), (-25.14, 90.64), (-26.41, 90.64)], 10.0 / 3),
    ("Site_wall_north_diag", [(-24.06, 98.86), (-22.32, 98.43), (-15.60, 111.55), (-17.14, 112.34)], 10.0 / 3),
    ("Low_wall_stub", [(-20.32, 17.23), (-19.03, 17.23), (-19.03, 24.80), (-20.32, 24.80)], 8.0 / 3),
    ("Low_wall_diag", [(-20.32, 17.23), (1.96, -5.05), (2.48, -3.77), (-19.04, 17.75)], 8.0 / 3),
]
YARD_DOOR_LINTELS = [  # wall above the two enclosure doors; door head 7'-0" is an assumption
    ("Gen_north_lintel", [(-10.60, 62.98), (-6.26, 62.98), (-6.26, 64.41), (-10.60, 64.41)], 7.0, 14.0),
    ("Gen_south_lintel", [(-14.42, 24.80), (-11.09, 24.80), (-11.09, 26.24), (-14.42, 26.24)], 7.0, 14.0),
]
# ============================ END OF DATA ===================================


def m(v):
    return v * FT


def new_material(name, grey):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (grey, grey, grey, 1.0)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (grey, grey, grey, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.85
    return mat


def collection(name):
    col = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(col)
    return col


def mesh_object(name, verts_ft, faces, col, mat, source=""):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata([(m(x), m(y), m(z)) for x, y, z in verts_ft], [], faces)
    mesh.update()
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    col.objects.link(obj)
    obj.data.materials.append(mat)
    if source:
        obj["source"] = source
    return obj


def ccw(poly):
    area = sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1]
               for i in range(len(poly)))
    return poly if area > 0 else list(reversed(poly))


def prism(name, poly, z0, z1, col, mat, source=""):
    n = len(poly)
    verts = [(x, y, z0) for x, y in poly] + [(x, y, z1) for x, y in poly]
    faces = [tuple(reversed(range(n))), tuple(range(n, 2 * n))]
    faces += [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    return mesh_object(name, verts, faces, col, mat, source)


def box(name, x0, x1, y0, y1, z0, z1, col, mat, source=""):
    return prism(name, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], z0, z1, col, mat, source)


def hexa(name, bottom4, top4, col, mat, source=""):
    """Six-sided solid from 4 bottom and 4 top corners given in the same order."""
    faces = [(3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return mesh_object(name, list(bottom4) + list(top4), faces, col, mat, source)


def edge_normal(p, q, inward):
    dx, dy = q[0] - p[0], q[1] - p[1]
    length = math.hypot(dx, dy)
    nx, ny = -dy / length, dx / length           # CCW polygon: left side is inside
    return (nx, ny) if inward else (-nx, -ny)


def offset_poly(poly, dists):
    """Move each edge of a rectilinear CCW polygon outward by its own distance."""
    n = len(poly)
    out = []
    for i in range(n):
        prev_n = edge_normal(poly[i - 1], poly[i], False)
        next_n = edge_normal(poly[i], poly[(i + 1) % n], False)
        out.append((poly[i][0] + prev_n[0] * dists[i - 1] + next_n[0] * dists[i],
                    poly[i][1] + prev_n[1] * dists[i - 1] + next_n[1] * dists[i]))
    return out


def parapets(name, poly, tops, thick, z_base, col, mat, source=""):
    """One prism per edge of the FINISH-face polygon; mitred where both neighbours exist."""
    n = len(poly)
    for i in range(n):
        if tops[i] is None:
            continue
        p, q = poly[i], poly[(i + 1) % n]
        nx, ny = edge_normal(p, q, True)
        ends = []
        for vert, other in ((p, (i - 1) % n), (q, (i + 1) % n)):
            if tops[other] is None:
                ends.append((vert[0] + nx * thick, vert[1] + ny * thick))
            else:
                ox, oy = edge_normal(poly[other], poly[(other + 1) % n], True)
                ends.append((vert[0] + (nx + ox) * thick, vert[1] + (ny + oy) * thick))
        prism(f"{name}_edge{i:02d}", [p, q, ends[1], ends[0]], z_base, tops[i], col, mat, source)


def opening_boxes(normal, plane, a0, a1, buildup):
    """Cutter runs from outside the finish face to the glass plane; panel sits at the glass plane."""
    out, t = buildup + 0.3, 0.05
    g = GLASS_SETBACK
    if normal == "N":
        return (a0, a1, plane - g, plane + out), (a0, a1, plane - g, plane - g + t)
    if normal == "S":
        return (a0, a1, plane - out, plane + g), (a0, a1, plane + g - t, plane + g)
    if normal == "E":
        return (plane - g, plane + out, a0, a1), (plane - g, plane - g + t, a0, a1)
    if normal == "W":
        return (plane - out, plane + g, a0, a1), (plane + g - t, plane + g, a0, a1)
    raise ValueError(normal)


def bbox_ft(obj):
    pts = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    return ([min(p[i] for p in pts) / FT for i in range(3)],
            [max(p[i] for p in pts) / FT for i in range(3)])


def overlaps(a, b, eps=1e-4):
    (amin, amax), (bmin, bmax) = a, b
    return all(amin[i] < bmax[i] - eps and bmin[i] < amax[i] - eps for i in range(3))


def cut(target, cutter):
    mod = target.modifiers.new("cut", "BOOLEAN")
    mod.operation = "DIFFERENCE"
    mod.solver = "EXACT"
    mod.object = cutter
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier=mod.name)


def small_canopy(spec, col, mat):
    name, normal, plane, a0, a1, proj, zb, zt, s_soffit, s_top = spec
    zb_out, zt_out = zb + proj * s_soffit, zt - proj * s_top
    if normal == "N":
        w0, w1, o0, o1 = (a0, plane), (a1, plane), (a0, plane + proj), (a1, plane + proj)
    elif normal == "E":
        w0, w1, o0, o1 = (plane, a0), (plane, a1), (plane + proj, a0), (plane + proj, a1)
    else:
        raise ValueError(normal)
    bottom = [(*w0, zb), (*w1, zb), (*o1, zb_out), (*o0, zb_out)]
    top = [(*w0, zt), (*w1, zt), (*o1, zt_out), (*o0, zt_out)]
    hexa(f"Canopy_{name}", bottom, top, col, mat,
         "A701 plan size + slopes (W); heights from A815/A811 stacks (W) - East top assumed")


def louvers(name, fixed_lo, fixed_hi, run0, run1, along_x, tilt_sign, col, mat):
    """Tilted slats between fixed_lo..fixed_hi, running from run0 to run1."""
    s = SUNSHADE
    span = (s["louver_n"] - 1) * s["louver_oc"]
    start = (fixed_lo + fixed_hi) / 2 - span / 2
    zc = s["top"] - s["depth"] / 2
    ang = math.radians(s["louver_angle"])
    hw, ht = s["louver_w"] / 2, s["louver_t"] / 2
    for k in range(s["louver_n"]):
        c = start + k * s["louver_oc"]
        corners = []
        for du, dv in ((-hw, -ht), (hw, -ht), (hw, ht), (-hw, ht)):
            across = du * math.cos(ang) - dv * math.sin(ang)
            up = du * math.sin(ang) + dv * math.cos(ang)
            corners.append((c + tilt_sign * across, zc + up))
        if along_x:
            a = [(run0, p, z) for p, z in corners]
            b = [(run1, p, z) for p, z in corners]
        else:
            a = [(p, run0, z) for p, z in corners]
            b = [(p, run1, z) for p, z in corners]
        hexa(f"{name}_{k:02d}", a, b, col, mat, "A702 (12) 1x10 louvers at 40 deg, 11\" o.c. (W); tilt direction assumed")


def look_at(obj, target_ft):
    direction = Vector([m(c) for c in target_ft]) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def add_camera(name, loc_ft, target_ft, col, ortho_ft=None, lens=35.0):
    cam = bpy.data.cameras.new(name)
    cam.clip_start, cam.clip_end = 0.5, 2000.0
    if ortho_ft:
        cam.type = "ORTHO"
        cam.ortho_scale = m(ortho_ft)
    else:
        cam.lens = lens
    obj = bpy.data.objects.new(name, cam)
    obj.location = [m(c) for c in loc_ft]
    col.objects.link(obj)
    look_at(obj, target_ft)
    return obj


def setup_gpu(scene):
    scene.render.engine = "CYCLES"
    info = {"backend": "CPU", "devices": []}
    try:
        prefs = bpy.context.preferences.addons["cycles"].preferences
        for backend in ("OPTIX", "CUDA"):
            try:
                prefs.compute_device_type = backend
            except TypeError:
                continue
            prefs.refresh_devices()
            gpus = [d for d in prefs.devices if d.type == backend]
            if gpus:
                for d in prefs.devices:
                    d.use = d.type == backend
                scene.cycles.device = "GPU"
                info = {"backend": backend, "devices": [d.name for d in gpus]}
                break
    except Exception as exc:
        info["error"] = str(exc)
    return info


def main():
    global BLEND, REPORT, RENDER_DIR
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    do_render = "--no-render" not in argv
    if "--out" in argv:
        out = Path(argv[argv.index("--out") + 1])
        BLEND, REPORT, RENDER_DIR = out / BLEND.name, out / REPORT.name, out
    views = ["front_north", "rear_south", "left_east", "right_west", "oblique_northeast"]
    outputs = [BLEND, REPORT] + ([RENDER_DIR / f"{STEM}_{v}.png" for v in views] if do_render else [])
    for path in outputs:
        if path.exists():
            raise SystemExit(f"Refusing to overwrite existing file: {path}")

    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "IMPERIAL"
    scene.unit_settings.length_unit = "FEET"
    scene.unit_settings.scale_length = 1.0

    wall = new_material("CLAY_wall", 0.62)
    dark = new_material("CLAY_opening", 0.12)
    canopy_mat = new_material("CLAY_canopy", 0.42)
    ground_mat = new_material("CLAY_ground", 0.30)
    context_mat = new_material("CLAY_context", 0.08)
    yard_mat = new_material("CLAY_yard_wall", 0.52)

    c_mass = collection("01_Masses")
    c_par = collection("02_Parapets")
    c_open = collection("03_Opening_panels")
    c_can = collection("04_DropOff_Canopy_PROVISIONAL")
    c_small = collection("05_Door_Side_Canopies")
    c_ss = collection("06_SunShade")
    c_rail = collection("07_Glass_Railings")
    c_yard = collection("08_Utility_Yard")
    c_site = collection("09_Site_context")
    c_cam = collection("10_Cameras_Lights")
    c_cut = collection("zz_Cutters")

    # ---- masses on the FINISH face (stud control line + A003 build-up) ----
    p1_finish = offset_poly(P1, P1_OFFSET)
    masses = [prism("L1_Podium", p1_finish, AVG_GRADE, TERRACE_FF, c_mass, wall,
                    "A112 Rev5 face-of-stud grids + A003 build-up")]
    finish = {}
    for zname, zone in ZONES.items():
        finish[zname] = offset_poly(zone["poly"], zone["offset"])
        masses.append(prism(f"L2_{zname}", finish[zname], TERRACE_FF, ROOF_STRUCT,
                            c_mass, wall, zone["source"]))
    c = CLOSET
    masses.append(box("L2_Terrace_closet", c["x0"], c["x1"], c["y0"], c["y1"], TERRACE_FF, c["z1"],
                      c_mass, wall, "A122 linework (M); top 34'-11\" from A301 (M); EW7"))

    # ---- parapets ----
    parapets("Par_Terrace", p1_finish, P1_PARAPET, TERRACE_PARAPET_T, TERRACE_FF, c_par, wall,
             "A132 Rev5 19'-6\" / 17'-6\" (W); thickness M")
    for zname, zone in ZONES.items():
        parapets(f"Par_{zname}", finish[zname], zone["parapet"], zone["parapet_t"], ROOF_STRUCT,
                 c_par, wall, zone["source"])

    # ---- glass railings on the 17'-6" parapets ----
    n1 = len(p1_finish)
    for i in RAIL_EDGES:
        p, q = p1_finish[i], p1_finish[(i + 1) % n1]
        nx, ny = edge_normal(p, q, True)
        d0, d1 = TERRACE_PARAPET_T / 2 - RAIL_T / 2, TERRACE_PARAPET_T / 2 + RAIL_T / 2
        quad = [(p[0] + nx * d0, p[1] + ny * d0), (q[0] + nx * d0, q[1] + ny * d0),
                (q[0] + nx * d1, q[1] + ny * d1), (p[0] + nx * d1, p[1] + ny * d1)]
        prism(f"GlassRail_edge{i:02d}", ccw(quad), P1_PARAPET[i], RAIL_TOP, c_rail, canopy_mat,
              "GR-1: extents and 17'-6\" to 19'-6\" from A300/A301 (M); centred on parapet (A)")

    # ---- cutters ----
    r = LOBBY_RECESS
    cutters = [box("CUT_lobby_recess", r["x0"], r["x1"], r["y_back"], GY["A'"] + 1.0,
                   r["z0"] - 0.5, r["z1"], c_cut, dark, "A112/A122 piers 3'-8\", grid A")]
    for i, (normal, plane, a0, a1, z0, z1, buildup, tag) in enumerate(OPENINGS):
        cxy, pxy = opening_boxes(normal, plane, a0, a1, buildup)
        cutters.append(box(f"CUT_{i:02d}_{normal}", *cxy, z0, z1, c_cut, dark, tag))
        panel = box(f"Opening_{i:02d}_{normal}_{tag.split()[0]}", *pxy, z0, z1, c_open, dark, tag)
        panel["tag"] = tag
    bpy.context.view_layer.update()
    cut_count = 0
    for cutter in cutters:
        cb = bbox_ft(cutter)
        for mass in masses:
            if overlaps(bbox_ft(mass), cb):
                cut(mass, cutter)
                cut_count += 1
    c_cut.hide_render = True
    c_cut.hide_viewport = True

    # ---- drop-off canopy (unchanged from v001, provisional heights) ----
    cn = CANOPY
    x0, x1 = cn["cols_x"][0] - cn["end_overhang"], cn["cols_x"][-1] + cn["end_overhang"]
    yg, zt, t = cn["y_gutter"], cn["z_gutter_top"], cn["glass_t"]
    for label, y_edge, run in (("south", yg - cn["south"], cn["south"]),
                               ("north", yg + cn["north"], cn["north"])):
        ze = zt + run * cn["slope"]
        hexa(f"Canopy_glass_{label}",
             [(x0, yg, zt - t), (x1, yg, zt - t), (x1, y_edge, ze - t), (x0, y_edge, ze - t)],
             [(x0, yg, zt), (x1, yg, zt), (x1, y_edge, ze), (x0, y_edge, ze)], c_can, canopy_mat,
             "A700 Rev5 plan + slope (W); HEIGHTS PROVISIONAL - measured (M)")
    h = cn["col_size"] / 2
    for i, cx in enumerate(cn["cols_x"], 1):
        box(f"Canopy_column_X{i}", cx - h, cx + h, yg - h, yg + h, AVG_GRADE, cn["col_top"],
            c_can, canopy_mat, "A700 Rev5 grid XA (G); size and top PROVISIONAL (A/M)")

    # ---- door / side canopies ----
    for spec in SMALL_CANOPIES:
        small_canopy(spec, c_small, canopy_mat)

    # ---- louvered sun-shade ----
    s = SUNSHADE
    zt_ss, zb_ss, bw = s["top"], s["top"] - s["depth"], s["beam_w"]
    wall_s = L2_SOUTH_Y - EW5
    wall_e = L2_EAST_X + EW5
    wall_n = L2_NE_Y + EW5
    src = "A702 plan dims (W); TOS 32'-0\" S133 Rev5 (W); 12\" beam A340 (W)"
    box("SS_edge_south", s["x_south_start"], s["x_out"], s["y_south"], s["y_south"] + bw, zb_ss, zt_ss, c_ss, canopy_mat, src)
    box("SS_edge_east", s["x_out"] - bw, s["x_out"], s["y_south"], s["y_north"], zb_ss, zt_ss, c_ss, canopy_mat, src)
    box("SS_edge_north", s["x_north_start"], s["x_out"], s["y_north"] - bw, s["y_north"], zb_ss, zt_ss, c_ss, canopy_mat, src)
    box("SS_end_south_west", s["x_south_start"], s["x_south_start"] + bw, s["y_south"], wall_s, zb_ss, zt_ss, c_ss, canopy_mat, src)
    box("SS_end_north_west", s["x_north_start"], s["x_north_start"] + bw, wall_n, s["y_north"], zb_ss, zt_ss, c_ss, canopy_mat, src)
    for k, bx in enumerate(s["south_beams_x"]):
        box(f"SS_beam_south_{k:02d}", bx - bw / 2, bx + bw / 2, s["y_south"], wall_s, zb_ss, zt_ss, c_ss, canopy_mat, src)
    for k, by in enumerate(s["east_beams_y"]):
        box(f"SS_beam_east_{k:02d}", wall_e, s["x_out"], by - bw / 2, by + bw / 2, zb_ss, zt_ss, c_ss, canopy_mat, src)
    for k, bx in enumerate(s["north_beams_x"]):
        box(f"SS_beam_north_{k:02d}", bx - bw / 2, bx + bw / 2, wall_n, s["y_north"], zb_ss, zt_ss, c_ss, canopy_mat, src)
    xc, yc_s, yc_n = GX["10"], GY["H"], GY["D"]
    for label, a, b in (("SE", (xc, yc_s), (s["x_out"], s["y_south"])), ("NE", (xc, yc_n), (s["x_out"], s["y_north"]))):
        dx, dy = b[0] - a[0], b[1] - a[1]
        length = math.hypot(dx, dy)
        px, py = -dy / length * bw / 2, dx / length * bw / 2
        quad = ccw([(a[0] + px, a[1] + py), (b[0] + px, b[1] + py), (b[0] - px, b[1] - py), (a[0] - px, a[1] - py)])
        prism(f"SS_hip_{label}", quad, zb_ss, zt_ss, c_ss, canopy_mat, src)
    louvers("SS_louver_south", s["y_south"] + bw, wall_s, s["x_south_start"] + bw, xc, True, 1, c_ss, canopy_mat)
    louvers("SS_louver_east", wall_e, s["x_out"] - bw, yc_s, yc_n, False, -1, c_ss, canopy_mat)
    louvers("SS_louver_north", wall_n, s["y_north"] - bw, s["x_north_start"] + bw, xc, True, -1, c_ss, canopy_mat)

    # ---- utility yard screen walls ----
    for name, poly, top in YARD_WALLS:
        prism(f"Yard_{name}", ccw(poly), AVG_GRADE, top, c_yard, yard_mat,
              "A012 Rev5 T.O. masonry (W); plan position from A112 linework (M)")
    for name, poly, z0, z1 in YARD_DOOR_LINTELS:
        prism(f"Yard_{name}", ccw(poly), z0, z1, c_yard, yard_mat, "door head 7'-0\" ASSUMED")

    # ---- minimal site context (unchanged) ----
    box("Ground_flat_at_average_grade", -150, 355, -120, 260, AVG_GRADE - 1.0, AVG_GRADE,
        c_site, ground_mat, "Average Grade -1'-9 3/4\" (W); flat is an assumption")
    ax, ay, z = 250.0, 150.0, AVG_GRADE + 0.05
    mesh_object("North_arrow", [(ax - 6, ay, z), (ax + 6, ay, z), (ax + 6, ay + 30, z),
                                (ax + 14, ay + 30, z), (ax, ay + 50, z), (ax - 14, ay + 30, z),
                                (ax - 6, ay + 30, z)], [(0, 1, 2, 3, 4, 5, 6)], c_site, context_mat,
                "Project north, A112")
    for text, loc, size, rot in (("N", (ax - 5, ay + 54, z), 14.0, 0),
                                 ("FRONT / NORTH: parking lot, Golf Links Dr beyond", (215, 175, z), 7.0, 180),
                                 ("EXISTING BUILDING I (not modeled)", (250, -10, z), 7.0, 90)):
        curve = bpy.data.curves.new(text[:12], "FONT")
        curve.body = text
        curve.size = m(size)
        tobj = bpy.data.objects.new("Label_" + text[:12], curve)
        tobj.location = [m(v) for v in loc]
        tobj.rotation_euler = (0, 0, math.radians(rot))
        c_site.objects.link(tobj)
        tobj.data.materials.append(context_mat)

    # ---- lights, world, cameras (same set-up as v001; N/S views widened for the yard) ----
    sun = bpy.data.lights.new("Sun", "SUN")
    sun.energy = 3.0
    sun.angle = math.radians(3)
    sun_obj = bpy.data.objects.new("Sun", sun)
    sun_obj.rotation_euler = (math.radians(55), 0, math.radians(250))
    c_cam.objects.link(sun_obj)
    world = bpy.data.worlds.new("Clay_world")
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.50, 0.56, 0.66, 1)
    bg.inputs[1].default_value = 0.7
    scene.world = world

    cx, cy, cz = 92.0, 58.0, 18.0
    cams = {
        "front_north": (add_camera("Cam_front_north", (cx, 500, cz), (cx, cy, cz), c_cam, 275), (2600, 900)),
        "rear_south": (add_camera("Cam_rear_south", (cx, -400, cz), (cx, cy, cz), c_cam, 275), (2600, 900)),
        "left_east": (add_camera("Cam_left_east", (600, cy + 4, cz), (cx, cy + 4, cz), c_cam, 190), (2400, 1000)),
        "right_west": (add_camera("Cam_right_west", (-400, cy + 4, cz), (cx, cy + 4, cz), c_cam, 190), (2400, 1000)),
        "oblique_northeast": (add_camera("Cam_oblique_NE", (330, 290, 150), (105, 55, 12), c_cam, None, 40.0), (2400, 1350)),
    }
    scene.camera = cams["oblique_northeast"][0]

    # ---- checks: control lines preserved, finish faces where A003 puts them ----
    lo, hi = [1e9] * 3, [-1e9] * 3
    for col in (c_mass, c_par):
        for obj in col.objects:
            bmin, bmax = bbox_ft(obj)
            lo = [min(a, b) for a, b in zip(lo, bmin)]
            hi = [max(a, b) for a, b in zip(hi, bmax)]
    expected = {"x_min": -EW2, "x_max": 205.0 + EW1, "y_min": -EW1, "y_max": GY["A'"] + EW5,
                "top": HIGH_PARAPET_3}
    report = {"version": VERSION, "blender": bpy.app.version_string,
              "control_box_face_of_stud_ft": [205.0, 105.833],
              "building_bbox_finish_ft": {"min": [round(v, 3) for v in lo], "max": [round(v, 3) for v in hi]},
              "expected_finish_ft": {k: round(v, 3) for k, v in expected.items()},
              "boolean_cuts_applied": cut_count, "openings": len(OPENINGS),
              "objects": {col.name: len(col.objects) for col in bpy.data.collections},
              "mass_faces": {o.name: len(o.data.polygons) for o in masses}}
    assert abs(lo[0] - expected["x_min"]) < 0.01 and abs(hi[0] - expected["x_max"]) < 0.01, "X finish check"
    assert abs(lo[1] - expected["y_min"]) < 0.01 and abs(hi[1] - expected["y_max"]) < 0.01, "Y finish check"
    assert abs(hi[2] - expected["top"]) < 0.01, "top of parapet check"

    bpy.context.preferences.filepaths.save_version = 0   # session only: no .blend1 copies
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))

    if do_render:
        report["gpu"] = setup_gpu(scene)
        scene.cycles.samples = 64
        scene.cycles.use_denoising = True
        scene.render.image_settings.file_format = "PNG"
        scene.view_settings.view_transform = "Standard"
        times = {}
        for view, (cam, (rx, ry)) in cams.items():
            scene.camera = cam
            scene.render.resolution_x, scene.render.resolution_y = rx, ry
            scene.render.filepath = str(RENDER_DIR / f"{STEM}_{view}.png")
            t0 = time.time()
            bpy.ops.render.render(write_still=True)
            times[view] = round(time.time() - t0, 1)
        report["render_seconds"] = times
        scene.camera = cams["oblique_northeast"][0]
        bpy.ops.wm.save_mainfile()

    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("BUILD_REPORT=" + json.dumps(report))


if __name__ == "__main__":
    main()
