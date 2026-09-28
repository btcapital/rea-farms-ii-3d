"""Building II print derivative v002 - 3MF EXPORT at 1:240 in millimetres (read-only; the .blend is never saved).

Run:  blender -b models/Building_II/print_derivatives/building_II_print_v002.blend \
            --python scripts/3d_print/export_print_v002.py
Writes exports/Building_II/3d_print/3mf/building_II_v002_1-240_<component>.3mf (3MF core spec, unit="millimeter").
Mesh = approved v002 geometry x 4.1667 (1 m real = 4.1667 mm at 1:240), same triangulation rule as v001
(Blender default triangles, only self-folding polygons re-split). The <build><item> transform is RIGID ONLY and
places each part in its recommended print orientation, centred on the 340 x 320 bed with its lowest point at Z = 0:
  building body, site base : upright (translation only)
  drop-off canopy          : standing on its south edge (rotation +90 deg about X, real +Y up) - see PRINT_EXPORT.md
  sun-shade                : top face down (rotation 180 deg about X)
v001 exports are not touched.
"""
import bpy, hashlib, json, math, os, struct, time, zipfile
import numpy as np

T0 = time.time()
BLEND = bpy.data.filepath
ROOT = os.path.abspath(os.path.join(os.path.dirname(BLEND), "..", "..", ".."))
EXP = os.path.join(ROOT, "exports", "Building_II", "3d_print")
STL, MF, VAL = os.path.join(EXP, "stl"), os.path.join(EXP, "3mf"), os.path.join(EXP, "validation")
for d in (MF, VAL):
    os.makedirs(d, exist_ok=True)
APPROVED_V002 = "9aa5e3a4574e758f7fc914d9e6df887482791585a673d8b542420e7f4369a27c"
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()
assert sha(BLEND) == APPROVED_V002, "v002 is not the validated prepared derivative"

SCALE = 240
K = 1000.0 / SCALE                     # 4.1667 mm per real metre
BED = (340.0, 320.0)
PREFIX = "building_II_v002_1-240_"
PARTS = {"building_body": "PRINT_building_body", "site_base": "PRINT_site_base",
         "dropoff_canopy": "PRINT_canopy_dropoff", "sunshade": "PRINT_sunshade"}

import bmesh
def _bad_edge_polys(tv, tp):
    e = np.concatenate([tv[:, [0, 1]], tv[:, [1, 2]], tv[:, [2, 0]]]); ep = np.concatenate([tp, tp, tp])
    und = np.sort(e, axis=1)
    u, inv, cnt = np.unique(und, axis=0, return_inverse=True, return_counts=True); inv = inv.ravel()
    d, dinv, dcnt = np.unique(e, axis=0, return_inverse=True, return_counts=True); dinv = dinv.ravel()
    bad = (cnt[inv] != 2) | (dcnt[dinv] > 1)
    return set(np.unique(ep[bad]).tolist())

def triangulate(me, M=None):
    """Triangles for export. Vertices are kept exactly (same order). Every polygon keeps Blender's own default
    triangulation (the one used for the approved validation and previews) EXCEPT polygons whose default split
    folds onto itself (non-manifold / duplicated diagonals) - only those are re-split with the BEAUTY method.
    Returns co, tv, and the list of re-split polygon indices."""
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

def mesh_arrays(ob):
    return triangulate(ob.data, ob.matrix_world)   # co, tv, resplit

