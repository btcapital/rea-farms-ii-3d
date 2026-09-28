"""Rea Farms II 3D - viewer v026: browser-viewer export from the APPROVED v023 model (lobby baseline) - final polish of v025.

v026 change over v025 (viewer-only): walnut texture with a subtle fine vertical grain octave, stronger board-to-board variation and a
slightly less red base. Everything else (materials, pools, data) identical to v025; data asserted equal to viewer v024 as before.

--- v025 header follows ---
Rea Farms II 3D - viewer v025: browser-viewer export from the APPROVED v023 model (lobby baseline) - visual tuning of v024.

v025 changes over v024 (viewer-only, model untouched): regenerated walnut texture (fine linear vertical grain from 1-D value noise,
low contrast, neutral brown, 8 ft repeat), softer graze pools, refined material overrides (glass clearer, cushions off-white, bronze
softer, pendant emitters warmer / dimmer). Data (grids, stair surfaces, viewpoints) is asserted identical to viewer v024.

--- v024 header follows ---
Rea Farms II 3D - viewer v024: browser-viewer export from the APPROVED v023 model (lobby baseline).

v024 additions over v022: simplified furniture collision footprints (chairs, tables, planters) in the lobby walk grid; a baked
warm graze pool below each of the 64 wall fixtures (viewer-only stand-in for the Cycles spot lights); refreshed material
overrides matching the v023 look; Lobby - Seating viewpoint read from the v023 review camera. Stair 1 navigation surface is
asserted identical to viewer v020; every grid cell that differs from v020 is asserted to lie inside a furniture footprint.

--- v022 header follows ---
Rea Farms II 3D - viewer v022: browser-viewer export from the v021 model (Lobby Concept A, Pass 1 + Pass 2 FF&E).

Same pipeline and navigation as viewer v020: the walk grids and the Stair 1 surface are computed by the identical rules and
asserted identical to viewer_v020/assets/viewer_data_v020.json (Pass 2 loose objects LOB_A_P2_* are NOT collision blockers).

--- v020 header follows ---
Rea Farms II 3D - viewer v020: browser-viewer export from the v019 model (Lobby Concept A, Pass 1).

MODEL version = v023 (models/building_shell_v023.blend).  VIEWER version = v026 (viewer_v026/).
Reads the v019 .blend and NEVER saves it (opened, regrouped in memory, exported, session discarded). No architectural
geometry is created, moved or edited. Viewer-only work done in memory: objects are grouped / joined per browser group,
Cycles materials are flattened to plain glTF colours (with viewer-specific colour, emissive and wood-grain overrides for
the lobby so that the design intent stays recognizable), 64 Blender lights are NOT exported (fixtures are emissive).

Writes (refuses to overwrite):
  exports/building_II_model_v019_viewer_v020.glb          glTF binary, Y-up, metres
  viewer_v020/models/building_II_model_v019_viewer_v020.glb   identical copy used by the viewer
  viewer_v020/assets/viewer_data_v020.json                groups, floors, walk grids, Stair 1 navigation surface,
                                                          tenant concept (rooms, viewpoints, underlay), lobby concept
  viewer_v020/assets/tenant_underlay_Concept_A_CNSA_ASC_v015.png   copy of the registered underlay image

Run (Blender 5.2):  blender --background --python scripts/export_viewer_v026.py [-- --data-only]
  --data-only : rewrite only the data JSON (GLB must already exist); used while tuning viewpoints.
See notes/browser_viewer_control_v026.md.
"""
import hashlib
import json
import math
import shutil
import struct
import sys
from pathlib import Path

import bpy
import numpy as np
from mathutils import Matrix, Vector

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "models" / "building_shell_v023.blend"
GLB = ROOT / "exports" / "building_II_model_v023_viewer_v026.glb"
VIEWER = ROOT / "viewer_v026"
V024_DATA = ROOT / "viewer_v024" / "assets" / "viewer_data_v024.json"
V020_DATA = ROOT / "viewer_v020" / "assets" / "viewer_data_v020.json"
GLB_COPY = VIEWER / "models" / GLB.name
DATA = VIEWER / "assets" / "viewer_data_v026.json"
UNDERLAY_SRC = ROOT / "exports" / "tenant_underlay_Concept_A_CNSA_ASC_v015.png"
UNDERLAY_COPY = VIEWER / "assets" / UNDERLAY_SRC.name
SCHEDULE_SRC = ROOT / "notes" / "tenant_concept_A_CNSA_ASC_room_schedule_v023.json"   # byte-identical to the v015 schedule
FT = 0.3048
CONCEPT = "Concept_A_CNSA_ASC"
LOBBY_GROUP = "GRP_Lobby_Concept_A"
LOBBY_SUBS = ["ARCH_WOOD_WALL", "ARCH_STAIR_FINISH", "ARCH_GUARDRAIL", "LIGHT_DECORATIVE", "LIGHT_FEATURE_WALL", "FINISH_FLOOR",
              "FINISH_WALL", "FF&E_SEATING", "FF&E_TABLES", "FF&E_PLANTERS", "SIGNAGE_DIRECTORY", "ART_DECOR"]
DATA_ONLY = "--data-only" in sys.argv

GROUPS = {
    "GRP_Exterior_Solid_Shell": "Building II exterior: solid masses and opening panels (v001-v005). Hidden automatically in walk / plan mode.",
    "GRP_Exterior_Envelope": "Building II exterior: terrace parapets, canopies, glass railings, facade detail, utility yard",
    "GRP_Exterior_Upper": "Building II exterior above Level 2: roof parapets and sun-shade (upper obstruction)",
    "GRP_Base_Interior_Level_1": "Base building interior, Level 1 (v014): inside shell with glazing, slabs, columns, core, stairs, elevator, service rooms",
    "GRP_Base_Interior_Level_2": "Base building interior, Level 2 and terrace slab (v014) (upper obstruction)",
    "GRP_Base_Interior_Roof": "Roof deck lid (v014) (upper obstruction)",
    "GRP_Concept_A_CNSA_ASC": "Tenant concept A - CNSA ASC (v015): partitions, dividers, tables, markers, room plates",
    LOBBY_GROUP: "Lobby Concept A (v023 approved baseline = v019 Pass 1 + Pass 2 + v023 refinement): wood feature wall, wall lights with baked graze, stair finishes, guard shoes / rails, coffer, "
                 "pendants, porcelain floor, banquettes, wall paint, directory massing. Toggle this one node to compare base vs concept.",
    "GRP_Site_Context": "Site, context, site detail and backdrop (v006-v013)",
    "GRP_Landscaping": "Building II landscaping (v008-v012)",
}
# face-of-stud Level 1 outline (v001 control polygon) - used only for the walk grid
P1 = [(5, 0), (82.875, 0), (82.875, 2), (94.125, 2), (94.125, 0), (147.875, 0), (147.875, 2), (203, 2), (203, 23.056), (205, 23.056),
      (205, 97.833), (144.5, 97.833), (144.5, 105.833), (104.646, 105.833), (104.646, 104.417), (94.375, 104.417), (94.375, 104.917),
      (0, 104.917), (0, 57.604), (5, 57.604)]
