"""Rea Farms II 3D - Building II, v012: VEGETATION REALISM PASS on the frozen v011 model.

Everything = v011, rebuilt by the identical code. v012 then swaps the MESH and MATERIAL of the existing
plant and tree objects for procedurally generated leaf-card plants (fixed seed, no external assets) and
adds shader breakup to lawn and mulch. No plant location, quantity, bed outline, site or building
geometry changes; cameras, sun and exposure are those of v010/v011, plus one landscape view.
See notes/vegetation_control_v012.md.

--- v011 header follows ---
Rea Farms II 3D - Building II, v011: CONTEXT-ONLY REALISM PASS on the frozen v010 presentation model.

Building II, its site, landscape, materials, lighting, exposure and the six cameras = v010, rebuilt by
the identical code. v011 adds surrounding context only (collection "14_Context_v011", objects CTX_...):
Building I massing, parking islands, streets, sidewalks, lawns, street / island trees, distant buildings
and a wooded horizon. Confidence of every element: notes/context_control_v011.md.

--- v010 header follows ---
Rea Farms II 3D - Building II, v010: PHOTOREALISTIC PRESENTATION PASS on the frozen v009 model.

Geometry, material assignments, site and planting = v009, rebuilt by the identical code and data.
v010 changes presentation only: shader response of the existing materials (names and assignments
unchanged), physical daylight, exposure, eye-level cameras, and a backdrop ground outside the
modeled site (collection "13_Presentation_v010"). No signage, branding, people, vehicles or new
planting. See notes/presentation_control_v010.md.

--- v009 header follows ---
Rea Farms II 3D - Building II, v009: ENTRANCE PAVING / PLANTING COORDINATION on v008.

See notes/site_landscape_coordination_v009.md. Only the hardscape west of the north entrance
changes: the walk follows the documented S-curve (CS-101 rev 6 and LP-101: R10.50 ft inner curve,
8.50 ft band), the bed between the curve and the building gets its own ground, the unlabelled strip
against the building gets a placeholder, and the 29 seasonal annuals are re-packed inside the
documented bed. The v007 interpolation inputs are kept, so the terrain and every other object are
identical to v008.

--- v008 header follows ---
Rea Farms II 3D - Building II, v008: LANDSCAPE PASS on the frozen v007 site.

Building and site = v007, rebuilt by the identical code and data. v008 adds only the collection
"12_Landscape_v008": plant proxies from the LP-101 Plant Schedule BLDG II plus thin mulch / lawn
surface patches. See notes/landscape_control_v008.md. Nothing in v007 is moved to make planting fit.

--- v007 header follows ---
Rea Farms II 3D - Building II, v007: SITE COORDINATION CORRECTIONS on v006.

See notes/site_coordination_review_v007.md. Building (v005) untouched. Two site changes only:
  1. Transformer enclosure interior is at the LOW (west street) level: pad 655.32 at the gate
     (CG-101 spot; S141 CMU-5/6/7 show 9'-4" walls and a full-height gate from -6'-0").
     v006 had wrongly placed the pad at 659.94, which is the walk grade east of the wall.
  2. South-west low site wall is a RETAINING wall (A012 B2): retained fill at 659.71 added
     on its inner side. The wall itself is unchanged (top +2'-8" per A012 and S141).

--- v006 header follows ---
Rea Farms II 3D - Building II, v006: SITE AND GRADING PASS.

Building = frozen v005, rebuilt by the identical code and data below (building geometry,
materials and facade detail untouched; the building is not moved). v006 replaces the flat
placeholder ground with the documented site: interpolated terrain through the CG-101 spot
elevations and contours, paver walks, drop-off band, entry plaza, stairs, yard slabs,
parking islands and foundation skirts. See notes/site_control_v006.md. All terrain between
written spot elevations is INTERPOLATED, not exact.

--- v005 header follows ---
Rea Farms II 3D - Building II, v005: TARGETED CORRECTION PASS on v004.

v005 = v004 with exactly two kinds of change (see notes/shell_comparison_v004_to_v005.md):
  1. GEOMETRY: door 100A inside its CW3 bay now has the 9" panel on the EAST jamb and the
     6" panel on the WEST jamb, as drawn on A815 (v002-v004 had them reversed, which put
     the door opening 3" too far east). Only the door opening, its glass panel, its
     frame/mullion overlay and the three door-bay panel overlays move.
  2. MATERIALS: updated only where the project specifications are clear
     (notes/material_control_v005.md): frames are a painted 3-coat fluoropolymer finish
     (not metallic); terrace paving is 24" x 24" pedestal-set concrete pavers (colour still
     unresolved); source notes on the other materials now cite the specification.

--- v004 header follows ---
Rea Farms II 3D - Building II, v004: FIRST MATERIALS / FACADE-DETAILING PASS.

Geometry = frozen v003, rebuilt by the identical code and data below (nothing in the
DATA section or the geometry functions was edited). v004 adds only:
  1. materials, assigned per face (see notes/material_control_v004.md), and
  2. thin overlay objects in collection "11_Facade_Detail_v004" (frames, mullions,
     spandrel panels, door-bay panel, hollow-metal door leaves).
Unresolved finishes use neutral placeholders named UNRES_*. Colours of named finishes
are approximations only (no colour values exist on the drawings).

--- v003 header follows ---
Rea Farms II 3D - Building II geometry validation shell, v003 (drop-off canopy only).

v003 = v002 with ONE change: the drop-off canopy now follows the written steel
elevations on structural sheet S132, Section 01 (Approved set p.73). Every other
value, function and object is identical to v002. See notes/model_control_v003.md.

--- v002 header follows ---
Rea Farms II 3D - Building II geometry validation shell, v002 (refinement pass).

Builds on the approved v001 dimensional control: SAME origin, axes, datums, grids and
face-of-stud control lines. v001 files are not touched. New in v002: exterior wall
build-up (A003), openings checked against A811/A815/A816, CW3 door bay, louvered
sun-shade (A702), door/side canopies (A701), glass railings, terrace closet and the
utility yard screen walls (A012). Every number is documented in
notes/model_control_v002.md with a confidence code:
  W written dimension/datum, G grid position, M measured from exact-scale vector
  linework or elevation raster, A assumption.

Run (from the project root) with:
  "C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe" --background --python scripts/build_shell_v012.py
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

VERSION = "v012"
STEM = f"building_shell_{VERSION}"
ROOT = Path(__file__).resolve().parent.parent
BLEND = ROOT / "models" / f"{STEM}.blend"
REPORT = ROOT / "notes" / f"{STEM}_build_report.json"
RENDER_DIR = ROOT / "renders"
FT = 0.3048
RENDER_SAMPLES_V010 = 256
EXPOSURE_V010 = -0.35

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
DOOR_JAMB_WEST, DOOR_JAMB_EAST = 6.0 / 12, 9.0 / 12  # W, A815 (drawn from outside: left = east)
DOOR_HEAD = 3.0 + 1 / 12 + 5.0 + 0.625 / 12 + 1.0 + 10.0 / 12   # 9'-11 5/8" (W, A815)
OPENINGS = [
    ("N", GY["A.1'"], -EW2, DOOR_BAY[0], 0.0, CW_HEAD, EW2, "CW3 main"),      # glazed NW corner
    ("N", GY["A.1'"], DOOR_BAY[0], DOOR_BAY[1], DOOR_HEAD + 2.0 + 2.75 / 12, CW_HEAD, EW2,
     "CW3 above door bay"),
    ("N", GY["A.1'"], DOOR_BAY[0] + DOOR_JAMB_WEST, DOOR_BAY[1] - DOOR_JAMB_EAST, 0.0, DOOR_HEAD, EW2,
     "Door 100A"),                                  # v005: corrected, 6" west / 9" east (A815)
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

# --- drop-off canopy: plan A700 Rev5 (W); STEEL ELEVATIONS S132 Section 01 (W) - CHANGED in v003 ---
CANOPY = {"cols_x": [79.644, 108.233, 140.922], "end_overhang": 2.0 + 2.0 / 12,
          "y_gutter": GY["XA"], "south": 6.625, "north": 16.625,      # W: A700 and S132
          "slope": 1.5 / 12,                                           # W: A700; S132 linework = 0.1250
          "tos_north_tip": 16.0 + 11.9375 / 12,                        # W: 16'-11 15/16" top of W27x84 at north tip
          "bos_north_tip": 16.0 + 4.0 / 12,                            # W: 16'-4"
          "tos_south_tip": 15.0 + 8.9375 / 12,                         # W: 15'-8 15/16"
          "bos_south_tip": 15.0 + 1.0 / 12,                            # W: 15'-1"
          "bos_at_column": 13.0,                                       # W: 13'-0"
          "col_top": 15.0 + 1.5 / 12,                                  # W: 15'-1 1/2" top of cap plate
          "col_depth_ns": 16.97 / 12, "col_width_ew": 10.425 / 12,     # W: W16X100 (AISC section size)
          "beam_w": 10.0 / 12,                                         # W: W27X84 (PC) with 10" x 3/4" plate
          "purlin_d": 1.0, "purlin_w": 0.5,                            # W: HSS12X6X3/8
          "purlin_from_tip": 0.5, "purlin_oc_north": 5.0 + 0.375 / 12, # W: 0'-6", 5'-0 3/8" (along slope)
          "purlin_oc_south": 5.0 + 0.25 / 12, "purlins_north": 4, "purlins_south": 2,
          "glass_above_tos": 1.322,                                    # M: S132 linework, top of beam to top of glass
          "glass_t": 1.0 / 12,                                         # W: A700 "1\" laminated clear glazing"
          "glass_gap_from_xa": 0.364}                                  # M: S132 linework, glass stops short of the gutter

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
        pobj = prism(f"{name}_edge{i:02d}", [p, q, ends[1], ends[0]], z_base, tops[i], col, mat, source)
        pobj["edge"], pobj["inward_x"], pobj["inward_y"] = i, nx, ny      # v004: used for material assignment only


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


# ===================== v004 MATERIALS AND FACADE DETAIL (no geometry edits) =====================
CW_HORIZ = [3.0 + 1 / 12, 8.0 + 1.625 / 12, DOOR_HEAD, 13.0 + 8.625 / 12, 16.0 + 3.625 / 12,
            18.0 + 11 / 12, 25.0 + 10 / 12]                     # A815 stack (W)
CW_CAPS = [DOOR_HEAD, 13.0 + 8.625 / 12, 16.0 + 3.625 / 12, 25.0 + 10 / 12]   # A815 leaders
CW_SPANDREL = (13.0 + 8.625 / 12, 16.0 + 3.625 / 12)            # G3 band
SF_L1_HORIZ = [8.0 + 1 / 12, 9.0 + 1 / 12]                      # A811 SF1/SF3: 3'-0" + 5'-1" + 1'-0"
SF_L2_HORIZ = [L2_SILL + 6.0 + 8.375 / 12]                      # A811 SF4-SF7
LAYOUT = {   # tag -> (system, start or None, bays in +axis order or count, horizontals, caps, spandrel)
    "CW3": ("CW", DOOR_BAY[1] - (90.0 + 1 / 12), [5.0625] + [5.0] * 14 + [5.0625, 4.979, 4.979],
            CW_HORIZ, CW_CAPS, CW_SPANDREL),
    "CW4": ("CW", 74.01, [5.156] + [5.0 + 2 / 12] * 5, CW_HORIZ, CW_CAPS, CW_SPANDREL),
    "CW2": ("CW", 94.885, [4.625, 4.625], CW_HORIZ, CW_CAPS, CW_SPANDREL),
    "CW1": ("CW", 108.655, [8.896, 7.021, 7.021, 8.896], [8.0 + 1.625 / 12, 13.71, 16.29, 18.91, 25.82],
            [13.71, 16.29, 25.82], (11.70, 13.71)),
    "CW5": ("CW", 153.47, [5.0] * 9, [8.0 + 2 / 12, 10.0], [10.0], None),
    "CW6": ("CW", 7.08, [3.865, 6.135], [8.0 + 2 / 12, 10.0], [10.0], None),
    "Door": ("CW", None, [1.479, 6.0, 1.229], [3.0 + 1 / 12, 8.0 + 1.625 / 12], [], None),
    "SF1": ("SF", None, 2, SF_L1_HORIZ, [SF_L1_HORIZ[1]], None),
    "SF3": ("SF", None, [5.0625, 4.9583, 4.9583, 4.9583, 5.0625], SF_L1_HORIZ, [SF_L1_HORIZ[1]], None),
    "SF2": ("SF", 33.70, [3.25, 3.8333, 3.8333, 3.9167], [8.0 + 1 / 12], [], None),
    "SF6": ("SF", None, 5, SF_L2_HORIZ, SF_L2_HORIZ, None),
    "SF4": ("SF", None, [5.0208, 4.9583, 5.0208], SF_L2_HORIZ, SF_L2_HORIZ, None),
    "SF7": ("SF", None, [4.5, 4.4167, 4.5], SF_L2_HORIZ, SF_L2_HORIZ, None),
    "SF5B": ("SF", None, [5.5, 5.4167, 5.4167, 5.5], SF_L2_HORIZ, SF_L2_HORIZ, None),
    "SF5A": ("SF", None, 1, [L2_FF + 8.0 + 1 / 12, SF_L2_HORIZ[0]], [], None),
}
HM_DOORS = [  # (name, normal, finish-face coordinate, a0, a1, z0, z1): sizes A800 (W); positions from plan tags (INT)
    ("110B", "W", -EW2, 64.8, 67.8, 0.0, 7.0), ("102", "W", GX["1.2'"] - EW1, 49.8, 53.8, 0.0, 7.0),
    ("104", "W", GX["1.2'"] - EW1, 19.8, 22.8, 0.0, 7.0), ("210B", "S", GY["F'"] - EW2, 21.8, 24.8, L2_FF, L2_FF + 7.0)]
YARD_DOOR_LEAVES = [("001A", -10.43, -6.43, 63.60, 63.78), ("001B", -14.25, -11.25, 25.43, 25.61)]


def _set(bsdf, names, value):
    for nm in names:
        if nm in bsdf.inputs:
            bsdf.inputs[nm].default_value = value
            return


def principled(name, color, rough=0.5, metallic=0.0, transmission=0.0, note=""):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    mat.diffuse_color = (*color, 1.0)
    b = mat.node_tree.nodes.get("Principled BSDF")
    _set(b, ["Base Color"], (*color, 1.0))
    _set(b, ["Roughness"], rough)
    _set(b, ["Metallic"], metallic)
    if transmission:
        _set(b, ["Transmission Weight", "Transmission"], transmission)
        _set(b, ["IOR"], 1.5)
    mat["note"] = note
    return mat


def brick_material(name, c1, c2, mortar, note):
    """Procedural brick at the documented utility module: 12" x 4" coursing incl. 3/8" joint."""
    mat = principled(name, c1, 0.8, note=note)
    nt = mat.node_tree
    b = nt.nodes.get("Principled BSDF")

    def math(op, v0=None, v1=None):
        node = nt.nodes.new("ShaderNodeMath")
        node.operation = op
        if v0 is not None:
            node.inputs[0].default_value = v0
        if v1 is not None:
            node.inputs[1].default_value = v1
        return node

    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    nsep = nt.nodes.new("ShaderNodeSeparateXYZ")
    ab = math("ABSOLUTE")
    gt = math("GREATER_THAN", v1=0.5)
    inv = math("SUBTRACT", v0=1.0)
    mx = math("MULTIPLY")
    my = math("MULTIPLY")
    add = math("ADD")
    hinv = math("SUBTRACT", v0=1.0)
    comb = nt.nodes.new("ShaderNodeCombineXYZ")
    brick = nt.nodes.new("ShaderNodeTexBrick")
    brick.offset, brick.offset_frequency, brick.squash = 0.5, 2, 1.0
    for key, val in (("Color1", (*c1, 1)), ("Color2", (*c2, 1)), ("Mortar", (*mortar, 1))):
        brick.inputs[key].default_value = val
    brick.inputs["Scale"].default_value = 1.0
    brick.inputs["Mortar Size"].default_value = 0.375 / 12 * FT
    brick.inputs["Brick Width"].default_value = 1.0 * FT          # 11 5/8" + 3/8"
    brick.inputs["Row Height"].default_value = (4.0 / 12) * FT    # 3 5/8" + 3/8"
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.25
    link = nt.links.new
    link(tc.outputs["Object"], sep.inputs[0])
    link(geo.outputs["Normal"], nsep.inputs[0])
    link(nsep.outputs["X"], ab.inputs[0])
    link(ab.outputs[0], gt.inputs[0])
    link(gt.outputs[0], inv.inputs[1])
    link(sep.outputs["X"], mx.inputs[0])
    link(inv.outputs[0], mx.inputs[1])            # north/south faces run along X
    link(sep.outputs["Y"], my.inputs[0])
    link(gt.outputs[0], my.inputs[1])             # east/west faces run along Y
    link(mx.outputs[0], add.inputs[0])
    link(my.outputs[0], add.inputs[1])
    link(add.outputs[0], comb.inputs["X"])
    link(sep.outputs["Z"], comb.inputs["Y"])
    link(comb.outputs[0], brick.inputs["Vector"])
    link(brick.outputs["Color"], b.inputs["Base Color"])
    link(brick.outputs["Fac"], hinv.inputs[1])
    link(hinv.outputs[0], bump.inputs["Height"])
    link(bump.outputs[0], b.inputs["Normal"])
    return mat


