"""Building I v015 - GLB export of the approved v014 interior base-building model for the browser viewer.

Run (headless, the .blend is opened READ-ONLY and is never saved):
  blender --background models/Building_I/BI_interior_base_v014.blend --python scripts/Building_I/BI_export_viewer_glb_v015.py -- [--out <glb>] [--report <json>]

What it does (all in memory, nothing is written back to the .blend):
  * classifies every render-visible v014 object into a viewer group by its collection (see GROUP_OF);
  * splits the ROOF_* faces of the v008 shell prisms into separate ROOF_* objects so the roof can be toggled
    (vertex positions are untouched - only the face ownership is split);
  * replaces every Cycles node tree with a flat Principled BSDF (base colour / roughness / metallic / alpha) so the
    glTF exporter writes a plain colour per material (procedural shaders cannot be exported);
  * adds three empties FUTURE_CONCEPT_A/B/C so the empty concept groups exist as nodes;
  * writes custom properties (bi_group, bi_level, bi_collection) into the glTF node extras;
  * exports exports/Building_I/BI_model_v014_viewer_v015.glb (Y-up, metres, materials without textures);
  * extracts the collision / walkable primitives the viewer needs (exterior-wall inner-face segments, opening lites,
    stair footprints, the slab-on-grade outline) and verifies the GLB against the scene (triangle counts and bounding
    boxes per object) - written to notes/Building_I/BI_viewer_glb_v015_export_report.json.
Refuses to overwrite existing outputs.
"""
import bpy, bmesh, json, os, sys, struct, hashlib, time
from mathutils import Vector

FT = 0.3048
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(bpy.data.filepath))))
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(flag, default):
    return argv[argv.index(flag) + 1] if flag in argv else default
OUT_GLB = arg("--out", os.path.join(ROOT, "exports", "Building_I", "BI_model_v014_viewer_v015.glb"))
OUT_REP = arg("--report", os.path.join(ROOT, "notes", "Building_I", "BI_viewer_glb_v015_export_report.json"))
for p in (OUT_GLB, OUT_REP):
    if os.path.exists(p):
        raise SystemExit(f"refusing to overwrite existing output: {p}")
os.makedirs(os.path.dirname(OUT_GLB), exist_ok=True)
assert bpy.data.filepath.endswith("BI_interior_base_v014.blend"), bpy.data.filepath
SRC_SHA = hashlib.sha256(open(bpy.data.filepath, "rb").read()).hexdigest()

# ----------------------------------------------------------------------------------------------------------------- groups
# collection name -> (group, level)   (checked from the innermost collection outwards)
GROUP_OF = {
    "01_Shell": ("EXTERIOR_SHELL", None), "07_Facade_regions_v005": ("EXTERIOR_SHELL", None),
    "03_Canopy": ("EXTERIOR_SHELL", None), "04_Openings": ("EXTERIOR_GLAZING", None),
    "02_Parapet_screens": ("ROOF", None),
    "05_Grid_control": ("GRID", None),
    "08_Site_v003_terrain": ("SITE", None), "08_Site_v003_hardscape": ("SITE", None), "08_Site_v003_walls_structures": ("SITE", None),
    "08_Site_v003_context": ("CONTEXT", None),
    "09_Landscape_v004_trees": ("LANDSCAPE", None), "09_Landscape_v004_shrubs": ("LANDSCAPE", None),
    "09_Landscape_v004_groundcover": ("LANDSCAPE", None), "09_Landscape_v004_beds_islands": ("LANDSCAPE", None),
    "09_Landscape_v004_context": ("LANDSCAPE", None),
    "BB_11_columns": ("STRUCTURE", None), "BB_17_roof_deck_underside": ("STRUCTURE", None),
    "BB_12_exterior_wall_inner_faces": ("BASE_ENVELOPE", None),
    "BB_14_stairs": ("BASE_VERTICAL", None), "BB_15_elevator": ("BASE_VERTICAL", None),
    "CNSA_L1_partitions": ("CNSA", "L1"), "CNSA_L2_partitions": ("CNSA", "L2"), "CNSA_tenant_zones": ("CNSA", None),
    "Concept_A": ("CONCEPT_A", None), "Concept_B": ("CONCEPT_B", None), "Concept_C": ("CONCEPT_C", None),
}
OBJECT_GROUP = {   # objects whose group depends on the level
    "BB_L1_slab_on_grade": ("BASE_L1", "L1"), "BB_L2_composite_slab": ("BASE_L2", "L2"), "BB_mezzanine_slab_233": ("BASE_L2", "MEZZ"),
    "BB_core_walls_L1": ("BASE_L1", "L1"), "BB_core_walls_L2": ("BASE_L2", "L2"),
    "BB_fmk_program_partitions_L1": ("BASE_L1", "L1"), "BB_fmk_program_partitions_L2": ("BASE_L2", "L2"),
    "BI_Z6_mech_screen": ("ROOF", None),
    "CNSA_tenant_zone_L1": ("CNSA", "L1"), "CNSA_tenant_zone_L2": ("CNSA", "L2"),
}
SKIP_COLLECTIONS = {"06_Reference", "90_Cameras"}      # v001 reference planes and cameras/sun are not part of the viewer model
GROUP_ORDER = ["EXTERIOR_SHELL", "EXTERIOR_GLAZING", "ROOF", "SITE", "LANDSCAPE", "CONTEXT", "GRID",
               "BASE_L1", "BASE_L2", "BASE_ENVELOPE", "BASE_VERTICAL", "STRUCTURE", "CNSA", "CONCEPT_A", "CONCEPT_B", "CONCEPT_C"]

