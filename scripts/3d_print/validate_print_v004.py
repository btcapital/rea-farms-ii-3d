"""Building II print v004 (MULTICOLOR SITE BASE) - independent validation of the exported 3MF, read FROM DISK.

Run:  python scripts/3d_print/validate_print_v004.py          (Blender 5.2 Python module, for mathutils BVH trees)
Checks:
  1. frozen v003 package unchanged (print_phase_v003_FROZEN_2026-09-29.sha256; text files hashed as CRLF, as frozen)
  2. 3MF structure: one object, 3 parts in order base (3) < GREEN (4) < BLACK (2)
  3. base part = the approved v003 site base: identical vertices and triangles, identical item transform -> same 1:240
     scale, same footprint, same pocket and same canopy sockets (fit geometry)
  4. every colour shell closed; colour parts inside the base (generalized winding number; 0.02 m = 0.08 mm tolerance)
     -> no colour part reaches into the pocket, the sockets or past the edges
  5. colour correctness from the DOCUMENTED v023 sources (pristine audit copy, read-only), not from the build's own
     classification: points on asphalt / Onyx plaza (dark), lawn and beds (green), walks / concrete (gray), bollards
     (gray), shrubs (green) are located on the base surface and their effective Bambu colour (later part wins) checked
  6. layer analysis: colours present per layer -> filament-change estimate at 0.12 / 0.16 / 0.20 mm layers
Writes exports/Building_II/3d_print/validation/print_validation_v004.json
"""
import bpy, hashlib, json, os, sys, time, zipfile
import numpy as np
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from mathutils import Vector
from mathutils.bvhtree import BVHTree

T0 = time.time()
COLOUR_ONLY = "--colour-only" in sys.argv          # re-run sections 5-6 only; sections 1-4 are kept from the last report
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MF = os.path.join(ROOT, "exports", "Building_II", "3d_print", "3mf"); VAL = os.path.join(ROOT, "exports", "Building_II", "3d_print", "validation")
V004 = os.path.join(MF, "building_II_v004_1-240_multicolor_site_base.3mf")
V003_SITE = os.path.join(MF, "building_II_v003_1-240_site_base.3mf")
ARCHIVE = os.path.join(ROOT, "models", "Building_II", "print_derivatives", "archive", "building_II_print_v001_audit_copy.blend")
NS = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
K = 1000.0 / 240.0
OUT = {"file": os.path.relpath(V004, ROOT), "checks": {}}
if COLOUR_ONLY:
    _prev = json.load(open(os.path.join(VAL, "print_validation_v004.json"), encoding="utf-8"))
    _w = json.load(open(os.path.join(VAL, "print_export_v004_written.json"), encoding="utf-8"))["sha256"]
    assert _prev.get("sha256_of_3mf", _w) == _w == hashlib.sha256(open(V004, "rb").read()).hexdigest(), "3MF changed since the full run"
    OUT["checks"] = {k: v for k, v in _prev["checks"].items() if not k.startswith("colour:")}
def ok(name, passed, **kw):
    OUT["checks"][name] = dict(passed=bool(passed), **kw); print(f"[validate v004] {'PASS' if passed else 'FAIL'} {name} {kw if not passed else ''}")
def sha_file(p, crlf=False):
    b = open(p, "rb").read()
    if crlf:
        b = b.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
    return hashlib.sha256(b).hexdigest()

OUT["sha256_of_3mf"] = hashlib.sha256(open(V004, "rb").read()).hexdigest()
# 1. frozen package ------------------------------------------------------------------------------------------------
TEXT = (".py", ".json", ".csv", ".txt", ".md")
res = []
for line in ([] if COLOUR_ONLY else  open(os.path.join(ROOT, "manifests", "3d_print", "print_phase_v003_FROZEN_2026-09-29.sha256"), encoding="utf-8")):
    h, p = line.strip().split(" *", 1); fp = os.path.join(ROOT, p)
    if not os.path.exists(fp) or open(fp, "rb").read(40).startswith(b"version https://git-lfs"):
        res.append((p, "not checked out (Git LFS pointer)")); continue
    got = {sha_file(fp)} | ({sha_file(fp, crlf=True)} if p.endswith(TEXT) else set())
    res.append((p, "OK" if h in got else "CHANGED"))
changed = [p for p, r in res if r == "CHANGED"]
if not COLOUR_ONLY:
    ok("frozen_v003_package_unchanged", not changed, checked=sum(r == "OK" for _, r in res), changed=changed,
       not_checked_out=[p for p, r in res if r.startswith("not")])

