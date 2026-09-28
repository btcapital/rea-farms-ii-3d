"""Building II print derivative v002 - preview and comparison renders (read-only, never saves).

Run:  blender -b models/Building_II/print_derivatives/building_II_print_v002.blend \
            --python scripts/3d_print/preview_print_v002.py
Writes exports/Building_II/3d_print/validation/previews_v002/print_v002_*.png
The v001 parts are appended IN MEMORY from building_II_print_v001.blend for the comparison views only
(the v001 file is only read, never written).
"""
import bpy, math, os
from mathutils import Vector, Matrix

BLEND = bpy.data.filepath
ROOT = os.path.abspath(os.path.join(os.path.dirname(BLEND), "..", "..", ".."))
OUT = os.path.join(ROOT, "exports", "Building_II", "3d_print", "validation", "previews_v002")
os.makedirs(OUT, exist_ok=True)
sc = bpy.context.scene
NAMES = ("PRINT_building_body", "PRINT_site_base", "PRINT_canopy_dropoff", "PRINT_sunshade")
PARTS = {n: bpy.data.objects[n] for n in NAMES}
HOME = {n: o.matrix_world.copy() for n, o in PARTS.items()}
CLAY = (0.86, 0.85, 0.82, 1.0)
for o in PARTS.values():
    o.color = CLAY

sc.render.engine = "BLENDER_WORKBENCH"
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1600, 1000, 100
sc.display.render_aa = "16"
sh = sc.display.shading
sh.light = "STUDIO"; sh.color_type = "OBJECT"
sh.show_cavity = True; sh.cavity_type = "BOTH"; sh.cavity_ridge_factor = 1.0; sh.cavity_valley_factor = 1.2
sh.show_shadows = True; sh.shadow_intensity = 0.25; sh.show_object_outline = True; sh.object_outline_color = (0.25, 0.25, 0.25)
sc.display.light_direction = (0.45, -0.35, 0.82)
if sc.world is None:
    sc.world = bpy.data.worlds.new("preview")
sc.world.color = (0.93, 0.94, 0.95)
sc.view_settings.view_transform = "Standard"; sc.view_settings.exposure = 1.1; sc.view_settings.gamma = 1.1

cam_data = bpy.data.cameras.new("preview_cam"); cam = bpy.data.objects.new("preview_cam", cam_data)
sc.collection.objects.link(cam); sc.camera = cam
EXTRA = []

def look(loc, target, lens=35, ortho=None):
    cam.location = Vector(loc)
    cam.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    if ortho:
        cam_data.type = "ORTHO"; cam_data.ortho_scale = ortho
    else:
        cam_data.type = "PERSP"; cam_data.lens = lens
    cam_data.clip_start, cam_data.clip_end = 0.1, 5000

def show(names, offsets=None, extra=()):
    for n, o in PARTS.items():
        o.hide_render = n not in names
        o.matrix_world = Matrix.Translation(Vector(offsets.get(n, (0, 0, 0)) if offsets else (0, 0, 0))) @ HOME[n]
    for e in EXTRA:
        e.hide_render = e not in extra

def shot(fname, names, loc, target, lens=35, ortho=None, offsets=None, extra=()):
    show(names, offsets, extra); look(loc, target, lens, ortho)
    sc.render.filepath = os.path.join(OUT, fname)
    bpy.ops.render.render(write_still=True)
    print("[preview]", fname)

def box(name, x0, x1, y0, y1, z0, z1, color):
    me = bpy.data.meshes.new(name)
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    f = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    me.from_pydata(v, [], f); o = bpy.data.objects.new(name, me); o.color = color
    sc.collection.objects.link(o); EXTRA.append(o); return o

def frame(prefix, x0, x1, y0, y1, z, w, color):
    return [box(prefix + "_s", x0 - w, x1 + w, y0 - w, y0, z, z + w, color), box(prefix + "_n", x0 - w, x1 + w, y1, y1 + w, z, z + w, color),
            box(prefix + "_w", x0 - w, x0, y0, y1, z, z + w, color), box(prefix + "_e", x1, x1 + w, y0, y1, z, z + w, color)]

def text(name, body, loc, size, color=(0.1, 0.1, 0.1, 1)):
    cu = bpy.data.curves.new(name, "FONT"); cu.body = body; cu.size = size; cu.extrude = 0.2
    o = bpy.data.objects.new(name, cu); o.location = loc; o.color = color
    sc.collection.objects.link(o); EXTRA.append(o); return o

ALL = list(PARTS)
RED = (0.85, 0.12, 0.12, 1.0)
# ------------------------------------------------------------------ v002 views (real-metre coordinates)
shot("print_v002_01_assembly_northwest.png", ALL, (-30, 78, 46), (29, 18, 0), 32)
shot("print_v002_02_assembly_southeast.png", ALL, (92, -44, 50), (29, 18, 0), 32)
old_crop = frame("v001crop", -9.75, 72.75, -5.25, 52.25, 6.5, 0.45, RED)
lbl1 = text("lbl_old", "v001 crop (1:250)", Vector((-9.5, 53.3, 6.5)), 2.4, RED)
lbl2 = text("lbl_new", "v002 crop (1:240)", Vector((-8.8, 41.2, 6.5)), 2.4)
shot("print_v002_03_top_revised_crop_vs_v001.png", ALL, (31.5, 24.0, 150), (31.5, 24.0, 0), ortho=112, extra=old_crop + [lbl1, lbl2])
shot("print_v002_04_porte_cochere_closeup.png", ALL, (46, 50, 11), (33.6, 35.5, 3.0), 42)
shot("print_v002_05_sunshade_closeup.png", ALL, (70, -16, 24), (46, 12, 9.2), 40)
shot("print_v002_06_exploded_assembly.png", ALL, (-34, 84, 66), (29, 18, 12), 30,
     offsets={"PRINT_building_body": (0, 0, 16), "PRINT_canopy_dropoff": (0, 8, 34), "PRINT_sunshade": (0, 0, 32)})
