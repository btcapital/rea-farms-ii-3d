"""Building II 3D-print derivative v004 - MULTICOLOR SITE BASE (1:240), 2026-10-02.

Only the site base changes. The approved v003 building, drop-off canopy and sun-shade (and their colours) are frozen and
are the companion parts of this site base; they are not rebuilt here.

Run (background Blender 5.2, from the project root; the archive audit copy is opened READ-ONLY and never saved):
  blender -b models/Building_II/print_derivatives/archive/building_II_print_v001_audit_copy.blend \
          --python scripts/3d_print/build_print_v004.py
  (or, with Blender as a Python module:  python scripts/3d_print/build_print_v004.py)

Input : archive/building_II_print_v001_audit_copy.blend (= frozen v023, hash-checked) for the documented site sources;
        exports/.../3mf/building_II_v003_1-240_site_base.3mf (the approved, printed site-base mesh, hash-checked).
Output: models/Building_II/print_derivatives/building_II_print_v004.blend (new file) + print_prep_v004_build_log.json.

Site colour mapping (owner 2026-10-02; filament slots match v003 where the colour is shared):
  slot 2 BLACK  = vehicular asphalt (terrain faces SITE_existing_asphalt: drive aisle / drop-off lane)
                  + entry plaza pavers (SITE_plaza_Techo-Bloc_Westmount_Onyx = dark charcoal, documented)
                  + utility-yard metal copings (MTL-1, match ACM-2 black, documented; same as the building copings)
  slot 3 GRAY   = the exact v003 site base itself: concrete flatwork, stairs, landings, pads, Linea Shale Gray paver walks
                  and drop-off bands, curbs, bollards (owner), light poles (inferred, see below), brick yard walls,
                  base edges / underside / pocket / sockets
  slot 4 GREEN  = lawn and planting-bed terrain, lawn / mulch beds and the entrance bed fill, retained lawn fill,
                  all 338 shrubs and the tree canopy
Method (the v003 priority overlay): the exact v003 site base stays ONE gray part. Colour parts lie INSIDE it:
  * skins: every lawn / bed / asphalt / plaza / coping face of the approved base gets a 1.0 mm piece below it (upward
    faces: swept straight down, so neighbouring regions meet on clean vertical planes; steep faces: swept along the
    inward normal); depth limited to the base thickness under the face
  * plants: the shrub domes and the tree canopy (the exact operands that were unioned into the base) as whole solids
Part order = colour priority in Bambu Studio (a later part wins where parts overlap): base (3) < GREEN (4) < BLACK (2).
Each colour part is a JOIN of closed shells (no 3D union); Bambu fills touching / overlapping shells of a part as their
union (verified for v003 with the H2S CLI). The approved base is never cut by a boolean.
Every face of the base is classified from its DOCUMENTED source surface: the v023 object (and, for the interpolated
terrain, the v023 face material) that coincides with it. The site operands are rebuilt by running the frozen v003
script's own site-operand code (hash-checked) on the pristine v023 copy, so they are the exact solids that formed the base.
"""
import bpy, bmesh, hashlib, json, math, os, sys, time, zipfile
import numpy as np
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from mathutils import Vector
from mathutils.bvhtree import BVHTree

