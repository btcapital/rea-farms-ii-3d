"""Building II 3D-print derivative v002 - GEOMETRY PREPARATION at 1:240 (owner-directed revision 2026-09-25).

Run (background Blender 5.2, from the project root):
  blender -b models/Building_II/print_derivatives/building_II_print_v002.blend \
          --python scripts/3d_print/build_print_v002.py

Input : building_II_print_v002.blend as a PRISTINE copy of the audit copy (byte-identical to the frozen v023).
Output: the same v002 file with ONLY the four print parts (collection PRINT_v002), + print_prep_v002_build_log.json.
v002 = v001 method + lessons from the physical v001 coupon print:
  * revised site crop (red-box design intent) and uniform scale 1:240 (1 in = 20 ft) for all four parts
  * conservative minimums: ribs 0.70 mm, free-standing fins/plates/bars 1.0 mm, bollards/columns 1.4 mm,
    light poles 1.9 mm, canopy beams 1.2 mm
  * fit clearances 0.50 mm (building/base pocket) and 0.40 mm (canopy sockets) + lead-in chamfers
  * porte cochere: hidden valley tie joining both glass wings, 1.2 mm beams, 1.0 mm purlins/glass, 1.4 mm columns
  * sun-shade louvers redistributed inside their documented band for >= 1.0 mm bars and 0.50 mm clear gaps
Geometry stays in REAL-WORLD METRES; the scale is applied only at export (1 m = 4.1667 mm).
"""
import bpy, bmesh, hashlib, json, math, os, time
import numpy as np
from collections import defaultdict
from mathutils import Vector
from mathutils.bvhtree import BVHTree

T0 = time.time()
V023_SHA = "7fe33f1e4dc906c75b54122203fec75ee9ef948be70897e46fcfd1b288235c91"
BLEND = bpy.data.filepath
DERIV = os.path.dirname(BLEND)
ROOT = os.path.abspath(os.path.join(DERIV, "..", "..", ".."))
ARCHIVE = os.path.join(DERIV, "archive", "building_II_print_v001_audit_copy.blend")   # pristine = v023
VAL = os.path.join(ROOT, "exports", "Building_II", "3d_print", "validation")

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

assert os.path.basename(BLEND) == "building_II_print_v002.blend", BLEND
assert sha(BLEND) == V023_SHA, "v002 is not a pristine copy of the audit copy - copy archive/building_II_print_v001_audit_copy.blend over it first"
assert os.path.exists(ARCHIVE) and sha(ARCHIVE) == V023_SHA, "verified archive audit copy is missing"

# ------------------------------------------------------------------ v002 parameters (1:240)
SCALE = 240
def pm(mm):                      # printed millimetres -> real metres
    return mm * SCALE / 1000.0
T_WALL = pm(1.0)       # free-standing wall / fin / railing / plate / bar / sun-shade member   0.240 m
T_POST = pm(1.4)       # bollards, canopy columns, tree trunk                                  0.336 m
T_POLE = pm(1.9)       # light-pole shafts                                                     0.456 m
T_POLE_BASE = pm(2.6)  # light-pole base (kept wider than the thickened shaft)                 0.624 m
T_BEAM = pm(1.2)       # porte-cochere beams (fragile junction members)                        0.288 m
T_RIB = pm(0.70)       # bonded facade relief rib (mullion face width)                         0.168 m
T_RIB_PROJ = pm(0.42)  # minimum rib projection in front of the glazing plane                  0.101 m
T_RELIEF = pm(0.3)     # raised bed / planting-area pad                                        0.072 m
CLR_POCKET = pm(0.5)   # building-to-base pocket clearance per side                            0.120 m
CLR_SOCKET = pm(0.4)   # canopy column socket clearance per side                               0.096 m
CH_BODY = pm(0.4)      # lead-in chamfer on the body foundation's bottom edge                  0.096 m
CH_COLUMN = pm(0.3)    # lead-in chamfer on the canopy column feet                             0.072 m
LEADIN = pm(0.4)       # lead-in flare at the top of each socket                               0.096 m
LOUVER_GAP = pm(0.5)   # sun-shade clear gap between louver bars                               0.120 m
PLANT_MIN_D = pm(1.5)  # minimum shrub diameter                                                0.360 m
PLANT_MIN_H = pm(1.0)  # minimum shrub height                                                  0.240 m
EMBED = 0.02           # overlap used to bond touching solids
CROP = dict(x0=-9.0, x1=67.25, y0=-5.0, y1=40.5)   # revised red-box crop (see PRINT_CONTROL.md section 21)
SOCKET_FLOOR = -0.50   # canopy column socket floor

LOG = {"script": "scripts/3d_print/build_print_v002.py", "scale": f"1:{SCALE}",
       "parameters_real_m": dict(T_WALL=T_WALL, T_POST=T_POST, T_POLE=T_POLE, T_RIB=T_RIB, T_RELIEF=T_RELIEF,
                                 CLR_POCKET=CLR_POCKET, CLR_SOCKET=CLR_SOCKET, PLANT_MIN_D=PLANT_MIN_D,
                                 PLANT_MIN_H=PLANT_MIN_H, EMBED=EMBED, T_RIB_PROJ=T_RIB_PROJ, T_POLE_BASE=T_POLE_BASE,
                                 T_BEAM=T_BEAM, CH_BODY=CH_BODY, CH_COLUMN=CH_COLUMN, LEADIN=LEADIN, LOUVER_GAP=LOUVER_GAP, SOCKET_FLOOR=SOCKET_FLOOR),
       "crop_window_m": CROP, "classes": {}, "omitted": {}, "warnings": [], "booleans": []}
def log_class(key, **kw):
    LOG["classes"].setdefault(key, {}).update(kw)

sc = bpy.context.scene
bpy.context.preferences.filepaths.save_version = 0      # no .blend1 backup next to v001

# ------------------------------------------------------------------ collections / helpers
ROOTC = bpy.data.collections.new("PRINT_v002"); sc.collection.children.link(ROOTC)
def newcol(n):
    c = bpy.data.collections.new(n); ROOTC.children.link(c); return c
C_BODY, C_SITE = newcol("PRINT_BUILDING_BODY"), newcol("PRINT_SITE_BASE")
C_CAN, C_SUN = newcol("PRINT_ADDON_DROPOFF_CANOPY"), newcol("PRINT_ADDON_SUNSHADE")
WORK = bpy.data.collections.new("PRINT_work"); sc.collection.children.link(WORK)

parent = {}
def _walk(c):
    for ch in c.children:
        parent[ch.name] = c.name; _walk(ch)
_walk(sc.collection)
def colls_of(o):
    out = set()
    for c in o.users_collection:
        n = c.name
        out.add(n)
        while n in parent:
            n = parent[n]; out.add(n)
    return out
def in_coll(cname):
    return sorted(o.name for o in bpy.data.objects if o.type == "MESH" and cname in colls_of(o))

DG = bpy.context.evaluated_depsgraph_get()
def wcopy(name, new=None, coll=WORK):
    src = bpy.data.objects[name]
    me = bpy.data.meshes.new_from_object(src.evaluated_get(DG))
    me.transform(src.matrix_world)
    me.materials.clear()
    ob = bpy.data.objects.new(new or ("P_" + name), me)
    coll.objects.link(ob)
    ob["src"] = name
    return ob

def getco(ob):
    a = np.empty(len(ob.data.vertices) * 3); ob.data.vertices.foreach_get("co", a); return a.reshape(-1, 3)
def setco(ob, co):
    ob.data.vertices.foreach_set("co", np.ascontiguousarray(co, dtype=np.float64).ravel()); ob.data.update()

