"""Rea Farms II 3D - v016: browser-viewer export from the frozen v015 model.

Reads models/building_shell_v015.blend and NEVER saves it (the .blend is opened, regrouped in memory, exported, and the
session is thrown away). No architectural geometry is created, moved or edited; objects are only grouped / joined for the
browser and their materials flattened to plain colours, all in memory.

Writes (refuses to overwrite):
  exports/building_II_CNSA_ASC_v016.glb          the export (glTF binary, Y-up, metres)
  viewer/models/building_II_CNSA_ASC_v016.glb    identical copy used by the viewer at run time
  viewer/assets/viewer_data_v016.json            groups, viewpoints, rooms, walk grid, underlay registration
  viewer/assets/tenant_underlay_Concept_A_CNSA_ASC_v015.png   copy of the registered underlay image

Run (Blender 5.2):  blender --background --python scripts/export_viewer_v016.py
See notes/browser_viewer_control_v016.md.
"""
import hashlib
import json
import shutil
import sys
from pathlib import Path

import bpy
from mathutils import Matrix, Vector

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "models" / "building_shell_v015.blend"
GLB = ROOT / "exports" / "building_II_CNSA_ASC_v016.glb"
VIEWER = ROOT / "viewer"
GLB_COPY = VIEWER / "models" / GLB.name
DATA = VIEWER / "assets" / "viewer_data_v016.json"
UNDERLAY_SRC = ROOT / "exports" / "tenant_underlay_Concept_A_CNSA_ASC_v015.png"
UNDERLAY_COPY = VIEWER / "assets" / UNDERLAY_SRC.name
SCHEDULE_SRC = ROOT / "notes" / "tenant_concept_A_CNSA_ASC_room_schedule_v015.json"
FT = 0.3048
CONCEPT = "Concept_A_CNSA_ASC"

# browser groups: key -> (label, which v015 content)
GROUPS = {
    "GRP_Exterior_Solid_Shell": "Building II exterior: solid masses and opening panels (v001-v005). Hidden automatically in walk / plan mode.",
    "GRP_Exterior_Envelope": "Building II exterior: terrace parapets, canopies, glass railings, facade detail, utility yard",
    "GRP_Exterior_Upper": "Building II exterior above Level 2: roof parapets and sun-shade (upper obstruction)",
    "GRP_Base_Interior_Level_1": "Base building interior, Level 1 (v014): inside shell with glazing, slabs, columns, core, stairs, elevator, service rooms",
    "GRP_Base_Interior_Level_2": "Base building interior, Level 2 and terrace slab (v014) (upper obstruction)",
    "GRP_Base_Interior_Roof": "Roof deck lid (v014) (upper obstruction)",
    "GRP_Concept_A_CNSA_ASC": "Tenant concept A - CNSA ASC (v015): partitions, dividers, tables, markers, room plates",
    "GRP_Site_Context": "Site, context, site detail and backdrop (v006-v013)",
    "GRP_Landscaping": "Building II landscaping (v008-v012)",
}
# face-of-stud Level 1 outline (v001 control polygon) - used only for the walk grid
P1 = [(5, 0), (82.875, 0), (82.875, 2), (94.125, 2), (94.125, 0), (147.875, 0), (147.875, 2), (203, 2), (203, 23.056), (205, 23.056),
      (205, 97.833), (144.5, 97.833), (144.5, 105.833), (104.646, 105.833), (104.646, 104.417), (94.375, 104.417), (94.375, 104.917),
      (0, 104.917), (0, 57.604), (5, 57.604)]
EXTRA_BLOCK = [(135.75, 143.08, 72.58, 82.58, "elevator hoistway (pit at -5 ft): not walkable")]
GRID_CELL, GRID_X0, GRID_Y0, GRID_NX, GRID_NY = 0.25, -2.0, -2.0, 840, 444


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
    """Return the browser group for a v015 object, or None if it is not exported."""
    cols = [c.name for c in obj.users_collection]
    name = obj.name
    if obj.type != "MESH" or not cols or "zz_Cutters" in cols:
        return None
    if name.startswith("TEN_A_"):
        kind = obj.get("kind", "")
        if kind in ("underlay", "perimeter_outline"):
            return None                                  # underlay is drawn by the viewer; ambiguous outline walls stay hidden
        return "GRP_Concept_A_CNSA_ASC"
    if name.startswith("INT_"):
        level = obj.get("level")
        if level in (1, "lid1"):
            return "GRP_Base_Interior_Level_1"
        if level == "roof":
            return "GRP_Base_Interior_Roof"
        return "GRP_Base_Interior_Level_2"               # 2, lid2, terrace
    if obj.hide_render:
        return None                                      # e.g. the hidden north-arrow review aid
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


