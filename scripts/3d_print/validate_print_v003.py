"""Building II print derivative v003 (multicolour) - validation. READ-ONLY: never saves any .blend.

Run:  blender -b models/Building_II/print_derivatives/building_II_print_v003.blend --python scripts/3d_print/validate_print_v003.py
Writes exports/Building_II/3d_print/validation/print_validation_v003.json (+ _colour_mismatches.csv)

Checks
 1. frozen files: v023 / v001 / v002 blend hashes + every entry of manifests/3d_print/print_phase_v002.sha256
 2. the four v002 parts in v003 are vertex-identical to v002 (v002 objects linked read-only)
 3. scale 1:240, printed sizes, H2S fit (unchanged from v002)
 4. every part watertight with outward normals; colour parts have 0 non-planar faces
 5. colour parts lie inside their base part (vertices + BEAUTY face centroids)
 6. colour correctness: area-weighted surface samples of the body; EFFECTIVE colour (priority: frames > clear > black >
    white > body) vs the EXPECTED colour from the v023 source finish at that point (v023 linked read-only)
 7. per-colour printed thickness (inward ray) and small-island report
"""
import bpy, bmesh, hashlib, json, os, csv, time
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

T0 = time.time()
BLEND = bpy.data.filepath
ROOT = os.path.abspath(os.path.join(os.path.dirname(BLEND), "..", "..", ".."))
VAL = os.path.join(ROOT, "exports", "Building_II", "3d_print", "validation")
V023 = os.path.join(ROOT, "models", "Building_II", "building_shell_v023.blend")
V001 = os.path.join(ROOT, "models", "Building_II", "print_derivatives", "building_II_print_v001.blend")
V002 = os.path.join(ROOT, "models", "Building_II", "print_derivatives", "building_II_print_v002.blend")
SCALE = 240.0; MM = 1000.0 / SCALE
H2S = (340.0, 320.0, 340.0)
REP = {}

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

# ---------------------------------------------------------------- 1 frozen files
EXPECT = {"v023": (V023, "7fe33f1e4dc906c75b54122203fec75ee9ef948be70897e46fcfd1b288235c91"),
          "print_v001": (V001, "c4684e8d8345ff3105599b4ed2dbc67dbb47bc04bef0822bbae2eb8e36242875"),
          "print_v002": (V002, "9aa5e3a4574e758f7fc914d9e6df887482791585a673d8b542420e7f4369a27c")}
frozen = {k: dict(path=os.path.relpath(p, ROOT), sha256=sha(p), expected=e) for k, (p, e) in EXPECT.items()}
for v in frozen.values():
    v["ok"] = v["sha256"] == v["expected"]
man = os.path.join(ROOT, "manifests", "3d_print", "print_phase_v002.sha256")
mres = []
for line in open(man, encoding="utf-8"):
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    h, p = line.split(None, 1); p = p.lstrip("*").strip()
    fp = os.path.join(ROOT, p)
    mres.append(dict(path=p, ok=os.path.exists(fp) and sha(fp) == h))
REP["frozen_files"] = frozen
frozen_m = [m for m in mres if not m["path"].startswith("notes/")]            # notes are living documents (updated per phase)
REP["v002_manifest_entries"] = dict(count=len(mres), frozen_entries=len(frozen_m), all_ok=all(m["ok"] for m in frozen_m),
                                    failures=[m["path"] for m in frozen_m if not m["ok"]],
                                    living_notes_changed=[m["path"] for m in mres if m["path"].startswith("notes/") and not m["ok"]])

# ---------------------------------------------------------------- helpers
def getco(o):
    a = np.empty(len(o.data.vertices) * 3); o.data.vertices.foreach_get("co", a); co = a.reshape(-1, 3)
    M = np.array(o.matrix_world); return co @ M[:3, :3].T + M[:3, 3]