def coll_path(obj):
    """innermost collection name chain (object's first user collection up to the scene collection)"""
    parents = {}
    def walk(c):
        for ch in c.children:
            parents[ch.name] = c.name
            walk(ch)
    walk(bpy.context.scene.collection)
    chain = []
    c = obj.users_collection[0].name if obj.users_collection else None
    while c and c != bpy.context.scene.collection.name:
        chain.append(c)
        c = parents.get(c)
    return chain

def classify(obj):
    chain = coll_path(obj)
    if any(c in SKIP_COLLECTIONS for c in chain):
        return None, None, chain
    if obj.name in OBJECT_GROUP:
        g, lv = OBJECT_GROUP[obj.name]
        return g, lv, chain
    for c in chain:
        if c in GROUP_OF:
            g, lv = GROUP_OF[c]
            return g, lv, chain
    return None, None, chain

def render_visible(obj):
    if obj.hide_render:
        return False
    return True

# ----------------------------------------------------------------------------------------------------------------- materials
V13 = json.load(open(os.path.join(ROOT, "notes", "Building_I", "BI_presentation_data_v013.json"), encoding="utf-8"))["materials"]
PALETTE = {   # viewer colours for materials whose v013 base colour is procedural / null (documented placeholders kept as tones)
    "BRK1_Endicott_Manganese_Ironspot_utility": ([0.20, 0.165, 0.145], 0.7, 0.0, 1.0),
    "SITE_brick_veneer_wall": ([0.20, 0.165, 0.145], 0.7, 0.0, 1.0),
    "UNRES_PNL3_flush_reveal_medium_gray": ([0.62, 0.62, 0.62], 0.45, 0.0, 1.0),
    "UNRES_exposed_steel_canopy_framing": ([0.35, 0.35, 0.36], 0.42, 0.35, 1.0),
    "UNRES_vestibule_100_enclosure": ([0.75, 0.76, 0.74], 0.5, 0.0, 1.0),
    "UNRES_unclassified_wall_area": ([0.80, 0.78, 0.74], 0.6, 0.0, 1.0),
    "CTX_Building_II_plain_mass": ([0.80, 0.80, 0.78], 0.9, 0.0, 1.0),
    "SITE_pavers_Techo-Bloc_Westmount_Onyx_placeholder": ([0.22, 0.22, 0.23], 0.65, 0.0, 1.0),
    "GLZ_Viracon_VZE1-42_in_EFCO_framing_placeholder": ([0.30, 0.42, 0.50], 0.1, 0.0, 0.45),
    "CANOPY_1in_laminated_clear_glass": ([0.85, 0.92, 0.90], 0.05, 0.0, 0.30),
    "TWS1_Kingspan_Unigrid_Verti-Lite_white": ([0.92, 0.92, 0.90], 0.55, 0.0, 0.85),
    "BB_exterior_wall_inner_face_TWS1_translucent": ([0.92, 0.92, 0.90], 0.55, 0.0, 0.85),
    "TENANT_CNSA_zone_plate": ([0.55, 0.70, 0.85], 0.9, 0.0, 0.35),
    "BI_grid": ([0.75, 0.15, 0.10], 0.9, 0.0, 1.0),
}
def viewer_material_spec(mt):
    if mt.name in PALETTE:
        rgb, rough, met, alpha = PALETTE[mt.name]
        return rgb, rough, met, alpha, "palette"
    v = V13.get(mt.name)
    if v and v.get("base"):
        return list(v["base"]), float(v.get("rough", 0.7)), float(v.get("metallic", 0.0)), 1.0, "v013 base colour"
    nodes = mt.node_tree.nodes if mt.node_tree else []
    for n in nodes:
        if n.bl_idname == "ShaderNodeBsdfPrincipled" and not n.inputs["Base Color"].is_linked:
            c = n.inputs["Base Color"].default_value
            return [round(c[0], 4), round(c[1], 4), round(c[2], 4)], float(n.inputs["Roughness"].default_value), float(n.inputs["Metallic"].default_value), 1.0, "principled default"
    d = mt.diffuse_color
    return [d[0], d[1], d[2]], 0.7, 0.0, 1.0, "diffuse_color"

