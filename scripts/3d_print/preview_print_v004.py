"""Building II print derivative v004 - MULTICOLOR SITE BASE preview renders (read-only, never saves).

Run:  python scripts/3d_print/preview_print_v004.py          (Blender 5.2 Python module; Cycles CPU, no GPU needed)
Writes exports/Building_II/3d_print/validation/previews_v004/print_v004_*.png
Sources (opened read-only): building_II_print_v004.blend (site base + its colour parts) and, for the assembled views, the
approved v003 building / drop-off canopy / sun-shade parts appended from building_II_print_v003.blend (unchanged).
Colours = the print filaments: green (slot 4), black (slot 2), gray (slot 3), and for the v003 companions white (1),
black (2), gray (3), clear (4, drawn light clear-blue).
The colour parts are a PRIORITY OVERLAY (Bambu Studio: a later part wins where parts overlap) and share the base's
surface, so for display only each overlay part is moved a few millimetres per rank TOWARD THE CAMERA (sub-pixel at these
camera distances) - the render then shows the colour the slicer assigns (same method as preview_print_v003.py).
"""
import bpy, math, os, sys
from mathutils import Vector

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DER = os.path.join(ROOT, "models", "Building_II", "print_derivatives")
OUT = os.path.join(ROOT, "exports", "Building_II", "3d_print", "validation", "previews_v004")
os.makedirs(OUT, exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=os.path.join(DER, "building_II_print_v004.blend"), load_ui=False)
with bpy.data.libraries.load(os.path.join(DER, "building_II_print_v003.blend"), link=False) as (src, dst):
    dst.objects = [n for n in src.objects if n.startswith(("PRINT_building_body", "PRINT_canopy_dropoff", "PRINT_sunshade"))]
sc = bpy.context.scene
for o in dst.objects:
    sc.collection.objects.link(o)
COL = {"WHITE": (0.92, 0.92, 0.90), "BLACK": (0.045, 0.045, 0.05), "GRAY": (0.42, 0.43, 0.43), "CLEAR": (0.62, 0.80, 0.90),
       "GREEN": (0.13, 0.33, 0.12)}
PARTS = {"PRINT_site_base": ("GRAY", 0), "PRINT_site_base_GREEN": ("GREEN", 1), "PRINT_site_base_BLACK": ("BLACK", 2),
         "PRINT_building_body": ("GRAY", 0), "PRINT_building_body_WHITE": ("WHITE", 1), "PRINT_building_body_BLACK": ("BLACK", 2),
         "PRINT_building_body_CLEAR": ("CLEAR", 3), "PRINT_building_body_FRAMES": ("GRAY", 4),
         "PRINT_canopy_dropoff": ("GRAY", 0), "PRINT_canopy_dropoff_CLEAR": ("CLEAR", 1), "PRINT_sunshade": ("WHITE", 0)}
SITE = [n for n in PARTS if n.startswith("PRINT_site")]
ALL = list(PARTS)
MATS = {}
for c, rgb in COL.items():
    m = bpy.data.materials.new("PV_" + c); m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]; bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.62 if c != "CLEAR" else 0.25
    MATS[c] = m
OBJ = {n: bpy.data.objects[n] for n in PARTS}
for n, (c, rank) in PARTS.items():
    o = OBJ[n]; o.data.materials.clear(); o.data.materials.append(MATS[c])
    for p in o.data.polygons:
        p.use_smooth = False
HOME = {n: o.matrix_world.copy() for n, o in OBJ.items()}

sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = 96; sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1600, 1000, 100
sc.view_settings.view_transform = "Standard"; sc.view_settings.exposure = -0.85
world = bpy.data.worlds.new("preview"); sc.world = world; world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.93, 0.94, 0.95, 1.0)
sc.render.film_transparent = False
world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.45
sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN")); sc.collection.objects.link(sun)
sun.data.energy = 2.6; sun.data.angle = math.radians(8); sun.rotation_euler = (math.radians(38), math.radians(-18), math.radians(-35))
cam_data = bpy.data.cameras.new("cam"); cam = bpy.data.objects.new("cam", cam_data); sc.collection.objects.link(cam); sc.camera = cam
STEP = 0.006          # m of display offset per rank (0.025 mm printed; sub-pixel in these renders)

def shot(fname, show, loc, target, lens=35, ortho=None):
    toward = (Vector(loc) - Vector(target)).normalized()
    for n, o in OBJ.items():
        o.hide_render = n not in show
        o.matrix_world = HOME[n].copy(); o.matrix_world.translation += toward * STEP * PARTS[n][1]
    cam.location = Vector(loc); cam.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    cam_data.type = "ORTHO" if ortho else "PERSP"
    if ortho:
        cam_data.ortho_scale = ortho
    else:
        cam_data.lens = lens
    cam_data.clip_start, cam_data.clip_end = 1.0, 800.0
    sc.render.filepath = os.path.join(OUT, fname)
    bpy.ops.render.render(write_still=True)
    print("[preview v004]", fname)

only = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
SHOTS = [
    ("print_v004_01_site_base_oblique_northwest.png", SITE, (-38, 82, 58), (29, 17, -1), 32, None),
    ("print_v004_02_site_base_top_plan.png", SITE, (29.1, 17.75, 150), (29.1, 17.75, 0), 35, 82),
    ("print_v004_03_site_closeup_entry_landscape_paving.png", SITE, (2, 58, 16), (22, 33, -0.5), 35, None),
    ("print_v004_04_site_closeup_southwest_yard_stairs.png", SITE, (-24, -26, 18), (2, 6, -0.5), 35, None),
    ("print_v004_05_assembled_oblique_northwest.png", ALL, (-38, 82, 58), (29, 17, 2), 32, None),
    ("print_v004_06_assembled_oblique_southeast.png", ALL, (98, -46, 52), (29, 17, 2), 32, None),
    ("print_v004_07_assembled_north_entry_closeup.png", ALL, (14, 70, 18), (32, 30, 3), 35, None),
]
for fname, show, loc, target, lens, ortho in SHOTS:
    if not only or any(k in fname for k in only):
        shot(fname, show, loc, target, lens, ortho)
