"""Object-by-object comparison BI_footprint_v008.blend -> BI_presentation_v009.blend.
Confirms every object's world-space vertices, per-face material indices, material slot names, transform, collections and
visibility are identical, and lists exactly which materials' node trees changed, plus world / colour-management / camera
differences. Run:  blender --background --python scripts/Building_I/BI_compare_geometry_v008_v009.py
"""
from pathlib import Path
import hashlib
import json
import bpy

ROOT = Path(__file__).resolve().parent.parent.parent
A = ROOT / "models" / "Building_I" / "BI_footprint_v008.blend"
B = ROOT / "models" / "Building_I" / "BI_presentation_v009.blend"


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
    geo, mats, extra = {}, {}, {}
    for o in bpy.data.objects:
        h = hashlib.sha256()
        h.update(",".join(f"{v:.5f}" for row in o.matrix_world for v in row).encode())
        h.update("|".join(sorted(c.name for c in o.users_collection)).encode())
        h.update(f"{o.hide_render}{o.hide_viewport}{o.type}".encode())
        if o.type == "MESH":
            for v in o.data.vertices:
                w = o.matrix_world @ v.co
                h.update(f"{w.x:.5f},{w.y:.5f},{w.z:.5f};".encode())
            h.update(",".join(str(p.material_index) for p in o.data.polygons).encode())
            h.update("|".join(s.material.name if s.material else "-" for s in o.material_slots).encode())
        geo[o.name] = h.hexdigest()
    for mt in bpy.data.materials:
        mats[mt.name] = mat_sig(mt)
    sc = bpy.context.scene
    extra["world"] = [n.bl_idname for n in sc.world.node_tree.nodes] if sc.world and sc.world.use_nodes else None
    extra["view"] = (sc.view_settings.view_transform, sc.view_settings.look, sc.view_settings.exposure)
    extra["samples"] = sc.cycles.samples
    extra["cameras"] = sorted(o.name for o in bpy.data.objects if o.type == "CAMERA")
    extra["lights_render"] = {o.name: o.hide_render for o in bpy.data.objects if o.type == "LIGHT"}
    return geo, mats, extra


ga, ma, ea = snapshot(A)
gb, mb, eb = snapshot(B)
changed = sorted(n for n in ga if n in gb and ga[n] != gb[n])
added = sorted(n for n in gb if n not in ga)
removed = sorted(n for n in ga if n not in gb)
mats_changed = sorted(n for n in ma if n in mb and ma[n] != mb[n])
mats_added = sorted(n for n in mb if n not in ma)
mats_removed = sorted(n for n in ma if n not in mb)
res = {"v008_objects": len(ga), "v009_objects": len(gb),
       "objects_changed_geometry_transform_assignment_or_collection": changed, "objects_added": added, "objects_removed": removed,
       "geometry_identical_for_all_common_objects": not changed and not removed,
       "materials_changed_node_trees": mats_changed, "materials_added": mats_added, "materials_removed": mats_removed,
       "world_nodes": {"v008": ea["world"], "v009": eb["world"]}, "view": {"v008": ea["view"], "v009": eb["view"]},
       "samples": {"v008": ea["samples"], "v009": eb["samples"]}, "cameras_added": sorted(set(eb["cameras"]) - set(ea["cameras"])),
       "sun_lamp_hide_render": {"v008": ea["lights_render"], "v009": eb["lights_render"]}}
print("COMPARE=" + json.dumps(res))