def flatten_material(mat):
    """Replace a (possibly procedural) Cycles material by a plain glTF-friendly one, in memory only."""
    colour = list(mat.diffuse_color)
    rough, alpha, glass = 0.8, 1.0, False
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
        colour, rough, alpha = [0.62, 0.74, 0.80, 1.0], 0.1, 0.28
    mat.use_nodes = True
    nt = mat.node_tree
    for node in list(nt.nodes):
        nt.nodes.remove(node)
    out, b = nt.nodes.new("ShaderNodeOutputMaterial"), nt.nodes.new("ShaderNodeBsdfPrincipled")
    b.inputs["Base Color"].default_value = (colour[0], colour[1], colour[2], 1.0)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Alpha"].default_value = alpha
    nt.links.new(b.outputs[0], out.inputs["Surface"])
    if alpha < 1.0:
        try:
            mat.surface_render_method = "BLENDED"
        except AttributeError:
            mat.blend_method = "BLEND"
    mat.use_backface_culling = False


def main():
    for path in (GLB, GLB_COPY, DATA, UNDERLAY_COPY):
        if path.exists():
            raise SystemExit(f"Refusing to overwrite existing file: {path}")
    src_hash = sha256(SRC)
    bpy.ops.wm.open_mainfile(filepath=str(SRC))
    scene = bpy.context.scene

    # ---------- metadata first (read straight from the untouched v015 objects) ----------
    viewpoints = []
    for o in sorted(bpy.data.objects, key=lambda o: o.name):
        if o.type == "CAMERA" and o.name.startswith("VP_A_"):
            fwd = o.matrix_world.to_quaternion() @ Vector((0, 0, -1))
            viewpoints.append({"id": o.name, "title": o.get("title", o.name), "position_ft": [round(v / FT, 3) for v in o.location],
                               "forward": [round(v, 5) for v in fwd], "lens_mm": round(o.data.lens, 2)})
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

    # ---------- walk grid: a cell is open only if it is inside Level 1 and nothing solid stands between 0.5 and 6.5 ft ----------
    blocked = bytearray(GRID_NX * GRID_NY)
    for j in range(GRID_NY):
        for i in range(GRID_NX):
            if not inside((GRID_X0 + (i + 0.5) * GRID_CELL, GRID_Y0 + (j + 0.5) * GRID_CELL), P1):
                blocked[j * GRID_NX + i] = 1
    blockers = 0
    for o in bpy.data.objects:
        if o.type != "MESH":
            continue
        name, kind = o.name, o.get("kind", "")
        if name.startswith("INT_"):
            if o.get("level") not in (1, "lid1") or "slab" in name.lower() or "ceiling" in name.lower() or "FUTURE_room" in name:
                continue
        elif name.startswith("TEN_A_"):
            if kind not in ("partition", "demising", "bay_divider", "equipment"):
                continue
        else:
            continue
        lo, hi = bbox_ft(o)
        if hi[2] <= 0.5 or lo[2] >= 6.5:
            continue                                     # floor-level markers, door heads, lids: do not block
        blockers += 1
        i0, i1 = int((lo[0] - GRID_X0) / GRID_CELL), int((hi[0] - GRID_X0) / GRID_CELL)
        j0, j1 = int((lo[1] - GRID_Y0) / GRID_CELL), int((hi[1] - GRID_Y0) / GRID_CELL)
        for j in range(max(0, j0), min(GRID_NY - 1, j1) + 1):
            for i in range(max(0, i0), min(GRID_NX - 1, i1) + 1):
                blocked[j * GRID_NX + i] = 1
    for x0, x1, y0, y1, why in EXTRA_BLOCK:
        for j in range(int((y0 - GRID_Y0) / GRID_CELL), int((y1 - GRID_Y0) / GRID_CELL) + 1):
            for i in range(int((x0 - GRID_X0) / GRID_CELL), int((x1 - GRID_X0) / GRID_CELL) + 1):
                blocked[j * GRID_NX + i] = 1
    rows = []
    for j in range(GRID_NY):                              # run-length encoding per row, starting with an "open" run
        runs, cur, n = [], 0, 0
        for i in range(GRID_NX):
            v = blocked[j * GRID_NX + i]
            if v == cur:
                n += 1
            else:
                runs.append(n)
                cur, n = v, 1
        runs.append(n)
        rows.append(runs)
    open_cells = GRID_NX * GRID_NY - sum(blocked)

    # ---------- group, flatten materials, join (all in memory) ----------
    members = {k: [] for k in GROUPS}
    for o in bpy.data.objects:
        g = classify(o)
        if g:
            members[g].append(o)
    export_objs = [o for objs in members.values() for o in objs]
    source_counts = {k: len(v) for k, v in members.items()}
    for o in export_objs:
        o.hide_viewport = o.hide_render = False
        o.hide_set(False)
    for mat in {s.material for o in export_objs for s in o.material_slots if s.material}:
        flatten_material(mat)

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
                keep_separate.append(o)                  # instanced planting / trees, and pickable tenant room plates
            else:
                mergeable.append(o)
        buckets = {}
        if g == "GRP_Concept_A_CNSA_ASC":
            for o in mergeable:
                buckets.setdefault("TEN_A_" + {"partition": "Partitions", "demising": "Partitions", "bay_divider": "Bay_dividers_TYPE_UNKNOWN",
                                               "equipment": "Table_proxies", "marker": "Floor_markers"}.get(o.get("kind", ""), "Other"), []).append(o)
        else:
            for o in mergeable:
                buckets.setdefault(g.replace("GRP_", "") + "__" + (o.users_collection[0].name if not o.name.startswith("INT_") else
                                                                     ([c.name for c in o.users_collection if not c.name.startswith("BASE_Level")] or [o.users_collection[0].name])[0]), []).append(o)
        nodes = [join(v, k) for k, v in sorted(buckets.items())] + keep_separate
        empty = bpy.data.objects.new(g, None)
        scene.collection.objects.link(empty)
        empty["description"] = GROUPS[g]
        for n_ in nodes:
            n_.parent = empty
            n_.matrix_parent_inverse = Matrix.Identity(4)
        final[g] = [empty] + nodes

    bpy.ops.object.select_all(action="DESELECT")
    for nodes in final.values():
        for o in nodes:
            o.select_set(True)
    for d in (GLB.parent, GLB_COPY.parent, DATA.parent):
        d.mkdir(parents=True, exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=str(GLB), export_format="GLB", use_selection=True, export_apply=True, export_extras=True,
                              export_cameras=False, export_lights=False, export_yup=True, export_materials="EXPORT", export_animations=False)
    assert sha256(SRC) == src_hash, "v015 .blend changed on disk"   # it is never saved by this script
    shutil.copyfile(GLB, GLB_COPY)
    shutil.copyfile(UNDERLAY_SRC, UNDERLAY_COPY)

    # registration of the underlay (from the v015 concept data: x=(X-651.395)/9, y=(1571.795-Y)/9, page 3024 x 2160 pt)
    underlay = {"image": "assets/" + UNDERLAY_COPY.name, "x0_ft": (0.0 - 651.395) / 9.0, "x1_ft": (3024.0 - 651.395) / 9.0,
                "y0_ft": (1571.795 - 2160.0) / 9.0, "y1_ft": 1571.795 / 9.0,
                "source": "tenant_testfits/CNSA_ASC/ASC Rea Farms PRESENTATION PLAN v3 20260915.pdf (registered in v015: scale 1.0000158, RMS 0.027 ft)"}
    data = {"version": "v016", "source_model": "models/building_shell_v015.blend", "source_model_sha256": src_hash,
            "glb": "models/" + GLB.name, "glb_bytes": GLB.stat().st_size,
            "units": {"glb": "metres, Y up (glTF)", "model": "decimal feet, X east, Y north, Z up",
                      "conversion": "x_ft = X / 0.3048 ; y_ft(north) = -Z / 0.3048 ; z_ft(up) = Y / 0.3048"},
            "groups": [{"node": k, "description": v, "source_objects": source_counts[k], "exported_nodes": len(final[k]) - 1} for k, v in GROUPS.items()],
            "concept": {"id": CONCEPT, "tenant": "CNSA Rea Farms ASC", "source": schedule["source"], "areas": schedule["areas"],
                        "warning": "Concept plan does not document tenant doors/openings. Room-to-room circulation is incomplete and no openings have been invented."},
            "viewpoints": viewpoints, "rooms": rooms, "underlay": underlay,
            "walk_grid": {"cell_ft": GRID_CELL, "x0_ft": GRID_X0, "y0_ft": GRID_Y0, "nx": GRID_NX, "ny": GRID_NY, "blocking_objects": blockers,
                          "open_cells": open_cells, "encoding": "per row: run lengths, alternating open / blocked, starting with open",
                          "rule": "open = inside the Level 1 face-of-stud outline and no base-building or tenant solid between 0.5 ft and 6.5 ft; no openings were added",
                          "rows": rows}}
    DATA.write_text(json.dumps(data, separators=(",", ":")), encoding="utf-8")
    print("EXPORT_REPORT=" + json.dumps({"glb_bytes": data["glb_bytes"], "groups": data["groups"], "viewpoints": len(viewpoints), "rooms": len(rooms),
                                         "walk_grid_open_cells": open_cells, "blocking_objects": blockers}))


if __name__ == "__main__":
    main()