def thin_dir(ob, ncand=24):
    me = ob.data; n = len(me.polygons)
    nr = np.empty(n * 3); me.polygons.foreach_get("normal", nr); nr = nr.reshape(-1, 3)
    ar = np.empty(n); me.polygons.foreach_get("area", ar)
    co = getco(ob)
    key = np.round(np.abs(nr), 3)
    _, first, inv = np.unique(key, axis=0, return_index=True, return_inverse=True); inv = inv.ravel()
    w = np.bincount(inv, weights=ar)
    best = (None, 1e9)
    for k in np.argsort(-w)[:ncand]:
        d = nr[first[k]] / np.linalg.norm(nr[first[k]])
        pr = co @ d; t = float(pr.max() - pr.min())
        if t < best[1]:
            best = (d, t)
    return best

def thicken(ob, target, keep="center", ref=None):
    """Thicken a two-plane solid (box / plate / bar) along its thinnest normal to `target`."""
    d, t = thin_dir(ob)
    if t >= target - 1e-6:
        return t, t
    if keep == "top" and d[2] < 0:
        d = -d
    co = getco(ob); pr = co @ d; lo, hi = pr.min(), pr.max(); mid = (lo + hi) / 2
    if np.max(np.minimum(abs(pr - lo), abs(pr - hi))) > 1e-3:
        raise RuntimeError(f"{ob.name}: not a two-plane solid along its thin axis")
    H = pr > mid; delta = target - t
    if keep == "center":
        a_lo = a_hi = delta / 2
    elif keep == "top":
        a_lo, a_hi = delta, 0.0
    elif keep == "outer":
        r = np.asarray(ref[:2], float)
        outer_hi = np.linalg.norm(co[H, :2].mean(0) - r) > np.linalg.norm(co[~H, :2].mean(0) - r)
        a_lo, a_hi = (delta, 0.0) if outer_hi else (0.0, delta)
    else:
        raise ValueError(keep)
    co[~H] -= d * a_lo; co[H] += d * a_hi
    setco(ob, co)
    return t, target

def widen_axis(ob, ax, target):
    co = getco(ob); lo, hi = co[:, ax].min(), co[:, ax].max(); t = hi - lo
    if t >= target - 1e-6:
        return t, t
    H = co[:, ax] > (lo + hi) / 2; delta = target - t
    co[~H, ax] -= delta / 2; co[H, ax] += delta / 2
    setco(ob, co)
    return t, target

def is_axis_box(ob, tol=1e-4):
    co = getco(ob)
    return len(co) == 8 and all(len(np.unique(np.round(co[:, a] / tol))) == 2 for a in range(3))

def extend_bottom(ob, z):
    """Lower the bottom vertex of every vertical vertex column to z (prism-like solids only)."""
    co = getco(ob)
    key = np.round(co[:, :2], 4)
    _, inv = np.unique(key, axis=0, return_inverse=True); inv = inv.ravel()
    cnt = np.bincount(inv)
    if (cnt < 2).any():
        return False
    order = np.lexsort((co[:, 2], inv))
    firsts = order[np.r_[True, inv[order][1:] != inv[order][:-1]]]
    co[firsts, 2] = np.minimum(co[firsts, 2], z)
    setco(ob, co)
    return True

def islands(nv, ed):
    lab = np.arange(nv)
    if len(ed) == 0:
        return lab
    a, b = ed[:, 0], ed[:, 1]
    while True:
        old = lab.copy(); m = np.minimum(lab[a], lab[b])
        np.minimum.at(lab, a, m); np.minimum.at(lab, b, m); lab = lab[lab]
        if np.array_equal(lab, old):
            return lab

def metrics(ob):
    me = ob.data; me.calc_loop_triangles()
    nv, ne, nl, nt = len(me.vertices), len(me.edges), len(me.loops), len(me.loop_triangles)
    co = getco(ob)
    ed = np.empty(ne * 2, dtype=np.int64); me.edges.foreach_get("vertices", ed); ed = ed.reshape(-1, 2)
    lv = np.empty(nl, dtype=np.int64); me.loops.foreach_get("vertex_index", lv)
    le = np.empty(nl, dtype=np.int64); me.loops.foreach_get("edge_index", le)
    fpe = np.bincount(le, minlength=ne)
    sign = np.where(lv == ed[le, 0], 1, -1); ssum = np.bincount(le, weights=sign, minlength=ne)
    tv = np.empty(nt * 3, dtype=np.int64); me.loop_triangles.foreach_get("vertices", tv); tv = tv.reshape(-1, 3)
    p0, p1, p2 = co[tv[:, 0]], co[tv[:, 1]], co[tv[:, 2]]
    vol = float(np.einsum("ij,ij->i", p0, np.cross(p1, p2)).sum() / 6.0) if nt else 0.0
    used = np.zeros(nv, bool); used[ed.ravel()] = True
    lab = islands(nv, ed)
    return dict(verts=nv, tris=nt, boundary_edges=int((fpe == 1).sum()), nonmanifold_edges=int((fpe > 2).sum()),
                wire_edges=int((fpe == 0).sum()), flipped_edges=int(((fpe == 2) & (np.abs(ssum) == 2)).sum()),
                islands=int(len(np.unique(lab[used]))) if used.any() else 0, loose_verts=int((~used).sum()),
                volume_m3=vol, bbox_min=co.min(0).tolist() if nv else None, bbox_max=co.max(0).tolist() if nv else None)
def solid_ok(m):
    return m["boundary_edges"] == 0 and m["nonmanifold_edges"] == 0 and m["flipped_edges"] == 0 and m["volume_m3"] > 0

def fix_solid(ob):
    """Merge coincident vertices, recalc outward normals. Returns metrics."""
    bm = bmesh.new(); bm.from_mesh(ob.data)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(ob.data); bm.free(); ob.data.update()
    m = metrics(ob)
    if m["volume_m3"] < 0:
        bm = bmesh.new(); bm.from_mesh(ob.data); bmesh.ops.reverse_faces(bm, faces=bm.faces)
        bm.to_mesh(ob.data); bm.free(); ob.data.update(); m = metrics(ob)
    return m

def boolean(target, operands, op, label):
    bad = [o.name for o in operands + [target] if not solid_ok(metrics(o))]
    if bad:
        raise SystemExit(f"[build] {label}: non-watertight boolean inputs {bad[:10]} - not saved")
    before = metrics(target)
    tmp = bpy.data.collections.new(f"tmp_{label}"); sc.collection.children.link(tmp)
    for o in operands:
        for c in list(o.users_collection):
            c.objects.unlink(o)
        tmp.objects.link(o)
    mod = target.modifiers.new("b", "BOOLEAN"); mod.operation = op
    mod.operand_type = "COLLECTION"; mod.collection = tmp; mod.solver = "MANIFOLD"
    t = time.time()
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(target.evaluated_get(dg))
    target.modifiers.remove(mod)
    old = target.data; target.data = me; bpy.data.meshes.remove(old)
    for o in list(tmp.objects):
        m_ = o.data; bpy.data.objects.remove(o); bpy.data.meshes.remove(m_)
    bpy.data.collections.remove(tmp)
    m = metrics(target)
    if m["verts"] == before["verts"] and abs(m["volume_m3"] - before["volume_m3"]) < 1e-9:
        raise SystemExit(f"[build] {label}: boolean had no effect (solver refused?) - not saved")
    LOG["booleans"].append(dict(label=label, op=op, operands=len(operands), seconds=round(time.time() - t, 2),
                                result_tris=m["tris"], islands=m["islands"], watertight=solid_ok(m)))
    return m

def make_mesh(name, bm, coll=WORK):
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); coll.objects.link(ob)
    return ob

def make_box(name, x0, x1, y0, y1, z0, z1, coll=WORK):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = Vector((x0 if v.co.x < 0 else x1, y0 if v.co.y < 0 else y1, z0 if v.co.z < 0 else z1))
    return make_mesh(name, bm, coll)

def make_prism(name, pts, z0, z1, coll=WORK):
    bm = bmesh.new()
    vb = [bm.verts.new((x, y, z0)) for x, y in pts]; vt = [bm.verts.new((x, y, z1)) for x, y in pts]
    n = len(pts)
    bm.faces.new(vb[::-1]); bm.faces.new(vt)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new((vb[i], vb[j], vt[j], vt[i]))
    return make_mesh(name, bm, coll)