T0 = time.time()
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DERIV = os.path.join(ROOT, "models", "Building_II", "print_derivatives")
ARCHIVE = os.path.join(DERIV, "archive", "building_II_print_v001_audit_copy.blend")
V003_BLEND = os.path.join(DERIV, "building_II_print_v003.blend")
OUT_BLEND = os.path.join(DERIV, "building_II_print_v004.blend")
V003_SCRIPT = os.path.join(ROOT, "scripts", "3d_print", "build_print_v003.py")
MF = os.path.join(ROOT, "exports", "Building_II", "3d_print", "3mf")
V003_SITE_3MF = os.path.join(MF, "building_II_v003_1-240_site_base.3mf")
VAL = os.path.join(ROOT, "exports", "Building_II", "3d_print", "validation")
FROZEN = {  # print_phase_v003_FROZEN_2026-09-29.sha256 (scripts were hashed with Windows CRLF line endings)
    ARCHIVE: "7fe33f1e4dc906c75b54122203fec75ee9ef948be70897e46fcfd1b288235c91",
    V003_BLEND: "27737a83aee78fa464a9e3c75b518540909339b42845283857293232bb6352a7",
    V003_SITE_3MF: "9c533994379897554a8cd7e93eeb9e2fc1a0fcbb3ce7bd9ff9c565970ca4682e",
    V003_SCRIPT: "7938dc313137f7ad2e121bc9566f01d2b66a782fd44434ddb30bc20737899df9"}

def sha(p, crlf=False):
    b = open(p, "rb").read()
    if crlf:
        b = b.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
    return hashlib.sha256(b).hexdigest()
for p, h in FROZEN.items():
    assert sha(p, crlf=p.endswith(".py")) == h, f"frozen input changed or missing: {p}"
assert not os.path.exists(OUT_BLEND), "v004 exists - revisions are saved separately; never overwrite (make v005)"
if os.path.abspath(bpy.data.filepath or "") != ARCHIVE:
    bpy.ops.wm.open_mainfile(filepath=ARCHIVE, load_ui=False)

# ------------------------------------------------------------------ the frozen v003 site operands (exact code reuse)
# preamble (parameters, helpers, object classification) + the SITE BASE section up to the union. The two asserts that
# require the open file to be named v003 are dropped (this run opens the archive copy itself, hash-checked above).
_src = open(V003_SCRIPT, encoding="utf-8").read().splitlines()
_i_body = _src.index("# ================================================================== BUILDING BODY")
_i_site = _src.index("# ================================================================== SITE BASE")
_i_union = next(i for i, l in enumerate(_src) if l.startswith("m1 = boolean(terrain, site_parts"))
_pre = [l.replace("BLEND = bpy.data.filepath", f"BLEND = {OUT_BLEND!r}") for l in _src[:_i_body]
        if not l.startswith(("assert os.path.basename(BLEND)", "assert sha(BLEND)"))]
G = {"__name__": "v003_site_operands", "COLOUR_STAGE": False}
exec(compile("\n".join(_pre), "build_print_v003.py:preamble", "exec"), G)
exec(compile("\n".join(_src[_i_site:_i_union]), "build_print_v003.py:site_operands", "exec"), G)
_i_w = _src.index("def winding(Tri, Q):")
exec(compile("\n".join(_src[_i_w:_src.index("def outside_body(points, tol, bvh=None, tri=None):")]), "build_print_v003.py:winding", "exec"), G)
getco, metrics, solid_ok, fix_solid, boolean, WORK = G["getco"], G["metrics"], G["solid_ok"], G["fix_solid"], G["boolean"], G["WORK"]
SITE_OPS = G["site_parts"] + [G["terrain"]]
SCALE = 240
K = 1000.0 / SCALE
def pm(mm):
    return mm * SCALE / 1000.0
D_SKIN = pm(1.0)       # colour skin depth below lawn / asphalt / plaza / coping faces         0.240 m
STEEP_NZ = 0.3         # faces with normal z above this are swept straight down; steeper ones along -normal
CLASS_TOL = 0.05       # a base face belongs to a source surface within 5 cm (0.2 mm printed) with a parallel normal
TERRAIN_TOL = 0.25     # interpolated terrain: non-planar quads were re-triangulated by the union (seen up to 0.13 m)
EDGE_INSET = pm(0.5)   # colour stops 0.5 mm inside the base's outer edge, so the exposed edge prints gray all round 0.120 m
LOG = {"script": "scripts/3d_print/build_print_v004.py", "scale": f"1:{SCALE}", "frozen_inputs": {os.path.relpath(p, ROOT): h for p, h in FROZEN.items()},
       "parameters": dict(D_SKIN_m=D_SKIN, EDGE_INSET_m=EDGE_INSET, STEEP_NZ=STEEP_NZ, CLASS_TOL_m=CLASS_TOL, TERRAIN_TOL_m=TERRAIN_TOL),
       "site_operands": len(SITE_OPS), "warnings": []}
