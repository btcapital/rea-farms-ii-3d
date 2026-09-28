"""Independent check: every object of BI_site_v003.blend exists in BI_landscape_v004.blend with identical
world-space vertices (0.1 mm), material slots, collections and visibility; every object added in v004 is
prefixed LS_ or CTX_ and lives under 09_Landscape_v004 (plus the camera BI_cam_landscape_entry in 90_Cameras).
Run with Blender in background:  blender --background --python scripts/Building_I/BI_compare_geometry_v003_v004.py
"""
from pathlib import Path
import json
import bpy

ROOT = Path(__file__).resolve().parent.parent.parent
A = ROOT / "models" / "Building_I" / "BI_site_v003.blend"
B = ROOT / "models" / "Building_I" / "BI_landscape_v004.blend"


def snapshot(path):
    bpy.ops.wm.open_mainfile(filepath=str(path))
    verts, mats, colls, hidden = {}, {}, {}, {}
    for o in bpy.data.objects:
        if o.type == "MESH":
            verts[o.name] = [tuple(round(c, 4) for c in (o.matrix_world @ v.co)) for v in o.data.vertices]
            mats[o.name] = [s.material.name if s.material else None for s in o.material_slots]
        colls[o.name] = sorted(c.name for c in o.users_collection)
        hidden[o.name] = (o.hide_render, o.hide_viewport)
    return verts, mats, colls, hidden


va, ma, ca, ha = snapshot(A)
vb, mb, cb, hb = snapshot(B)
missing = [n for n in va if n not in vb]
changed = [n for n in va if n in vb and va[n] != vb[n]]
mat_changed = [n for n in va if n in mb and ma[n] != mb[n]]
coll_changed = [n for n in ca if n in cb and ca[n] != cb[n]]
vis_changed = [n for n in ha if n in hb and ha[n] != hb[n]]
added = [n for n in cb if n not in ca]
bad_prefix = [n for n in added if not (n.startswith("LS_") or n.startswith("CTX_") or n == "BI_cam_landscape_entry")]
bad_coll = [n for n in added if not any(c.startswith("09_Landscape_v004") for c in cb[n]) and n != "BI_cam_landscape_entry"]
res = {"v003_objects": len(ca), "v004_objects": len(cb), "v003_mesh_objects": len(va),
       "missing_in_v004": missing, "vertex_changed": changed, "material_slots_changed": mat_changed,
       "collection_changed": coll_changed, "visibility_changed": vis_changed,
       "added_in_v004": len(added), "added_prefixes": sorted({n.split("_")[0] for n in added}),
       "added_not_landscape_prefixed": bad_prefix, "added_outside_09_Landscape_v004": bad_coll,
       "v003_identical": not (missing or changed or mat_changed or coll_changed or vis_changed)}
print("COMPARE=" + json.dumps(res))