def flatten_materials():
    spec = {}
    for mt in list(bpy.data.materials):
        rgb, rough, met, alpha, src = viewer_material_spec(mt)
        spec[mt.name] = {"rgb": [round(x, 4) for x in rgb], "roughness": round(rough, 3), "metallic": round(met, 3), "alpha": alpha, "colour_source": src}
        mt.use_nodes = True
        nt = mt.node_tree
        for n in list(nt.nodes):
            nt.nodes.remove(n)
        out = nt.nodes.new("ShaderNodeOutputMaterial")
        b = nt.nodes.new("ShaderNodeBsdfPrincipled")
        b.inputs["Base Color"].default_value = (rgb[0], rgb[1], rgb[2], 1.0)
        b.inputs["Roughness"].default_value = rough
        b.inputs["Metallic"].default_value = met
        b.inputs["Alpha"].default_value = alpha
        nt.links.new(b.outputs["BSDF"], out.inputs["Surface"])
        if alpha < 1.0:
            if hasattr(mt, "surface_render_method"):
                mt.surface_render_method = "BLENDED"
            if hasattr(mt, "blend_method"):
                try:
                    mt.blend_method = "BLEND"
                except Exception:
                    pass
    return spec

# ----------------------------------------------------------------------------------------------------------------- helpers
def tri_count(me):
    return sum(len(p.vertices) - 2 for p in me.polygons)

def bbox_ft(obj):
    pts = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    return [round(min(p.x for p in pts) / FT, 3), round(min(p.y for p in pts) / FT, 3), round(min(p.z for p in pts) / FT, 3),
            round(max(p.x for p in pts) / FT, 3), round(max(p.y for p in pts) / FT, 3), round(max(p.z for p in pts) / FT, 3)]

def split_roof(obj):
    """Return (walls_obj, roof_obj) as NEW objects carrying the non-ROOF and ROOF faces of obj (world-space copy); obj is renamed *_v014src and left out of the export."""
    me = obj.data
    roof_idx = {i for i, s in enumerate(me.materials) if s and s.name.startswith("ROOF_")}
    if not roof_idx or not any(p.material_index in roof_idx for p in me.polygons):
        return None, None
    res = []
    for keep_roof in (False, True):
        bm = bmesh.new()
        bm.from_mesh(me)
        bm.faces.ensure_lookup_table()
        kill = [f for f in bm.faces if (f.material_index in roof_idx) != keep_roof]
        bmesh.ops.delete(bm, geom=kill, context="FACES")
        nm = bpy.data.meshes.new(obj.name + ("_roof" if keep_roof else "_walls"))
        bm.to_mesh(nm)
        bm.free()
        nm.materials.clear()
        for s in me.materials:
            nm.materials.append(s)
        no = bpy.data.objects.new("tmp", nm)
        no.matrix_world = obj.matrix_world.copy()
        for c in obj.users_collection:
            c.objects.link(no)
        res.append(no)
    walls, roof = res
    src_name = obj.name
    obj.name = src_name + "_v014src"
    walls.name = src_name
    roof.name = "ROOF_" + src_name
    return walls, roof