def make_materials():
    bone, black = (0.78, 0.76, 0.70), (0.02, 0.02, 0.022)
    approx = "colour is an APPROXIMATION of the named finish - calibrate to a sample"
    M = {
        "BRK": brick_material("BRK-1_Endicott_Manganese_Ironspot_utility", (0.060, 0.052, 0.050),
                              (0.095, 0.082, 0.078), (0.025, 0.025, 0.025),
                              "A300 legend; spec 042000: Endicott utility, Holcim Ultra Dark mortar, running bond, "
                              "joints tooled slightly concave, grade SW type FBX. " + approx),
        "BC": principled("BC-1_BC-2_brick_cap_match_BRK-1", (0.075, 0.066, 0.063), 0.8, note="A300 legend: match BRK-1"),
        "ACM1": principled("ACM-1_Alucobond_Bone_White_dry_reveal", bone, 0.35, note="A300 legend. " + approx),
        "ACM2": principled("ACM-2_Alucobond_Tri-Corn_Black_dry_reveal", black, 0.35, note="A300 legend. " + approx),
        "ACM3": principled("ACM-3_Alucobond_Tri-Corn_Black_wet_seal", black, 0.35, note="A300 legend / A701. " + approx),
        "ACM4": principled("ACM-4_Alucobond_Bone_White_wet_seal", bone, 0.35, note="A300 legend / A701. " + approx),
        "MTL1": principled("MTL-1_metal_coping_match_ACM-2", black, 0.35, note="A300 legend; manufacturer blank"),
        "MTL2": principled("MTL-2_alum_coping_match_ACM-1", bone, 0.35, note="A300 legend"),
        "MTL3": principled("MTL-3_alum_coping_match_ACM-2", black, 0.35, note="A300 legend"),
        "GLASS": principled("GLASS_G1_G2_Viracon_VZE1-42_vision", (0.015, 0.022, 0.026), 0.03,
                            note="A811/A815 glazing schedule; shown dark-reflective because no interior is modeled"),
        "G3": principled("GLASS_G3_Viracon_V953_Medium_Gray_spandrel", (0.16, 0.16, 0.165), 0.06, note="A815. " + approx),
        "FRAME": principled("FRAME_YKK_Beachstone_Gray_painted_fluoropolymer", (0.42, 0.40, 0.37), 0.35,
                            note="A811/A815: Beachstone Gray. Spec 084113/084413: painted 3-coat fluoropolymer, "
                                 "match architect's sample -> non-metallic paint. " + approx),
        "TPO": principled("TPO_white_roof_membrane", (0.80, 0.80, 0.80), 0.6, note="A132 notes + spec 075423: white TPO (mechanically fastened per spec); A003 EW8"),
        "CLEAR": principled("GLASS_clear_laminated_1in", (1.0, 1.0, 1.0), 0.0, transmission=1.0,
                            note="A700 + spec 088000 GL-4: 1in laminated fully tempered clear canopy glazing"),
        "RAIL": principled("GLASS_GR-1_Viva_view_glass_railing", (1.0, 1.0, 1.0), 0.0, transmission=1.0,
                           note="A300 legend GR-1; spec 057313: Viva VIEW, laminated tempered clear glass, no top rail"),
        "SUNSHADE": principled("PAINT_match_ACM-1_sunshade_steel", bone, 0.45,
                               note="A702: painted to match ACM-1. " + approx),
    }
    grey = (0.5, 0.5, 0.5)
    for key, nm, note in (("U_STEEL", "UNRES_canopy_steel_paint_COLOR_TBD", "A700: painted, color TBD; spec 099113: colour as selected by Architect"),
                          ("U_CMU", "UNRES_painted_CMU_COLOR_TBD", "A012: color TBD; spec 099113: S-W latex on block filler, colour and sheen by Architect"),
                          ("U_HM", "UNRES_HM_door_paint", "A800 HM EXT; spec 081113 factory primed, 099113 field painted, colour by Architect"),
                          ("U_PAR_IN", "UNRES_terrace_parapet_inner", "A003 EW9 metal panel, finish not tagged")):
        M[key] = principled(nm, grey, 0.7, note="PLACEHOLDER - " + note)
    M["U_STRIP"] = principled("UNRES_building_base_strip_north", (0.5, 0.5, 0.5), 0.7,
                              note="PLACEHOLDER - CS-101 shows an unlabelled hatched strip against the building; material not given")
    M["U_BEDFILL"] = principled("SITE_entrance_bed_mulch", (0.13, 0.09, 0.06), 0.95, note="bed ground; mulch type not given on LP-101")
    M["U_TERRACE"] = paver_material("UNRES-colour_terrace_pavers_24in_concrete_pedestal_set")
    return M


def paver_material(name):
    """Spec 071413 2.6: plaza-deck pavers 24 in. square x 2 in., pedestal set; colour by Architect (UNRESOLVED).
    Neutral placeholder colour with a 24 in. stacked joint grid (layout pattern is an interpretation)."""
    mat = principled(name, (0.5, 0.5, 0.5), 0.7,
                     note="PLACEHOLDER COLOUR - spec 071413 2.6: 24x24x2 concrete pavers on pedestals, colour as selected by Architect")
    nt = mat.node_tree
    b = nt.nodes.get("Principled BSDF")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    grid = nt.nodes.new("ShaderNodeTexBrick")
    grid.offset, grid.offset_frequency, grid.squash = 0.0, 2, 1.0
    for key, val in (("Color1", (0.5, 0.5, 0.5, 1)), ("Color2", (0.5, 0.5, 0.5, 1)), ("Mortar", (0.12, 0.12, 0.12, 1))):
        grid.inputs[key].default_value = val
    grid.inputs["Scale"].default_value = 1.0
    grid.inputs["Mortar Size"].default_value = (0.1875 / 12) * FT
    grid.inputs["Brick Width"].default_value = 2.0 * FT
    grid.inputs["Row Height"].default_value = 2.0 * FT
    nt.links.new(tc.outputs["Object"], grid.inputs["Vector"])
    nt.links.new(grid.outputs["Color"], b.inputs["Base Color"])
    return mat


def assign(obj, mats, chooser):
    """Replace material slots and pick one per face. Vertices are never touched."""
    obj.data.materials.clear()
    for mt in mats:
        obj.data.materials.append(mt)
    index = {mt.name: i for i, mt in enumerate(mats)}
    for poly in obj.data.polygons:
        c = [v / FT for v in poly.center]
        poly.material_index = index[chooser(c, poly.normal).name]


def mass_chooser(name, M):
    def choose(c, n):
        x, y, z = c
        if n.z > 0.9:
            if abs(z - ROOF_STRUCT) < 0.05 or abs(z - CLOSET["z1"]) < 0.05:
                return M["TPO"]
            if abs(z - TERRACE_FF) < 0.05:
                return M["U_TERRACE"]
        if name in ("L2_LowRoof", "L2_LobbyBlock", "L2_Terrace_closet"):
            return M["ACM1"]
        if name == "L2_HighBlock":
            if x > 94.3 and y > 104.0 and not (n.x > 0.5 and x < 95.1):
                return M["ACM1"]                                   # CW2 bay
            return M["BRK"]
        # Level 1 podium
        if 82.2 < x < 94.8 and 1.0 < y < 2.3 and abs(n.y) > 0.5:
            return M["ACM2"]                                       # south recess back wall
        if x > 147.5 and y < 2.3 and not (n.x > 0.5 and x < 148.6):
            return M["ACM2"]                                       # J' south-east face and CW5 reveals
        if x > 203.0 and y < 22.3:
            return M["ACM2"]                                       # 11' face and CW6 reveals
        if 94.3 < x < 145.0 and y > 98.7 and not (n.x > 0.5 and x < 95.1 and y > 104.0):
            return M["ACM1"]                                       # lobby piers, recess, CW2 bay, east return
        return M["BRK"]
    return choose


def parapet_chooser(obj, M):
    zone = obj.name.split("_")[1]
    i = obj["edge"]
    inward = (obj["inward_x"], obj["inward_y"])
    if zone == "Terrace":
        acm2 = abs(P1_OFFSET[i] - EW5) < 1e-6
        outer, cope, inner = (M["ACM2"], M["MTL3"], M["U_PAR_IN"]) if acm2 else (M["BRK"], M["MTL1"], M["U_PAR_IN"])
    elif zone == "HighBlock" and i != 2:
        outer, cope, inner = M["BRK"], M["MTL1"], M["TPO"]
    else:
        outer, cope, inner = M["ACM1"], M["MTL2"], M["TPO"]

    def choose(c, n):
        if n.z > 0.9:
            return cope
        if n.x * inward[0] + n.y * inward[1] > 0.5:
            return inner
        return outer
    return [outer, cope, inner], choose


def yard_chooser(obj, M):
    nm = obj.name
    if "Gen_" in nm:
        def choose(c, n):
            if n.z > 0.9:
                return M["MTL1"]
            if abs(n.z) < 0.5 and (n.x * (-8.0 - c[0]) + n.y * (44.6 - c[1])) > 0.0:
                return M["U_CMU"]                                  # faces looking into the enclosure
            return M["BRK"]
        return [M["BRK"], M["MTL1"], M["U_CMU"]], choose
    if "Low_wall" in nm:
        def choose(c, n):
            if n.z > 0.9:
                return M["BC"]
            return M["U_CMU"] if (n.x + n.y) > 0.3 else M["BRK"]   # brick on the street (south-west) side: INT
        return [M["BRK"], M["BC"], M["U_CMU"]], choose
    return [M["BRK"], M["BC"]], (lambda c, n: M["BC"] if n.z > 0.9 else M["BRK"])


def face_box(name, normal, surf, a0, a1, z0, z1, proj, col, mat, source):
    if normal == "N":
        return box(name, a0, a1, surf, surf + proj, z0, z1, col, mat, source)
    if normal == "S":
        return box(name, a0, a1, surf - proj, surf, z0, z1, col, mat, source)
    if normal == "E":
        return box(name, surf, surf + proj, a0, a1, z0, z1, col, mat, source)
    return box(name, surf - proj, surf, a0, a1, z0, z1, col, mat, source)


def facade_detail(col, M):
    count = 0
    for i, (normal, plane, a0, a1, z0, z1, buildup, tag) in enumerate(OPENINGS):
        key = "Door" if tag.startswith("Door") else tag.split()[0]
        system, start, bays, horiz, caps, spandrel = LAYOUT[key]
        surf = plane - GLASS_SETBACK + 0.05 if normal in "NE" else plane + GLASS_SETBACK - 0.05
        fw = (2.0 if system == "SF" else 2.5) / 12
        vw, vproj = (fw, 0.12) if system == "SF" else (0.75 / 12, 0.012)   # CW verticals: 2-sided SSG joint
        src = f"{tag}: A811/A815/A816 layout (W); cap projection and SSG joint width INT"
        pre = f"FD_{i:02d}_{key}"
        sill_h = 4.0 / 12 if system == "CW" and z0 < 0.01 else fw
        for nm, b0, b1, c0, c1 in (("sill", a0, a1, z0, z0 + sill_h), ("head", a0, a1, z1 - fw, z1),
                                   ("jambA", a0, a0 + fw, z0, z1), ("jambB", a1 - fw, a1, z0, z1)):
            face_box(f"{pre}_{nm}", normal, surf, b0, b1, c0, c1, 0.12, col, M["FRAME"], src)
            count += 1
        if isinstance(bays, int):
            lines = [a0 + (a1 - a0) * k / bays for k in range(1, bays)]
        else:
            origin, lines, run = (a0 if start is None else start), [], 0.0
            for wdt in bays[:-1]:
                run += wdt
                lines.append(origin + run)
        for k, v in enumerate(lines):
            if a0 + fw < v < a1 - fw:
                face_box(f"{pre}_v{k:02d}", normal, surf, v - vw / 2, v + vw / 2, z0, z1, vproj, col, M["FRAME"], src)
                count += 1
        for k, h in enumerate(horiz):
            if z0 + fw < h < z1 - fw:
                deep = any(abs(h - cz) < 0.01 for cz in caps)
                hh = 4.0 / 12 if deep else fw
                face_box(f"{pre}_h{k:02d}" + ("_cap4x10" if deep else ""), normal, surf, a0, a1,
                         h - hh / 2, h + hh / 2, 8.0 / 12 if deep else 0.12, col, M["FRAME"], src)
                count += 1
        if spandrel:
            s0, s1 = max(spandrel[0], z0), min(spandrel[1], z1)
            if s1 - s0 > 0.1:
                face_box(f"{pre}_G3_spandrel", normal, surf, a0, a1, s0, s1, 0.015, col, M["G3"], "A815 G3 band (W)")
                count += 1
    # solid door bay in CW3: architectural metal panel (A815) -> ACM-4 (INT)
    yf = GY["A.1'"] + EW2
    top = DOOR_HEAD + 2.0 + 2.75 / 12
    for nm, b0, b1, c0, c1 in (("west", DOOR_BAY[0], DOOR_BAY[0] + DOOR_JAMB_WEST, 0.0, top),
                               ("east", DOOR_BAY[1] - DOOR_JAMB_EAST, DOOR_BAY[1], 0.0, top),
                               ("head", DOOR_BAY[0] + DOOR_JAMB_WEST, DOOR_BAY[1] - DOOR_JAMB_EAST, DOOR_HEAD, top)):
        face_box(f"FD_CW3_doorbay_panel_{nm}", "N", yf, b0, b1, c0, c1, 0.02, col, M["ACM4"],
                 "A815 architectural metal panel; ACM-4 per A300 tag (INT)")
        count += 1
    for nm, normal, surf, b0, b1, c0, c1 in HM_DOORS:
        face_box(f"FD_HM_door_{nm}", normal, surf, b0, b1, c0, c1, 0.08, col, M["U_HM"],
                 "A800 size (W); position from plan tag +/-1 ft (INT)")
        count += 1
    for nm, b0, b1, y0, y1 in YARD_DOOR_LEAVES:
        box(f"FD_HM_door_{nm}", b0, b1, y0, y1, 0.0, 7.0, col, M["U_HM"], "A800 size (W); 7'-0\" head")
        count += 1
    return count


