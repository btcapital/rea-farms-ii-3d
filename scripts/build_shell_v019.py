"""Rea Farms II 3D - Building II, v019: MAIN LOBBY CONCEPT A, PASS 1 (architectural) on the frozen v015 model.

Everything = v015, rebuilt by the identical code. v019 only ADDS objects (LOB_A_...) inside
Building_II > INT_LOBBY_CONCEPT_A: wood feature wall, feature-wall lights, stair finish overlays, guard shoes and rails,
coffer, LT-02 track, SH1 pendant cluster, POR-01 floor, walk-off, plinths and banquettes, PT-01 / PT-02 overlays,
directory massing and three lobby cameras. Controlling sources: permit-set ID201 / ID302 / ID303 / ID801, A212, A500,
E003 and permit revision RV-001319-001; concept reference Rea_Farms_2_Lobby.pptx. See notes/lobby_concept_control_v019.md.

--- v015 header follows ---
Rea Farms II 3D - Building II, v015: FIRST TENANT TEST FIT (Concept_A_CNSA_ASC) on the frozen v014 model.

Everything = v014, rebuilt by the identical code. v015 only ADDS tenant objects (TEN_A_...) inside
Building_II > TENANT_CONCEPTS > Concept_A_CNSA_ASC (the empty v014 placeholder "Concept_A" carries the tenant name
in this version). The tenant plan is modeled as drawn: it shows no doors, so none are modeled.
See notes/tenant_testfit_control_v015.md.

--- v014 header follows ---
Rea Farms II 3D - Building II, v014: INTERIOR BASE-BUILDING FRAMEWORK on the frozen v013 model.

Everything = v013, rebuilt by the identical code. v014 only ADDS objects (INT_...) in the collection tree
"Building_II" (BASE_Exterior, BASE_Structure, BASE_Core, BASE_Vertical_Circulation, BASE_Restrooms,
BASE_MEP_Constraints, BASE_Level_1, BASE_Level_2, BASE_Terraces, TENANT_CONCEPTS/Concept_A-C left empty).
Not a tenant upfit. Renders six interior validation views; while they render, the solid exterior masses are
switched off by visibility flags only and switched back on before saving.
See notes/interior_base_control_v014.md.

--- v013 header follows ---
Rea Farms II 3D - Building II, v013: SMALL-SCALE SITE DETAIL PASS on the frozen v012 model.

Everything = v012, rebuilt by the identical code. v013 only ADDS objects, all in collection
"15_Site_Detail_v013" (DET_...): parking striping and hatching, curbs, bollards, light bollards, light
poles, area-drain grates, door hardware and approximate concrete joints. No people, vehicles, signage or
interiors. Building I context mass untouched. See notes/site_detail_control_v013.md.

--- v012 header follows ---
Rea Farms II 3D - Building II, v012: VEGETATION REALISM PASS on the frozen v011 model.

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
  "C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe" --background --python scripts/build_shell_v019.py
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

VERSION = "v019"
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


# ===================== v013 SITE DETAIL (everything above is v012, unchanged) =====================
# Additions only, all in collection "15_Site_Detail_v013", named DET_...  See notes/site_detail_control_v013.md.
# W = written, M = measured from CS-101 rev 6 vector linework, A = approximate.
STALL_LINES_M = [
    (-15.67, 132.35, 1.83, 132.35), (-15.67, 140.85, 1.83, 140.85), (-15.67, 149.35, 1.83, 149.35), (-15.67, 157.85,
    1.83, 157.85), (-15.67, 166.35, 1.83, 166.35), (-15.67, 174.85, 1.83, 174.85), (-15.67, 183.35, 1.83, 183.35),
    (-15.67, 191.85, 1.83, 191.85), (-15.67, 200.35, 1.83, 200.35), (-15.67, 208.85, 1.83, 208.85), (-15.63, 356.28,
    1.87, 356.28), (1.83, 157.85, 1.83, 140.85), (1.83, 284.28, -15.67, 284.28), (1.83, 292.28, -15.67, 292.28),
    (1.83, 300.28, -15.67, 300.28), (1.83, 308.28, -15.67, 308.28), (1.83, 316.28, -15.67, 316.28), (1.83, 324.28,
    -15.67, 324.28), (1.83, 332.28, -15.67, 332.28), (1.83, 340.28, -15.67, 340.28), (1.83, 348.28, -15.67, 348.28),
    (19.13, 400.82, 19.13, 383.28), (25.83, 277.28, 44.33, 277.28), (25.83, 286.28, 44.33, 286.28), (25.83, 295.28,
    44.33, 295.28), (25.83, 304.28, 44.33, 304.28), (25.83, 313.28, 44.33, 313.28), (25.83, 322.28, 44.33, 322.28),
    (25.83, 331.28, 44.33, 331.28), (25.83, 340.28, 44.33, 340.28), (27.13, 400.82, 27.13, 383.28), (35.13, 400.82,
    35.13, 383.28), (43.13, 400.82, 43.13, 383.28), (44.33, 277.28, 62.83, 277.28), (44.33, 286.28, 62.83, 286.28),
    (44.33, 295.28, 62.83, 295.28), (44.33, 304.28, 62.83, 304.28), (44.33, 313.28, 62.83, 313.28), (44.33, 322.28,
    62.83, 322.28), (44.33, 331.28, 62.83, 331.28), (44.33, 340.28, 62.83, 340.28), (51.13, 400.82, 51.13, 383.28),
    (59.17, 400.82, 59.17, 383.28), (67.17, 400.82, 67.17, 383.28), (75.17, 400.82, 75.17, 383.28), (83.17, 400.82,
    83.17, 383.28), (86.83, 277.28, 105.33, 277.28), (86.83, 286.28, 105.33, 286.28), (86.83, 295.28, 105.33, 295.28),
    (86.83, 304.28, 105.33, 304.28), (86.83, 313.28, 105.33, 313.28), (86.83, 322.28, 105.33, 322.28), (86.83, 331.28,
    105.33, 331.28), (86.83, 340.28, 105.33, 340.28), (91.17, 400.82, 91.17, 383.28), (99.17, 400.82, 99.17, 383.28),
    (105.33, 277.28, 123.87, 277.28), (105.33, 286.28, 123.87, 286.28), (105.33, 295.28, 123.87, 295.28), (105.33,
    304.28, 123.87, 304.28), (105.33, 313.28, 123.87, 313.28), (105.33, 322.28, 123.87, 322.28), (105.33, 331.28,
    123.87, 331.28), (105.33, 340.28, 123.87, 340.28), (107.17, 400.82, 107.17, 383.28), (115.17, 400.82, 115.17,
    383.28), (123.17, 400.82, 123.17, 383.28), (131.17, 400.82, 131.17, 383.28), (139.17, 400.82, 139.17, 383.28),
    (147.17, 400.82, 147.17, 383.28), (147.87, 277.28, 166.37, 277.28), (147.87, 286.28, 166.37, 286.28), (147.87,
    295.28, 166.37, 295.28), (147.87, 304.28, 166.37, 304.28), (147.87, 313.28, 166.37, 313.28), (147.87, 322.28,
    166.37, 322.28), (147.87, 331.28, 166.37, 331.28), (147.87, 340.28, 166.37, 340.28), (155.17, 400.82, 155.17,
    383.28), (163.17, 400.82, 163.17, 383.28), (166.37, 277.28, 184.87, 277.28), (166.37, 286.28, 184.87, 286.28),
    (166.37, 295.28, 184.87, 295.28), (166.37, 304.28, 184.87, 304.28), (166.37, 313.28, 184.87, 313.28), (166.37,
    322.28, 184.87, 322.28), (166.37, 331.28, 184.87, 331.28), (166.37, 340.28, 184.87, 340.28), (171.17, 400.82,
    171.17, 383.28), (179.17, 400.82, 179.17, 383.28), (187.17, 400.82, 187.17, 383.28), (195.17, 400.82, 195.17,
    383.28), (203.17, 400.82, 203.17, 383.28), (211.17, 400.82, 211.17, 383.28), (216.87, 146.85, 233.63, 146.85),
    (216.87, 148.35, 233.63, 148.35), (219.17, 400.82, 219.17, 383.28), (226.37, 169.55, 208.87, 169.55), (226.37,
    178.05, 208.87, 178.05), (226.37, 186.55, 208.87, 186.55), (226.37, 195.05, 208.87, 195.05), (226.37, 203.55,
    208.87, 203.55), (226.37, 212.05, 208.87, 212.05), (226.37, 277.28, 208.87, 277.28), (226.37, 286.28, 208.87,
    286.28), (226.37, 295.28, 208.87, 295.28), (226.37, 304.28, 208.87, 304.28), (226.37, 313.28, 208.87, 313.28),
    (226.37, 322.28, 208.87, 322.28), (226.37, 331.28, 208.87, 331.28), (226.37, 340.28, 208.87, 340.28), (227.67,
    387.28, 227.67, 402.32), (279.40, 402.32, 279.40, 387.28), (280.63, 234.78, 296.90, 234.78), (280.63, 236.28,
    296.90, 236.28), (280.90, 277.28, 298.40, 277.28), (280.90, 286.28, 298.40, 286.28), (280.90, 295.28, 298.40,
    295.28), (280.90, 304.28, 298.40, 304.28), (280.90, 313.28, 298.40, 313.28), (280.90, 322.28, 298.40, 322.28),
    (280.90, 331.28, 298.40, 331.28), (280.90, 340.28, 298.40, 340.28), (288.90, 383.28, 288.90, 400.82), (297.90,
    383.28, 297.90, 400.82), (306.90, 383.28, 306.90, 400.82), (309.90, 217.78, 309.90, 235.28), (315.90, 383.28,
    315.90, 400.82), (318.93, 217.78, 318.93, 235.28), (322.40, 277.28, 340.90, 277.28), (322.40, 286.28, 340.90,
    286.28), (322.40, 295.28, 340.90, 295.28), (322.40, 304.28, 340.90, 304.28), (322.40, 313.28, 340.90, 313.28),
    (322.40, 322.28, 340.90, 322.28), (322.40, 331.28, 340.90, 331.28), (322.40, 340.28, 340.90, 340.28), (324.90,
    383.28, 324.90, 400.82), (327.93, 217.78, 327.93, 235.28), (333.90, 383.28, 333.90, 400.82), (336.93, 217.78,
    336.93, 235.28), (340.90, 277.28, 359.40, 277.28), (340.90, 286.28, 359.40, 286.28), (340.90, 295.28, 359.40,
    295.28), (340.90, 304.28, 359.40, 304.28), (340.90, 313.28, 359.40, 313.28), (340.90, 322.28, 359.40, 322.28),
    (340.90, 331.28, 359.40, 331.28), (340.90, 340.28, 359.40, 340.28), (342.90, 383.28, 342.90, 400.82), (345.93,
    217.78, 345.93, 235.28), (351.90, 383.28, 351.90, 400.82), (353.93, 217.78, 353.93, 235.28), (360.90, 383.28,
    360.90, 400.82), (361.93, 217.78, 361.93, 235.28), (369.90, 383.28, 369.90, 400.82), (369.93, 217.78, 369.93,
    235.28), (377.93, 217.78, 377.93, 235.28), (378.90, 383.28, 378.90, 400.82), (382.93, 217.78, 382.93, 235.28),
    (383.40, 277.28, 401.90, 277.28), (383.40, 286.28, 401.90, 286.28), (383.40, 295.28, 401.90, 295.28), (383.40,
    304.28, 401.90, 304.28), (383.40, 313.28, 401.90, 313.28), (383.40, 322.28, 401.90, 322.28), (383.40, 331.28,
    401.90, 331.28), (383.40, 340.28, 401.90, 340.28), (387.90, 383.28, 387.90, 400.82), (391.93, 217.78, 391.93,
    235.28), (396.90, 383.28, 396.90, 400.82), (398.00, 202.75, 414.00, 202.75), (400.93, 217.78, 400.93, 235.28),
    (401.90, 277.28, 420.40, 277.28), (401.90, 286.28, 420.40, 286.28), (401.90, 295.28, 420.40, 295.28), (401.90,
    304.28, 420.40, 304.28), (401.90, 313.28, 420.40, 313.28), (401.90, 322.28, 420.40, 322.28), (401.90, 331.28,
    420.40, 331.28), (401.90, 340.28, 420.40, 340.28), (405.90, 383.28, 405.90, 400.82), (409.93, 217.78, 409.93,
    235.28), (413.93, 201.92, 398.83, 201.92), (413.97, 202.42, 398.33, 202.42), (413.97, 202.45, 398.30, 202.45),
    (414.00, 202.58, 398.17, 202.58), (414.00, 202.65, 398.00, 202.65), (414.00, 202.65, 398.10, 202.65), (414.00,
    202.75, 398.00, 202.75), (414.90, 383.28, 414.90, 400.82), (418.93, 217.78, 418.93, 235.28), (423.90, 383.28,
    423.90, 400.82), (427.93, 217.78, 427.93, 235.28), (428.87, 216.28, 428.87, 200.08), (432.90, 383.28, 432.90,
    400.82), (436.53, 198.75, 451.73, 198.75), (436.93, 217.78, 436.93, 235.28), (441.90, 383.28, 441.90, 400.82),
    (444.40, 277.28, 462.90, 277.28), (444.40, 286.28, 462.90, 286.28), (444.40, 295.28, 462.90, 295.28), (444.40,
    304.28, 462.90, 304.28), (444.40, 313.28, 462.90, 313.28), (444.40, 322.28, 462.90, 322.28), (444.40, 331.28,
    462.90, 331.28), (444.40, 340.28, 462.90, 340.28), (445.93, 217.78, 445.93, 235.28), (450.90, 383.28, 450.90,
    400.82), (454.93, 217.78, 454.93, 235.28), (459.90, 383.28, 459.90, 400.82), (462.90, 277.28, 481.40, 277.28),
    (462.90, 286.28, 481.40, 286.28), (462.90, 295.28, 481.40, 295.28), (462.90, 304.28, 481.40, 304.28), (462.90,
    313.28, 481.40, 313.28), (462.90, 322.28, 481.40, 322.28), (462.90, 331.28, 481.40, 331.28), (462.90, 340.28,
    481.40, 340.28), (463.93, 217.78, 463.93, 235.28), (468.90, 383.28, 468.90, 400.82), (472.93, 217.78, 472.93,
    235.28), (477.90, 383.28, 477.90, 400.82), (481.93, 217.78, 481.93, 235.28), (486.90, 383.28, 486.90, 400.82),
    (490.93, 217.78, 490.93, 235.28), (495.90, 383.28, 495.90, 400.82), (499.93, 217.78, 499.93, 235.28), (503.90,
    400.82, 503.90, 383.28), (505.40, 349.28, 522.90, 349.28), (505.40, 387.28, 505.40, 402.32), (522.90, 277.28,
    505.40, 277.28), (522.90, 286.28, 505.40, 286.28), (522.90, 295.28, 505.40, 295.28), (522.90, 304.28, 505.40,
    304.28), (522.90, 313.28, 505.40, 313.28), (522.90, 322.28, 505.40, 322.28), (522.90, 331.28, 505.40, 331.28),
    (522.90, 340.28, 505.40, 340.28), (522.90, 349.28, 505.40, 349.28), (25.80, 166.30, 62.80, 166.30), (25.80,
    174.80, 62.80, 174.80), (25.80, 183.30, 62.80, 183.30), (25.80, 191.80, 62.80, 191.80), (25.80, 200.30, 62.80,
    200.30), (25.80, 208.80, 62.80, 208.80), (25.80, 217.30, 62.80, 217.30), (86.80, 166.30, 123.90, 166.30), (86.80,
    174.80, 123.90, 174.80), (86.80, 183.30, 123.90, 183.30), (86.80, 191.80, 123.90, 191.80), (86.80, 200.30, 123.90,
    200.30), (86.80, 208.80, 123.90, 208.80), (86.80, 217.30, 123.90, 217.30), (147.90, 166.30, 184.90, 166.30),
    (147.90, 174.80, 184.90, 174.80), (147.90, 183.30, 184.90, 183.30), (147.90, 191.80, 184.90, 191.80), (147.90,
    200.30, 184.90, 200.30), (147.90, 208.80, 184.90, 208.80), (147.90, 217.30, 184.90, 217.30), (44.30, 158.80,
    44.30, 224.80), (105.30, 158.80, 105.30, 224.80), (166.40, 158.80, 166.40, 224.80), (44.30, 269.30, 44.30,
    348.30), (105.30, 269.30, 105.30, 348.30), (166.40, 269.30, 166.40, 348.30), (340.90, 269.30, 340.90, 348.30),
    (401.90, 269.30, 401.90, 348.30)
]
HATCH_LINES_M = [
    (-15.67, 134.35, -9.17, 140.85), (-15.67, 137.88, -12.70, 140.85), (-15.67, 159.08, -8.40, 166.35), (-15.67,
    162.62, -11.97, 166.35), (-15.63, 356.28, -13.03, 358.92), (-14.13, 132.35, -5.63, 140.85), (-13.53, 356.28,
    -10.90, 358.92), (-13.37, 157.85, -4.87, 166.35), (-11.40, 356.28, -8.77, 358.92), (-10.60, 132.35, -2.10,
    140.85), (-9.83, 157.85, -1.33, 166.35), (-9.30, 356.28, -6.67, 358.92), (-7.17, 356.28, -3.87, 359.58), (-7.07,
    132.35, 1.43, 140.85), (-6.30, 157.85, 2.20, 166.35), (-5.03, 356.28, -1.73, 359.58), (-3.53, 132.35, 6.83,
    142.72), (-2.93, 356.28, 0.37, 359.58), (-2.77, 157.85, 5.73, 166.35), (-1.00, 363.95, -5.00, 359.88), (-0.80,
    356.28, 1.87, 358.95), (0.00, 132.35, 6.83, 139.18), (0.77, 157.85, 6.83, 163.92), (1.83, 127.08, 6.83, 132.08),
    (1.83, 130.65, 6.83, 135.65), (1.83, 141.25, 6.83, 146.25), (1.83, 144.78, 6.83, 149.78), (1.83, 148.32, 6.83,
    153.32), (1.83, 151.85, 6.83, 156.85), (1.83, 155.38, 6.83, 160.38), (3.13, 124.85, 6.83, 128.55), (290.70,
    158.55, 300.70, 168.55), (290.70, 162.08, 300.70, 172.08), (290.70, 165.62, 300.70, 175.62), (290.70, 169.15,
    300.70, 179.15), (290.70, 172.68, 298.93, 180.95), (290.70, 176.25, 295.40, 180.95), (291.63, 155.95, 300.70,
    165.02), (295.17, 155.95, 300.70, 161.48), (298.70, 155.95, 300.70, 157.95), (353.93, 218.15, 361.93, 226.15),
    (353.93, 221.68, 361.93, 229.68), (353.93, 225.22, 361.93, 233.22), (353.93, 228.75, 360.47, 235.28), (353.93,
    232.28, 356.93, 235.28), (357.10, 217.78, 361.93, 222.62), (377.93, 218.52, 382.93, 223.52), (377.93, 222.05,
    382.93, 227.05), (377.93, 225.58, 382.93, 230.58), (377.93, 229.12, 382.93, 234.12), (377.93, 232.65, 380.57,
    235.28), (380.73, 217.78, 382.93, 219.98), (505.40, 349.95, 514.40, 358.92), (505.40, 352.05, 512.30, 358.92),
    (505.40, 354.18, 510.83, 359.58), (505.40, 356.28, 508.70, 359.58), (506.90, 349.28, 516.53, 358.92), (509.03,
    349.28, 518.63, 358.92), (511.13, 349.28, 520.77, 358.92), (513.27, 349.28, 522.90, 358.92), (515.40, 349.28,
    522.90, 356.82), (517.50, 349.28, 522.90, 354.72), (519.63, 349.28, 522.90, 352.58), (525.97, 401.28, 532.13,
    395.12), (528.33, 401.02, 531.87, 397.48), (531.07, 394.05, 524.90, 400.25)
]
STRIPE_W = 4.0 / 12                                   # A: 4 in. white, standard practice
STEEL_BOLLARDS_X = [87.4, 93.9, 106.9, 113.4, 126.4, 132.9]      # M; (6) at 6'-6" o.c. (W)
LIGHT_BOLLARDS_X = [80.9, 100.4, 119.9, 139.4]                   # M; (4) Forms+Surfaces light column bollards (W)
BOLLARD_Y = 115.1
LIGHT_POLES = [(4.0, 114.9), (62.0, 114.9), (158.9, 115.2), (194.9, 114.0)]      # M (LP-101 symbols); height A (photo)
AREA_DRAINS = [("AD-213", 32.2, 113.1), ("AD-214", 173.5, 110.4), ("AD-209", -12.2, 52.8), ("AD-208", -16.6, 33.2)]   # A +/-3 ft


def _site_ctrl():
    ctrl = [(x, y, e - FFE) for x, y, e, *_ in SITE_SPOTS]
    for hname, _, verts in HARDSCAPE:
        ctrl += [(x, y, (659.94 if hname == "Transformer_pad" else e) - FFE) for x, y, e in verts]
    return ctrl


def site_detail_v013():
    col = collection("15_Site_Detail_v013")
    ctrl = _site_ctrl()
    zn, zs, ze, zw = BACKDROP_Z_V010
    terrain_y_max = TERRAIN_Y[0] + TERRAIN_CELL * int((TERRAIN_Y[1] - TERRAIN_Y[0]) / TERRAIN_CELL)
    white = principled("DET_pavement_marking_white", (0.78, 0.78, 0.76), 0.75, note="4 in. white striping - colour/width standard practice (A)")
    conc = bpy.data.materials.get("SITE_concrete_flatwork")
    black = principled("DET_black_paint_steel", (0.015, 0.015, 0.016), 0.45, note="CX-101 detail 9: two field coats black (W); light poles black per photo")
    unres = principled("UNRES_light_bollard_finish", (0.5, 0.5, 0.5), 0.5, note="PLACEHOLDER - Forms+Surfaces Series 600 finish not given")
    lens = principled("DET_luminaire_lens", (0.85, 0.85, 0.82), 0.3)
    iron = principled("DET_cast_iron_grate", (0.04, 0.04, 0.045), 0.7)
    steel = principled("DET_door_hardware_stainless", (0.55, 0.55, 0.56), 0.3, metallic=1.0, note="hardware finish per A800 sets not reviewed in detail (A)")
    joint = principled("DET_joint_shadow", (0.03, 0.03, 0.03), 0.9)
    counts = {}

    def ground(x, y):
        if y > terrain_y_max - 0.01 or x > TERRAIN_X[1]:        # outside the modeled terrain: flat context lot
            return zn + 0.04
        return _idw(x, y, ctrl)

    def strip(x0, y0, x1, y1, width, lift, bucket):
        dx, dy = x1 - x0, y1 - y0
        L = math.hypot(dx, dy)
        nx, ny = -dy / L * width / 2, dx / L * width / 2
        seg = max(1, int(L / 6.0))
        verts, faces = [], []
        for k in range(seg + 1):
            t = k / seg
            x, y = x0 + dx * t, y0 + dy * t
            z = ground(x, y) + lift
            verts += [(x + nx, y + ny, z), (x - nx, y - ny, z)]
            if k:
                faces.append((2 * k - 2, 2 * k - 1, 2 * k + 1, 2 * k))
        bucket.append((verts, faces))

    def merge(name, bucket, mat, source):
        verts, faces = [], []
        for v, f in bucket:
            o = len(verts)
            verts += v
            faces += [tuple(i + o for i in face) for face in f]
        mesh_object(name, verts, faces, col, mat, source)

    # ---- striping ----
    b1, b2 = [], []
    for x0, y0, x1, y1 in STALL_LINES_M:
        strip(x0, y0, x1, y1, STRIPE_W, 0.05, b1)
    for x0, y0, x1, y1 in HATCH_LINES_M:
        strip(x0, y0, x1, y1, STRIPE_W, 0.05, b2)
    merge("DET_Striping_stalls", b1, white, "CS-101 rev 6 stall lines (M); 4 in. white (A)")
    merge("DET_Striping_hatch", b2, white, "CS-101 rev 6 hatch lines at accessible aisles / no-parking areas (M); 4 in. white (A)")
    counts["striping_lines"] = len(STALL_LINES_M) + len(HATCH_LINES_M)

    # ---- curbs ----
    for label, xa, xb in (("west", -17.0, 56.8), ("east", 160.0, 189.6)):
        bkt = []
        strip(xa, 123.65, xb, 123.65, 0.5, 0.0, bkt)
        verts, faces = bkt[0]
        n = len(verts)
        tops = [(x, y, _idw(x, 123.2, ctrl)) for x, y, z in verts]         # top of curb = walk level (W: 6 in. above the asphalt)
        verts = [(x, y, z - 0.8) for x, y, z in tops]
        allv = verts + tops
        fcs = [tuple(i + n for i in f) for f in faces]
        for k in range(0, n - 2, 2):
            fcs += [(k, k + 2, k + 2 + n, k + n), (k + 1, k + 1 + n, k + 3 + n, k + 3)]
        mesh_object(f"DET_Curb_walk_{label}", allv, fcs, col, conc, "CX-101 6 in. curb (W); 6 in. wide top, gutter not modeled (A)")
    isl = []
    for k, (xa, xb) in enumerate(ISLANDS, 1):
        zc = _idw((xa + xb) / 2, sum(ISLAND_Y) / 2, ctrl)
        isl.append((f"site_{k}", xa, xb, ISLAND_Y[0], ISLAND_Y[1], zc + CURB_H))
    for yc in ISLAND_ROWS_Y:
        for xc in ISLAND_X:
            isl.append((f"ctx_{int(yc)}_{int(xc)}", xc - 19.5, xc + 19.5, yc - 5.7, yc + 5.7, zn + 0.5))
    for name, xa, xb, ya, yb, ztop in isl:
        c, o = 4.0, 0.5
        poly = [(xa + c, ya - o), (xb - c, ya - o), (xb + o, ya + c), (xb + o, yb - c), (xb - c, yb + o), (xa + c, yb + o),
                (xa - o, yb - c), (xa - o, ya + c)]
        prism(f"DET_Curb_island_{name}", poly, ztop - 1.2, ztop - 0.03, col, conc, "CS-101 island outline (M); 6 in. curb (W), 6 in. wide (A)")
    counts["curbs"] = 2 + len(isl)

    # ---- bollards, light bollards, light poles ----
    def cylinder(name, x, y, z0, z1, r, mat, source, segs=14):
        ring = [(x + r * math.cos(6.283 * k / segs), y + r * math.sin(6.283 * k / segs)) for k in range(segs)]
        return prism(name, ring, z0, z1, col, mat, source)

    for k, x in enumerate(STEEL_BOLLARDS_X, 1):
        z = _idw(x, BOLLARD_Y, ctrl)
        cylinder(f"DET_Bollard_steel_{k}", x, BOLLARD_Y, z - 0.1, z + 3.0, 0.25, black, "CS-101 (6) at 6 ft 6 in. o.c. (W); CX-101 det. 9: 3 ft high, black (W); 6 in. dia (A)")
    for k, x in enumerate(LIGHT_BOLLARDS_X, 1):
        z = _idw(x, BOLLARD_Y, ctrl)
        cylinder(f"DET_Bollard_light_{k}", x, BOLLARD_Y, z - 0.1, z + 3.0, 0.25, unres, "CS-101 (4) Forms+Surfaces light column bollards (W); size A; finish UNRESOLVED")
        cylinder(f"DET_Bollard_light_{k}_lens", x, BOLLARD_Y, z + 3.0, z + 3.3, 0.24, lens, "A")
    for k, (x, y) in enumerate(LIGHT_POLES, 1):
        z = _idw(x, y, ctrl)
        box(f"DET_Light_pole_{k}_base", x - 0.75, x + 0.75, y - 0.75, y + 0.75, z - 0.2, z + 2.5, col, conc, "concrete base, size A (photo)")
        box(f"DET_Light_pole_{k}", x - 0.21, x + 0.21, y - 0.21, y + 0.21, z + 2.5, z + 20.0, col, black, "LP-101 symbol (M); about 20 ft, black (A, 8.29.26 photo)")
        box(f"DET_Light_pole_{k}_luminaire", x - 0.4, x + 0.4, y, y + 2.2, z + 19.6, z + 20.0, col, black, "A")
    counts.update({"steel_bollards": 6, "light_bollards": 4, "light_poles": 4})

    # ---- area drains ----
    for tag, x, y in AREA_DRAINS:
        z = _idw(x, y, ctrl)
        cylinder(f"DET_Area_drain_{tag}", x, y, z - 0.2, z + 0.04, 0.5, iron, "CG-101 rev 6 structure label (W); position +/-3 ft, 12 in. grate (A)", segs=16)
    counts["area_drains"] = len(AREA_DRAINS)

    # ---- door hardware ----
    yg = GY["A.1'"] - GLASS_SETBACK
    for k, x in enumerate((84.87 - 0.22, 84.87 + 0.22), 1):
        box(f"DET_Door_pull_100A_{k}", x - 0.04, x + 0.04, yg + 0.12, yg + 0.30, 3.0, 4.0, col, steel, "door 100A pair, A800 / A815 (W position); 12 in. pull at 42 in. (A)")
    for tag, x0, x1, y0, y1 in (("110B", -EW2 - 0.28, -EW2 - 0.08, 65.05, 65.45), ("102", GX["1.2'"] - EW1 - 0.28, GX["1.2'"] - EW1 - 0.08, 50.05, 50.45),
                                ("104", GX["1.2'"] - EW1 - 0.28, GX["1.2'"] - EW1 - 0.08, 20.05, 20.45)):
        box(f"DET_Door_lever_{tag}", x0, x1, y0, y1, 3.28, 3.38, col, steel, "A800 hardware set; lever shape, side and height A")
    counts["door_hardware"] = 5

    # ---- concrete control joints (A: 5 ft spacing) ----
    jb = []
    for name, _, verts in HARDSCAPE:
        if name not in ("Walk_southwest", "Landing_door_110B", "Landing_west_stair_bottom", "Generator_yard_slab"):
            continue
        xs, ys = [v[0] for v in verts], [v[1] for v in verts]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        poly = [(v[0], v[1]) for v in verts]
        yy = y0 + 5.0
        while yy < y1 - 1.0:
            pts = [x0 + 0.05 * k for k in range(int((x1 - x0) / 0.05) + 1) if _inside((x0 + 0.05 * k, yy), poly)]
            if pts:
                strip(min(pts), yy, max(pts), yy, 0.04, 0.03, jb)
            yy += 5.0
        xx = x0 + 5.0
        while xx < x1 - 1.0:
            pts = [y0 + 0.05 * k for k in range(int((y1 - y0) / 0.05) + 1) if _inside((xx, y0 + 0.05 * k), poly)]
            if pts:
                strip(xx, min(pts), xx, max(pts), 0.04, 0.03, jb)
            xx += 5.0
    merge("DET_Joint_concrete_control_joints_APPROX_5ft", jb, joint, "spacing not written on the sheets reviewed - 5 ft (A)")
    counts["joint_lines"] = len(jb)
    return counts


# ===================== v014 INTERIOR BASE BUILDING (everything above is v013, unchanged) =====================
# Additions only: objects INT_... in the collection tree "Building_II". See notes/interior_base_control_v014.md.
# W = written, G = grid, M = measured from vector linework, A = assumed.
INT_T_IN = (6.0 + 0.625) / 12            # W A003: 6" stud + 5/8" gypsum inside the face of stud
INT_GYP = 0.625 / 12                     # W A003
INT_SLAB_L2 = 6.5 / 12                   # W S102 note 1
INT_SOG = 4.0 / 12                       # W S101 / A191
INT_DECK_UNDERSIDE_L2 = L2_FF - INT_SLAB_L2
INT_TERRACE_UNDERSIDE = TERRACE_FF - INT_SLAB_L2
INT_ROOF_UNDERSIDE = ROOF_STRUCT - 0.25  # W S103 3" deck
INT_RISER = 16.0 / 28                    # W A501: 15 + 13 risers in 16'-0"
INT_TREAD = 11.0 / 12                    # W A500 / A502
INT_DOOR_HEAD = 7.0                      # W A800 (7'-0" doors); used for all interior openings
INT_VIEWS = ("interior_L1_topdown_cutaway", "interior_L2_topdown_cutaway", "interior_L1_oblique_cutaway",
             "interior_L2_oblique_cutaway", "interior_section_looking_north", "interior_eye_level_lobby")
INT_SAMPLES = 160
INT_MODE = dict(zip(INT_VIEWS, ("L1", "L2", "L1", "L2", "section", "eye")))
INT_EXPOSURE = dict(zip(INT_VIEWS, (-0.35, -0.35, -0.35, -0.35, 0.4, 2.2)))      # validation views only; exterior set-up untouched
INT_SECTION_Y = 75.0                     # section plane: through elevator, Stair 1 upper run and the Level 2 lobby

# S600 sizes (W): AISC depth x flange width, inches
INT_SHAPES = {"W10X39": (9.92, 7.99), "W10X45": (10.1, 8.02), "W10X49": (10.0, 10.0), "W10X54": (10.1, 10.0),
              "W10X60": (10.2, 10.1), "W10X68": (10.4, 10.1), "W12X65": (12.1, 12.0), "W12X79": (12.4, 12.1),
              "W14X90": (14.0, 14.5), "HSS12": (12.0, 12.0), "HSS8": (8.0, 8.0), "HSS6": (6.0, 6.0)}
INT_GX = dict(GX, **{"2.8": 27.719})                      # W S102 grid string 21'-8 5/8" + 4'-9 3/8"
INT_GY = dict(GY, **{"E.1": 68.29})                       # M S102 bubble position
# (grid letter, grid number, shape, dx, dy, z0, z1)   z1: "roof", "l2" (under Level 2 slab) or "ter" (under terrace slab)
INT_COLUMNS = [
    ("A", "1", "W10X68", 0, 0, 0, "roof"), ("A", "3", "W10X68", 0, 0, 0, "roof"), ("A", "5", "W10X68", 0, 0, 0, "roof"),
    ("A", "7", "W10X68", 0, 0, 0, "roof"), ("A", "8", "W14X90", 0, 0, 0, "roof"), ("A", "9", "W14X90", 0, 0, 0, "roof"),
    ("A", "6", "HSS6", 0, 1.333, 0, "l2"), ("A", "7", "HSS6", -2.979, 1.333, 0, "l2"),
    ("B", "9.1", "W10X39", 0, 0, 0, "ter"), ("B", "10", "W10X39", 0, 0, 0, "ter"), ("B", "12", "W10X49", 0, 0, 0, "ter"),
    ("C", "1", "W10X49", 0, 0, 0, "roof"), ("D", "10", "HSS12", 0, 0, 0, "roof"),
    ("E", "8", "W10X68", 0, 0, 0, "roof"), ("E", "8.4", "W10X68", 0, 0, 0, "l2"), ("E", "9", "W10X60", 0, 0, 0, "roof"),
    ("E.1", "2.8", "HSS8", 0, 0, 0, "l2"), ("E.4", "12", "W10X49", 0, 0, 0, "ter"),
    ("F", "1", "W10X60", 0, 0, 0, "roof"), ("F", "3", "W12X79", 0, 0, 0, "roof"), ("F", "4", "W12X79", 0, 0, 0, "roof"),
    ("F", "7", "W12X79", 0, 0, 0, "roof"), ("G", "3", "HSS6", -1.75, 0, L2_FF, "roof"),
    ("G", "8", "W10X68", 0, 0, 0, "roof"), ("G", "9", "W10X60", 0, 0, 0, "roof"), ("G", "10", "HSS12", 0, 0, 0, "roof"),
    ("G", "12", "W10X45", 0, 0, 0, "ter"), ("H", "2", "W10X49", 0, 0, 0, "ter"),
    ("H", "3", "W12X65", 0, 0, 0, "roof"), ("H", "5", "W12X65", 0, 0, 0, "roof"), ("H", "7.2", "W12X65", 0, 0, 0, "roof"),
    ("H", "8.3", "W12X65", 0, 0, 0, "roof"), ("H", "9.1", "W12X65", 0, 0, 0, "roof"), ("H", "10", "HSS12", 0, 0, 0, "roof"),
    ("H", "12", "W10X54", 0, 0, 0, "ter"), ("J", "10", "W10X39", 0, 0, 0, "ter"), ("J", "11", "W10X39", 0, 0, 0, "ter"),
    ("K", "2", "W10X39", 0, 0, 0, "ter"), ("K", "3.1", "W10X39", 0, 0, 0, "ter"), ("K", "5", "W10X39", 0, 0, 0, "ter"),
    ("K", "6", "W10X39", 0, 0, 0, "ter"), ("K", "7.2", "W10X39", 0, 0, 0, "ter"), ("K", "8.3", "W10X39", 0, 0, 0, "ter"),
    ("K", "9.1", "W10X49", 0, 0, 0, "ter"),
]

# Lobby "open to below" and Stair 1 void in the Level 2 floor (M A500 Level 2 plan)
INT_LOBBY_WALL_X = 106.54
INT_L2_EDGE_X, INT_L2_EDGE_Y, INT_STAIR1_SOUTH_Y = 124.52, 82.52, 73.44
INT_VOIDS_L2 = [
    [(INT_LOBBY_WALL_X, INT_STAIR1_SOUTH_Y), (INT_L2_EDGE_X, INT_STAIR1_SOUTH_Y), (INT_L2_EDGE_X, GY["A"]), (INT_LOBBY_WALL_X, GY["A"])],
    [(INT_L2_EDGE_X, INT_L2_EDGE_Y), (GX["9'"], INT_L2_EDGE_Y), (GX["9'"], GY["A"]), (INT_L2_EDGE_X, GY["A"])],
    [(136.39, 73.22), (142.45, 73.22), (142.45, 81.95), (136.39, 81.95)],                 # elevator hoistway
    [(100.89, 73.44), (106.24, 73.44), (106.24, 100.6), (100.89, 100.6)],                 # mechanical shaft
    [(136.73, 59.31), (139.9, 59.31), (139.9, 63.99), (136.73, 63.99)],                   # exhaust shaft at restroom
    [(27.19, 59.5), (30.88, 59.5), (30.88, 63.02), (27.19, 63.02)],                       # exhaust shaft at Stair 2
    [(0.0, 59.87), (19.55, 59.87), (19.55, 69.64), (0.0, 69.64)],                         # Stair 2 well
]


def _int_poly_with_recess(poly):
    """Insert the lobby recess (v001 cutter) into a face-of-stud polygon that has the edge 9'-A' -> 8'-A'."""
    r, out = LOBBY_RECESS, []
    for i, p in enumerate(poly):
        q = poly[(i + 1) % len(poly)]
        out.append((p, None))
        if abs(p[1] - GY["A'"]) < 1e-6 and abs(q[1] - GY["A'"]) < 1e-6 and p[0] > q[0]:
            out += [((r["x1"], GY["A'"]), "side"), ((r["x1"], r["y_back"]), "back"), ((r["x0"], r["y_back"]), "side"), ((r["x0"], GY["A'"]), None)]
    return out


def _int_on_boundary(pt, poly, tol=0.02):
    n = len(poly)
    for i in range(n):
        (ax, ay), (bx, by) = poly[i], poly[(i + 1) % n]
        if abs(ax - bx) < 1e-9 and abs(pt[0] - ax) < tol and min(ay, by) - tol <= pt[1] <= max(ay, by) + tol:
            return True
        if abs(ay - by) < 1e-9 and abs(pt[1] - ay) < tol and min(ax, bx) - tol <= pt[0] <= max(ax, bx) + tol:
            return True
    return False


def _int_cells(include, exclude, extra=()):
    """Rectangular cells covering union(include) minus union(exclude); all polygons rectilinear."""
    xs = sorted({round(p[0], 4) for poly in list(include) + list(exclude) for p in poly} | {round(v, 4) for v in extra if v is not None})
    ys = sorted({round(p[1], 4) for poly in list(include) + list(exclude) for p in poly})
    cells = {}
    for i in range(len(xs) - 1):
        for j in range(len(ys) - 1):
            c = ((xs[i] + xs[i + 1]) / 2, (ys[j] + ys[j + 1]) / 2)
            if any(_inside(c, p) for p in include) and not any(_inside(c, p) for p in exclude):
                cells[(i, j)] = (xs[i], xs[i + 1], ys[j], ys[j + 1])
    return cells


def _int_slab(name, cells, z0, z1, col, mat, source, keep=None):
    verts, faces, area = [], [], 0.0
    for (i, j), (x0, x1, y0, y1) in cells.items():
        if keep and not keep((x0 + x1) / 2, (y0 + y1) / 2):
            continue
        area += (x1 - x0) * (y1 - y0)
        o = len(verts)
        verts += [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
        faces += [(o + 3, o + 2, o + 1, o), (o + 4, o + 5, o + 6, o + 7), (o, o + 1, o + 5, o + 4), (o + 1, o + 2, o + 6, o + 5),
                  (o + 2, o + 3, o + 7, o + 6), (o + 3, o, o + 4, o + 7)]
    if not verts:
        return None, 0.0
    return mesh_object(name, verts, faces, col, mat, source), area


def interior_base_v014(scene):
    root = bpy.data.collections.new("Building_II")
    scene.collection.children.link(root)
    C = {}
    for cname in ("BASE_Exterior", "BASE_Structure", "BASE_Core", "BASE_Vertical_Circulation", "BASE_Restrooms",
                  "BASE_MEP_Constraints", "BASE_Level_1", "BASE_Level_2", "BASE_Terraces", "TENANT_CONCEPTS"):
        C[cname] = bpy.data.collections.new(cname)
        root.children.link(C[cname])
    for cname in (list(TENANT_CONCEPTS) + ["Concept_B", "Concept_C"]):        # v015: Concept_A carries the tenant name; B and C stay empty
        C["TENANT_CONCEPTS"].children.link(bpy.data.collections.new(cname))

    gyp = principled("INT_neutral_wall", (0.78, 0.78, 0.77), 0.8, note="neutral - geometry validation only")
    rated = principled("INT_neutral_rated_wall", (0.62, 0.66, 0.74), 0.8, note="neutral tint = fire-rated core wall (A003 .1 types)")
    cmu = principled("INT_neutral_cmu_shaft", (0.50, 0.50, 0.50), 0.9, note="neutral - MA8.1 elevator shaft")
    shaftm = principled("INT_neutral_shaft_wall", (0.70, 0.62, 0.55), 0.8, note="neutral tint = shaft wall (SJ2.1)")
    slabm = principled("INT_neutral_slab", (0.60, 0.60, 0.59), 0.85)
    future = principled("INT_neutral_future_slab_NIC", (0.20, 0.15, 0.10), 0.95, note="S101: future slab on grade not in scope")
    colm = principled("INT_neutral_steel_column", (0.20, 0.22, 0.26), 0.6)
    stairm = principled("INT_neutral_stair", (0.46, 0.46, 0.45), 0.7)
    ceilm = principled("INT_neutral_ceiling", (0.86, 0.86, 0.85), 0.9)
    markm = principled("INT_neutral_marker", (0.75, 0.45, 0.10), 0.8, note="outline of documented but unbuilt room")
    glass = bpy.data.materials.new("INT_neutral_glass")
    glass.use_nodes = True
    nt = glass.node_tree
    for node in list(nt.nodes):
        nt.nodes.remove(node)
    n_out, n_mix = nt.nodes.new("ShaderNodeOutputMaterial"), nt.nodes.new("ShaderNodeMixShader")
    n_tr, n_gl = nt.nodes.new("ShaderNodeBsdfTransparent"), nt.nodes.new("ShaderNodeBsdfGlossy")
    n_tr.inputs["Color"].default_value = (0.90, 0.93, 0.92, 1.0)
    n_gl.inputs["Roughness"].default_value = 0.03
    n_mix.inputs[0].default_value = 0.07
    nt.links.new(n_tr.outputs[0], n_mix.inputs[1])
    nt.links.new(n_gl.outputs[0], n_mix.inputs[2])
    nt.links.new(n_mix.outputs[0], n_out.inputs["Surface"])
    glass.diffuse_color = (0.7, 0.8, 0.85, 0.3)

    counts = {}

    def tag(obj, level, *extra_cols):
        obj["level"] = level
        for cname in extra_cols:
            C[cname].objects.link(obj)
        return obj

    def ibox(name, x0, x1, y0, y1, z0, z1, cname, mat, source, level, *extra):
        obj = box(name, min(x0, x1), max(x0, x1), min(y0, y1), max(y0, y1), z0, z1, C[cname], mat, source)
        counts[cname] = counts.get(cname, 0) + 1
        return tag(obj, level, *extra)

    # ---------------- BASE_Exterior: inside shell from the SAME polygons, build-ups and openings as v013 ----------------
    zone_polys = {k: z["poly"] for k, z in ZONES.items()}
    hm = [(nm, normal, surf, a0, a1, z0, z1) for nm, normal, surf, a0, a1, z0, z1 in HM_DOORS]

    def shell(level, tagname, entries, offsets, z_of_edge):
        """entries: [(vertex, kind)] CCW; offsets per edge; one set of boxes per edge with openings cut out."""
        pts = [e[0] for e in entries]
        n = len(pts)
        for i in range(n):
            p, q = pts[i], pts[(i + 1) % n]
            off = offsets[i]
            if off is None:
                continue
            horiz = abs(p[1] - q[1]) < 1e-9
            nx, ny = edge_normal(p, q, False)
            normal = {(0, 1): "N", (0, -1): "S", (1, 0): "E", (-1, 0): "W"}[(round(nx), round(ny))]
            plane = p[1] if horiz else p[0]
            a_lo, a_hi = sorted((p[0], q[0]) if horiz else (p[1], q[1]))
            # sub-segments that really face outside on this level
            cuts = {a_lo, a_hi}
            if level == 2:
                for poly in zone_polys.values():
                    for v in poly:
                        a = v[0] if horiz else v[1]
                        if a_lo < a < a_hi:
                            cuts.add(a)
            cuts = sorted(cuts)
            for s0, s1 in zip(cuts, cuts[1:]):
                mid = (s0 + s1) / 2
                probe = (mid + nx * 0.3, plane + ny * 0.3) if horiz else (plane + nx * 0.3, mid + ny * 0.3)
                if level == 2 and any(_inside(probe, poly) for poly in zone_polys.values()):
                    continue                                   # internal boundary between roof zones
                z0, z1 = z_of_edge(((mid, plane) if horiz else (plane, mid)))
                # corner extensions: convex corner -> neighbour's outer build-up, reflex corner -> inside lining
                e0 = e1 = 0.0
                for start in (True, False):
                    vert = p if start else q
                    a_, b_, c_ = (pts[i - 1], p, q) if start else (p, q, pts[(i + 2) % n])
                    nb = (i - 1) % n if start else (i + 1) % n
                    cross = (b_[0] - a_[0]) * (c_[1] - b_[1]) - (b_[1] - a_[1]) * (c_[0] - b_[0])
                    ext = (offsets[nb] or 0.0) if cross > 0 else INT_T_IN
                    a_end = vert[0] if horiz else vert[1]
                    if abs(a_end - s0) < 1e-6:
                        e0 = ext
                    elif abs(a_end - s1) < 1e-6:
                        e1 = ext
                lo, hi = s0 - e0, s1 + e1
                # openings on this edge
                ops = []
                for onorm, oplane, a0, a1, oz0, oz1, _bu, otag in OPENINGS:
                    if onorm == normal and abs(oplane - plane) < 0.02 and min(a1, s1) - max(a0, s0) > 0.05 and min(oz1, z1) - max(oz0, z0) > 0.05:
                        ops.append((max(a0, s0), min(a1, s1), max(oz0, z0), min(oz1, z1), otag, True))
                for nm, onorm, surf, a0, a1, oz0, oz1 in hm:
                    fin = plane + off if normal in "NE" else plane - off
                    if onorm == normal and abs(surf - fin) < 0.06 and min(a1, s1) - max(a0, s0) > 0.05 and min(oz1, z1) - max(oz0, z0) > 0.05:
                        ops.append((a0, a1, max(oz0, z0), min(oz1, z1), "HM door " + nm, False))
                us = sorted({lo, hi} | {o[0] for o in ops} | {o[1] for o in ops})
                for u0, u1 in zip(us, us[1:]):
                    um = (u0 + u1) / 2
                    zr = sorted((o[2], o[3]) for o in ops if o[0] <= um <= o[1])
                    solid, z = [], z0
                    for oa, ob in zr:
                        if oa > z + 1e-6:
                            solid.append((z, oa))
                        z = max(z, ob)
                    if z < z1 - 1e-6:
                        solid.append((z, z1))
                    for k, (za, zb) in enumerate(solid):
                        d0, d1 = -INT_T_IN, off
                        if normal in "SW":
                            d0, d1 = -off, INT_T_IN
                        nm_ = f"INT_ExtWall_L{level}_{tagname}_e{i:02d}_{u0:06.2f}_{k}"
                        if horiz:
                            ibox(nm_, u0, u1, plane + d0, plane + d1, za, zb, "BASE_Exterior", gyp, "v013 face-of-stud polygon + A003 build-up (W); 6 in. stud + 5/8 in. gyp inside (W)", level, f"BASE_Level_{level}")
                        else:
                            ibox(nm_, plane + d0, plane + d1, u0, u1, za, zb, "BASE_Exterior", gyp, "v013 face-of-stud polygon + A003 build-up (W); 6 in. stud + 5/8 in. gyp inside (W)", level, f"BASE_Level_{level}")
                for a0, a1, oz0, oz1, otag, glazed in ops:
                    if not glazed:
                        continue
                    g = -0.20 if normal in "NE" else 0.20
                    nm_ = f"INT_Glass_L{level}_{tagname}_e{i:02d}_{a0:06.2f}_{oz0:05.2f}"
                    if horiz:
                        ibox(nm_, a0, a1, plane + g - 0.04, plane + g + 0.04, oz0, oz1, "BASE_Exterior", glass, "same opening as v013: " + otag, level, f"BASE_Level_{level}")
                    else:
                        ibox(nm_, plane + g - 0.04, plane + g + 0.04, a0, a1, oz0, oz1, "BASE_Exterior", glass, "same opening as v013: " + otag, level, f"BASE_Level_{level}")

    # Level 1: P1 with the lobby recess
    ent1 = _int_poly_with_recess(P1)
    # the edge that enters the recess and the edge that leaves it both belong to original edge 12 (9'-A' -> 8'-A')
    off1 = []
    k = 0
    for idx, (pt, kind) in enumerate(ent1):
        if kind in ("side", "back"):
            off1.append(0.0)
            continue
        off1.append(P1_OFFSET[k])
        if ent1[(idx + 1) % len(ent1)][1] != "side":
            k += 1
    L1POLY = [e[0] for e in ent1]

    def z_l1(pt):
        rr = LOBBY_RECESS
        in_recess = rr["y_back"] - 0.02 <= pt[1] <= GY["A'"] + 0.02 and rr["x0"] - 0.02 <= pt[0] <= rr["x1"] + 0.02
        tall = any(_int_on_boundary(pt, poly) for poly in zone_polys.values()) or in_recess
        return (0.0, L2_FF) if tall else (0.0, INT_TERRACE_UNDERSIDE)
    shell(1, "P1", ent1, off1, z_l1)

    for zname, zone in ZONES.items():
        entz = _int_poly_with_recess(zone["poly"]) if zname == "LobbyBlock" else [(p, None) for p in zone["poly"]]
        offz, k = [], 0
        for idx, (pt, kind) in enumerate(entz):
            if kind in ("side", "back"):
                offz.append(0.0)
                continue
            offz.append(zone["offset"][k])
            if entz[(idx + 1) % len(entz)][1] != "side":
                k += 1
        shell(2, zname, entz, offz, lambda pt: (L2_FF, ROOF_STRUCT))
    r = LOBBY_RECESS
    ibox("INT_ExtWall_L2_lobby_head_above_CW1", r["x0"], r["x1"], r["y_back"], GY["A'"] + EW5, CW_HEAD, ROOF_STRUCT, "BASE_Exterior", gyp,
         "v001 recess stops at the CW head 28 ft 10 7/8 in. (W A815)", 2, "BASE_Level_2")

    # roof lid (so interior views have a roof); Level 2 zones at roof structure
    cells_roof = _int_cells(list(zone_polys.values()), [])
    lid, _ = _int_slab("INT_Roof_deck_lid", cells_roof, ROOF_STRUCT - 0.25, ROOF_STRUCT, C["BASE_Exterior"], slabm, "roof structure 32 ft 0 in. (W); 3 in. deck S103 (W)")
    tag(lid, "roof")
    counts["BASE_Exterior"] += 1

    # ---------------- slabs ----------------
    core_l1 = [[(GX["8'"], GY["E"]), (GX["9'"], GY["E"]), (GX["9'"], GY["A"]), (GX["8'"], GY["A"])],          # lobby + elevator (A191)
               [(0.0, GY["F'"]), (27.19, GY["F'"]), (27.19, 70.14), (0.0, 70.14)],                           # Stair 2
               [(GX["1.2'"], 45.14), (18.08, 45.14), (18.08, GY["F'"]), (GX["1.2'"], GY["F'"])],             # Elec. Room 102
               [(GX["1.2'"], 28.71), (10.5, 28.71), (10.5, 45.14), (GX["1.2'"], 45.14)],                     # strip shown on A191 (M, approx.)
               [(GX["1.2'"], 15.5), (18.08, 15.5), (18.08, 28.71), (GX["1.2'"], 28.71)]]                     # Riser Room 104
    extra_x = [v for p in L1POLY for v in (p[0] - 4.0, p[0] + 4.0)]
    cells_l1 = _int_cells_y(L1POLY, None, extra_x + [v[0] for poly in core_l1 for v in poly],
                            [p[1] + d for p in L1POLY for d in (-4.0, 4.0)] + [v[1] for poly in core_l1 for v in poly])

    def near_edge(cx, cy):
        n = len(L1POLY)
        for i in range(n):
            (ax, ay), (bx, by) = L1POLY[i], L1POLY[(i + 1) % n]
            if abs(ax - bx) < 1e-9:
                if min(ay, by) - 1e-6 <= cy <= max(ay, by) + 1e-6 and abs(cx - ax) < 4.0:
                    return True
            elif min(ax, bx) - 1e-6 <= cx <= max(ax, bx) + 1e-6 and abs(cy - ay) < 4.0:
                return True
        return False

    def poured(cx, cy):
        return near_edge(cx, cy) or any(_inside((cx, cy), p) for p in core_l1)
    o1, a_poured = _int_slab("INT_L1_slab_poured_ribbon_and_core", cells_l1, -INT_SOG, 0.0, C["BASE_Level_1"], slabm,
                             "A191 Rev5 / S101: 4 in. slab, 4 ft 0 in. ribbon + lobby, Stair 2, 102, 104 (W; extents M)", keep=poured)
    o2, a_future = _int_slab("INT_L1_slab_FUTURE_not_in_base_scope", cells_l1, -INT_SOG, -0.02, C["BASE_Level_1"], future,
                             "S101 Rev5: FUTURE SLAB ON GRADE NOT IN SCOPE (W)", keep=lambda cx, cy: not poured(cx, cy))
    tag(o1, 1)
    tag(o2, 1)
    counts["BASE_Level_1"] = counts.get("BASE_Level_1", 0) + 2

    cells_l2 = _int_cells(list(zone_polys.values()), INT_VOIDS_L2)
    o3, a_l2 = _int_slab("INT_L2_slab", cells_l2, INT_DECK_UNDERSIDE_L2, L2_FF, C["BASE_Level_2"], slabm,
                         "S102: 3 1/2 in. NW concrete on 3 in. composite deck, 6 1/2 in. total (W); voids M A500/A502/A420")
    tag(o3, 2)
    counts["BASE_Level_2"] = counts.get("BASE_Level_2", 0) + 1
    cells_t = _int_cells([P1], list(zone_polys.values()))
    o4, a_ter = _int_slab("INT_Terrace_slab", cells_t, INT_TERRACE_UNDERSIDE, TERRACE_FF, C["BASE_Terraces"], slabm,
                          "terrace finish floor 15 ft 2 in. (W); 6 1/2 in. composite slab S102/S122 (W)")
    tag(o4, "terrace")
    c = CLOSET
    ibox("INT_Terrace_closet_solid_volume", c["x0"], c["x1"], c["y0"], c["y1"], TERRACE_FF, c["z1"], "BASE_Terraces", gyp,
         "v002 terrace closet volume, interior not modeled", "terrace")
    counts["BASE_Terraces"] = counts.get("BASE_Terraces", 0) + 1

    # ---------------- BASE_Structure: columns ----------------
    for gl, gn, shape, dx, dy, z0, ztop in INT_COLUMNS:
        x, y = INT_GX[gn] + dx, INT_GY[gl] + dy
        d, bf = INT_SHAPES[shape]
        z1 = {"roof": INT_ROOF_UNDERSIDE, "l2": INT_DECK_UNDERSIDE_L2, "ter": INT_TERRACE_UNDERSIDE}[ztop]
        nm_ = f"INT_Column_{gl}-{gn}_{shape}" + ("_offset" if dx or dy else "")
        src_ = f"S600 {shape} (W); grid {gl}-{gn} (G); orientation A"
        pieces = []
        if z0 < L2_FF:
            pieces.append((1, z0, min(z1, INT_DECK_UNDERSIDE_L2)))
        if z1 > L2_FF:
            pieces.append((2, max(z0, L2_FF), z1))
        for lvl, za, zb in pieces:                                             # one object per storey, so a storey can be shown alone
            ibox(f"{nm_}_L{lvl}", x - bf / 24, x + bf / 24, y - d / 24, y + d / 24, za, zb, "BASE_Structure", colm, src_, lvl, f"BASE_Level_{lvl}")
    ibox("INT_Column_G-12_post_HSS6_offset", 204.75 - 0.25, 204.75 + 0.25, GY["G"] - 0.25, GY["G"] + 0.25, TERRACE_FF, LOW_PARAPET_2, "BASE_Structure", colm,
         "S600 G-12(1 ft 3 in.) HSS6X6X3/8 post (W); offset direction and top A", "terrace", "BASE_Terraces")
    ibox("INT_Column_H-11_HSS6_offset", 204.75 - 0.25, 204.75 + 0.25, GY["H"] + 8.25 - 0.25, GY["H"] + 8.25 + 0.25, 0.0, INT_TERRACE_UNDERSIDE, "BASE_Structure", colm,
         "S600 H(8 ft 3 in.)-11(2 ft 9 in.) HSS6X6X3/8 (W); offset direction A", 1, "BASE_Level_1")

    # ---------------- walls with door gaps ----------------
    def wall(name, axis, c0, c1, a0, a1, z0, z1, cname, mat, source, level, gaps=(), skin=INT_GYP):
        """axis 'x': wall runs along x (c = y faces); axis 'y': runs along y (c = x faces). Faces = stud/CMU faces + skin."""
        lvls = [f"BASE_Level_{level}"] if level in (1, 2) else ["BASE_Level_1", "BASE_Level_2"]
        c0, c1 = c0 - skin, c1 + skin
        pieces, a = [], a0
        for g0, g1, head in sorted(gaps):
            if g0 > a:
                pieces.append((a, g0, z0, z1))
            if head is not None and z0 + head < z1:
                pieces.append((g0, g1, z0 + head, z1))
            a = g1
        if a < a1:
            pieces.append((a, a1, z0, z1))
        for k, (p0, p1, za, zb) in enumerate(pieces):
            if axis == "x":
                ibox(f"{name}_{k}", p0, p1, c0, c1, za, zb, cname, mat, source, level, *lvls)
            else:
                ibox(f"{name}_{k}", c0, c1, p0, p1, za, zb, cname, mat, source, level, *lvls)

    H1, H2a, H2b = INT_DECK_UNDERSIDE_L2, L2_FF, INT_ROOF_UNDERSIDE
    A500 = "rated-wall hatch A500 (M), agrees with A112 Rev5 / A122; type A003 (W)"
    # lobby
    wall("INT_Core_L1_lobby_west_SA3.1", "y", 106.24, 106.54, 72.36, GY["A.1'"], 0.0, H1, "BASE_Core", rated, A500, 1, gaps=[(97.56, 101.12, INT_DOOR_HEAD)])
    wall("INT_Core_L1_lobby_south_SA6.1", "x", 72.34, 72.84, 106.55, 135.75, 0.0, H1, "BASE_Core", rated, A500, 1, gaps=[(126.66, 133.2, INT_DOOR_HEAD)])
    wall("INT_Core_L1_lobby_east_SA6.1", "y", 142.5, 143.0, 82.58, 97.84, 0.0, H1, "BASE_Core", rated, A500, 1, gaps=[(88.16, 94.74, INT_DOOR_HEAD)])
    wall("INT_Core_L1_lobby_east_return_SA6.1", "x", 97.34, 97.84, 143.0, GX["9'"], 0.0, H1, "BASE_Core", rated, A500, 1)
    wall("INT_Core_L2_lobby_west_SA3.1", "y", 106.24, 106.54, 64.07, GY["A.1'"], H2a, H2b, "BASE_Core", rated, A500, 2, gaps=[(64.76, 71.4, INT_DOOR_HEAD)])
    wall("INT_Core_L2_lobby_south_SA6.1", "x", 64.06, 64.56, 106.55, 139.91, H2a, H2b, "BASE_Core", rated, A500, 2, gaps=[(126.46, 132.88, INT_DOOR_HEAD)])
    wall("INT_Core_L2_lobby_east_SA6.1", "y", 150.5, 151.0, 55.32, 78.45, H2a, H2b, "BASE_Core", rated, "rated-wall hatch A420 (M); SA6.1 / SA6.1A (W)", 2)
    # Stair 2 enclosure, both levels
    A502 = "rated-wall hatch A502 (M); SA6.1 (W)"
    for lvl, z0, z1, egap, sgap in ((1, 0.0, H1, (60.75, 64.21), None), (2, H2a, H2b, (65.98, 69.64), (21.67, 25.08))):
        wall(f"INT_Stair2_L{lvl}_south_SA6.1", "x", 59.38, 59.87, 0.2, 27.19, z0, z1, "BASE_Vertical_Circulation", rated, A502, lvl,
             gaps=[(sgap[0], sgap[1], INT_DOOR_HEAD)] if sgap else ())
        wall(f"INT_Stair2_L{lvl}_north_SA6.1", "x", 69.64, 70.14, 0.2, 27.19, z0, z1, "BASE_Vertical_Circulation", rated, A502, lvl)
        wall(f"INT_Stair2_L{lvl}_east_SA6.1", "y", 26.69, 27.19, 59.87, 69.64, z0, z1, "BASE_Vertical_Circulation", rated, A502, lvl,
             gaps=[(egap[0], egap[1], INT_DOOR_HEAD)])
    # elevator shaft: CMU, pit to roof
    EL = "MA8.1 7 5/8 in. CMU (W A003); hatch A500 (M); clear 6 ft 0 3/4 in. x 8 ft 8 3/4 in. (W); pit -5 ft 0 in. (W A191)"
    for lvl, za, zb in ((1, -5.0, L2_FF), (2, L2_FF, H2b)):                     # one set per storey
        wall(f"INT_Elevator_shaft_L{lvl}_south", "x", 72.58, 73.22, 135.75, 143.08, za, zb, "BASE_Vertical_Circulation", cmu, EL, lvl, skin=0.0)
        wall(f"INT_Elevator_shaft_L{lvl}_north", "x", 81.95, 82.58, 135.75, 143.08, za, zb, "BASE_Vertical_Circulation", cmu, EL, lvl, skin=0.0)
        wall(f"INT_Elevator_shaft_L{lvl}_east", "y", 142.45, 143.08, 73.22, 81.95, za, zb, "BASE_Vertical_Circulation", cmu, EL, lvl, skin=0.0)
        wall(f"INT_Elevator_shaft_L{lvl}_west", "y", 135.75, 136.39, 73.22, 81.95, za, zb, "BASE_Vertical_Circulation", cmu, EL + "; 3 ft 6 in. door (W), position A", lvl,
             gaps=[(77.6, 81.1, None)], skin=0.0)
        floor = 0.0 if lvl == 1 else L2_FF
        if lvl == 1:
            ibox("INT_Elevator_shaft_L1_west_below_door", 135.75, 136.39, 77.6, 81.1, -5.0, 0.0, "BASE_Vertical_Circulation", cmu, EL, 1, "BASE_Level_1")
        ibox(f"INT_Elevator_shaft_L{lvl}_west_over_door", 135.75, 136.39, 77.6, 81.1, floor + INT_DOOR_HEAD, zb, "BASE_Vertical_Circulation", cmu, EL, lvl, f"BASE_Level_{lvl}")
    ibox("INT_Elevator_pit_floor", 136.39, 142.45, 73.22, 81.95, -5.5, -5.0, "BASE_Vertical_Circulation", slabm, "pit -5 ft 0 in. (W A191)", 1, "BASE_Level_1")

    # ---------------- BASE_MEP_Constraints ----------------
    A112 = "rated-wall hatch A112 Rev5 (M); type A003 (W)"
    wall("INT_MEP_Elec_102_south_SA6.1", "x", 45.14, 45.63, GX["1.2'"], 18.08, 0.0, H1, "BASE_MEP_Constraints", rated, A112 + "; door 103 4 ft 0 in. (W A800)", 1, gaps=[(5.83, 10.18, INT_DOOR_HEAD)])
    wall("INT_MEP_Elec_102_east_SA6.1", "y", 17.59, 18.08, 45.63, 59.38, 0.0, H1, "BASE_MEP_Constraints", rated, A112, 1)
    wall("INT_MEP_Riser_104_south_SA3.1", "x", 15.5, 15.8, GX["1.2'"], 18.08, 0.0, H1, "BASE_MEP_Constraints", rated, A112, 1)
    wall("INT_MEP_Riser_104_north_SA3.1", "x", 28.4, 28.71, GX["1.2'"], 18.08, 0.0, H1, "BASE_MEP_Constraints", rated, A112, 1)
    wall("INT_MEP_Riser_104_east_SA3.1", "y", 17.78, 18.08, 15.8, 28.4, 0.0, H1, "BASE_MEP_Constraints", rated, A112, 1)
    ibox("INT_MEP_Elec_102_ceiling_10ft", GX["1.2'"], 17.59, 45.63, 59.38, 10.0, 10.05, "BASE_MEP_Constraints", ceilm, "A212 Rev5 CA-2 10 ft 0 in. (W)", "lid1", "BASE_Level_1")
    ibox("INT_MEP_Riser_104_ceiling_10ft", GX["1.2'"], 17.78, 15.8, 28.4, 10.0, 10.05, "BASE_MEP_Constraints", ceilm, "A212 Rev5 CA-2 10 ft 0 in. (W)", "lid1", "BASE_Level_1")
    fx0, fx1, fy0, fy1 = GX["1.2'"] + INT_T_IN, GX["1.2'"] + INT_T_IN + 12.583, 28.71 + INT_GYP, 45.14 - INT_GYP
    for k, (x0, x1, y0, y1) in enumerate(((fx0, fx1, fy0, fy0 + 0.15), (fx0, fx1, fy1 - 0.15, fy1), (fx1 - 0.15, fx1, fy0, fy1))):
        ibox(f"INT_MEP_FUTURE_room_103_outline_NOT_BUILT_{k}", x0, x1, y0, y1, 0.0, 0.03, "BASE_MEP_Constraints", markm,
             "A112 Rev5: FUTURE EMERGENCY ELECT. ROOM 103, drawn dashed, 12 ft 7 in. wide (W) - floor outline only", 1, "BASE_Level_1")
    SH = "shaft wall hatch (M) A500 / A420 / A502; SJ2.1 (W)"
    t = 0.13
    wall("INT_MEP_Mech_shaft_west", "y", 100.76, 100.76 + t, 73.31, 100.73, H2a, H2b, "BASE_MEP_Constraints", shaftm, SH, 2, skin=0.0)
    wall("INT_MEP_Mech_shaft_south", "x", 73.31, 73.31 + t, 100.76, 106.24, H2a, H2b, "BASE_MEP_Constraints", shaftm, SH, 2, skin=0.0)
    wall("INT_MEP_Mech_shaft_north", "x", 100.6, 100.6 + t, 100.76, 106.24, H2a, H2b, "BASE_MEP_Constraints", shaftm, SH, 2, skin=0.0)
    for nm_, x0, x1, y0, y1 in (("restroom", 136.61, 140.03, 59.18, 63.99), ("stair2", 27.19, 31.0, 59.37, 63.14)):
        wall(f"INT_MEP_Exhaust_shaft_{nm_}_w", "y", x0, x0 + t, y0, y1, H2a, H2b, "BASE_MEP_Constraints", shaftm, SH, 2, skin=0.0)
        wall(f"INT_MEP_Exhaust_shaft_{nm_}_e", "y", x1 - t, x1, y0, y1, H2a, H2b, "BASE_MEP_Constraints", shaftm, SH, 2, skin=0.0)
        wall(f"INT_MEP_Exhaust_shaft_{nm_}_s", "x", y0, y0 + t, x0, x1, H2a, H2b, "BASE_MEP_Constraints", shaftm, SH, 2, skin=0.0)
        wall(f"INT_MEP_Exhaust_shaft_{nm_}_n", "x", y1 - t, y1, x0, x1, H2a, H2b, "BASE_MEP_Constraints", shaftm, SH, 2, skin=0.0)

    # ---------------- BASE_Restrooms ----------------
    A420 = "A420 enlarged restroom plan: hatch (M), types SA6.1 / SA6.0 (W)"
    wall("INT_Restroom_205_west_SA6.1", "y", 139.14, 139.64, 55.32, 59.18, H2a, H2b, "BASE_Restrooms", rated, A420, 2)
    wall("INT_Restroom_205_south_SA6.1", "x", 55.32, 55.81, 139.14, 150.5, H2a, H2b, "BASE_Restrooms", rated, A420, 2)
    wall("INT_Restroom_205_north_SA6.0", "x", 64.07, 64.57, 139.91, 150.5, H2a, H2b, "BASE_Restrooms", gyp, A420 + "; door 200C 3 ft 6 in. (W A800), position M", 2, gaps=[(146.6, 150.1, INT_DOOR_HEAD)])
    ibox("INT_Restroom_205_ceiling_10ft", 139.64, 150.5, 55.81, 64.07, L2_FF + 10.0, L2_FF + 10.05, "BASE_Restrooms", ceilm, "A212 Rev5 10 ft 0 in. (W)", "lid2", "BASE_Level_2")

    # ---------------- Level 2 lobby ceiling plane ----------------
    zc = L2_FF + 12.0 + 11.375 / 12
    ibox("INT_Ceiling_L2_lobby_CA-1_a", INT_LOBBY_WALL_X, GX["9'"], 64.56, GY["A"], zc, zc + 0.05, "BASE_Level_2", ceilm, "A212 Rev5 CA-1 12 ft 11 3/8 in. AFF (W); feature drop not modeled", "lid2")
    ibox("INT_Ceiling_L2_lobby_CA-1_b", GX["9'"], 150.5, 64.56, 78.45, zc, zc + 0.05, "BASE_Level_2", ceilm, "A212 Rev5 CA-1 (W)", "lid2")
    counts["BASE_Level_2"] += 2

    # ---------------- stairs ----------------
    S1 = "A500 / A501: 15 + 13 risers, 11 in. treads, landing 8 ft 6 7/8 in. (W); positions M"
    x_w, x_e = 107.08, 113.52
    for i in range(1, 15):                                                       # run 1, north -> south
        y_hi = 92.20 - (i - 1) * INT_TREAD
        ibox(f"INT_Stair1_run1_tread_{i:02d}", x_w, 113.02, y_hi - INT_TREAD, y_hi, max(0.0, i * INT_RISER - 0.9), i * INT_RISER, "BASE_Vertical_Circulation", stairm, S1, 1, "BASE_Level_1")
        ibox(f"INT_Stair1_run1_guard_{i:02d}", 113.02, 113.07, y_hi - INT_TREAD, y_hi, i * INT_RISER, i * INT_RISER + 3.5, "BASE_Vertical_Circulation", glass, "glass guardrail 42 in. (W A500 detail); stepped simplification A", 1, "BASE_Level_1")
    zl = 15 * INT_RISER
    ibox("INT_Stair1_landing", x_w, x_e, INT_STAIR1_SOUTH_Y, 79.37, zl - 0.9, zl, "BASE_Vertical_Circulation", stairm, S1, 1, "BASE_Level_1")
    for j in range(1, 13):                                                       # run 2, west -> east
        x_lo = x_e + (j - 1) * INT_TREAD
        zt = (15 + j) * INT_RISER
        ibox(f"INT_Stair1_run2_tread_{j:02d}", x_lo, x_lo + INT_TREAD, INT_STAIR1_SOUTH_Y, 79.37, zt - 0.9, zt, "BASE_Vertical_Circulation", stairm, S1, 1, "BASE_Level_1")
        ibox(f"INT_Stair1_run2_guard_{j:02d}", x_lo, x_lo + INT_TREAD, 79.37, 79.42, zt, zt + 3.5, "BASE_Vertical_Circulation", glass, "glass guardrail (W); stepped simplification A", 1, "BASE_Level_1")
    GR = "shoe glass railing, A500 Level 2 plan (M); 42 in. (W)"
    ibox("INT_Guard_L2_balcony_east_of_stair", INT_L2_EDGE_X, INT_L2_EDGE_X + 0.05, 79.37, INT_L2_EDGE_Y, L2_FF, L2_FF + 3.5, "BASE_Vertical_Circulation", glass, GR, 2, "BASE_Level_2")
    ibox("INT_Guard_L2_balcony_north", INT_L2_EDGE_X, 135.75, INT_L2_EDGE_Y - 0.05, INT_L2_EDGE_Y, L2_FF, L2_FF + 3.5, "BASE_Vertical_Circulation", glass, GR, 2, "BASE_Level_2")
    ibox("INT_Guard_L2_south_of_stair", INT_LOBBY_WALL_X + INT_GYP, INT_L2_EDGE_X, INT_STAIR1_SOUTH_Y - 0.05, INT_STAIR1_SOUTH_Y, L2_FF, L2_FF + 3.5, "BASE_Vertical_Circulation", glass, GR, 2, "BASE_Level_2")
    S2 = "A502: 13 treads at 11 in. per run (W), tread lines M; 28 equal risers and 8 ft 0 in. mid-landing A"
    for i in range(1, 14):                                                       # north run rises westward
        x_hi = 19.55 - (i - 1) * INT_TREAD
        ibox(f"INT_Stair2_runN_tread_{i:02d}", x_hi - INT_TREAD, x_hi, 65.53, 69.35, max(0.0, i * INT_RISER - 0.8), i * INT_RISER, "BASE_Vertical_Circulation", stairm, S2, 1, "BASE_Level_1")
    zm = 14 * INT_RISER
    ibox("INT_Stair2_mid_landing", 0.0 + INT_T_IN, 7.64, 59.87 + INT_GYP, 69.64 - INT_GYP, zm - 0.8, zm, "BASE_Vertical_Circulation", stairm, S2, 1, "BASE_Level_1")
    for j in range(1, 14):                                                       # south run rises eastward
        x_lo = 7.64 + (j - 1) * INT_TREAD
        zt = (14 + j) * INT_RISER
        ibox(f"INT_Stair2_runS_tread_{j:02d}", x_lo, x_lo + INT_TREAD, 60.16, 63.98, zt - 0.8, zt, "BASE_Vertical_Circulation", stairm, S2 + "; south run position mirrored A", 2, "BASE_Level_2")

    # ---------------- tenant areas (report only) ----------------
    core_excl_l1 = [[(106.24, 72.34), (GX["9'"], 72.34), (GX["9'"], GY["A'"]), (106.24, GY["A'"])],
                    [(0.0, 59.38), (27.19, 59.38), (27.19, 70.14), (0.0, 70.14)],
                    [(GX["1.2'"], 45.14), (18.08, 45.14), (18.08, 59.38), (GX["1.2'"], 59.38)],
                    [(GX["1.2'"], 15.5), (18.08, 15.5), (18.08, 28.71), (GX["1.2'"], 28.71)]]
    a1 = sum((c_[1] - c_[0]) * (c_[3] - c_[2]) for c_ in _int_cells([L1POLY], core_excl_l1).values())
    core_excl_l2 = [[(100.76, 64.06), (GX["9'"], 64.06), (GX["9'"], GY["A'"]), (100.76, GY["A'"])],
                    [(GX["9'"], 55.32), (151.0, 55.32), (151.0, L2_NE_Y), (GX["9'"], L2_NE_Y)], [(136.61, 55.32), (GX["9'"], 55.32), (GX["9'"], 64.06), (136.61, 64.06)],
                    [(0.0, GY["F'"]), (31.0, GY["F'"]), (31.0, 70.14), (0.0, 70.14)]]
    a2 = sum((c_[1] - c_[0]) * (c_[3] - c_[2]) for c_ in _int_cells(list(zone_polys.values()), core_excl_l2).values())
    per1 = sum(abs(L1POLY[i][0] - L1POLY[(i + 1) % len(L1POLY)][0]) + abs(L1POLY[i][1] - L1POLY[(i + 1) % len(L1POLY)][1]) for i in range(len(L1POLY)))
    primary = {}
    for o in bpy.data.objects:
        if o.name.startswith("INT_"):
            first = [c.name for c in o.users_collection if not c.name.startswith("BASE_Level")] or [o.users_collection[0].name]
            primary[first[0]] = primary.get(first[0], 0) + 1
    report = {"objects_by_collection": primary, "total_new_objects": sum(primary.values()),
              "level1_slab_poured_sf": round(a_poured), "level1_slab_future_sf": round(a_future), "level2_slab_sf": round(a_l2), "terrace_slab_sf": round(a_ter),
              "level1_tenant_area_face_of_stud_sf": round(a1), "level1_tenant_area_less_exterior_wall_lining_sf": round(a1 - per1 * INT_T_IN),
              "level2_tenant_area_face_of_stud_sf": round(a2), "boma_usable_2025_09_23_sf": {"level1": 18484, "level2": 9918}}
    txt = bpy.data.texts.new("README_v014_view_modes")
    txt.write("v014: the file is saved in EXTERIOR mode (looks like v013). "
              "To look inside: hide collections 01_Masses and 03_Opening_panels, and un-hide the objects in "
              "Building_II > BASE_Exterior and BASE_Terraces (they are hidden only so they do not z-fight with the solid masses). "
              "Nothing in collections 01-15 was edited. Tenant concepts go in Building_II > TENANT_CONCEPTS. v015: Concept_A_CNSA_ASC holds the CNSA ASC test fit; hide or delete that one collection to remove it. Saved eye-level viewpoints are the cameras VP_A_01 ... VP_A_10. v019: Building_II > INT_LOBBY_CONCEPT_A holds the lobby concept (additive overlays only); hide or delete it to remove the concept.")
    return report, C


def _int_cells_y(poly, _unused, extra_x, extra_y):
    xs = sorted({round(p[0], 4) for p in poly} | {round(v, 4) for v in extra_x})
    ys = sorted({round(p[1], 4) for p in poly} | {round(v, 4) for v in extra_y})
    cells = {}
    for i in range(len(xs) - 1):
        for j in range(len(ys) - 1):
            c = ((xs[i] + xs[i + 1]) / 2, (ys[j] + ys[j + 1]) / 2)
            if _inside(c, poly):
                cells[(i, j)] = (xs[i], xs[i + 1], ys[j], ys[j + 1])
    return cells


INT_EXEMPT_COLLECTIONS = ("09_Site_context", "12_Landscape_v008", "13_Presentation_v010", "14_Context_v011", "15_Site_Detail_v013", "10_Cameras_Lights")


INT_ORIG_HIDE = {}                       # flags exactly as the v013 code left them (e.g. the hidden north arrow)


def _int_set_visibility(mode):
    """mode: 'exterior' (v013 look), 'L1', 'L2', 'section', 'eye'. Only render/viewport flags change - never geometry."""
    for obj in bpy.data.objects:
        cols = [c.name for c in obj.users_collection]
        orig = INT_ORIG_HIDE.setdefault(obj.name, (obj.hide_render, obj.hide_viewport))
        if obj.type != "MESH":
            continue
        is_int = obj.name.startswith("INT_")
        hide = False
        if mode == "exterior":
            hide = is_int and ("BASE_Exterior" in cols or "BASE_Terraces" in cols)
        else:
            if "01_Masses" in cols or "03_Opening_panels" in cols:
                hide = True
            lvl = obj.get("level") if is_int else None
            zmin, zmax = bbox_ft(obj)[0][2], bbox_ft(obj)[1][2]
            exempt = any(c in INT_EXEMPT_COLLECTIONS or c.startswith("VEG") for c in cols) or not cols
            if mode == "L1":
                if is_int:
                    hide = hide or lvl not in (1, "all")
                elif not exempt and zmax > 16.2:
                    hide = True
            elif mode == "L2":
                if is_int:
                    hide = hide or lvl in ("roof", "lid2")
                elif not exempt and zmin >= 30.9:
                    hide = True
            elif mode in ("section", "eye"):
                if mode == "section" and ((bbox_ft(obj)[1][1] < INT_SECTION_Y - 0.01 and not exempt) or
                                          any(c in ("12_Landscape_v008", "14_Context_v011", "15_Site_Detail_v013") for c in cols) or not cols):
                    hide = True
        obj.hide_render = hide or orig[0]
        obj.hide_viewport = hide or orig[1]


def interior_cameras_v014(col):
    cams = {
        "interior_L1_topdown_cutaway": (add_camera("Cam_INT_L1_topdown", (100.0, 53.0, 300.0), (100.0, 53.001, 0.0), col, 250), (2400, 1350)),
        "interior_L2_topdown_cutaway": (add_camera("Cam_INT_L2_topdown", (100.0, 53.0, 300.0), (100.0, 53.001, 16.0), col, 250), (2400, 1350)),
        "interior_L1_oblique_cutaway": (add_camera("Cam_INT_L1_oblique", (250.0, 250.0, 200.0), (100.0, 55.0, 0.0), col, None, 40.0), (2400, 1350)),
        "interior_L2_oblique_cutaway": (add_camera("Cam_INT_L2_oblique", (250.0, 250.0, 215.0), (100.0, 55.0, 16.0), col, None, 40.0), (2400, 1350)),
        "interior_section_looking_north": (add_camera("Cam_INT_section_north", (102.0, INT_SECTION_Y - 300.0, 18.0), (102.0, INT_SECTION_Y, 18.0), col, 235), (2600, 900)),
        "interior_eye_level_lobby": (add_camera("Cam_INT_eye_lobby", (139.0, 100.0, 5.5), (112.0, 79.0, 7.5), col, None, 20.0), (2400, 1350)),
    }
    sec = cams["interior_section_looking_north"][0]
    sec.data.clip_start = m(300.0)
    cams["interior_eye_level_lobby"][0].data.clip_start = 0.05
    return cams


# ===================== v015 TENANT CONCEPTS (everything above is v014, unchanged) =====================
# One data dictionary per concept; build_tenant_concept() is generic, so Concept_B / Concept_C / revised plans
# are added by adding a dictionary. See notes/tenant_testfit_control_v015.md.  W = written, M = measured, A = assumed.
TENANT_CONCEPTS = {'Concept_A_CNSA_ASC': {'letter': 'A',
                        'tenant': 'CNSA Rea Farms ASC',
                        'source': 'tenant_testfits/CNSA_ASC/ASC Rea Farms PRESENTATION PLAN v3 20260915.pdf (9-15-2026, 1/8 in. = 1 ft)',
                        'floor': 'Level 1',
                        'printed_asc_sf': 12503,
                        'printed_shell_sf': 5716,
                        'reg_x0_pt': 651.395,
                        'reg_y0_pt': 1571.795,
                        'pt_per_ft': 9.0,
                        'page_w_pt': 3024.0,
                        'page_h_pt': 2160.0,
                        'fitted_scale': 1.0000158,
                        'fitted_rotation_deg': 0.0006,
                        'residual_rms_ft': 0.027,
                        'residual_max_ft': 0.07,
                        'underlay_png': 'exports/tenant_underlay_Concept_A_CNSA_ASC_v015.png',
                        'partition_height_ft': 10.0,
                        'divider_height_ft': 7.0,
                        'divider_thickness_ft': 0.16666666666666666,
                        'demising_thickness_ft': 0.406,
                        'table_height_ft': 3.0,
                        'walls': [[17.783, 43.93, 10.91, 11.32], [122.796, 127.796, 13.5, 13.91], [98.089, 104.956, 13.91, 14.32],
                                  [105.383, 110.383, 13.91, 14.32], [110.383, 128.21, 19.32, 19.74], [44.343, 61.836, 20.91, 21.32],
                                  [62.263, 79.756, 20.91, 21.32], [80.17, 97.676, 22.91, 23.32], [128.21, 143.716, 24.99, 25.4],
                                  [122.796, 127.796, 25.07, 25.5], [98.089, 104.956, 25.58, 25.99], [17.663, 40.876, 33.99, 34.4],
                                  [69.756, 83.756, 33.99, 34.4], [92.583, 104.956, 33.99, 34.4], [49.716, 69.329, 37.83, 38.24],
                                  [105.383, 122.383, 38.5, 38.91], [122.796, 127.796, 38.5, 38.91], [128.21, 138.716, 38.5, 38.91],
                                  [17.663, 41.289, 44.31, 44.72], [49.716, 69.329, 49.4, 49.83], [69.756, 83.756, 49.4, 49.83],
                                  [104.996, 114.596, 49.83, 50.24], [115.023, 138.289, 49.83, 50.24], [92.17, 105.383, 51.4, 51.83],
                                  [104.996, 113.836, 56.74, 57.16], [18.089, 27.329, 57.74, 58.16], [27.756, 40.876, 57.74, 58.16],
                                  [92.583, 104.996, 63.66, 64.07], [105.423, 113.423, 63.66, 64.07], [27.25, 32.17, 64.91, 65.32],
                                  [32.583, 40.876, 64.91, 65.32], [59.21, 67.996, 67.32, 67.74], [68.423, 74.996, 67.32, 67.74],
                                  [27.25, 32.17, 69.78, 70.19], [92.583, 104.583, 71.4, 71.83], [32.583, 40.876, 71.83, 72.24],
                                  [67.996, 83.756, 76.83, 77.24], [0.956, 14.916, 83.12, 83.54], [15.329, 22.73, 83.12, 83.54],
                                  [23.156, 40.876, 83.12, 83.54], [59.21, 67.996, 83.12, 83.54], [68.423, 83.756, 83.12, 83.54],
                                  [49.289, 58.796, 83.16, 83.54], [92.583, 104.996, 84.76, 85.18], [92.583, 104.996, 90.55, 90.98],
                                  [0.956, 14.503, 91.54, 91.96], [14.916, 27.583, 91.54, 91.96], [33.916, 46.583, 91.54, 91.96],
                                  [46.996, 59.663, 91.54, 91.96], [65.996, 78.663, 91.54, 91.96], [27.996, 33.503, 93.54, 93.96],
                                  [60.089, 65.583, 93.54, 93.96], [79.089, 92.17, 95.96, 96.38], [1.42, 1.84, 91.964, 103.964],
                                  [1.84, 2.25, 70.191, 83.124], [7.45, 7.86, 83.537, 91.537], [14.5, 14.92, 91.537, 104.377],
                                  [14.92, 15.33, 69.777, 83.537], [17.66, 18.09, 11.324, 34.164], [17.66, 18.09, 34.404, 44.311],
                                  [17.66, 18.09, 44.657, 57.737], [17.78, 18.2, 0.497, 15.43], [22.73, 23.16, 69.777, 83.537],
                                  [27.33, 27.74, 44.724, 57.737], [27.33, 27.76, 44.724, 57.737], [27.34, 27.74, 44.311, 58.164],
                                  [27.34, 27.76, 44.724, 57.737], [27.58, 28.0, 91.964, 104.377], [32.17, 32.58, 65.324, 69.777],
                                  [32.17, 32.58, 70.191, 71.831], [33.5, 33.92, 91.964, 104.377], [37.5, 37.93, 11.324, 33.991],
                                  [40.88, 41.29, 34.404, 44.311], [40.88, 41.29, 44.724, 57.737], [40.88, 41.29, 65.324, 71.831],
                                  [40.88, 41.29, 72.244, 83.124], [43.93, 44.34, 0.497, 20.91], [46.58, 47.0, 91.537, 104.377],
                                  [49.29, 49.72, 33.991, 37.831], [49.29, 49.72, 38.244, 49.404], [58.8, 59.21, 59.324, 67.324],
                                  [58.8, 59.21, 67.737, 83.124], [58.8, 59.25, 49.831, 59.324], [59.66, 60.09, 91.964, 104.377],
                                  [61.84, 62.26, 0.497, 21.324], [65.58, 66.0, 91.964, 104.377], [68.0, 68.42, 67.324, 83.537],
                                  [69.33, 69.76, 34.404, 49.831], [75.0, 75.42, 67.737, 76.831], [78.66, 79.09, 91.964, 104.377],
                                  [79.76, 80.17, 0.91, 2.497], [79.76, 80.17, 2.91, 22.91], [83.76, 84.17, 34.404, 49.404],
                                  [83.76, 84.17, 49.831, 59.324], [83.76, 84.17, 67.324, 76.831], [83.76, 84.17, 77.244, 83.124],
                                  [92.17, 92.58, 34.404, 51.404], [92.17, 92.58, 51.831, 63.657], [92.17, 92.58, 71.831, 84.764],
                                  [92.17, 92.58, 90.977, 104.377], [94.17, 94.58, 85.177, 90.551], [97.68, 98.09, 0.497, 2.497],
                                  [97.68, 98.09, 2.91, 25.577], [104.96, 105.38, 14.324, 25.577], [104.96, 105.38, 34.404, 51.404],
                                  [105.0, 105.38, 49.831, 51.831], [105.0, 105.42, 50.244, 64.071], [110.38, 110.8, 0.071, 19.324],
                                  [110.38, 110.8, 19.737, 38.497], [113.42, 113.84, 50.244, 56.737], [113.42, 113.84, 57.164, 63.657],
                                  [114.6, 115.02, 38.497, 50.244], [122.38, 122.8, 0.497, 13.497], [122.38, 122.8, 25.497, 38.497],
                                  [127.8, 128.21, 0.497, 13.497], [127.8, 128.21, 13.91, 25.071], [127.8, 128.21, 25.497, 38.497],
                                  [138.29, 138.72, 25.404, 38.497], [138.29, 138.72, 38.91, 49.831], [143.72, 144.13, 0.497, 24.991]],
                        'perimeter_outline_walls': [[5.089, 23.503, -0.05, 0.5], [5.089, 23.503, -0.01, 0.5], [98.089, 110.383, 0.07, 0.5],
                                                    [110.796, 122.383, 0.07, 0.5], [122.796, 127.796, 0.07, 0.5], [128.21, 143.716, 0.07, 0.5],
                                                    [5.503, 17.783, 0.5, 0.91], [18.196, 43.93, 0.5, 0.91], [44.343, 61.836, 0.5, 0.91],
                                                    [62.263, 79.756, 0.5, 0.91], [82.916, 94.089, 1.95, 2.5], [82.876, 94.129, 1.99, 2.5],
                                                    [80.17, 97.676, 2.5, 2.91], [95.236, 99.543, 103.87, 104.32], [99.756, 104.063, 103.87, 104.32],
                                                    [92.583, 104.583, 103.91, 104.32], [1.836, 14.503, 103.96, 104.38],
                                                    [14.916, 27.583, 103.96, 104.38], [27.996, 33.503, 103.96, 104.38],
                                                    [33.916, 46.583, 103.96, 104.38], [46.996, 59.663, 103.96, 104.38],
                                                    [60.089, 65.583, 103.96, 104.38], [65.996, 78.663, 103.96, 104.38],
                                                    [92.17, 94.383, 104.32, 104.91], [92.17, 94.423, 104.32, 104.95], [78.663, 92.17, 104.38, 104.79],
                                                    [0.53, 0.96, 83.537, 91.537], [5.09, 5.5, 0.91, 15.844]],
                        'dividers': [['x', 58.16, 49.289, 58.796], ['x', 66.5, 49.289, 58.796], ['x', 74.83, 49.289, 58.796],
                                     ['y', 67.42, 49.831, 59.324], ['y', 75.58, 49.831, 59.324]],
                        'front_lines': [['y', 49.29, 49.83, 83.2], ['x', 59.32, 59.21, 84.17], ['x', 33.99, 49.289, 64.329],
                                        ['y', 62.76, 59.324, 67.324], ['y', 64.19, 33.991, 37.831]],
                        'demising': ['y', 144.13, 24.991, 72.29],
                        'red_line': [41.29, 92.17, [37.99]],
                        'red_line_spans': [[41.29, 49.29], [84.17, 92.17]],
                        'tables': [['OR_table', 51.596, 54.596, 6.91, 13.91], ['OR_table', 69.503, 72.503, 6.91, 13.91],
                                   ['OR_table', 87.423, 90.423, 8.91, 15.91], ['Procedure_table', 75.25, 78.25, 39.404, 46.404],
                                   ['Procedure_table', 97.289, 100.289, 39.404, 46.404]],
                        'rooms': [{'id': 'A-001',
                                   'name': 'DISCHARGE VESTIBULE',
                                   'cls': 'CIRC',
                                   'printed_sf': 105,
                                   'modeled_sf': 104.7,
                                   'modeled_net_sf': 104.7,
                                   'gross_fill_sf': 122.9,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 78.663,
                                   'y0': 95.964,
                                   'x1': 92.583,
                                   'y1': 104.791},
                                  {'id': 'A-002',
                                   'name': 'PRE/POST',
                                   'cls': 'PREPOST',
                                   'printed_sf': 152,
                                   'modeled_sf': 152.1,
                                   'modeled_net_sf': 152.1,
                                   'gross_fill_sf': 173.3,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 1.423,
                                   'y0': 91.537,
                                   'x1': 14.916,
                                   'y1': 104.377},
                                  {'id': 'A-003',
                                   'name': 'PRE/POST',
                                   'cls': 'PREPOST',
                                   'printed_sf': 152,
                                   'modeled_sf': 152.1,
                                   'modeled_net_sf': 152.1,
                                   'gross_fill_sf': 173.3,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 14.503,
                                   'y0': 91.537,
                                   'x1': 27.996,
                                   'y1': 104.377},
                                  {'id': 'A-004',
                                   'name': 'SHARED TLT',
                                   'cls': 'TOILET_JAN',
                                   'printed_sf': 55,
                                   'modeled_sf': 55.0,
                                   'modeled_net_sf': 55.0,
                                   'gross_fill_sf': 68.6,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 27.583,
                                   'y0': 93.537,
                                   'x1': 33.916,
                                   'y1': 104.377},
                                  {'id': 'A-005',
                                   'name': 'PRE/POST',
                                   'cls': 'PREPOST',
                                   'printed_sf': 152,
                                   'modeled_sf': 152.1,
                                   'modeled_net_sf': 152.1,
                                   'gross_fill_sf': 173.3,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 33.503,
                                   'y0': 91.537,
                                   'x1': 46.996,
                                   'y1': 104.377},
                                  {'id': 'A-006',
                                   'name': 'PRE/POST',
                                   'cls': 'PREPOST',
                                   'printed_sf': 152,
                                   'modeled_sf': 152.1,
                                   'modeled_net_sf': 152.1,
                                   'gross_fill_sf': 173.4,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 46.583,
                                   'y0': 91.537,
                                   'x1': 60.089,
                                   'y1': 104.377},
                                  {'id': 'A-007',
                                   'name': 'SHARED TLT',
                                   'cls': 'TOILET_JAN',
                                   'printed_sf': 55,
                                   'modeled_sf': 54.9,
                                   'modeled_net_sf': 54.9,
                                   'gross_fill_sf': 68.6,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 59.663,
                                   'y0': 93.537,
                                   'x1': 65.996,
                                   'y1': 104.377},
                                  {'id': 'A-008',
                                   'name': 'PRE/POST',
                                   'cls': 'PREPOST',
                                   'printed_sf': 152,
                                   'modeled_sf': 152.3,
                                   'modeled_net_sf': 152.3,
                                   'gross_fill_sf': 173.4,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 65.583,
                                   'y0': 91.537,
                                   'x1': 79.089,
                                   'y1': 104.377},
                                  {'id': 'A-009',
                                   'name': 'PRE/POST',
                                   'cls': 'PREPOST',
                                   'printed_sf': 155,
                                   'modeled_sf': 160.6,
                                   'modeled_net_sf': 160.6,
                                   'gross_fill_sf': 176.7,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 92.17,
                                   'y0': 90.551,
                                   'x1': 104.996,
                                   'y1': 104.324},
                                  {'id': 'A-010',
                                   'name': 'TLT',
                                   'cls': 'TOILET_JAN',
                                   'printed_sf': 52,
                                   'modeled_sf': 52.3,
                                   'modeled_net_sf': 52.3,
                                   'gross_fill_sf': 64.8,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 0.529,
                                   'y0': 83.124,
                                   'x1': 7.863,
                                   'y1': 91.964},
                                  {'id': 'A-011',
                                   'name': 'SHARED TLT',
                                   'cls': 'TOILET_JAN',
                                   'printed_sf': 54,
                                   'modeled_sf': 55.9,
                                   'modeled_net_sf': 55.9,
                                   'gross_fill_sf': 67.3,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 94.17,
                                   'y0': 84.764,
                                   'x1': 104.996,
                                   'y1': 90.977},
                                  {'id': 'A-012',
                                   'name': 'PRE/POST',
                                   'cls': 'PREPOST',
                                   'printed_sf': 155,
                                   'modeled_sf': 161.1,
                                   'modeled_net_sf': 161.1,
                                   'gross_fill_sf': 176.7,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 92.17,
                                   'y0': 71.404,
                                   'x1': 104.996,
                                   'y1': 85.177},
                                  {'id': 'A-013',
                                   'name': 'PRE/POST',
                                   'cls': 'PREPOST',
                                   'printed_sf': 164,
                                   'modeled_sf': 169.3,
                                   'modeled_net_sf': 169.3,
                                   'gross_fill_sf': 185.7,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 1.836,
                                   'y0': 69.777,
                                   'x1': 15.329,
                                   'y1': 83.537},
                                  {'id': 'A-014',
                                   'name': 'MEDS',
                                   'cls': 'SUPPORT',
                                   'printed_sf': 96,
                                   'modeled_sf': 98.8,
                                   'modeled_net_sf': 98.8,
                                   'gross_fill_sf': 113.4,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 14.916,
                                   'y0': 69.777,
                                   'x1': 23.156,
                                   'y1': 83.537},
                                  {'id': 'A-015',
                                   'name': 'NURSE STATION',
                                   'cls': 'NURSE_PROC',
                                   'printed_sf': 216,
                                   'modeled_sf': 230.7,
                                   'modeled_net_sf': 213.1,
                                   'gross_fill_sf': 255.4,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': ['A-022'],
                                   'x0': 22.73,
                                   'y0': 69.777,
                                   'x1': 41.289,
                                   'y1': 83.537},
                                  {'id': 'A-016',
                                   'name': 'CLEAN',
                                   'cls': 'SUPPORT',
                                   'printed_sf': 135,
                                   'modeled_sf': 135.6,
                                   'modeled_net_sf': 135.6,
                                   'gross_fill_sf': 156.1,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 58.796,
                                   'y0': 67.324,
                                   'x1': 68.423,
                                   'y1': 83.537},
                                  {'id': 'A-017',
                                   'name': 'NOURISH',
                                   'cls': 'SUPPORT',
                                   'printed_sf': 90,
                                   'modeled_sf': 90.6,
                                   'modeled_net_sf': 90.6,
                                   'gross_fill_sf': 108.5,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 67.996,
                                   'y0': 76.831,
                                   'x1': 84.17,
                                   'y1': 83.537},
                                  {'id': 'A-018',
                                   'name': 'PACU',
                                   'cls': 'PACU',
                                   'printed_sf': 65,
                                   'modeled_sf': 79.2,
                                   'modeled_net_sf': 79.2,
                                   'gross_fill_sf': 79.2,
                                   'enclosure': 'open bay / alcove (single lines)',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 49.289,
                                   'y0': 74.831,
                                   'x1': 58.796,
                                   'y1': 83.164},
                                  {'id': 'A-019',
                                   'name': 'TLT',
                                   'cls': 'TOILET_JAN',
                                   'printed_sf': 60,
                                   'modeled_sf': 60.1,
                                   'modeled_net_sf': 60.1,
                                   'gross_fill_sf': 73.7,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 67.996,
                                   'y0': 67.324,
                                   'x1': 75.423,
                                   'y1': 77.244},
                                  {'id': 'A-020',
                                   'name': 'PRE/POST',
                                   'cls': 'PREPOST',
                                   'printed_sf': 65,
                                   'modeled_sf': 79.2,
                                   'modeled_net_sf': 79.2,
                                   'gross_fill_sf': 79.2,
                                   'enclosure': 'open bay / alcove (single lines)',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 75.423,
                                   'y0': 67.324,
                                   'x1': 83.756,
                                   'y1': 76.831},
                                  {'id': 'A-021',
                                   'name': 'PACU',
                                   'cls': 'PACU',
                                   'printed_sf': 65,
                                   'modeled_sf': 79.2,
                                   'modeled_net_sf': 79.2,
                                   'gross_fill_sf': 79.2,
                                   'enclosure': 'open bay / alcove (single lines)',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 49.289,
                                   'y0': 66.497,
                                   'x1': 58.796,
                                   'y1': 74.831},
                                  {'id': 'A-022',
                                   'name': 'TLT',
                                   'cls': 'TOILET_JAN',
                                   'printed_sf': 54,
                                   'modeled_sf': 54.9,
                                   'modeled_net_sf': 54.9,
                                   'gross_fill_sf': 66.9,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 32.17,
                                   'y0': 64.91,
                                   'x1': 41.289,
                                   'y1': 72.244},
                                  {'id': 'A-023',
                                   'name': 'WAIT (west arm, same fill colour, no separate label)',
                                   'cls': 'SUPPORT',
                                   'printed_sf': None,
                                   'modeled_sf': 61.7,
                                   'modeled_net_sf': 61.7,
                                   'gross_fill_sf': 61.7,
                                   'enclosure': 'open area',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 105.423,
                                   'y0': 64.071,
                                   'x1': 113.836,
                                   'y1': 71.404},
                                  {'id': 'A-024',
                                   'name': 'WAIT',
                                   'cls': 'SUPPORT',
                                   'printed_sf': 591,
                                   'modeled_sf': 632.2,
                                   'modeled_net_sf': 632.2,
                                   'gross_fill_sf': 632.3,
                                   'enclosure': 'open area',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 113.836,
                                   'y0': 50.244,
                                   'x1': 143.716,
                                   'y1': 71.404},
                                  {'id': 'A-025',
                                   'name': 'JAN',
                                   'cls': 'TOILET_JAN',
                                   'printed_sf': 22,
                                   'modeled_sf': 24.6,
                                   'modeled_net_sf': 24.6,
                                   'gross_fill_sf': 30.4,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 26.823,
                                   'y0': 64.91,
                                   'x1': 32.583,
                                   'y1': 70.191},
                                  {'id': 'A-026',
                                   'name': 'NURSE',
                                   'cls': 'NURSE_PROC',
                                   'printed_sf': 19,
                                   'modeled_sf': 28.4,
                                   'modeled_net_sf': 28.4,
                                   'gross_fill_sf': 28.4,
                                   'enclosure': 'open bay / alcove (single lines)',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 59.21,
                                   'y0': 59.324,
                                   'x1': 62.756,
                                   'y1': 67.324},
                                  {'id': 'A-027',
                                   'name': 'PACU',
                                   'cls': 'PACU',
                                   'printed_sf': 65,
                                   'modeled_sf': 79.2,
                                   'modeled_net_sf': 79.2,
                                   'gross_fill_sf': 79.2,
                                   'enclosure': 'open bay / alcove (single lines)',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 49.289,
                                   'y0': 58.164,
                                   'x1': 58.796,
                                   'y1': 66.497},
                                  {'id': 'A-028',
                                   'name': 'OFFICE',
                                   'cls': 'SUPPORT',
                                   'printed_sf': 147,
                                   'modeled_sf': 147.1,
                                   'modeled_net_sf': 147.1,
                                   'gross_fill_sf': 167.9,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 92.17,
                                   'y0': 51.404,
                                   'x1': 105.423,
                                   'y1': 64.071},
                                  {'id': 'A-029',
                                   'name': 'TLT',
                                   'cls': 'TOILET_JAN',
                                   'printed_sf': 52,
                                   'modeled_sf': 52.2,
                                   'modeled_net_sf': 52.2,
                                   'gross_fill_sf': 64.8,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 104.996,
                                   'y0': 56.737,
                                   'x1': 113.836,
                                   'y1': 64.071},
                                  {'id': 'A-030',
                                   'name': 'PRE/POST',
                                   'cls': 'PREPOST',
                                   'printed_sf': 64,
                                   'modeled_sf': 77.6,
                                   'modeled_net_sf': 77.6,
                                   'gross_fill_sf': 77.6,
                                   'enclosure': 'open bay / alcove (single lines)',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 59.25,
                                   'y0': 49.831,
                                   'x1': 67.423,
                                   'y1': 59.324},
                                  {'id': 'A-031',
                                   'name': 'PRE/POST',
                                   'cls': 'PREPOST',
                                   'printed_sf': 64,
                                   'modeled_sf': 77.5,
                                   'modeled_net_sf': 77.5,
                                   'gross_fill_sf': 77.5,
                                   'enclosure': 'open bay / alcove (single lines)',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 67.423,
                                   'y0': 49.831,
                                   'x1': 75.583,
                                   'y1': 59.324},
                                  {'id': 'A-032',
                                   'name': 'PRE/POST',
                                   'cls': 'PREPOST',
                                   'printed_sf': 64,
                                   'modeled_sf': 77.6,
                                   'modeled_net_sf': 77.6,
                                   'gross_fill_sf': 77.6,
                                   'enclosure': 'open bay / alcove (single lines)',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 75.583,
                                   'y0': 49.831,
                                   'x1': 83.756,
                                   'y1': 59.324},
                                  {'id': 'A-033',
                                   'name': 'MED GAS',
                                   'cls': 'MEP',
                                   'printed_sf': 120,
                                   'modeled_sf': 120.5,
                                   'modeled_net_sf': 126.1,
                                   'gross_fill_sf': 139.6,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 17.663,
                                   'y0': 44.311,
                                   'x1': 27.743,
                                   'y1': 58.164},
                                  {'id': 'A-034',
                                   'name': 'BREAK DOWN',
                                   'cls': 'STERILE',
                                   'printed_sf': 171,
                                   'modeled_sf': 171.1,
                                   'modeled_net_sf': 171.1,
                                   'gross_fill_sf': 193.2,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 27.343,
                                   'y0': 44.311,
                                   'x1': 41.289,
                                   'y1': 58.164},
                                  {'id': 'A-035',
                                   'name': 'PACU',
                                   'cls': 'PACU',
                                   'printed_sf': 65,
                                   'modeled_sf': 79.2,
                                   'modeled_net_sf': 79.2,
                                   'gross_fill_sf': 79.2,
                                   'enclosure': 'open bay / alcove (single lines)',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 49.289,
                                   'y0': 49.831,
                                   'x1': 58.796,
                                   'y1': 58.164},
                                  {'id': 'A-036',
                                   'name': 'TLT',
                                   'cls': 'TOILET_JAN',
                                   'printed_sf': 52,
                                   'modeled_sf': 52.1,
                                   'modeled_net_sf': 52.1,
                                   'gross_fill_sf': 64.8,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 104.996,
                                   'y0': 49.831,
                                   'x1': 113.836,
                                   'y1': 57.164},
                                  {'id': 'A-037',
                                   'name': 'PROCEDURE',
                                   'cls': 'NURSE_PROC',
                                   'printed_sf': 210,
                                   'modeled_sf': 210.9,
                                   'modeled_net_sf': 210.9,
                                   'gross_fill_sf': 235.7,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 92.17,
                                   'y0': 33.991,
                                   'x1': 105.383,
                                   'y1': 51.831},
                                  {'id': 'A-038',
                                   'name': 'ANESTHESIA OFFICE',
                                   'cls': 'SUPPORT',
                                   'printed_sf': 101,
                                   'modeled_sf': 100.8,
                                   'modeled_net_sf': 100.8,
                                   'gross_fill_sf': 118.3,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 104.956,
                                   'y0': 38.497,
                                   'x1': 115.023,
                                   'y1': 50.244},
                                  {'id': 'A-039',
                                   'name': 'RECEPTION',
                                   'cls': 'SUPPORT',
                                   'printed_sf': 254,
                                   'modeled_sf': 254.8,
                                   'modeled_net_sf': 254.8,
                                   'gross_fill_sf': 283.3,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 114.596,
                                   'y0': 38.497,
                                   'x1': 138.716,
                                   'y1': 50.244},
                                  {'id': 'A-040',
                                   'name': 'SOILED',
                                   'cls': 'SUPPORT',
                                   'printed_sf': 219,
                                   'modeled_sf': 219.2,
                                   'modeled_net_sf': 219.2,
                                   'gross_fill_sf': 245.6,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 49.289,
                                   'y0': 37.831,
                                   'x1': 69.756,
                                   'y1': 49.831},
                                  {'id': 'A-041',
                                   'name': 'PROCEDURE',
                                   'cls': 'NURSE_PROC',
                                   'printed_sf': 210,
                                   'modeled_sf': 210.6,
                                   'modeled_net_sf': 210.6,
                                   'gross_fill_sf': 235.1,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 69.329,
                                   'y0': 33.991,
                                   'x1': 84.17,
                                   'y1': 49.831},
                                  {'id': 'A-042',
                                   'name': 'DECONTAM',
                                   'cls': 'STERILE',
                                   'printed_sf': 226,
                                   'modeled_sf': 226.1,
                                   'modeled_net_sf': 230.3,
                                   'gross_fill_sf': 253.6,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 17.663,
                                   'y0': 33.991,
                                   'x1': 41.289,
                                   'y1': 44.724},
                                  {'id': 'A-043',
                                   'name': 'LOCKER',
                                   'cls': 'SUPPORT',
                                   'printed_sf': 319,
                                   'modeled_sf': 311.8,
                                   'modeled_net_sf': 246.1,
                                   'gross_fill_sf': 349.2,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': ['A-044'],
                                   'x0': 110.383,
                                   'y0': 19.324,
                                   'x1': 128.21,
                                   'y1': 38.91},
                                  {'id': 'A-044',
                                   'name': 'TLT',
                                   'cls': 'TOILET_JAN',
                                   'printed_sf': 65,
                                   'modeled_sf': 65.7,
                                   'modeled_net_sf': 65.7,
                                   'gross_fill_sf': 80.6,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 122.383,
                                   'y0': 25.071,
                                   'x1': 128.21,
                                   'y1': 38.91},
                                  {'id': 'A-045',
                                   'name': 'OFFICE',
                                   'cls': 'SUPPORT',
                                   'printed_sf': 132,
                                   'modeled_sf': 132.5,
                                   'modeled_net_sf': 132.5,
                                   'gross_fill_sf': 152.0,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 127.796,
                                   'y0': 24.991,
                                   'x1': 138.716,
                                   'y1': 38.91},
                                  {'id': 'A-046',
                                   'name': 'CONTROL',
                                   'cls': 'SUPPORT',
                                   'printed_sf': 41,
                                   'modeled_sf': 55.0,
                                   'modeled_net_sf': 55.0,
                                   'gross_fill_sf': 55.0,
                                   'enclosure': 'open bay / alcove (single lines)',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 49.716,
                                   'y0': 33.991,
                                   'x1': 64.049,
                                   'y1': 37.831},
                                  {'id': 'A-047',
                                   'name': 'STERILE PROCESSING',
                                   'cls': 'STERILE',
                                   'printed_sf': 440,
                                   'modeled_sf': 439.7,
                                   'modeled_net_sf': 448.1,
                                   'gross_fill_sf': 476.2,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 17.663,
                                   'y0': 10.91,
                                   'x1': 37.93,
                                   'y1': 34.404},
                                  {'id': 'A-048',
                                   'name': 'JAN',
                                   'cls': 'TOILET_JAN',
                                   'printed_sf': 77,
                                   'modeled_sf': 78.0,
                                   'modeled_net_sf': 78.0,
                                   'gross_fill_sf': 93.1,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 97.676,
                                   'y0': 13.91,
                                   'x1': 105.383,
                                   'y1': 25.991},
                                  {'id': 'A-049',
                                   'name': 'LOUNGE',
                                   'cls': 'SUPPORT',
                                   'printed_sf': 380,
                                   'modeled_sf': 380.8,
                                   'modeled_net_sf': 380.8,
                                   'gross_fill_sf': 413.8,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 127.796,
                                   'y0': 0.071,
                                   'x1': 144.129,
                                   'y1': 25.404},
                                  {'id': 'A-050',
                                   'name': 'OR',
                                   'cls': 'OR',
                                   'printed_sf': 350,
                                   'modeled_sf': 350.9,
                                   'modeled_net_sf': 350.9,
                                   'gross_fill_sf': 381.8,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 79.756,
                                   'y0': 2.497,
                                   'x1': 98.089,
                                   'y1': 23.324},
                                  {'id': 'A-051',
                                   'name': 'OR',
                                   'cls': 'OR',
                                   'printed_sf': 350,
                                   'modeled_sf': 350.4,
                                   'modeled_net_sf': 350.4,
                                   'gross_fill_sf': 381.8,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 43.93,
                                   'y0': 0.497,
                                   'x1': 62.263,
                                   'y1': 21.324},
                                  {'id': 'A-052',
                                   'name': 'OR',
                                   'cls': 'OR',
                                   'printed_sf': 350,
                                   'modeled_sf': 350.6,
                                   'modeled_net_sf': 350.6,
                                   'gross_fill_sf': 381.8,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 61.836,
                                   'y0': 0.497,
                                   'x1': 80.17,
                                   'y1': 21.324},
                                  {'id': 'A-053',
                                   'name': 'LOCKER',
                                   'cls': 'SUPPORT',
                                   'printed_sf': 320,
                                   'modeled_sf': 313.0,
                                   'modeled_net_sf': 247.3,
                                   'gross_fill_sf': 350.6,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': ['A-056'],
                                   'x0': 110.383,
                                   'y0': 0.071,
                                   'x1': 128.21,
                                   'y1': 19.737},
                                  {'id': 'A-054',
                                   'name': 'MECH. PUMP',
                                   'cls': 'MEP',
                                   'printed_sf': 178,
                                   'modeled_sf': 183.1,
                                   'modeled_net_sf': 183.7,
                                   'gross_fill_sf': 201.2,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 5.089,
                                   'y0': 0.497,
                                   'x1': 18.196,
                                   'y1': 15.844},
                                  {'id': 'A-055',
                                   'name': 'CLEAN',
                                   'cls': 'SUPPORT',
                                   'printed_sf': 165,
                                   'modeled_sf': 165.4,
                                   'modeled_net_sf': 165.4,
                                   'gross_fill_sf': 187.0,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 97.676,
                                   'y0': 0.071,
                                   'x1': 110.796,
                                   'y1': 14.324},
                                  {'id': 'A-056',
                                   'name': 'TLT',
                                   'cls': 'TOILET_JAN',
                                   'printed_sf': 65,
                                   'modeled_sf': 65.7,
                                   'modeled_net_sf': 65.7,
                                   'gross_fill_sf': 80.6,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 122.383,
                                   'y0': 0.071,
                                   'x1': 128.21,
                                   'y1': 13.91},
                                  {'id': 'A-057',
                                   'name': 'STERILE INSTRUMENTS',
                                   'cls': 'STERILE',
                                   'printed_sf': 257,
                                   'modeled_sf': 257.5,
                                   'modeled_net_sf': 257.5,
                                   'gross_fill_sf': 287.6,
                                   'enclosure': 'walled (double lines), no door drawn',
                                   'overlapping_smaller_rooms': [],
                                   'x0': 17.783,
                                   'y0': 0.497,
                                   'x1': 44.343,
                                   'y1': 11.324}],
                        'circ': [{'x0': 79.089, 'y0': 91.537, 'x1': 92.17, 'y1': 95.964}, {'x0': 27.996, 'y0': 91.537, 'x1': 33.503, 'y1': 93.537},
                                 {'x0': 60.089, 'y0': 91.537, 'x1': 65.583, 'y1': 93.537}, {'x0': 7.863, 'y0': 83.537, 'x1': 92.17, 'y1': 91.537},
                                 {'x0': 92.17, 'y0': 85.177, 'x1': 94.17, 'y1': 90.551}, {'x0': 41.289, 'y0': 33.991, 'x1': 49.289, 'y1': 83.537},
                                 {'x0': 84.17, 'y0': 33.991, 'x1': 92.17, 'y1': 83.537}, {'x0': 92.17, 'y0': 64.071, 'x1': 105.423, 'y1': 71.404},
                                 {'x0': 62.756, 'y0': 59.324, 'x1': 84.17, 'y1': 67.324}, {'x0': 27.25, 'y0': 58.164, 'x1': 41.289, 'y1': 64.91},
                                 {'x0': 138.716, 'y0': 25.404, 'x1': 143.716, 'y1': 50.244},
                                 {'x0': 105.383, 'y0': 33.991, 'x1': 110.383, 'y1': 38.497}, {'x0': 64.329, 'y0': 33.991, 'x1': 69.329, 'y1': 37.831},
                                 {'x0': 37.93, 'y0': 25.991, 'x1': 110.383, 'y1': 33.991}, {'x0': 37.93, 'y0': 11.324, 'x1': 43.93, 'y1': 25.991},
                                 {'x0': 43.93, 'y0': 21.324, 'x1': 79.756, 'y1': 25.991}, {'x0': 79.756, 'y0': 23.324, 'x1': 97.676, 'y1': 25.991},
                                 {'x0': 105.383, 'y0': 14.324, 'x1': 110.383, 'y1': 25.991}],
                        'review_lights': [[53.0, 52.5, 102.0, 101.0], [125.0, 36.5, 38.0, 70.0]],
                        'review_light_w_per_sf': 0.07,
                        'viewpoints': [['01_ASC_entrance_arrival', 'ASC entrance / arrival (Lobby 101 looking through door 101C into WAIT)',
                                        [133.5, 91.0], [129.9, 64.0, 4.5], 22.0],
                                       ['02_reception', 'Reception and toilets seen from the north-east corner of WAIT', [141.5, 69.8],
                                        [113.0, 47.0, 4.5], 18.0],
                                       ['03_waiting', 'Waiting', [116.5, 52.5], [140.0, 69.0, 5.0], 18.0],
                                       ['04_main_clinical_circulation', 'Main clinical corridor looking east', [10.0, 87.5], [90.0, 87.5, 5.0], 20.0],
                                       ['05_nurse_station', 'Nurse station (inside)', [39.5, 74.0], [25.0, 82.0, 5.0], 16.0],
                                       ['06_pre_post_room', 'Representative pre/post room A-002', [13.6, 92.8], [3.0, 104.0, 4.5], 16.0],
                                       ['07_procedure_room_approach', 'Procedure-room approach looking south', [88.2, 62.0], [88.2, 34.0, 5.0], 20.0],
                                       ['08_operating_room', 'Representative OR A-051', [45.2, 19.8], [55.0, 8.0, 3.5], 16.0],
                                       ['09_sterile_processing', 'Sterile processing', [36.6, 33.0], [24.0, 16.0, 4.0], 16.0],
                                       ['10_staff_lounge', 'Staff / support: lounge', [142.5, 23.8], [131.0, 4.0, 4.5], 16.0]]}}


TEN_VIEWS = ("tenant_A_01_registration_overlay", "tenant_A_02_L1_topdown_plan", "tenant_A_03_L1_oblique_cutaway", "tenant_A_04_fp_ASC_entrance",
             "tenant_A_05_fp_reception_waiting", "tenant_A_06_fp_main_clinical_corridor", "tenant_A_07_fp_pre_post_room",
             "tenant_A_08_fp_operating_room", "tenant_A_09_fp_sterile_processing")
TEN_SAMPLES = 160
TEN_FP_EXPOSURE = 0.8
TEN_PLAN_EXPOSURE = 1.4                  # overlay and plan views are lit by the sky only (sun off) so the tints and the underlay read
TEN_CLASS_TINT = {"CIRC": (0.62, 0.60, 0.58), "PREPOST": (0.70, 0.73, 0.78), "TOILET_JAN": (0.80, 0.66, 0.68), "SUPPORT": (0.74, 0.74, 0.84),
                  "PACU": (0.52, 0.66, 0.78), "STERILE": (0.50, 0.72, 0.68), "NURSE_PROC": (0.70, 0.64, 0.70), "OR": (0.80, 0.68, 0.50),
                  "MEP": (0.72, 0.58, 0.58)}


def build_tenant_concept(cid, data, parent):
    """Generic tenant-concept builder. Everything it creates lives in the collection `cid` (or its sub-collections),
    so hiding or deleting that one collection removes the concept. `data` is a plain dictionary (see TENANT_CONCEPTS)."""
    letter = data["letter"]
    pre = f"TEN_{letter}_"
    col = bpy.data.collections.get(cid)
    if col is None:
        col = bpy.data.collections.new(cid)
        parent.children.link(col)
    sub = {}
    for sname in ("rooms", "labels", "viewpoints", "underlay", "review_lighting", "ambiguous_perimeter_outline_walls"):
        sub[sname] = bpy.data.collections.new(f"{cid}_{sname}")
        col.children.link(sub[sname])
    H = data["partition_height_ft"]
    wallm = principled(f"{pre}neutral_partition", (0.80, 0.80, 0.79), 0.8, note=f"tenant partition as drawn; height {H} ft ASSUMED")
    divm = principled(f"{pre}UNRES_bay_divider_type_unknown", (0.62, 0.70, 0.74), 0.7, note="single line on the tenant plan: curtain or partition not determinable")
    demm = principled(f"{pre}neutral_demising", (0.70, 0.70, 0.66), 0.8, note="single heavy line on the tenant plan; thickness and height ASSUMED")
    eqm = principled(f"{pre}neutral_equipment_proxy", (0.35, 0.37, 0.40), 0.6)
    redm = principled(f"{pre}marker_red_line", (0.75, 0.05, 0.05), 0.7, note="'RED LINE' drawn on the tenant plan")
    linem = principled(f"{pre}marker_open_front", (0.25, 0.25, 0.25), 0.8, note="single line at an open bay / alcove front")
    textm = principled(f"{pre}label_text", (0.05, 0.05, 0.06), 0.9)
    tints = {k: principled(f"{pre}neutral_floor_{k}", v, 0.85, note="neutral tint = room colour group on the tenant plan") for k, v in TEN_CLASS_TINT.items()}

    def put(obj, **props):
        obj["concept"] = cid
        for k, v in props.items():
            obj[k] = v
        return obj

    n = {"perimeter_outline_walls_hidden": 0, "partitions": 0, "dividers": 0, "markers": 0, "equipment": 0, "room_plates": 0, "circulation_plates": 0, "labels": 0}
    src = data["source"]
    for i, (x0, x1, y0, y1) in enumerate(data["walls"], 1):
        put(box(f"{pre}Partition_{i:03d}", x0, x1, y0, y1, 0.0, H, col, wallm, f"{src}: double-line partition (M); height {H} ft (A)"), kind="partition")
        n["partitions"] += 1
    for i, (x0, x1, y0, y1) in enumerate(data["perimeter_outline_walls"], 1):
        o = put(box(f"{pre}Perimeter_outline_wall_{i:02d}_AMBIGUOUS_hidden", x0, x1, y0, y1, 0.0, H, sub["ambiguous_perimeter_outline_walls"], wallm,
                    f"{src}: room-outline double line lying along the exterior wall (M); would cover exterior glazing - kept but hidden"), kind="perimeter_outline")
        o.hide_render = o.hide_viewport = True
        n["perimeter_outline_walls_hidden"] += 1
    ax, c, a, b = data["demising"]
    t = data["demising_thickness_ft"]
    put(box(f"{pre}Demising_partition_ASSUMED_thickness_height", c - t / 2, c + t / 2, a, b, 0.0, H, col, demm,
            f"{src}: heavy single boundary line at x = {c} (M); {t} ft thick, {H} ft high (A)"), kind="demising")
    n["partitions"] += 1
    dh, dt = data["divider_height_ft"], data["divider_thickness_ft"]
    for i, (ax, c, a, b) in enumerate(data["dividers"], 1):
        args = (a, b, c - dt / 2, c + dt / 2) if ax == "x" else (c - dt / 2, c + dt / 2, a, b)
        put(box(f"{pre}Bay_divider_{i:02d}_TYPE_UNKNOWN", *args, 0.0, dh, col, divm, f"{src}: single line between bays (M); {dh} ft x {dt * 12:.0f} in. (A)"), kind="bay_divider")
        n["dividers"] += 1
    for i, (ax, c, a, b) in enumerate(data["front_lines"], 1):
        args = (a, b, c - 0.04, c + 0.04) if ax == "x" else (c - 0.04, c + 0.04, a, b)
        put(box(f"{pre}Open_front_line_{i:02d}", *args, 0.0, 0.045, col, linem, f"{src}: single line at an open front (M); floor marker only"), kind="marker")
        n["markers"] += 1
    rx0, rx1, rys = data["red_line"]
    for i, (a, b) in enumerate(data["red_line_spans"], 1):
        put(box(f"{pre}RED_LINE_marker_{i}", a, b, rys[0] - 0.08, rys[0] + 0.08, 0.0, 0.05, col, redm, f"{src}: 'RED LINE' (W); position M"), kind="marker")
        n["markers"] += 1
    for i, (nm, x0, x1, y0, y1) in enumerate(data["tables"], 1):
        put(box(f"{pre}{nm}_{i}_proxy", x0, x1, y0, y1, 0.0, data["table_height_ft"], col, eqm, f"{src}: 3 ft x 7 ft rectangle (M); height A"), kind="equipment")
        n["equipment"] += 1

    # floor plates: one per room / circulation piece; smaller rooms sit a hair higher so nested rooms read correctly
    order = sorted(data["rooms"], key=lambda r: -r["gross_fill_sf"])
    for rank, r in enumerate(order):
        z = 0.012 + 0.0006 * rank
        o = box(f"{pre}Room_{r['id']}_{r['name'].split(' (')[0].replace(' ', '_').replace('/', '-').replace('.', '')}", r["x0"], r["x1"], r["y0"], r["y1"], 0.0, z,
                sub["rooms"], tints[r["cls"]], f"{src}: coloured room fill (M)")
        put(o, kind="room", room_id=r["id"], room_name=r["name"], floor="Level 1", printed_sf=r["printed_sf"] or 0, modeled_sf=r["modeled_sf"],
            modeled_net_sf=r["modeled_net_sf"], enclosure=r["enclosure"])
        n["room_plates"] += 1
        if r["printed_sf"]:
            cu = bpy.data.curves.new(f"{pre}Label_{r['id']}", "FONT")
            cu.body = f"{r['name']}\n{r['printed_sf']} SF"
            cu.align_x, cu.align_y = "CENTER", "CENTER"
            cu.size = m(min(1.7, max(0.75, (r["x1"] - r["x0"]) / 7.0)))
            lo = bpy.data.objects.new(f"{pre}Label_{r['id']}", cu)
            lo.location = (m((r["x0"] + r["x1"]) / 2), m((r["y1"] - 3.0) if (r["cls"] == "OR" or r["name"] == "PROCEDURE") else (r["y0"] + r["y1"]) / 2), m(0.08))
            cu.materials.append(textm)
            sub["labels"].objects.link(lo)
            put(lo, kind="label", room_id=r["id"])
            n["labels"] += 1
    for i, c_ in enumerate(data["circ"], 1):
        put(box(f"{pre}Circulation_{i:02d}", c_["x0"], c_["x1"], c_["y0"], c_["y1"], 0.0, 0.010, sub["rooms"], tints["CIRC"], f"{src}: circulation fill (M)"), kind="circulation")
        n["circulation_plates"] += 1

    # registered underlay of the source sheet (hidden except in the overlay render)
    img_path = ROOT / data["underlay_png"]
    if not img_path.exists():
        raise SystemExit(f"Underlay image missing: {img_path} (see notes/tenant_testfit_control_v015.md section 10)")
    img = bpy.data.images.load(str(img_path))
    um = bpy.data.materials.new(f"{pre}underlay_source_plan")
    um.use_nodes = True
    nt = um.node_tree
    for node in list(nt.nodes):
        nt.nodes.remove(node)
    n_out, n_em, n_tex = nt.nodes.new("ShaderNodeOutputMaterial"), nt.nodes.new("ShaderNodeEmission"), nt.nodes.new("ShaderNodeTexImage")
    n_tex.image = img
    nt.links.new(n_tex.outputs["Color"], n_em.inputs["Color"])
    nt.links.new(n_em.outputs[0], n_out.inputs["Surface"])
    px0, py0 = (0.0 - data["reg_x0_pt"]) / data["pt_per_ft"], (data["reg_y0_pt"] - data["page_h_pt"]) / data["pt_per_ft"]
    px1, py1 = (data["page_w_pt"] - data["reg_x0_pt"]) / data["pt_per_ft"], data["reg_y0_pt"] / data["pt_per_ft"]
    mesh = bpy.data.meshes.new(f"{pre}Underlay_registered_source_plan")
    mesh.from_pydata([(m(px0), m(py0), m(0.06)), (m(px1), m(py0), m(0.06)), (m(px1), m(py1), m(0.06)), (m(px0), m(py1), m(0.06))], [], [(0, 1, 2, 3)])
    uv = mesh.uv_layers.new(name="UVMap")
    for li, co in zip(range(4), ((0, 0), (1, 0), (1, 1), (0, 1))):
        uv.data[li].uv = co
    mesh.materials.append(um)
    uo = bpy.data.objects.new(f"{pre}Underlay_registered_source_plan", mesh)
    sub["underlay"].objects.link(uo)
    put(uo, kind="underlay", source=f"{src}; x=(X-{data['reg_x0_pt']})/{data['pt_per_ft']}, y=({data['reg_y0_pt']}-Y)/{data['pt_per_ft']}")
    uo.hide_render = uo.hide_viewport = True

    # review lighting (NOT a lighting design): soft overhead area lights so windowless rooms can be seen
    lights = []
    for i, (cx, cy, sx, sy) in enumerate(data["review_lights"], 1):
        ld = bpy.data.lights.new(f"{pre}Review_light_{i}_NOT_DESIGN", "AREA")
        ld.shape, ld.size, ld.size_y = "RECTANGLE", m(sx), m(sy)
        ld.energy = data["review_light_w_per_sf"] * sx * sy
        lo = bpy.data.objects.new(f"{pre}Review_light_{i}_NOT_DESIGN", ld)
        lo.location = (m(cx), m(cy), m(14.9))
        lo.visible_camera = False
        sub["review_lighting"].objects.link(lo)
        put(lo, kind="review_light")
        lights.append(lo)

    # saved human-eye viewpoints (5 ft 6 in.)
    cams = {}
    for key, title, loc, target, lens in data["viewpoints"]:
        cam = add_camera(f"VP_{letter}_{key}", (loc[0], loc[1], 5.5), target, sub["viewpoints"], None, lens)
        cam.data.clip_start = 0.05
        put(cam, kind="viewpoint", title=title, eye_height_ft=5.5)
        cams[key] = cam
    report = {"concept": cid, "source": src, "objects": n, "viewpoints": len(cams), "partition_height_ft_ASSUMED": H,
              "tenant_doors_modeled": 0, "note": "the source plan draws no tenant doors; none were invented"}
    return report, cams, uo, lights, sub


def tenant_areas_v015(data):
    """ASC and shell areas from the registered geometry and the v014 base model (report only)."""
    ent1 = [e[0] for e in _int_poly_with_recess(P1)]
    dem_x = data["demising"][1]
    lobby_e, lobby_s = 143.0 + INT_GYP, 72.34 - INT_GYP
    # interior = face-of-stud polygon less the inside lining, approximated by testing the four lining offsets
    def interior(pt):
        return all(_inside((pt[0] + dx, pt[1] + dy), ent1) for dx, dy in ((INT_T_IN, 0), (-INT_T_IN, 0), (0, INT_T_IN), (0, -INT_T_IN)))
    step, shell, = 0.25, 0.0
    y = step / 2
    while y < 106.0:
        x = 140.0 + step / 2
        while x < 206.0:
            if interior((x, y)) and ((y < lobby_s and x > dem_x) or (y >= lobby_s and x > lobby_e)):
                shell += step * step
            x += step
        y += step
    rects = [(r["x0"], r["x1"], r["y0"], r["y1"]) for r in data["rooms"]] + [(c["x0"], c["x1"], c["y0"], c["y1"]) for c in data["circ"]]
    xs = sorted({v for r in rects for v in r[:2]})
    ys = sorted({v for r in rects for v in r[2:]})
    asc = 0.0
    for i in range(len(xs) - 1):
        for j in range(len(ys) - 1):
            cx, cy = (xs[i] + xs[i + 1]) / 2, (ys[j] + ys[j + 1]) / 2
            if any(r[0] < cx < r[1] and r[2] < cy < r[3] for r in rects):
                asc += (xs[i + 1] - xs[i]) * (ys[j + 1] - ys[j])
    return {"asc_modeled_sf": round(asc), "asc_printed_sf": data["printed_asc_sf"], "shell_modeled_sf": round(shell), "shell_printed_sf": data["printed_shell_sf"]}


def tenant_render_setup_v015(view, uo, lights, sub):
    """Visibility for the nine tenant review renders - flags only."""
    fp = "_fp_" in view
    _int_set_visibility("eye" if fp else "L1")
    overlay = view.endswith("registration_overlay")
    uo.hide_render = not overlay
    for o in sub["rooms"].objects:
        o.hide_render = overlay
    for o in sub["labels"].objects:
        o.hide_render = fp or overlay
    for lo in lights:
        lo.hide_render = not fp
    bpy.data.objects["Sun"].hide_render = overlay or "topdown" in view


# ===================== v019 LOBBY CONCEPT A - Pass 1 (everything above is v015, unchanged) =====================
# Additive overlays only. All objects LOB_A_... inside Building_II > INT_LOBBY_CONCEPT_A. See notes/lobby_concept_control_v019.md.
# W = written on the permit set, M = measured from sealed vector linework, C = concept (Rea_Farms_2_Lobby.pptx), A = assumption.
LOBBY_VIEWS = ("lobby_A_01_entrance", "lobby_A_02_level1_corner", "lobby_A_03_level2_overlook")
LOBBY_SAMPLES = 256
LOBBY_EXPOSURE = 0.45                                                   # review renders only; the exterior set-up is untouched
LOBBY_RES = (2400, 1350)

# ---------------- centralized parameter block (feet unless noted) ----------------
LOBBY_A = {
    # wood feature wall: west wall of Lobby 101 / 204 (ID201 B2 extent W/M; ID302 module M; ID801 PL-01 W)
    "wall_face_x": 106.59, "wall_y0": 73.41, "wall_y1": 92.86, "wall_z0": 0.0, "wall_z1": 28.95,
    "field_t": 0.75 / 12,                        # laminate-wrapped field over the gypsum (W "plastic laminate wrapping the wall")
    "box_depth": 2.4 / 12,                       # M: ID302 B4 plan section
    "box_reveal": 0.0,                           # W: boxes are drawn contiguous (no reveal)
    "module_ft": 36.53 / 12,                     # M: ID302 A6 repeating group
    "light_offsets_in_aff_ft": [(3.3, 22.17), (10.6, 22.17), (17.7, 18.84), (32.2, 17.73), (25.5, 16.89), (22.2, 13.37),
                                (3.3, 4.30), (10.6, 4.30), (10.1, 2.45), (26.6, 2.08)],     # M +/-3 in. from ID302 A6 raster; 10 per group
    "light_count_documented": 64,                # W: E003 / RV-001319-001 WLC x 64
    "light_size": (3.0 / 12, 5.125 / 12, 3.75 / 12),   # W: ID801 LT-04 BEGA 33 590, 3 in. x 5 1/8 in. x 3 3/4 in.
    "light_lumens": 294, "light_cct_k": 3500,    # W: E003 WLC
    "light_point_w": 0.9, "light_emit": 0.55,     # A: render intensity
    "plinth_h": 1.0 + 1.75 / 12, "plinth_d": 1.0 + 10.0 / 12,   # W: ID303 1 ft 1 3/4 in. high, 1 ft 10 in. deep (POR-02)
    "plinth_west_y": (73.41, 88.85),             # M: ID302 A6 base band 15.4 ft from the south end
    "seat_west_y": (75.60, 84.26),               # W: ID201 string 8 1/4 in. + 1 ft 6 in. -> 8 ft 7 7/8 in.
    "seat_south_x": (106.59, 115.84),            # W: ID303 south banquette 9 ft 3 in.
    "seat_d": 1.5, "seat_t": 4.0 / 12,           # W seat depth 1 ft 6 in.; A cushion thickness
    # stair finish package (A500 W; colour C/A)
    "tread_t": 1.25 / 12, "nosing": 1.0 / 12, "riser_t": 0.0625 / 12 * 12 / 12,
    "stringer_t": 1.0 / 12, "stringer_d": 14.0 / 12,         # W: (2) 1 in. x 14 in. plates
    "soffit_t": 0.75 / 12, "shoe_w": 2.5 / 12, "shoe_h": 4.0 / 12, "handrail_d": 1.5 / 12, "handrail_h": 3.0,   # W 1 1/2 in. O.D. at 36 in.
    # pendants: A212 coffer (W/M), SH1 Lightnet Caleo Inverse x 7, 3500 K (W); sizes / heights C/A
    "coffer_outer": (112.9, 136.4, 79.9, 98.4, 28.5), "coffer_inner": (119.0, 130.5, 85.9, 92.4, 28.0), "ceiling_z": 28.95,
    "track_w": 1.5 / 12, "track_emit": 2.0,
    "ring_profile": (1.5 / 12, 2.0 / 12),        # W: 1.5 in. system; height A
    "rings": [  # (centre x, centre y, size x, size y, bottom z) - inside the inner panel, over the void, above the 19.5 guard top
        (122.0, 89.2, 5.5, 5.5, 25.0), (127.5, 88.6, 4.5, 4.5, 23.5), (124.0, 88.0, 3.5, 3.5, 22.0), (128.5, 90.0, 3.0, 4.5, 26.0),
        (122.5, 90.5, 6.0, 3.0, 21.0), (125.5, 89.8, 4.5, 4.5, 24.5), (128.6, 87.8, 3.5, 3.5, 22.5)],
    "ring_emit": 9.0, "ring_cct_k": 3500, "ring_lumens": 3570,
    # floor: ID801 POR-01 47 in. x 47 in. (W); grout / origin / walk-off extent A
    "tile": 47.0 / 12, "grout": 0.125 / 12, "tile_axis_x": 124.58, "tile_origin_y": 103.09,
    "floor_rect": (106.59, 142.45, 72.89, 103.09), "walkoff_rect": (117.58, 131.58, 95.09, 103.09), "walkoff_tile": 2.0,
    # walls
    "pt01_rgb": (0.78, 0.77, 0.71), "pt02_rgb": (0.16, 0.16, 0.17), "dark_metal_rgb": (0.055, 0.056, 0.060),   # A (PT-01 SW 7646 First Star, PT-02 Scuffmaster metal)
    "walnut_rgb": ((0.24, 0.145, 0.085), (0.35, 0.225, 0.13)),                                                     # A tone for PL-01 Uptown Walnut
    # directory: XL Media quote 8/10/2026 Panasonic TH-75EQ3W (66.3 x 38.4 x 2.8 in.) portrait, Chief AS3PL mount; location owner-approved
    "directory": {"wall_x": 142.45, "y_center": 85.37, "w": 38.4 / 12, "h": 66.3 / 12, "d": 2.8 / 12, "bottom_z": 2.5, "frame": 1.0 / 12, "mount_d": 3.0 / 12},
    # review cameras (owner-approved; eye 5 ft 6 in. on Level 1 and Level 2)
    "cameras": [("lobby_A_01_entrance", (128.0, 101.8, 5.5), (113.0, 82.0, 13.5), 18.0),                    # inside door 101A, looking SW
                ("lobby_A_02_level1_corner", (141.2, 88.5, 5.5), (110.0, 84.0, 12.5), 20.0),               # east wall by door 101B, opposite the feature wall
                ("lobby_A_03_level2_overlook", (134.2, 69.5, 21.5), (116.0, 92.0, 17.0), 20.0)],            # Level 2 balcony, looking NW / down
}
# ID302 A6 box pieces (M): (from the south end of the wall, ft) y0, y1 and z0, z1 above the floor - protruding laminate-wrapped boxes
LOBBY_A["wood_boxes"] = [(0.002, 0.499, 7.0, 16.0), (0.506, 1.173, 10.145, 15.46), (1.173, 1.679, 2.487, 10.611), (1.679, 2.013, 1.145, 4.678),
    (1.679, 2.013, 24.611, 28.949), (2.013, 2.364, 1.145, 9.234), (2.364, 3.03, 1.145, 5.194), (2.364, 3.03, 23.607, 28.949),
    (3.03, 3.539, 7.0, 16.0), (3.548, 4.213, 10.145, 15.46), (4.213, 4.719, 2.487, 10.611), (4.719, 5.052, 1.145, 4.678),
    (4.719, 5.052, 24.611, 28.949), (5.052, 5.404, 1.145, 11.056), (5.404, 6.07, 1.145, 5.194), (5.404, 6.07, 23.607, 28.949),
    (6.07, 6.58, 7.0, 16.0), (6.589, 7.256, 10.145, 15.46), (7.257, 7.763, 2.487, 10.611), (7.763, 8.096, 1.145, 4.678),
    (7.763, 8.096, 24.611, 28.949), (8.096, 8.448, 1.145, 11.191), (8.448, 9.113, 1.145, 5.194), (8.448, 9.113, 23.607, 28.949),
    (9.113, 9.622, 7.0, 16.0), (9.63, 10.296, 10.145, 15.46), (10.296, 10.804, 2.487, 10.611), (10.804, 11.137, 1.145, 4.678),
    (10.804, 11.137, 24.611, 28.949), (11.137, 11.485, 1.145, 9.234), (11.485, 12.152, 1.145, 5.194), (11.485, 12.152, 23.607, 28.949),
    (12.152, 12.661, 7.0, 16.0), (12.67, 13.337, 10.145, 15.46), (13.337, 13.844, 2.487, 10.611), (13.844, 14.178, 1.145, 4.678),
    (13.844, 14.178, 24.611, 28.949), (14.178, 14.526, 1.145, 9.234), (14.526, 15.193, 1.145, 5.194), (14.526, 15.193, 23.607, 28.949),
    (15.193, 15.702, 7.0, 16.0), (15.711, 16.419, 10.145, 15.46), (16.404, 16.907, 2.487, 10.611), (16.907, 17.241, 1.155, 4.678),
    (16.919, 17.25, 24.611, 28.949), (17.256, 17.593, 1.155, 11.802), (17.593, 18.244, 1.155, 5.194), (17.593, 18.259, 23.607, 28.949),
    (18.259, 18.769, 7.0, 16.0), (18.778, 19.384, 10.145, 15.46)]


def _lob_cct(k):
    """Warm-white RGB for a colour temperature (linear, approximate)."""
    return {3000: (1.0, 0.78, 0.55), 3500: (1.0, 0.84, 0.66), 4000: (1.0, 0.90, 0.78)}.get(k, (1.0, 0.84, 0.66))


def _lob_emission(name, rgb, strength):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out, em = nt.nodes.new("ShaderNodeOutputMaterial"), nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (*rgb, 1.0)
    em.inputs["Strength"].default_value = strength
    nt.links.new(em.outputs[0], out.inputs["Surface"])
    mat.diffuse_color = (*rgb, 1.0)
    return mat


def _lob_walnut(name, c_dark, c_light):
    """PL-01 walnut laminate: vertical grain (noise stretched along Z), subtle roughness variation, no bump."""
    mat = principled(name, c_light, 0.5, note="PL-01 Wilsonart Uptown Walnut Softgrain, grain vertical (W); tone A")
    nt = mat.node_tree
    b = nt.nodes.get("Principled BSDF")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (18.0, 18.0, 0.35)                # long grain along Z (vertical)
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 1.0
    nz.inputs["Detail"].default_value = 8.0
    nz.inputs["Roughness"].default_value = 0.62
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position, ramp.color_ramp.elements[1].position = 0.35, 0.68
    ramp.color_ramp.elements[0].color = (*c_dark, 1.0)
    ramp.color_ramp.elements[1].color = (*c_light, 1.0)
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    nt.links.new(mp.outputs[0], nz.inputs["Vector"])
    nt.links.new(nz.outputs["Fac"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    nz2 = nt.nodes.new("ShaderNodeTexNoise")
    nz2.inputs["Scale"].default_value = 6.0
    nt.links.new(tc.outputs["Object"], nz2.inputs["Vector"])
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.inputs["From Min"].default_value, mr.inputs["From Max"].default_value = 0.3, 0.7
    mr.inputs["To Min"].default_value, mr.inputs["To Max"].default_value = 0.42, 0.56
    nt.links.new(nz2.outputs["Fac"], mr.inputs["Value"])
    nt.links.new(mr.outputs[0], b.inputs["Roughness"])
    return mat


def _lob_tile(name, rgb, rough, note):
    mat = principled(name, rgb, rough, note=note)
    nt = mat.node_tree
    b = nt.nodes.get("Principled BSDF")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 0.9
    nz.inputs["Detail"].default_value = 5.0
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    mix.inputs[0].default_value = 0.18
    mix.inputs[6].default_value = (*rgb, 1.0)
    mix.inputs[7].default_value = (rgb[0] * 0.86, rgb[1] * 0.86, rgb[2] * 0.85, 1.0)
    nt.links.new(nz.outputs["Fac"], mix.inputs[0])
    nt.links.new(mix.outputs[2], b.inputs["Base Color"])
    return mat


def build_lobby_concept_a(scene, int_cols):
    P = LOBBY_A
    root = bpy.data.collections["Building_II"]
    top = bpy.data.collections.new("INT_LOBBY_CONCEPT_A")
    root.children.link(top)
    C = {}
    for n in ("ARCH_WOOD_WALL", "ARCH_STAIR_FINISH", "ARCH_GUARDRAIL", "LIGHT_DECORATIVE", "LIGHT_FEATURE_WALL", "FINISH_FLOOR", "FINISH_WALL",
              "FF&E_SEATING", "FF&E_TABLES", "FF&E_PLANTERS", "SIGNAGE_DIRECTORY", "ART_DECOR", "CAMERAS_LOBBY"):
        C[n] = bpy.data.collections.new(n)
        top.children.link(C[n])
    counts = {}

    def add(fn, cname, *args, **kw):
        obj = fn(*args, C[cname], **kw)
        obj["concept"] = "INT_LOBBY_CONCEPT_A"
        counts[cname] = counts.get(cname, 0) + 1
        return obj

    def B(name, cname, x0, x1, y0, y1, z0, z1, mat, src):
        return add(lambda *a, **k: box(name, min(x0, x1), max(x0, x1), min(y0, y1), max(y0, y1), min(z0, z1), max(z0, z1), a[0], mat, src), cname)

    # ---- materials ----
    walnut = _lob_walnut("LOB_A_PL-01_walnut_laminate", *P["walnut_rgb"])
    tread = _lob_walnut("LOB_A_WD-01_walnut_tread", (0.26, 0.15, 0.08), (0.38, 0.23, 0.12))
    dark = principled("LOB_A_dark_metal_PT-02_gunmetal", P["dark_metal_rgb"], 0.42, metallic=0.65, note="stair / shoe / rails: dark charcoal = design choice (C); PT-02 Scuffmaster metal (W) as the tone")
    pt02 = principled("LOB_A_PT-02_Scuffmaster_metal", P["pt02_rgb"], 0.35, metallic=0.55, note="ID801 PT-02 (W); colour A")
    pt01 = principled("LOB_A_PT-01_SW7646_First_Star", P["pt01_rgb"], 0.62, note="ID801 PT-01 SW 7646 First Star satin (W); RGB A")
    por01 = _lob_tile("LOB_A_POR-01_Santorini_Gray_47in", (0.60, 0.59, 0.56), 0.38, "ID801 POR-01 Porcelanosa Santorini Gray Nature 47 x 47 (W); tone A")
    grout = principled("LOB_A_grout_custom_643_warm_gray", (0.40, 0.38, 0.35), 0.8, note="ID801 custom #643 warm gray (W)")
    por02 = _lob_tile("LOB_A_POR-02_plinth_tile", (0.52, 0.51, 0.49), 0.4, "ID801 POR-02 Porcelanosa (W, spec incomplete); tone A")
    wom = principled("LOB_A_WOM-01_walk_off", (0.06, 0.06, 0.06), 0.9, note="ID801 WOM-01 Mohawk Ironwood 24 x 24 (W)")
    fab = principled("LOB_A_FAB-01_leather", (0.24, 0.21, 0.18), 0.55, note="ID801 FAB-01 Green Hide Lena Mystic (W); colour A")
    black = principled("LOB_A_black_fixture", (0.02, 0.02, 0.022), 0.5, metallic=0.3, note="LT-02 / LT-04 / SH1 black (W)")
    screen = principled("LOB_A_display_screen_off", (0.03, 0.03, 0.035), 0.15, note="Panasonic TH-75EQ3W (XL Media quote 8/10/2026); content not populated")
    ring_em = _lob_emission("LOB_A_SH1_ring_emitter_3500K", _lob_cct(P["ring_cct_k"]), P["ring_emit"])
    wlc_em = _lob_emission("LOB_A_WLC_lens_3500K", _lob_cct(P["light_cct_k"]), P["light_emit"])
    trk_em = _lob_emission("LOB_A_LT-02_track_slot_3500K", _lob_cct(3500), P["track_emit"])
    glass = bpy.data.materials.get("INT_neutral_glass")

    # ================= A. wood feature wall =================
    wx, y0, y1, z0, z1 = P["wall_face_x"], P["wall_y0"], P["wall_y1"], P["wall_z0"], P["wall_z1"]
    ft = P["field_t"]
    B("LOB_A_WoodWall_field_PL-01", "ARCH_WOOD_WALL", wx, wx + ft, y0, y1, z0, z1, walnut, "ID201 B2 extent (W/M); PL-01 wrapping the wall (W ID302)")
    for i, (a, b, za, zb) in enumerate(P["wood_boxes"], 1):
        B(f"LOB_A_WoodWall_box_{i:02d}", "ARCH_WOOD_WALL", wx + ft, wx + ft + P["box_depth"], y0 + a, y0 + b, za, zb, walnut,
          "ID302 A6 box piece (M); depth ID302 B4 (M); PL-01 wrapped plywood box (W)")
    # feature-wall lights (WLC / LT-04) placed per group
    lights = []
    k = 0
    while True:
        gy = y0 + k * P["module_ft"]
        if gy >= y1 - 0.2:
            break
        for off_in, aff in P["light_offsets_in_aff_ft"]:
            yc = gy + off_in / 12
            if yc > y1 - 0.15:
                continue
            lights.append((yc, aff))
        k += 1
    lights = lights[:P["light_count_documented"]]
    lw, lh, ld = P["light_size"]
    for i, (yc, zc) in enumerate(lights, 1):
        on_box = any(a <= yc - y0 <= b and za <= zc <= zb for a, b, za, zb in P["wood_boxes"])
        xb = wx + ft + (P["box_depth"] if on_box else 0.0)
        body = B(f"LOB_A_WLC_{i:02d}_BEGA_33590", "LIGHT_FEATURE_WALL", xb, xb + ld, yc - lw / 2, yc + lw / 2, zc - lh / 2, zc + lh / 2, black,
                 "E003 WLC BEGA 33590 3500 K (W); ID302 A6 position (M +/-3 in.)")
        B(f"LOB_A_WLC_{i:02d}_lens", "LIGHT_FEATURE_WALL", xb + ld - 0.01, xb + ld + 0.005, yc - lw / 2 + 0.01, yc + lw / 2 - 0.01, zc - lh / 2 + 0.01, zc + lh / 2 - 0.01, wlc_em, "A render emitter")
        ld_ = bpy.data.lights.new(f"LOB_A_WLC_{i:02d}_point", "POINT")
        ld_.energy = P["light_point_w"]
        ld_.color = _lob_cct(P["light_cct_k"])
        ld_.shadow_soft_size = 0.06
        lo = bpy.data.objects.new(f"LOB_A_WLC_{i:02d}_point", ld_)
        lo.location = (m(xb + ld + 0.12), m(yc), m(zc))
        C["LIGHT_FEATURE_WALL"].objects.link(lo)
        lo["concept"] = "INT_LOBBY_CONCEPT_A"
        counts["LIGHT_FEATURE_WALL"] = counts.get("LIGHT_FEATURE_WALL", 0) + 1
    # plinths and banquettes (ID303)
    pw = P["plinth_west_y"]
    B("LOB_A_Plinth_west_POR-02", "FF&E_SEATING", wx, wx + P["plinth_d"], pw[0], pw[1], 0.0, P["plinth_h"], por02, "ID303 west banquette plinth 1 ft 1 3/4 in. x 1 ft 10 in. (W); length M (ID302 A6 band)")
    sw = P["seat_west_y"]
    B("LOB_A_Banquette_west_seat_FAB-01", "FF&E_SEATING", wx + P["plinth_d"] - P["seat_d"], wx + P["plinth_d"], sw[0], sw[1], P["plinth_h"], P["plinth_h"] + P["seat_t"], fab, "ID303 / ID201 8 ft 7 7/8 in. (W); cushion thickness A")
    sx = P["seat_south_x"]
    sy0 = 72.89
    B("LOB_A_Plinth_south_POR-02", "FF&E_SEATING", sx[0], sx[1], sy0, sy0 + P["plinth_d"], 0.0, P["plinth_h"], por02, "ID303 south banquette 9 ft 3 in. (W)")
    B("LOB_A_Banquette_south_seat_FAB-01", "FF&E_SEATING", sx[0] + 0.1, sx[1], sy0 + P["plinth_d"] - P["seat_d"], sy0 + P["plinth_d"], P["plinth_h"], P["plinth_h"] + P["seat_t"], fab, "ID303 (W); cushion A")

    # ================= B. stair finish package (overlays on the frozen Stair 1) =================
    R, T = INT_RISER, INT_TREAD
    tt, nose = P["tread_t"], P["nosing"]
    x_w, x_e = 107.08, 113.02
    st, sd = P["stringer_t"], P["stringer_d"]
    for i in range(1, 15):                                                    # run 1: north -> south, leading edge on the north face
        y_hi, top = 92.20 - (i - 1) * T, i * R
        B(f"LOB_A_Stair1_run1_tread_{i:02d}_WD-01", "ARCH_STAIR_FINISH", x_w, x_e, y_hi - T, y_hi + nose, top + 0.005, top + tt, tread, "A500 wood tread (W); WD-01 walnut (W); 1 in. nosing A")
        B(f"LOB_A_Stair1_run1_riser_{i:02d}", "ARCH_STAIR_FINISH", x_w, x_e, y_hi, y_hi + 0.006, max(0.0, top - R), top + 0.005, dark, "A500 riser painted to match (W); colour C/A")
    zl = 15 * R
    B("LOB_A_Stair1_landing_WD-01", "ARCH_STAIR_FINISH", x_w, 113.52, 73.44, 79.37 + nose, zl + 0.005, zl + tt, tread, "A500 landing (W)")
    for j in range(1, 13):                                                    # run 2: west -> east, leading edge on the west face
        x_lo, top = 113.52 + (j - 1) * T, (15 + j) * R
        B(f"LOB_A_Stair1_run2_tread_{j:02d}_WD-01", "ARCH_STAIR_FINISH", x_lo - nose, x_lo + T, 73.44, 79.37, top + 0.005, top + tt, tread, "A500 wood tread (W); WD-01 (W)")
        B(f"LOB_A_Stair1_run2_riser_{j:02d}", "ARCH_STAIR_FINISH", x_lo - 0.006, x_lo, 73.44, 79.37, top - R, top + 0.005, dark, "A500 riser (W); colour C/A")

    def slab_along_y(name, cname, x0, x1, ya, yb, z_at, drop, thick, mat, src):    # sloped plate along y between ya (low) and yb (high)
        za, zb = z_at(ya) - drop, z_at(yb) - drop
        add(lambda col: hexa(name, [(x0, ya, za), (x1, ya, za), (x1, yb, zb), (x0, yb, zb)], [(x0, ya, za + thick), (x1, ya, za + thick), (x1, yb, zb + thick), (x0, yb, zb + thick)], col, mat, src), cname)

    def slab_along_x(name, cname, xa, xb, y0_, y1_, z_at, drop, thick, mat, src):
        za, zb = z_at(xa) - drop, z_at(xb) - drop
        add(lambda col: hexa(name, [(xa, y0_, za), (xb, y0_, zb), (xb, y1_, zb), (xa, y1_, za)], [(xa, y0_, za + thick), (xb, y0_, zb + thick), (xb, y1_, zb + thick), (xa, y1_, za + thick)], col, mat, src), cname)

    nose1 = lambda y: 0.571 + (92.20 - y) / T * R                             # nosing line, run 1 (z at the leading edge)
    nose2 = lambda x: 9.143 + (x - 113.52) / T * R                            # nosing line, run 2
    # stringers (outer / open side) and soffit panels
    slab_along_y("LOB_A_Stair1_run1_stringer_east", "ARCH_STAIR_FINISH", x_e, x_e + st, 79.37, 92.20 + T, nose1, sd, sd, dark, "A500 (2) 1 in. x 14 in. stringer plates (W); colour C/A")
    slab_along_y("LOB_A_Stair1_run1_soffit_panel", "ARCH_STAIR_FINISH", x_w, x_e + st, 79.37, 92.20 + T, nose1, 0.97 + R, 0.35 + R, dark, "A500 metal panel ceiling between stringers (W); drawn as a solid wedge because the frozen v014 tread blocks are 10.8 in. thick (A)")
    slab_along_x("LOB_A_Stair1_run2_stringer_north", "ARCH_STAIR_FINISH", 113.52 - T, 124.52, 79.37, 79.37 + st, nose2, sd, sd, dark, "A500 stringer plate (W); colour C/A")
    slab_along_x("LOB_A_Stair1_run2_soffit_panel", "ARCH_STAIR_FINISH", 113.52 - T, 124.52, 73.44, 79.37 + st, nose2, 0.97 + R, 0.35 + R, dark, "A500 metal panel ceiling (W); solid wedge (A, see run 1)")
    B("LOB_A_Stair1_landing_fascia_east", "ARCH_STAIR_FINISH", 113.52, 113.52 + st, 73.44, 79.37, zl - sd, zl, dark, "landing edge plate (A500 stringer depth W)")
    B("LOB_A_Stair1_landing_soffit", "ARCH_STAIR_FINISH", x_w, 113.52, 73.44, 79.37, 7.67 - P["soffit_t"] - 0.01, 7.67 - 0.01, dark, "A500 metal panel ceiling (W)")
    # glass shoe and handrails (guards themselves are the frozen v014 glass panels)
    shw, shh, hd, hh = P["shoe_w"], P["shoe_h"], P["handrail_d"], P["handrail_h"]
    slab_along_y("LOB_A_Stair1_run1_shoe", "ARCH_GUARDRAIL", x_e - shw / 2 + 0.025, x_e + shw / 2 + 0.025, 79.37, 92.20 + T, lambda y: nose1(y) + 0.11, 0.0, shh, dark, "A500 glass shoe guardrail, metal panel wrap (W); profile A")
    slab_along_y("LOB_A_Stair1_run1_handrail_glass_side", "ARCH_GUARDRAIL", x_e - 0.20, x_e - 0.20 + hd, 79.37, 92.20 + T, lambda y: nose1(y) + hh, 0.0, hd, dark, "A500 1 1/2 in. O.D. handrail at 36 in. (W); round drawn square A")
    slab_along_y("LOB_A_Stair1_run1_handrail_wall_side", "ARCH_GUARDRAIL", wx + ft + P["box_depth"] + 0.15, wx + ft + P["box_depth"] + 0.15 + hd, 79.37, 92.20 + T, lambda y: nose1(y) + hh, 0.0, hd, dark, "A500 wall handrail (W); offset from the wood wall A")
    slab_along_x("LOB_A_Stair1_run2_shoe", "ARCH_GUARDRAIL", 113.52 - T, 124.52, 79.37 - shw / 2 + 0.025, 79.37 + shw / 2 + 0.025, lambda x: nose2(x) + 0.11, 0.0, shh, dark, "A500 shoe (W)")
    slab_along_x("LOB_A_Stair1_run2_handrail_glass_side", "ARCH_GUARDRAIL", 113.52 - T, 124.52, 79.37 - 0.20, 79.37 - 0.20 + hd, lambda x: nose2(x) + hh, 0.0, hd, dark, "A500 handrail (W)")
    # Level 2 guards: shoe at the slab, top cap, PT-02 fascia on the slab edge
    for nm, x0, x1, ya, yb in (("balcony_east_of_stair", 124.52 - shw / 2 + 0.025, 124.52 + shw / 2 + 0.025, 79.37, 82.52),
                               ("balcony_north", 124.52, 135.75, 82.47 - shw / 2 + 0.025, 82.47 + shw / 2 + 0.025),
                               ("south_of_stair", 106.59 + INT_GYP, 124.52, 73.39 - shw / 2 + 0.025, 73.39 + shw / 2 + 0.025)):
        B(f"LOB_A_L2_guard_shoe_{nm}", "ARCH_GUARDRAIL", x0, x1, ya, yb, L2_FF + 0.005, L2_FF + shh, dark, "A500 shoe glass railing (W); profile A")
        B(f"LOB_A_L2_guard_cap_{nm}", "ARCH_GUARDRAIL", x0, x1, ya, yb, L2_FF + 3.5 - 0.005, L2_FF + 3.5 + 0.06, dark, "top cap A")
    for nm, x0, x1, ya, yb in (("void_west_edge", 124.52 - 0.012, 124.52, 79.37, 82.52), ("void_north_edge", 124.52, 135.75, 82.52, 82.52 + 0.012),
                               ("void_south_edge", 106.59, 124.52, 73.44 - 0.012, 73.44)):
        B(f"LOB_A_L2_fascia_PT-02_{nm}", "FINISH_WALL", x0, x1, ya, yb, INT_DECK_UNDERSIDE_L2, L2_FF, pt02, "ID201 PT-02 on the balcony fascia (W)")

    # ================= C. coffer, LT-02 track and SH1 pendant cluster =================
    ox0, ox1, oy0, oy1, oz = P["coffer_outer"]
    ix0, ix1, iy0, iy1, iz = P["coffer_inner"]
    cz = P["ceiling_z"]
    B("LOB_A_Coffer_outer_plane_12ft6", "FINISH_WALL", ox0, ox1, oy0, oy1, oz, oz + 0.04, pt01, "A212 Rev5 coffer 12 ft 6 in. AFF L2 (W); position M")
    for nm, x0, x1, ya, yb in (("s", ox0, ox1, oy0, oy0 + 0.04), ("n", ox0, ox1, oy1 - 0.04, oy1), ("w", ox0, ox0 + 0.04, oy0, oy1), ("e", ox1 - 0.04, ox1, oy0, oy1)):
        B(f"LOB_A_Coffer_outer_return_{nm}", "FINISH_WALL", x0, x1, ya, yb, oz, cz, pt01, "A212 (W)")
    B("LOB_A_Coffer_inner_panel_12ft0", "FINISH_WALL", ix0, ix1, iy0, iy1, iz, iz + 0.04, pt01, "A212 Rev5 inner panel 12 ft 0 in. AFF L2 (W)")
    for nm, x0, x1, ya, yb in (("s", ix0, ix1, iy0, iy0 + 0.04), ("n", ix0, ix1, iy1 - 0.04, iy1), ("w", ix0, ix0 + 0.04, iy0, iy1), ("e", ix1 - 0.04, ix1, iy0, iy1)):
        B(f"LOB_A_Coffer_inner_return_{nm}", "FINISH_WALL", x0, x1, ya, yb, iz, oz, pt01, "A212 (W)")
    tw = P["track_w"]
    for nm, x0, x1, ya, yb in (("s", ox0, ox1, oy0 + 0.05, oy0 + 0.05 + tw), ("n", ox0, ox1, oy1 - 0.05 - tw, oy1 - 0.05), ("w", ox0 + 0.05, ox0 + 0.05 + tw, oy0, oy1), ("e", ox1 - 0.05 - tw, ox1 - 0.05, oy0, oy1)):
        B(f"LOB_A_LT-02_track_{nm}", "LIGHT_DECORATIVE", x0, x1, ya, yb, oz - 0.02, oz + 0.01, black, "ID801 LT-02 Coronet Magneto black recessed track, mitered (W); at the coffer edge (A212 tag)")
        B(f"LOB_A_LT-02_slot_{nm}", "LIGHT_DECORATIVE", x0 + 0.02, x1 - 0.02, ya + 0.02, yb - 0.02, oz - 0.025, oz - 0.015, trk_em, "A render emitter")
    pw_, ph_ = P["ring_profile"]
    for i, (cx, cy, rsx, rsy, rzb) in enumerate(P["rings"], 1):
        zb = rzb
        za = zb + ph_
        x0, x1, ya, yb = cx - rsx / 2, cx + rsx / 2, cy - rsy / 2, cy + rsy / 2
        src = "E003 / RV-001319-001 SH1 Lightnet Caleo Inverse 3500 K x 7 (W); A212 cluster position (M); size and height C/A"
        for nm, bx0, bx1, by0, by1 in (("s", x0, x1, ya, ya + pw_), ("n", x0, x1, yb - pw_, yb), ("w", x0, x0 + pw_, ya, yb), ("e", x1 - pw_, x1, ya, yb)):
            B(f"LOB_A_SH1_ring_{i}_{nm}", "LIGHT_DECORATIVE", bx0, bx1, by0, by1, zb, za, black, src)
        for nm, bx0, bx1, by0, by1 in (("s", x0 + pw_, x1 - pw_, ya + pw_ - 0.006, ya + pw_), ("n", x0 + pw_, x1 - pw_, yb - pw_, yb - pw_ + 0.006),
                                       ("w", x0 + pw_ - 0.006, x0 + pw_, ya + pw_, yb - pw_), ("e", x1 - pw_, x1 - pw_ + 0.006, ya + pw_, yb - pw_)):
            B(f"LOB_A_SH1_ring_{i}_emit_{nm}", "LIGHT_DECORATIVE", bx0, bx1, by0, by1, zb + 0.02, za - 0.02, ring_em, "A render emitter (3,570 lm class)")
        for nm, bx0, bx1, by0, by1 in (("s", x0, x1, ya, ya + pw_), ("n", x0, x1, yb - pw_, yb), ("w", x0, x0 + pw_, ya, yb), ("e", x1 - pw_, x1, ya, yb)):
            B(f"LOB_A_SH1_ring_{i}_emit_down_{nm}", "LIGHT_DECORATIVE", bx0 + 0.01, bx1 - 0.01, by0 + 0.01, by1 - 0.01, zb - 0.004, zb, ring_em, "A render emitter (direct component on the tube underside)")
        for k_, (px, py) in enumerate(((x0 + pw_ / 2, ya + pw_ / 2), (x1 - pw_ / 2, ya + pw_ / 2), (x1 - pw_ / 2, yb - pw_ / 2), (x0 + pw_ / 2, yb - pw_ / 2)), 1):
            B(f"LOB_A_SH1_ring_{i}_cable_{k_}", "LIGHT_DECORATIVE", px - 0.008, px + 0.008, py - 0.008, py + 0.008, za, iz, black, "aircraft-cable suspension from the 12 ft 0 in. panel (W mounting; length A)")
        B(f"LOB_A_SH1_ring_{i}_canopy", "LIGHT_DECORATIVE", cx - 0.25, cx + 0.25, cy - 0.25, cy + 0.25, iz - 0.06, iz, black, "canopy A")

    # ================= D. floor =================
    fx0, fx1, fy0, fy1 = P["floor_rect"]
    B("LOB_A_Floor_grout_bed", "FINISH_FLOOR", fx0, fx1, fy0, fy1, 0.001, 0.012, grout, "ID801 custom #643 warm gray grout (W)")
    mod = P["tile"] + P["grout"]
    xs, x = [], P["tile_axis_x"] - mod / 2
    while x > fx0 - mod:
        x -= mod
    while x < fx1:
        xs.append(x)
        x += mod
    ys, y = [], P["tile_origin_y"]
    while y > fy0:
        ys.append(y)
        y -= mod
    n_tiles = 0
    for xa in xs:
        for yb_ in ys:
            tx0, tx1 = max(fx0, xa + P["grout"] / 2), min(fx1, xa + mod - P["grout"] / 2)
            ty1, ty0 = min(fy1, yb_ - P["grout"] / 2), max(fy0, yb_ - mod + P["grout"] / 2)
            if tx1 - tx0 < 0.05 or ty1 - ty0 < 0.05:
                continue
            n_tiles += 1
            B(f"LOB_A_Tile_POR-01_{n_tiles:03d}", "FINISH_FLOOR", tx0, tx1, ty0, ty1, 0.012, 0.03, por01, "ID801 POR-01 47 x 47 (W); grout 1/8 in. and origin on the entry axis A")
    wx0, wx1, wy0, wy1 = P["walkoff_rect"]
    B("LOB_A_WalkOff_WOM-01", "FINISH_FLOOR", wx0, wx1, wy0, wy1, 0.03, 0.045, wom, "ID101 WOM-01 at the entry (W); extent A")

    # ================= E. wall finishes (PT-01 overlays, 1/16 in. off the frozen faces) =================
    t_, g_ = 0.005, 0.003
    wy0, wy1 = P["wall_y0"], P["wall_y1"]
    for nm, x0, x1, ya, yb, za, zb in (
            ("L1_west_north_of_wood", wx + g_, wx + g_ + t_, wy1, 97.56, 0.0, 15.46), ("L1_west_door_head", wx + g_, wx + g_ + t_, 97.56, 101.12, 7.0, 15.46),
            ("L1_west_north_end", wx + g_, wx + g_ + t_, 101.12, 103.09, 0.0, 15.46), ("L1_west_south_return", wx + g_, wx + g_ + t_, 72.89, wy0, 0.0, 15.46),
            ("L1_south_west_of_101C", P["seat_south_x"][1], 126.66, 72.89 + g_, 72.89 + g_ + t_, 0.0, 15.46), ("L1_south_101C_head", 126.66, 133.20, 72.89 + g_, 72.89 + g_ + t_, 7.0, 15.46),
            ("L1_south_east_of_101C", 133.20, 135.75, 72.89 + g_, 72.89 + g_ + t_, 0.0, 15.46),
            ("L1_east_south_of_101B", 142.45 - g_ - t_, 142.45 - g_, 82.58, 88.16, 0.0, 15.46), ("L1_east_101B_head", 142.45 - g_ - t_, 142.45 - g_, 88.16, 94.74, 7.0, 15.46),
            ("L1_east_north_of_101B", 142.45 - g_ - t_, 142.45 - g_, 94.74, 97.29, 0.0, 15.46), ("L1_east_return", 143.0, 143.95, 97.29 - g_ - t_, 97.29 - g_, 0.0, 15.46),
            ("L2_west_above_wood", wx + g_, wx + g_ + t_, wy0, wy1, 15.46, 16.0), ("L2_west_north", wx + g_, wx + g_ + t_, wy1, 104.92, 16.0, 28.95),
            ("L2_west_south", wx + g_, wx + g_ + t_, 71.4, wy0, 16.0, 28.95), ("L2_south_lobby", 106.59, 139.91, 64.61 + g_, 64.61 + g_ + t_, 16.0, 28.95),
            ("L2_east_lobby", 143.95 - g_ - t_, 143.95 - g_, 78.96, 104.42, 16.0, 28.95)):
        B(f"LOB_A_PT-01_{nm}", "FINISH_WALL", x0, x1, ya, yb, za, zb, pt01, "ID801 PT-01 SW 7646 First Star on gypsum (W)")
    B("LOB_A_RB-01_base_east", "FINISH_WALL", 142.45 - 0.02, 142.45 - g_, 82.58, 88.16, 0.0, 0.5, dark, "ID801 RB-01 6 in. base (W); colour A")

    # ================= G. directory massing (75 in. portrait per the approved XL Media quote) =================
    d = P["directory"]
    xw, yc = d["wall_x"], d["y_center"]
    B("LOB_A_Directory_mount_Chief_AS3PL", "SIGNAGE_DIRECTORY", xw - d["mount_d"], xw - 0.01, yc - 1.0, yc + 1.0, d["bottom_z"] + 1.0, d["bottom_z"] + d["h"] - 1.0, black, "XL Media quote 8/10/2026 Chief AS3PL portrait mount (W); size A")
    B("LOB_A_Directory_frame", "SIGNAGE_DIRECTORY", xw - d["mount_d"] - d["d"], xw - d["mount_d"], yc - d["w"] / 2 - d["frame"], yc + d["w"] / 2 + d["frame"], d["bottom_z"] - d["frame"], d["bottom_z"] + d["h"] + d["frame"], black, "Panasonic TH-75EQ3W 75 in. portrait (W quote); bezel A")
    B("LOB_A_Directory_screen_75in_portrait", "SIGNAGE_DIRECTORY", xw - d["mount_d"] - d["d"] - 0.004, xw - d["mount_d"] - d["d"], yc - d["w"] / 2, yc + d["w"] / 2, d["bottom_z"], d["bottom_z"] + d["h"], screen, "content / branding not populated (owner instruction)")
    B("LOB_A_Directory_accent_panel_PT-02", "SIGNAGE_DIRECTORY", xw - 0.012, xw - 0.008, yc - 2.0, yc + 2.0, 1.5, 10.5, pt02, "accent panel behind the display (C/A)")

    # ================= cameras =================
    cams = {}
    for key, eye, tgt, lens in P["cameras"]:
        cam = add_camera("Cam_" + key, eye, tgt, C["CAMERAS_LOBBY"], None, lens)
        cam["concept"] = "INT_LOBBY_CONCEPT_A"
        cam.data.clip_start = 0.05
        cams[key] = (cam, LOBBY_RES)
        counts["CAMERAS_LOBBY"] = counts.get("CAMERAS_LOBBY", 0) + 1

    # ================= checks =================
    checks = {}
    stair_bb = (107.08, 124.52, 73.44, 92.20 + P["nosing"], 0.0, 16.0)
    guard_top = L2_FF + 3.5
    checks["pendants"] = []
    for i, (cx, cy, rsx, rsy, zb) in enumerate(P["rings"], 1):
        x0, x1, ya, yb = cx - rsx / 2, cx + rsx / 2, cy - rsy / 2, cy + rsy / 2
        over_stair = not (x1 < stair_bb[0] or x0 > stair_bb[1] or yb < stair_bb[2] or ya > stair_bb[3])
        inside_panel = ix0 <= x0 and x1 <= ix1 and iy0 <= ya and yb <= iy1
        over_l2_floor = yb < 82.52 and x0 > 124.52 or yb < 73.44
        checks["pendants"].append({"ring": i, "bottom_z": zb, "clear_above_stair_top_ft": round(zb - 16.0, 2) if over_stair else None,
                                   "clear_above_L2_guard_top_ft": round(zb - guard_top, 2), "inside_documented_panel": inside_panel, "over_level2_floor": over_l2_floor})
    checks["wood_wall_vs_door_101D_clear_ft"] = round(97.56 - wy1, 2)
    checks["directory_vs_door_101B_clear_ft"] = round(88.16 - (yc + d["w"] / 2 + d["frame"]), 2)
    checks["directory_projection_ft"] = round(d["mount_d"] + d["d"], 3)
    checks["south_banquette_east_end_vs_101C_path_x"] = {"banquette_x1": P["seat_south_x"][1], "door_101C_x0": 126.66, "clear_ft": round(126.66 - sx[1], 2)}
    checks["west_banquette_headroom_under_run1_ft"] = round(nose1(sw[1]) - 0.92 - (P["plinth_h"] + P["seat_t"]), 2)
    checks["wood_boxes_max_projection_from_gypsum_ft"] = round(ft + P["box_depth"], 3)
    checks["entry_path_101A_to_101C_clear_x"] = {"path_x": (124.6, 130.0), "obstructions": "none (tiles / walk-off only)"}
    report = {"objects_by_collection": counts, "total_objects": sum(counts.values()), "wood_box_pieces": len(P["wood_boxes"]), "feature_wall_lights": len(lights),
              "pendants": len(P["rings"]), "floor_tiles": n_tiles, "checks": checks}
    return report, cams, C


def lobby_render_setup_v019(view, t_underlay, t_lights, t_sub):
    """Visibility for the three lobby review renders - flags only. Solid masses off, everything inside on, tenant helpers off."""
    _int_set_visibility("eye")
    t_underlay.hide_render = True
    for o in list(t_sub["labels"].objects):
        o.hide_render = True
    for lo in t_lights:
        lo.hide_render = True
    bpy.data.objects["Sun"].hide_render = False


def main():
    global BLEND, REPORT, RENDER_DIR
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    do_render = "--no-render" not in argv
    if "--out" in argv:
        out = Path(argv[argv.index("--out") + 1])
        BLEND, REPORT, RENDER_DIR = out / BLEND.name, out / REPORT.name, out
    views = list(LOBBY_VIEWS)                                                         # v019: three lobby review views
    SCHEDULE = REPORT.with_name("tenant_concept_A_CNSA_ASC_room_schedule_v019.json")   # identical data to the v015 schedule
    outputs = [BLEND, REPORT, SCHEDULE] + ([RENDER_DIR / f"{STEM}_{v}.png" for v in views] if do_render else [])
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
    detail_report = site_detail_v013()                                         # v013
    interior_report, int_cols = interior_base_v014(scene)                      # v014
    tenant_reports = {}                                                        # v015
    for cid, tdata in TENANT_CONCEPTS.items():
        trep, t_cams, t_underlay, t_lights, t_sub = build_tenant_concept(cid, tdata, int_cols["TENANT_CONCEPTS"])
        trep["areas"] = tenant_areas_v015(tdata)
        tenant_reports[cid] = trep
    tdata = TENANT_CONCEPTS["Concept_A_CNSA_ASC"]
    SCHEDULE.write_text(json.dumps({"concept": "Concept_A_CNSA_ASC", "source": tdata["source"], "floor": tdata["floor"],
                                    "note": "modeled_sf = coloured fill rectangle minus the partitions extracted from the drawing",
                                    "areas": tenant_reports["Concept_A_CNSA_ASC"]["areas"],
                                    "rooms": [dict(r, concept="Concept_A_CNSA_ASC", floor="Level 1") for r in tdata["rooms"]]}, indent=1), encoding="utf-8")
    lobby_report, lobby_cams, lobby_cols = build_lobby_concept_a(scene, int_cols)   # v019
    cams.update(interior_cameras_v014(c_cam))                                  # v014
    cams.update(lobby_cams)                                                    # v019
    cams["tenant_A_01_registration_overlay"] = (add_camera("Cam_TEN_A_overlay", (88.0, 53.0, 300.0), (88.0, 53.001, 0.0), t_sub["viewpoints"], 205), (3200, 1800))
    cams["tenant_A_02_L1_topdown_plan"] = (add_camera("Cam_TEN_A_topdown", (88.0, 53.0, 300.0), (88.0, 53.001, 0.0), t_sub["viewpoints"], 205), (3200, 1800))
    cams["tenant_A_03_L1_oblique_cutaway"] = (add_camera("Cam_TEN_A_oblique", (-70.0, -150.0, 170.0), (72.0, 50.0, 0.0), t_sub["viewpoints"], None, 40.0), (2400, 1350))
    for view, key in (("tenant_A_04_fp_ASC_entrance", "01_ASC_entrance_arrival"), ("tenant_A_05_fp_reception_waiting", "02_reception"),
                      ("tenant_A_06_fp_main_clinical_corridor", "04_main_clinical_circulation"), ("tenant_A_07_fp_pre_post_room", "06_pre_post_room"),
                      ("tenant_A_08_fp_operating_room", "08_operating_room"), ("tenant_A_09_fp_sterile_processing", "09_sterile_processing")):
        cams[view] = (t_cams[key], (2400, 1350))
    _int_set_visibility("exterior")                                            # saved file looks like v013
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
              "boolean_cuts_applied": cut_count, "facade_detail_objects": detail_count, "site_objects": site_count, "context_objects": context_count, "vegetation_v012": vegetation_report, "site_detail_v013": detail_report, "interior_base_v014": interior_report, "tenant_concepts_v015": tenant_reports, "lobby_concept_A_v019": lobby_report, "refined_materials": refined_materials, "sky_type": sky_type, "landscape_counts": LANDSCAPE_COUNTS,
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
        scene.cycles.samples = LOBBY_SAMPLES
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
            lobby_render_setup_v019(view, t_underlay, t_lights, t_sub)         # v019: flags only
            scene.view_settings.exposure = LOBBY_EXPOSURE
            scene.render.resolution_x, scene.render.resolution_y = rx, ry
            scene.render.filepath = str(RENDER_DIR / f"{STEM}_{view}.png")
            t0 = time.time()
            bpy.ops.render.render(write_still=True)
            times[view] = round(time.time() - t0, 1)
        report["render_seconds"] = times
        t_underlay.hide_render = True                                          # v015: leave the file as built
        bpy.data.objects["Sun"].hide_render = False
        for o in list(t_sub["rooms"].objects) + list(t_sub["labels"].objects) + list(t_lights):
            o.hide_render = False
        _int_set_visibility("exterior")
        scene.view_settings.exposure = EXPOSURE_V010
        scene.cycles.samples = RENDER_SAMPLES_V010
        scene.camera = cams["hero_front_north"][0]
        bpy.ops.wm.save_mainfile()

    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("BUILD_REPORT=" + json.dumps(report))


if __name__ == "__main__":
    main()
