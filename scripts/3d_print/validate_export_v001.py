"""Building II print v001 - independent validation of the exported STL / 3MF files (read-only).

Run:  blender -b models/Building_II/print_derivatives/building_II_print_v001.blend \
            --python scripts/3d_print/validate_export_v001.py
Reads every exported file back FROM DISK (own STL / 3MF parsers), and compares it with the approved
derivative (opened read-only, never saved). Writes exports/Building_II/3d_print/validation/print_export_v001_validation.json
"""
import bpy, glob, hashlib, json, os, struct, zipfile, time
import xml.etree.ElementTree as ET
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

T0 = time.time()
BLEND = bpy.data.filepath
ROOT = os.path.abspath(os.path.join(os.path.dirname(BLEND), "..", "..", ".."))
EXP = os.path.join(ROOT, "exports", "Building_II", "3d_print")
VAL = os.path.join(EXP, "validation")
K = 4.0
APPROVED = json.load(open(os.path.join(VAL, "print_validation_v001.json")))["parts"]
PARTS = {"building_body": "PRINT_building_body", "site_base": "PRINT_site_base",
         "dropoff_canopy": "PRINT_canopy_dropoff", "sunshade": "PRINT_sunshade"}
NS = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

def read_stl(p):
    b = open(p, "rb").read()
    n = struct.unpack("<I", b[80:84])[0]
    assert len(b) == 84 + 50 * n, "binary STL size mismatch"
    rec = np.frombuffer(b[84:], dtype=[("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")], count=n)
    tri = rec["v"].astype(np.float64)
    V, inv = np.unique(tri.reshape(-1, 3), axis=0, return_inverse=True)
    return dict(header=b[:80].decode("ascii", "replace").strip(), co=V, tv=inv.reshape(-1, 3),
                stored_normals=rec["n"].astype(np.float64), raw=tri)

def read_3mf(p):
    z = zipfile.ZipFile(p)
    names = z.namelist()
    root = ET.fromstring(z.read("3D/3dmodel.model"))
    objs = []
    for o in root.findall("m:resources/m:object", NS):
        vs = o.findall("m:mesh/m:vertices/m:vertex", NS); ts = o.findall("m:mesh/m:triangles/m:triangle", NS)
        co = np.array([[float(v.get("x")), float(v.get("y")), float(v.get("z"))] for v in vs])
        tv = np.array([[int(t.get("v1")), int(t.get("v2")), int(t.get("v3"))] for t in ts], dtype=np.int64)
        objs.append(dict(id=o.get("id"), name=o.get("name"), co=co, tv=tv))
    items = [dict(objectid=i.get("objectid"), T=[float(x) for x in i.get("transform").split()])
             for i in root.findall("m:build/m:item", NS)]
    return dict(unit=root.get("unit"), files=names, objects=objs, items=items)

def mesh_checks(co, tv):
    e = np.concatenate([tv[:, [0, 1]], tv[:, [1, 2]], tv[:, [2, 0]]])
    und = np.sort(e, axis=1)
    _, cnt = np.unique(und, axis=0, return_counts=True)
    _, dcnt = np.unique(e, axis=0, return_counts=True)
    p0, p1, p2 = co[tv[:, 0]], co[tv[:, 1]], co[tv[:, 2]]
    cr = np.cross(p1 - p0, p2 - p0); area = 0.5 * np.linalg.norm(cr, axis=1)
    vol = float(np.einsum("ij,ij->i", p0, np.cross(p1, p2)).sum() / 6.0)
    lab = np.arange(len(co)); a, b = und[:, 0], und[:, 1]
    while True:
        old = lab.copy(); m = np.minimum(lab[a], lab[b]); np.minimum.at(lab, a, m); np.minimum.at(lab, b, m); lab = lab[lab]
        if np.array_equal(lab, old):
            break
    used = np.unique(tv)
    return dict(triangles=int(len(tv)), vertices=int(len(used)), open_edges=int((cnt == 1).sum()),
                nonmanifold_edges=int((cnt > 2).sum()), duplicate_directed_edges=int((dcnt > 1).sum()),
                volume_mm3=round(vol, 3), outward_normals=vol > 0, components=int(len(np.unique(lab[used]))),
                degenerate_triangles=int((area < 1e-9).sum()),
                size_mm=(co[used].max(0) - co[used].min(0)).round(3).tolist(),
                min_mm=co[used].min(0).round(3).tolist(), max_mm=co[used].max(0).round(3).tolist(),
                watertight=bool((cnt == 1).sum() == 0 and (cnt > 2).sum() == 0 and (dcnt > 1).sum() == 0 and vol > 0))

def source(obname):
    """Approved mesh (x4.0) with Blender's default triangulation and its polygons."""
    ob = bpy.data.objects[obname]; me = ob.data; me.calc_loop_triangles()
    co = np.array([v.co for v in me.vertices]).reshape(-1, 3) * K
    tv = np.array([t.vertices[:] for t in me.loop_triangles], dtype=np.int64).reshape(-1, 3)
    tp = np.array([t.polygon_index for t in me.loop_triangles], dtype=np.int64)
    polys = [tuple(p.vertices) for p in me.polygons]
    return co, tv, tp, polys

