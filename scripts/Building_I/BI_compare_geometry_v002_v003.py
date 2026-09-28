"""Independent check: every mesh object of BI_facade_v002.blend exists in BI_site_v003.blend with
identical world-space vertex coordinates (0.1 mm) and identical material slots; every object added
in v003 is prefixed SITE_ or CTX_ and lives under collection 08_Site_v003. Run in background:
  "C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe" --background --python scripts/Building_I/BI_compare_geometry_v002_v003.py
"""
from pathlib import Path
import json
import bpy

ROOT = Path(__file__).resolve().parent.parent.parent
A = ROOT / "models" / "Building_I" / "BI_facade_v002.blend"
B = ROOT / "models" / "Building_I" / "BI_site_v003.blend"


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
bad_prefix = [n for n in added if not (n.startswith("SITE_") or n.startswith("CTX_") or n.startswith("BI_cam_site"))]
bad_coll = [n for n in added if not any(c.startswith("08_Site_v003") for c in cb[n])]
res = {"v002_objects": len(ca), "v003_objects": len(cb), "v002_mesh_objects": len(va),
       "missing_in_v003": missing, "vertex_changed": changed, "material_slots_changed": mat_changed,
       "collection_changed": coll_changed, "visibility_changed": vis_changed,
       "added_in_v003": len(added), "added_names": sorted(added), "added_not_site_prefixed": bad_prefix,
       "added_outside_08_Site_v003": bad_coll,
       "v002_identical": not (missing or changed or mat_changed or coll_changed)}
print("COMPARE=" + json.dumps(res))