def apply_materials(cols, masses, M):
    c_par, c_open, c_can, c_small, c_ss, c_rail, c_yard = cols
    for mass in masses:
        assign(mass, [M["BRK"], M["ACM1"], M["ACM2"], M["TPO"], M["U_TERRACE"]], mass_chooser(mass.name, M))
    for obj in c_par.objects:
        mats, choose = parapet_chooser(obj, M)
        assign(obj, mats, choose)
    for obj in c_open.objects:
        assign(obj, [M["GLASS"]], lambda c, n: M["GLASS"])
    for obj in c_can.objects:
        mt = M["CLEAR"] if "glass" in obj.name else M["U_STEEL"]
        assign(obj, [mt], lambda c, n, mt=mt: mt)
    for obj in c_small.objects:
        mt = M["ACM3"] if obj.name.endswith("East") else M["ACM4"]
        assign(obj, [mt], lambda c, n, mt=mt: mt)
    for obj in c_ss.objects:
        assign(obj, [M["SUNSHADE"]], lambda c, n: M["SUNSHADE"])
    for obj in c_rail.objects:
        assign(obj, [M["RAIL"]], lambda c, n: M["RAIL"])
    for obj in c_yard.objects:
        mats, choose = yard_chooser(obj, M)
        assign(obj, mats, choose)


# ===================== v006 SITE AND GRADING (building code above is unchanged) =====================
# Z values are feet relative to Building II FFE 660.30 (CG-101). Positions are in the building
# coordinate system; civil sheets registered +/-0.5 ft (notes/site_control_v006.md).
FFE = 660.30
SKIRT_BOTTOM = -8.0

# (x, y, elevation, code, note)  W = written on CG-101, V = read visually, C = contour label position
SITE_SPOTS = [
    (60.7, 105.6, 659.80, "W", "north walk"), (-0.4, 105.4, 659.40, "W", "NW corner"),
    (69.9, 109.6, 660.08, "W", "north walk"), (140.1, 107.5, 660.27, "W", "entry plaza"),
    (145.2, 99.2, 660.09, "W", "lobby east return"), (205.9, 98.9, 659.79, "W", "NE corner"),
    (-5.4, 106.4, 659.31, "W", "NW walk"), (-17.3, 110.2, 659.09, "W", "NW walk"),
    (-16.9, 99.1, 659.59, "W", "NW walk"), (-12.7, 91.9, 659.80, "W", "NW walk"),
    (-27.6, 82.5, 655.32, "W", "west of transformer"), (-29.3, 92.4, 655.53, "W", "BW"),
    (-23.6, 58.5, 656.28, "W", "BW"), (-22.1, 68.6, 655.60, "W", "BS west stair"),
    (-20.8, 18.7, 656.98, "W", "BW"), (1.4, -5.2, 656.44, "W", "BW"),
    (88.4, 1.4, 657.49, "W", "south face"), (149.7, 1.4, 658.47, "W", "south face"),
    (202.5, 1.0, 658.50, "W", "SE corner"),
    (13.5, -2.2, 656.88, "W", "BS south-west stair"),
    (-17.0, 120.0, 658.81, "V", "EX"), (6.9, 118.7, 658.70, "V", "EX"), (61.7, 116.3, 659.80, "V", "EX"),
    (79.3, 114.3, 660.14, "V", "EX flush curb"), (105.2, 114.3, 660.14, "V", "EX flush curb"),
    (142.3, 114.3, 660.14, "V", "EX flush curb"), (161.5, 116.3, 659.77, "V", "EX"),
    (208.2, 102.5, 659.72, "V", "EX"), (218.8, 14.3, 660.04, "V", "EX plaza"),
    (-28.9, 59.2, 655.47, "V", "EX"), (13.4, -13.1, 656.37, "V", "EX"),
    (-63.4, 103.8, 654.60, "V", "EX west street"), (-63.4, 97.0, 655.11, "V", "EX west street"),
    (-63.4, 76.0, 654.86, "V", "EX west street"), (-63.4, 61.7, 654.92, "V", "EX west street"),
    (-29, 151, 655.0, "C", ""), (-47, 100, 655.0, "C", ""), (-26, 146, 656.0, "C", ""), (-69, 8, 656.0, "C", ""),
    (-23, 142, 657.0, "C", ""), (48, -3, 657.0, "C", ""), (-20, 137, 658.0, "C", ""), (163, -6, 658.0, "C", ""),
    (69, 185, 658.0, "C", ""), (148, 204, 658.0, "C", ""), (193, 202, 658.0, "C", ""),
    (6, 113, 659.0, "C", ""), (64, 138, 659.0, "C", ""), (239, 115, 660.0, "C", ""), (254, 155, 660.0, "C", ""),
    (287, 163, 661.0, "C", ""), (287, 119, 661.0, "C", ""),
]
CURB_H = 0.5                     # W: 6" high curb (CX-101)
# asphalt edge points 6" below the walk where the curb is NOT flush (INT)
for _x, _z in ((-15, 658.81), (7, 658.70), (30, 659.20), (52, 659.70), (165, 659.77), (185, 659.72)):
    SITE_SPOTS.append((_x, 126.5, _z - CURB_H, "I", "asphalt at curb"))

# hardscape slabs: name, material key, [(x, y, elevation), ...]
HARDSCAPE = [
    ("Walk_north_west", "LINEA", [(-17, 116.6, 658.81), (6.9, 116.6, 658.70), (56.8, 116.6, 659.78),
                                  (56.8, 123.4, 659.78), (6.9, 123.4, 658.70), (-17, 123.4, 658.81)]),
    ("Walk_north_transition_west", "LINEA", [(56.8, 116.6, 659.78), (62.0, 115.7, 659.80), (78.5, 115.7, 660.14),
                                             (56.8, 123.4, 659.78)]),
    ("Dropoff_band_west", "LINEA", [(62.0, 106.3, 659.80), (108.3, 106.3, 660.25), (108.3, 115.7, 660.14),
                                    (78.5, 115.7, 660.14), (62.0, 115.7, 659.80)]),
    ("Entry_plaza", "WESTMOUNT", [(108.3, 103.45, 660.30), (140.8, 103.45, 660.30), (140.8, 115.7, 660.14),
                                  (108.3, 115.7, 660.14)]),
    ("Dropoff_band_east", "LINEA", [(140.8, 106.3, 660.27), (160.0, 116.6, 659.77), (160.0, 123.4, 659.77),
                                    (140.8, 115.7, 660.14)]),
    ("Walk_north_east", "LINEA", [(160.0, 116.6, 659.77), (189.6, 116.6, 659.72), (189.6, 123.4, 659.72),
                                  (160.0, 123.4, 659.77)]),
    ("Walk_to_BuildingI_plaza", "LINEA", [(189.6, 116.6, 659.72), (226.0, 85.5, 659.85), (233.0, 89.0, 659.85),
                                          (189.6, 123.4, 659.72)]),
    ("Walk_west", "LINEA", [(-10.6, 72.7, 660.10), (-4.9, 72.7, 660.10), (-4.9, 91.9, 659.80), (-4.9, 99.1, 659.59),
                            (-4.9, 116.6, 658.85), (-17.0, 116.6, 658.81), (-17.0, 106.0, 659.20),
                            (-10.6, 99.1, 659.59), (-10.6, 91.9, 659.80)]),
    ("Landing_door_110B", "CONC", [(-12.7, 64.5, 660.10), (-0.6, 64.5, 660.18), (-0.6, 72.7, 660.18), (-12.7, 72.7, 660.10)]),
    ("Landing_west_stair_bottom", "CONC", [(-28.0, 64.5, 655.60), (-21.7, 64.5, 655.60), (-21.7, 72.7, 655.60),
                                           (-28.0, 72.7, 655.60)]),
    ("Transformer_pad", "CONC", [(-25.1, 74.1, 655.32), (-11.9, 74.1, 655.32), (-11.9, 90.6, 655.32), (-25.1, 90.6, 655.32)]),  # v007
    ("Generator_yard_slab", "CONC", [(-18.8, 26.24, 659.90), (4.24, 26.24, 659.90), (4.24, 57.0, 660.15),
                                     (-0.6, 57.0, 660.15), (-0.6, 62.98, 660.18), (-18.8, 62.98, 660.18)]),
    ("Walk_southwest", "CONC", [(-1.0, -0.8, 660.19), (4.2, -0.8, 660.19), (4.2, 24.8, 660.30), (-1.0, 24.8, 660.30)]),
    ("Landing_sw_stair_top", "CONC", [(-1.0, -3.7, 660.19), (5.6, -3.7, 660.19), (5.6, -0.8, 660.19), (-1.0, -0.8, 660.19)]),
    ("Walk_east_door_100B", "LINEA", [(205.8, 32.8, 660.30), (218.75, 32.8, 660.04), (218.75, 38.0, 660.04), (205.8, 38.0, 660.30)]),
    ("Walk_east_door_100C", "LINEA", [(203.4, 10.8, 660.30), (218.75, 10.8, 660.04), (218.75, 17.7, 660.04), (203.4, 17.7, 660.30)]),
    ("Existing_plaza_between_buildings", "EXPLAZA", [(218.75, -13.3, 660.04), (248.3, -13.3, 660.04), (248.3, 42.2, 660.04),
                                                     (218.75, 42.2, 660.04)]),
]
# stairs: name, x_top, x_bottom, y0, y1, top elevation, bottom elevation, risers
STAIRS = [("Stair_west_9_risers", -12.7, -21.7, 64.5, 72.7, 660.10, 655.60, 9),          # W: (8) 12" treads, (9) 6" risers
          ("Stair_southwest_7_risers_ASSUMED", 5.6, 12.6, -3.7, -0.8, 660.19, 656.88, 7)]  # W: TS/BS; riser count A
ISLANDS = [(24.6, 63.7), (86.3, 124.5), (147.1, 185.3)]      # x ranges; y 146.9 -> 158.3 (M, CS-101)
ISLAND_Y = (146.9, 158.3)
ASPHALT_REGION = [(-20, 123.4), (56.8, 123.4), (78.5, 115.7), (142.7, 115.7), (160, 123.4), (196, 123.4),
                  (236, 92), (262, 92), (262, 205), (-20, 205)]
BED_REGIONS = [[(-4.9, 106.2), (62.0, 106.2), (62.0, 115.7), (56.8, 116.6), (-4.9, 116.6)],
               [(145.2, 99.3), (205.0, 99.3), (205.0, 112.0), (189.6, 116.6), (160.0, 116.6), (145.2, 108.5)],
               [(-4.9, 74.0), (-1.0, 74.0), (-1.0, 105.0), (-4.9, 105.0)]]
TERRAIN_X, TERRAIN_Y, TERRAIN_CELL = (-70.0, 262.0), (-24.0, 205.0), 4.0
# v009: documented entrance edges (CS-101 rev 6 vector samples)
V009_OUTER = [(61.6, 123.4), (63.9, 123.1), (66.1, 122.2), (68.0, 120.9), (69.5, 119.1), (71.2, 117.1), (73.3, 115.6),
              (75.7, 114.7), (78.3, 114.4)]
V009_INNER = [(62.0, 116.6), (63.7, 115.2), (66.5, 111.9), (70.0, 109.4), (74.0, 107.9), (78.3, 107.4)]
V009_SLABS = [
    ("Walk_entrance_curve_west", "LINEA", [(56.8, 116.6)] + V009_INNER + [(78.3, 114.4)] + V009_OUTER[-2::-1] + [(56.8, 123.4)]),
    ("Dropoff_band_west", "LINEA", [(78.3, 107.4), (80.1, 107.35), (80.1, 106.3), (88.3, 106.3), (88.3, 107.35), (108.3, 107.35),
                                    (108.3, 115.7), (78.3, 115.7), (78.3, 114.4)]),
    ("Entrance_bed_fill_west", "BED", [(62.0, 106.3), (80.1, 106.3), (80.1, 107.35)] + V009_INNER[::-1] + [(62.0, 115.7)]),
    ("Building_base_strip_UNRES", "STRIP", [(88.3, 106.3), (108.3, 106.3), (108.3, 107.35), (88.3, 107.35)]),
]
TERRAIN_BASE = -10.0            # flat underside so the terrain reads as a solid block at its cut edges
# slabs on retained fill (yard, pad, landings): carried down so no void shows where the outside grade is lower
DEEP_SLABS = {"Transformer_pad", "Generator_yard_slab", "Landing_door_110B", "Walk_southwest", "Landing_sw_stair_top", "Walk_west"}


def _inside(pt, poly):
    x, y = pt
    hit = False
    for i in range(len(poly)):
        (x0, y0), (x1, y1) = poly[i][:2], poly[(i + 1) % len(poly)][:2]
        if (y0 > y) != (y1 > y) and x < (x1 - x0) * (y - y0) / (y1 - y0) + x0:
            hit = not hit
    return hit


def _idw(x, y, pts):
    num = den = 0.0
    for px, py, pz in pts:
        w = 1.0 / ((x - px) ** 2 + (y - py) ** 2 + 4.0) ** 1.5
        num += w * pz
        den += w
    return num / den