def triangulation_audit(tv_exp, src_co, src_tv, src_tp, polys, claimed_resplit):
    """Exported triangles must equal Blender's default triangles of the approved mesh, except on the polygons the
    exporter declares as re-split; re-split triangles must lie inside those polygons (n-2 each). Reports how far
    the re-split polygons are from planar - the only place the printed surface can differ from the approved one."""
    from collections import Counter
    exp = Counter(tuple(sorted(t)) for t in tv_exp)
    dflt = Counter(tuple(sorted(t)) for t in src_tv)
    dpoly = {}
    for t, p in zip(src_tv, src_tp):
        dpoly.setdefault(tuple(sorted(t)), set()).add(int(p))
    removed = dflt - exp; added = exp - dflt
    rs = set(claimed_resplit)
    removed_outside = sum(n for t, n in removed.items() if not (dpoly[t] & rs))
    added_outside, per = 0, Counter()
    for t, n in added.items():
        owners = [i for i in rs if set(t) <= set(polys[i])]
        if len(owners) < 1:
            added_outside += n
        else:
            per[owners[0]] += n
    counts_ok = (sum(added.values()) == sum(removed.values()) <= sum(len(polys[i]) - 2 for i in rs))   # replaced 1-for-1 inside the re-split polygons (unchanged diagonals are not counted)
    dev = 0.0
    for i in rs:
        P = src_co[list(polys[i])]; c = P.mean(0)
        dev = max(dev, float(np.abs((P - c) @ np.linalg.svd(P - c)[2][-1]).max()))
    return dict(triangles_equal_to_default_outside_resplit=bool(removed_outside == 0 and added_outside == 0),
                resplit_polygons=len(rs), resplit_triangle_counts_ok=bool(counts_ok),
                triangles_changed=int(sum(added.values())), default_triangles_replaced=int(sum(removed.values())),
                triangles_in_resplit_polygons=int(sum(len(polys[i]) - 2 for i in rs)), total_triangles=int(len(tv_exp)),
                max_nonplanarity_of_resplit_polygons_mm=round(dev, 4))

def tri_area(co, tv):
    return float(0.5 * np.linalg.norm(np.cross(co[tv[:, 1]] - co[tv[:, 0]], co[tv[:, 2]] - co[tv[:, 0]]), axis=1).sum())

def thickness_peaks(co, tv, off=1e-3):
    """Ray-cast wall thickness (mm) from every triangle; returns a histogram of the thin end."""
    bvh = BVHTree.FromPolygons([tuple(v) for v in co], [tuple(t) for t in tv], epsilon=0.0)
    p0, p1, p2 = co[tv[:, 0]], co[tv[:, 1]], co[tv[:, 2]]
    cr = np.cross(p1 - p0, p2 - p0); ar = np.linalg.norm(cr, axis=1); n = cr / np.maximum(ar, 1e-30)[:, None]
    cen = (p0 + p1 + p2) / 3
    th = []
    for i in range(len(tv)):
        if ar[i] < 1e-6:
            continue
        h = bvh.ray_cast(Vector(cen[i] - n[i] * off), Vector(-n[i]), 1000.0)
        if h[0] is not None:
            th.append(round(h[3] + off, 2))
    th = np.array(th)
    vals, cnts = np.unique(th[th < 1.6], return_counts=True)
    return {f"{v:.2f}": int(c) for v, c in zip(vals, cnts) if c >= 2}

R = {"checked": time.strftime("%Y-%m-%d %H:%M"), "unit_rule": "STL carries no unit field: values are millimetres (x4.0 of real metres); 3MF declares unit=\"millimeter\"",
     "production": {}, "coupons": {}, "files": {}}
