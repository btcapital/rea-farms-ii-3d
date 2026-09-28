"""Independent check: every mesh object of BI_shell_v001.blend exists in BI_facade_v002.blend
with identical world-space vertex coordinates (0.1 mm). Run with Blender in background:
  "C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe" --background --python scripts/Building_I/BI_compare_geometry_v001_v002.py
"""
from pathlib import Path
import json
import bpy

ROOT = Path(__file__).resolve().parent.parent.parent
A = ROOT / "models" / "Building_I" / "BI_shell_v001.blend"
B = ROOT / "models" / "Building_I" / "BI_facade_v002.blend"


def snapshot(path):
    bpy.ops.wm.open_mainfile(filepath=str(path))
    out = {}
    for o in bpy.data.objects:
        if o.type == "MESH":
            out[o.name] = [tuple(round(c, 4) for c in (o.matrix_world @ v.co)) for v in o.data.vertices]
    mats = {o.name: [s.material.name if s.material else None for s in o.material_slots] for o in bpy.data.objects if o.type == "MESH"}
    return out, mats


a, ma = snapshot(A)
b, mb = snapshot(B)
missing = [n for n in a if n not in b]
changed = [n for n in a if n in b and a[n] != b[n]]
added = [n for n in b if n not in a]
mat_changed = [n for n in a if n in mb and ma[n] != mb[n]]
res = {"v001_mesh_objects": len(a), "v002_mesh_objects": len(b), "missing_in_v002": missing, "vertex_changed": changed,
       "added_in_v002": len(added), "added_prefixes": sorted({n.split("_")[0] for n in added}),
       "material_slots_changed_on_v001_objects": len(mat_changed), "geometry_identical": not missing and not changed}
print("COMPARE=" + json.dumps(res))