EXTRA_BLOCK = [(135.75, 143.08, 72.58, 82.58, "elevator hoistway (pit at -5 ft): not walkable")]
GRID_CELL, GRID_X0, GRID_Y0, GRID_NX, GRID_NY = 0.25, -2.0, -2.0, 840, 444
FURNITURE_RECTS = []
WLC_BODY_BOXES = []               # v024: fixture body bounding boxes (feet) recorded before the meshes are joined              # v024: (name, [x0, x1, y0, y1]) simplified footprints of chairs, tables and planter pots (filled in main)
L2_FF = 16.0                      # W: Level 02 finish floor 16'-0"
WALK_LOW, WALK_HIGH = 0.5, 6.5    # blocking band above a floor (unchanged since v016)
EYE_FT = 5.5                      # 5'-6"

# ---------------------------------------------------------------- viewer-only material treatment of the lobby (v019 master untouched)
# rgb = plain base colour (linear), rough / metal = glTF factors, emit = emissive colour + strength (fixtures read as lit without web lights),
# tex = "grain" applies the generated vertical wood-grain image (box-projected UVs, 4 ft repeat).
VIEWER_MATERIALS = {
    "LOB_A_PL-01_walnut_laminate": dict(rgb=(0.35, 0.21, 0.115), rough=0.55, tex="grain"),
    "LOB_A_WD-01_walnut_tread": dict(rgb=(0.30, 0.185, 0.105), rough=0.55, tex="grain"),
    "LOB_A_dark_metal_PT-02_gunmetal": dict(rgb=(0.135, 0.138, 0.148), rough=0.5, metal=0.4),   # v023 charcoal / gunmetal
    "LOB_A_PT-02_Scuffmaster_metal": dict(rgb=(0.22, 0.22, 0.24), rough=0.4, metal=0.6),
    "LOB_A_black_fixture": dict(rgb=(0.06, 0.06, 0.065), rough=0.6, metal=0.3),
    "LOB_A_PT-01_SW7646_First_Star": dict(rgb=(0.80, 0.79, 0.74), rough=0.85),
    "LOB_A_POR-01_Santorini_Gray_47in": dict(rgb=(0.64, 0.63, 0.60), rough=0.55),
    "LOB_A_grout_custom_643_warm_gray": dict(rgb=(0.42, 0.40, 0.37), rough=0.9),
    "LOB_A_POR-02_plinth_tile": dict(rgb=(0.55, 0.54, 0.51), rough=0.55),
    "LOB_A_WOM-01_walk_off": dict(rgb=(0.16, 0.16, 0.16), rough=0.95),
    "LOB_A_FAB-01_leather": dict(rgb=(0.28, 0.23, 0.19), rough=0.6),
    "LOB_A_display_screen_off": dict(rgb=(0.05, 0.05, 0.06), rough=0.2),
    "LOB_A_SH1_ring_emitter_3500K": dict(rgb=(1.0, 0.86, 0.68), rough=0.5, emit=((1.0, 0.84, 0.64), 1.5)),
    "LOB_A_WLC_lens_3500K": dict(rgb=(1.0, 0.80, 0.55), rough=0.5, emit=((1.0, 0.78, 0.50), 1.6)),   # v023: 3/8 in. exit slot
    "LOB_A_LT-02_track_slot_3500K": dict(rgb=(1.0, 0.90, 0.75), rough=0.5, emit=((1.0, 0.90, 0.75), 1.5)),
    # ---- Pass 2 (v021) ----
    "LOB_A_P2_chair_frame_walnut": dict(rgb=(0.32, 0.20, 0.12), rough=0.55, tex="grain"),
    "LOB_A_P2_chair_cushion_fabric": dict(rgb=(0.84, 0.81, 0.75), rough=0.97),
    "LOB_A_V23_cable_dark": dict(rgb=(0.05, 0.05, 0.052), rough=0.6, metal=0.5),
    "LOB_A_P2_table_dark_bronze": dict(rgb=(0.13, 0.105, 0.09), rough=0.5, metal=0.6),
    "LOB_A_P2_SP-01_planter_gray_speck": dict(rgb=(0.48, 0.48, 0.47), rough=0.75),
    "LOB_A_P2_planter_soil": dict(rgb=(0.14, 0.10, 0.07), rough=0.95),
    "LOB_A_P2_plant_trunk": dict(rgb=(0.24, 0.18, 0.13), rough=0.85),
    "LOB_A_P2_plant_foliage": dict(rgb=(0.15, 0.29, 0.13), rough=0.8),
    "LOB_A_P2_art_frame_black": dict(rgb=(0.06, 0.06, 0.065), rough=0.45, metal=0.2),
    "LOB_A_P2_art_A1_abstract": dict(rgb=(0.6, 0.65, 0.7), rough=0.7, tex="keep"),
    "LOB_A_P2_art_A2_abstract": dict(rgb=(0.6, 0.65, 0.7), rough=0.7, tex="keep"),
    "LOB_A_P2_directory_screen_on_neutral": dict(rgb=(0.08, 0.09, 0.11), rough=0.2, tex="keep", emit=((1.0, 1.0, 1.0), 1.0)),
    "LOB_A_P2_DP-01_Clarus_CBC-201_glass": dict(rgb=(0.56, 0.67, 0.75), rough=0.1),
    "LOB_A_P2_TR-05_brushed_stainless": dict(rgb=(0.62, 0.62, 0.60), rough=0.35, metal=0.9),
}
# fourth browser viewpoint (viewer only; no Blender camera was added): east side of the lobby looking west-north-west and up
FEATURE_WALL_VIEW = {"id": "LV_04_feature_wall", "title": "Lobby - Feature Wall", "position_ft": (137.5, 95.5, EYE_FT), "target_ft": (109.0, 84.5, 12.5), "lens_mm": 16.0}
LOBBY_ORBIT = {"target_ft": (116.0, 86.0, 10.0), "position_ft": (146.0, 124.0, 40.0)}   # looks down into the two-storey void from the north-east


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def bbox_ft(obj):
    pts = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    return [min(p[i] for p in pts) / FT for i in range(3)], [max(p[i] for p in pts) / FT for i in range(3)]


def inside(pt, poly):
    x, y, c = pt[0], pt[1], False
    for i in range(len(poly)):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % len(poly)]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            c = not c
    return c