def metrics(o):
    me = o.data; me.calc_loop_triangles(); co = getco(o)
    ne = len(me.edges); le = np.empty(len(me.loops), dtype=np.int64); me.loops.foreach_get("edge_index", le)
    lv = np.empty(len(me.loops), dtype=np.int64); me.loops.foreach_get("vertex_index", lv)
    ed = np.empty(ne * 2, dtype=np.int64); me.edges.foreach_get("vertices", ed); ed = ed.reshape(-1, 2)
    fpe = np.bincount(le, minlength=ne); sign = np.where(lv == ed[le, 0], 1, -1); ssum = np.bincount(le, weights=sign, minlength=ne)
    tv = np.array([t.vertices[:] for t in me.loop_triangles])
    vol = float(np.einsum("ij,ij->i", co[tv[:, 0]], np.cross(co[tv[:, 1]], co[tv[:, 2]])).sum() / 6.0)
    return dict(verts=len(co), tris=len(tv), boundary_edges=int((fpe == 1).sum()), nonmanifold_edges=int((fpe > 2).sum()),
                flipped_edges=int(((fpe == 2) & (np.abs(ssum) == 2)).sum()), volume_m3=vol)
def islands(o):
    me = o.data; n = len(me.vertices); ed = np.empty(len(me.edges) * 2, dtype=np.int64); me.edges.foreach_get("vertices", ed); ed = ed.reshape(-1, 2)
    lab = np.arange(n)
    while True:
        old = lab.copy(); m = np.minimum(lab[ed[:, 0]], lab[ed[:, 1]]); np.minimum.at(lab, ed[:, 0], m); np.minimum.at(lab, ed[:, 1], m); lab = lab[lab]
        if np.array_equal(lab, old):
            return lab
def beauty_tris(o):
    bm = bmesh.new(); bm.from_mesh(o.data); bm.transform(o.matrix_world)
    bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method="BEAUTY", ngon_method="BEAUTY")
    T = np.array([[v.co[:] for v in f.verts] for f in bm.faces]); bm.free(); return T
def bvh_world(o):
    return BVHTree.FromPolygons([tuple(c) for c in getco(o)], [tuple(p.vertices) for p in o.data.polygons])
def inside(bvh, p):
    n_, o_ = 0, Vector(p); d = Vector((0.00017, 0.00023, 1.0)).normalized()
    for _ in range(80):
        h = bvh.ray_cast(o_, d, 500.0)
        if h[0] is None:
            break
        n_ += 1; o_ = h[0] + d * 1e-5
    return n_ % 2 == 1
def nonplanar(o, tol=1e-3):
    co = getco(o); k = 0
    for p in o.data.polygons:
        if len(p.vertices) > 3:
            V = co[list(p.vertices)]; c = V.mean(0)
            if float(np.abs((V - c) @ np.linalg.svd(V - c)[2][2]).max()) > tol:
                k += 1
    return k

PARTS = {"PRINT_building_body": ("GRAY", 3, 1), "PRINT_building_body_WHITE": ("WHITE", 1, 2), "PRINT_building_body_BLACK": ("BLACK", 2, 3),
         "PRINT_building_body_CLEAR": ("CLEAR", 4, 4), "PRINT_building_body_FRAMES": ("GRAY", 3, 5),
         "PRINT_canopy_dropoff": ("GRAY", 3, 1), "PRINT_canopy_dropoff_CLEAR": ("CLEAR", 4, 2),
         "PRINT_sunshade": ("WHITE", 1, 1), "PRINT_site_base": ("GRAY", 3, 1)}
OB = {n: bpy.data.objects[n] for n in PARTS}
BASE = {"PRINT_building_body_WHITE": "PRINT_building_body", "PRINT_building_body_BLACK": "PRINT_building_body",
        "PRINT_building_body_CLEAR": "PRINT_building_body", "PRINT_building_body_FRAMES": "PRINT_building_body",
        "PRINT_canopy_dropoff_CLEAR": "PRINT_canopy_dropoff"}

# ---------------------------------------------------------------- 2 v002 parts identical (linked read-only)
V2N = ["PRINT_building_body", "PRINT_site_base", "PRINT_canopy_dropoff", "PRINT_sunshade"]
with bpy.data.libraries.load(V002, link=True) as (src, dst):
    dst.objects = [n for n in src.objects if n in V2N]
ident = {}
for lo in dst.objects:
    a = getco(lo); b = getco(OB[lo.name])
    def canon(f):                                    # same face regardless of the loop's start vertex
        k = f.index(min(f)); return f[k:] + f[:k]
    fa = sorted(canon(tuple(p.vertices)) for p in lo.data.polygons); fb = sorted(canon(tuple(p.vertices)) for p in OB[lo.name].data.polygons)
    ident[lo.name] = dict(verts=(len(a), len(b)), faces=(len(fa), len(fb)),
                          max_vertex_diff_m=float(np.abs(a - b).max()) if a.shape == b.shape else None, same_topology=fa == fb)
    ident[lo.name]["identical"] = ident[lo.name]["max_vertex_diff_m"] is not None and ident[lo.name]["max_vertex_diff_m"] < 1e-9 and fa == fb
