"""Object-by-object comparison BI_landscape_v007.blend -> BI_footprint_v008.blend, plus footprint areas.
Lists every object changed / added / removed by class, confirms the canopy, vestibule, mechanical screen, grid, site
(except the foundation skirts) and non-rebuilt landscape objects are identical, and rasterises the Level 1 footprint of
both models (0.1 ft cells, shell objects cut at z = 1 ft) to report the square-foot change.
Run:  blender --background --python scripts/Building_I/BI_compare_geometry_v007_v008.py
"""
from pathlib import Path
import json
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parent.parent.parent
A = ROOT / "models" / "Building_I" / "BI_landscape_v007.blend"
B = ROOT / "models" / "Building_I" / "BI_footprint_v008.blend"
FT = 0.3048


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
    # Level 1 footprint raster: shell objects (01_Shell) that contain z = 1 ft -> point-in-solid test by ray parity
    shell = [o for o in bpy.data.collections["01_Shell"].objects if o.type == "MESH"]
    cells = set()
    step = 0.5
    zc = 1.0 * FT
    for o in shell:
        bb = [o.matrix_world @ Vector(c) for c in o.bound_box]
        if min(p.z for p in bb) > zc or max(p.z for p in bb) < zc:
            continue
        x0, x1 = min(p.x for p in bb) / FT, max(p.x for p in bb) / FT
        y0, y1 = min(p.y for p in bb) / FT, max(p.y for p in bb) / FT
        inv = o.matrix_world.inverted()
        direction = (inv.to_3x3() @ Vector((0, 0, 1))).normalized()
        ix0, ix1 = int(x0 // step) - 1, int(x1 // step) + 1     # common global grid so cells of both models coincide
        iy0, iy1 = int(y0 // step) - 1, int(y1 // step) + 1
        for i in range(ix0, ix1 + 1):
            for j in range(iy0, iy1 + 1):
                x = (i + 0.5) * step
                y = (j + 0.5) * step
                p = inv @ Vector((x * FT, y * FT, zc))
                hits = 0
                o_ = p.copy()
                for _ in range(30):
                    hit, loc, nrm, idx = o.ray_cast(o_, direction)
                    if not hit:
                        break
                    hits += 1
                    o_ = loc + direction * 1e-4
                if hits % 2 == 1:
                    cells.add((round(x, 2), round(y, 2)))
    return verts, mats, colls, hidden, fidx, cells, step


va, ma, ca, ha, fa, cells_a, step = snapshot(A)
vb, mb, cb, hb, fb, cells_b, _ = snapshot(B)
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
    if n.startswith("SITE_foundation_skirt"):
        return "foundation_skirt"
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
    if n.startswith("BI_screen"):
        return "parapet_screen"
    if n.startswith("BI_grid"):
        return "grid"
    if n.startswith("BI_Z3_vestibule") or n.startswith("BI_Z6_mech"):
        return "vestibule_mech_screen"
    if n.startswith("BI_Z") or n == "BI_L2_floor_slab":
        return "shell"
    if n.startswith("BI_"):
        return "other_building"
    return "other"


def group(names):
    g = {}
    for n in names:
        g.setdefault(cls(n), []).append(n)
    return g


chg = group([c["object"] for c in changed])
add = group(added)
mis = group(missing)
area_a = len(cells_a) * step * step
area_b = len(cells_b) * step * step
only_a = cells_a - cells_b
only_b = cells_b - cells_a
res = {"v007_objects": len(ca), "v008_objects": len(cb),
       "changed_by_class": {k: len(v) for k, v in chg.items()}, "added_by_class": {k: len(v) for k, v in add.items()}, "removed_by_class": {k: len(v) for k, v in mis.items()},
       "changed_objects": {k: v for k, v in chg.items() if k not in ("opening", "facade_region")},
       "added_objects": {k: v for k, v in add.items() if k not in ("opening", "facade_region")},
       "removed_objects": {k: v for k, v in mis.items() if k not in ("opening", "facade_region")},
       "canopy_identical": "canopy" not in chg and "canopy" not in mis,
       "vestibule_and_mech_screen_identical": "vestibule_mech_screen" not in chg and "vestibule_mech_screen" not in mis,
       "grid_identical": "grid" not in chg and "grid" not in mis,
       "site_identical_except_skirts": "site" not in chg and "site" not in mis and "site" not in add,
       "landscape_unchanged_count": len([n for n in common if cls(n) == "landscape" and n not in {c["object"] for c in changed}]),
       "landscape_changed": chg.get("landscape", []), "landscape_added": add.get("landscape", []), "landscape_removed": mis.get("landscape", []),
       "footprint_L1_at_z1ft": {"cell_ft": step, "v007_sqft": round(area_a, 0), "v008_sqft": round(area_b, 0), "change_sqft": round(area_b - area_a, 0),
                                "removed_from_v007_sqft": round(len(only_a) * step * step, 0), "added_in_v008_sqft": round(len(only_b) * step * step, 0)}}
print("COMPARE=" + json.dumps(res))
