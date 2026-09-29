"""Building II print derivative v003 - MULTICOLOR preview renders (read-only, never saves).

Run:  blender -b models/Building_II/print_derivatives/building_II_print_v003.blend \
            --python scripts/3d_print/preview_print_v003.py
Writes exports/Building_II/3d_print/validation/previews_v003/print_v003_*.png
Colours: slot 1 white = white metal panel, slot 2 black = black metal panel, slot 3 gray = gray brick / frames / steel,
slot 4 light clear-blue = glazing (clear/translucent filament). The site base is drawn neutral.

v003 colour parts are a PRIORITY OVERLAY on the exact v002 parts (Bambu Studio: a later part of an object wins where parts
overlap): body (gray) < white < black < clear < frames (gray). The overlay parts share the body's surface, so for display
only each one is moved a few millimetres per rank TOWARD THE CAMERA (sub-pixel at these camera distances) - the render
then shows the colour the slicer assigns. Nothing is saved.
"""
import bpy, math, os
from mathutils import Vector, Matrix

BLEND = bpy.data.filepath
ROOT = os.path.abspath(os.path.join(os.path.dirname(BLEND), "..", "..", ".."))
OUT = os.path.join(ROOT, "exports", "Building_II", "3d_print", "validation", "previews_v003")
os.makedirs(OUT, exist_ok=True)
sc = bpy.context.scene
COL = {"WHITE": (0.95, 0.95, 0.93, 1), "BLACK": (0.07, 0.07, 0.08, 1), "GRAY": (0.47, 0.48, 0.48, 1), "CLEAR": (0.62, 0.80, 0.90, 1),
       "SITE": (0.80, 0.79, 0.76, 1)}
# name: (colour, display rank)
PARTS = {"PRINT_building_body": ("GRAY", 0), "PRINT_building_body_WHITE": ("WHITE", 1), "PRINT_building_body_BLACK": ("BLACK", 2),
         "PRINT_building_body_CLEAR": ("CLEAR", 3), "PRINT_building_body_FRAMES": ("GRAY", 4),
         "PRINT_canopy_dropoff": ("GRAY", 0), "PRINT_canopy_dropoff_CLEAR": ("CLEAR", 1),
         "PRINT_sunshade": ("WHITE", 0), "PRINT_site_base": ("SITE", 0)}
STEP = 0.006          # m of display offset per rank (0.025 mm printed; < 0.2 px in these renders)
OBJ = {n: bpy.data.objects[n] for n in PARTS}
for n, (c, rank) in PARTS.items():
    o = OBJ[n]; o.color = COL[c]; o.hide_render = False
HOME = {n: o.matrix_world.copy() for n, o in OBJ.items()}

sc.render.engine = "BLENDER_WORKBENCH"
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1600, 1000, 100
sc.display.render_aa = "16"
sh = sc.display.shading
sh.light = "STUDIO"; sh.color_type = "OBJECT"
sh.show_cavity = True; sh.cavity_type = "BOTH"; sh.cavity_ridge_factor = 0.8; sh.cavity_valley_factor = 1.0
sh.show_shadows = True; sh.shadow_intensity = 0.25; sh.show_object_outline = True; sh.object_outline_color = (0.2, 0.2, 0.2)
sh.show_specular_highlight = True
sc.display.light_direction = (0.45, -0.35, 0.82)
if sc.world is None:
    sc.world = bpy.data.worlds.new("preview")
sc.world.color = (0.93, 0.94, 0.95)
sc.view_settings.view_transform = "Standard"; sc.view_settings.exposure = 0.9; sc.view_settings.gamma = 1.0
cam_data = bpy.data.cameras.new("cam"); cam = bpy.data.objects.new("cam", cam_data); sc.collection.objects.link(cam); sc.camera = cam

def look(loc, target, lens=35, ortho=None):
    cam.location = Vector(loc); cam.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    cam_data.type = "ORTHO" if ortho else "PERSP"
    if ortho: cam_data.ortho_scale = ortho
    else: cam_data.lens = lens
    cam_data.clip_start, cam_data.clip_end = 2.0, 600.0          # tight range: depth precision for the display offsets

def shot(fname, show, loc, target, lens=35, ortho=None, offsets=None):
    toward = (Vector(loc) - Vector(target)).normalized()          # display offset: overlay rank k moves k*STEP toward the camera
    for n, o in OBJ.items():
        o.hide_render = n not in show
        o.matrix_world = Matrix.Translation(Vector((offsets or {}).get(n, (0, 0, 0))) + toward * STEP * PARTS[n][1]) @ HOME[n]
    look(loc, target, lens, ortho)
    sc.render.filepath = os.path.join(OUT, fname); bpy.ops.render.render(write_still=True); print("[preview]", fname)

ALL = list(OBJ); BLD = [n for n in OBJ if n != "PRINT_site_base"]
shot("print_v003_01_multicolor_assembly_northwest.png", ALL, (-30, 78, 46), (29, 18, 0), 32)
shot("print_v003_02_multicolor_assembly_southeast.png", ALL, (92, -44, 50), (29, 18, 0), 32)
shot("print_v003_03_north_facade_elevation.png", BLD, (31.5, 120, 5.5), (31.5, 16, 5.5), ortho=70)
shot("print_v003_04_south_facade_elevation.png", BLD, (31.5, -90, 5.5), (31.5, 16, 5.5), ortho=70)
shot("print_v003_05_east_facade_elevation.png", BLD, (140, 16, 5.5), (31.5, 16, 5.5), ortho=40)
shot("print_v003_06_west_facade_elevation.png", BLD, (-80, 16, 5.5), (31.5, 16, 5.5), ortho=40)
shot("print_v003_07_north_entrance_closeup.png", ALL, (44, 58, 10), (32, 32, 3.5), 40)
shot("print_v003_08_roof_top_view.png", BLD, (31.5, 16.5, 120), (31.5, 16.5, 0), ortho=70)
shot("print_v003_09_exploded_colour_parts.png", BLD, (-40, 90, 60), (29, 16, 10), 30,
     offsets={"PRINT_building_body_WHITE": (0, 0, 24), "PRINT_building_body_BLACK": (0, 0, 36), "PRINT_building_body_CLEAR": (0, 0, 12),
              "PRINT_building_body_FRAMES": (0, 0, 48), "PRINT_canopy_dropoff_CLEAR": (0, 10, 40), "PRINT_sunshade": (0, 0, 60)})
shot("print_v003_10_southwest_brick_and_panels.png", BLD, (-28, -30, 22), (22, 10, 5), 35)
print("[preview] done (file not saved)", bpy.data.is_dirty)