# 2. structure -----------------------------------------------------------------------------------------------------
def read_3mf(path):
    z = zipfile.ZipFile(path)
    sub = ET.fromstring(z.read("3D/Objects/object_1.model"))
    meshes = {}
    for o in sub.findall("m:resources/m:object", NS):
        co = np.array([[float(v.get(a)) for a in "xyz"] for v in o.findall("m:mesh/m:vertices/m:vertex", NS)])
        tv = np.array([[int(t.get(a)) for a in ("v1", "v2", "v3")] for t in o.findall("m:mesh/m:triangles/m:triangle", NS)], dtype=np.int64)
        meshes[o.get("id")] = (co, tv)
    top = ET.fromstring(z.read("3D/3dmodel.model"))
    comps = [c.get("objectid") for c in top.find("m:resources/m:object", NS).findall("m:components/m:component", NS)]
    T = [float(x) for x in top.find("m:build/m:item", NS).get("transform").split()]
    cfg = ET.fromstring(z.read("Metadata/model_settings.config"))
    parts = [(p.get("id"), {m.get("key"): m.get("value") for m in p.findall("metadata")}) for p in cfg.find("object").findall("part")]
    return meshes, comps, T, parts, len(top.findall("m:resources/m:object", NS))
meshes, comps, T, parts, nobj = read_3mf(V004)
names = [d["name"] for _, d in parts]; ext = [int(d["extruder"]) for _, d in parts]
ok("structure_one_object_three_parts", nobj == 1 and len(parts) == 3 and ext == [3, 4, 2] and [i for i, _ in parts] == comps,
   parts=list(zip(names, ext)))
BASE4, GREEN, BLACK = (meshes[i] for i in comps)
m3, c3, T3, p3, _ = read_3mf(V003_SITE)
BASE3 = m3[c3[0]]

# 3. base identical -> scale, footprint, pocket and sockets unchanged -----------------------------------------------
same = BASE4[0].shape == BASE3[0].shape and np.array_equal(BASE4[1], BASE3[1]) and np.abs(BASE4[0] - BASE3[0]).max() < 1e-9
ok("base_identical_to_v003", same and T == T3, vertices=len(BASE4[0]), triangles=len(BASE4[1]), transform=T)
size = (BASE4[0].max(0) - BASE4[0].min(0))
ok("scale_1_to_240_and_size", np.allclose(size, [76.25 * K, 45.5 * K, size[2]], atol=1e-3) and np.allclose(size, [317.708, 189.583, 37.465], atol=2e-3),
   size_mm=size.round(3).tolist(), crop_real_m=[76.25, 45.5])
P = BASE4[0] + np.array(T[9:12]); lo = np.vstack([P, GREEN[0] + T[9:12], BLACK[0] + T[9:12]]).min(0); hi = np.vstack([P, GREEN[0] + T[9:12], BLACK[0] + T[9:12]]).max(0)
ok("on_bed", abs(lo[2]) < 1e-6 and lo[0] >= 0 and lo[1] >= 0 and hi[0] <= 340 and hi[1] <= 320, bbox_on_bed_mm=[lo.round(3).tolist(), hi.round(3).tolist()])

# 4. closed shells + containment -------------------------------------------------------------------------------------
def shells_closed(tv):
    e = np.sort(np.concatenate([tv[:, [0, 1]], tv[:, [1, 2]], tv[:, [2, 0]]]), axis=1)
    _, cnt = np.unique(e, axis=0, return_counts=True)
    d = np.concatenate([tv[:, [0, 1]], tv[:, [1, 2]], tv[:, [2, 0]]]); _, dc = np.unique(d, axis=0, return_counts=True)
    return int((cnt != 2).sum()), int((dc > 1).sum())
for nm, (co, tv) in (("GREEN", GREEN), ("BLACK", BLACK)):
    bad_e, bad_o = shells_closed(tv)
    ok(f"{nm}_shells_closed_and_oriented", bad_e == 0 and bad_o == 0, open_or_nonmanifold_edges=bad_e, misoriented_edges=bad_o, triangles=len(tv))