def build_site(col, M, p1_finish):
    S = {"ASPHALT": principled("SITE_existing_asphalt", (0.05, 0.05, 0.055), 0.9, note="existing parking / drive; representational"),
         "LAWN": principled("SITE_lawn_ground_shape_no_planting", (0.20, 0.26, 0.14), 0.95, note="representational; no planting modeled"),
         "BED": principled("SITE_landscape_bed_ground_shape", (0.16, 0.12, 0.09), 0.95, note="CS-101 bed outlines as ground shapes only"),
         "LINEA": principled("SITE_pavers_Techo-Bloc_Linea_Shale_Gray", (0.42, 0.42, 0.41), 0.8,
                             note="CS-101 note: pathways Techo-Bloc Linea, Shale Gray - colour approximates the name"),
         "WESTMOUNT": principled("SITE_plaza_Techo-Bloc_Westmount_Onyx", (0.07, 0.07, 0.075), 0.8,
                                 note="CS-101 note: plaza Techo-Bloc Westmount, Onyx - colour approximates the name"),
         "CONC": principled("SITE_concrete_flatwork", (0.55, 0.55, 0.53), 0.85, note="CG-101 concrete hatch; representational"),
         "EXPLAZA": principled("SITE_existing_plaza_not_detailed", (0.5, 0.5, 0.5), 0.85, note="existing plaza between buildings; placeholder")}
    count = 0
    ctrl = [(x, y, e - FFE) for x, y, e, *_ in SITE_SPOTS]
    for hname, _, verts in HARDSCAPE:
        # v007: interpolation control set kept EXACTLY as v006 (pad corners still enter at 659.94) so the
        # terrain outside the enclosure is unchanged; only the interior is lowered explicitly below
        ctrl += [(x, y, (659.94 if hname == "Transformer_pad" else e) - FFE) for x, y, e in verts]

    # ---- hardscape slabs: top at the documented elevations, 0.6 ft thick ----
    hard_polys = []
    for name, key, verts in HARDSCAPE:
        poly = ccw([(x, y) for x, y, _ in verts])
        zmap = {(x, y): e - FFE for x, y, e in verts}
        n = len(poly)
        pts = [(x, y, SKIRT_BOTTOM if name in DEEP_SLABS else zmap[(x, y)] - 0.6) for x, y in poly] + [(x, y, zmap[(x, y)]) for x, y in poly]
        faces = [tuple(reversed(range(n))), tuple(range(n, 2 * n))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
        obj = mesh_object("Site_" + name, pts, faces, col, S[key], "CS-101 outline (M); CG-101 elevations (W/V), linear between spots (INT)")
        bm = bmesh.new(); bm.from_mesh(obj.data)
        bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) > 4])
        bm.to_mesh(obj.data); bm.free()
        hard_polys.append(poly)
        count += 1

    # ---- v009: entrance walk west of door 100A re-shaped to the documented edges ----
    for old in ("Site_Walk_north_transition_west", "Site_Dropoff_band_west"):
        bpy.data.objects.remove(bpy.data.objects[old], do_unlink=True)
    for name, key, poly in V009_SLABS:
        poly = ccw(poly)
        n = len(poly)
        tops = [_idw(x, y, ctrl) for x, y in poly]
        pts = [(x, y, z - 0.6) for (x, y), z in zip(poly, tops)] + [(x, y, z) for (x, y), z in zip(poly, tops)]
        faces = [tuple(reversed(range(n))), tuple(range(n, 2 * n))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
        mat9 = M["U_STRIP"] if key == "STRIP" else (M["U_BEDFILL"] if key == "BED" else S[key])
        obj = mesh_object("Site_" + name, pts, faces, col, mat9, "CS-101 rev 6 + LP-101 edges (M, agree within 0.5 ft); R10.50 ft and 8.50 ft written; top from the v007 interpolation")
        bm = bmesh.new(); bm.from_mesh(obj.data)
        bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) > 4])
        bm.to_mesh(obj.data); bm.free()
    count += len(V009_SLABS) - 2

    # ---- stairs ----
    for name, xt, xb, y0, y1, et, eb, risers in STAIRS:
        rise = (et - eb) / risers
        run = (xb - xt) / (risers - 1)
        for k in range(risers - 1):                     # treads between top landing and bottom
            xa, xb2 = xt + k * run, xt + (k + 1) * run
            ztop = et - FFE - (k + 1) * rise
            box(f"Site_{name}_tread{k + 1:02d}", min(xa, xb2), max(xa, xb2), y0, y1, eb - FFE - 0.6, ztop, col, S["CONC"],
                "CG-101 TS/BS and riser note")
            count += 1
        hard_polys.append(ccw([(xt, y0), (xb, y0), (xb, y1), (xt, y1)]))

    # ---- parking islands (6 in. above interpolated pavement) ----
    for k, (xa, xb2) in enumerate(ISLANDS, 1):
        zc = _idw((xa + xb2) / 2, sum(ISLAND_Y) / 2, ctrl)
        c = 4.0
        poly = [(xa + c, ISLAND_Y[0]), (xb2 - c, ISLAND_Y[0]), (xb2, ISLAND_Y[0] + c), (xb2, ISLAND_Y[1] - c),
                (xb2 - c, ISLAND_Y[1]), (xa + c, ISLAND_Y[1]), (xa, ISLAND_Y[1] - c), (xa, ISLAND_Y[0] + c)]
        prism(f"Site_Parking_island_{k}", poly, zc - 1.0, zc + CURB_H, col, S["BED"], "CS-101 outline (M); height A; surface INTERPOLATED")
        count += 1

    # ---- interpolated terrain grid ----
    nx = int((TERRAIN_X[1] - TERRAIN_X[0]) / TERRAIN_CELL) + 1
    ny = int((TERRAIN_Y[1] - TERRAIN_Y[0]) / TERRAIN_CELL) + 1
    verts, faces = [], []
    for j in range(ny):
        for i in range(nx):
            x, y = TERRAIN_X[0] + i * TERRAIN_CELL, TERRAIN_Y[0] + j * TERRAIN_CELL
            z = _idw(x, y, ctrl)
            if any(_inside((x, y), hp) for hp in hard_polys):
                z -= 0.45                                   # keep the ground just under the slabs
            verts.append((x, y, z))
    for j in range(ny - 1):
        for i in range(nx - 1):
            a = j * nx + i
            faces.append((a, a + 1, a + nx + 1, a + nx))
    # v007: enclosure interior at pad level; the four bounding grid lines are snapped into the wall thickness
    pad_z = 655.32 - FFE - 0.45
    for k, (x, y, z) in enumerate(verts):
        if -26.1 <= x <= -13.9 and 75.9 <= y <= 88.1:
            z = pad_z
        if 71.9 <= y <= 92.1:
            x = -11.6 if abs(x + 14.0) < 0.01 else (-10.95 if abs(x + 10.0) < 0.01 else x)
        if -26.1 <= x <= -9.9:
            y = {88.0: 90.95, 92.0: 91.6, 76.0: 73.75, 72.0: 73.1}.get(round(y, 2), y)
        verts[k] = (x, y, z)
    ring = ([i for i in range(nx)] + [j * nx + nx - 1 for j in range(1, ny)] +
            [(ny - 1) * nx + i for i in range(nx - 2, -1, -1)] + [j * nx for j in range(ny - 2, 0, -1)])
    base0 = len(verts)
    verts += [(verts[k][0], verts[k][1], TERRAIN_BASE) for k in ring]
    for k in range(len(ring)):
        k2 = (k + 1) % len(ring)
        faces.append((ring[k2], ring[k], base0 + k, base0 + k2))
    faces.append(tuple(base0 + k for k in range(len(ring))))
    terrain = mesh_object("Site_Terrain_INTERPOLATED", verts, faces, col, S["LAWN"],
                          "IDW through CG-101 spots and contour positions - INTERPOLATED, exact only at written spots")
    terrain.data.materials.append(S["ASPHALT"])
    terrain.data.materials.append(S["BED"])
    for poly in terrain.data.polygons:
        c = (poly.center.x / FT, poly.center.y / FT)
        if _inside(c, ASPHALT_REGION):
            poly.material_index = 1
        elif any(_inside(c, b) for b in BED_REGIONS):
            poly.material_index = 2
    for poly in terrain.data.polygons:
        poly.use_smooth = abs(poly.normal.z) > 0.5 and len(poly.vertices) == 4
    count += 1

    # ---- v007: retained fill on the inner (high) side of the south-west low site wall ----
    prism("Site_Retained_fill_southwest", [(-19.03, 17.75), (-1.0, -0.29), (-1.0, 24.8), (-19.03, 24.8)],
          SKIRT_BOTTOM, 659.71 - FFE, col, S["LAWN"],
          "A012 B2: low site wall retains grade just below Level 1; CG-101 TW 659.71 = high-side grade (W); flat top INT")
    count += 1

    # ---- foundation skirts so nothing floats where the real grade is below the v005 base ----
    prism("Site_Foundation_skirt_podium", p1_finish, SKIRT_BOTTOM, AVG_GRADE, col, M["BRK"],
          "A301/A302 show brick to grade; depth arbitrary (A); v005 podium untouched")
    count += 1
    for name, poly, top in YARD_WALLS:
        prism(f"Site_Foundation_skirt_{name}", ccw(poly), SKIRT_BOTTOM, AVG_GRADE, col, M["BRK"], "extends frozen v005 yard wall down to grade (A)")
        count += 1
    for cx in CANOPY["cols_x"]:
        pass                                               # canopy columns already reach below the entry plaza
    z = 0.4
    ax, ay = 236.0, 168.0
    mesh_object("Site_North_arrow", [(ax - 4, ay, z), (ax + 4, ay, z), (ax + 4, ay + 18, z), (ax + 9, ay + 18, z), (ax, ay + 30, z),
                                     (ax - 9, ay + 18, z), (ax - 4, ay + 18, z)], [(0, 1, 2, 3, 4, 5, 6)], col, M["ACM1"], "project north")
    globals()["LANDSCAPE_COUNTS"] = build_landscape(ctrl)          # v008
    return count + 1


# ===================== v008 LANDSCAPE (v007 building and site code above is unchanged) =====================
# Source: LP-101 "Landscape Plan - Building", Plant Schedule BLDG II (approved civil set, rev 1 11.06.25,
# City final approval 1/9/2026). Codes: W = written in the schedule/callouts, M = symbol position measured from
# the LP-101 vector linework (+/-0.7 ft registration), INT = interpreted. See notes/landscape_control_v008.md.
# species: code -> (category, installed height ft (W), proxy spread ft (INT), colour (INT, representational))
PLANTS = {
    "SANJ": ("tree", 8.0, 4.0, (0.10, 0.20, 0.08)),       # Osmanthus x fortunei 'San Jose', B&B 1.5" cal, 8' min
    "DAZA": ("shrub", 1.25, 2.4, (0.16, 0.30, 0.12)),     # Encore azalea 'Roblen', 7 gal, 15" min, 3' o.c.
    "RHCO": ("shrub", 1.25, 3.0, (0.22, 0.26, 0.12)),     # Encore azalea 'Conlea', 7 gal, 15" min, 5' o.c.
    "GATE": ("upright", 3.0, 3.0, (0.06, 0.16, 0.07)),    # Camellia japonica, 7 gal, 36" min
    "ILST": ("upright", 3.0, 2.5, (0.05, 0.13, 0.06)),    # Ilex crenata 'Steeds', 15 gal, 36" min
    "JEWL": ("shrub", 1.25, 2.4, (0.12, 0.28, 0.20)),     # Distylium 'Jewel Box', 3 gal, 15" min, 3' o.c.
    "JADE": ("shrub", 1.5, 3.2, (0.10, 0.25, 0.18)),      # Distylium 'Vintage Jade', 3 gal, 18" min, 4' o.c.
    "FOAR": ("shrub", 1.0, 4.0, (0.30, 0.38, 0.12)),      # Forsythia 'Arnold's Dwarf', 3 gal, 12" min, 7' o.c.
    "SEAS": ("cover", 0.5, 0.8, (0.45, 0.16, 0.25)),      # seasonal annuals, 6" pot, 12" o.c.
    "CARE": ("cover", 0.7, 1.2, (0.42, 0.45, 0.18)),      # Carex 'Evergold', 1 gal, 18" o.c.
    "COZA": ("cover", 0.8, 1.2, (0.40, 0.38, 0.10)),      # Coreopsis 'Zagreb', 1 gal, 18" o.c.
    "CORA": ("cover", 0.7, 1.6, (0.22, 0.08, 0.18)),      # Heuchera 'Electric Plum', 1 gal, 24" o.c.
    "JUNE": ("cover", 0.8, 1.7, (0.25, 0.36, 0.22)),      # Hosta 'June', 1 gal, 24" o.c.
    "CATM": ("cover", 0.9, 1.7, (0.32, 0.34, 0.42)),      # Nepeta 'Walker's Low', 1 gal, 24" o.c.
    "OSOR": ("cover", 1.2, 1.8, (0.30, 0.34, 0.20)),      # Rosa 'Oso Easy Italian Ice', 3 gal, 24" o.c.
}
# individually drawn symbols: positions M from LP-101 (RHCO positions INT: symbol centres could not be extracted)
POINT_PLANTS = {
    "DAZA": [(x, 107.85) for x in (3.5, 6.6, 10.35, 14.05, 17.75, 21.45, 25.15, 28.85)] +
            [(x, 108.55) for x in (37.3, 41.0, 44.7, 48.45, 52.15, 55.85, 59.55)] +
            [(x, 101.95) for x in (152.65, 156.15, 159.65, 163.15, 166.65, 170.15, 178.6, 182.25, 185.85, 189.5,
                                   193.15, 196.8, 200.45)],
    "ILST": [(-0.35, 107.6), (32.9, 107.6), (174.2, 101.95), (204.5, 101.95), (-3.0, 102.5), (-3.4, 73.5)],
    "GATE": [(63.5, 109.5), (148.3, 102.0)],
    "JEWL": [(-2.75, y) for y in (76.95, 79.95, 83.05, 86.05, 89.05, 92.15, 95.15, 98.15)],
    "JADE": [(x, -3.8) for x in (24.75, 28.8, 32.85, 36.85, 65.5, 69.55, 73.6, 77.6, 81.65, 96.7, 100.7, 104.75,
                                 108.75, 137.45, 141.5, 145.5, 149.55)],
    "FOAR": [(x, -3.5) for x in (155.4, 161.5, 167.5, 173.6, 179.6, 185.6, 191.7, 197.7)],
    "SANJ": [(88.9, -4.2)],
    "RHCO": [(x, -3.8) for x in (41.5, 46.5, 51.5, 56.5, 61.5, 113.5, 118.5, 123.5, 128.5, 133.5)],   # INT: 5' o.c. in the two gaps
    "OSOR": [(98.5, 107.0), (100.5, 107.0), (102.5, 107.0)] + [(166.5 + 2.0 * k, 104.6) for k in range(8)],  # INT rows, 24" o.c.
    "CORA": [(40.5 + 2.0 * k, -5.7) for k in range(12)] + [(112.5 + 2.0 * k, -5.7) for k in range(12)],      # INT: front row at the RHCO gaps
    "CATM": [(x0 + 2.0 * k, -5.7) for x0, n in ((22.5, 9), (64.5, 10), (94.5, 9), (136.5, 9)) for k in range(n)],  # INT: front row at JADE groups
}