print(f"[v004] site operands rebuilt: {len(SITE_OPS)}  ({time.time()-T0:.1f}s)")

# ------------------------------------------------------------------ the approved site base, verbatim from the v003 3MF
NS = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
def threemf_parts(path):
    z = zipfile.ZipFile(path); out = []
    for name in sorted(n for n in z.namelist() if n.startswith("3D/Objects/")):
        for o in ET.fromstring(z.read(name)).findall("m:resources/m:object", NS):
            co = np.array([[float(v.get(a)) for a in "xyz"] for v in o.findall("m:mesh/m:vertices/m:vertex", NS)])
            tv = np.array([[int(t.get(a)) for a in ("v1", "v2", "v3")] for t in o.findall("m:mesh/m:triangles/m:triangle", NS)], dtype=np.int64)
            out.append((co, tv))
    return out
(BASE_MM, BASE_TV), = threemf_parts(V003_SITE_3MF)
BASE_CO = BASE_MM / K                                                    # real metres, model space
with bpy.data.libraries.load(V003_BLEND, link=False) as (src_, dst_):
    dst_.objects = ["PRINT_site_base"]
v3 = dst_.objects[0]; v3co = np.array([v3.matrix_world @ v.co for v in v3.data.vertices])
assert v3co.shape == BASE_CO.shape and np.abs(v3co - BASE_CO).max() < 1e-5, "v003 site base (blend) differs from the v003 3MF mesh"
bpy.data.objects.remove(v3, do_unlink=True)

G["terrain"].name = "O_site_terrain_operand"               # v003 named its terrain operand PRINT_site_base
ROOTC = bpy.data.collections.new("PRINT_v004"); bpy.context.scene.collection.children.link(ROOTC)
C_SITE = bpy.data.collections.new("PRINT_SITE_BASE"); ROOTC.children.link(C_SITE)
me = bpy.data.meshes.new("PRINT_site_base_mesh"); me.from_pydata(BASE_CO.tolist(), [], BASE_TV.tolist()); me.update()
BASE = bpy.data.objects.new("PRINT_site_base", me); C_SITE.objects.link(BASE)
BASE_BVH = BVHTree.FromPolygons(BASE_CO.tolist(), BASE_TV.tolist())
A_, B_, C_ = BASE_CO[BASE_TV[:, 0]], BASE_CO[BASE_TV[:, 1]], BASE_CO[BASE_TV[:, 2]]
NR = np.cross(B_ - A_, C_ - A_); AR = np.linalg.norm(NR, axis=1) / 2; NR = NR / np.maximum(2 * AR, 1e-30)[:, None]
CEN = (A_ + B_ + C_) / 3
LOG["base"] = dict(triangles=int(len(BASE_TV)), vertices=int(len(BASE_CO)), bbox_min_m=BASE_CO.min(0).round(4).tolist(),
                   bbox_max_m=BASE_CO.max(0).round(4).tolist(), size_mm=((BASE_CO.max(0) - BASE_CO.min(0)) * K).round(3).tolist())

# ------------------------------------------------------------------ documented colour of every source surface
def site_colour(mat):
    if mat in ("SITE_existing_asphalt", "SITE_plaza_Techo-Bloc_Westmount_Onyx") or mat.startswith("MTL-1"):
        return "BLACK"
    if mat in ("SITE_lawn_ground_shape_no_planting", "SITE_landscape_bed_ground_shape", "LAND_lawn", "LAND_mulch_bed_surface",
               "SITE_entrance_bed_mulch"):
        return "GREEN"
    return "GRAY"    # concrete flatwork, Shale Gray pavers, brick / caps / CMU, bollards, poles, lenses, HM doors, undetailed plaza
