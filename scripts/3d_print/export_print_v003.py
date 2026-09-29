"""Building II print derivative v003 (MULTICOLOR) - 3MF EXPORT at 1:240 in millimetres (read-only; the .blend is never saved).

Run:  blender -b models/Building_II/print_derivatives/building_II_print_v003.blend \
            --python scripts/3d_print/export_print_v003.py
Writes exports/Building_II/3d_print/3mf/building_II_v003_1-240_<component>.3mf - Bambu Studio multi-part objects
(generic 3MF + Metadata/model_settings.config with a filament per part):
  multicolor_building : ONE object, 5 parts in priority order (a later part wins where parts overlap in Bambu Studio)
                        1 body (exact v002 geometry) -> filament 3 Gray
                        2 white paneling / roofs     -> filament 1 White
                        3 black paneling / copings   -> filament 2 Black
                        4 glazing / glass rails      -> filament 4 Clear
                        5 storefront / CW frames     -> filament 3 Gray
  dropoff_canopy      : ONE object, 2 parts: canopy (exact v002, filament 3 Gray) + canopy glass (filament 4 Clear)
  sunshade            : exact v002, filament 1 White
  site_base           : exact v002, filament 3 Gray
Triangulation rule = v002 (Blender default triangles; only self-folding polygons re-split BEAUTY), so the four v002 parts
are written with exactly the triangles that were printed. Placement = v002 (rigid item transform, centred on the
340 x 320 bed, lowest point at Z = 0): building / site upright, canopy on its south edge (+90 deg X), sun-shade top down.
"""
import bpy, bmesh, hashlib, json, os, sys, time
import numpy as np

T0 = time.time()
BLEND = bpy.data.filepath
ROOT = os.path.abspath(os.path.join(os.path.dirname(BLEND), "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts", "3d_print"))
import bambu_3mf_v003 as B3
EXP = os.path.join(ROOT, "exports", "Building_II", "3d_print")
MF, VAL = os.path.join(EXP, "3mf"), os.path.join(EXP, "validation")
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()
BLEND_SHA = sha(BLEND)
K = 1000.0 / 240.0
BED = (340.0, 320.0)
PREFIX = "building_II_v003_1-240_"

def _bad_edge_polys(tv, tp):
    e = np.concatenate([tv[:, [0, 1]], tv[:, [1, 2]], tv[:, [2, 0]]]); ep = np.concatenate([tp, tp, tp])
    und = np.sort(e, axis=1)
    u, inv, cnt = np.unique(und, axis=0, return_inverse=True, return_counts=True); inv = inv.ravel()
    d, dinv, dcnt = np.unique(e, axis=0, return_inverse=True, return_counts=True); dinv = dinv.ravel()
    bad = (cnt[inv] != 2) | (dcnt[dinv] > 1)
    return set(np.unique(ep[bad]).tolist())

def triangulate(me, M=None):
    """identical to export_print_v002.triangulate (the rule the printed v002 files were written with)"""
    me.calc_loop_triangles()
    tv = np.empty(len(me.loop_triangles) * 3, dtype=np.int64); me.loop_triangles.foreach_get("vertices", tv); tv = tv.reshape(-1, 3)
    tp = np.empty(len(me.loop_triangles), dtype=np.int64); me.loop_triangles.foreach_get("polygon_index", tp)
    co = np.empty(len(me.vertices) * 3); me.vertices.foreach_get("co", co); co = co.reshape(-1, 3)
    resplit = set()
    for _ in range(6):
        bad = _bad_edge_polys(tv, tp)
        if not bad:
            break
        resplit |= bad
        bm = bmesh.new(); bm.from_mesh(me); bm.faces.ensure_lookup_table()
        res = bmesh.ops.triangulate(bm, faces=[bm.faces[i] for i in sorted(resplit)], quad_method="BEAUTY", ngon_method="BEAUTY")
        bm.verts.index_update()
        pverts = {i: set(me.polygons[i].vertices) for i in resplit}
        new_t, new_p = [], []
        for f in res["faces"]:
            vi = [v.index for v in f.verts]
            owner = [i for i in resplit if set(vi) <= pverts[i]]
            new_t.append(vi); new_p.append(owner[0])
        bm.free()
        keep = ~np.isin(tp, sorted(resplit))
        tv = np.vstack([tv[keep], np.array(new_t, dtype=np.int64)]); tp = np.concatenate([tp[keep], np.array(new_p, dtype=np.int64)])
    assert not _bad_edge_polys(tv, tp), "triangulation still not manifold"
    if M is not None:
        M = np.array(M); co = co @ M[:3, :3].T + M[:3, 3]
    order = np.argsort(tp, kind="stable")
    return co, tv[order], sorted(resplit)

def triangulate_beauty(me, M=None):
    """new v003 colour parts: every polygon split with the BEAUTY method (non-folding)"""
    bm = bmesh.new(); bm.from_mesh(me)
    bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method="BEAUTY", ngon_method="BEAUTY")
    bm.verts.index_update()
    co = np.array([v.co[:] for v in bm.verts]); tv = np.array([[v.index for v in f.verts] for f in bm.faces], dtype=np.int64); bm.free()
    bad = _bad_edge_polys(tv, np.arange(len(tv)))
    if bad:
        raise AssertionError(f"{me.name}: {len(bad)} triangles on non-manifold edges after BEAUTY triangulation")
    if M is not None:
        M = np.array(M); co = co @ M[:3, :3].T + M[:3, 3]
    return co, tv, []
V002_PARTS = {"PRINT_building_body": "building_body", "PRINT_canopy_dropoff": "dropoff_canopy", "PRINT_sunshade": "sunshade",
              "PRINT_site_base": "site_base"}