def _v009_inner_y(x):              # documented inner walk edge (CS-101 rev 6), linear between sampled points
    pts = [(63.7, 115.2), (66.5, 111.9), (70.0, 109.4), (74.0, 107.9), (78.3, 107.4)]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return 116.6 if x < 63.7 else 107.35


def _arc_y(x):                      # INT: bed edge arc in the north-west bed, read from LP-101
    return 116.4 - 6.0 * (1.0 - ((x - 30.0) / 28.0) ** 2)


# groundcover masses: code, quantity (W), spacing ft (W), region test (INT)
MASS_PLANTS = [
    ("COZA", 27, 1.5, lambda x, y: -4.7 <= x <= 3.0 and 109.0 <= y <= 116.3),
    ("CARE", 17, 1.5, lambda x, y: 3.2 <= x <= 20.0 and _arc_y(x) + 0.5 <= y <= 116.2),
    ("CARE", 16, 1.5, lambda x, y: 42.0 <= x <= 57.5 and _arc_y(x) + 0.5 <= y <= 116.2),
    ("SEAS", 29, 1.0, lambda x, y: 62.6 <= x <= 77.8 and 106.8 <= y <= min(_v009_inner_y(x), 115.0) - 0.6 and (x - 63.5) ** 2 + (y - 109.5) ** 2 > 3.6),   # v009: inside the documented bed, clear of the camellia
    ("SEAS", 34, 1.0, lambda x, y: 141.5 <= x <= 151.0 and 103.6 <= y <= 108.0),
    ("CARE", 36, 1.5, lambda x, y: 146.0 <= x <= 164.0 and 104.0 <= y <= 111.5),
    ("JUNE", 28, 2.0, lambda x, y: 181.0 <= x <= 204.0 and 103.8 <= y <= 110.5 - 0.22 * (x - 181.0)),
]
# thin surface patches (INT outlines): name, kind, polygon
PATCHES = [
    ("Planter_bed_at_CW2_bay", "MULCH", [(96.0, 106.35), (105.0, 106.35), (105.0, 107.7), (96.0, 107.7)]),
    ("Lawn_northwest_bed", "LAWN", [(20.5, 116.2)] + [(20.5 + 2.15 * k, _arc_y(20.5 + 2.15 * k) + 0.4) for k in range(11)] + [(42.0, 116.2)]),
    ("Lawn_northeast_bed", "LAWN", [(164.5, 106.5), (180.5, 106.5), (188.5, 108.5), (188.5, 115.8), (164.5, 115.8)]),
    ("Bed_mulch_south_strip", "MULCH", [(20.0, -7.0), (204.0, -7.0), (204.0, -0.95), (20.0, -0.95)]),
    ("Bed_mulch_south_recess", "MULCH", [(83.4, -0.95), (93.7, -0.95), (93.7, 1.5), (83.4, 1.5)]),
    ("Bed_mulch_southeast", "MULCH", [(148.6, -0.95), (204.0, -0.95), (204.0, 1.5), (148.6, 1.5)]),
]


def _blob_mesh(name, kind):
    """Unit proxy mesh (1 ft wide, 1 ft tall, base at z=0), scaled per species."""
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.5)
    for v in bm.verts:
        v.co.z += 0.5
        if kind == "upright":
            taper = 1.0 - 0.45 * v.co.z
            v.co.x *= taper
            v.co.y *= taper
    for v in bm.verts:
        v.co *= FT
    bm.to_mesh(mesh)
    bm.free()
    for poly in mesh.polygons:
        poly.use_smooth = True
    return mesh


def build_landscape(ctrl):
    col = collection("12_Landscape_v008")
    mats = {code: principled(f"LAND_{code}_proxy_colour_representational", colr, 0.9,
                             note="category proxy; colour is representational, not documented")
            for code, (_, _, _, colr) in PLANTS.items()}
    mulch = principled("LAND_mulch_bed_surface", (0.13, 0.09, 0.06), 0.95, note="bed surface; mulch type not given on LP-101")
    lawn = principled("LAND_lawn", (0.22, 0.30, 0.14), 0.95, note="lawn / sod area per LP-101 (extent INT)")
    trunk = principled("LAND_trunk", (0.12, 0.09, 0.07), 0.9)
    meshes = {"shrub": _blob_mesh("proxy_shrub", "shrub"), "cover": _blob_mesh("proxy_cover", "cover"),
              "upright": _blob_mesh("proxy_upright", "upright"), "tree": _blob_mesh("proxy_tree_canopy", "shrub")}
    count = {}

    def place(code, x, y, k):
        kind, h, spread, _ = PLANTS[code]
        z = _idw(x, y, ctrl)
        data = meshes[kind].copy() if count.get(code, 0) == 0 else bpy.data.meshes[f"LAND_{code}_mesh"]
        if count.get(code, 0) == 0:
            data.name = f"LAND_{code}_mesh"
            data.materials.append(mats[code])
        obj = bpy.data.objects.new(f"LAND_{code}_{k:03d}", data)
        col.objects.link(obj)
        if kind == "tree":
            obj.location = (m(x), m(y), m(z + h * 0.4))
            obj.scale = (spread, spread, h * 0.6)
            box(f"LAND_{code}_{k:03d}_trunk", x - 0.08, x + 0.08, y - 0.08, y + 0.08, z, z + h * 0.45, col, trunk, "1.5 in. caliper (W); drawn 2 in.")
        else:
            obj.location = (m(x), m(y), m(z))
            obj.scale = (spread, spread, h)
        obj["code"] = code
        count[code] = count.get(code, 0) + 1

    for code, pts in POINT_PLANTS.items():
        for k, (x, y) in enumerate(pts):
            place(code, x, y, count.get(code, 0))
    for code, qty, sp, inside in MASS_PLANTS:
        cand = []
        for i in range(-10, 160):
            for j in range(-20, 100):
                x, y = -6.0 + i * sp + (sp / 2 if j % 2 else 0.0), -8.0 + j * sp * 0.866 + 100.0
                if inside(x, y):
                    cand.append((x, y))
        cx = sum(p[0] for p in cand) / len(cand)
        cy = sum(p[1] for p in cand) / len(cand)
        cand.sort(key=lambda p: (p[0] - cx) ** 2 + (p[1] - cy) ** 2)
        assert len(cand) >= qty, (code, qty, len(cand))
        for x, y in cand[:qty]:
            place(code, x, y, count.get(code, 0))
    for name, kind, poly in PATCHES:
        poly = ccw(poly)
        n = len(poly)
        verts = [(x, y, _idw(x, y, ctrl) + (0.08 if kind == "LAWN" else 0.05)) for x, y in poly]
        cxp, cyp = sum(p[0] for p in poly) / n, sum(p[1] for p in poly) / n
        verts.append((cxp, cyp, _idw(cxp, cyp, ctrl) + (0.08 if kind == "LAWN" else 0.05)))
        faces = [(i, (i + 1) % n, n) for i in range(n)]
        mesh_object("LAND_" + name, verts, faces, col, lawn if kind == "LAWN" else mulch, "LP-101 bed / lawn extent (INT outline)")
    return count


# ===================== v010 PRESENTATION (all v009 geometry, assignments and planting untouched) =====================
# Shader response, daylight, exposure and cameras only. Material NAMES and per-face ASSIGNMENTS are unchanged.
# Every value here is a visual-realism assumption, not a documented finish (notes/presentation_control_v010.md).
SUN_AZIMUTH_DEG, SUN_ELEVATION_DEG = 80.0, 36.0      # A: about 8:20 am solar time, mid-June, 35 deg N - lights the north front
PRESENTATION_VIEWS = {   # name: (camera position ft, target ft, lens mm, keep verticals, resolution)
    "hero_front_north": ((112.0, 292.0, 3.2), (100.0, 105.0, 3.2), 30.0, True, (2560, 1200)),
    "entrance_oblique_northeast": ((205.0, 196.0, 4.0), (118.0, 104.0, 4.0), 30.0, True, (2560, 1440)),
    "rear_oblique_southeast": ((262.0, -118.0, 2.1), (110.0, 20.0, 2.1), 40.0, True, (2560, 1440)),
    "elevated_site_oblique_northwest": ((-165.0, 262.0, 135.0), (88.0, 62.0, 4.0), 35.0, False, (2560, 1440)),
    "facade_material_closeup": ((48.0, 140.0, 4.3), (88.0, 106.0, 4.3), 45.0, True, (2560, 1440)),
    "corner_northwest_eye_level": ((-92.0, 196.0, 0.0), (40.0, 85.0, 0.0), 30.0, True, (2560, 1440)),
    "landscape_entrance_oblique": ((44.0, 150.0, 11.0), (50.0, 108.0, 1.5), 28.0, False, (2560, 1440)),   # v012 addition
}


def _nodes(mat):
    nt = mat.node_tree
    return nt, nt.nodes.get("Principled BSDF")


def _noise(nt, scale, detail=6.0, rough=0.55, coord="Object"):
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = scale
    nz.inputs["Detail"].default_value = detail
    nz.inputs["Roughness"].default_value = rough
    nt.links.new(tc.outputs[coord], nz.inputs["Vector"])
    return nz


def _ramp_value(nt, src, lo, hi):
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.inputs["To Min"].default_value = lo
    mr.inputs["To Max"].default_value = hi
    nt.links.new(src, mr.inputs["Value"])
    return mr.outputs[0]


def _vary_colour(nt, b, amount, scale):
    """Multiply the existing base colour by a gentle noise (keeps the hue that was assigned)."""
    base_in = b.inputs["Base Color"]
    nz = _noise(nt, scale)
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    mix.blend_type = "MULTIPLY"
    nt.links.new(_ramp_value(nt, nz.outputs["Fac"], 0.0, amount), mix.inputs["Factor"])
    if base_in.is_linked:
        nt.links.new(base_in.links[0].from_socket, mix.inputs["A"])
    else:
        mix.inputs["A"].default_value = base_in.default_value
    mix.inputs["B"].default_value = (0.35, 0.35, 0.35, 1.0)
    nt.links.new(mix.outputs["Result"], base_in)


def _vary_roughness(nt, b, lo, hi, scale):
    nz = _noise(nt, scale, detail=3.0)
    nt.links.new(_ramp_value(nt, nz.outputs["Fac"], lo, hi), b.inputs["Roughness"])


def _add_bump(nt, b, scale, strength, distance_ft):
    nz = _noise(nt, scale, detail=8.0, rough=0.65)
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = strength
    bump.inputs["Distance"].default_value = distance_ft * FT
    nt.links.new(nz.outputs["Fac"], bump.inputs["Height"])
    normal_in = b.inputs["Normal"]
    if normal_in.is_linked:                       # chain after an existing bump (brick joints)
        nt.links.new(normal_in.links[0].from_socket, bump.inputs["Normal"])
    nt.links.new(bump.outputs[0], normal_in)


def _per_object_tint(nt, b, amount):
    info = nt.nodes.new("ShaderNodeObjectInfo")
    hsv = nt.nodes.new("ShaderNodeHueSaturation")
    base_in = b.inputs["Base Color"]
    if base_in.is_linked:
        nt.links.new(base_in.links[0].from_socket, hsv.inputs["Color"])
    else:
        hsv.inputs["Color"].default_value = base_in.default_value
    nt.links.new(_ramp_value(nt, info.outputs["Random"], 1.0 - amount, 1.0 + amount), hsv.inputs["Value"])
    nt.links.new(hsv.outputs["Color"], base_in)


def refine_materials_v010():
    done = []
    for mat in bpy.data.materials:
        if not mat.use_nodes:
            continue
        nt, b = _nodes(mat)
        if b is None:
            continue
        n = mat.name
        if n.startswith("BRK-1") or n.startswith("BC-1"):
            _vary_colour(nt, b, 0.35, 0.9)            # brick-to-brick and lot variation
            _vary_roughness(nt, b, 0.55, 0.85, 6.0)   # ironspot bricks have a slight sheen
            _add_bump(nt, b, 40.0, 0.12, 0.02)
        elif n.startswith(("ACM-", "MTL-", "PAINT_match", "UNRES_canopy_steel", "UNRES_HM_door")):
            _vary_roughness(nt, b, 0.22, 0.36, 0.6)   # coil-coated / painted metal, faint oil-canning in reflection
            _add_bump(nt, b, 0.35, 0.02, 0.01)
            if "Coat Weight" in b.inputs:
                b.inputs["Coat Weight"].default_value = 0.15
        elif n.startswith("FRAME_"):
            _vary_roughness(nt, b, 0.28, 0.40, 2.0)
        elif n.startswith("GLASS_G1_G2"):
            b.inputs["Base Color"].default_value = (0.012, 0.018, 0.020, 1.0)
            b.inputs["Roughness"].default_value = 0.0
            if "Specular IOR Level" in b.inputs:
                b.inputs["Specular IOR Level"].default_value = 0.65  # coated IGU reads a little more reflective than bare glass
            _add_bump(nt, b, 0.25, 0.004, 0.01)       # very slight roller-wave distortion
        elif n.startswith("GLASS_G3"):
            b.inputs["Roughness"].default_value = 0.03
        elif n.startswith("TPO_"):
            _vary_colour(nt, b, 0.10, 0.4)
            _vary_roughness(nt, b, 0.5, 0.7, 1.0)
        elif n.startswith(("SITE_pavers", "SITE_plaza", "SITE_concrete", "SITE_existing_plaza", "UNRES-colour_terrace",
                           "UNRES_building_base", "UNRES_painted_CMU", "UNRES_terrace_parapet")):
            _vary_colour(nt, b, 0.25, 1.5)
            _vary_roughness(nt, b, 0.7, 0.9, 3.0)
            _add_bump(nt, b, 25.0, 0.10, 0.01)
        elif n.startswith("SITE_existing_asphalt"):
            _vary_colour(nt, b, 0.30, 0.25)
            _vary_roughness(nt, b, 0.75, 0.95, 1.5)
            _add_bump(nt, b, 120.0, 0.20, 0.01)
        elif n.startswith(("SITE_lawn", "LAND_lawn")):
            _vary_colour(nt, b, 0.35, 0.8)
            _add_bump(nt, b, 60.0, 0.5, 0.08)
        elif n.startswith(("SITE_landscape_bed", "SITE_entrance_bed", "LAND_mulch")):
            _vary_colour(nt, b, 0.4, 3.0)
            _add_bump(nt, b, 35.0, 0.6, 0.06)
        elif n.startswith("LAND_") and "proxy_colour" in n:
            _per_object_tint(nt, b, 0.18)             # plant-to-plant variation
            _vary_colour(nt, b, 0.45, 9.0)            # leaf-scale mottling
            _add_bump(nt, b, 14.0, 0.9, 0.12)         # breaks up the smooth proxy silhouette shading
            if "Subsurface Weight" in b.inputs:
                b.inputs["Subsurface Weight"].default_value = 0.05
        else:
            continue
        done.append(n)
    return done