VEG_OPS = [o for o in G["site_parts"] if o.name.startswith("P_LAND_") and o.get("src", "") in G["VEG"]]
TREE_OPS = [o for o in G["site_parts"] if o.name == "P_tree_SANJ_canopy"]
PLANT_OPS = VEG_OPS + TREE_OPS
def priority(o):            # coincident sources (a walk top flush with the grade): the more specific one shows
    s = o.get("src", "")
    if o in PLANT_OPS: return 1
    if s.startswith(("DET_Bollard", "DET_Light", "FD_HM")) or o.name == "P_tree_SANJ_trunk": return 2
    if s.startswith("DET_Curb"): return 3
    if s.startswith("Yard_"): return 4
    if s.startswith("LAND_"): return 5
    if s == G["TERRAIN"]: return 7
    return 6
V, F, LAB = [], [], []
for o in SITE_OPS:
    s = o.get("src", ""); so = bpy.data.objects.get(s)
    if so is not None and so.type == "MESH":
        # the operand copies lost their material slots: read each face's material from the v023 source face it lies on
        Mw = so.matrix_world; slots = [sl.material.name if sl.material else "NONE" for sl in so.material_slots]
        sb = BVHTree.FromPolygons([tuple(Mw @ v.co) for v in so.data.vertices], [tuple(p.vertices) for p in so.data.polygons])
        smi = [p.material_index for p in so.data.polygons]
    off = len(V); V.extend(map(tuple, getco(o))); pr = priority(o)
    for p in o.data.polygons:
        F.append(tuple(i + off for i in p.vertices))
        if o in PLANT_OPS or s.startswith("LAND_"):
            c, m_ = "GREEN", ("planting (simplified plant)" if o in PLANT_OPS else s)
        elif so is None or so.type != "MESH":
            c, m_ = "GRAY", "tree trunk (print addition)"
        else:
            j = sb.find_nearest(p.center)[2]
            m_ = slots[smi[j]] if j is not None and smi[j] < len(slots) else (slots[0] if slots else "NONE")
            c = site_colour(m_)
        LAB.append((c, pr, s or o.name, tuple(p.normal), m_))
OPS_BVH = BVHTree.FromPolygons(V, F)
TER = bpy.data.objects[G["TERRAIN"]]; Mt = TER.matrix_world
TER_BVH = BVHTree.FromPolygons([tuple(Mt @ v.co) for v in TER.data.vertices], [tuple(p.vertices) for p in TER.data.polygons])
TER_MAT = [TER.material_slots[p.material_index].material.name for p in TER.data.polygons]

CLS = np.array(["GRAY"] * len(BASE_TV), dtype=object); SRC = [""] * len(BASE_TV); MAT = [""] * len(BASE_TV); HOW = Counter()
for i in range(len(BASE_TV)):
    best = None
    for loc, n_, idx, dist in OPS_BVH.find_nearest_range(Vector(CEN[i]), CLASS_TOL):
        c, pr, s, nn, m_ = LAB[idx]
        if float(np.dot(nn, NR[i])) < 0.8:
            continue
        if best is None or pr < best[1] or (pr == best[1] and dist < best[3]):
            best = (c, pr, s, dist, m_)
    if NR[i, 2] < -STEEP_NZ:
        HOW["underside (never coloured) -> gray"] += 1; SRC[i] = "(underside)"; continue
    if best is None and NR[i, 2] > STEEP_NZ:
        # interpolated terrain only: the union re-split its non-planar quads; take the documented terrain face under / over
        for d_ in ((0, 0, -1), (0, 0, 1)):
            h = TER_BVH.ray_cast(Vector(CEN[i]) - Vector(d_) * 1e-4, Vector(d_), TERRAIN_TOL)
            if h[0] is not None:
                m_ = TER_MAT[h[2]]; best = (site_colour(m_), 7, G["TERRAIN"], h[3], m_); HOW["terrain_vertical_lookup"] += 1; break
    if best is None:
        HOW["unmatched (cut faces: crop sides, underside, pocket, sockets, rib clearances) -> gray"] += 1
        SRC[i] = "(cut face)"; continue
    HOW["matched_source_surface"] += 1
    CLS[i], SRC[i], MAT[i] = best[0], best[2], best[4]