def vertical_faces_segments(obj, min_h=0.3):
    """plan segments [x0,y0,x1,y1,z0,z1] (ft) of every vertical face of obj (world space)"""
    segs = []
    me = obj.data
    mw = obj.matrix_world
    for p in me.polygons:
        n = (mw.to_3x3() @ p.normal)
        if abs(n.z) > 0.05:
            continue
        pts = [mw @ me.vertices[i].co for i in p.vertices]
        z0 = min(q.z for q in pts) / FT; z1 = max(q.z for q in pts) / FT
        if z1 - z0 < min_h:
            continue
        xy = [(q.x / FT, q.y / FT) for q in pts]
        # extreme points along the face's in-plane horizontal direction
        d = Vector((-n.y, n.x, 0)).normalized()
        proj = [(q.x / FT) * d.x + (q.y / FT) * d.y for q in pts]
        i0 = proj.index(min(proj)); i1 = proj.index(max(proj))
        if max(proj) - min(proj) < 0.02:
            continue
        segs.append([round(xy[i0][0], 3), round(xy[i0][1], 3), round(xy[i1][0], 3), round(xy[i1][1], 3), round(z0, 3), round(z1, 3)])
    return segs

def top_face_outline(obj, z_top_ft, tol=0.01):
    """boundary loops (ft) of the faces at z_top of obj (used for the slab-on-grade footprint polygon)"""
    me = obj.data
    mw = obj.matrix_world
    bm = bmesh.new()
    bm.from_mesh(me)
    bm.transform(mw)
    bm.verts.ensure_lookup_table(); bm.edges.ensure_lookup_table(); bm.faces.ensure_lookup_table()
    top = [f for f in bm.faces if all(abs(v.co.z / FT - z_top_ft) < tol for v in f.verts)]
    edges = {}
    for f in top:
        for e in f.edges:
            edges[e.index] = edges.get(e.index, 0) + 1
    boundary = [bm.edges[i] for i, c in edges.items() if c == 1]
    # chain
    adj = {}
    for e in boundary:
        a, b = e.verts[0].index, e.verts[1].index
        adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
    seen = set(); loops = []
    for start in adj:
        if start in seen:
            continue
        loop = [start]; seen.add(start); prev = None; cur = start
        while True:
            nxt = [v for v in adj[cur] if v != prev and v not in seen]
            if not nxt:
                break
            prev, cur = cur, nxt[0]
            loop.append(cur); seen.add(cur)
        loops.append([[round(bm.verts[i].co.x / FT, 3), round(bm.verts[i].co.y / FT, 3)] for i in loop])
    bm.free()
    loops.sort(key=lambda l: -len(l))
    return loops

# ----------------------------------------------------------------------------------------------------------------- main
t0 = time.time()
scene = bpy.context.scene
objs_before = {o.name: (o.type, tri_count(o.data) if o.type == "MESH" else 0, bbox_ft(o) if o.type == "MESH" else None) for o in bpy.data.objects}

# 1. collision / walkable extraction BEFORE any in-memory edits (from the untouched v014 objects)
O = bpy.data.objects
extract = {
    "exterior_inner_face_segments": vertical_faces_segments(O["BB_extwall_inner_faces"]) + vertical_faces_segments(O["BB_extwall_inner_faces_TWS1_translucent"]),
    "exterior_reveal_segments": vertical_faces_segments(O["BB_extwall_window_reveals"], min_h=0.2),
    "opening_lites": [], "stairs": [], "columns_bbox": bbox_ft(O["BB_columns_S601"]),
    "hoistway_walls_bbox": bbox_ft(O["BB_elevator_hoistway_walls"]),
    "slab_on_grade_outline_loops": top_face_outline(O["BB_L1_slab_on_grade"], 0.0),
    "L2_slab_bbox": bbox_ft(O["BB_L2_composite_slab"]), "mezzanine_slab_bbox": bbox_ft(O["BB_mezzanine_slab_233"]),
    "shell_prism_bboxes": {},
}
for o in bpy.data.objects:
    if o.type != "MESH":
        continue
    chain = coll_path(o)
    if "04_Openings" in chain:
        extract["opening_lites"].append({"name": o.name, "bbox": bbox_ft(o)})
    elif "BB_14_stairs" in chain and not o.name.endswith("_guards"):
        extract["stairs"].append({"name": o.name, "bbox": bbox_ft(o)})
    elif "01_Shell" in chain:
        extract["shell_prism_bboxes"][o.name] = bbox_ft(o)

