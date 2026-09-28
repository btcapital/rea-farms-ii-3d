"""Building II print derivative v001 - STL / 3MF EXPORT at 1:250 in millimetres + printability test coupons.

Run:  blender -b models/Building_II/print_derivatives/building_II_print_v001.blend \
            --python scripts/3d_print/export_print_v001.py
Read-only: the .blend is never saved (test-coupon booleans exist only in memory).

Production parts - geometry written EXACTLY as approved, only scaled x4.0 (1 m real = 4 mm at 1:250):
  exports/Building_II/3d_print/stl/building_II_v001_1-250_<component>.stl  (binary STL, mm, raw model coordinates)
  exports/Building_II/3d_print/3mf/building_II_v001_1-250_<component>.3mf  (3MF core spec, unit="millimeter";
        same vertices/triangles; the <build><item> transform is a pure TRANSLATION that centres the part on a
        340 x 320 bed with its lowest point at Z = 0 - placement only, no rotation, no scaling)
Test coupons - boxes intersected with the approved parts (no thickening or editing), x4.0:
  exports/Building_II/3d_print/stl/test_coupons_v001/building_II_v001_1-250_testcoupon_NN_<name>.stl
  exports/Building_II/3d_print/3mf/building_II_v001_1-250_test_coupons_v001.3mf  (all coupons on one plate,
        each placed by its build-item transform in its recommended print orientation)
"""
import bpy, hashlib, json, math, os, struct, time, zipfile
import numpy as np

T0 = time.time()
BLEND = bpy.data.filepath
ROOT = os.path.abspath(os.path.join(os.path.dirname(BLEND), "..", "..", ".."))
EXP = os.path.join(ROOT, "exports", "Building_II", "3d_print")
STL, MF, VAL = os.path.join(EXP, "stl"), os.path.join(EXP, "3mf"), os.path.join(EXP, "validation")
COUP = os.path.join(STL, "test_coupons_v001")
for d in (STL, MF, VAL, COUP):
    os.makedirs(d, exist_ok=True)
APPROVED_V001 = "c4684e8d8345ff3105599b4ed2dbc67dbb47bc04bef0822bbae2eb8e36242875"
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()
assert sha(BLEND) == APPROVED_V001, "v001 is not the approved prepared derivative"

SCALE = 250
K = 1000.0 / SCALE                     # 4.0 mm per real metre
BED = (340.0, 320.0)
PREFIX = "building_II_v001_1-250_"
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
             f'<metadata name="Title">{title}</metadata>', '<metadata name="Designer">Rea Farms Building II print derivative v001</metadata>',
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

# ------------------------------------------------------------------ production parts
for comp, obname in PARTS.items():
    co, tv, resplit = mesh_arrays(bpy.data.objects[obname])
    co_mm = co * K
    stl = os.path.join(STL, f"{PREFIX}{comp}.stl")
    mf = os.path.join(MF, f"{PREFIX}{comp}.3mf")
    write_stl(stl, co_mm, tv, f"{PREFIX}{comp}")
    write_3mf(mf, [(f"{PREFIX}{comp}", co_mm, tv, placement(co_mm))], f"{PREFIX}{comp}")
    OUT["production"][comp] = dict(source_object=obname, stl=os.path.relpath(stl, ROOT), threemf=os.path.relpath(mf, ROOT),
                                   triangles=int(len(tv)), vertices=int(len(co)), resplit_polygons=resplit,
                                   size_mm=(co_mm.max(0) - co_mm.min(0)).round(3).tolist())
    print(f"[export] {comp}: {len(tv)} tris, {OUT['production'][comp]['size_mm']} mm")