def presentation_v010(scene, col):
    refined = refine_materials_v010()
    # ---- daylight: physical sky for ambient + a sun lamp with a true solar disc size ----
    sun_obj = bpy.data.objects.get("Sun")
    az, el = math.radians(SUN_AZIMUTH_DEG), math.radians(SUN_ELEVATION_DEG)
    to_sun = Vector((math.sin(az) * math.cos(el), math.cos(az) * math.cos(el), math.sin(el)))
    sun_obj.rotation_euler = (-to_sun).to_track_quat("-Z", "Y").to_euler()
    sun_obj.data.angle = math.radians(0.545)
    sun_obj.data.energy = 7.0
    sun_obj.data.color = (1.0, 0.95, 0.88)
    world = bpy.data.worlds.new("Daylight_v010")
    world.use_nodes = True
    nt = world.node_tree
    bg = nt.nodes["Background"]
    sky_type = "flat"
    try:
        sky = nt.nodes.new("ShaderNodeTexSky")
        for candidate in ("NISHITA", "MULTIPLE_SCATTERING", "SINGLE_SCATTERING", "HOSEK_WILKIE"):
            try:
                sky.sky_type = candidate
                sky_type = candidate
                break
            except TypeError:
                continue
        for attr, val in (("sun_disc", False), ("sun_elevation", el), ("sun_rotation", az), ("altitude", 200.0),
                          ("air_density", 1.0), ("dust_density", 1.0), ("aerosol_density", 1.0), ("ozone_density", 1.0)):
            if hasattr(sky, attr):
                try:
                    setattr(sky, attr, val)
                except (TypeError, AttributeError):
                    pass
        if hasattr(sky, "sun_direction"):
            sky.sun_direction = to_sun
        nt.links.new(sky.outputs[0], bg.inputs[0])
        bg.inputs[1].default_value = 0.16
    except Exception:
        bg.inputs[0].default_value = (0.55, 0.70, 1.0, 1)
        bg.inputs[1].default_value = 1.2
    scene.world = world
    # ---- backdrop ground outside the modeled site so eye-level views do not show the cut edge (not a site element) ----
    terr = bpy.data.objects["Site_Terrain_INTERPOLATED"]
    tv = [(v.co.x / FT, v.co.y / FT, v.co.z / FT) for v in terr.data.vertices if v.co.z / FT > TERRAIN_BASE + 0.5]
    x_lo, x_hi = min(v[0] for v in tv), max(v[0] for v in tv)
    y_lo, y_hi = min(v[1] for v in tv), max(v[1] for v in tv)

    def edge_mean(test):
        zs = [z for x, y, z in tv if test(x, y)]
        return sum(zs) / len(zs)
    zn = edge_mean(lambda x, y: y > y_hi - 0.1)
    zs_ = edge_mean(lambda x, y: y < y_lo + 0.1)
    ze = edge_mean(lambda x, y: x > x_hi - 0.1)
    zw = edge_mean(lambda x, y: x < x_lo + 0.1)
    back_g = principled("PRES_backdrop_ground_not_site", (0.17, 0.21, 0.12), 0.95, note="presentation backdrop only")
    back_a = principled("PRES_backdrop_paving_not_site", (0.05, 0.05, 0.055), 0.9, note="presentation backdrop only")
    far = 2600.0
    box("PRES_backdrop_north", -far, far, y_hi, far, -14.0, zn, col, back_a, "presentation backdrop only")
    box("PRES_backdrop_south", -far, far, -far, y_lo, -14.0, zs_, col, back_g, "presentation backdrop only")
    box("PRES_backdrop_east", x_hi, far, y_lo, y_hi, -14.0, ze, col, back_g, "presentation backdrop only")
    box("PRES_backdrop_west", -far, x_lo, y_lo, y_hi, -14.0, zw, col, back_g, "presentation backdrop only")
    arrow = bpy.data.objects.get("Site_North_arrow")
    if arrow:
        arrow.hide_render = True                    # review aid, not part of the presentation
    # ---- cameras ----
    cams = {}
    for name, (pos, tgt, lens, level, res) in PRESENTATION_VIEWS.items():
        ground = 0.0
        cam = add_camera("Cam_" + name, pos, tgt, col, None, lens)
        if level:                                   # level camera + vertical shift = no converging verticals
            cam.data.shift_y = 0.16
        cam.data.dof.use_dof = False
        cams[name] = (cam, res)
    globals()["BACKDROP_Z_V010"] = (zn, zs_, ze, zw)          # v011 reads the backdrop heights
    return cams, refined, sky_type


# ===================== v011 CONTEXT (v010 model, lighting and cameras above are unchanged) =====================
# Everything here is CONTEXT ONLY, in collection "14_Context_v011", named CTX_... and labelled with its confidence:
#   MEASURED = outline scaled from CS-101 rev 6 (+/-2 ft), SIMPLIFIED = real element reduced to a plain shape,
#   APPROX = existence supported by site photos, size/position estimated. See notes/context_control_v011.md.
BUILDING_I_FOOTPRINT = [(256, -3.5), (297, -3.5), (297, -1.5), (490, -1.5), (490, 3), (519.5, 3), (519.5, 62), (530, 62),
                        (530, 170), (518, 170), (518, 197.5), (340, 197.5), (340, 170), (320, 170), (320, 74.5),
                        (278.5, 74.5), (278.5, 53.5), (260.5, 53.5), (260.5, 38), (256, 38)]      # MEASURED, simplified corners
BUILDING_I_FFE = 661.75 - 660.30                    # W (CG-101)
BUILDING_I_HEIGHT = 34.0                            # APPROX: two-level, reads about as tall as Building II's low roof in the drone photos
BLOCK = {"x0": -38.5, "x1": 545.0, "y0": -6.8, "y1": 410.0}      # right-of-way lines, MEASURED from CS-101
ISLAND_ROWS_Y = [230.0, 264.0, 354.0]               # MEASURED (+/-3 ft); the y = 152.6 row already exists in v006
ISLAND_X = [44.0, 105.0, 166.0, 337.0, 399.0, 461.0]
STREET_TREES_SOUTH = [(-13.6 + 40.3 * k, -19.3) for k in range(14)]      # first 7 MEASURED on LP-101, remainder continue the same spacing
ISLAND_TREES = [(44.0, 152.6), (105.0, 152.6), (166.0, 152.6)]          # MEASURED on LP-101 (existing trees)


def build_context_v011(col, zn, zs, ze, zw):
    import random
    rng = random.Random(11)
    mats = {
        "bldg": principled("CTX_BuildingI_APPROX_massing_only", (0.10, 0.095, 0.09), 0.75, note="existing Building I: massing only, material approximate (dark masonry in photos)"),
        "bldg_band": principled("CTX_BuildingI_APPROX_light_band", (0.62, 0.61, 0.58), 0.5, note="approximate light panel band seen in photos"),
        "asphalt": bpy.data.materials.get("SITE_existing_asphalt"),
        "conc": bpy.data.materials.get("SITE_concrete_flatwork"),
        "lawn": bpy.data.materials.get("SITE_lawn_ground_shape_no_planting"),
        "island": bpy.data.materials.get("SITE_landscape_bed_ground_shape"),
        "far": principled("CTX_distant_buildings_APPROX", (0.30, 0.29, 0.27), 0.85, note="apartments / townhomes seen in drone photos; size and position approximate"),
        "roof": principled("CTX_distant_roofs_APPROX", (0.12, 0.12, 0.13), 0.8),
        "tree": principled("CTX_tree_canopy_APPROX", (0.08, 0.12, 0.06), 0.95, note="context trees; species and size approximate"),
        "trunk": principled("CTX_trunk", (0.12, 0.09, 0.07), 0.9),
    }
    n = 0
    b = BLOCK
    # --- Building I: plain mass on the documented footprint ---
    prism("CTX_BuildingI_mass_MEASURED_footprint_APPROX_height", ccw(BUILDING_I_FOOTPRINT), ze - 0.5, BUILDING_I_FFE + BUILDING_I_HEIGHT,
          col, mats["bldg"], "footprint CS-101 rev 6 (M +/-2 ft); FFE 661.75 (W); height APPROX from photos")
    prism("CTX_BuildingI_upper_band_APPROX", ccw(offset_poly(ccw(BUILDING_I_FOOTPRINT), [0.15] * len(BUILDING_I_FOOTPRINT))),
          BUILDING_I_FFE + 18.0, BUILDING_I_FFE + 34.2, col, mats["bldg_band"], "APPROX: lighter upper storey seen in photos")
    n += 2
    # --- north parking lot to Golf Links Dr: islands, perimeter lawn and sidewalk ---
    for yc in ISLAND_ROWS_Y:
        for xc in ISLAND_X:
            c = 4.0
            xa, xb, ya, yb = xc - 19.5, xc + 19.5, yc - 5.7, yc + 5.7
            poly = [(xa + c, ya), (xb - c, ya), (xb, ya + c), (xb, yb - c), (xb - c, yb), (xa + c, yb), (xa, yb - c), (xa, ya + c)]
            prism(f"CTX_Parking_island_{int(yc)}_{int(xc)}_MEASURED_approx", poly, zn - 0.5, zn + 0.5, col, mats["island"], "CS-101 (M +/-3 ft); 6 in. curb")
            n += 1
    # perimeter strips inside the right-of-way: lawn band + sidewalk (SIMPLIFIED, widths scaled from CS-101)
    box("CTX_Lawn_band_north_SIMPLIFIED", b["x0"], b["x1"], b["y1"] - 22.0, b["y1"], zn, zn + 0.35, col, mats["lawn"], "CS-101 perimeter landscape strip")
    box("CTX_Sidewalk_north_SIMPLIFIED", b["x0"], b["x1"], b["y1"], b["y1"] + 8.0, zn, zn + 0.4, col, mats["conc"], "existing sidewalk (CS-101 label)")
    box("CTX_Street_Golf_Links_Dr_SIMPLIFIED", -600, 1100, b["y1"] + 14.0, b["y1"] + 74.0, zn, zn + 0.05, col, mats["asphalt"], "Golf Links Dr, 60 ft public R/W (CS-101 label)")
    box("CTX_Lawn_beyond_Golf_Links_APPROX", -600, 1100, b["y1"] + 74.0, b["y1"] + 600.0, zn, zn + 0.3, col, mats["lawn"], "APPROX")
    box("CTX_Street_N_Rea_Park_Ln_SIMPLIFIED", -600, 1100, b["y0"] - 62.0, b["y0"] - 8.0, zs - 0.1, zs + 0.05, col, mats["asphalt"], "North Rea Park Ln, proposed 60 ft public R/W with on-street parking (CS-101)")
    box("CTX_Sidewalk_south_SIMPLIFIED", -60, b["x1"], b["y0"] - 8.0, b["y0"] - 1.0, zs - 0.1, zs + 0.35, col, mats["conc"], "sidewalk along North Rea Park Ln (CS-101)")
    box("CTX_Park_lawn_south_APPROX", -600, 1100, b["y0"] - 420.0, b["y0"] - 62.0, zs - 0.1, zs + 0.3, col, mats["lawn"], "open lawn / park south of the street seen in the drone photos (APPROX extent)")
    box("CTX_Street_Terminus_Rd_SIMPLIFIED", b["x0"] - 66.0, b["x0"] - 8.0, -600, 1100, zw - 0.2, zw + 0.05, col, mats["asphalt"], "Terminus Road, proposed public R/W (CS-101)")
    box("CTX_Street_Midway_Park_Dr_SIMPLIFIED", b["x1"] + 10.0, b["x1"] + 60.0, -600, 1100, ze - 0.2, ze + 0.05, col, mats["asphalt"], "Midway Park Dr, 60 ft public R/W (CS-101)")
    box("CTX_Ground_east_of_site_SIMPLIFIED", TERRAIN_X[1], b["x1"] + 10.0, -6.8, 204.0, ze - 0.3, ze + 0.2, col, mats["conc"], "paved plaza / walks around Building I (SIMPLIFIED to one surface)")
    box("CTX_Parking_east_half_SIMPLIFIED", TERRAIN_X[1], b["x1"], 204.0, b["y1"] - 22.0, zn - 0.3, zn + 0.04, col, mats["asphalt"], "existing parking lot east half (CS-101)")
    n += 10

    # --- distant buildings seen in the drone photos (APPROX) ---
    for k, (x0, x1, y0, y1, h) in enumerate([(-120, 140, -560, -480, 48), (190, 470, -580, -500, 48), (520, 760, -520, -440, 48),
                                             (-420, -330, -120, 260, 30), (-420, -330, 300, 520, 30), (700, 800, 40, 300, 30)]):
        box(f"CTX_Distant_building_{k + 1}_APPROX", x0, x1, y0, y1, zs - 1.0, zs + h, col, mats["far"], "seen in 8.29.26 drone photos; size / position APPROX")
        box(f"CTX_Distant_building_{k + 1}_roof_APPROX", x0 - 2, x1 + 2, y0 - 2, y1 + 2, zs + h, zs + h + 6, col, mats["roof"], "APPROX")
        n += 2

    # --- trees: shared low-detail meshes ---
    canopy = bpy.data.meshes.new("CTX_tree_canopy_mesh")
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.5 * FT)
    for v in bm.verts:
        v.co *= 1.0 + 0.18 * (rng.random() - 0.5)
    bm.to_mesh(canopy)
    bm.free()
    canopy.materials.append(mats["tree"])
    for poly in canopy.polygons:
        poly.use_smooth = True

    def tree(name, x, y, z, height, spread, trunk=True):
        obj = bpy.data.objects.new(name, canopy)
        obj.location = (m(x), m(y), m(z + height - spread * 0.45))
        obj.scale = (spread, spread, spread * 0.9)
        obj.rotation_euler = (0, 0, rng.random() * 6.28)
        col.objects.link(obj)
        if trunk:
            box(name + "_trunk", x - 0.2, x + 0.2, y - 0.2, y + 0.2, z, z + height - spread * 0.5, col, mats["trunk"], "")

    for k, (x, y) in enumerate(STREET_TREES_SOUTH):
        tree(f"CTX_Street_tree_south_{k + 1:02d}_young_APPROX_size", x, y, zs, 12.0, 5.5)
    for k, (x, y) in enumerate(ISLAND_TREES):
        tree(f"CTX_Island_tree_{k + 1}_existing_APPROX_size", x, y, -1.2, 12.0, 5.5)
    n += len(STREET_TREES_SOUTH) + len(ISLAND_TREES)
    # distant tree line on all sides (APPROX; drone photos show a continuous wooded horizon)
    k = 0
    for side in range(4):
        for i in range(70):
            t = -1100.0 + i * 38.0 + rng.uniform(-10, 10)
            d = 900.0 + rng.uniform(-60, 120)
            x, y = ((t, 250 + d), (t, 200 - d), (250 + d, t), (250 - d, t))[side]
            tree(f"CTX_Horizon_tree_{k:03d}_APPROX", x, y, -6.0, rng.uniform(45, 65), rng.uniform(45, 70), trunk=False)
            k += 1
    n += k
    return n


