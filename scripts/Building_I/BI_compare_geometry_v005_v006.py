"""Object-by-object comparison BI_landscape_v005.blend -> BI_landscape_v006.blend.
Reports every object whose world-space vertices, material slots, per-face material indices, collections or visibility
differ, with the previous and new y-plane for the moved placeholders; confirms Z4b vertices are identical and that no
cap triangle lies in the entrance notch; lists added objects (validation cameras only expected).
Run:  blender --background --python scripts/Building_I/BI_compare_geometry_v005_v006.py
"""
from pathlib import Path
import json
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parent.parent.parent
A = ROOT / "models" / "Building_I" / "BI_landscape_v005.blend"
B = ROOT / "models" / "Building_I" / "BI_landscape_v006.blend"
FT = 0.3048


def snapshot(path):
    bpy.ops.wm.open_mainfile(filepath=str(path))
    verts, mats, colls, hidden, fidx, bboxes, tris = {}, {}, {}, {}, {}, {}, {}
    for o in bpy.data.objects:
        if o.type == "MESH":
            verts[o.name] = sorted(tuple(round(c, 4) for c in (o.matrix_world @ v.co)) for v in o.data.vertices)
            mats[o.name] = [s.material.name if s.material else None for s in o.material_slots]
            fidx[o.name] = sorted(p.material_index for p in o.data.polygons)
            bb = [o.matrix_world @ Vector(c) for c in o.bound_box]
            bboxes[o.name] = [round(min(q.x for q in bb) / FT, 2), round(min(q.y for q in bb) / FT, 2), round(min(q.z for q in bb) / FT, 2), round(max(q.x for q in bb) / FT, 2), round(max(q.y for q in bb) / FT, 2), round(max(q.z for q in bb) / FT, 2)]
            if o.name == "BI_Z4b_north_block_south_part":
                o.data.calc_loop_triangles()
                n = 0
                for t in o.data.loop_triangles:
                    vs = [o.matrix_world @ o.data.vertices[i].co for i in t.vertices]
                    cx = sum(v.x for v in vs) / 3 / FT; cy = sum(v.y for v in vs) / 3 / FT
                    if 30 < cx < 71 and 74.6 < cy < 97.7:
                        n += 1
                tris[o.name] = {"polygons": len(o.data.polygons), "triangles_in_entrance_notch": n}
        colls[o.name] = sorted(c.name for c in o.users_collection)
        hidden[o.name] = (o.hide_render, o.hide_viewport)
    return verts, mats, colls, hidden, fidx, bboxes, tris


va, ma, ca, ha, fa, ba, ta = snapshot(A)
vb, mb, cb, hb, fb, bb_, tb = snapshot(B)
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
        rec = {"object": n, "changed": why}
        if n in ba:
            rec["bbox_before_ft"] = ba[n]; rec["bbox_after_ft"] = bb_[n]
            if n.startswith("BI_open_"):
                rec["plane_before_ft"] = round((ba[n][1] + ba[n][4]) / 2, 2); rec["plane_after_ft"] = round((bb_[n][1] + bb_[n][4]) / 2, 2)
                rec["shift_ft"] = round(rec["plane_after_ft"] - rec["plane_before_ft"], 2)
        changed.append(rec)
z4b_same_verts = va["BI_Z4b_north_block_south_part"] == vb["BI_Z4b_north_block_south_part"]
canopy = [n for n in common if n.startswith("BI_canopy")]
canopy_changed = [n for n in canopy if va[n] != vb[n] or ma[n] != mb[n]]
groups = {"openings": [c for c in changed if c["object"].startswith("BI_open_")], "shell": [c for c in changed if c["object"].startswith("BI_Z")],
          "facade_regions": [c["object"] for c in changed if c["object"].startswith("FR_")],
          "other": [c["object"] for c in changed if not c["object"].startswith(("BI_open_", "BI_Z", "FR_"))]}
res = {"v005_objects": len(ca), "v006_objects": len(cb), "missing_in_v006": missing, "added_in_v006": added,
       "changed_objects_total": len(changed), "changed_openings": groups["openings"], "changed_shell": groups["shell"],
       "changed_facade_regions": groups["facade_regions"], "changed_other": groups["other"],
       "z4b_vertices_identical": z4b_same_verts, "z4b_before": ta.get("BI_Z4b_north_block_south_part"), "z4b_after": tb.get("BI_Z4b_north_block_south_part"),
       "canopy_objects": len(canopy), "canopy_changed": canopy_changed,
       "site_landscape_changed": [c["object"] for c in changed if c["object"].startswith(("SITE_", "CTX_", "LS_"))]}
print("COMPARE=" + json.dumps(res))