def write_stl(path, co_mm, tv, name):
    co32 = co_mm.astype(np.float32)
    p0, p1, p2 = co32[tv[:, 0]], co32[tv[:, 1]], co32[tv[:, 2]]
    n = np.cross(p1.astype(np.float64) - p0.astype(np.float64), p2.astype(np.float64) - p0.astype(np.float64))
    ln = np.linalg.norm(n, axis=1); n = np.where(ln[:, None] > 0, n / np.maximum(ln, 1e-30)[:, None], 0.0)
    rec = np.zeros(len(tv), dtype=[("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
    rec["n"] = n; rec["v"][:, 0] = p0; rec["v"][:, 1] = p1; rec["v"][:, 2] = p2
    header = f"{name} | Building II print v001 | 1:250 | units mm".encode("ascii")[:80].ljust(80, b" ")
    with open(path, "wb") as f:
        f.write(header); f.write(struct.pack("<I", len(tv))); f.write(rec.tobytes())

def write_3mf(path, objects, title):
    """objects: list of (name, co_mm, tv, transform 3x4 as 12 floats)."""
    ct = ('<?xml version="1.0" encoding="UTF-8"?>\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    parts = ['<?xml version="1.0" encoding="UTF-8"?>\n<model unit="millimeter" xml:lang="en-US" '
             'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">',
             f'<metadata name="Title">{title}</metadata>', '<metadata name="Designer">Rea Farms Building II print derivative v002 (1:240)</metadata>',
             '<resources>']
    for i, (name, co, tv, _) in enumerate(objects, 1):
        parts.append(f'<object id="{i}" type="model" name="{name}"><mesh><vertices>')
        parts.append("".join(f'<vertex x="{x:.6f}" y="{y:.6f}" z="{z:.6f}"/>' for x, y, z in co))
        parts.append("</vertices><triangles>")
        parts.append("".join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in tv))
        parts.append("</triangles></mesh></object>")
    parts.append("</resources><build>")
    for i, (_, _, _, T) in enumerate(objects, 1):
        parts.append(f'<item objectid="{i}" transform="{" ".join(f"{t:.6f}" for t in T)}"/>')
    parts.append("</build></model>")
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct); z.writestr("_rels/.rels", rels); z.writestr("3D/3dmodel.model", "".join(parts))

def placement(co_mm, cx=BED[0] / 2, cy=BED[1] / 2, rot_x180=False):
    """3MF 3x4 transform (row-major m00 m01 m02 m10 m11 m12 m20 m21 m22 tx ty tz), rigid only."""
    R = np.diag([1.0, -1.0, -1.0]) if rot_x180 else np.eye(3)
    p = co_mm @ R.T
    lo, hi = p.min(0), p.max(0)
    t = np.array([cx - (lo[0] + hi[0]) / 2, cy - (lo[1] + hi[1]) / 2, -lo[2]])
    # 3MF applies v' = v * M (row vector); rows 0-2 = R^T, row 3 = t
    Mt = R.T
    return [Mt[0, 0], Mt[0, 1], Mt[0, 2], Mt[1, 0], Mt[1, 1], Mt[1, 2], Mt[2, 0], Mt[2, 1], Mt[2, 2], t[0], t[1], t[2]]

OUT = {"production": {}, "coupons": {}, "units": "millimetre", "scale_factor_mm_per_m": K}

ROT = {"building_body": np.eye(3), "site_base": np.eye(3),
       "dropoff_canopy": np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]], float),   # +90 deg about X: print Z = real Y
       "sunshade": np.diag([1.0, -1.0, -1.0])}                                   # 180 deg about X: top face down
ORIENT_TXT = {"building_body": "upright", "site_base": "upright",
              "dropoff_canopy": "standing on its south edge (rotated +90 deg about X)", "sunshade": "top face down (rotated 180 deg about X)"}

def placement_R(co_mm, R, cx=BED[0] / 2, cy=BED[1] / 2):
    """3MF 3x4 transform (m00 m01 m02 m10 m11 m12 m20 m21 m22 tx ty tz), rigid only; 3MF applies v' = v * M."""
    p = co_mm @ R.T
    lo, hi = p.min(0), p.max(0)
    t = np.array([cx - (lo[0] + hi[0]) / 2, cy - (lo[1] + hi[1]) / 2, -lo[2]])
    Mt = R.T
    return [Mt[0, 0], Mt[0, 1], Mt[0, 2], Mt[1, 0], Mt[1, 1], Mt[1, 2], Mt[2, 0], Mt[2, 1], Mt[2, 2], t[0], t[1], t[2]]

OUT = {"production": {}, "units": "millimetre", "scale": "1:240", "scale_factor_mm_per_m": K, "source_v002_sha256": APPROVED_V002}
for comp, obname in PARTS.items():
    co, tv, resplit = mesh_arrays(bpy.data.objects[obname])
    co_mm = co * K
    mf = os.path.join(MF, f"{PREFIX}{comp}.3mf")
    assert not os.path.exists(mf) or "v002" in mf
    write_3mf(mf, [(f"{PREFIX}{comp}", co_mm, tv, placement_R(co_mm, ROT[comp]))], f"{PREFIX}{comp}")
    p = co_mm @ ROT[comp].T
    OUT["production"][comp] = dict(source_object=obname, threemf=os.path.relpath(mf, ROOT), triangles=int(len(tv)),
                                   vertices=int(len(co)), resplit_polygons=resplit, print_orientation=ORIENT_TXT[comp],
                                   size_mm=(co_mm.max(0) - co_mm.min(0)).round(3).tolist(),
                                   size_on_bed_mm=(p.max(0) - p.min(0)).round(3).tolist())
    print(f"[export] {comp}: {len(tv)} tris, model {OUT['production'][comp]['size_mm']} mm, on bed {OUT['production'][comp]['size_on_bed_mm']} mm")
with open(os.path.join(VAL, "print_export_v002_written.json"), "w", encoding="utf-8") as f:
    json.dump(OUT, f, indent=1)
print(f"[export] done in {time.time()-T0:.1f}s; blend dirty={bpy.data.is_dirty} (never saved)")