by_mat = defaultdict(lambda: [0, 0.0])
for i in range(len(BASE_TV)):
    k = (CLS[i], MAT[i] or SRC[i]); by_mat[k][0] += 1; by_mat[k][1] += float(AR[i])
LOG["classification"] = dict(how=dict(HOW), by_colour_and_material={f"{c} | {m}": dict(tris=n, area_m2=round(a, 2))
                                                                    for (c, m), (n, a) in sorted(by_mat.items(), key=lambda kv: -kv[1][1])})
print(f"[v004] classified {len(BASE_TV)} base triangles {dict(HOW)}  ({time.time()-T0:.1f}s)")

# ------------------------------------------------------------------ inside tests against the approved base
BASE_TRI = BASE_CO[BASE_TV]
def _parity_inside(p, d=(0.000173, 0.000231, 1.0)):
    d = Vector(d).normalized(); o_ = Vector(p); n_ = 0
    for _ in range(200):
        h = BASE_BVH.ray_cast(o_, d, 500.0)
        if h[0] is None:
            break
        n_ += 1; o_ = h[0] + d * 1e-5
    return n_ % 2 == 1
def outside_points(pts, tol=0.005):
    """indices of points farther than tol from the base surface AND outside it. Fast ray-parity pre-test; every point it
    calls outside is confirmed with the generalized winding number (< 0.5 = outside, v003 rule; ray parity can miscount
    where a ray runs through a mesh vertex or edge)"""
    far = [k for k, p in enumerate(pts) if (lambda r: r[3] is not None and r[3] > tol)(BASE_BVH.find_nearest(Vector(p)))]
    sus = [k for k in far if not _parity_inside(pts[k])]
    if not sus:
        return []
    w = G["winding"](BASE_TRI, np.array([pts[k] for k in sus]))
    return [k for k, wk in zip(sus, w) if wk < 0.5]
def depth_below(p, direction, cap):
    h = BASE_BVH.ray_cast(Vector(p) + Vector(direction) * 1e-4, Vector(direction), cap + 1.0)
    return cap if h[0] is None else min(cap, max(0.0, (h[0] - Vector(p)).length - 0.002))

# ------------------------------------------------------------------ colour skins
def mesh_obj(name, Vs, Fs):
    m = bpy.data.meshes.new(name + "_mesh"); m.from_pydata(Vs, [], Fs); m.update()
    o = bpy.data.objects.new(name, m); WORK.objects.link(o); return o
GUARD = []
def guard(o):
    """a colour piece must lie inside the approved base; a piece with any vertex or face centre outside (a plant cut by
    the crop, the pocket clearance or a socket) is intersected with a COPY of the base (the base itself is never cut)"""
    me_ = o.data; pts = [np.array(v.co) for v in me_.vertices] + [np.array(p.center) for p in me_.polygons]
    if not outside_points(pts):
        return o
    G["COLOUR_STAGE"] = True
    bc = bpy.data.objects.new(o.name + "_basecopy", BASE.data.copy()); WORK.objects.link(bc)
    v0 = metrics(o)["volume_m3"]
    m = boolean(o, [bc], "INTERSECT", f"guard_{o.name}", allow_noop=True, unzip=True)
    G["COLOUR_STAGE"] = False
    ok = m["tris"] > 0 and m["volume_m3"] > 1e-9 and solid_ok(m) and not outside_points([np.array(v.co) for v in o.data.vertices])
    GUARD.append(dict(piece=o.get("src", o.name), volume_before_m3=round(v0, 6), volume_after_m3=round(m["volume_m3"], 6), kept=ok))
    if not ok:
        bpy.data.objects.remove(o, do_unlink=True); return None
    return o