REP["v002_parts_identical"] = ident

# ---------------------------------------------------------------- 3 scale / size / fit
size = {}
for n, o in OB.items():
    co = getco(o); ext = (co.max(0) - co.min(0)) * MM
    size[n] = dict(printed_mm=[round(float(x), 2) for x in ext], filament_slot=o.get("filament_slot"), part_order=o.get("part_order"),
                   print_scale=o.get("print_scale"))
REP["scale"] = dict(scale=f"1:{int(SCALE)}", mm_per_m=round(MM, 5), parts=size,
                    fits_H2S={n: bool(all(a <= b for a, b in zip(sorted(v["printed_mm"][:2], reverse=True), sorted(H2S[:2], reverse=True))) and v["printed_mm"][2] <= H2S[2])
                              for n, v in size.items()})

# ---------------------------------------------------------------- 4 watertight / planar
wt = {}
for n, o in OB.items():
    m = metrics(o); isl = islands(o)
    used = np.zeros(len(isl), bool)
    for p in o.data.polygons:
        used[list(p.vertices)] = True
    m["islands"] = int(len(np.unique(isl[used]))); m["nonplanar_faces"] = nonplanar(o) if n in BASE else None
    m["watertight"] = m["boundary_edges"] == 0 and m["nonmanifold_edges"] == 0 and m["flipped_edges"] == 0 and m["volume_m3"] > 0
    wt[n] = m
REP["watertight"] = wt