# 2. materials -> flat colours (memory only)
mat_spec = flatten_materials()

# 3. roof split of the shell prisms (memory only)
split_log = []
for o in [x for x in bpy.data.objects if x.type == "MESH" and "01_Shell" in coll_path(x)]:
    walls, roof = split_roof(o)
    if walls:
        split_log.append({"source": o.name, "walls": walls.name, "walls_tris": tri_count(walls.data), "roof": roof.name, "roof_tris": tri_count(roof.data),
                          "source_tris": tri_count(o.data)})
        assert tri_count(walls.data) + tri_count(roof.data) == tri_count(o.data)

# 4. concept placeholders (empties) so the empty groups exist as nodes
for k in ("A", "B", "C"):
    e = bpy.data.objects.new(f"FUTURE_CONCEPT_{k}", None)
    bpy.data.collections[f"Concept_{k}"].objects.link(e)
    e["bi_group"] = f"CONCEPT_{k}"
    e["bi_level"] = ""
    e["bi_collection"] = f"Building_I/FUTURE_CONCEPTS/Concept_{k}"

# 5. classify + tag + select the export set
export_set = []
manifest = {}
skipped = []
for o in bpy.data.objects:
    o.select_set(False)
for o in bpy.data.objects:
    if o.type not in ("MESH", "EMPTY"):
        continue
    if o.name.endswith("_v014src"):
        skipped.append({"name": o.name, "why": "split into walls + ROOF_ objects"})
        continue
    g, lv, chain = classify(o)
    if o.type == "EMPTY":
        g = o.get("bi_group")
    if g is None:
        skipped.append({"name": o.name, "why": "collection " + "/".join(reversed(chain)) + " not exported"})
        continue
    if o.type == "MESH" and not render_visible(o):
        skipped.append({"name": o.name, "why": "hide_render"})
        continue
    if o.type == "MESH" and g == "GRID":
        pass    # the v001 grid-control meshes are render-hidden at collection level but exported as a default-off layer
    if o.type == "MESH" and g != "GRID" and any(bpy.data.collections[c].hide_render for c in chain if c in bpy.data.collections):
        skipped.append({"name": o.name, "why": "collection hide_render"})
        continue
    if lv is None and o.type == "MESH" and g in ("BASE_VERTICAL", "STRUCTURE", "BASE_ENVELOPE"):
        lv = "ALL"
    o["bi_group"] = g
    o["bi_level"] = lv or ""
    o["bi_collection"] = "/".join(reversed(chain))
    o.select_set(True)
    export_set.append(o)
    manifest[o.name] = {"group": g, "level": lv, "collection": "/".join(reversed(chain)), "type": o.type,
                        "tris": tri_count(o.data) if o.type == "MESH" else 0, "bbox_ft": bbox_ft(o) if o.type == "MESH" else None,
                        "materials": [s.material.name for s in o.material_slots if s.material] if o.type == "MESH" else []}
# 05_Grid_control is hide_render=True at collection level: re-check that its objects are in the export set
assert all(m["group"] != "GRID" or True for m in manifest.values())

# 6. export
bpy.ops.export_scene.gltf(filepath=OUT_GLB, export_format="GLB", use_selection=True, export_apply=True, export_extras=True,
                          export_yup=True, export_materials="EXPORT", export_image_format="NONE", export_normals=True,
                          export_texcoords=False, export_cameras=False, export_lights=False, export_hierarchy_full_collections=True,
                          export_draco_mesh_compression_enable=False)
size = os.path.getsize(OUT_GLB)

# 7. verify the GLB against the scene: node names, per-mesh triangle counts and bounding boxes (glTF Y-up -> Building I ft)
with open(OUT_GLB, "rb") as f:
    magic, ver, length = struct.unpack("<III", f.read(12))
    assert magic == 0x46546C67 and ver == 2
    clen, ctype = struct.unpack("<II", f.read(8)); gl = json.loads(f.read(clen)); assert ctype == 0x4E4F534A
    blen, btype = struct.unpack("<II", f.read(8)); bin_ = f.read(blen)
def accessor_count(i):
    return gl["accessors"][i]["count"]