X0, X1 = float(BASE_CO[:, 0].min()) + EDGE_INSET, float(BASE_CO[:, 0].max()) - EDGE_INSET
Y0, Y1 = float(BASE_CO[:, 1].min()) + EDGE_INSET, float(BASE_CO[:, 1].max()) - EDGE_INSET
EDGE_LOG = Counter()
WHOLE_PLANTS = []
for o in PLANT_OPS:                                                      # whole simplified plants (the exact base operands)
    o["src"] = o.get("src", o.name)
    o2 = guard(o)
    if o2 is not None:
        co_ = getco(o2)
        if co_[:, 0].min() < X0 or co_[:, 0].max() > X1 or co_[:, 1].min() < Y0 or co_[:, 1].max() > Y1:
            # a plant cut by the crop edge: keep the base's edge gray (same 0.5 mm inset as the skins)
            G["COLOUR_STAGE"] = True
            bx = G["make_box"](o2.name + "_inset", X0, X1, Y0, Y1, float(co_[:, 2].min()) - 1.0, float(co_[:, 2].max()) + 1.0)
            m = boolean(o2, [bx], "INTERSECT", f"inset_{o2.name}", allow_noop=True, unzip=True)
            G["COLOUR_STAGE"] = False
            EDGE_LOG["plant clipped at the edge band"] += 1
            if m["tris"] == 0 or m["volume_m3"] < 1e-9 or not solid_ok(m):
                bpy.data.objects.remove(o2, do_unlink=True); EDGE_LOG["plant entirely in the edge band"] += 1; continue
        G["triangulate"](o2); m = metrics(o2)
        if not solid_ok(m):
            # a plant cut by the pocket into lumps that touch along an edge: colour its visible faces as skins instead
            GUARD.append(dict(piece=o2.get("src", o2.name), fallback="surface skins (pinched after clipping)", metrics=m))
            bpy.data.objects.remove(o2, do_unlink=True); continue
        WHOLE_PLANTS.append(o2)
PLANT_SRCS = {o.get("src", "") for o in WHOLE_PLANTS}      # plants not kept whole fall back to surface skins
skin_V = {"GREEN": [], "BLACK": []}; skin_F = {"GREEN": [], "BLACK": []}
SKIN_LOG = defaultdict(lambda: dict(prisms=0, area_m2=0.0, depth_limited=0, dropped_no_thickness=0, steep=0))
def add_prism(c, top, bot):
    """closed prism between the convex polygon 'top' (outward = up / out of the base) and its swept copy 'bot'"""
    n = len(top); off = len(skin_V[c]); skin_V[c].extend(map(tuple, top)); skin_V[c].extend(map(tuple, bot))
    skin_F[c].append(tuple(off + k for k in range(n))); skin_F[c].append(tuple(off + n + k for k in reversed(range(n))))
    for a in range(n):
        b = (a + 1) % n
        skin_F[c].append((off + a, off + n + a, off + n + b, off + b))
def clip_to_inset(poly, nrm):
    """Sutherland-Hodgman clip of a planar polygon (in its plane) to the inset rectangle X0..X1 x Y0..Y1"""
    for ax, lim, keep_lo in ((0, X0, False), (0, X1, True), (1, Y0, False), (1, Y1, True)):
        out = []
        for k in range(len(poly)):
            p, q = poly[k], poly[(k + 1) % len(poly)]
            pin = p[ax] <= lim if keep_lo else p[ax] >= lim
            qin = q[ax] <= lim if keep_lo else q[ax] >= lim
            if pin:
                out.append(p)
            if pin != qin:
                t = (lim - p[ax]) / (q[ax] - p[ax]); out.append(p + (q - p) * t)
        poly = out
        if len(poly) < 3:
            return None
    return np.array(poly)