def classify(obj):
    """Return the browser group for a v019 object, or None if it is not exported."""
    cols = [c.name for c in obj.users_collection]
    name = obj.name
    if obj.type != "MESH" or not cols or "zz_Cutters" in cols:
        return None
    if name.startswith("LOB_A_"):
        return LOBBY_GROUP
    if name.startswith("TEN_A_"):
        kind = obj.get("kind", "")
        if kind in ("underlay", "perimeter_outline"):
            return None
        return "GRP_Concept_A_CNSA_ASC"
    if name.startswith("INT_"):
        level = obj.get("level")
        if level in (1, "lid1"):
            return "GRP_Base_Interior_Level_1"
        if level == "roof":
            return "GRP_Base_Interior_Roof"
        return "GRP_Base_Interior_Level_2"
    if obj.hide_render:
        return None
    first = cols[0]
    if first in ("01_Masses", "03_Opening_panels"):
        return "GRP_Exterior_Solid_Shell"
    if first[:2] in ("02", "04", "05", "06", "07", "08", "11"):
        return "GRP_Exterior_Upper" if bbox_ft(obj)[0][2] >= 15.0 and first[:2] in ("02", "06") else "GRP_Exterior_Envelope"
    if first.startswith("12_"):
        return "GRP_Landscaping"
    if first[:2] in ("09", "13", "14", "15"):
        return "GRP_Site_Context"
    return None


def _noise1d(n, cells, rng):
    """Smooth 1-D value noise, n samples over `cells` random control points (tileable: first == last)."""
    pts = rng.uniform(-1.0, 1.0, cells + 1)
    pts[-1] = pts[0]
    x = np.linspace(0, cells, n, endpoint=False)
    i = np.floor(x).astype(int)
    t = x - i
    t = t * t * (3 - 2 * t)
    return pts[i] * (1 - t) + pts[i + 1] * t


def make_grain_image():
    """v025 viewer-only walnut laminate (Wilsonart Uptown Walnut intent): fine, linear, vertical grain built from tileable 1-D value
    noise across the width (no periodic terms), a slow drift along the height, low contrast (+/-9 %), neutral mid-dark brown.
    Mapped at an 8 ft repeat by box_uvs."""
    w, h = 1024, 2048
    rng = np.random.default_rng(31)
    g = np.zeros(w)
    for cells, amp in ((28, 1.0), (72, 0.6), (190, 0.38), (480, 0.26), (1024, 0.20)):   # v026: + fine grain octave
        g += amp * _noise1d(w, cells, rng)
    g /= 2.44
    drift = _noise1d(h, 7, rng) * 5.0                                          # +/- 5 px lateral drift along the grain
    field = np.empty((h, w))
    for j in range(h):
        field[j] = np.roll(g, int(round(drift[j])))
    lowv = _noise1d(h, 5, rng)[:, None] * 0.025                                 # very slow tonal change along the height
    lowu = (_noise1d(w, 12, rng) * 0.045 + _noise1d(w, 3, rng) * 0.02)[None, :]   # v026: board-to-board (about 8 in.) + wide drift
    tone = 1.0 + 0.11 * field + lowv + lowu                                  # v026: 0.09 -> 0.11 (still low contrast)
    base = np.array([0.28, 0.188, 0.122])                                    # v026: slightly less red / orange
    rgb = np.clip(base[None, None, :] * tone[:, :, None], 0, 1)
    rgba = np.concatenate([rgb, np.ones((h, w, 1))], axis=2).astype(np.float32)
    img = bpy.data.images.new("LOB_A_walnut_grain_viewer_v026", w, h, alpha=False)
    img.pixels.foreach_set(rgba.ravel())
    img.pack()
    return img


def make_pool_image():
    """Warm light pool (RGBA) below a wall fixture: bright at the top centre, widening and fading downward. Viewer only."""
    w, h = 128, 256
    v = np.linspace(0, 1, h)[:, None]                     # 0 = bottom, 1 = top (image row 0 is the bottom in Blender)
    u = np.linspace(0, 1, w)[None, :]
    width = 0.15 + 0.42 * (1.0 - v)                                          # v025: wider, softer
    a = np.exp(-2.1 * (1.0 - v)) * np.exp(-((u - 0.5) / width) ** 2 * 1.5) * 0.62
    a = np.clip(a, 0, 1)
    rgb = np.stack([np.full_like(a, 1.0), np.full_like(a, 0.80), np.full_like(a, 0.55)], axis=-1)
    rgba = np.concatenate([rgb, a[..., None]], axis=2).astype(np.float32)
    img = bpy.data.images.new("LOB_A_V24_wall_graze_pool_img", w, h, alpha=True)
    img.pixels.foreach_set(rgba.ravel())
    img.pack()
    return img


def make_graze_pools(bodies, col):
    """One mesh of trapezoid quads (one below each fixture) with the pool image, alpha-blended and emissive (viewer only)."""
    img = make_pool_image()
    mat = bpy.data.materials.new("LOB_A_V24_wall_graze_pool")
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out, b, tex = nt.nodes.new("ShaderNodeOutputMaterial"), nt.nodes.new("ShaderNodeBsdfPrincipled"), nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    nt.links.new(tex.outputs["Color"], b.inputs["Base Color"])
    nt.links.new(tex.outputs["Alpha"], b.inputs["Alpha"])
    nt.links.new(tex.outputs["Color"], b.inputs["Emission Color"])
    b.inputs["Emission Strength"].default_value = 0.75                       # v025
    b.inputs["Roughness"].default_value = 1.0
    nt.links.new(b.outputs[0], out.inputs["Surface"])
    try:
        mat.surface_render_method = "BLENDED"
    except AttributeError:
        mat.blend_method = "BLEND"
    mat.use_backface_culling = False
    x_plane = 106.59 + 0.75 / 12 + 2.4 / 12 + 0.012                # just in front of the box faces (field + box depth)
    verts, faces = [], []
    for lo, hi in bodies:
        yc, zt = (lo[1] + hi[1]) / 2, lo[2] - 0.01
        zb, wt, wb = zt - 2.8, 0.7, 1.9                                     # v025: larger, softer pool
        base = len(verts)
        verts += [(x_plane, yc - wb / 2, zb), (x_plane, yc + wb / 2, zb), (x_plane, yc + wt / 2, zt), (x_plane, yc - wt / 2, zt)]
        faces.append((base, base + 1, base + 2, base + 3))
    me = bpy.data.meshes.new("LOBBY_A__LIGHT_FEATURE_WALL_graze")
    me.from_pydata([(v[0] * FT, v[1] * FT, v[2] * FT) for v in verts], [], faces)
    me.update()
    uv = me.uv_layers.new(name="UVMap")
    for li, loop in enumerate(me.loops):
        k = loop.vertex_index % 4
        uv.data[li].uv = ((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0))[k]
    me.materials.append(mat)
    obj = bpy.data.objects.new("LOBBY_A__LIGHT_FEATURE_WALL_graze", me)
    col.objects.link(obj)
    obj["viewer_only"] = "baked warm graze pools standing in for the 64 Cycles spot lights (v024); not a model element"
    return obj


