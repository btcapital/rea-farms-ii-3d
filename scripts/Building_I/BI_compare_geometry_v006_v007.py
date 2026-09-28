"""Object-by-object comparison BI_landscape_v006.blend -> BI_landscape_v007.blend.
Confirms every building, facade-region, opening, canopy, camera and site object is identical (world-space vertices,
material slots, per-face material indices, collections, visibility) and lists exactly which landscape objects changed,
were added or removed. Run:  blender --background --python scripts/Building_I/BI_compare_geometry_v006_v007.py
"""
from pathlib import Path
import json
import bpy

ROOT = Path(__file__).resolve().parent.parent.parent
A = ROOT / "models" / "Building_I" / "BI_landscape_v006.blend"
B = ROOT / "models" / "Building_I" / "BI_landscape_v007.blend"


def snapshot(path):
    bpy.ops.wm.open_mainfile(filepath=str(path))
    verts, mats, colls, hidden, fidx = {}, {}, {}, {}, {}
    for o in bpy.data.objects:
        if o.type == "MESH":
            verts[o.name] = sorted(tuple(round(c, 4) for c in (o.matrix_world @ v.co)) for v in o.data.vertices)
            mats[o.name] = [s.material.name if s.material else None for s in o.material_slots]
            fidx[o.name] = sorted(p.material_index for p in o.data.polygons)
        colls[o.name] = sorted(c.name for c in o.users_collection)
        hidden[o.name] = (o.hide_render, o.hide_viewport)
    return verts, mats, colls, hidden, fidx


va, ma, ca, ha, fa = snapshot(A)
vb, mb, cb, hb, fb = snapshot(B)
common = [n for n in ca if n in cb]
missing = [n for n in ca if n not in cb]
added = [n for n in cb if n not in ca]
changed = []
for n in common:
    why = []
    if n in va and n in vb and va[n] != vb[n]:
        why.append("vertices")
    if n in ma and n in mb and ma[n] != mb[n]:
        why.append("materials")
    if n in fa and n in fb and fa[n] != fb[n]:
        why.append("face_material_indices")
    if ca[n] != cb[n]:
        why.append("collection")
    if ha[n] != hb[n]:
        why.append("visibility")
    if why:
        changed.append({"object": n, "changed": why})


def cls(n):
    if n.startswith(("LS_", "CTX_existing_street_tree")):
        return "landscape"
    if n.startswith("SITE_") or n.startswith("CTX_"):
        return "site"
    if n.startswith("FR_"):
        return "facade_region"
    if n.startswith("BI_open_"):
        return "opening"
    if n.startswith("BI_canopy"):
        return "canopy"
    if n.startswith("BI_cam"):
        return "camera"
    if n.startswith("BI_"):
        return "building"
    return "other"


by_class = {}
for c in changed:
    by_class.setdefault(cls(c["object"]), []).append(c["object"])
add_class = {}
for n in added:
    add_class.setdefault(cls(n), []).append(n)
miss_class = {}
for n in missing:
    miss_class.setdefault(cls(n), []).append(n)
entrance = ["BI_Z4b_north_block_south_part", "BI_Z2_band_E_F2", "BI_Z3_vestibule_100"] + [n for n in common if n.startswith("BI_open_NORTH_")]
res = {"v006_objects": len(ca), "v007_objects": len(cb),
       "changed_by_class": {k: len(v) for k, v in by_class.items()}, "added_by_class": {k: len(v) for k, v in add_class.items()}, "removed_by_class": {k: len(v) for k, v in miss_class.items()},
       "changed_non_landscape": [c for c in changed if cls(c["object"]) != "landscape"],
       "added_non_landscape": [n for n in added if cls(n) != "landscape"], "removed_non_landscape": [n for n in missing if cls(n) != "landscape"],
       "changed_landscape": by_class.get("landscape", []), "added_landscape": add_class.get("landscape", []), "removed_landscape": miss_class.get("landscape", []),
       "building_identical": not any(cls(c["object"]) == "building" for c in changed),
       "facade_regions_identical": not any(cls(c["object"]) == "facade_region" for c in changed),
       "openings_identical": not any(cls(c["object"]) == "opening" for c in changed),
       "entrance_correction_identical": all(n in cb and (n not in va or va[n] == vb[n]) for n in entrance),
       "site_identical": not any(cls(c["object"]) == "site" for c in changed) and not add_class.get("site") and not miss_class.get("site")}
print("COMPARE=" + json.dumps(res))