for i in range(len(BASE_TV)):
    c = CLS[i]
    if c not in skin_V or SRC[i] in PLANT_SRCS or AR[i] < 1e-8:
        continue                                                         # plants are added whole (below)
    L = SKIN_LOG[c]; tri = BASE_CO[BASE_TV[i]]
    if NR[i, 2] > STEEP_NZ:
        dirn = np.array([0.0, 0.0, -1.0])
    elif NR[i, 2] > -STEEP_NZ:
        dirn = -NR[i]; L["steep"] += 1
    else:
        continue                                                         # undersides are not seen
    top = tri
    if tri[:, 0].min() < X0 or tri[:, 0].max() > X1 or tri[:, 1].min() < Y0 or tri[:, 1].max() > Y1:
        if dirn[2] != -1.0:
            EDGE_LOG["steep face in the edge band dropped"] += 1; continue
        top = clip_to_inset(list(tri), NR[i])
        if top is None or len(top) < 3:
            EDGE_LOG["face entirely in the edge band"] += 1; continue
        EDGE_LOG["face clipped at the edge band"] += 1
    cen = top.mean(0)
    probes = [cen] + [v + (cen - v) * 0.05 for v in top]
    dep = min(depth_below(p, dirn, D_SKIN) for p in probes)
    if dep < 0.01:
        L["dropped_no_thickness"] += 1; continue
    L["depth_limited"] += dep < D_SKIN - 1e-6
    add_prism(c, top, top + dirn * dep); L["prisms"] += 1; L["area_m2"] += float(AR[i])
LOG["skins"] = {c: dict(v, area_m2=round(v["area_m2"], 2)) for c, v in SKIN_LOG.items()}

parts = {"GREEN": list(WHOLE_PLANTS), "BLACK": []}
for c in parts:
    if skin_F[c]:
        parts[c].append(mesh_obj(f"skins_{c}", skin_V[c], skin_F[c]))     # separate prisms, outward by construction

# skins are checked prism by prism (vertices + face centres)
for c, objs in parts.items():
    for o in objs:
        if o.name.startswith("skins_"):
            co_ = getco(o); bad = outside_points(list(co_) + [np.array(p.center) for p in o.data.polygons])
            allp = list(co_) + [np.array(p.center) for p in o.data.polygons]
            dist = [BASE_BVH.find_nearest(Vector(allp[k]))[3] for k in bad]
            # crop-edge prisms: their outer wall lies in the crop side plane; the approved side faces deviate from that
            # plane by up to ~1 cm (0.04 mm printed) - documented tolerance 0.02 m (0.08 mm printed, below the layer height)
            LOG.setdefault("skin_outside_points", {})[c] = dict(beyond_5mm=len(bad), beyond_20mm=sum(d_ > 0.02 for d_ in dist),
                                                                 max_m=round(max(dist), 4) if dist else 0.0)
            LOG.setdefault("skin_outside_examples", {})[c] = [dict(at=np.round(allp[k], 3).tolist(), dist=round(d_, 4)) for k, d_ in zip(bad[:20], dist[:20])]
            if any(d_ > 0.02 for d_ in dist):
                LOG["warnings"].append(f"{c} skins: {sum(d_ > 0.02 for d_ in dist)} points more than 0.02 m outside the base")
LOG["plants"] = dict(shrubs=len(VEG_OPS), tree_canopy=len(TREE_OPS), kept_whole=len(WHOLE_PLANTS), guarded=GUARD)
LOG["edge_inset"] = dict(EDGE_LOG)

def join(objs, name):
    Vs, Fs = [], []
    for o in objs:
        co_ = getco(o); off = len(Vs); Vs.extend(map(tuple, co_)); Fs.extend(tuple(i + off for i in p.vertices) for p in o.data.polygons)
    m = bpy.data.meshes.new(name + "_mesh"); m.from_pydata(Vs, [], Fs); m.update()
    ob = bpy.data.objects.new(name, m); C_SITE.objects.link(ob)
    return ob