def make_loft(name, rings, coll=WORK):
    """rings = [(pts2d, z), ...] bottom -> top, equal vertex counts; capped at both ends."""
    bm = bmesh.new()
    vs = [[bm.verts.new((x, y, z)) for x, y in pts] for pts, z in rings]
    n = len(vs[0])
    bm.faces.new(vs[0][::-1]); bm.faces.new(vs[-1])
    for k in range(len(vs) - 1):
        for i in range(n):
            j = (i + 1) % n
            bm.faces.new((vs[k][i], vs[k][j], vs[k + 1][j], vs[k + 1][i]))
    return make_mesh(name, bm, coll)

def rect(x0, x1, y0, y1, d=0.0):
    return [(x0 - d, y0 - d), (x1 + d, y0 - d), (x1 + d, y1 + d), (x0 - d, y1 + d)]

def make_lathe(name, cx, cy, profile, seg=16, coll=WORK):
    """profile = [(r, z), ...] bottom -> top; first ring is capped, last point must have r = 0 (apex)."""
    bm = bmesh.new(); rings = []
    for r, z in profile[:-1]:
        rings.append([bm.verts.new((cx + r * math.cos(2 * math.pi * i / seg), cy + r * math.sin(2 * math.pi * i / seg), z))
                      for i in range(seg)])
    apex = bm.verts.new((cx, cy, profile[-1][1]))
    bm.faces.new(rings[0][::-1])
    for k in range(len(rings) - 1):
        for i in range(seg):
            j = (i + 1) % seg
            bm.faces.new((rings[k][i], rings[k][j], rings[k + 1][j], rings[k + 1][i]))
    for i in range(seg):
        bm.faces.new((rings[-1][i], rings[-1][(i + 1) % seg], apex))
    return make_mesh(name, bm, coll)

def dome_profile(zg, r, h, embed=0.10, rings=4):
    prof = [(r, zg - embed)]
    for k in range(rings):
        a = (math.pi / 2) * k / rings
        prof.append((r * math.cos(a), zg + h * math.sin(a)))
    prof.append((0.0, zg + h))
    return prof

def bvh_of(obs):
    V, F, off = [], [], 0
    for o in obs:
        co = getco(o); V.extend(map(tuple, co))
        F.extend(tuple(i + off for i in p.vertices) for p in o.data.polygons)
        off += len(co)
    return BVHTree.FromPolygons(V, F)

def ground_z(bvh, x, y):
    hit = bvh.ray_cast(Vector((x, y, 40.0)), Vector((0, 0, -1)), 100.0)
    return None if hit[0] is None else hit[0].z

def poly_area(P):
    P = np.asarray(P); return 0.5 * float(np.sum(P[:, 0] * np.roll(P[:, 1], -1) - np.roll(P[:, 0], -1) * P[:, 1]))

def offset_poly(pts, d):
    P = np.asarray(pts, float)
    if poly_area(P) < 0:
        P = P[::-1]
    keep = []
    for i in range(len(P)):
        a, b, c = P[i - 1], P[i], P[(i + 1) % len(P)]
        u, v = b - a, c - b
        if abs(u[0] * v[1] - u[1] * v[0]) > 1e-9 * (np.linalg.norm(u) * np.linalg.norm(v) + 1e-12):
            keep.append(b)
    P = np.array(keep); out = []
    for i in range(len(P)):
        a, b, c = P[i - 1], P[i], P[(i + 1) % len(P)]
        e1 = (b - a) / np.linalg.norm(b - a); e2 = (c - b) / np.linalg.norm(c - b)
        n1 = np.array([e1[1], -e1[0]]); n2 = np.array([e2[1], -e2[0]])
        p1, p2 = b + n1 * d, b + n2 * d
        t, s = np.linalg.solve(np.array([e1, -e2]).T, p2 - p1)
        out.append(p1 + t * e1)
    return [tuple(p) for p in out]

def bottom_outline(ob, zval, tol=1e-3):
    bm = bmesh.new(); bm.from_mesh(ob.data)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
    bm.normal_update()
    sel = {f for f in bm.faces if f.normal.z < -0.99 and all(abs(v.co.z - zval) < tol for v in f.verts)}
    bed = [e for e in bm.edges if sum(1 for f in e.link_faces if f in sel) == 1]
    adj = defaultdict(list)
    for e in bed:
        a, b = e.verts; adj[a].append(b); adj[b].append(a)
    assert all(len(v) == 2 for v in adj.values()), "footprint boundary is not a simple loop"
    loops, seen = [], set()
    for s in list(adj):
        if s in seen:
            continue
        loop, prev, cur = [], None, s
        while True:
            loop.append((cur.co.x, cur.co.y)); seen.add(cur)
            nxt = adj[cur][0] if adj[cur][0] is not prev else adj[cur][1]
            prev, cur = cur, nxt
            if cur is s:
                break
        loops.append(loop)
    bm.free()
    loops.sort(key=lambda L: -abs(poly_area(L)))
    return loops

# ------------------------------------------------------------------ source classification
MASSES = in_coll("01_Masses")
PARAPETS = in_coll("02_Parapets")
GLAZING = in_coll("03_Opening_panels")
CANOPY_SRC = in_coll("04_DropOff_Canopy")
DOOR_CANOPIES = in_coll("05_Door_Side_Canopies")
SUNSHADE_SRC = in_coll("06_SunShade")
RAILS = in_coll("07_Glass_Railings")
YARD = in_coll("08_Utility_Yard")
SITE09 = in_coll("09_Site_context")
FD = in_coll("11_Facade_Detail_v004")
LAND = in_coll("12_Landscape_v008")
DET = in_coll("15_Site_Detail_v013")
CUTTERS = in_coll("zz_Cutters")
def mats(n):
    return " ".join(s.material.name for s in bpy.data.objects[n].material_slots if s.material)
VEG = [n for n in LAND if "VEG_" in mats(n)]
BEDS = [n for n in LAND if n not in VEG]
FD_SPANDREL = [n for n in FD if "spandrel" in n]
FD_HM = [n for n in FD if "HM_door" in n]
FD_RIBS = [n for n in FD if n not in FD_SPANDREL and n not in FD_HM]
HM_IN_YARD = ["FD_HM_door_001A", "FD_HM_door_001B"]
HM_FLUSH = [n for n in FD_HM if n not in HM_IN_YARD]
TERRAIN = "Site_Terrain_INTERPOLATED"
SKIRT = "Site_Foundation_skirt_podium"
HARDSCAPE = [n for n in SITE09 if n not in (TERRAIN, SKIRT, "Site_North_arrow")]
BOLLARDS = [n for n in DET if n.startswith("DET_Bollard") and not n.endswith("_lens")]
LENSES = [n for n in DET if n.endswith("_lens")]
POLES = [n for n in DET if n.startswith("DET_Light_pole") and n.count("_") == 3]
POLE_BASES = [n for n in DET if n.endswith("_base")]
LUMINAIRES = [n for n in DET if n.endswith("_luminaire")]
CURBS = [n for n in DET if n.startswith("DET_Curb") and "_ctx_" not in n]
OMIT_DET = {"parking striping (zero-thickness paint lines)": [n for n in DET if "Striping" in n],
            "concrete control joints (zero-thickness lines)": [n for n in DET if "Joint" in n],
            "area drains (flush 1 ft grates, 1.2 mm, no relief)": [n for n in DET if "Area_drain" in n],
            "door pulls / levers (sub-0.2 mm hardware)": [n for n in DET if "Door_pull" in n or "Door_lever" in n],
            "context parking curbs (outside crop window)": [n for n in DET if "_ctx_" in n]}
for k, v in OMIT_DET.items():
    LOG["omitted"][k] = v
LOG["omitted"]["glazing panes (represented as recessed openings)"] = GLAZING + FD_SPANDREL
LOG["omitted"]["hollow-metal door leaves flush with wall faces (<= 0.1 mm relief)"] = HM_FLUSH
LOG["omitted"]["north arrow (presentation marker)"] = ["Site_North_arrow"]
LOG["omitted"]["whole collections"] = ["14_Context_v011 (Building I mass, streets, sidewalks, 7 street trees + 3 parking-island trees inside the window, horizon)",
                                       "13_Presentation_v010", "zz_Cutters", "10_Cameras_Lights", "all Building_II interior / lobby / tenant collections"]