# ------------------------------------------------------------------ production files
written_prod = json.load(open(os.path.join(VAL, "print_export_v001_written.json")))["production"]
for comp, obname in PARTS.items():
    src_co, src_tv, src_tp, polys = source(obname)
    ap = APPROVED[obname]["printed_size_mm"]
    stl_p = os.path.join(EXP, "stl", f"building_II_v001_1-250_{comp}.stl")
    mf_p = os.path.join(EXP, "3mf", f"building_II_v001_1-250_{comp}.3mf")
    s = read_stl(stl_p); cs = mesh_checks(s["co"], s["tv"])
    m = read_3mf(mf_p); o = m["objects"][0]
    # STL triangles == 3MF triangles, and 3MF vertices == approved vertices x4
    exact = bool(s["raw"].shape == o["co"][o["tv"]].shape and np.abs(s["raw"] - o["co"][o["tv"]]).max() < 1e-4
                 and o["co"].shape == src_co.shape and np.abs(o["co"] - src_co).max() < 1e-5)
    cn = np.cross(s["raw"][:, 1] - s["raw"][:, 0], s["raw"][:, 2] - s["raw"][:, 0]); ln = np.linalg.norm(cn, axis=1)
    ok = ln > 1e-9
    ndot = np.einsum("ij,ij->i", cn[ok] / ln[ok, None], s["stored_normals"][ok])
    cs.update(stored_normals_agree=bool((ndot > 0.999).all()), identical_to_approved_mesh_x4=bool(exact),
              size_matches_approved=bool(np.allclose(cs["size_mm"], ap, atol=0.06)), approved_size_mm=ap, header=s["header"])
    cm = mesh_checks(o["co"], o["tv"])
    T = np.array(m["items"][0]["T"]); rot = T[:9].reshape(3, 3)
    placed = o["co"] @ rot + T[9:]
    cm.update(unit=m["unit"], objects=len(m["objects"]), build_items=len(m["items"]),
              item_transform_is_pure_translation=bool(np.allclose(rot, np.eye(3))),
              placed_min_z_mm=round(float(placed[:, 2].min()), 4),
              placed_within_bed=bool(placed[:, 0].min() >= 0 and placed[:, 0].max() <= 340 and placed[:, 1].min() >= 0 and placed[:, 1].max() <= 320),
              vertices_match_approved_x4=bool(o["co"].shape == src_co.shape and np.abs(o["co"] - src_co).max() < 1e-5),
              triangulation=triangulation_audit(o["tv"], src_co, src_tv, src_tp, polys,
                                                written_prod[comp]["resplit_polygons"]),
              size_matches_approved=bool(np.allclose(cm["size_mm"], ap, atol=0.06)))
    R["production"][comp] = dict(stl=cs, threemf=cm)
    for p in (stl_p, mf_p):
        R["files"][os.path.relpath(p, ROOT)] = dict(sha256=sha(p), bytes=os.path.getsize(p))
    print(f"[validate-export] {comp}: stl watertight {cs['watertight']} exact {exact}; 3mf unit {m['unit']} ok {cm['vertices_match_approved_x4']}")

# ------------------------------------------------------------------ coupons
written = json.load(open(os.path.join(VAL, "print_export_v001_written.json")))
coup = {}
for cid, info in written["coupons"].items():
    p = os.path.join(ROOT, info["stl"]); s = read_stl(p); c = mesh_checks(s["co"], s["tv"])
    c["thin_thickness_histogram_mm"] = thickness_peaks(s["co"], s["tv"])
    c.update(name=info["name"], purpose=info["purpose"], print_top_face_down=info["print_top_face_down"])
    coup[cid] = (s, c); R["coupons"][cid] = c
    R["files"][info["stl"]] = dict(sha256=sha(p), bytes=os.path.getsize(p))
mf_p = os.path.join(ROOT, written["coupon_plate_3mf"]); m = read_3mf(mf_p)
plate = []
for o, it in zip(m["objects"], m["items"]):
    T = np.array(it["T"]); placed = o["co"] @ T[:9].reshape(3, 3) + T[9:]
    plate.append(dict(name=o["name"], min=placed.min(0).round(2).tolist(), max=placed.max(0).round(2).tolist(),
                      watertight=mesh_checks(o["co"], o["tv"])["watertight"]))
R["coupon_plate_3mf"] = dict(file=written["coupon_plate_3mf"], unit=m["unit"], objects=len(m["objects"]), items=plate,
                             all_on_bed=all(q["min"][0] >= 0 and q["max"][0] <= 340 and q["min"][1] >= 0 and q["max"][1] <= 320
                                            and abs(q["min"][2]) < 1e-3 for q in plate))
R["files"][written["coupon_plate_3mf"]] = dict(sha256=sha(mf_p), bytes=os.path.getsize(mf_p))

def min_gap(a_raw, b, zmin, zmax):
    """smallest distance from coupon-A surface samples (zmin<z<zmax, mm) to coupon-B surface"""
    bvh = BVHTree.FromPolygons([tuple(v) for v in b["co"]], [tuple(t) for t in b["tv"]], epsilon=0.0)
    rng = np.random.default_rng(1); best = 1e9
    for t in a_raw:
        u = rng.random((60, 2)); mm = u.sum(1) > 1; u[mm] = 1 - u[mm]
        pts = t[0] + u[:, :1] * (t[1] - t[0]) + u[:, 1:] * (t[2] - t[0])
        for q in pts[(pts[:, 2] > zmin) & (pts[:, 2] < zmax)]:
            h = bvh.find_nearest(Vector(q), 3.0)
            if h[0] is not None:
                best = min(best, h[3])
    return round(best, 4)
R["fit_pairs"] = {
    "03 canopy column in 04 socket (side walls)": min_gap(coup["03"][0]["raw"], coup["04"][0], -1.2, 0.0),
    "07 body corner in 08 pocket (side walls)": min_gap(coup["07"][0]["raw"], coup["08"][0], -8.5, 0.0),
    "design_clearance_mm": {"socket": 0.2, "pocket": 0.3},
}
v023 = os.path.join(ROOT, "models", "Building_II", "building_shell_v023.blend")
R["v023_sha256"] = sha(v023); R["v001_sha256"] = sha(BLEND)
R["runtime_s"] = round(time.time() - T0, 1)
json.dump(R, open(os.path.join(VAL, "print_export_v001_validation.json"), "w", encoding="utf-8"), indent=1)
print(f"[validate-export] done in {R['runtime_s']}s; fit {R['fit_pairs']}")
