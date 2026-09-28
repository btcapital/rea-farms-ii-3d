"""Building II print derivative v001 - preview renders of the prepared print parts (read-only, never saves).

Run:  blender -b models/Building_II/print_derivatives/building_II_print_v001.blend \
            --python scripts/3d_print/preview_print_v001.py
Writes exports/Building_II/3d_print/validation/previews/print_v001_*.png (Workbench, single clay colour,
cavity + shadows - the look of an unpainted single-colour print). Cameras exist only in memory.
"""
import bpy, math, os
from mathutils import Vector

BLEND = bpy.data.filepath
ROOT = os.path.abspath(os.path.join(os.path.dirname(BLEND), "..", "..", ".."))
OUT = os.path.join(ROOT, "exports", "Building_II", "3d_print", "validation", "previews")
os.makedirs(OUT, exist_ok=True)
sc = bpy.context.scene
PARTS = {n: bpy.data.objects[n] for n in ("PRINT_building_body", "PRINT_site_base", "PRINT_canopy_dropoff", "PRINT_sunshade")}
HOME = {n: o.location.copy() for n, o in PARTS.items()}

sc.render.engine = "BLENDER_WORKBENCH"
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1600, 1000, 100
sc.display.render_aa = "16"
sh = sc.display.shading
sh.light = "STUDIO"; sh.color_type = "SINGLE"; sh.single_color = (0.86, 0.85, 0.82)
sh.show_cavity = True; sh.cavity_type = "BOTH"; sh.cavity_ridge_factor = 1.0; sh.cavity_valley_factor = 1.2
sh.show_shadows = True; sh.shadow_intensity = 0.25; sh.show_object_outline = True; sh.object_outline_color = (0.25, 0.25, 0.25)
sc.display.light_direction = (0.45, -0.35, 0.82)
if sc.world is None:
    sc.world = bpy.data.worlds.new("preview")
sc.world.color = (0.93, 0.94, 0.95)
sc.view_settings.view_transform = "Standard"; sc.view_settings.exposure = 1.1; sc.view_settings.gamma = 1.1

cam_data = bpy.data.cameras.new("preview_cam"); cam = bpy.data.objects.new("preview_cam", cam_data)
sc.collection.objects.link(cam); sc.camera = cam

def look(loc, target, lens=35, ortho=None):
    cam.location = Vector(loc)
    cam.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    if ortho:
        cam_data.type = "ORTHO"; cam_data.ortho_scale = ortho
    else:
        cam_data.type = "PERSP"; cam_data.lens = lens
    cam_data.clip_start, cam_data.clip_end = 0.1, 2000

def show(names, offsets=None):
    for n, o in PARTS.items():
        o.hide_render = n not in names
        o.location = HOME[n] + Vector(offsets.get(n, (0, 0, 0)) if offsets else (0, 0, 0))

def shot(fname, names, loc, target, lens=35, ortho=None, offsets=None):
    show(names, offsets); look(loc, target, lens, ortho)
    sc.render.filepath = os.path.join(OUT, fname)
    bpy.ops.render.render(write_still=True)
    print("[preview]", fname)

ALL = list(PARTS)
shot("print_v001_01_assembly_northwest.png", ALL, (-38, 92, 52), (31, 22, 0), 32)
shot("print_v001_02_assembly_southeast.png", ALL, (100, -52, 55), (31, 22, 0), 32)
shot("print_v001_03_assembly_plan.png", ALL, (31.5, 23.5, 120), (31.5, 23.5, 0), ortho=86)
shot("print_v001_04_north_entrance_closeup.png", ALL, (44, 58, 10), (32, 32, 3.5), 40)
shot("print_v001_05_sunshade_terrace_southeast.png", ALL, (78, -22, 26), (42, 12, 8), 40)
shot("print_v001_06_exploded_parts.png", ALL, (-40, 95, 70), (31, 22, 12), 30,
     offsets={"PRINT_building_body": (0, 0, 16), "PRINT_canopy_dropoff": (0, 8, 34), "PRINT_sunshade": (0, 0, 32)})
shot("print_v001_07_site_base_only.png", ["PRINT_site_base"], (-30, 88, 48), (31, 22, -1), 32)
shot("print_v001_08_building_body_only_northwest.png", ["PRINT_building_body"], (-22, 68, 30), (31, 16, 5), 35)
shot("print_v001_09_canopy_part.png", ["PRINT_canopy_dropoff"], (46, 52, 12), (33.6, 36, 2.5), 45)
shot("print_v001_10_sunshade_part.png", ["PRINT_sunshade"], (72, -14, 30), (38, 14, 9.6), 38)
shot("print_v001_11_west_utility_yard.png", ALL, (-30, 6, 16), (-3, 16, 1), 40)
show(ALL)
print("[preview] done (file not saved)")