def wbox(n):
    o = bpy.data.objects[n]
    co = np.array([o.matrix_world @ v.co for v in o.data.vertices])
    return co.min(0), co.max(0)

print(f"[build] classified in {time.time()-T0:.1f}s")

# ================================================================== BUILDING BODY
body_parts = []
podium = wcopy("L1_Podium", "PRINT_building_body", C_BODY)
for n in MASSES:
    if n != "L1_Podium":
        body_parts.append(wcopy(n))
Z_FFE_BOTTOM = float(getco(podium)[:, 2].min())                       # -0.552
Z_FOUND = float(wbox(SKIRT)[0][2])                                     # -2.438
loops = bottom_outline(podium, Z_FFE_BOTTOM)
FOOT = loops[0]
sk = wcopy(SKIRT, "tmp_skirt")
skirt_loops = bottom_outline(sk, Z_FOUND)
skm = sk.data; bpy.data.objects.remove(sk); bpy.data.meshes.remove(skm)
FOOT_FULL = offset_poly(FOOT, 0.0)
FOOT_IN = offset_poly(FOOT, -CH_BODY)
def _simple(poly):
    P = np.asarray(poly); n = len(P)
    def inter(a, b, c, d):
        def o(p, q, r): return np.sign((q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0]))
        return o(a, b, c) != o(a, b, d) and o(c, d, a) != o(c, d, b)
    for i in range(n):
        for j in range(i + 2, n):
            if i == 0 and j == n - 1: continue
            if inter(P[i], P[(i + 1) % n], P[j], P[(j + 1) % n]): return False
    return True
chamfer_ok = len(FOOT_IN) == len(FOOT_FULL) and _simple(FOOT_IN) and abs(poly_area(FOOT_IN)) < abs(poly_area(FOOT_FULL))
if chamfer_ok:
    foundation = make_loft("P_foundation", [(FOOT_IN, Z_FOUND), (FOOT_FULL, Z_FOUND + CH_BODY), (FOOT_FULL, Z_FFE_BOTTOM + EMBED)])
else:
    foundation = make_prism("P_foundation", FOOT, Z_FOUND, Z_FFE_BOTTOM + EMBED)
    LOG["warnings"].append("foundation lead-in chamfer skipped (inset outline not simple)")
body_parts.append(foundation)
log_class("foundation", lead_in_chamfer_m=CH_BODY if chamfer_ok else 0.0,
          lead_in_note="45-degree chamfer on the bottom perimeter edge of the foundation (hidden inside the pocket) - guides the body into the pocket and absorbs elephant's foot")
log_class("foundation", source=SKIRT, treatment="extruded from the L1_Podium bottom outline (excludes the lobby-entrance notch) from the skirt bottom to FFE-level podium underside",
          podium_outline_area_m2=round(abs(poly_area(FOOT)), 3), skirt_outline_area_m2=round(abs(poly_area(skirt_loops[0])), 3),
          outline_loops=len(loops), z_bottom=Z_FOUND)

# parapets: thicken toward the roof they belong to
ref_of = {}
for n in MASSES:
    a, b = wbox(n); ref_of[n] = ((a + b) / 2)[:2]
def par_ref(n):
    if "HighBlock" in n: return ref_of["L2_HighBlock"]
    if "LobbyBlock" in n: return ref_of["L2_LobbyBlock"]
    if "LowRoof" in n: return ref_of["L2_LowRoof"]
    return ref_of["L1_Podium"]
par_log = []
PARAPET_EXEMPT = {"Par_HighBlock_edge03": "0.49 m long 45-degree chamfer segment bonded at both ends to 0.34 m parapets; "
                                          "thickening it pushes its ends past the neighbours (0.008 m sliver) - kept at documented 0.164 m (0.68 mm at 1:240); "
                                          "not free-standing (2 mm long, bonded both ends)"}
for n in PARAPETS:
    o = wcopy(n)
    if n in PARAPET_EXEMPT:
        t = thin_dir(o)[1]; before, after = t, t
    else:
        before, after = thicken(o, T_WALL, "outer", par_ref(n))
    par_log.append((n, round(before, 4), round(after, 4))); body_parts.append(o)
log_class("parapets", count=len(PARAPETS), thickened=[p for p in par_log if p[1] != p[2]],
          min_before_m=min(p[1] for p in par_log), min_after_m=min(p[2] for p in par_log),
          rule="thickened only where < 1.0 mm printed, toward the roof (outer face kept)", exempt=PARAPET_EXEMPT)

# facade relief: mullions / frames / door-bay panels extended back to the pocket back, widened to T_RIB
cut = {n: wbox(n) for n in CUTTERS}
CENTER = ref_of["L1_Podium"]
openings = {}
for n, (a, b) in cut.items():
    ext = b - a; ax = int(np.argmin(ext[:2]))
    back_is_min = abs(a[ax] - CENTER[ax]) < abs(b[ax] - CENTER[ax])
    openings[n] = dict(min=a.tolist(), max=b.tolist(), axis=ax, back=float(a[ax] if back_is_min else b[ax]),
                       out_sign=1 if back_is_min else -1)
def cutter_for(a, b):
    c = (a + b) / 2
    cands = [k for k, (ca, cb) in cut.items() if np.all(c >= ca - 0.05) and np.all(c <= cb + 0.05)]
    return min(cands, key=lambda k: float(np.prod(cut[k][1] - cut[k][0]))) if cands else None
NW_X0 = float(cut["CUT_00_N"][0][0]); NW_Y1 = float(cut["CUT_21_W"][1][1])   # west / north facade planes at the NW corner
CLAMPED = []
LOW_RIBS = []   # facade relief that reaches grade (lobby storefront sits in the footprint notch)
rib_log = defaultdict(lambda: dict(count=0, face_before=[], face_after=[], relief=[]))
unmatched = []
for n in FD_RIBS:
    o = wcopy(n)
    a, b = wbox(n); k = cutter_for(a, b)
    if k is None or not is_axis_box(o):
        unmatched.append(n); t0, t1 = thicken(o, T_RIB, "center"); body_parts.append(o); continue
    op = openings[k]; ax, s = op["axis"], op["out_sign"]
    co = getco(o)
    inner = (co[:, ax] * s) < ((co[:, ax].min() + co[:, ax].max()) / 2) * s
    co[inner, ax] = op["back"] - s * EMBED
    front = float((co[~inner, ax] * s).max())
    proj0 = front - op["back"] * s
    if proj0 < T_RIB_PROJ:
        co[~inner, ax] = s * (op["back"] * s + T_RIB_PROJ)
    setco(o, co)
    before, after = [], []
    for pax in (1 - ax, 2):
        t0, t1 = widen_axis(o, pax, T_RIB); before.append(t0); after.append(t1)
    # NW curtain-wall corner (the only place two glazing pockets meet at a building edge): widened edge ribs must not
    # stick out past the two facade planes of the corner
    if k in ("CUT_00_N", "CUT_21_W"):
        co = getco(o)
        if k == "CUT_00_N" and co[:, 0].min() < NW_X0 - 1e-6:
            co[:, 0] = np.clip(co[:, 0], NW_X0, None); CLAMPED.append((n, "x >= west facade"))
        if k == "CUT_21_W" and co[:, 1].max() > NW_Y1 + 1e-6:
            co[:, 1] = np.clip(co[:, 1], None, NW_Y1); CLAMPED.append((n, "y <= north facade"))
        setco(o, co)
    co = getco(o)
    relief = float((co[:, ax] * s).max() - op["back"] * s)
    import re as _re
    cls = _re.sub(r"\d+", "#", n)
    if co[:, 2].min() < 0.5:
        LOW_RIBS.append((co.min(0), co.max(0)))
    L = rib_log[cls]; L.setdefault("proj_before", []).append(proj0); L["count"] += 1; L["face_before"].append(min(before)); L["face_after"].append(min(after)); L["relief"].append(relief)
    body_parts.append(o)