P_GREEN = join(parts["GREEN"], "PRINT_site_base_GREEN")
P_BLACK = join(parts["BLACK"], "PRINT_site_base_BLACK")

# ------------------------------------------------------------------ finalise: keep only the v004 site parts
SLOT = {"GRAY": (3, (0.50, 0.51, 0.50, 1.0)), "GREEN": (4, (0.22, 0.42, 0.20, 1.0)), "BLACK": (2, (0.06, 0.06, 0.07, 1.0))}
FINAL = [("PRINT_site_base", "GRAY", 1, "exact v003 site base (unchanged geometry) - gray; colour parts overlay it"),
         ("PRINT_site_base_GREEN", "GREEN", 2, "lawn / planting beds / shrubs / tree canopy - inside the base; later part wins"),
         ("PRINT_site_base_BLACK", "BLACK", 3, "asphalt drive + Onyx entry plaza + yard copings - inside the base; later part wins")]
for name, cname, order, note in FINAL:
    o = bpy.data.objects[name]; slot, rgba = SLOT[cname]
    mat = bpy.data.materials.get("PRINT_" + cname) or bpy.data.materials.new("PRINT_" + cname); mat.diffuse_color = rgba
    o.color = rgba; o.data.materials.clear(); o.data.materials.append(mat)
    o["filament_slot"] = slot; o["filament_colour"] = cname; o["part_order"] = order; o["note"] = note
    o["print_scale"] = f"1:{SCALE}"; o["units"] = "real-world metres; export factor 4.1667 mm per m (1000/240)"
LOG["final_parts"] = {name: metrics(bpy.data.objects[name]) for name, *_ in FINAL}
keep = {n for n, *_ in FINAL}
for o in list(bpy.data.objects):
    if o.name not in keep:
        bpy.data.objects.remove(o, do_unlink=True)
for c in list(bpy.data.collections):
    if c not in (ROOTC, C_SITE):          # by identity: the v003 code made its own PRINT_SITE_BASE collection first
        bpy.data.collections.remove(c)
ROOTC.name, C_SITE.name = "PRINT_v004", "PRINT_SITE_BASE"
bpy.data.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
bpy.context.scene["print_derivative"] = json.dumps({"version": "print_v004 (multicolor SITE BASE of the approved v003 site base)",
                                                    "companions": "v003 multicolor building, drop-off canopy and sun-shade (frozen, unchanged)",
                                                    "scale": f"1:{SCALE}", "units": "metres (real)", "built": time.strftime("%Y-%m-%d %H:%M")})
b = LOG["final_parts"]["PRINT_site_base"]
bad = [n for n in keep if n not in bpy.data.objects or C_SITE not in bpy.data.objects[n].users_collection]
if b["tris"] != len(BASE_TV) or not solid_ok(b) or b["islands"] != 1:
    bad.append("base changed or not a single closed solid")
for n in ("PRINT_site_base_GREEN", "PRINT_site_base_BLACK"):
    m = LOG["final_parts"][n]
    if m["boundary_edges"] or m["volume_m3"] <= 0:
        bad.append(f"{n}: not closed")
if any(v["beyond_20mm"] for v in LOG.get("skin_outside_points", {}).values()):
    bad.append("skin points outside the base")
LOG["save_gate_failures"] = bad; LOG["runtime_s"] = round(time.time() - T0, 1)
os.makedirs(VAL, exist_ok=True)
with open(os.path.join(VAL, "print_prep_v004_build_log.json"), "w", encoding="utf-8") as f:
    json.dump(LOG, f, indent=1, default=lambda x: x.tolist() if hasattr(x, "tolist") else str(x))
if bad:
    raise SystemExit(f"[v004] NOT SAVED - save gate: {bad}")
bpy.context.preferences.filepaths.save_version = 0
bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND, compress=True)
print(f"[v004] saved {OUT_BLEND} in {time.time()-T0:.1f}s")