def box_uvs(obj, repeat_ft=4.0):
    """Box-projected UVs in world feet (viewer only, in memory): grain runs along texture v = model z on vertical faces."""
    me = obj.data
    uv = me.uv_layers.new(name="UVMap") if not me.uv_layers else me.uv_layers[0]
    mw = obj.matrix_world
    rot = mw.to_3x3()
    for poly in me.polygons:
        n = (rot @ poly.normal).normalized()
        ax, ay, az = abs(n.x), abs(n.y), abs(n.z)
        for li in poly.loop_indices:
            p = (mw @ me.vertices[me.loops[li].vertex_index].co) / FT
            if az >= ax and az >= ay:
                a, b = p.y, p.x          # horizontal face (tread tops): stripes vary with y -> grain along x
            elif ax >= ay:
                a, b = p.y, p.z          # face normal +-x (the wood wall): stripes vary with y, grain vertical
            else:
                a, b = p.x, p.z
            uv.data[li].uv = (a / repeat_ft, b / repeat_ft)


def flatten_material(mat, grain_img):
    """Replace a (possibly procedural) Cycles material by a plain glTF-friendly one, in memory only."""
    ov = VIEWER_MATERIALS.get(mat.name)
    keep_img = None
    if ov and ov.get("tex") == "keep" and mat.use_nodes:
        for n in mat.node_tree.nodes:
            if n.bl_idname == "ShaderNodeTexImage" and n.image:
                keep_img = n.image
    colour = list(mat.diffuse_color)
    rough, alpha, glass, metal, emit = 0.8, 1.0, False, 0.0, None
    if mat.use_nodes:
        b = mat.node_tree.nodes.get("Principled BSDF")
        if b:
            if not b.inputs["Base Color"].is_linked:
                colour = list(b.inputs["Base Color"].default_value)
            if not b.inputs["Roughness"].is_linked:
                rough = b.inputs["Roughness"].default_value
            for key in ("Transmission Weight", "Transmission"):
                if key in b.inputs and b.inputs[key].default_value > 0.5:
                    glass = True
        else:
            glass = any(n.bl_idname == "ShaderNodeBsdfTransparent" for n in mat.node_tree.nodes)
    if glass or "glass" in mat.name.lower():
        colour, rough, alpha = [0.76, 0.83, 0.87, 1.0], 0.08, 0.20              # v025: clearer, less milky glass
    if ov:
        colour, rough, metal, emit = list(ov["rgb"]) + [1.0], ov.get("rough", 0.6), ov.get("metal", 0.0), ov.get("emit")
    mat.use_nodes = True
    nt = mat.node_tree
    for node in list(nt.nodes):
        nt.nodes.remove(node)
    out, b = nt.nodes.new("ShaderNodeOutputMaterial"), nt.nodes.new("ShaderNodeBsdfPrincipled")
    b.inputs["Base Color"].default_value = (colour[0], colour[1], colour[2], 1.0)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    b.inputs["Alpha"].default_value = alpha
    if emit:
        b.inputs["Emission Color"].default_value = (emit[0][0], emit[0][1], emit[0][2], 1.0)
        b.inputs["Emission Strength"].default_value = emit[1]
    if ov and ov.get("tex") == "grain":
        tex = nt.nodes.new("ShaderNodeTexImage")
        tex.image = grain_img
        nt.links.new(tex.outputs["Color"], b.inputs["Base Color"])
    if keep_img is not None:                                            # v022: generated art / directory images from the v021 master
        tex = nt.nodes.new("ShaderNodeTexImage")
        tex.image = keep_img
        nt.links.new(tex.outputs["Color"], b.inputs["Base Color"])
        if emit:
            nt.links.new(tex.outputs["Color"], b.inputs["Emission Color"])
    nt.links.new(b.outputs[0], out.inputs["Surface"])
    if alpha < 1.0:
        try:
            mat.surface_render_method = "BLENDED"
        except AttributeError:
            mat.blend_method = "BLEND"
    mat.use_backface_culling = False


def rle_rows(blocked, nx, ny):
    rows = []
    for j in range(ny):
        runs, cur, n = [], 0, 0
        for i in range(nx):
            v = blocked[j * nx + i]
            if v == cur:
                n += 1
            else:
                runs.append(n)
                cur, n = v, 1
        runs.append(n)
        rows.append(runs)
    return rows


def cells_of(lo, hi):
    i0, i1 = int((lo[0] - GRID_X0) / GRID_CELL), int((hi[0] - GRID_X0) / GRID_CELL)
    j0, j1 = int((lo[1] - GRID_Y0) / GRID_CELL), int((hi[1] - GRID_Y0) / GRID_CELL)
    for j in range(max(0, j0), min(GRID_NY - 1, j1) + 1):
        for i in range(max(0, i0), min(GRID_NX - 1, i1) + 1):
            yield j * GRID_NX + i


def stair1_surfaces():
    """Viewer-only navigation surface for Stair 1, derived from the frozen v014 tread / landing objects (read, not edited).
    Each run is a straight ramp through the tread centres (mid-tread), so the camera climbs without stepping; the landing is a plane.
    The L-shaped route Level 1 -> run 1 -> landing -> run 2 -> Level 2 is kept; no shortcut."""
    def objs(prefix):
        return sorted((o for o in bpy.data.objects if o.type == "MESH" and o.name.startswith(prefix)), key=lambda o: o.name)
    r1, r2, land = objs("INT_Stair1_run1_tread_"), objs("INT_Stair1_run2_tread_"), bpy.data.objects["INT_Stair1_landing"]
    b1 = [bbox_ft(o) for o in r1]
    b2 = [bbox_ft(o) for o in r2]
    bl = bbox_ft(land)
    y_bot, y_top = max(b[1][1] for b in b1), min(b[0][1] for b in b1)          # run 1 climbs toward -y (south)
    x_bot, x_top = min(b[0][0] for b in b2), max(b[1][0] for b in b2)          # run 2 climbs toward +x (east)
    riser1, tread1 = max(b[1][2] for b in b1) / len(b1), (y_bot - y_top) / len(b1)
    riser2, tread2 = (L2_FF - bl[1][2]) / (len(b2) + 1), (x_top - x_bot) / len(b2)
    return [
        {"id": "COLLISION_STAIR1_RUN_01", "kind": "ramp", "rect": [round(min(b[0][0] for b in b1), 3), round(max(b[1][0] for b in b1), 3), round(y_top, 3), round(y_bot, 3)],
         "axis": "y", "start": round(y_bot, 3), "direction": -1, "z_base": 0.0, "riser_ft": round(riser1, 4), "tread_ft": round(tread1, 4), "z_max": round(bl[1][2], 3),   # ramp may rise to the landing height
         "grids": ["level1", "level1_lobby_A", "level2"], "source": f"{len(b1)} treads INT_Stair1_run1_tread_* (v014, frozen)"},
        {"id": "COLLISION_STAIR1_LANDING", "kind": "plane", "rect": [round(bl[0][0], 3), round(bl[1][0], 3), round(bl[0][1], 3), round(bl[1][1], 3)], "z": round(bl[1][2], 3),
         "grids": ["level2"], "source": "INT_Stair1_landing (v014, frozen)"},
        {"id": "COLLISION_STAIR1_RUN_02", "kind": "ramp", "rect": [round(x_bot, 3), round(x_top, 3), round(min(b[0][1] for b in b2), 3), round(max(b[1][1] for b in b2), 3)],
         "axis": "x", "start": round(x_bot, 3), "direction": 1, "z_base": round(bl[1][2], 3), "riser_ft": round(riser2, 4), "tread_ft": round(tread2, 4), "z_max": L2_FF,
         "grids": ["level2"], "source": f"{len(b2)} treads INT_Stair1_run2_tread_* (v014, frozen); Level 2 at {L2_FF} ft"},
    ]