log_class("facade_relief_ribs", clamped_at_building_edge=CLAMPED)
log_class("facade_relief_ribs", count=len(FD_RIBS), unmatched_to_opening=unmatched,
          by_class={k: dict(count=v["count"], face_min_before_m=round(min(v["face_before"]), 4),
                            face_min_after_m=round(min(v["face_after"]), 4), projection_before_m=round(min(v["proj_before"]), 4), relief_min_m=round(min(v["relief"]), 4),
                            relief_max_m=round(max(v["relief"]), 4)) for k, v in sorted(rib_log.items())})
# NW curtain-wall corner: where the north (CUT_00_N) and west (CUT_21_W) glazing pockets meet, v023 leaves a
# 0.12 m corner post (0.50 mm at 1:240). Widen it to the rib minimum, keeping both outer faces flush with the facades.
cx0 = float(cut["CUT_00_N"][0][0]); cy1 = float(cut["CUT_21_W"][1][1])
cz0 = max(float(cut["CUT_00_N"][0][2]), float(cut["CUT_21_W"][0][2])); cz1 = min(float(cut["CUT_00_N"][1][2]), float(cut["CUT_21_W"][1][2]))
corner_post = make_box("P_NW_corner_post", cx0, cx0 + T_RIB, cy1 - T_RIB, cy1, cz0 - EMBED, cz1 + EMBED); corner_post["src"] = "print reinforcement"
body_parts.append(corner_post)
log_class("nw_curtainwall_corner_post", x=[round(cx0, 3), round(cx0 + T_RIB, 3)], y=[round(cy1 - T_RIB, 3), round(cy1, 3)],
          z=[round(cz0, 3), round(cz1, 3)], documented_m=0.12, printed_m=T_RIB,
          treatment="corner post between the north and west curtain-wall recesses widened 0.12 -> 0.168 m (0.50 -> 0.70 mm), outer faces flush with both facades")
log_class("glazing_recess", openings=len(openings),
          rule="glass panes and spandrels removed; the approved v023 opening pockets remain as the glazing recess; mullions become bonded relief ribs")

for n in DOOR_CANOPIES:
    body_parts.append(wcopy(n))
log_class("door_side_canopies", count=len(DOOR_CANOPIES), treatment="unchanged (>= 1.88 mm at 1:240), part of the body",
          min_thickness_m=round(min(thin_dir(bpy.data.objects[n])[1] for n in DOOR_CANOPIES), 4))

rail_log = []
for n in RAILS:
    o = wcopy(n); t0, t1 = thicken(o, T_WALL, "center")
    co = getco(o); zmin = co[:, 2].min(); co[np.isclose(co[:, 2], zmin), 2] -= EMBED; setco(o, co)
    rail_log.append((n, round(t0, 4), round(t1, 4))); body_parts.append(o)
log_class("glass_railings", count=len(RAILS), thickened=rail_log,
          treatment="30 mm glass panels thickened to a solid 1.0 mm fin centred on the glass line, on top of the low parapet")

for o in body_parts + [podium]:
    m = fix_solid(o)
    if not solid_ok(m):
        LOG["warnings"].append(f"body operand not solid: {o.name} {m}")
mb = boolean(podium, body_parts, "UNION", "body_union")
print(f"[build] body union: {mb['tris']} tris, islands {mb['islands']}, watertight {solid_ok(mb)}  ({time.time()-T0:.1f}s)")

# ================================================================== DROP-OFF CANOPY / PORTE COCHERE (separate part)
can_parts, can_log = [], {}
carrier = None
columns = []
for n in CANOPY_SRC:
    o = wcopy(n)
    if "column" in n:
        a0, b0 = getco(o).min(0), getco(o).max(0)
        t0 = float(min((b0 - a0)[:2]))
        cx, cy = (a0[:2] + b0[:2]) / 2
        hx, hy = max((b0 - a0)[0], T_POST) / 2, max((b0 - a0)[1], T_POST) / 2
        ztop = float(b0[2])
        m_ = o.data; bpy.data.objects.remove(o); bpy.data.meshes.remove(m_)
        base = rect(cx - hx, cx + hx, cy - hy, cy + hy)
        foot = rect(cx - hx, cx + hx, cy - hy, cy + hy, -CH_COLUMN)
        o = make_loft("P_" + n, [(foot, SOCKET_FLOOR), (base, SOCKET_FLOOR + CH_COLUMN), (base, ztop)]); o["src"] = n
        columns.append((n, cx - hx, cx + hx, cy - hy, cy + hy))
        can_log[n] = ("column", round(t0, 4), round(2 * min(hx, hy), 4), "foot chamfer", CH_COLUMN)
    elif "purlin" in n:
        t0, t1 = thicken(o, T_WALL, "center"); can_log[n] = ("purlin", round(t0, 4), round(t1, 4))
    elif "glass" in n:
        t0, t1 = thicken(o, T_WALL, "top"); can_log[n] = ("glass plate", round(t0, 4), round(t1, 4))
    else:
        t0, t1 = thicken(o, T_BEAM, "center"); can_log[n] = ("beam", round(t0, 4), round(t1, 4))
    fix_solid(o)
    if carrier is None:
        carrier = o; carrier.name = "PRINT_canopy_dropoff"
        for c in list(o.users_collection): c.objects.unlink(o)
        C_CAN.objects.link(o)
    else:
        can_parts.append(o)
# valley tie: the two glass wings are separated by an open 0.22 m valley in v023, so the south (rear) wing hung only
# on its three thin beams and snapped off the v001 coupon during support removal. A continuous tie between the
# innermost purlins (south_1 and north_3), below the glass plane, joins both wings along the full canopy length.
ps1, pn3 = wbox("Canopy_purlin_south_1"), wbox("Canopy_purlin_north_3")
gs, gn = wbox("Canopy_glass_south"), wbox("Canopy_glass_north")
tie_x0, tie_x1 = float(min(ps1[0][0], pn3[0][0])), float(max(ps1[1][0], pn3[1][0]))
tie_y0, tie_y1 = float(ps1[0][1]) - (T_WALL - 0.1512) / 2, float(pn3[1][1]) + (T_WALL - 0.1512) / 2
tie_z0, tie_z1 = float(min(ps1[0][2], pn3[0][2])), float(max(ps1[1][2], pn3[1][2]))
valley_glass_top = float(min(gs[1][2], gn[1][2], 4.963))
assert tie_z1 < valley_glass_top, "valley tie would show above the glass"
tie = make_box("P_canopy_valley_tie", tie_x0, tie_x1, tie_y0, tie_y1, tie_z0, tie_z1); tie["src"] = "print reinforcement"
fix_solid(tie); can_parts.append(tie)
mc = boolean(carrier, can_parts, "UNION", "canopy_union")
log_class("dropoff_canopy", members=can_log,
          valley_tie=dict(x=[round(tie_x0, 3), round(tie_x1, 3)], y=[round(tie_y0, 3), round(tie_y1, 3)], z=[round(tie_z0, 3), round(tie_z1, 3)],
                          below_glass_top_m=round(valley_glass_top - tie_z1, 3),
                          purpose="joins the south (rear) glass wing to the north wing along the full 20 m; sits between the two innermost purlins, "
                                  "below the glass plane - visible from above only as a gutter in the 0.22 m valley"),
          treatment="separate part; columns 1.4 mm with a 0.3 mm lead-in chamfer at the foot, extended to the socket floor; beams 1.2 mm; "
                    "purlins and glass plates 1.0 mm (glass keeps its documented top surface; thickening closes the standoff gap); "
                    "hidden valley tie added (print reinforcement)")
print(f"[build] canopy union: islands {mc['islands']}, watertight {solid_ok(mc)}")