import zipfile, xml.etree.ElementTree as ET
def v002_mesh(comp):
    """the EXACT printed v002 mesh (vertices + triangles) from building_II_v002_1-240_<comp>.3mf, back in real metres.
    Re-triangulating the v002 part in Blender can pick other diagonals on its non-planar n-gons (the loop start vertex
    of some site-base polygons differs after reload), so the base parts are taken from the printed files verbatim."""
    ns = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
    root = ET.fromstring(zipfile.ZipFile(os.path.join(MF, f"building_II_v002_1-240_{comp}.3mf")).read("3D/3dmodel.model"))
    o = root.find("m:resources/m:object", ns)
    co = np.array([[float(v.get("x")), float(v.get("y")), float(v.get("z"))] for v in o.findall("m:mesh/m:vertices/m:vertex", ns)])
    tv = np.array([[int(t.get("v1")), int(t.get("v2")), int(t.get("v3"))] for t in o.findall("m:mesh/m:triangles/m:triangle", ns)], dtype=np.int64)
    return co / K, tv, []
def tri_for(obn):
    if obn in V002_PARTS:
        co, tv, rs = v002_mesh(V002_PARTS[obn])
        o = bpy.data.objects[obn]; me = o.data; M = np.array(o.matrix_world)
        cb = np.array([v.co[:] for v in me.vertices]) @ M[:3, :3].T + M[:3, 3]
        assert cb.shape == co.shape and np.abs(cb - co).max() < 1e-5, f"{obn}: v003 part differs from the printed v002 mesh"
        return co, tv, rs
    o = bpy.data.objects[obn]
    return triangulate_beauty(o.data, o.matrix_world)

ROT = {"multicolor_building": np.eye(3), "site_base": np.eye(3),
       "dropoff_canopy": np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]], float),     # +90 deg about X: print Z = real Y
       "sunshade": np.diag([1.0, -1.0, -1.0])}                                     # 180 deg about X: top face down
ORIENT_TXT = {"multicolor_building": "upright", "site_base": "upright",
              "dropoff_canopy": "standing on its south edge (rotated +90 deg about X)", "sunshade": "top face down (rotated 180 deg about X)"}
def placement_R(co_mm, R, cx=BED[0] / 2, cy=BED[1] / 2):
    p = co_mm @ R.T
    lo, hi = p.min(0), p.max(0)
    t = np.array([cx - (lo[0] + hi[0]) / 2, cy - (lo[1] + hi[1]) / 2, -lo[2]])
    Mt = R.T
    return [Mt[0, 0], Mt[0, 1], Mt[0, 2], Mt[1, 0], Mt[1, 1], Mt[1, 2], Mt[2, 0], Mt[2, 1], Mt[2, 2], t[0], t[1], t[2]]

FILES = {
    "multicolor_building": ("Building II v003 1-240 multicolor", [
        ("PRINT_building_body", "1 body - gray brick (exact v002)", 3),
        ("PRINT_building_body_WHITE", "2 white metal paneling + white roofs", 1),
        ("PRINT_building_body_BLACK", "3 black metal paneling + black copings", 2),
        ("PRINT_building_body_CLEAR", "4 glazing + glass rails - clear", 4),
        ("PRINT_building_body_FRAMES", "5 storefront + curtain-wall frames - gray", 3)]),
    "dropoff_canopy": ("Building II v003 1-240 drop-off canopy", [
        ("PRINT_canopy_dropoff", "1 canopy steel - gray (exact v002)", 3),
        ("PRINT_canopy_dropoff_CLEAR", "2 canopy glass - clear", 4)]),
    "sunshade": ("Building II v003 1-240 sun-shade", [("PRINT_sunshade", "sun-shade - white (exact v002)", 1)]),
    "site_base": ("Building II v003 1-240 site base", [("PRINT_site_base", "site base - gray (exact v002)", 3)]),
}
OUT = {"source_blend": os.path.relpath(BLEND, ROOT), "source_sha256": BLEND_SHA, "scale": "1:240", "mm_per_m": K, "files": {}}
for comp, (title, parts) in FILES.items():
    arrs = [(obn, label, ext) + tri_for(obn) for obn, label, ext in parts]
    base_mm = arrs[0][3] * K
    T = placement_R(base_mm, ROT[comp])
    objs = [dict(name=title, transform=T,
                 parts=[dict(name=label, co_mm=co * K, tv=tv, extruder=ext) for obn, label, ext, co, tv, rs in arrs])]
    path = os.path.join(MF, f"{PREFIX}{comp}.3mf")
    B3.write_bambu_3mf(path, objs, title, designer="Rea Farms Building II print derivative v003 (1:240, multicolor)")
    p = base_mm @ ROT[comp].T
    OUT["files"][comp] = dict(threemf=os.path.relpath(path, ROOT), sha256=sha(path), print_orientation=ORIENT_TXT[comp],
                              transform=[round(float(x), 6) for x in T], size_on_bed_mm=(p.max(0) - p.min(0)).round(3).tolist(),
                              parts=[dict(object=obn, name=label, filament=ext, triangles=int(len(tv)), vertices=int(len(co)),
                                          resplit_polygons=len(rs)) for obn, label, ext, co, tv, rs in arrs])
    print(f"[export] {comp}: {[(a[0], len(a[4])) for a in arrs]} on bed {OUT['files'][comp]['size_on_bed_mm']} mm")
with open(os.path.join(VAL, "print_export_v003_written.json"), "w", encoding="utf-8") as f:
    json.dump(OUT, f, indent=1)
print(f"[export] done in {time.time()-T0:.1f}s; blend dirty={bpy.data.is_dirty} (never saved)")