def build_grid(floor_z, band, blocker_filter, floor_cells, surfaces, grid_key, guard_objs):
    """Generic walk grid: blocked unless it has floor and nothing solid stands in the walking band; then the Stair 1 surface cells
    for this grid are opened (navigation ramps) and guard lines inside the stair footprint are re-applied (fall protection)."""
    blocked = bytearray(1 if not floor_cells[k] else 0 for k in range(GRID_NX * GRID_NY))
    blockers = []
    for o in bpy.data.objects:
        if o.type != "MESH" or not blocker_filter(o):
            continue
        lo, hi = bbox_ft(o)
        if hi[2] <= floor_z + band[0] or lo[2] >= floor_z + band[1]:
            continue
        blockers.append(o.name)
        for k in cells_of(lo, hi):
            blocked[k] = 1
    if floor_z == 0.0:
        for x0, x1, y0, y1, why in EXTRA_BLOCK:
            for k in cells_of((x0, y0), (x1, y1)):
                blocked[k] = 1
    if grid_key == "level1_lobby_A":                               # v024: furniture footprints block only while the concept is shown
        for name, (x0, x1, y0, y1) in FURNITURE_RECTS:
            for k in cells_of((x0, y0), (x1, y1)):
                blocked[k] = 1
    opened = 0
    for s in surfaces:
        if grid_key not in s["grids"]:
            continue
        x0, x1, y0, y1 = s["rect"]
        for j in range(GRID_NY):
            cy = GRID_Y0 + (j + 0.5) * GRID_CELL
            if not (y0 < cy < y1):
                continue
            for i in range(GRID_NX):
                cx = GRID_X0 + (i + 0.5) * GRID_CELL
                if x0 < cx < x1 and blocked[j * GRID_NX + i]:
                    blocked[j * GRID_NX + i] = 0
                    opened += 1
    stair_rects = [s["rect"] for s in surfaces if grid_key in s["grids"]]
    reblocked = 0
    for o in guard_objs:                                         # guards along the stair edges: block their footprint inside the stair rects only
        lo, hi = bbox_ft(o)
        for k in cells_of(lo, hi):
            j, i = divmod(k, GRID_NX)
            cx, cy = GRID_X0 + (i + 0.5) * GRID_CELL, GRID_Y0 + (j + 0.5) * GRID_CELL
            if any(r[0] - 0.3 < cx < r[1] + 0.3 and r[2] - 0.3 < cy < r[3] + 0.3 for r in stair_rects) and not blocked[k]:
                blocked[k] = 1
                reblocked += 1
    return blocked, blockers, opened, reblocked