# ================================================================== SUN-SHADE (separate part)
sun_parts, sun_log = [], {}
frame = [n for n in SUNSHADE_SRC if "louver" not in n]
louvers = [n for n in SUNSHADE_SRC if "louver" in n]
frame_top = max(wbox(n)[1][2] for n in frame)
ss_ref = ref_of["L2_LowRoof"]
carrier = None
for n in frame:
    o = wcopy(n)
    t0, t1 = thicken(o, T_WALL, "outer" if ("edge" in n or "_end_" in n) else "center", ss_ref)
    sun_log[n] = ("frame", round(t0, 4), round(t1, 4))
    if carrier is None:
        carrier = o; carrier.name = "PRINT_sunshade"
        for c in list(o.users_collection): c.objects.unlink(o)
        C_SUN.objects.link(o)
    else:
        sun_parts.append(o)
louver_plan = {}
for side in ("south", "east", "north"):
    names = sorted(n for n in louvers if f"_{side}_" in n)
    bbs = [wbox(n) for n in names]
    lo = np.min([p[0] for p in bbs], axis=0); hi = np.max([p[1] for p in bbs], axis=0)
    ax = int(np.argmin((bbs[0][1] - bbs[0][0])[:2])); al = 1 - ax        # across / along
    band = float(hi[ax] - lo[ax])
    n_new = int(math.floor((band + LOUVER_GAP) / (T_WALL + LOUVER_GAP)))
    w = (band - (n_new - 1) * LOUVER_GAP) / n_new
    w_doc = float(np.mean([(p[1] - p[0])[ax] for p in bbs]))
    gaps_doc = sorted(float(q[0][ax] - p[1][ax]) for p, q in zip(sorted(bbs, key=lambda t: t[0][ax]), sorted(bbs, key=lambda t: t[0][ax])[1:]))
    for i in range(n_new):
        c0 = float(lo[ax]) + i * (w + LOUVER_GAP)
        bx = [0, 0, 0, 0]
        if ax == 1:
            o = make_box(f"P_louver_{side}_{i:02d}", float(lo[0]), float(hi[0]), c0, c0 + w, float(lo[2]), frame_top)
        else:
            o = make_box(f"P_louver_{side}_{i:02d}", c0, c0 + w, float(lo[1]), float(hi[1]), float(lo[2]), frame_top)
        o["src"] = f"SS_louver_{side}_* (redistributed)"
        sun_parts.append(o)
    louver_plan[side] = dict(documented_count=len(names), documented_bar_m=round(w_doc, 4), documented_gap_m=round(gaps_doc[0], 4),
                             band_m=round(band, 4), printed_count=n_new, bar_m=round(w, 4), gap_m=round(LOUVER_GAP, 4),
                             bar_mm=round(w * 1000 / SCALE, 3), gap_mm=round(LOUVER_GAP * 1000 / SCALE, 3),
                             height_m=round(float(frame_top - lo[2]), 4))
    sun_log[f"louvers_{side}"] = louver_plan[side]
for o in [carrier] + sun_parts:
    fix_solid(o)
ms = boolean(carrier, sun_parts, "UNION", "sunshade_union")
log_class("sunshade", frame_members=len(frame), documented_louvers=len(louvers), frame_top_z=frame_top, louver_plan=louver_plan,
          treatment="separate flat part (printed top face down); frame members 0.152 -> 0.240 m (1.0 mm), perimeter edges and end pieces keep their outer face; "
                    "louvers: the documented 12 per side at 1.16 mm pitch cannot hold 1.0 mm bars with 0.5 mm gaps at 1:240, so each side's louvers are "
                    "redistributed evenly inside the SAME documented band (first and last louver edges unchanged) as 9 solid bars with exact 0.50 mm clear gaps; "
                    "bars run from the documented underside to the frame top plane; trimmed so it butts against (never intrudes into) the body",
          members_detail=sun_log)
print(f"[build] sunshade union: islands {ms['islands']}, watertight {solid_ok(ms)}")

# sun-shade must butt against, not intrude into, the body (v023 hips run into the low-roof corners;
# the thickened west end piece reaches 0.024 m into the terrace closet)
bcopy = bpy.data.objects.new("P_body_cutter", podium.data.copy()); WORK.objects.link(bcopy)
ms2 = boolean(carrier, [bcopy], "DIFFERENCE", "sunshade_minus_body")
log_class("sunshade", trimmed_against_body=True, islands_after_trim=ms2["islands"])

# ================================================================== SITE BASE
def outside_crop(n, pad=0.0):
    a, b = wbox(n)
    return b[0] < CROP["x0"] - pad or a[0] > CROP["x1"] + pad or b[1] < CROP["y0"] - pad or a[1] > CROP["y1"] + pad
def crossing_crop(n):
    a, b = wbox(n)
    return not outside_crop(n) and (a[0] < CROP["x0"] or b[0] > CROP["x1"] or a[1] < CROP["y0"] or b[1] > CROP["y1"])
CROP_OUT = {}
for grp, names in (("hardscape", [n for n in SITE09 if n not in (TERRAIN, SKIRT, "Site_North_arrow")]), ("utility yard", YARD),
                   ("beds", BEDS), ("curbs", CURBS), ("bollards", BOLLARDS), ("light poles", POLES), ("plants", VEG)):
    out = [n for n in names if outside_crop(n)]
    cut_ = [n for n in names if crossing_crop(n)]
    CROP_OUT[grp] = dict(omitted=out, cut_at_crop_edge=cut_)
LOG["revised_crop"] = CROP_OUT
HARDSCAPE = [n for n in HARDSCAPE if not outside_crop(n)]
YARD = [n for n in YARD if not outside_crop(n)]
BEDS = [n for n in BEDS if not outside_crop(n)]
CURBS = [n for n in CURBS if not outside_crop(n)]
BOLLARDS = [n for n in BOLLARDS if not outside_crop(n)]
LENSES = [n for n in LENSES if not outside_crop(n)]
POLES = [n for n in POLES if not outside_crop(n)]
POLE_BASES = [n for n in POLE_BASES if not outside_crop(n)]
LUMINAIRES = [n for n in LUMINAIRES if not outside_crop(n)]
VEG = [n for n in VEG if not outside_crop(n)]
terrain = wcopy(TERRAIN, "PRINT_site_base", C_SITE)
BASE_BOTTOM = float(getco(terrain)[:, 2].min())
site_parts = []
hs = []
hs_skipped = []
for n in HARDSCAPE:
    o = wcopy(n)
    if not extend_bottom(o, BASE_BOTTOM + 0.05):
        hs_skipped.append(n)
    hs.append(o)
log_class("hardscape", count=len(HARDSCAPE), bottoms_extended_to_base=len(HARDSCAPE) - len(hs_skipped), not_prism=hs_skipped,
          treatment="walks, plaza, drop-off bands, stairs, landings, pads, slabs, parking islands, retained fill at documented tops; bottoms extended into the base so nothing overhangs")
ground_bvh = bvh_of([terrain] + hs)
site_parts += hs

yard_log = []
for n in YARD:
    o = wcopy(n)
    if "lintel" not in n:
        extend_bottom(o, BASE_BOTTOM + 0.05)
    yard_log.append((n, round(thin_dir(o)[1], 4)))
    site_parts.append(o)
log_class("utility_yard_walls", count=len(YARD), min_thickness_m=min(t for _, t in yard_log),
          treatment="moved to the site base (they stand on the site, west of the building); unchanged thickness (>= 1.5 mm); bottoms extended to the base, lintels unchanged")

for n in HM_IN_YARD:
    o = wcopy(n); t0, t1 = thicken(o, T_WALL, "center")
    co = getco(o); d_ax = int(np.argmax((co.max(0) - co.min(0))[:2]))
    lo, hi = co[:, d_ax].min(), co[:, d_ax].max()
    co[np.isclose(co[:, d_ax], lo), d_ax] -= 0.07; co[np.isclose(co[:, d_ax], hi), d_ax] += 0.07
    zt = co[:, 2].max(); co[np.isclose(co[:, 2], zt), 2] += 0.03
    setco(o, co); extend_bottom(o, BASE_BOTTOM + 0.05)
    site_parts.append(o)
    log_class("yard_doors", **{n: dict(before=round(t0, 4), after=round(t1, 4))})
