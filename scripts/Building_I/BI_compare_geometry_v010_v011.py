"""Object-by-object comparison BI_entrance_site_v010.blend -> BI_entrance_facade_v011.blend.
Confirms that every object except the two rebuilt finish regions (FR_WEST_PNL1_W2b, FR_WEST_GLZ_W2) is identical
(world-space vertices, per-face material indices, material slot names, transform, collections, visibility) - building,
canopy, vestibule, v010 site and curbs, landscape - that no material node tree changed, and lists exactly what changed.
Run:  blender --background --python scripts/Building_I/BI_compare_geometry_v010_v011.py
Writes notes/Building_I/BI_compare_v010_v011.json (refuses to overwrite).
"""
from pathlib import Path
import hashlib
import json
import bpy

ROOT = Path(__file__).resolve().parent.parent.parent
A = ROOT / "models" / "Building_I" / "BI_entrance_site_v010.blend"
B = ROOT / "models" / "Building_I" / "BI_entrance_facade_v011.blend"
OUT = ROOT / "notes" / "Building_I" / "BI_compare_v010_v011.json"
FT = 0.3048


def mat_sig(mt):
    h = hashlib.sha256()
    if mt.use_nodes and mt.node_tree:
        for n in sorted(mt.node_tree.nodes, key=lambda x: x.name):
            h.update(n.bl_idname.encode())
            for i in n.inputs:
                dv = getattr(i, "default_value", None)
                try:
                    h.update(json.dumps(list(dv) if hasattr(dv, "__len__") else dv).encode())
                except TypeError:
                    pass
        for l in mt.node_tree.links:
            h.update(f"{l.from_node.bl_idname}.{l.from_socket.name}->{l.to_node.bl_idname}.{l.to_socket.name}".encode())
    return h.hexdigest()


def snapshot(path):
    bpy.ops.wm.open_mainfile(filepath=str(path))
    geo, mats, bbox, extra = {}, {}, {}, {}
    for o in bpy.data.objects:
        h = hashlib.sha256()
        h.update(",".join(f"{v:.5f}" for row in o.matrix_world for v in row).encode())
        h.update("|".join(sorted(c.name for c in o.users_collection)).encode())
        h.update(f"{o.hide_render}{o.hide_viewport}{o.type}".encode())
        if o.type == "MESH":
            xs, ys, zs = [], [], []
            for v in o.data.vertices:
                w = o.matrix_world @ v.co
                h.update(f"{w.x:.5f},{w.y:.5f},{w.z:.5f};".encode())
                xs.append(w.x); ys.append(w.y); zs.append(w.z)
            h.update(",".join(str(p.material_index) for p in o.data.polygons).encode())
            h.update("|".join(s.material.name if s.material else "-" for s in o.material_slots).encode())
            if xs:
                bbox[o.name] = [round(min(xs) / FT, 2), round(min(ys) / FT, 2), round(min(zs) / FT, 2), round(max(xs) / FT, 2), round(max(ys) / FT, 2), round(max(zs) / FT, 2),
                                len(o.data.vertices), len(o.data.polygons), "|".join(s.material.name if s.material else "-" for s in o.material_slots)]
        geo[o.name] = h.hexdigest()
    for mt in bpy.data.materials:
        mats[mt.name] = mat_sig(mt)
    sc = bpy.context.scene
    extra["world"] = [n.bl_idname for n in sc.world.node_tree.nodes] if sc.world and sc.world.use_nodes else None
    extra["view"] = (sc.view_settings.view_transform, sc.view_settings.look, sc.view_settings.exposure)
    extra["samples"] = sc.cycles.samples
    extra["cameras"] = sorted(o.name for o in bpy.data.objects if o.type == "CAMERA")
    return geo, mats, bbox, extra


if OUT.exists():
    raise SystemExit(f"refusing to overwrite {OUT}")
ga, ma, ba, ea = snapshot(A)
gb, mb, bb, eb = snapshot(B)
changed = sorted(n for n in ga if n in gb and ga[n] != gb[n])
added = sorted(n for n in gb if n not in ga)
removed = sorted(n for n in ga if n not in gb)
building_a = sorted(n for n in ga if n.startswith(("BI_", "FR_")) and not n.startswith("BI_cam") and n not in ("FR_WEST_PNL1_W2b", "FR_WEST_GLZ_W2"))
building_changed = [n for n in changed if n in building_a]
building_missing = [n for n in building_a if n not in gb]
site_changed = [n for n in changed if n.startswith(("SITE_", "CTX_"))]
land_changed = [n for n in changed if n.startswith("LS_")]
other_changed = [n for n in changed if n not in site_changed and n not in land_changed and n not in building_changed]
res = {"v010_objects": len(ga), "v011_objects": len(gb),
       "building_facade_openings_canopy_objects_excluding_the_two_rebuilt_regions": len(building_a), "rebuilt_regions_changed": [n for n in changed if n in ("FR_WEST_PNL1_W2b", "FR_WEST_GLZ_W2")], "building_objects_changed": building_changed, "building_objects_missing": building_missing,
       "building_identical": not building_changed and not building_missing,
       "objects_changed": {"site": site_changed, "landscape": land_changed, "other": other_changed},
       "objects_added": added, "objects_removed": removed,
       "objects_changed_count": len(changed), "objects_identical_count": len([n for n in ga if n in gb and ga[n] == gb[n]]),
       "materials_changed_node_trees": sorted(n for n in ma if n in mb and ma[n] != mb[n]),
       "materials_added": sorted(n for n in mb if n not in ma), "materials_removed": sorted(n for n in ma if n not in mb),
       "world_nodes_identical": ea["world"] == eb["world"], "view_identical": ea["view"] == eb["view"], "samples": {"v010": ea["samples"], "v011": eb["samples"]},
       "cameras_added": sorted(set(eb["cameras"]) - set(ea["cameras"])),
       "bbox_ft_changed_and_added": {n: {"v010": ba.get(n), "v011": bb.get(n)} for n in changed + added if n in bb or n in ba}}
OUT.write_text(json.dumps(res, indent=2), encoding="utf-8")
print("COMPARE=" + json.dumps({k: v for k, v in res.items() if k != "bbox_ft_changed_and_added"}))