def winding(Tri, Q, chunk=None):
    """generalized winding number (robust inside test; see section 6)"""
    Q = np.atleast_2d(np.asarray(Q, float)); chunk = chunk or max(1, int(1.5e7 // (len(Tri) * 9))); out = np.zeros(len(Q))
    for s in range(0, len(Q), chunk):
        R = Tri[None, :, :, :] - Q[s:s + chunk][:, None, None, :]
        a, b, c = R[..., 0, :], R[..., 1, :], R[..., 2, :]
        la, lb, lc = np.linalg.norm(a, axis=-1), np.linalg.norm(b, axis=-1), np.linalg.norm(c, axis=-1)
        num = np.einsum("mti,mti->mt", a, np.cross(b, c))
        den = la * lb * lc + np.einsum("mti,mti->mt", a, b) * lc + np.einsum("mti,mti->mt", b, c) * la + np.einsum("mti,mti->mt", c, a) * lb
        out[s:s + chunk] = (2 * np.arctan2(num, den)).sum(1) / (4 * np.pi)
    return out

# ---------------------------------------------------------------- 5 containment
BV = {n: bvh_world(o) for n, o in OB.items()}
cont = {}
for n, b in BASE.items():
    tol = 0.02 if n.endswith("FRAMES") else 0.003
    pts = np.vstack([getco(OB[n]), beauty_tris(OB[n]).mean(1)]); far, dists = [], []
    for i, p in enumerate(pts):
        loc, nrm, idx, dist = BV[b].find_nearest(Vector(p))
        if dist is not None and dist > tol:
            far.append(i); dists.append(dist)
    w = winding(beauty_tris(OB[b]), pts[far]) if far else np.zeros(0)       # robust inside test (winding number)
    out_d = [d_ for d_, wi in zip(dists, w) if wi < 0.5]
    cont[n] = dict(points=len(pts), outside=len(out_d), worst_m=round(max(out_d), 4) if out_d else 0.0, tolerance_m=tol)
REP["containment"] = cont

# ---------------------------------------------------------------- 6 colour correctness vs v023
def colour_of_material(m):
    if m.startswith(("ACM-1", "ACM-4", "MTL-2", "TPO", "UNRES-colour_terrace_pavers", "PAINT_match_ACM-1")): return "WHITE"
    if m.startswith(("ACM-2", "ACM-3", "MTL-1", "MTL-3")): return "BLACK"
    if m.startswith("GLASS"): return "CLEAR"
    return "GRAY"
SRC_COLL = ["01_Masses", "02_Parapets", "03_Opening_panels", "05_Door_Side_Canopies", "07_Glass_Railings", "11_Facade_Detail_v004"]
with bpy.data.libraries.load(V023, link=True) as (src, dst):
    dst.collections = [c for c in src.collections if c in SRC_COLL]
V, F, FC = [], [], []            # every non-glass finish face
GV, GF = [], []                  # glass faces (vision + spandrel panes, rails, canopy glass)
RV, RF = [], []                  # storefront / curtain-wall frame faces (gray by owner decision; widened / extended in v002)
for c in dst.collections:
    for o in c.all_objects:
        if o.type != "MESH" or not o.data.polygons:
            continue
        co = getco(o); off = len(V); goff = len(GV); roff = len(RV)
        slots = [s.material.name if s.material else "" for s in o.material_slots]
        V.extend(map(tuple, co)); GV.extend(map(tuple, co)); RV.extend(map(tuple, co))
        is_frame = c.name == "11_Facade_Detail_v004" and "spandrel" not in o.name and "HM_door" not in o.name
        for p in o.data.polygons:
            mat = slots[p.material_index] if p.material_index < len(slots) else ""
            col = colour_of_material(mat)
            if c.name == "11_Facade_Detail_v004" and "spandrel" not in o.name and col not in ("WHITE", "BLACK"):
                col = "GRAY"                               # frames / mullions: Beachstone Gray (owner 2026-09-29)
            if col == "CLEAR":
                GF.append(tuple(i + goff for i in p.vertices))
            else:
                F.append(tuple(i + off for i in p.vertices)); FC.append(col)
                if is_frame and col == "GRAY":
                    RF.append(tuple(i + roff for i in p.vertices))
SRC = BVHTree.FromPolygons(V, F)
GLASS = BVHTree.FromPolygons(GV, GF)
FRM = BVHTree.FromPolygons(RV, RF)
body = OB["PRINT_building_body"]; T = beauty_tris(body)
nrm = np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0]); area = np.linalg.norm(nrm, axis=1) / 2; nrm = nrm / np.maximum(2 * area, 1e-30)[:, None]
vis = (nrm[:, 2] > -0.5) & (T.mean(1)[:, 2] > 0.02)           # visible exterior: not undersides, above grade (foundation is in the pocket)
rng = np.random.default_rng(240)
NS = 24000
cand = np.where(vis)[0]; w = area[cand] / area[cand].sum()
pick = rng.choice(cand, size=NS, p=w)
r1, r2 = rng.random(NS), rng.random(NS); s = np.sqrt(r1)
P = (1 - s)[:, None] * T[pick, 0] + (s * (1 - r2))[:, None] * T[pick, 1] + (s * r2)[:, None] * T[pick, 2]
N = nrm[pick]
ORDER = [("PRINT_building_body_FRAMES", "GRAY"), ("PRINT_building_body_CLEAR", "CLEAR"), ("PRINT_building_body_BLACK", "BLACK"),
         ("PRINT_building_body_WHITE", "WHITE")]