shot("print_v002_07_site_base_only.png", ["PRINT_site_base"], (-26, 74, 44), (29, 18, -1), 32)
shot("print_v002_08_building_only.png", ["PRINT_building_body"], (-22, 68, 30), (31, 16, 5), 35)
shot("print_v002_09_porte_cochere_part_underside.png", ["PRINT_canopy_dropoff"], (40, 44, 0.8), (33.6, 35.6, 3.8), 40)
shot("print_v002_10_sunshade_part.png", ["PRINT_sunshade"], (72, -14, 30), (40, 14, 9.6), 38)

# canopy in its recommended print orientation (standing on its south edge) on a bed strip
can = PARTS["PRINT_canopy_dropoff"]
R = Matrix.Rotation(math.radians(90), 4, "X")
co = [R @ (HOME["PRINT_canopy_dropoff"] @ v.co) for v in can.data.vertices]
zmin = min(p.z for p in co); cx = sum(p.x for p in co) / len(co); cy = sum(p.y for p in co) / len(co)
can.matrix_world = Matrix.Translation(Vector((200 - cx, 200 - cy, -zmin))) @ R @ HOME["PRINT_canopy_dropoff"]
bed = box("bed_canopy", 185, 215, 190, 211, -0.2, 0.0, (0.35, 0.36, 0.38, 1))
for n, o in PARTS.items():
    o.hide_render = n != "PRINT_canopy_dropoff"
for e in EXTRA:
    e.hide_render = e is not bed
look((222, 176, 14), (200, 200, 3.2), 40)
sc.render.filepath = os.path.join(OUT, "print_v002_11_porte_cochere_print_orientation.png"); bpy.ops.render.render(write_still=True)
print("[preview] print_v002_11_porte_cochere_print_orientation.png")
can.matrix_world = HOME["PRINT_canopy_dropoff"]

# ------------------------------------------------------------------ v001 vs v002 at printed size on the H2S bed
v001 = os.path.join(os.path.dirname(BLEND), "building_II_print_v001.blend")
with bpy.data.libraries.load(v001, link=False) as (src, dst):
    dst.objects = list(NAMES)
old = []
for o in dst.objects:
    sc.collection.objects.link(o); o.color = (0.80, 0.83, 0.88, 1); old.append(o)
def place(objs, k, bed_x0):
    import numpy as np
    pts = [(o.matrix_world @ v.co) for o in objs for v in o.data.vertices]
    x0 = min(p.x for p in pts); x1 = max(p.x for p in pts); y0 = min(p.y for p in pts); y1 = max(p.y for p in pts); z0 = min(p.z for p in pts)
    cxm, cym = (x0 + x1) / 2 * k, (y0 + y1) / 2 * k
    T = Matrix.Translation(Vector((bed_x0 + 170 - cxm, 160 - cym, -z0 * k))) @ Matrix.Scale(k, 4)
    for o in objs:
        o.matrix_world = T @ o.matrix_world
beds = [box("bedA", 0, 340, 0, 320, -1.0, 0.0, (0.33, 0.34, 0.36, 1)), box("bedB", 420, 760, 0, 320, -1.0, 0.0, (0.33, 0.34, 0.36, 1))]
place(old, 1000 / 250, 0)
for n, o in PARTS.items():
    o.matrix_world = HOME[n]
place(list(PARTS.values()), 1000 / 240, 420)
labels = [text("t1", "v001  1:250   base 330 x 230 mm   building 255 x 138 x 63 mm", Vector((5, 330, 0)), 9),
          text("t2", "v002  1:240   base 318 x 190 mm   building 266 x 144 x 66 mm", Vector((425, 330, 0)), 9),
          text("t3", "Bambu H2S bed 340 x 320 mm (both at true printed size)", Vector((190, -22, 0)), 9)]
for o in PARTS.values():
    o.hide_render = False
for e in EXTRA:
    e.hide_render = e not in beds + labels
look((380, 160, 900), (380, 160, 0), ortho=800)
sc.render.filepath = os.path.join(OUT, "print_v002_12_compare_v001_v002_on_bed.png"); bpy.ops.render.render(write_still=True)
print("[preview] print_v002_12_compare_v001_v002_on_bed.png")
look((380, -420, 330), (380, 150, 0), 38)
sc.render.filepath = os.path.join(OUT, "print_v002_13_compare_v001_v002_perspective.png"); bpy.ops.render.render(write_still=True)
print("[preview] print_v002_13_compare_v001_v002_perspective.png")
print("[preview] done (file not saved)", bpy.data.is_dirty)