# ===================== v012 VEGETATION (positions, quantities, beds, site and building unchanged) =====================
# Procedural leaf-card plants generated from a fixed seed; no external assets. See notes/vegetation_control_v012.md.
# spec: leaf colour, accent colour or None, leaf roughness, (leaf_len, leaf_w) ft, leaf count, habit, accents
VEG_SPECS = {
    "DAZA": dict(leaf=(0.158, 0.273, 0.116), rough=0.45, size=(0.12, 0.05), n=420, habit="mound"),
    "RHCO": dict(leaf=(0.179, 0.273, 0.126), rough=0.45, size=(0.13, 0.055), n=440, habit="mound"),
    "JEWL": dict(leaf=(0.147, 0.263, 0.179), rough=0.4, size=(0.13, 0.045), n=380, habit="layered"),
    "JADE": dict(leaf=(0.137, 0.252, 0.189), rough=0.4, size=(0.14, 0.045), n=460, habit="layered"),
    "FOAR": dict(leaf=(0.273, 0.399, 0.147), rough=0.55, size=(0.16, 0.06), n=300, habit="arching"),
    "ILST": dict(leaf=(0.074, 0.158, 0.074), rough=0.3, size=(0.07, 0.035), n=620, habit="upright"),
    "GATE": dict(leaf=(0.074, 0.179, 0.074), rough=0.22, size=(0.25, 0.11), n=380, habit="upright_oval"),
    "SANJ": dict(leaf=(0.095, 0.179, 0.084), rough=0.3, size=(0.18, 0.07), n=950, habit="tree"),
    "CARE": dict(leaf=(0.425, 0.463, 0.200), rough=0.6, habit="blades"),
    "COZA": dict(leaf=(0.273, 0.420, 0.147), accent=(0.55, 0.45, 0.08), rough=0.6, size=(0.15, 0.02), n=300, habit="mound", flowers=14),
    "CORA": dict(leaf=(0.273, 0.116, 0.210), accent=(0.45, 0.32, 0.36), rough=0.5, habit="rosette", leaf_size=(0.30, 0.28), leaves=20, stalks=3),
    "JUNE": dict(leaf=(0.200, 0.300, 0.163), rough=0.45, habit="rosette", leaf_size=(0.55, 0.34), leaves=16, stalks=0),
    "CATM": dict(leaf=(0.250, 0.300, 0.237), accent=(0.30, 0.28, 0.45), rough=0.7, size=(0.08, 0.04), n=260, habit="mound", spikes=22),
    "OSOR": dict(leaf=(0.147, 0.294, 0.126), accent=(0.62, 0.58, 0.45), rough=0.45, size=(0.12, 0.06), n=230, habit="mound", flowers=7),
    "SEAS": dict(leaf=(0.210, 0.420, 0.168), accent=(0.50, 0.30, 0.36), rough=0.55, size=(0.09, 0.05), n=90, habit="mound", flowers=7),
}
VEG_VARIANTS = 4


def _leaf_material(name, colour, rough, note):
    mat = principled(name, colour, rough, note=note)
    nt = mat.node_tree
    b = nt.nodes.get("Principled BSDF")
    _per_object_tint(nt, b, 0.14)
    _vary_colour(nt, b, 0.55, 18.0)
    if "Subsurface Weight" in b.inputs:
        b.inputs["Subsurface Weight"].default_value = 0.08
    out = nt.nodes.get("Material Output")
    trans = nt.nodes.new("ShaderNodeBsdfTranslucent")
    trans.inputs["Color"].default_value = (colour[0] * 1.8, colour[1] * 2.0, colour[2] * 1.2, 1.0)
    mix = nt.nodes.new("ShaderNodeMixShader")
    mix.inputs[0].default_value = 0.30
    nt.links.new(b.outputs[0], mix.inputs[1])
    nt.links.new(trans.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs["Surface"])
    return mat


def _kite(bm, base, axis, side, normal, length, width):
    """One folded leaf: base, two shoulder points lifted along the fold, tip."""
    mid = base + axis * (length * 0.45)
    lift = normal * (width * 0.22)
    v = [bm.verts.new(base), bm.verts.new(mid + side * (width / 2) + lift), bm.verts.new(base + axis * length),
         bm.verts.new(mid - side * (width / 2) + lift)]
    bm.faces.new((v[0], v[1], v[2]))
    bm.faces.new((v[0], v[2], v[3]))


def _lobes(rng, count, rx, rz, z0, top_bias):
    out = []
    for _ in range(count):
        a, r = rng.uniform(0, 6.283), rng.uniform(0.0, 0.36) * rx
        cz = z0 + rz * rng.uniform(0.35, 0.62) * top_bias
        out.append((Vector((r * math.cos(a), r * math.sin(a), cz)), rng.uniform(0.66, 0.84)))
    return out


def _leaf_cloud(bm, rng, spec, rx, rz, z0=0.0, layered=False, upright=False, taper=0.0, lobes=5):
    ll, lw = spec["size"]
    up = Vector((0, 0, 1))
    centres = _lobes(rng, lobes, rx, rz, z0, 1.0)
    for _ in range(spec["n"]):
        c, f = centres[rng.randrange(len(centres))]
        d = Vector((rng.gauss(0, 1), rng.gauss(0, 1), rng.gauss(0, 1)))
        if d.length < 1e-6:
            continue
        d.normalize()
        if d.z < -0.25:
            d.z = -d.z * 0.3
        rad = rng.uniform(0.78, 1.0)
        p = c + Vector((d.x * rx * f * rad, d.y * rx * f * rad, d.z * rz * (0.62 if not upright else 0.66) * rad))
        if taper:                                    # narrow toward the top (pyramidal habit)
            k = max(0.25, 1.0 - taper * max(0.0, (p.z - z0) / max(rz, 1e-6)))
            p.x *= k
            p.y *= k
        p.z = max(z0 + 0.03, min(z0 + rz * 1.02, p.z))
        lim = math.hypot(p.x, p.y)
        if lim > rx:
            p.x *= rx / lim
            p.y *= rx / lim
        out = Vector((d.x, d.y, 0.0))
        if out.length < 1e-6:
            out = Vector((1, 0, 0))
        out.normalize()
        jitter = Vector((rng.uniform(-0.45, 0.45), rng.uniform(-0.45, 0.45), rng.uniform(-0.25, 0.25)))
        axis = out * (0.85 if layered else 0.6) + up * (0.06 if layered else 0.42) + jitter
        axis.normalize()
        side = axis.cross(up)
        if side.length < 1e-6:
            side = Vector((1, 0, 0))
        side.normalize()
        _kite(bm, p, axis, side, side.cross(axis).normalized(), ll * rng.uniform(0.75, 1.2), lw * rng.uniform(0.8, 1.15))
    return centres


def _core(bm, centres, rx, rz, shrink=0.55, floor=0.0):
    for c, f in centres:
        res = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.0)
        for v in res["verts"]:
            v.co = Vector((c.x + v.co.x * rx * f * shrink, c.y + v.co.y * rx * f * shrink, max(floor, c.z + v.co.z * rz * 0.5 * shrink)))


def _disc(bm, centre, r, sides=6):
    vs = [bm.verts.new(centre + Vector((r * math.cos(6.283 * k / sides), r * math.sin(6.283 * k / sides), 0))) for k in range(sides)]
    bm.faces.new(vs)


def _strip(bm, pts, width, side):
    prev = None
    for k, p in enumerate(pts):
        w = width * (1.0 - 0.8 * k / (len(pts) - 1))
        a, b2 = bm.verts.new(p + side * w / 2), bm.verts.new(p - side * w / 2)
        if prev:
            bm.faces.new((prev[0], a, b2, prev[1]))
        prev = (a, b2)


def _plant_mesh(code, variant, spread, height):
    """Mesh in real feet (then metres): slot 0 leaves, slot 1 accents/stems, slot 2 dark core."""
    import random
    rng = random.Random(f"{code}-{variant}")
    spec = VEG_SPECS[code]
    bm = bmesh.new()
    rx, rz = spread / 2.0, height
    first_accent_face = None
    habit = spec["habit"]
    centres = []
    if habit in ("mound", "layered", "arching"):
        centres = _leaf_cloud(bm, rng, spec, rx, rz, layered=(habit == "layered"), lobes=5 if habit != "arching" else 7)
    elif habit == "upright":
        centres = _leaf_cloud(bm, rng, spec, rx, rz, upright=True, taper=0.65, lobes=4)
    elif habit == "upright_oval":
        centres = _leaf_cloud(bm, rng, spec, rx, rz, upright=True, taper=0.3, lobes=4)
    elif habit == "tree":
        centres = _leaf_cloud(bm, rng, spec, rx, rz, upright=True, taper=0.25, lobes=6)
    elif habit == "blades":
        for _ in range(95):
            a = rng.uniform(0, 6.283)
            d = Vector((math.cos(a), math.sin(a), 0))
            L = rng.uniform(0.75, 1.15) * height * 1.35
            p0 = d * rng.uniform(0.0, 0.12)
            pts = [p0, p0 + d * L * 0.30 + Vector((0, 0, L * 0.52)), p0 + d * L * 0.62 + Vector((0, 0, L * 0.66)),
                   p0 + d * L * min(0.95, rx / max(L, 1e-6) * 1.0 + 0.35) + Vector((0, 0, L * rng.uniform(0.30, 0.50)))]
            _strip(bm, pts, rng.uniform(0.035, 0.055), d.cross(Vector((0, 0, 1))))
    elif habit == "rosette":
        ll, lw = spec["leaf_size"]
        for k in range(spec["leaves"]):
            a = 6.283 * k / spec["leaves"] + rng.uniform(-0.25, 0.25)
            d = Vector((math.cos(a), math.sin(a), 0))
            side = d.cross(Vector((0, 0, 1)))
            rise = rng.uniform(0.25, 0.75)
            L = ll * rng.uniform(0.8, 1.15)
            base = d * 0.05 + Vector((0, 0, 0.05))
            pts = [base, base + d * L * 0.45 + Vector((0, 0, height * rise)), base + d * L * 0.8 + Vector((0, 0, height * rise * 0.95)),
                   base + d * L + Vector((0, 0, height * rise * 0.6))]
            widths = [0.15 * lw, lw, 0.8 * lw, 0.05 * lw]
            prev = None
            for p, w in zip(pts, widths):
                crease = Vector((0, 0, -w * 0.18))
                tri = (bm.verts.new(p + side * w / 2), bm.verts.new(p + crease), bm.verts.new(p - side * w / 2))
                if prev:
                    bm.faces.new((prev[0], tri[0], tri[1], prev[1]))
                    bm.faces.new((prev[1], tri[1], tri[2], prev[2]))
                prev = tri
    leaf_faces = len(bm.faces)
    # accents (slot 1)
    for _ in range(spec.get("flowers", 0)):
        a, r = rng.uniform(0, 6.283), rng.uniform(0, 0.8) * rx
        _disc(bm, Vector((r * math.cos(a), r * math.sin(a), height * rng.uniform(0.85, 1.05))), rng.uniform(0.035, 0.06))
    for _ in range(spec.get("spikes", 0)):
        a, r = rng.uniform(0, 6.283), rng.uniform(0.1, 0.85) * rx
        base = Vector((r * math.cos(a), r * math.sin(a), height * 0.6))
        lean = Vector((math.cos(a) * 0.35, math.sin(a) * 0.35, 1.0)).normalized()
        _kite(bm, base, lean, lean.cross(Vector((0, 0, 1))).normalized(), Vector((math.cos(a), math.sin(a), 0)), height * 0.55, 0.035)
    for _ in range(spec.get("stalks", 0)):
        a, r = rng.uniform(0, 6.283), rng.uniform(0.0, 0.25) * rx
        base = Vector((r * math.cos(a), r * math.sin(a), height * 0.4))
        _kite(bm, base, Vector((0.05, 0.05, 1)).normalized(), Vector((1, 0, 0)), Vector((0, 1, 0)), height * 1.3, 0.02)
    if habit == "arching":
        for _ in range(14):
            a = rng.uniform(0, 6.283)
            d = Vector((math.cos(a), math.sin(a), 0))
            L = rx * rng.uniform(0.8, 1.05)
            pts = [Vector((0, 0, 0.02)), d * L * 0.35 + Vector((0, 0, height * 0.9)), d * L * 0.7 + Vector((0, 0, height * 0.95)),
                   d * L + Vector((0, 0, height * 0.45))]
            _strip(bm, pts, 0.03, d.cross(Vector((0, 0, 1))))
    accent_faces = len(bm.faces)
    if centres:                                     # tapered habits get a slimmer core so it never shows through
        _core(bm, centres, rx, rz, shrink=0.36 if habit in ("upright", "upright_oval", "tree") else 0.55)
    for v in bm.verts:
        v.co *= FT
    mesh = bpy.data.meshes.new(f"VEG_{code}_v{variant}")
    bm.faces.ensure_lookup_table()
    bm.to_mesh(mesh)
    bm.free()
    for i, poly in enumerate(mesh.polygons):
        poly.material_index = 0 if i < leaf_faces else (1 if i < accent_faces else 2)
    return mesh


def _canopy_mesh(name, seed, n_cards, lobes, card):
    """Unit-diameter tree canopy (centred on the origin, like the v011 canopy) with a lumpy dark core."""
    import random
    rng = random.Random(seed)
    bm = bmesh.new()
    spec = {"size": (card, card * 0.55), "n": n_cards}
    centres = _leaf_cloud(bm, rng, spec, 0.5, 0.9, z0=-0.45, upright=True, taper=0.15, lobes=lobes)
    leaf_faces = len(bm.faces)
    _core(bm, centres, 0.5, 0.9, shrink=0.5, floor=-0.42)
    for v in bm.verts:
        v.co *= FT
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    for i, poly in enumerate(mesh.polygons):
        poly.material_index = 0 if i < leaf_faces else 1
    return mesh