# ------------------------------------------------------------------ test coupons (in memory only)
COUPONS = [
    # id, name, source part, real-metre box (x0,x1,y0,y1,z0,z1), purpose, print orientation (rotate 180 about X?)
    ("01", "facade_storefront_railing", "PRINT_building_body", (46.0, 53.0, -0.5, 2.5, -0.6, 6.2),
     "south facade bay: storefront recess (0.61 mm) with 0.5 mm mullion ribs, parapet, 0.8 mm railing fin", False),
    ("02", "facade_curtainwall_west", "PRINT_building_body", (-0.4, 2.5, 27.0, 31.0, -0.6, 5.5),
     "west CW4 curtain wall: 0.93 mm recess, 0.5 mm curtain-wall ribs (the most exaggerated class)", False),
    ("03", "canopy_bay_column_X1", "PRINT_canopy_dropoff", (23.55, 27.0, 32.4, 39.7, -0.6, 5.7),
     "drop-off canopy bay: 1.2 mm column, 0.8 mm purlins, 0.8 mm glass plate, beams; column foot fits coupon 04", False),
    ("04", "socket_bollards", "PRINT_site_base", (23.5, 27.0, 33.8, 35.6, -1.5, 1.2),
     "site base at canopy column X1: 0.2 mm-clearance socket (receives coupon 03) + two 1.2 mm bollards", False),
    ("05", "light_pole_1", "PRINT_site_base", (0.2, 2.2, 34.0, 36.2, -1.0, 6.0),
     "site base at light pole 1: 1.5 mm pole shaft 21 mm tall + 0.8 mm luminaire head", False),
    ("06", "sunshade_SE_corner", "PRINT_sunshade", (47.5, 56.8, 3.2, 10.5, 9.0, 10.0),
     "sun-shade SE corner: 0.84 mm louver bars (0.27 mm gaps), 0.8 mm frame, hip; printed top face down", True),
    ("07", "pocket_body_corner_SE", "PRINT_building_body", (58.0, 62.8, -0.3, 3.5, -2.6, 0.5),
     "building-body SE corner below grade (foundation + podium); fits into coupon 08 with 0.3 mm clearance", False),
    ("08", "pocket_site_corner_SE", "PRINT_site_base", (57.5, 65.0, -3.5, 4.0, -3.2, 1.0),
     "site base at the SE pocket corner: 0.3 mm-clearance pocket walls + floor (receives coupon 07)", False),
]
def make_box(name, b):
    import bmesh
    from mathutils import Vector
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = Vector((b[0] if v.co.x < 0 else b[1], b[2] if v.co.y < 0 else b[3], b[4] if v.co.z < 0 else b[5]))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    return ob

plate = []
x_cursor, y_cursor, row_h = 8.0, 8.0, 0.0
for cid, name, src, box, purpose, flip in COUPONS:
    s = bpy.data.objects[src]
    tmp = bpy.data.objects.new(f"tmp_{cid}", s.data.copy()); tmp.matrix_world = s.matrix_world
    bpy.context.scene.collection.objects.link(tmp)
    bx = make_box(f"box_{cid}", box)
    m = tmp.modifiers.new("i", "BOOLEAN"); m.operation = "INTERSECT"; m.object = bx; m.solver = "MANIFOLD"
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(tmp.evaluated_get(dg))
    co, tv, _ = triangulate(me)
    co_mm = co * K
    fname = f"{PREFIX}testcoupon_{cid}_{name}"
    stl = os.path.join(COUP, fname + ".stl")
    write_stl(stl, co_mm, tv, fname)
    # plate layout (simple rows on the 340 x 320 bed)
    R = np.diag([1.0, -1.0, -1.0]) if flip else np.eye(3)
    p = co_mm @ R.T; w, d = (p.max(0) - p.min(0))[:2]
    if x_cursor + w > BED[0] - 8:
        x_cursor = 8.0; y_cursor += row_h + 10.0; row_h = 0.0
    T = placement(co_mm, x_cursor + w / 2, y_cursor + d / 2, flip)
    x_cursor += w + 10.0; row_h = max(row_h, d)
    plate.append((fname, co_mm, tv, T))
    OUT["coupons"][cid] = dict(name=name, source_part=src, box_real_m=box, purpose=purpose, print_top_face_down=flip,
                               stl=os.path.relpath(stl, ROOT), triangles=int(len(tv)),
                               size_mm=(co_mm.max(0) - co_mm.min(0)).round(3).tolist())
    for o in (tmp, bx):
        d_ = o.data; bpy.data.objects.remove(o); bpy.data.meshes.remove(d_)
    bpy.data.meshes.remove(me)
    print(f"[export] coupon {cid} {name}: {OUT['coupons'][cid]['size_mm']} mm, {len(tv)} tris")
cmf = os.path.join(MF, f"{PREFIX}test_coupons_v001.3mf")
write_3mf(cmf, plate, f"{PREFIX}test_coupons_v001")
OUT["coupon_plate_3mf"] = os.path.relpath(cmf, ROOT)
with open(os.path.join(VAL, "print_export_v001_written.json"), "w", encoding="utf-8") as f:
    json.dump(OUT, f, indent=1)
print(f"[export] done in {time.time()-T0:.1f}s; blend dirty={bpy.data.is_dirty} (never saved)")