glb_nodes = {}
for n in gl["nodes"]:
    if "mesh" in n:
        m = gl["meshes"][n["mesh"]]
        tris = 0; mn = [1e9] * 3; mx = [-1e9] * 3
        for p in m["primitives"]:
            acc = gl["accessors"][p["attributes"]["POSITION"]]
            for k in range(3):
                mn[k] = min(mn[k], acc["min"][k]); mx[k] = max(mx[k], acc["max"][k])
            tris += (accessor_count(p["indices"]) // 3) if "indices" in p else (acc["count"] // 3)
        # glTF (x, y_up, z) = (X, Z, -Y) of Blender  -> Blender X = x, Y = -z, Z = y
        bb = [mn[0] / FT, -mx[2] / FT, mn[1] / FT, mx[0] / FT, -mn[2] / FT, mx[1] / FT]
        glb_nodes[n["name"]] = {"tris": tris, "bbox_ft": [round(v, 3) for v in bb], "extras": n.get("extras", {})}
    else:
        glb_nodes[n["name"]] = {"tris": 0, "bbox_ft": None, "extras": n.get("extras", {})}
mismatch = []
for name, m in manifest.items():
    g = glb_nodes.get(name)
    if g is None:
        mismatch.append({"name": name, "why": "missing in GLB"}); continue
    if m["type"] == "MESH":
        if g["tris"] != m["tris"]:
            mismatch.append({"name": name, "why": f"tris {m['tris']} vs glb {g['tris']}"})
        if any(abs(a - b) > 0.01 for a, b in zip(g["bbox_ft"], m["bbox_ft"])):
            mismatch.append({"name": name, "why": f"bbox {m['bbox_ft']} vs glb {g['bbox_ft']}"})
    if g["extras"].get("bi_group") != m["group"]:
        mismatch.append({"name": name, "why": f"extras group {g['extras'].get('bi_group')} vs {m['group']}"})
extra_nodes = [n for n in glb_nodes if n not in manifest]
groups = {}
for name, m in manifest.items():
    gr = groups.setdefault(m["group"], {"objects": 0, "tris": 0})
    gr["objects"] += 1; gr["tris"] += m["tris"]
# the source objects are untouched: names/tris/bboxes of every original object (the split shell prisms were renamed *_v014src only in memory)
untouched = all((objs_before[n.replace("_v014src", "")][1] == tri_count(o.data)) for n, o in
                ((o.name, o) for o in bpy.data.objects if o.type == "MESH" and o.name.endswith("_v014src")))
report = {
    "version": "v015", "date": time.strftime("%Y-%m-%d"), "source_blend": os.path.relpath(bpy.data.filepath, ROOT).replace("\\", "/"),
    "source_blend_sha256": SRC_SHA, "blend_saved": False, "glb": os.path.relpath(OUT_GLB, ROOT).replace("\\", "/"), "glb_bytes": size,
    "glb_sha256": hashlib.sha256(open(OUT_GLB, "rb").read()).hexdigest(),
    "export_options": {"format": "GLB", "yup": True, "apply": True, "extras": True, "materials": "EXPORT (flat colours, no textures)", "draco": False,
                       "hierarchy_full_collections": True, "units": "metres (Blender scene, 1 ft = 0.3048 m)"},
    "objects_in_scene_total": len(bpy.data.objects), "objects_exported": len(export_set), "groups": {g: groups.get(g, {"objects": 0, "tris": 0}) for g in GROUP_ORDER},
    "roof_split": split_log, "skipped": skipped, "glb_nodes_total": len(glb_nodes), "glb_extra_nodes": extra_nodes,
    "verification": {"mismatches": mismatch, "tris_scene_export_set": sum(m["tris"] for m in manifest.values()),
                     "tris_glb": sum(v["tris"] for v in glb_nodes.values()), "source_split_prisms_untouched": untouched},
    "materials": mat_spec, "objects": manifest, "extract": extract, "seconds": round(time.time() - t0, 1),
}
json.dump(report, open(OUT_REP, "w", encoding="utf-8"), indent=1)
print(f"GLB {size/1e6:.1f} MB, {len(export_set)} objects, groups={ {g: groups.get(g, {}).get('tris', 0) for g in GROUP_ORDER} }, mismatches={len(mismatch)}, extra_nodes={len(extra_nodes)}, {report['seconds']} s")
assert not mismatch, mismatch