def _ground_breakup(mat, scale, amount, bump_strength, desaturate=0.0):
    nt = mat.node_tree
    b = nt.nodes.get("Principled BSDF")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    vor = nt.nodes.new("ShaderNodeTexVoronoi")
    vor.inputs["Scale"].default_value = scale
    nt.links.new(tc.outputs["Object"], vor.inputs["Vector"])
    base_in = b.inputs["Base Color"]
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    mix.blend_type = "MULTIPLY"
    mix.inputs["Factor"].default_value = amount
    if base_in.is_linked:
        nt.links.new(base_in.links[0].from_socket, mix.inputs["A"])
    else:
        mix.inputs["A"].default_value = base_in.default_value
    nt.links.new(vor.outputs["Color"], mix.inputs["B"])
    src = mix.outputs["Result"]
    if desaturate:
        hsv = nt.nodes.new("ShaderNodeHueSaturation")
        hsv.inputs["Saturation"].default_value = 1.0 - desaturate
        nt.links.new(src, hsv.inputs["Color"])
        src = hsv.outputs["Color"]
    nt.links.new(src, base_in)
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = bump_strength
    bump.inputs["Distance"].default_value = 0.05 * FT
    nt.links.new(vor.outputs["Distance"], bump.inputs["Height"])
    normal_in = b.inputs["Normal"]
    if normal_in.is_linked:
        nt.links.new(normal_in.links[0].from_socket, bump.inputs["Normal"])
    nt.links.new(bump.outputs[0], normal_in)


def vegetation_v012():
    import random
    rng = random.Random(12)
    report = {}
    core = principled("VEG_inner_shade", (0.035, 0.055, 0.03), 0.95, note="dark inner core so plants are not see-through")
    # ---- Building II planting: same objects, same locations; new mesh, material and scale ----
    land = bpy.data.collections["12_Landscape_v008"]
    mats, meshes = {}, {}
    for obj in land.objects:
        code = obj.get("code")
        if code not in VEG_SPECS:
            continue
        kind, h, spread, _ = PLANTS[code]
        spec = VEG_SPECS[code]
        if code not in mats:
            leaf = _leaf_material(f"VEG_{code}_foliage", spec["leaf"], spec["rough"], "cultivar-typical foliage tone; not from the drawings")
            acc = principled(f"VEG_{code}_accent", spec.get("accent", (0.10, 0.08, 0.05)), 0.6, note="flowers / stems, muted; not from the drawings")
            mats[code] = (leaf, acc)
            canopy_h = h * 0.6 if kind == "tree" else h
            meshes[code] = []
            for v in range(VEG_VARIANTS):
                me = _plant_mesh(code, v, spread, canopy_h)
                for mt in (leaf, acc, core):
                    me.materials.append(mt)
                meshes[code].append(me)
        index = int(obj.name.rsplit("_", 1)[-1])
        obj.data = meshes[code][index % VEG_VARIANTS]
        grow = 1.0 + 0.10 * rng.random()                     # never below the scheduled minimum size
        obj.scale = (grow, grow, grow)
        obj.rotation_euler = (0.0, 0.0, rng.uniform(0.0, 6.283))
        report[code] = report.get(code, 0) + 1
    # ---- context trees: same objects and positions; canopy mesh swapped, trunks rounded ----
    ctx = bpy.data.collections["14_Context_v011"]
    tree_leaf = _leaf_material("VEG_context_tree_foliage", (0.16, 0.25, 0.10), 0.6, "generic deciduous foliage; species unknown")
    far_leaf = _leaf_material("VEG_horizon_tree_foliage", (0.11, 0.17, 0.085), 0.8, "distant woodland; approximate")
    bark = principled("VEG_bark", (0.10, 0.08, 0.065), 0.9)
    near = [_canopy_mesh(f"VEG_tree_canopy_v{v}", f"near{v}", 2400, 7, 0.06) for v in range(3)]
    far = [_canopy_mesh(f"VEG_horizon_canopy_v{v}", f"far{v}", 1100, 8, 0.075) for v in range(4)]
    for me in near:
        me.materials.append(tree_leaf); me.materials.append(core)
    for me in far:
        me.materials.append(far_leaf); me.materials.append(core)
    n_near = n_far = n_trunk = 0
    for obj in ctx.objects:
        if obj.type != "MESH":
            continue
        if obj.name.endswith("_trunk"):
            (lo, hi) = bbox_ft(obj)
            cx, cy, z0, z1 = (lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, lo[2], hi[2]
            bm = bmesh.new()
            bmesh.ops.create_cone(bm, cap_ends=True, segments=10, radius1=0.24 * FT, radius2=0.11 * FT, depth=(z1 - z0 + 1.2) * FT)
            for v in bm.verts:
                v.co += Vector((cx * FT, cy * FT, (z0 + (z1 - z0 + 1.2) / 2) * FT))
            me = bpy.data.meshes.new(obj.name + "_round")
            bm.to_mesh(me)
            bm.free()
            me.materials.append(bark)
            obj.data = me
            n_trunk += 1
        elif obj.name.startswith(("CTX_Street_tree", "CTX_Island_tree")):
            obj.data = near[n_near % len(near)]
            n_near += 1
        elif obj.name.startswith("CTX_Horizon_tree"):
            obj.data = far[n_far % len(far)]
            n_far += 1
    osm_trunk = bpy.data.objects.get("LAND_SANJ_000_trunk")
    if osm_trunk:
        osm_trunk.data.materials.clear()
        osm_trunk.data.materials.append(bark)
    report.update({"context_trees_near": n_near, "context_trees_horizon": n_far, "trunks_rounded": n_trunk})
    # ---- ground surfaces: shader only ----
    for mat in bpy.data.materials:
        if mat.name.startswith(("SITE_lawn", "LAND_lawn", "PRES_backdrop_ground")):
            _ground_breakup(mat, 0.35, 0.18, 0.15, desaturate=0.12)
            _ground_breakup(mat, 28.0, 0.30, 0.55)
        elif mat.name.startswith(("SITE_landscape_bed", "SITE_entrance_bed", "LAND_mulch")):
            _ground_breakup(mat, 55.0, 0.55, 0.9)
    return report


def main():
    global BLEND, REPORT, RENDER_DIR
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    do_render = "--no-render" not in argv
    if "--out" in argv:
        out = Path(argv[argv.index("--out") + 1])
        BLEND, REPORT, RENDER_DIR = out / BLEND.name, out / REPORT.name, out
    views = list(PRESENTATION_VIEWS)                                                  # v010: six presentation views
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
    c_can = collection("04_DropOff_Canopy")
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

    # ---- drop-off canopy: v003, steel elevations from S132 Section 01 ----
    cn = CANOPY
    x0, x1 = cn["cols_x"][0] - cn["end_overhang"], cn["cols_x"][-1] + cn["end_overhang"]
    yg, slope = cn["y_gutter"], cn["slope"]
    src_w = "S132 Section 01 (Approved p.73) written steel elevations; plan A700 Rev5"
    wings = (("north", 1, cn["north"], cn["tos_north_tip"], cn["bos_north_tip"], cn["purlins_north"], cn["purlin_oc_north"]),
             ("south", -1, cn["south"], cn["tos_south_tip"], cn["bos_south_tip"], cn["purlins_south"], cn["purlin_oc_south"]))
    cosb = 1.0 / math.sqrt(1.0 + slope * slope)
    half_col = cn["col_depth_ns"] / 2
    for label, sgn, run, tos_tip, bos_tip, n_purl, oc in wings:
        def tos(d, run=run, tos_tip=tos_tip):          # top of steel at horizontal distance d from XA
            return tos_tip - (run - d) * slope
        # glass
        g0, gt = cn["glass_gap_from_xa"], cn["glass_t"]
        za, zb = tos(g0) + cn["glass_above_tos"], tos(run) + cn["glass_above_tos"]
        ya, yb = yg + sgn * g0, yg + sgn * run
        hexa(f"Canopy_glass_{label}",
             [(x0, ya, za - gt), (x1, ya, za - gt), (x1, yb, zb - gt), (x0, yb, zb - gt)],
             [(x0, ya, za), (x1, ya, za), (x1, yb, zb), (x0, yb, zb)], c_can, canopy_mat,
             "A700 plan + slope + 1\" glass (W); height = S132 top of steel (W) + 1.322 ft measured on S132 (M)")
        # tapered W27x84 beams at each column
        for i, cx in enumerate(cn["cols_x"], 1):
            bw = cn["beam_w"] / 2
            yc, yt = yg + sgn * half_col, yg + sgn * run
            hexa(f"Canopy_beam_X{i}_{label}",
                 [(cx - bw, yc, cn["bos_at_column"]), (cx + bw, yc, cn["bos_at_column"]), (cx + bw, yt, bos_tip), (cx - bw, yt, bos_tip)],
                 [(cx - bw, yc, tos(half_col)), (cx + bw, yc, tos(half_col)), (cx + bw, yt, tos_tip), (cx - bw, yt, tos_tip)],
                 c_can, canopy_mat, src_w)
        # HSS12x6 purlins, perpendicular to the slope, running the full canopy length
        for k in range(n_purl):
            d = run - (cn["purlin_from_tip"] + k * oc) * cosb
            hw, dep = cn["purlin_w"] / 2 * cosb, cn["purlin_d"]
            ya, yb = yg + sgn * (d - hw), yg + sgn * (d + hw)
            hexa(f"Canopy_purlin_{label}_{k}",
                 [(x0, ya, tos(d - hw)), (x1, ya, tos(d - hw)), (x1, yb, tos(d + hw)), (x0, yb, tos(d + hw))],
                 [(x0, ya, tos(d - hw) + dep), (x1, ya, tos(d - hw) + dep), (x1, yb, tos(d + hw) + dep), (x0, yb, tos(d + hw) + dep)],
                 c_can, canopy_mat, "S132 Section 01: HSS12X6X3/8 at 0'-6\" and 5'-0 3/8\" / 5'-0 1/4\" (W); drawn vertical-sided")
    hw_ew = cn["col_width_ew"] / 2
    for i, cx in enumerate(cn["cols_x"], 1):
        box(f"Canopy_column_X{i}", cx - hw_ew, cx + hw_ew, yg - half_col, yg + half_col, AVG_GRADE, cn["col_top"],
            c_can, canopy_mat, "S132 Section 01: W16X100, top of cap plate 15'-1 1/2\" (W); grid XA A700 (G)")

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

    # ---- v006: flat placeholder ground removed; documented site is built after the materials ----

    # ---- lights, world, cameras (same set-up as v001; N/S views widened for the yard) ----
    sun = bpy.data.lights.new("Sun", "SUN")
    sun.energy = 4.0                      # v004: neutral daylight for material review
    sun.angle = math.radians(3)
    sun_obj = bpy.data.objects.new("Sun", sun)
    sun_obj.rotation_euler = (math.radians(55), 0, math.radians(250))
    c_cam.objects.link(sun_obj)
    world = bpy.data.worlds.new("Clay_world")
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.80, 0.87, 1.0, 1)
    bg.inputs[1].default_value = 1.0
    scene.world = world

    cx, cy, cz = 92.0, 58.0, 18.0
    cams = {
        "front_north": (add_camera("Cam_front_north", (cx, 500, cz), (cx, cy, cz), c_cam, 275), (2600, 900)),
        "rear_south": (add_camera("Cam_rear_south", (cx, -400, cz), (cx, cy, cz), c_cam, 275), (2600, 900)),
        "left_east": (add_camera("Cam_left_east", (600, cy + 4, cz), (cx, cy + 4, cz), c_cam, 190), (2400, 1000)),
        "right_west": (add_camera("Cam_right_west", (-400, cy + 4, cz), (cx, cy + 4, cz), c_cam, 190), (2400, 1000)),
        "oblique_northeast": (add_camera("Cam_oblique_NE", (330, 290, 150), (105, 55, 12), c_cam, None, 40.0), (2400, 1350)),
        "landscape_oblique_north": (add_camera("Cam_landscape_oblique_N", (40, 200, 55), (95, 100, 2), c_cam, None, 32.0), (2400, 1350)),
        "site_oblique_northwest": (add_camera("Cam_site_oblique_NW", (-190, 250, 190), (75, 62, -2), c_cam, None, 35.0), (2400, 1350)),
    }
    scene.camera = cams["oblique_northeast"][0]

    # ---- v004: materials and facade-detail overlay (geometry above is untouched) ----
    M = make_materials()
    apply_materials((c_par, c_open, c_can, c_small, c_ss, c_rail, c_yard), masses, M)
    c_fd = collection("11_Facade_Detail_v004")
    detail_count = facade_detail(c_fd, M)
    site_count = build_site(c_site, M, p1_finish)          # v006
    c_pres = collection("13_Presentation_v010")
    cams, refined_materials, sky_type = presentation_v010(scene, c_pres)      # v010: replaces the review cameras for rendering
    c_ctx = collection("14_Context_v011")
    context_count = build_context_v011(c_ctx, *BACKDROP_Z_V010)                # v011
    vegetation_report = vegetation_v012()                                      # v012
    scene.camera = cams["hero_front_north"][0]

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
              "boolean_cuts_applied": cut_count, "facade_detail_objects": detail_count, "site_objects": site_count, "context_objects": context_count, "vegetation_v012": vegetation_report, "refined_materials": refined_materials, "sky_type": sky_type, "landscape_counts": LANDSCAPE_COUNTS,
              "materials": sorted(m_.name for m_ in bpy.data.materials), "openings": len(OPENINGS),
              "objects": {col.name: len(col.objects) for col in bpy.data.collections},
              "mass_faces": {o.name: len(o.data.polygons) for o in masses}}
    assert abs(lo[0] - expected["x_min"]) < 0.01 and abs(hi[0] - expected["x_max"]) < 0.01, "X finish check"
    assert abs(lo[1] - expected["y_min"]) < 0.01 and abs(hi[1] - expected["y_max"]) < 0.01, "Y finish check"
    assert abs(hi[2] - expected["top"]) < 0.01, "top of parapet check"

    bpy.context.preferences.filepaths.save_version = 0   # session only: no .blend1 copies
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))

    if do_render:
        report["gpu"] = setup_gpu(scene)
        scene.cycles.samples = RENDER_SAMPLES_V010
        scene.view_settings.exposure = EXPOSURE_V010
        scene.cycles.use_denoising = True
        scene.render.image_settings.file_format = "PNG"
        try:
            scene.view_settings.view_transform = "AgX"
        except TypeError:
            scene.view_settings.view_transform = "Standard"
        scene.view_settings.look = "None"
        times = {}
        for view, (cam, (rx, ry)) in cams.items():
            if view not in views:
                continue
            scene.camera = cam
            scene.render.resolution_x, scene.render.resolution_y = rx, ry
            scene.render.filepath = str(RENDER_DIR / f"{STEM}_{view}.png")
            t0 = time.time()
            bpy.ops.render.render(write_still=True)
            times[view] = round(time.time() - t0, 1)
        report["render_seconds"] = times
        scene.camera = cams["hero_front_north"][0]
        bpy.ops.wm.save_mainfile()

    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("BUILD_REPORT=" + json.dumps(report))


if __name__ == "__main__":
    main()
