"""Independent check for the v005 facade cleanup:
  * every object of BI_landscape_v004.blend that is not a v002 overlay box (FD_*) exists in BI_landscape_v005.blend
    with identical world-space vertices (0.1 mm), material slots, per-face material indices, collections and visibility
    (shell, parapets, canopy, openings, grid, site, landscape, cameras);
  * all FD_* overlay objects are absent from v005;
  * every object added in v005 is FR_* inside 07_Facade_regions_v005 (plus the three validation cameras);
  * no FR polygon overlaps a v001 opening placeholder on the same plane (glazing/door exclusion);
  * no two FR polygons on the same plane overlap (coplanar z-fighting check).
Run:  blender --background --python scripts/Building_I/BI_compare_geometry_v004_v005.py
"""
from pathlib import Path
import json
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parent.parent.parent
A = ROOT / "models" / "Building_I" / "BI_landscape_v004.blend"
B = ROOT / "models" / "Building_I" / "BI_landscape_v005.blend"
FT = 0.3048


def snapshot(path):
    bpy.ops.wm.open_mainfile(filepath=str(path))
    verts, mats, colls, hidden, fidx = {}, {}, {}, {}, {}
    for o in bpy.data.objects:
        if o.type == "MESH":
            verts[o.name] = [tuple(round(c, 4) for c in (o.matrix_world @ v.co)) for v in o.data.vertices]
            mats[o.name] = [s.material.name if s.material else None for s in o.material_slots]
            fidx[o.name] = [p.material_index for p in o.data.polygons]
        colls[o.name] = sorted(c.name for c in o.users_collection)
        hidden[o.name] = (o.hide_render, o.hide_viewport)
    return verts, mats, colls, hidden, fidx


va, ma, ca, ha, fa = snapshot(A)
keep = [n for n in ca if not n.startswith("FD_")]
fd_in_a = [n for n in ca if n.startswith("FD_")]
vb, mb, cb, hb, fb = snapshot(B)   # B is now open
missing = [n for n in keep if n not in cb]
changed = [n for n in keep if n in va and n in vb and va[n] != vb[n]]
mat_changed = [n for n in keep if n in ma and n in mb and (ma[n] != mb[n] or fa[n] != fb[n])]
coll_changed = [n for n in keep if n in cb and ca[n] != cb[n]]
vis_changed = [n for n in keep if n in hb and ha[n] != hb[n]]
fd_left = [n for n in cb if n.startswith("FD_")]
added = [n for n in cb if n not in ca]
cams = {"BI_cam_north_elevation_ortho", "BI_cam_entrance_closeup", "BI_cam_oblique_northeast"}
bad_prefix = [n for n in added if not n.startswith("FR_") and n not in cams]
bad_coll = [n for n in added if n.startswith("FR_") and "07_Facade_regions_v005" not in cb[n]]

# ---- geometric checks on the new region polygons (B is open)
def rect_of(o):
    bb = [o.matrix_world @ Vector(c) for c in o.bound_box]
    x0, x1 = min(q.x for q in bb) / FT, max(q.x for q in bb) / FT
    y0, y1 = min(q.y for q in bb) / FT, max(q.y for q in bb) / FT
    z0, z1 = min(q.z for q in bb) / FT, max(q.z for q in bb) / FT
    return (x0, x1, y0, y1, z0, z1)


openings = []
for o in bpy.data.collections["04_Openings"].objects:
    x0, x1, y0, y1, z0, z1 = rect_of(o)
    if (x1 - x0) < (y1 - y0):
        openings.append(("x", (x0 + x1) / 2, (y0, y1, z0, z1)))
    else:
        openings.append(("y", (y0 + y1) / 2, (x0, x1, z0, z1)))

polys = []  # (axis, plane, u0,u1,z0,z1, obj)
for o in bpy.data.collections["07_Facade_regions_v005"].objects:
    mw = o.matrix_world
    for p in o.data.polygons:
        pts = [mw @ o.data.vertices[i].co for i in p.vertices]
        n = (mw.to_3x3() @ p.normal).normalized()
        if abs(n.x) > 0.99:
            polys.append(("x", sum(q.x for q in pts) / len(pts) / FT, min(q.y for q in pts) / FT, max(q.y for q in pts) / FT, min(q.z for q in pts) / FT, max(q.z for q in pts) / FT, o.name))
        elif abs(n.y) > 0.99:
            polys.append(("y", sum(q.y for q in pts) / len(pts) / FT, min(q.x for q in pts) / FT, max(q.x for q in pts) / FT, min(q.z for q in pts) / FT, max(q.z for q in pts) / FT, o.name))


def overlap(a, b, tol=0.02):
    return min(a[1], b[1]) - max(a[0], b[0]) > tol and min(a[3], b[3]) - max(a[2], b[2]) > tol


open_hits = []
for ax, pl, u0, u1, z0, z1, nm in polys:
    for oax, opl, r in openings:
        if oax == ax and abs(opl - pl) < 0.4 and overlap((u0, u1, z0, z1), r):
            open_hits.append((nm, round(pl, 2), [round(v, 2) for v in r]))
            break
cop_hits = 0
byplane = {}
for rec in polys:
    byplane.setdefault((rec[0], round(rec[1], 2)), []).append(rec)
for k, lst in byplane.items():
    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):
            a, b = lst[i], lst[j]
            if overlap((a[2], a[3], a[4], a[5]), (b[2], b[3], b[4], b[5])):
                cop_hits += 1

res = {"v004_objects": len(ca), "v005_objects": len(cb), "v004_overlay_boxes": len(fd_in_a), "overlay_boxes_left_in_v005": len(fd_left),
       "kept_objects_checked": len(keep), "missing_in_v005": missing, "vertex_changed": changed, "material_changed": mat_changed,
       "collection_changed": coll_changed, "visibility_changed": vis_changed,
       "added_in_v005": len(added), "added_not_FR_or_camera": bad_prefix, "FR_outside_collection": bad_coll,
       "region_polygons": len(polys), "region_polygons_overlapping_openings": len(open_hits), "opening_hits_sample": open_hits[:8],
       "coplanar_overlapping_region_pairs": cop_hits,
       "v004_non_overlay_identical": not (missing or changed or mat_changed or coll_changed or vis_changed)}
print("COMPARE=" + json.dumps(res))
