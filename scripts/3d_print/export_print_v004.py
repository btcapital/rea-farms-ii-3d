"""Building II print derivative v004 (MULTICOLOR SITE BASE) - 3MF EXPORT at 1:240 in millimetres (read-only; the .blend
is never saved).

Run:  blender -b models/Building_II/print_derivatives/building_II_print_v004.blend \
            --python scripts/3d_print/export_print_v004.py
      (or, with Blender as a Python module:  python scripts/3d_print/export_print_v004.py)
Writes exports/Building_II/3d_print/3mf/building_II_v004_1-240_multicolor_site_base.3mf - a Bambu Studio multi-part
object (generic 3MF + Metadata/model_settings.config with a filament per part, written by the frozen bambu_3mf_v003):
  ONE object, 3 parts in priority order (a later part wins where parts overlap in Bambu Studio)
    1 site base (exact v003 geometry, triangles taken verbatim from the v003 3MF) -> filament 3 Gray
    2 lawn / planting beds / shrubs / tree canopy                                -> filament 4 Green
    3 asphalt drive + Onyx entry plaza + yard copings                            -> filament 2 Black
Placement = v003 site base exactly (same item transform: upright, centred on the 340 x 320 bed, lowest point Z = 0).
The v003 building, drop-off canopy and sun-shade 3MF files are the companions; they are not rewritten.
"""
import bpy, bmesh, hashlib, json, os, sys, time, zipfile
import numpy as np
import xml.etree.ElementTree as ET

T0 = time.time()
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BLEND = os.path.join(ROOT, "models", "Building_II", "print_derivatives", "building_II_print_v004.blend")
if os.path.abspath(bpy.data.filepath or "") != BLEND:
    bpy.ops.wm.open_mainfile(filepath=BLEND, load_ui=False)
sys.path.insert(0, os.path.join(ROOT, "scripts", "3d_print"))
import bambu_3mf_v003 as B3
EXP = os.path.join(ROOT, "exports", "Building_II", "3d_print")
MF, VAL = os.path.join(EXP, "3mf"), os.path.join(EXP, "validation")
def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()
K = 1000.0 / 240.0
V003_SITE = os.path.join(MF, "building_II_v003_1-240_site_base.3mf")
assert sha(V003_SITE) == "9c533994379897554a8cd7e93eeb9e2fc1a0fcbb3ce7bd9ff9c565970ca4682e", "v003 site base 3MF changed"
OUT_3MF = os.path.join(MF, "building_II_v004_1-240_multicolor_site_base.3mf")
assert not os.path.exists(OUT_3MF), "v004 3MF exists - never overwrite an export (make a new version)"

NS = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
z = zipfile.ZipFile(V003_SITE)
_o = ET.fromstring(z.read("3D/Objects/object_1.model")).find("m:resources/m:object", NS)
BASE_MM = np.array([[float(v.get(a)) for a in "xyz"] for v in _o.findall("m:mesh/m:vertices/m:vertex", NS)])
BASE_TV = np.array([[int(t.get(a)) for a in ("v1", "v2", "v3")] for t in _o.findall("m:mesh/m:triangles/m:triangle", NS)], dtype=np.int64)
_item = ET.fromstring(z.read("3D/3dmodel.model")).find("m:build/m:item", NS)
T_V003 = [float(x) for x in _item.get("transform").split()]

def blend_tris(name):
    """colour part triangles in mm, model space: every polygon split with the BEAUTY method (as v003's colour parts;
    the plants clipped at the pocket / edge carry concave n-gons that a simple fan would fold)"""
    o = bpy.data.objects[name]; M = np.array(o.matrix_world)
    bm = bmesh.new(); bm.from_mesh(o.data)
    bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method="BEAUTY", ngon_method="BEAUTY"); bm.verts.index_update()
    co = np.array([v.co[:] for v in bm.verts]) @ M[:3, :3].T + M[:3, 3]
    tv = np.array([[v.index for v in f.verts] for f in bm.faces], dtype=np.int64); bm.free()
    return co * K, tv
b = bpy.data.objects["PRINT_site_base"]; Mb = np.array(b.matrix_world)
cb = (np.array([v.co[:] for v in b.data.vertices]) @ Mb[:3, :3].T + Mb[:3, 3]) * K
assert cb.shape == BASE_MM.shape and np.abs(cb - BASE_MM).max() < 1e-4, "v004 base part differs from the v003 site base"

PARTS = [("PRINT_site_base", "1 site base - gray (exact v003)", 3, BASE_MM, BASE_TV),
         ("PRINT_site_base_GREEN", "2 lawn + planting beds + shrubs + tree - green", 4) + blend_tris("PRINT_site_base_GREEN"),
         ("PRINT_site_base_BLACK", "3 asphalt drive + entry plaza + yard copings - black", 2) + blend_tris("PRINT_site_base_BLACK")]
objs = [dict(name="Building II v004 1-240 multicolor site base", transform=T_V003,
             parts=[dict(name=label, co_mm=co, tv=tv, extruder=ext) for _, label, ext, co, tv in PARTS])]
B3.write_bambu_3mf(OUT_3MF, objs, "Building II v004 1-240 multicolor site base",
                   designer="Rea Farms Building II print derivative v004 (1:240, multicolor site base)")
OUT = {"source_blend": os.path.relpath(BLEND, ROOT), "source_sha256": sha(BLEND), "scale": "1:240", "mm_per_m": K,
       "threemf": os.path.relpath(OUT_3MF, ROOT), "sha256": sha(OUT_3MF), "transform": T_V003,
       "transform_equals_v003_site_base": True,
       "parts": [dict(object=n, name=label, filament=ext, triangles=int(len(tv)), vertices=int(len(co))) for n, label, ext, co, tv in PARTS],
       "companions_unchanged": {f: sha(os.path.join(MF, f)) for f in ("building_II_v003_1-240_multicolor_building.3mf",
                                                                       "building_II_v003_1-240_dropoff_canopy.3mf",
                                                                       "building_II_v003_1-240_sunshade.3mf")}}
with open(os.path.join(VAL, "print_export_v004_written.json"), "w", encoding="utf-8") as f:
    json.dump(OUT, f, indent=1)
print(f"[export v004] {OUT['threemf']} {[(p['name'], p['triangles']) for p in OUT['parts']]} in {time.time()-T0:.1f}s")
