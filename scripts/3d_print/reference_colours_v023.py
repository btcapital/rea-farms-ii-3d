"""Expected-colour reference renders from the approved v023 visualization model (READ-ONLY, never saved).

Run:  blender -b models/Building_II/building_shell_v023.blend --python scripts/3d_print/reference_colours_v023.py
Colours every exterior face from its documented material with the owner's controlling filament mapping
(white metal panel / black metal panel / gray brick+frames+steel / clear glazing; roofs+terrace white), using
the same cameras and flat colours as preview_print_v003.py, so the print colouring can be compared side by side.
Writes exports/Building_II/3d_print/validation/previews_v003/reference_v023_*.png
"""
import bpy, os
from mathutils import Vector

BLEND = bpy.data.filepath
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(BLEND)))
OUT = os.path.join(ROOT, "exports", "Building_II", "3d_print", "validation", "previews_v003")
os.makedirs(OUT, exist_ok=True)
sc = bpy.context.scene
COL = {"WHITE": (0.95, 0.95, 0.93, 1), "BLACK": (0.07, 0.07, 0.08, 1), "GRAY": (0.47, 0.48, 0.48, 1), "CLEAR": (0.62, 0.80, 0.90, 1)}
def colour_of_material(m):
    if m.startswith(("ACM-1", "ACM-4", "MTL-2", "TPO", "UNRES-colour_terrace_pavers", "PAINT_match_ACM-1")): return "WHITE"
    if m.startswith(("ACM-2", "ACM-3", "MTL-1", "MTL-3")): return "BLACK"
    if m.startswith("GLASS"): return "CLEAR"
    return "GRAY"
SHOW = ["01_Masses", "02_Parapets", "03_Opening_panels", "04_DropOff_Canopy", "05_Door_Side_Canopies", "06_SunShade", "07_Glass_Railings", "11_Facade_Detail_v004"]
keep = set()
for cn in SHOW:
    for o in bpy.data.collections[cn].all_objects:
        keep.add(o.name)
for o in sc.objects:
    o.hide_render = o.name not in keep
for m in bpy.data.materials:
    m.diffuse_color = COL[colour_of_material(m.name)]
sc.render.engine = "BLENDER_WORKBENCH"
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1600, 1000, 100
sc.display.render_aa = "16"
sh = sc.display.shading
sh.light = "STUDIO"; sh.color_type = "MATERIAL"
sh.show_cavity = True; sh.cavity_type = "BOTH"; sh.cavity_ridge_factor = 0.8; sh.cavity_valley_factor = 1.0
sh.show_shadows = True; sh.shadow_intensity = 0.25; sh.show_object_outline = True; sh.object_outline_color = (0.2, 0.2, 0.2)
sc.display.light_direction = (0.45, -0.35, 0.82)
if sc.world is None:
    sc.world = bpy.data.worlds.new("preview")
sc.world.color = (0.93, 0.94, 0.95)
sc.view_settings.view_transform = "Standard"; sc.view_settings.exposure = 0.9; sc.view_settings.gamma = 1.0
cd = bpy.data.cameras.new("refcam"); cam = bpy.data.objects.new("refcam", cd); sc.collection.objects.link(cam); sc.camera = cam
def shot(fname, loc, target, lens=35, ortho=None):
    cam.location = Vector(loc); cam.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    cd.type = "ORTHO" if ortho else "PERSP"
    if ortho: cd.ortho_scale = ortho
    else: cd.lens = lens
    cd.clip_start, cd.clip_end = 0.1, 5000
    sc.render.filepath = os.path.join(OUT, fname); bpy.ops.render.render(write_still=True); print("[ref]", fname)
shot("reference_v023_03_north_facade_elevation.png", (31.5, 120, 5.5), (31.5, 16, 5.5), ortho=70)
shot("reference_v023_04_south_facade_elevation.png", (31.5, -90, 5.5), (31.5, 16, 5.5), ortho=70)
shot("reference_v023_05_east_facade_elevation.png", (140, 16, 5.5), (31.5, 16, 5.5), ortho=40)
shot("reference_v023_06_west_facade_elevation.png", (-80, 16, 5.5), (31.5, 16, 5.5), ortho=40)
shot("reference_v023_08_roof_top_view.png", (31.5, 16.5, 120), (31.5, 16.5, 0), ortho=70)
shot("reference_v023_10_southwest.png", (-28, -30, 22), (22, 10, 5), 35)
print("[ref] done (v023 not saved)", bpy.data.is_dirty)