BB = BVHTree.FromPolygons(BASE4[0].tolist(), BASE4[1].tolist()); BTRI = BASE4[0][BASE4[1]]
def winding(Tri, Q):
    Q = np.atleast_2d(np.asarray(Q, float)); out = np.zeros(len(Q)); chunk = max(1, int(1.5e7 // (len(Tri) * 9)))
    for s in range(0, len(Q), chunk):
        R = Tri[None, :, :, :] - Q[s:s + chunk][:, None, None, :]
        a, b, c = R[..., 0, :], R[..., 1, :], R[..., 2, :]
        la, lb, lc = np.linalg.norm(a, axis=-1), np.linalg.norm(b, axis=-1), np.linalg.norm(c, axis=-1)
        num = np.einsum("mti,mti->mt", a, np.cross(b, c))
        den = la * lb * lc + np.einsum("mti,mti->mt", a, b) * lc + np.einsum("mti,mti->mt", b, c) * la + np.einsum("mti,mti->mt", c, a) * lb
        out[s:s + chunk] = (2 * np.arctan2(num, den)).sum(1) / (4 * np.pi)
    return out
def parity_inside(bvh, p, d=(0.3107, -0.2683, 0.9119)):      # tilted: a vertical ray runs through stacked skin / base vertices
    d = Vector(d).normalized(); o_ = Vector(p); n_ = 0
    for _ in range(400):
        h = bvh.ray_cast(o_, d, 1e4)
        if h[0] is None:
            break
        n_ += 1; o_ = h[0] + d * 1e-6
    return n_ % 2 == 1
for nm, (co, tv) in (() if COLOUR_ONLY else (("GREEN", GREEN), ("BLACK", BLACK))):
    pts = np.vstack([co, co[tv].mean(1)])
    far = [k for k, p in enumerate(pts) if BB.find_nearest(Vector(p))[3] > 0.02 * K]          # 0.02 m real
    sus = [k for k in far if not parity_inside(BB, pts[k])]
    out_ = [k for k, w in zip(sus, winding(BTRI, pts[sus])) if w < 0.5] if sus else []
    ok(f"{nm}_inside_base (tolerance 0.08 mm printed)", not out_, points=len(pts), outside=len(out_),
       examples_mm=[pts[k].round(3).tolist() for k in out_[:10]])

# 5. colour correctness from the documented v023 sources -------------------------------------------------------------
bpy.ops.wm.open_mainfile(filepath=ARCHIVE, load_ui=False)                    # read-only: never saved
CROP = dict(x0=-9.0, x1=67.25, y0=-5.0, y1=40.5)
PART_BVH = {nm: BVHTree.FromPolygons((co / K).tolist(), tv.tolist()) for nm, (co, tv) in (("GREEN", GREEN), ("BLACK", BLACK))}
BASE_M = BASE4[0] / K; BBM = BVHTree.FromPolygons(BASE_M.tolist(), BASE4[1].tolist())
def inside_part(nm, q, n):
    """q (just under the visible surface) is inside part nm if, along a ray from q, the part's faces are exited more often
    than entered (exits - entries > 0; the part is a join of closed shells that touch or overlap). Upward surfaces use a
    vertical ray: the skin prisms were swept straight down, so a vertical ray never runs into their coincident side walls
    (a ray along a sloped surface normal crosses them)."""
    d = Vector((0.0, 0.0, 1.0)) if n[2] > 0.3 else Vector(n)
    o_ = Vector(q); bal = 0
    for _ in range(64):
        h = PART_BVH[nm].ray_cast(o_, d, 3.0)
        if h[0] is None:
            break
        bal += 1 if h[1].dot(d) > 0 else -1; o_ = h[0] + d * 1e-6
    return bal > 0
def effective(p_surface, n_surface):
    q = np.asarray(p_surface) - np.asarray(n_surface) * 0.02                  # 0.08 mm under the visible surface
    for nm in ("BLACK", "GREEN"):                                              # later part wins
        if inside_part(nm, q, n_surface):
            return nm
    return "GRAY"
def surface_point_over(x, y, zref, lo=-0.03, hi=0.03):
    """the base's upward top surface at (x, y) whose height is within [zref+lo, zref+hi] of the documented surface; None
    where the documented surface is not the visible one there (covered by a walk, a bed, a plant, or cut away)"""
    o_ = Vector((x, y, 50.0)); best = None
    for _ in range(40):
        h = BBM.ray_cast(o_, Vector((0, 0, -1)), 200.0)
        if h[0] is None:
            break
        if h[1].z > 0.3 and lo <= h[0].z - zref <= hi:
            best = h; break
        if h[1].z > 0.3:
            break                                                              # the visible top is something else
        o_ = h[0] + Vector((0, 0, -1e-5))
    return best
rng = np.random.default_rng(240)
def sample_object_faces(obj_name, want, mat_filter=None, n=400, min_nz=0.5, lo=-0.03, hi=0.03):
    o = bpy.data.objects[obj_name]; M = o.matrix_world; me = o.data
    slots = [s.material.name if s.material else "" for s in o.material_slots]
    polys = [p for p in me.polygons if abs((M.to_3x3() @ p.normal).normalized().z) > min_nz and (mat_filter is None or slots[p.material_index] == mat_filter)]
    if not polys:
        return None
    areas = np.array([p.area for p in polys]); pick = rng.choice(len(polys), size=min(n * 3, 3000), p=areas / areas.sum())
    res = Counter(); used = 0
    for k in pick:
        p = polys[k]; vs = [M @ me.vertices[i].co for i in p.vertices]
        w = rng.dirichlet(np.ones(len(vs))); pt = sum((v * wi for v, wi in zip(vs, w)), Vector((0, 0, 0)))
        if not (CROP["x0"] + 0.3 < pt.x < CROP["x1"] - 0.3 and CROP["y0"] + 0.3 < pt.y < CROP["y1"] - 0.3):
            continue
        h = surface_point_over(pt.x, pt.y, pt.z, lo, hi)
        if h is None:
            res["documented surface not visible here (covered by another element, or cut)"] += 1; continue
        res[effective(np.array(h[0]), np.array(h[1]))] += 1; used += 1
        if used >= n:
            break
    tot = sum(v for k, v in res.items() if k in ("GREEN", "BLACK", "GRAY"))
    return dict(want=want, samples=tot, result=dict(res), agree_pct=round(100.0 * res[want] / tot, 2) if tot else None)
CHECKS = {
    "asphalt drive / drop-off lane (terrain SITE_existing_asphalt) is dark": ("Site_Terrain_INTERPOLATED", "BLACK", "SITE_existing_asphalt"),
    "entry plaza (Westmount Onyx pavers) is dark": ("Site_Entry_plaza", "BLACK", None),
    "lawn terrain is green": ("Site_Terrain_INTERPOLATED", "GREEN", "SITE_lawn_ground_shape_no_planting"),
    "landscape-bed terrain is green": ("Site_Terrain_INTERPOLATED", "GREEN", "SITE_landscape_bed_ground_shape"),
    "south mulch planting strip is green": ("LAND_Bed_mulch_south_strip", "GREEN", None),
    "north-east lawn bed is green": ("LAND_Lawn_northeast_bed", "GREEN", None),
    "north-west paver walk is gray": ("Site_Walk_north_west", "GRAY", None),
    "west paver walk is gray": ("Site_Walk_west", "GRAY", None),
    "drop-off band (pavers) is gray": ("Site_Dropoff_band_west", "GRAY", None),
    "generator-yard concrete slab is gray": ("Site_Generator_yard_slab", "GRAY", None),
    "south-west concrete walk is gray": ("Site_Walk_southwest", "GRAY", None),
    "transformer pad is gray": ("Site_Transformer_pad", "GRAY", None),
}
CC = {}
for label, (obj, want, mf) in CHECKS.items():
    # beds were printed as raised pads: top = max(bed sheet, grade) + 0.072 m, so their visible top is above the sheet
    lo_, hi_ = (0.0, 0.40) if obj.startswith("LAND_") else (-0.03, 0.03)
    CC[label] = sample_object_faces(obj, want, mf, lo=lo_, hi=hi_)
# bollards (owner: gray) and shrubs (green): the documented top of each item, located on the base surface
def item_tops(prefix, want, exclude=()):
    res = Counter()
    for o in bpy.data.objects:
        if o.type != "MESH" or not o.name.startswith(prefix) or any(e in o.name for e in exclude):
            continue
        co = np.array([o.matrix_world @ v.co for v in o.data.vertices]); c = (co.min(0) + co.max(0)) / 2
        if not (CROP["x0"] < c[0] < CROP["x1"] and CROP["y0"] < c[1] < CROP["y1"]):
            continue
        h = BBM.ray_cast(Vector((c[0], c[1], 50.0)), Vector((0, 0, -1)), 200.0)
        if h[0] is None:
            res["no base under item (inside the pocket footprint)"] += 1; continue
        res[effective(np.array(h[0]), np.array(h[1]))] += 1
    tot = sum(v for k, v in res.items() if k in ("GREEN", "BLACK", "GRAY"))
    return dict(want=want, samples=tot, result=dict(res), agree_pct=round(100.0 * res[want] / tot, 2) if tot else None)
CC["bollards are gray (top of each bollard)"] = item_tops("DET_Bollard", "GRAY", exclude=("_lens",))
VEGN = [o.name for o in bpy.data.objects if o.name.startswith("LAND_") and any(s.material and s.material.name.startswith("VEG_") for s in o.material_slots)]
res = Counter()
for n in VEGN:
    o = bpy.data.objects[n]; co = np.array([o.matrix_world @ v.co for v in o.data.vertices]); c = (co.min(0) + co.max(0)) / 2
    if not (CROP["x0"] < c[0] < CROP["x1"] and CROP["y0"] < c[1] < CROP["y1"]):
        continue
    h = BBM.ray_cast(Vector((c[0], c[1], 50.0)), Vector((0, 0, -1)), 200.0)
    if h[0] is None or h[0].z > 20:
        res["not on the site base (roof / terrace planting, part of the building)"] += 1; continue
    res[effective(np.array(h[0]), np.array(h[1]))] += 1
tot = sum(v for k, v in res.items() if k in ("GREEN", "BLACK", "GRAY"))
CC["shrubs and tree are green (top of each plant)"] = dict(want="GREEN", samples=tot, result=dict(res), agree_pct=round(100.0 * res["GREEN"] / tot, 2) if tot else None)
for label, r in CC.items():
    ok(f"colour: {label}", r is not None and r["samples"] > 0 and r["agree_pct"] >= 95.0, **(r or {}))

OUT["colour_sampling_note"] = ("points are drawn on the documented v023 surface and kept only where that surface is the visible top of "
                               "the base (within 3 cm real; beds: 0-40 cm above their sheet, as printed as raised pads); their colour is "
                               "the effective Bambu colour 0.08 mm under the surface (later part wins)")
# 6. layer analysis -> filament changes -------------------------------------------------------------------------------
def z_ranges(co, tv):
    """per closed shell (connected triangles) z-range in printed mm (on the bed: + item z offset)"""
    n = len(co); parent = np.arange(n)
    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]; a = parent[a]
        return a
    for t in tv:
        ra = find(t[0])
        for b in t[1:]:
            rb = find(b)
            if rb != ra:
                parent[rb] = ra
    roots = np.array([find(i) for i in range(n)])
    zs = co[:, 2] + T[11]; out = defaultdict(lambda: [1e9, -1e9])
    for r, z in zip(roots, zs):
        a = out[r]; a[0] = min(a[0], z); a[1] = max(a[1], z)
    return np.array(list(out.values()))
ZR = {"GREEN": z_ranges(*GREEN), "BLACK": z_ranges(*BLACK)}
top_z = (BASE4[0][:, 2] + T[11]).max()
LAYERS = {}
for lh in (0.12, 0.16, 0.20):
    zs = np.arange(0.2 + lh / 2, top_z, lh)
    k = np.ones(len(zs), int)                                                 # gray (edges / walls) is on every layer
    for nm, zr in ZR.items():
        present = np.zeros(len(zs), bool)
        for a, b in zr:
            present |= (zs > a) & (zs < b)
        k += present
    LAYERS[f"{lh:.2f}mm"] = dict(layers=int(len(zs)), layers_with_2_colours=int((k == 2).sum()), layers_with_3_colours=int((k == 3).sum()),
                                 estimated_filament_changes=int((k - 1).sum()),
                                 colour_z_range_mm={nm: [round(float(zr[:, 0].min()), 2), round(float(zr[:, 1].max()), 2)] for nm, zr in ZR.items()})
OUT["layer_analysis"] = LAYERS
OUT["layer_analysis_note"] = ("colours present per layer from the parts' shell height ranges; Bambu orders the filaments so each layer starts "
                              "with the previous layer's last colour, so changes = sum over layers of (colours on the layer - 1). An estimate: "
                              "the Bambu Studio slice is the authority.")
vol = {nm: float(np.einsum("ij,ij->i", co[tv[:, 0]], np.cross(co[tv[:, 1]], co[tv[:, 2]])).sum() / 6.0) for nm, (co, tv) in (("BASE", BASE4), ("GREEN", GREEN), ("BLACK", BLACK))}
OUT["volumes_mm3"] = {k: round(v, 1) for k, v in vol.items()}
OUT["passed"] = all(c["passed"] for c in OUT["checks"].values()); OUT["runtime_s"] = round(time.time() - T0, 1)
with open(os.path.join(VAL, "print_validation_v004.json"), "w", encoding="utf-8") as f:
    json.dump(OUT, f, indent=1, default=lambda x: x.tolist() if hasattr(x, "tolist") else str(x))
print(f"[validate v004] {'ALL PASS' if OUT['passed'] else 'FAILURES'}; layers {LAYERS}; volumes {OUT['volumes_mm3']}  ({OUT['runtime_s']}s)")