log_class("yard_doors", treatment="door leaves in the generator-yard wall openings thickened to 1.0 mm (centred, recessed ~0.10 m from both wall faces) and extended 0.07 m into the jambs/lintel so they bond")

# beds / planting areas -> raised pads (top = max(bed sheet, grade) + T_RELIEF)
bed_log = {}
bed_objs = []
for n in BEDS:
    src = wcopy(n, "tmp_bed")
    bm = bmesh.new(); bm.from_mesh(src.data)
    srcm = src.data; bpy.data.objects.remove(src); bpy.data.meshes.remove(srcm)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
    bmesh.ops.triangulate(bm, faces=bm.faces[:])
    for _ in range(8):
        if max(e.calc_length() for e in bm.edges) <= 1.0:
            break
        bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=1, use_grid_fill=True)
        bmesh.ops.triangulate(bm, faces=bm.faces[:])
    raised = 0
    for v in bm.verts:
        g = ground_z(ground_bvh, v.co.x, v.co.y)
        z0 = v.co.z
        v.co.z = max(z0, g if g is not None else z0) + T_RELIEF
        raised += (g is not None and g > z0)
    bm.normal_update()
    if sum(f.normal.z for f in bm.faces) < 0:
        bmesh.ops.reverse_faces(bm, faces=bm.faces[:])
    geom = bmesh.ops.extrude_face_region(bm, geom=bm.faces[:], use_keep_orig=True)
    for v in [g for g in geom["geom"] if isinstance(g, bmesh.types.BMVert)]:
        v.co.z -= 1.0
    o = make_mesh("P_" + n, bm); o["src"] = n
    m = fix_solid(o)
    bed_log[n] = dict(watertight=solid_ok(m), verts_raised_to_grade=raised)
    bed_objs.append(o)
site_parts += bed_objs
log_class("beds_planting_areas", beds=bed_log,
          treatment="open bed/lawn sheets rebuilt as closed pads: top = max(documented bed surface, local grade) + 0.075 m (0.3 mm relief), 1.0 m deep into the base")
plant_bvh = bvh_of([terrain] + hs + bed_objs)

curb_log = {}
for n in CURBS:
    o = wcopy(n)
    m = metrics(o)
    if m["boundary_edges"]:
        bm = bmesh.new(); bm.from_mesh(o.data)
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
        bmesh.ops.holes_fill(bm, edges=[e for e in bm.edges if e.is_boundary], sides=0)
        bm.to_mesh(o.data); bm.free(); o.data.update()
    m = fix_solid(o)
    ext = extend_bottom(o, BASE_BOTTOM + 0.05)
    m = fix_solid(o)
    curb_log[n] = dict(watertight=solid_ok(m), width_m=round(thin_dir(o)[1], 4), bottom_extended=ext)
    if solid_ok(m):
        site_parts.append(o)
    else:
        LOG["omitted"].setdefault("curbs that could not be closed", []).append(n)
        bpy.data.objects.remove(o)
log_class("curbs", curbs=curb_log, treatment="kept at documented 6 in width (0.64 mm at 1:240) as relief bonded to walk edges (not free-standing); open meshes closed; curbs outside the crop omitted")

boll_log = {}
for n in BOLLARDS + LENSES:
    o = wcopy(n); co = getco(o); a, b = co.min(0), co.max(0); c = (a + b) / 2
    d0 = float(max((b - a)[:2])); f = T_POST / d0 if d0 < T_POST else 1.0
    co[:, :2] = c[:2] + (co[:, :2] - c[:2]) * f
    setco(o, co)
    if n in BOLLARDS:
        extend_bottom(o, BASE_BOTTOM + 0.05)
    else:
        co = getco(o); zb = co[:, 2].min(); co[np.isclose(co[:, 2], zb), 2] -= EMBED; setco(o, co)
    fix_solid(o); boll_log[n] = (round(d0, 4), round(d0 * f, 4)); site_parts.append(o)
log_class("bollards", count=len(BOLLARDS), lenses=len(LENSES), diameters=boll_log,
          treatment="6 in bollards scaled in plan to 0.336 m (1.4 mm) posts, documented height kept; light-bollard lens caps scaled with them and bonded on top")

pole_log = {}
for n in POLES:
    o = wcopy(n); t0 = thin_dir(o)[1]
    widen_axis(o, 0, T_POLE); widen_axis(o, 1, T_POLE)
    co = getco(o); zb = co[:, 2].min(); co[np.isclose(co[:, 2], zb), 2] -= EMBED; setco(o, co)
    pole_log[n] = ("shaft", round(t0, 4), T_POLE); site_parts.append(o)
for n in POLE_BASES:
    o = wcopy(n); t0 = thin_dir(o)[1]
    widen_axis(o, 0, T_POLE_BASE); widen_axis(o, 1, T_POLE_BASE); extend_bottom(o, BASE_BOTTOM + 0.05)
    pole_log[n] = ("base", round(t0, 4), round(max(t0, T_POLE_BASE), 4)); site_parts.append(o)
for n in LUMINAIRES:
    o = wcopy(n); t0, t1 = thicken(o, T_WALL, "top")
    pole_log[n] = ("luminaire head", round(t0, 4), round(t1, 4)); site_parts.append(o)
log_class("light_poles", count=len(POLES), members=pole_log,
          treatment="5 in shafts thickened to 0.456 m (1.9 mm) square, documented height kept; bases widened 0.457 -> 0.624 m (2.6 mm) so they stay wider than the shaft; luminaire heads thickened to 1.0 mm keeping their top")

# vegetation -> simplified closed forms
veg_log = dict(shrubs=0, trees=0, min_diameter_m=9, max_diameter_m=0, enlarged_to_min_d=0, raised_to_min_h=0, no_ground=[])
done = set()
by_species = defaultdict(int)
for n in VEG:
    if n in done:
        continue
    a, b = wbox(n)
    cx, cy = (a[:2] + b[:2]) / 2
    if n.startswith("LAND_SANJ"):
        fol = [k for k in VEG if k.startswith("LAND_SANJ") and not k.endswith("_trunk")][0]
        fa, fb = wbox(fol); cx, cy = (fa[:2] + fb[:2]) / 2
        g = ground_z(plant_bvh, cx, cy)
        r = float(max(fb[:2] - fa[:2])) / 2; zb = float(fa[2]); zt = float(fb[2]); rt = T_POST / 2
        z_w = zb + (r - rt)
        prof = [(rt, zb)] + [(r * math.cos(a_), z_w + (zt - z_w) * math.sin(a_)) for a_ in np.linspace(0, math.pi / 2, 5)[:-1]] + [(0.0, zt)]
        can = make_lathe("P_tree_SANJ_canopy", cx, cy, prof, 20); can["src"] = fol
        tr = make_box("P_tree_SANJ_trunk", cx - T_POST / 2, cx + T_POST / 2, cy - T_POST / 2, cy + T_POST / 2, g - 0.2, zb + 0.05)
        site_parts += [can, tr]; veg_log["trees"] += 1
        done.update(k for k in VEG if k.startswith("LAND_SANJ")); by_species["SANJ"] += 1
        veg_log["tree_SANJ"] = dict(canopy_diameter_m=round(2 * r, 3), canopy_bottom=zb, top=zt, trunk_m=T_POST, ground=g,
                                    form="45-degree cone underside + dome top (prints without support)")
        continue
    g = ground_z(plant_bvh, cx, cy)
    if g is None:
        veg_log["no_ground"].append(n); continue
    d = float(max(b[:2] - a[:2])); h = float(b[2] - a[2])
    D = max(d, PLANT_MIN_D); H = max(h, PLANT_MIN_H)
    veg_log["enlarged_to_min_d"] += D > d; veg_log["raised_to_min_h"] += H > h
    veg_log["min_diameter_m"] = min(veg_log["min_diameter_m"], D); veg_log["max_diameter_m"] = max(veg_log["max_diameter_m"], D)
    o = make_lathe("P_" + n, cx, cy, dome_profile(g, D / 2, H), 12); o["src"] = n
    site_parts.append(o); veg_log["shrubs"] += 1; by_species[n.split("_")[1]] += 1
    done.add(n)