def main():
    targets = [DATA] if DATA_ONLY else [GLB, GLB_COPY, DATA, UNDERLAY_COPY]
    for path in targets:
        if path.exists():
            raise SystemExit(f"Refusing to overwrite existing file: {path}")
    if DATA_ONLY and not GLB.exists():
        raise SystemExit("--data-only needs the GLB to exist")
    src_hash = sha256(SRC)
    bpy.ops.wm.open_mainfile(filepath=str(SRC))
    scene = bpy.context.scene

    # ---------- metadata first (read straight from the untouched v019 objects) ----------
    def cam_entry(o, cid, title, floor):
        fwd = o.matrix_world.to_quaternion() @ Vector((0, 0, -1))
        return {"id": cid, "title": title, "position_ft": [round(v / FT, 3) for v in o.location], "forward": [round(v, 5) for v in fwd],
                "lens_mm": round(o.data.lens, 2), "floor": floor, "source": o.name}
    viewpoints = []
    for o in sorted(bpy.data.objects, key=lambda o: o.name):
        if o.type == "CAMERA" and o.name.startswith("VP_A_"):
            viewpoints.append(cam_entry(o, o.name, o.get("title", o.name), "L1"))
    lobby_views = [cam_entry(bpy.data.objects["Cam_lobby_A_01_entrance"], "LV_01_entrance", "Lobby - Entrance", "L1"),
                   cam_entry(bpy.data.objects["Cam_lobby_A_02_level1_corner"], "LV_02_level1", "Lobby - Level 1", "L1"),
                   cam_entry(bpy.data.objects["Cam_lobby_A_03_level2_overlook"], "LV_03_level2_overlook", "Lobby - Level 2 Overlook", "L2")]
    fw = FEATURE_WALL_VIEW
    d = Vector(fw["target_ft"]) - Vector(fw["position_ft"])
    d.normalize()
    lobby_views.append({"id": fw["id"], "title": fw["title"], "position_ft": list(fw["position_ft"]), "forward": [round(v, 5) for v in d], "lens_mm": fw["lens_mm"],
                        "floor": "L1", "source": "viewer-only viewpoint chosen from the v019 geometry (no Blender camera added)"})
    lobby_views.append(cam_entry(bpy.data.objects["Cam_lobby_A_04_seating"], "LV_05_seating", "Lobby - Seating", "L1"))   # v024: from the v023 review camera
    schedule = json.loads(SCHEDULE_SRC.read_text(encoding="utf-8"))
    sched = {r["id"]: r for r in schedule["rooms"]}
    rooms = []
    for o in bpy.data.objects:
        if o.get("kind") == "room":
            lo, hi = bbox_ft(o)
            r = sched[o["room_id"]]
            rooms.append({"id": o["room_id"], "object": o.name, "name": o["room_name"], "concept": CONCEPT, "floor": "Level 1",
                          "printed_sf": r["printed_sf"], "modeled_sf": r["modeled_sf"], "modeled_net_sf": r["modeled_net_sf"],
                          "overlapping_smaller_rooms": r["overlapping_smaller_rooms"], "enclosure": r["enclosure"], "cls": r["cls"],
                          "rect_ft": [round(lo[0], 3), round(lo[1], 3), round(hi[0], 3), round(hi[1], 3)]})
    rooms.sort(key=lambda r: r["id"])
    lobby_counts = {}
    lobby_bounds = {}
    for c in LOBBY_SUBS:
        col = bpy.data.collections[c]
        meshes = [o for o in col.objects if o.type == "MESH"]
        lobby_counts[c] = {"source_objects": len(col.objects), "meshes": len(meshes), "lights": sum(1 for o in col.objects if o.type == "LIGHT")}
        if meshes:
            bbs = [bbox_ft(o) for o in meshes]
            lobby_bounds[c] = [round(min(b[0][i] for b in bbs), 2) for i in range(3)] + [round(max(b[1][i] for b in bbs), 2) for i in range(3)]

    # ---------- walk grids (Level 1 base, Level 1 with the lobby concept, Level 2) + Stair 1 navigation surface ----------
    surfaces = stair1_surfaces()
    floor1 = bytearray(GRID_NX * GRID_NY)
    for j in range(GRID_NY):
        for i in range(GRID_NX):
            if inside((GRID_X0 + (i + 0.5) * GRID_CELL, GRID_Y0 + (j + 0.5) * GRID_CELL), P1):
                floor1[j * GRID_NX + i] = 1
    floor2 = bytearray(GRID_NX * GRID_NY)
    slab = bpy.data.objects["INT_L2_slab"]
    floor_faces = 0
    for poly in slab.data.polygons:
        n = slab.matrix_world.to_3x3() @ poly.normal
        if n.z < 0.9:
            continue
        pts = [slab.matrix_world @ slab.data.vertices[i].co for i in poly.vertices]
        if abs(pts[0].z / FT - L2_FF) > 0.01:
            continue
        floor_faces += 1
        fx0, fx1 = min(p.x for p in pts) / FT, max(p.x for p in pts) / FT
        fy0, fy1 = min(p.y for p in pts) / FT, max(p.y for p in pts) / FT
        for k in cells_of((fx0, fy0), (fx1, fy1)):
            j, i = divmod(k, GRID_NX)
            cx, cy = GRID_X0 + (i + 0.5) * GRID_CELL, GRID_Y0 + (j + 0.5) * GRID_CELL
            if fx0 <= cx <= fx1 and fy0 <= cy <= fy1:
                floor2[k] = 1

    def base_l1(o):
        name, kind = o.name, o.get("kind", "")
        if name.startswith("INT_"):
            return o.get("level") in (1, "lid1") and "slab" not in name.lower() and "ceiling" not in name.lower() and "FUTURE_room" not in name
        if name.startswith("TEN_A_"):
            return kind in ("partition", "demising", "bay_divider", "equipment")
        return False

    fr = {}
    for o in bpy.data.objects:                         # v024: one rectangle per chair / table / planter pot (plants and thin finishes excluded)
        if o.type == "MESH" and o.name.startswith(("LOB_A_P2_Chair_", "LOB_A_P2_Table_", "LOB_A_P2_Planter_")):
            key = "_".join(o.name.split("_")[:5])
            lo, hi = bbox_ft(o)
            r = fr.setdefault(key, [lo[0], hi[0], lo[1], hi[1]])
            r[0], r[1], r[2], r[3] = min(r[0], lo[0]), max(r[1], hi[0]), min(r[2], lo[1]), max(r[3], hi[1])
    FURNITURE_RECTS[:] = [(k, [round(v, 3) for v in r]) for k, r in sorted(fr.items())]

    def lobby_solid(o):                                # lobby-concept solids that block walking; stair finishes / guard shoes sit on the stair
        if o.name.startswith("LOB_A_P2_"):
            return False                               # Pass 2 objects: chairs / tables / planters block through FURNITURE_RECTS; art, DP-01, graphic are thin finishes
        return o.name.startswith("LOB_A_") and not any(c.name in ("ARCH_STAIR_FINISH", "ARCH_GUARDRAIL") for c in o.users_collection)

    def lobby_l1(o):
        return base_l1(o) or lobby_solid(o)

    def l2(o):
        if not (o.name.startswith("INT_") or o.name.startswith("TEN_") or lobby_solid(o)):
            return False
        low = o.name.lower()
        return not ("slab" in low or "ceiling" in low or "future_room" in low or "roof_deck" in low or "underlay" in low)

    # fall protection along the stair edges = the frozen v014 glass guards (open sides and the Level 2 void edge). The lobby concept's
    # shoes / handrails sit on those same lines or on the wall side, so they are not re-applied (a wall-side rail would pinch run 1).
    guards = [o for o in bpy.data.objects if o.type == "MESH" and "guard" in o.name.lower() and o.name.startswith("INT_")]
    grids, grid_reports = {}, {}
    for key, fz, filt, floor_cells in (("level1", 0.0, base_l1, floor1), ("level1_lobby_A", 0.0, lobby_l1, floor1), ("level2", L2_FF, l2, floor2)):
        blocked, blockers, opened, reblocked = build_grid(fz, (WALK_LOW, WALK_HIGH), filt, floor_cells, surfaces, key, guards)
        open_cells = GRID_NX * GRID_NY - sum(blocked)
        grids[key] = {"cell_ft": GRID_CELL, "x0_ft": GRID_X0, "y0_ft": GRID_Y0, "nx": GRID_NX, "ny": GRID_NY, "floor_z_ft": fz,
                      "blocking_objects": len(blockers), "open_cells": open_cells, "stair_cells_opened": opened, "guard_cells_reblocked": reblocked,
                      "encoding": "per row: run lengths, alternating open / blocked, starting with open", "rows": rle_rows(blocked, GRID_NX, GRID_NY)}
        grid_reports[key] = {"blocking_objects": len(blockers), "open_cells": open_cells, "stair_cells_opened": opened, "guard_cells_reblocked": reblocked}
    grids["level1"]["rule"] = "open = inside the Level 1 face-of-stud outline and no base-building or tenant solid between 0.5 ft and 6.5 ft; Stair 1 run 1 cells are a ramp surface"
    grids["level1_lobby_A"]["rule"] = "as level1 plus the Lobby Concept A solids (banquettes, directory, wood boxes) as blockers; used while the lobby concept is shown"
    grids["level2"]["rule"] = ("open = under an upward face of the approved Level 2 slab (16 ft 0 in) and no base-building, tenant or lobby-concept solid between "
                              "16.5 ft and 22.5 ft; Stair 1 run 1, landing and run 2 cells are the navigation surface; voids have no floor; no openings were added")

    # ---------- GLB (group, flatten materials, join - all in memory) ----------
    if not DATA_ONLY:
        members = {k: [] for k in GROUPS}
        for o in bpy.data.objects:
            g = classify(o)
            if g:
                members[g].append(o)
        export_objs = [o for objs in members.values() for o in objs]
        WLC_BODY_BOXES[:] = [bbox_ft(o) for o in members[LOBBY_GROUP] if o.name.startswith("LOB_A_WLC_") and o.name.endswith("_BEGA_33590")]   # v024
        source_counts = {k: len(v) for k, v in members.items()}
        for o in export_objs:
            o.hide_viewport = o.hide_render = False
            o.hide_set(False)
        grain = make_grain_image()
        for o in members[LOBBY_GROUP]:
            if any(s.material and VIEWER_MATERIALS.get(s.material.name, {}).get("tex") == "grain" for s in o.material_slots):
                box_uvs(o, 8.0)                                            # v025: 8 ft repeat (less repetition)
        for mat in {s.material for o in export_objs for s in o.material_slots if s.material}:
            flatten_material(mat, grain)

        def join(objs, new_name):
            if not objs:
                return None
            bpy.ops.object.select_all(action="DESELECT")
            for o in objs:
                o.select_set(True)
            bpy.context.view_layer.objects.active = objs[0]
            if len(objs) > 1:
                bpy.ops.object.join()
            res = bpy.context.view_layer.objects.active
            res.name = new_name
            res.data.name = new_name
            return res

        final = {}
        for g, objs in members.items():
            keep_separate, mergeable = [], []
            for o in objs:
                if o.data.users > 1 or o.get("kind") in ("room", "circulation"):
                    keep_separate.append(o)
                else:
                    mergeable.append(o)
            buckets = {}
            if g == "GRP_Concept_A_CNSA_ASC":
                for o in mergeable:
                    buckets.setdefault("TEN_A_" + {"partition": "Partitions", "demising": "Partitions", "bay_divider": "Bay_dividers_TYPE_UNKNOWN",
                                                   "equipment": "Table_proxies", "marker": "Floor_markers"}.get(o.get("kind", ""), "Other"), []).append(o)
            elif g == LOBBY_GROUP:
                for o in mergeable:                               # one node per v019 sub-collection (viewer-only consolidation of repeated pieces)
                    buckets.setdefault("LOBBY_A__" + o.users_collection[0].name, []).append(o)
            else:
                for o in mergeable:
                    buckets.setdefault(g.replace("GRP_", "") + "__" + (o.users_collection[0].name if not o.name.startswith("INT_") else
                                                                         ([c.name for c in o.users_collection if not c.name.startswith("BASE_Level")] or [o.users_collection[0].name])[0]), []).append(o)
            nodes = [join(v, k) for k, v in sorted(buckets.items())] + keep_separate
            if g == LOBBY_GROUP:
                for c in LOBBY_SUBS:                              # reserved (empty) Pass 2 sub-collections are kept as empty nodes, not removed
                    if not any(n_.name == "LOBBY_A__" + c for n_ in nodes):
                        e = bpy.data.objects.new("LOBBY_A__" + c, None)
                        scene.collection.objects.link(e)
                        e["reserved"] = "v019 sub-collection is empty (Pass 2 not yet authorized)"
                        nodes.append(e)
            empty = bpy.data.objects.new(g, None)
            scene.collection.objects.link(empty)
            empty["description"] = GROUPS[g]
            if g == LOBBY_GROUP:
                empty["building"], empty["level"], empty["category"] = "Building II", "Lobby / Level 1 / Level 2", "Interior Concept"
                empty["concept"], empty["model_version"], empty["source_collection"] = "Lobby Concept A", "v023", "Building_II > INT_LOBBY_CONCEPT_A"
            for n_ in nodes:
                n_.parent = empty
                n_.matrix_parent_inverse = Matrix.Identity(4)
            final[g] = [empty] + nodes

        graze = make_graze_pools(WLC_BODY_BOXES, scene.collection)          # v024: baked graze pools, parented into the lobby group
        graze.parent = final[LOBBY_GROUP][0]
        graze.matrix_parent_inverse = Matrix.Identity(4)
        final[LOBBY_GROUP].append(graze)
        bpy.ops.object.select_all(action="DESELECT")
        for nodes in final.values():
            for o in nodes:
                o.select_set(True)
        for d_ in (GLB.parent, GLB_COPY.parent, DATA.parent):
            d_.mkdir(parents=True, exist_ok=True)
        bpy.ops.export_scene.gltf(filepath=str(GLB), export_format="GLB", use_selection=True, export_apply=True, export_extras=True,
                                  export_cameras=False, export_lights=False, export_yup=True, export_materials="EXPORT", export_animations=False,
                                  export_image_format="AUTO")
        assert sha256(SRC) == src_hash, "v019 .blend changed on disk"   # it is never saved by this script
        shutil.copyfile(GLB, GLB_COPY)
        shutil.copyfile(UNDERLAY_SRC, UNDERLAY_COPY)
        group_report = [{"node": k, "description": v, "source_objects": source_counts[k], "exported_nodes": len(final[k]) - 1} for k, v in GROUPS.items()]
    else:
        group_report = json.loads((VIEWER / "assets" / "_groups_v026.json").read_text()) if (VIEWER / "assets" / "_groups_v026.json").exists() else []
    if not DATA_ONLY:
        (VIEWER / "assets" / "_groups_v026.json").write_text(json.dumps(group_report))

    underlay = {"image": "assets/" + UNDERLAY_COPY.name, "x0_ft": (0.0 - 651.395) / 9.0, "x1_ft": (3024.0 - 651.395) / 9.0,
                "y0_ft": (1571.795 - 2160.0) / 9.0, "y1_ft": 1571.795 / 9.0,
                "source": "tenant_testfits/CNSA_ASC/ASC Rea Farms PRESENTATION PLAN v3 20260915.pdf (registered in v015: scale 1.0000158, RMS 0.027 ft)"}
    warning = "Concept plan does not document tenant doors/openings. Room-to-room circulation is incomplete and no openings have been invented."
    data = {"version": "v026", "viewer_version": "v026", "model_version": "v023", "source_model": "models/building_shell_v023.blend", "source_model_sha256": src_hash,
            "glb": "models/" + GLB.name, "glb_bytes": GLB.stat().st_size,
            "units": {"glb": "metres, Y up (glTF)", "model": "decimal feet, X east, Y north, Z up",
                      "conversion": "x_ft = X / 0.3048 ; y_ft(north) = -Z / 0.3048 ; z_ft(up) = Y / 0.3048"},
            "groups": group_report, "eye_height_ft": EYE_FT,
            "walk": {"normal_ft_per_s": 9.0, "fast_ft_per_s": 18.0, "stair_factor": 0.6, "substep_ft": 0.2, "step_ft": 1.0, "body_radius_ft": 0.75,
                     "note": "approved v017 speeds; stair_factor slows walking on the Stair 1 ramps; step_ft = largest surface height change accepted per sub-step"},
            "floors": {"L1": {"label": "Level 1", "floor_z_ft": 0.0, "grid": "level1", "grid_with_lobby_concept": "level1_lobby_A", "default_walk_ft": [129.9, 79.0], "default_forward": [0.0, -1.0, 0.0]},
                       "L2": {"label": "Level 2", "floor_z_ft": L2_FF, "grid": "level2", "default_walk_ft": [118.0, 69.0], "default_forward": [0.0, 1.0, 0.0]}},
            "walk_grids": grids,
            "stair_surfaces": surfaces,
            "stair_surfaces_note": "Viewer-only navigation surfaces (invisible; not in the Blender master; not rendered). A ramp's height at distance d along the run is "
                                   "z_base + riser_ft * (0.5 + d / tread_ft), clamped to z_max. Guards, walls and the Level 2 void edge stop the walker through the grids and the step_ft rule.",
            "concepts": [{"id": CONCEPT, "label": "CNSA ASC — Concept A", "tenant": "CNSA Rea Farms ASC", "group": "GRP_Concept_A_CNSA_ASC",
                          "floor": "L1", "source": schedule["source"], "areas": schedule["areas"], "warning": warning,
                          "viewpoints": viewpoints, "rooms": rooms, "underlay": underlay}],
            "lobby_concept": {"id": "Lobby_Concept_A", "label": "Lobby Concept A (v023 approved)", "group": LOBBY_GROUP, "building": "Building II", "category": "Interior Concept",
                              "level": "Lobby / Level 1 / Level 2", "model_version": "v023", "pass": "approved lobby baseline: Pass 1 architectural + Pass 2 FF&E + v023 visual refinement",
                              "source_collection": "Building_II > INT_LOBBY_CONCEPT_A", "subcollections": lobby_counts, "bounds_ft": lobby_bounds,
                              "grid_L1": "level1_lobby_A", "viewpoints": lobby_views, "orbit": LOBBY_ORBIT,
                              "lobby_rect_ft": [106.59, 142.45, 72.89, 103.09],
                              "viewer_materials": {k: {kk: vv for kk, vv in v.items()} for k, v in VIEWER_MATERIALS.items()},
                              "lights_note": "The 64 Blender point lights and the Cycles emission are not exported; fixtures use emissive glTF materials plus a few browser lights."},
            "concept_architecture": "Each entry in 'concepts' carries its own GLB group node, floor, rooms, viewpoints, underlay and warning. The lobby concept is a "
                                    "separate 'lobby_concept' entry with its own group node so base building and lobby can be compared by one toggle."}
    v020 = json.loads(V020_DATA.read_text(encoding="utf-8"))
    assert surfaces == v020["stair_surfaces"], "Stair 1 navigation surface differs from viewer v020"

    def decode(rows):
        cells = bytearray(GRID_NX * GRID_NY)
        for j, runs in enumerate(rows):
            i, blk = 0, 0
            for n in runs:
                if blk:
                    cells[j * GRID_NX + i:j * GRID_NX + i + n] = b"\x01" * n
                i += n
                blk ^= 1
        return cells

    def in_furniture(k):
        j, i = divmod(k, GRID_NX)
        cx, cy = GRID_X0 + (i + 0.5) * GRID_CELL, GRID_Y0 + (j + 0.5) * GRID_CELL
        return any(x0 - GRID_CELL <= cx <= x1 + GRID_CELL and y0 - GRID_CELL <= cy <= y1 + GRID_CELL for _, (x0, x1, y0, y1) in FURNITURE_RECTS)
    grid_diff = {}
    for key in ("level1", "level1_lobby_A", "level2"):
        a, b_ = decode(v020["walk_grids"][key]["rows"]), decode(grids[key]["rows"])
        changed = [k for k in range(GRID_NX * GRID_NY) if a[k] != b_[k]]
        outside = [k for k in changed if not in_furniture(k)]
        grid_diff[key] = {"cells_changed_vs_v020": len(changed), "outside_furniture_footprints": len(outside)}
        assert not outside, f"grid {key}: {len(outside)} cells differ from v020 outside the furniture footprints"
        if key != "level1_lobby_A":
            assert not changed, f"grid {key} differs from v020"
    data["navigation_note"] = ("Stair 1 surfaces identical to viewer v020; level1 and level2 grids identical to v020; level1_lobby_A differs from v020 only "
                               "inside the simplified furniture footprints (chairs, tables, planter pots) added in v024")
    data["furniture_collision"] = {"rects_ft": FURNITURE_RECTS, "grid_diff_vs_v020": grid_diff,
                                   "rule": "one rectangle per chair / table / planter pot (bounding box of its parts); plants, art, DP-01 and the directory graphic do not block; banquettes and the directory massing block as in v020"}
    v024 = json.loads(V024_DATA.read_text(encoding="utf-8"))
    norm = lambda v: json.loads(json.dumps(v))                             # tuples -> lists, like the stored file
    for key in ("walk_grids", "stair_surfaces", "floors", "walk", "concepts"):
        assert norm(data[key]) == v024[key], f"{key} differs from viewer v024"
    assert norm(data["lobby_concept"]["viewpoints"]) == v024["lobby_concept"]["viewpoints"], "lobby viewpoints differ from viewer v024"
    assert norm(data["furniture_collision"]) == v024["furniture_collision"], "furniture collision differs from viewer v024"
    data["v025_note"] = "viewer-only visual tuning; grids, stair surfaces, furniture collision, floors and viewpoints asserted identical to viewer v024"
    DATA.write_text(json.dumps(data, separators=(",", ":")), encoding="utf-8")
    assert sha256(SRC) == src_hash

    # ---------- verify the GLB really contains the lobby group (parse the JSON chunk) ----------
    with open(GLB, "rb") as f:
        magic, ver, length = struct.unpack("<III", f.read(12))
        clen, ctype = struct.unpack("<II", f.read(8))
        gl = json.loads(f.read(clen).decode("utf-8"))
    nodes = gl["nodes"]
    by_name = {n.get("name"): i for i, n in enumerate(nodes)}
    lobby_i = by_name.get(LOBBY_GROUP)
    verify = {"lobby_group_present": lobby_i is not None, "children": [], "lobby_meshes": 0, "lobby_primitives": 0, "lobby_triangles": 0, "lobby_materials": set()}
    if lobby_i is not None:
        for ci in nodes[lobby_i].get("children", []):
            n = nodes[ci]
            entry = {"node": n.get("name"), "mesh": "mesh" in n}
            if "mesh" in n:
                m = gl["meshes"][n["mesh"]]
                tri = 0
                for p in m["primitives"]:
                    acc = gl["accessors"][p["indices"]] if "indices" in p else gl["accessors"][p["attributes"]["POSITION"]]
                    tri += acc["count"] // 3
                    if "material" in p:
                        verify["lobby_materials"].add(gl["materials"][p["material"]].get("name"))
                entry.update(primitives=len(m["primitives"]), triangles=tri)
                verify["lobby_meshes"] += 1
                verify["lobby_primitives"] += len(m["primitives"])
                verify["lobby_triangles"] += tri
            verify["children"].append(entry)
    verify["lobby_materials"] = sorted(verify["lobby_materials"])
    verify["glb_totals"] = {"nodes": len(nodes), "meshes": len(gl["meshes"]), "materials": len(gl["materials"]), "images": len(gl.get("images", [])),
                            "bytes": GLB.stat().st_size}
    print("EXPORT_REPORT=" + json.dumps({"glb_bytes": data["glb_bytes"], "groups": group_report, "viewpoints": len(viewpoints), "lobby_views": len(lobby_views),
                                         "rooms": len(rooms), "grids": grid_reports, "stair_surfaces": surfaces, "lobby_counts": lobby_counts, "verify": verify}))


if __name__ == "__main__":
    main()