def winding(Tri, Q, chunk=None):
    """generalized winding number of points Q w.r.t. triangle soup Tri (robust to internal walls / overlapping shells,
    unlike ray parity): sum of signed solid angles / 4 pi (Van Oosterom - Strackee)"""
    chunk = chunk or max(1, int(1.5e7 // (len(Tri) * 9)))          # ~120 MB working set per chunk
    out = np.zeros(len(Q))
    for s in range(0, len(Q), chunk):
        q = Q[s:s + chunk][:, None, None, :]
        R = Tri[None, :, :, :] - q                                  # (m, t, 3, 3)
        a, b, c = R[..., 0, :], R[..., 1, :], R[..., 2, :]
        la, lb, lc = np.linalg.norm(a, axis=-1), np.linalg.norm(b, axis=-1), np.linalg.norm(c, axis=-1)
        num = np.einsum("mti,mti->mt", a, np.cross(b, c))
        den = la * lb * lc + np.einsum("mti,mti->mt", a, b) * lc + np.einsum("mti,mti->mt", b, c) * la + np.einsum("mti,mti->mt", c, a) * lb
        out[s:s + chunk] = (2 * np.arctan2(num, den)).sum(1) / (4 * np.pi)
    return out
TRI = {n: beauty_tris(OB[n]) for n, _ in ORDER}
def effective_all(Q):
    res = np.array(["GRAY"] * len(Q), dtype=object); done = np.zeros(len(Q), bool); wn = {}
    for n, c in ORDER:                                               # frames > clear > black > white > body
        idx = np.where(~done)[0]
        if not len(idx):
            break
        # only points near this part's bounding box need the (costly) winding number
        lo, hi = TRI[n].reshape(-1, 3).min(0) - 0.05, TRI[n].reshape(-1, 3).max(0) + 0.05
        near = idx[np.all((Q[idx] >= lo) & (Q[idx] <= hi), axis=1)]
        w = winding(TRI[n], Q[near]) if len(near) else np.zeros(0)
        wn[n] = w
        hit = near[w > 0.5]; res[hit] = c; done[hit] = True
    return res, wn
CLS = ["WHITE", "BLACK", "GRAY", "CLEAR"]
conf = {e: {g: 0.0 for g in CLS + ["UNMATCHED"]} for e in CLS}
mism = []
per = area[cand].sum() / NS
Qs = P - N * 0.012                                              # 1.2 cm inside = 0.05 mm printed (the outer perimeter)
EFF, WN = effective_all(Qs)
REP["winding_number_overlap_check"] = {n: dict(points=int(len(w)), max=round(float(w.max()), 3) if len(w) else None,
                                               points_above_1p5=int((w > 1.5).sum())) for n, w in WN.items()}
for p, nv, eff in zip(P, N, EFF):
    g = GLASS.ray_cast(Vector(p + nv * 1e-4), Vector(nv), 0.8)     # a glass pane directly in front: glazing recess back
    gn = GLASS.find_nearest(Vector(p), 0.35)                        # or the point is ON glass (rail / canopy glass sides)
    loc, _, fi, dist = SRC.find_nearest(Vector(p), 0.35)
    fr = FRM.find_nearest(Vector(p), 0.12)                          # on a (widened) storefront / curtain-wall frame
    if g[0] is not None:
        exp, fi, dist = "CLEAR", 0, g[3]
    elif fr[0] is not None:
        exp, fi, dist = "GRAY", 0, fr[3]
    elif gn[0] is not None and (fi is None or gn[3] < dist - 0.01):
        exp, fi, dist = "CLEAR", 0, gn[3]
    else:
        exp = FC[fi] if fi is not None else "UNMATCHED"
    conf[eff][exp] += per
    if fi is not None and eff != exp:
        mism.append((round(float(p[0]), 2), round(float(p[1]), 2), round(float(p[2]), 2), exp, eff, round(float(dist), 3)))
EXPS = []
for p, nv in zip(P, N):                                         # expected colour per sample, kept for the G-code check
    g = GLASS.ray_cast(Vector(p + nv * 1e-4), Vector(nv), 0.8); gn = GLASS.find_nearest(Vector(p), 0.35)
    loc, _, fi, dist = SRC.find_nearest(Vector(p), 0.35); fr = FRM.find_nearest(Vector(p), 0.12)
    EXPS.append("CLEAR" if g[0] is not None else "GRAY" if fr[0] is not None else
                "CLEAR" if (gn[0] is not None and (fi is None or gn[3] < dist - 0.01)) else (FC[fi] if fi is not None else "UNMATCHED"))
np.savez(os.path.join(VAL, "print_validation_v003_samples.npz"), P=P, N=N, EFF=np.array(EFF, dtype="U8"), EXP=np.array(EXPS, dtype="U10"))
tot = sum(sum(r.values()) for r in conf.values())
matched = sum(conf[e][g] for e in CLS for g in CLS)
agree = sum(conf[c][c] for c in CLS)
REP["colour_correctness"] = dict(
    samples=NS, visible_body_area_m2=round(float(area[cand].sum()), 1),
    confusion_area_m2_effective_vs_expected={e: {g: round(v, 2) for g, v in r.items()} for e, r in conf.items()},
    agreement_pct_of_matched=round(100 * agree / matched, 2), unmatched_pct=round(100 * (tot - matched) / tot, 2),
    effective_colour_area_pct={e: round(100 * sum(conf[e].values()) / tot, 2) for e in CLS},
    note="expected = CLEAR where a v023 glass pane lies directly in front (outward ray <= 0.8 m), else the finish of the nearest "
         "non-glass v023 face within 0.35 m (frames forced gray); "
         "mismatches concentrate within a few cm of finish boundaries and on relief the print widened (frames, parapets)")
with open(os.path.join(VAL, "print_validation_v003_colour_mismatches.csv"), "w", newline="", encoding="utf-8") as f:
    wr = csv.writer(f); wr.writerow(["x", "y", "z", "expected_v023", "effective_print", "dist_to_source_m"]); wr.writerows(mism)
# cluster the mismatches on a 1 m grid so a real mis-assignment (a whole panel) stands out from boundary noise
cl = {}
for x, y, z, e, g, d in mism:
    k = (round(x), round(y), round(z), e, g); cl[k] = cl.get(k, 0) + per
REP["colour_mismatch_clusters_top"] = [dict(cell_m=list(k[:3]), expected=k[3], effective=k[4], area_m2=round(v, 3))
                                       for k, v in sorted(cl.items(), key=lambda kv: -kv[1])[:25]]

# ---------------------------------------------------------------- 7 thickness + islands per colour part
thick = {}
for n in list(BASE) + ["PRINT_sunshade"]:
    o = OB[n]; TT = beauty_tris(o); nn = np.cross(TT[:, 1] - TT[:, 0], TT[:, 2] - TT[:, 0]); aa = np.linalg.norm(nn, axis=1) / 2
    nn = nn / np.maximum(2 * aa, 1e-30)[:, None]
    k = min(3000, len(TT)); idx = rng.choice(len(TT), size=k, p=aa / aa.sum())
    ts = []
    for i in idx:
        c = TT[i].mean(0); h = BV[n].ray_cast(Vector(c - nn[i] * 1e-5), Vector(-nn[i]), 50.0)
        if h[0] is not None:
            ts.append((h[0] - Vector(c)).length * MM)
    ts = np.array(ts)
    lab = islands(o); co = getco(o); me = o.data; me.calc_loop_triangles()
    tv = np.array([t.vertices[:] for t in me.loop_triangles])
    vols = np.bincount(lab[tv[:, 0]], weights=np.einsum("ij,ij->i", co[tv[:, 0]], np.cross(co[tv[:, 1]], co[tv[:, 2]])) / 6.0, minlength=len(co))
    used = np.unique(lab[tv[:, 0]]); iv = np.abs(vols[used]) * MM ** 3
    thick[n] = dict(samples=int(len(ts)), min_mm=round(float(ts.min()), 3) if len(ts) else None,
                    p5_mm=round(float(np.percentile(ts, 5)), 3) if len(ts) else None, median_mm=round(float(np.median(ts)), 3) if len(ts) else None,
                    share_below_0p4mm_pct=round(100 * float((ts < 0.4).mean()), 2) if len(ts) else None,
                    islands=int(len(used)), islands_below_0p5mm3=int((iv < 0.5).sum()), smallest_island_mm3=round(float(iv.min()), 4) if len(iv) else None,
                    volume_mm3=round(float(np.abs(vols[used]).sum() * MM ** 3), 1))
REP["colour_part_thickness_and_islands"] = thick

REP["summary"] = dict(
    frozen_files_ok=all(v["ok"] for v in frozen.values()) and REP["v002_manifest_entries"]["all_ok"],
    v002_parts_identical=all(v["identical"] for v in ident.values()),
    all_watertight=all(v["watertight"] for v in wt.values()),
    colour_parts_planar=all((v["nonplanar_faces"] or 0) == 0 for v in wt.values()),
    colour_parts_inside_base=all(v["outside"] == 0 for v in cont.values()),
    colour_agreement_pct=REP["colour_correctness"]["agreement_pct_of_matched"],
    fits_H2S=all(REP["scale"]["fits_H2S"].values()),
    runtime_s=round(time.time() - T0, 1))
with open(os.path.join(VAL, "print_validation_v003.json"), "w", encoding="utf-8") as f:
    json.dump(REP, f, indent=1)
print("[validate] summary", json.dumps(REP["summary"]))
print("[validate] effective colour area %", REP["colour_correctness"]["effective_colour_area_pct"])
print("[validate] done (nothing saved)", bpy.data.is_dirty)