veg_log["by_species"] = dict(sorted(by_species.items()))
log_class("vegetation", **veg_log,
          treatment="each documented plant replaced by one closed dome at its documented plan centre, sitting on the local grade/bed; "
                    "diameter = documented plan size (min 1.5 mm), height = documented height (min 1.0 mm); the single tree = 1.4 mm trunk + onion canopy; plants outside the revised crop are omitted")

for o in site_parts + [terrain]:
    m = fix_solid(o)
    if not solid_ok(m):
        LOG["warnings"].append(f"site operand not solid: {o.name} {m}")
print(f"[build] site operands ready: {len(site_parts)}  ({time.time()-T0:.1f}s)")
m1 = boolean(terrain, site_parts, "UNION", "site_union")
crop = make_box("P_crop", CROP["x0"], CROP["x1"], CROP["y0"], CROP["y1"], BASE_BOTTOM - 1.0, 30.0)
m2 = boolean(terrain, [crop], "INTERSECT", "site_crop")
POCKET = offset_poly(FOOT, CLR_POCKET)
cutters = [make_prism("P_pocket", POCKET, Z_FOUND, 12.0)]
for i, (lo_, hi_) in enumerate(LOW_RIBS):
    cutters.append(make_box(f"P_rib_clear_{i}", lo_[0] - CLR_POCKET, hi_[0] + CLR_POCKET, lo_[1] - CLR_POCKET,
                            hi_[1] + CLR_POCKET, Z_FOUND, hi_[2] + CLR_POCKET))
socket_log = {}
for (n, x0, x1, y0, y1) in columns:
    g = ground_z(ground_bvh, (x0 + x1) / 2, (y0 + y1) / 2)
    g = 0.0 if g is None else g
    r0 = rect(x0, x1, y0, y1, CLR_SOCKET); r1 = rect(x0, x1, y0, y1, CLR_SOCKET + LEADIN)
    cutters.append(make_loft("P_socket_" + n, [(r0, SOCKET_FLOOR), (r0, g - LEADIN), (r1, g), (r1, 6.0)]))
    socket_log[n] = dict(grade_z=round(g, 3), clearance_m=CLR_SOCKET, lead_in_m=LEADIN, floor_z=SOCKET_FLOOR)
m3 = boolean(terrain, cutters, "DIFFERENCE", "site_pocket_sockets")
log_class("site_base", base_bottom_z=BASE_BOTTOM, pocket_floor_z=Z_FOUND, pocket_clearance_m=CLR_POCKET,
          socket_floor_z=SOCKET_FLOOR, socket_clearance_m=CLR_SOCKET, sockets=socket_log, pocket_outline_area_m2=round(abs(poly_area(POCKET)), 3), grade_level_rib_clearance_boxes=len(LOW_RIBS))
print(f"[build] site base: islands {m3['islands']}, watertight {solid_ok(m3)}  ({time.time()-T0:.1f}s)")

# ================================================================== remove zero-volume boolean slivers
def drop_degenerate_islands(ob, vol_tol=1e-7, size_tol=0.25):
    me = ob.data; me.calc_loop_triangles(); co = getco(ob)
    ed = np.empty(len(me.edges) * 2, dtype=np.int64); me.edges.foreach_get("vertices", ed); ed = ed.reshape(-1, 2)
    lab = islands(len(co), ed)
    tv = np.empty(len(me.loop_triangles) * 3, dtype=np.int64); me.loop_triangles.foreach_get("vertices", tv); tv = tv.reshape(-1, 3)
    tl = lab[tv[:, 0]]
    vols = np.bincount(tl, weights=np.einsum("ij,ij->i", co[tv[:, 0]], np.cross(co[tv[:, 1]], co[tv[:, 2]])) / 6.0, minlength=len(co))
    dropped = []
    for L in np.unique(lab):
        m = lab == L
        size = float((co[m].max(0) - co[m].min(0)).max())
        if abs(vols[L]) < vol_tol and size < size_tol:
            dropped.append(dict(verts=int(m.sum()), volume_m3=float(vols[L]), bbox_min=co[m].min(0).round(3).tolist(),
                                bbox_max=co[m].max(0).round(3).tolist()))
    if dropped:
        bm = bmesh.new(); bm.from_mesh(me); bm.verts.ensure_lookup_table()
        kill = [bm.verts[i] for i in range(len(co)) if any(abs(vols[lab[i]]) < vol_tol and
                float((co[lab == lab[i]].max(0) - co[lab == lab[i]].min(0)).max()) < size_tol for _ in [0])]
        bmesh.ops.delete(bm, geom=kill, context="VERTS"); bm.to_mesh(me); bm.free(); me.update()
    return dropped
LOG["degenerate_islands_removed"] = {n: drop_degenerate_islands(bpy.data.objects[n])
                                     for n in ("PRINT_building_body", "PRINT_site_base", "PRINT_canopy_dropoff", "PRINT_sunshade")}

# ================================================================== finalise: keep only PRINT parts
final = {"PRINT_building_body": C_BODY, "PRINT_site_base": C_SITE, "PRINT_canopy_dropoff": C_CAN, "PRINT_sunshade": C_SUN}
mat = bpy.data.materials.get("PRINT_single_color") or bpy.data.materials.new("PRINT_single_color")
mat.diffuse_color = (0.82, 0.81, 0.78, 1.0)
for name in final:
    o = bpy.data.objects[name]
    o.data.name = name + "_mesh"
    o.data.materials.clear(); o.data.materials.append(mat)
    for p in o.data.polygons:
        p.use_smooth = False
    o["print_scale"] = f"1:{SCALE}"
    o["units"] = "real-world metres; export factor 4.1667 mm per m (1000/240)"
keep = set(final)
for o in list(bpy.data.objects):
    if o.name not in keep:
        bpy.data.objects.remove(o, do_unlink=True)
for c in list(bpy.data.collections):
    if c.name not in ("PRINT_v002",) and c.name not in {cc.name for cc in final.values()}:
        bpy.data.collections.remove(c)
bpy.data.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
sc["print_derivative"] = json.dumps({"version": "print_v002", "source": "building_shell_v023.blend (via pristine audit copy)",
                                      "scale": f"1:{SCALE}", "units": "metres (real)", "openings": openings,
                                      "crop_window": CROP, "built": time.strftime("%Y-%m-%d %H:%M")})
LOG["final_parts"] = {name: metrics(bpy.data.objects[name]) for name in final}
LOG["runtime_s"] = round(time.time() - T0, 1)
bad = [n for n, m in LOG["final_parts"].items() if not (solid_ok(m) and m["islands"] == 1)]
def island_report(ob):
    me = ob.data; co = getco(ob)
    ed = np.empty(len(me.edges) * 2, dtype=np.int64); me.edges.foreach_get("vertices", ed); ed = ed.reshape(-1, 2)
    lab = islands(len(co), ed)
    return [dict(verts=int((lab == L).sum()), bbox_min=co[lab == L].min(0).round(3).tolist(), bbox_max=co[lab == L].max(0).round(3).tolist())
            for L in np.unique(lab)]
LOG["island_report"] = {n: island_report(bpy.data.objects[n]) for n in bad}
LOG["all_parts_single_watertight_island"] = not bad
os.makedirs(VAL, exist_ok=True)
with open(os.path.join(VAL, "print_prep_v002_build_log.json"), "w", encoding="utf-8") as f:
    json.dump(LOG, f, indent=1, default=lambda x: x.tolist() if hasattr(x, "tolist") else str(x))
if bad:
    raise SystemExit(f"[build] NOT SAVED - parts failing watertight/single-island check: {bad}")
bpy.ops.wm.save_mainfile(filepath=BLEND, compress=True)
print(f"[build] saved {BLEND} in {time.time()-T0:.1f}s")
