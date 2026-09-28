"""Rea Farms II 3D - Building II geometry validation shell, v001.

Procedural build. Every number below is documented in notes/model_control_v001.md
(source sheet, confidence code W/G/M/A). Edit the DATA section and re-run under a
new version number to revise geometry; nothing is modeled by hand.

Run (from the project root) with:
  "C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe" --background --python scripts/build_shell_v001.py
Optional:  -- --no-render     build and save the .blend only
           -- --out <folder>  write every output into <folder> instead (trial runs)

Units: all DATA values are decimal feet in the drawing coordinate system
  origin = grid 1' x grid K' at Level 01 finish floor, +X project east,
  +Y project north, +Z up.  Blender scene is metric at true scale (FT = 0.3048 m).
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

VERSION = "v001"
STEM = f"building_shell_{VERSION}"
ROOT = Path(__file__).resolve().parent.parent
BLEND = ROOT / "models" / f"{STEM}.blend"
REPORT = ROOT / "notes" / f"{STEM}_build_report.json"
RENDER_DIR = ROOT / "renders"
FT = 0.3048

# =============================== DATA (feet) ================================
# --- datums: Rev 5 A300/A301, Approved A302/A320 (W) ---
AVG_GRADE = -1.8125      # -1'-9 3/4"
L1_FF = 0.0
TERRACE_FF = 15.0 + 2.0 / 12
L2_FF = 16.0             # recorded; exterior shell does not use it (A-7)
LOW_PARAPET_1 = 17.5
LOW_PARAPET_2 = 19.5
ROOF_STRUCT = 32.0
HIGH_PARAPET_1 = 34.0 + 11.0 / 12
PARAPET_CW2_BAY = 38.0 + 9.5 / 12
HIGH_PARAPET_2 = 42.0
HIGH_PARAPET_3 = 43.0 + 10.0 / 12

# --- grids: Rev 5 A112 (G/W) ---
GX = {"1'": 0.0, "1": 1.5, "1.2'": 5.0, "2": 6.0, "3": 32.5, "3.1": 34.5, "4": 59.0,
      "5": 65.5, "6": 80.5, "6'": 82.875, "7": 92.5, "7'": 94.125, "7.1'": 94.375,
      "7.2": 95.5, "8'": 104.646, "8": 105.5, "8.3": 115.5, "8.4": 125.378, "9": 143.5,
      "9'": 144.5, "9.1": 145.125, "9.1'": 147.875, "10": 172.411, "11": 202.0,
      "11'": 203.0, "12": 203.5, "12'": 205.0}
GY = {"K'": 0.0, "K": 1.833, "J'": 2.0, "J": 3.833, "H'": 23.056, "H": 24.533,
      "G": 50.944, "F'": 57.604, "F": 58.789, "E.4": 65.944, "E": 71.833, "D": 77.378,
      "C": 83.789, "B": 96.833, "B'": 97.833, "A": 103.333, "A.1'": 104.917,
      "A'": 105.833, "XA": 113.311}

CW2_BAY_Y = 104.417                      # 6" setback of bay between 7.1' and 8' (M)
PIER_W = 3.0 + 8.0 / 12                  # lobby piers 3'-8" (W)
L2_WEST_X = GX["1.2'"] + 25.5            # 25'-6" east of 1.2' (W)
L2_EAST_X = 174.0                        # grid 10 + 1'-7" (W)
L2_SOUTH_Y = 22.95                       # grid H + 1'-7" south (M)
L2_NE_Y = 78.961                         # grid D + 1'-7" north (M)
LOBBY_SOUTH_Y = 48.789                   # A132 linework (M)
PARAPET_T = 1.0                          # A-2
OPENING_DEPTH = 0.5                      # A-4

# --- Level 1 footprint (podium), CCW; edge i runs vertex i -> i+1 ---
P1 = [(GX["1.2'"], 0.0), (GX["6'"], 0.0), (GX["6'"], GY["J'"]), (GX["7'"], GY["J'"]),
      (GX["7'"], 0.0), (GX["9.1'"], 0.0), (GX["9.1'"], GY["J'"]), (GX["11'"], GY["J'"]),
      (GX["11'"], GY["H'"]), (GX["12'"], GY["H'"]), (GX["12'"], GY["B'"]),
      (GX["9'"], GY["B'"]), (GX["9'"], GY["A'"]), (GX["8'"], GY["A'"]),
      (GX["8'"], CW2_BAY_Y), (GX["7.1'"], CW2_BAY_Y), (GX["7.1'"], GY["A.1'"]),
      (0.0, GY["A.1'"]), (0.0, GY["F'"]), (GX["1.2'"], GY["F'"])]
# terrace perimeter parapet top per P1 edge (None = wall continues up as Level 2 mass)
P1_PARAPET = [LOW_PARAPET_2, LOW_PARAPET_2, LOW_PARAPET_1, LOW_PARAPET_2, LOW_PARAPET_2,
              LOW_PARAPET_2, LOW_PARAPET_1, LOW_PARAPET_1, LOW_PARAPET_2, LOW_PARAPET_2,
              LOW_PARAPET_2, None, None, None, None, None, None, None, None, LOW_PARAPET_2]

# --- Level 2 roof zones (CCW) with parapet top per edge ---
ZONES = {
    "HighBlock": {
        "poly": [(0.0, GY["F'"]), (GX["8'"], GY["F'"]), (GX["8'"], CW2_BAY_Y),
                 (GX["7.1'"], CW2_BAY_Y), (GX["7.1'"], GY["A.1'"]), (0.0, GY["A.1'"])],
        "parapet": [HIGH_PARAPET_2, None, PARAPET_CW2_BAY, HIGH_PARAPET_2,
                    HIGH_PARAPET_2, HIGH_PARAPET_2],
        "source": "A132 Rev5 tags TO PARAPET 42'-0\" / 38'-9 1/2\"; A300/A301"},
    "LobbyBlock": {
        "poly": [(GX["8'"], LOBBY_SOUTH_Y), (GX["9'"], LOBBY_SOUTH_Y),
                 (GX["9'"], GY["A'"]), (GX["8'"], GY["A'"])],
        "parapet": [HIGH_PARAPET_3] * 4,
        "source": "A132 Rev5 tags TO PARAPET 43'-10\""},
    "LowRoof": {
        "poly": [(L2_WEST_X, L2_SOUTH_Y), (L2_EAST_X, L2_SOUTH_Y), (L2_EAST_X, L2_NE_Y),
                 (GX["9'"], L2_NE_Y), (GX["9'"], LOBBY_SOUTH_Y), (GX["8'"], LOBBY_SOUTH_Y),
                 (GX["8'"], GY["F'"]), (L2_WEST_X, GY["F'"])],
        "parapet": [HIGH_PARAPET_1, HIGH_PARAPET_1, HIGH_PARAPET_1, None, None, None,
                    None, HIGH_PARAPET_1],
        "source": "A122 Approved; A132 Rev5 tags TO PARAPET 34'-11\""},
}

# --- lobby recess between piers, glazing plane on grid A (W) ---
LOBBY_RECESS = {"x0": GX["8'"] + PIER_W, "x1": GX["9'"] - PIER_W,
                "y_back": GY["A"], "z0": AVG_GRADE, "z1": 28.77}

# --- openings: (normal, plane, a0, a1, z0, z1, tag) ; a = X for N/S faces, Y for E/W ---
S_SILL, S_HEAD = 3.09, 13.77
L2_SILL, L2_HEAD = 19.81, 28.77
OPENINGS = [
    ("N", GY["A.1'"], 0.0, 89.8, 0.21, 28.77, "CW3"),
    ("N", CW2_BAY_Y, 95.05, 104.05, 0.21, 14.97, "CW2 lower"),
    ("N", CW2_BAY_Y, 95.05, 104.05, 18.25, 28.77, "CW2 upper"),
    ("N", GY["A"], 108.69, 140.29, 0.21, 9.81, "CW1 lower / 101A"),
    ("N", GY["A"], 108.69, 140.29, 18.25, 28.77, "CW1 upper"),
    ("N", GY["B'"], 145.63, 170.63, S_SILL, S_HEAD, "SF3"),
    ("N", GY["B'"], 175.63, 200.63, S_SILL, S_HEAD, "SF3"),
    ("N", L2_NE_Y, 151.77, 173.29, L2_SILL, L2_HEAD, "SF5B"),
    ("N", L2_NE_Y, 146.97, 149.97, 24.09, L2_HEAD, "SF5A"),
    ("E", GX["12'"], 33.88, 48.36, 3.14, 9.78, "E storefront under canopy"),
    ("E", GX["12'"], 53.68, 63.36, 3.14, 13.78, "E SF"),
    ("E", GX["12'"], 68.64, 93.36, 3.14, 13.78, "E SF"),
    ("E", GX["11'"], 7.20, 16.96, 0.10, 13.82, "E entrance SF"),
    ("E", L2_EAST_X, 23.68, 48.36, 19.82, 28.78, "SF6"),
    ("E", L2_EAST_X, 53.68, 78.36, 19.82, 28.78, "SF6"),
    ("E", GX["9'"], 83.68, 96.76, 19.82, 28.78, "SF7"),
    ("S", GY["J'"], 153.47, 198.47, 3.05, 13.81, "S 45'-0\" SF"),
    ("W", GX["1.2'"], 4.35, 14.03, 3.18, 13.78, "SF1"),
    ("W", L2_WEST_X, 25.55, 50.27, 19.82, 28.78, "SF6"),
    ("W", 0.0, 74.07, 104.83, 0.22, 28.82, "CW4"),
]
for x0 in (23.5, 38.5, 53.5, 68.5, 103.5, 118.5, 133.5):      # SF1 10'-0" RO (W)
    OPENINGS.append(("S", 0.0, x0, x0 + 10.0, S_SILL, S_HEAD, "SF1"))
for x0, x1 in ((38.67, 63.33), (68.67, 93.33), (98.67, 113.33), (118.67, 143.33),
               (148.67, 173.33)):                               # SF6 on Level 2 south
    OPENINGS.append(("S", L2_SOUTH_Y, x0, x1, L2_SILL, L2_HEAD, "SF6"))

# --- drop-off canopy: Rev 5 A700 ---
CANOPY = {"cols_x": [79.644, 108.233, 140.922], "end_overhang": 2.0 + 2.0 / 12,
          "y_gutter": GY["XA"], "south": 6.625, "north": 16.625,
          "z_gutter_top": 16.1, "slope": 1.5 / 12, "glass_t": 0.25,
          "col_top": 15.0, "col_size": 14.0 / 12}
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


def prism(name, poly, z0, z1, col, mat, source=""):
    n = len(poly)
    verts = [(x, y, z0) for x, y in poly] + [(x, y, z1) for x, y in poly]
    faces = [tuple(reversed(range(n))), tuple(range(n, 2 * n))]
    faces += [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    return mesh_object(name, verts, faces, col, mat, source)


def box(name, x0, x1, y0, y1, z0, z1, col, mat, source=""):
    return prism(name, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], z0, z1, col, mat, source)


def inward_normal(p, q):
    dx, dy = q[0] - p[0], q[1] - p[1]
    length = math.hypot(dx, dy)
    return (-dy / length, dx / length)          # CCW polygon -> left side is inside


def parapets(name, poly, tops, z_base, col, mat, source=""):
    """One prism per edge, mitred where both neighbours exist, square-ended otherwise."""
    n = len(poly)
    made = []
    for i in range(n):
        if tops[i] is None:
            continue
        p, q = poly[i], poly[(i + 1) % n]
        nx, ny = inward_normal(p, q)
        ends = []
        for vert, other_edge in ((p, (i - 1) % n), (q, (i + 1) % n)):
            if tops[other_edge] is None:
                ends.append((vert[0] + nx * PARAPET_T, vert[1] + ny * PARAPET_T))
            else:
                a, b = poly[other_edge], poly[(other_edge + 1) % n]
                ox, oy = inward_normal(a, b)
                ends.append((vert[0] + (nx + ox) * PARAPET_T, vert[1] + (ny + oy) * PARAPET_T))
        quad = [p, q, ends[1], ends[0]]
        made.append(prism(f"{name}_edge{i:02d}", quad, z_base, tops[i], col, mat, source))
    return made


def opening_boxes(normal, plane, a0, a1):
    """Return (cutter xy-range, panel xy-range) for a face with the given outward normal."""
    d, out, t = OPENING_DEPTH, 0.3, 0.05
    if normal == "N":
        return (a0, a1, plane - d, plane + out), (a0, a1, plane - d, plane - d + t)
    if normal == "S":
        return (a0, a1, plane - out, plane + d), (a0, a1, plane + d - t, plane + d)
    if normal == "E":
        return (plane - d, plane + out, a0, a1), (plane - d, plane - d + t, a0, a1)
    if normal == "W":
        return (plane - out, plane + d, a0, a1), (plane + d - t, plane + d, a0, a1)
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
    except Exception as exc:                       # fall back to CPU, record why
        info["error"] = str(exc)
    return info


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    do_render = "--no-render" not in argv
    global BLEND, REPORT, RENDER_DIR
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

    c_mass = collection("01_Masses")
    c_par = collection("02_Parapets")
    c_open = collection("03_Opening_panels")
    c_can = collection("04_DropOff_Canopy")
    c_site = collection("05_Site_context")
    c_cut = collection("zz_Cutters")
    c_cam = collection("06_Cameras_Lights")

    # ---- masses ----
    masses = [prism("L1_Podium", P1, AVG_GRADE, TERRACE_FF, c_mass, wall,
                    "A112 Rev5 p3 primed grids (face of stud); datums A300")]
    for zname, zone in ZONES.items():
        masses.append(prism(f"L2_{zname}", zone["poly"], TERRACE_FF, ROOF_STRUCT,
                            c_mass, wall, zone["source"]))

    # ---- parapets ----
    parapets("Par_Terrace", P1, P1_PARAPET, TERRACE_FF, c_par, wall,
             "A132 Rev5 tags TO PARAPET 19'-6\" / 17'-6\"")
    for zname, zone in ZONES.items():
        parapets(f"Par_{zname}", zone["poly"], zone["parapet"], ROOF_STRUCT, c_par, wall,
                 zone["source"])

    # ---- cutters: lobby recess first, then openings ----
    r = LOBBY_RECESS
    cutters = [box("CUT_lobby_recess", r["x0"], r["x1"], r["y_back"], GY["A'"] + 0.5,
                   r["z0"] - 0.5, r["z1"], c_cut, dark, "A112/A122 piers 3'-8\", grid A")]
    for i, (normal, plane, a0, a1, z0, z1, tag) in enumerate(OPENINGS):
        cxy, pxy = opening_boxes(normal, plane, a0, a1)
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

    # ---- drop-off canopy ----
    c = CANOPY
    x0, x1 = c["cols_x"][0] - c["end_overhang"], c["cols_x"][-1] + c["end_overhang"]
    yg, zt, t = c["y_gutter"], c["z_gutter_top"], c["glass_t"]
    for label, y_edge, run in (("south", yg - c["south"], c["south"]),
                               ("north", yg + c["north"], c["north"])):
        ze = zt + run * c["slope"]
        verts = [(x0, yg, zt - t), (x1, yg, zt - t), (x1, y_edge, ze - t), (x0, y_edge, ze - t),
                 (x0, yg, zt), (x1, yg, zt), (x1, y_edge, ze), (x0, y_edge, ze)]
        faces = [(0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
        mesh_object(f"Canopy_glass_{label}", verts, faces, c_can, canopy_mat,
                    "A700 Rev5: 65'-7 1/4\" x 23'-3\", slope 1 1/2:12; heights measured (M)")
    h = c["col_size"] / 2
    for i, cx in enumerate(c["cols_x"], 1):
        box(f"Canopy_column_X{i}", cx - h, cx + h, yg - h, yg + h, AVG_GRADE, c["col_top"],
            c_can, canopy_mat, "A700 Rev5 grid XA; size assumed (A-6)")

    # ---- minimal site context ----
    box("Ground_flat_at_average_grade", -150, 355, -120, 260, AVG_GRADE - 1.0, AVG_GRADE,
        c_site, ground_mat, "Average Grade -1'-9 3/4\" (A300); flat is an assumption (U-7)")
    ax, ay, z = 250.0, 150.0, AVG_GRADE + 0.05
    mesh_object("North_arrow", [(ax - 6, ay, z), (ax + 6, ay, z), (ax + 6, ay + 30, z),
                                (ax + 14, ay + 30, z), (ax, ay + 50, z), (ax - 14, ay + 30, z),
                                (ax - 6, ay + 30, z)], [(0, 1, 2, 3, 4, 5, 6)], c_site, context_mat,
                "Project north, A112")
    for text, loc, size in (("N", (ax - 5, ay + 54, z), 14.0),
                            ("FRONT / NORTH: parking lot, Golf Links Dr beyond", (215, 175, z), 7.0),
                            ("EXISTING BUILDING I (not modeled)", (250, -10, z), 7.0)):
        curve = bpy.data.curves.new(text[:12], "FONT")
        curve.body = text
        curve.size = m(size)
        tobj = bpy.data.objects.new("Label_" + text[:12], curve)
        tobj.location = [m(v) for v in loc]
        tobj.rotation_euler = (0, 0, math.radians(90 if text.startswith("EXISTING") else 180 if text.startswith("FRONT") else 0))
        c_site.objects.link(tobj)
        tobj.data.materials.append(context_mat)

    # ---- lights, world, cameras ----
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

    cx, cy, cz = 102.5, 58.0, 18.0
    cams = {
        "front_north": (add_camera("Cam_front_north", (cx, 500, cz), (cx, cy, cz), c_cam, 260), (2600, 900)),
        "rear_south": (add_camera("Cam_rear_south", (cx, -400, cz), (cx, cy, cz), c_cam, 260), (2600, 900)),
        "left_east": (add_camera("Cam_left_east", (600, cy + 4, cz), (cx, cy + 4, cz), c_cam, 190), (2400, 1000)),
        "right_west": (add_camera("Cam_right_west", (-400, cy + 4, cz), (cx, cy + 4, cz), c_cam, 190), (2400, 1000)),
        "oblique_northeast": (add_camera("Cam_oblique_NE", (330, 290, 150), (105, 55, 12), c_cam, None, 40.0), (2400, 1350)),
    }
    scene.camera = cams["oblique_northeast"][0]

    # ---- checks ----
    lo = [1e9] * 3
    hi = [-1e9] * 3
    for col in (c_mass, c_par):
        for obj in col.objects:
            bmin, bmax = bbox_ft(obj)
            lo = [min(a, b) for a, b in zip(lo, bmin)]
            hi = [max(a, b) for a, b in zip(hi, bmax)]
    report = {"version": VERSION, "blender": bpy.app.version_string,
              "building_bbox_ft": {"min": [round(v, 3) for v in lo], "max": [round(v, 3) for v in hi]},
              "expected_ft": {"x": 205.0, "y": 105.833, "top": HIGH_PARAPET_3},
              "boolean_cuts_applied": cut_count, "openings": len(OPENINGS),
              "objects": {col.name: len(col.objects) for col in bpy.data.collections},
              "mass_faces": {o.name: len(o.data.polygons) for o in masses}}
    assert abs((hi[0] - lo[0]) - 205.0) < 0.01, "overall X dimension check failed"
    assert abs((hi[1] - lo[1]) - 105.833) < 0.01, "overall Y dimension check failed"
    assert abs(hi[2] - HIGH_PARAPET_3) < 0.01, "top of parapet check failed"

    bpy.context.preferences.filepaths.save_version = 0   # session only: no .blend1 copies
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))

    # ---- renders ----
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
