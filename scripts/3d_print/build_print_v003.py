"""Building II 3D-print derivative v003 - MULTICOLOR version of the approved v002 geometry (1:240), 2026-09-29.

Run (background Blender 5.2, from the project root):
  blender -b models/Building_II/print_derivatives/building_II_print_v003.blend \
          --python scripts/3d_print/build_print_v003.py

Input : building_II_print_v003.blend as a PRISTINE copy of the archive audit copy (= frozen v023).
Output: the same v003 file with the print parts (collection PRINT_v003) + print_prep_v003_build_log.json.
Geometry: IDENTICAL to v002 (this script is build_print_v002.py unchanged up to each part's union; the build gate checks
triangle counts and volumes of all four parts against print_prep_v002_build_log.json). v003 adds colour OVERLAY parts,
per the owner's controlling colour mapping:
  slot 1 WHITE  = white metal paneling  (ACM-1 / ACM-4 Bone White, MTL-2 coping) + white TPO roofs / terrace tops (owner 2026-09-29)
  slot 2 BLACK  = black metal paneling  (ACM-2 / ACM-3 Tri-Corn Black, MTL-1 / MTL-3 copings)
  slot 3 GRAY   = gray brick (BRK-1, BC-1/2) + storefront/curtain-wall frames (Beachstone Gray, owner 2026-09-29) + canopy steel
                  (owner 2026-09-29) + interior core
  slot 4 CLEAR  = exterior glazing (vision + spandrel glass, glass railings, canopy glass)
Method (priority overlay): the exact v002 building body is the gray base part. Colour parts lying INSIDE it:
  WHITE / BLACK = 1.0 mm skins behind every exterior white / black face of the masses and parapets (mitred on the bisector
                  at convex corners to a different finish) + white / black door canopies and doorbay panels
  CLEAR         = 1.2 mm slabs behind each glazing pane at the back of its recess (intersected with a body copy) + glass rails
  FRAMES (gray) = storefront / curtain-wall frames and the NW corner post
In Bambu Studio a later part of an object clips the earlier parts where they overlap (verified with the H2S CLI), so the
part order body < white < black < clear < frames is the colour priority and the slicer resolves the regions per layer.
Each colour part is a JOIN of closed convex shells (skin prisms, slabs, canopies, rails, frames) - no 3D union; Bambu
fills overlapping / touching shells of a part as their union (verified with the H2S CLI).
The approved body is never cut by a 3D boolean (Blender's Manifold boolean returned non-planar n-gons when partitioning the
body into thin skins, cutting diagonal wedges through the colour regions - see PRINT_CONTROL.md Pass 5).
"""
import bpy, bmesh, hashlib, json, math, os, time
import numpy as np
from collections import defaultdict
from mathutils import Vector, Matrix
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

assert os.path.basename(BLEND) == "building_II_print_v003.blend", BLEND
assert sha(BLEND) == V023_SHA, "v003 is not a pristine copy of the audit copy - copy archive/building_II_print_v001_audit_copy.blend over it first"
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

LOG = {"script": "scripts/3d_print/build_print_v003.py", "scale": f"1:{SCALE}",
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
ROOTC = bpy.data.collections.new("PRINT_v003"); sc.collection.children.link(ROOTC)
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

UNZIP_LOG = {}
def unzip_nonmanifold(ob):
    """Where two separate solids of a region touch only along an edge or at a vertex (a 'pinch'), give each solid its
    own copy of the shared vertices. Geometry is unchanged (coincident vertices); every edge then has exactly 2 faces."""
    me = ob.data
    faces = [list(pp.vertices) for pp in me.polygons]
    co = [tuple(v.co) for v in me.vertices]
    ecount = defaultdict(int)
    for f in faces:
        for i in range(len(f)):
            a_, b_ = f[i], f[(i + 1) % len(f)]; ecount[(min(a_, b_), max(a_, b_))] += 1
    bad_e = {e for e, c in ecount.items() if c != 2}
    vfaces = defaultdict(list)
    for fi, f in enumerate(faces):
        for v in f:
            vfaces[v].append(fi)
    new_co = list(co); changed = 0
    for v, fl in vfaces.items():
        if len(fl) < 2:
            continue
        par = {f: f for f in fl}
        def find(x):
            while par[x] != x:
                par[x] = par[par[x]]; x = par[x]
            return x
        ef = defaultdict(list)
        for fi in fl:
            f = faces[fi]; k = f.index(v); n = len(f)
            for w in (f[(k - 1) % n], f[(k + 1) % n]):
                e = (min(v, w), max(v, w))
                if e not in bad_e:
                    ef[e].append(fi)
        for fs in ef.values():
            for x in fs[1:]:
                par[find(x)] = find(fs[0])
        comps = defaultdict(list)
        for fi in fl:
            comps[find(fi)].append(fi)
        if len(comps) > 1:
            for comp in list(comps.values())[1:]:
                nv = len(new_co); new_co.append(co[v]); changed += 1
                for fi in comp:
                    faces[fi][faces[fi].index(v)] = nv
    if changed:
        me.clear_geometry(); me.from_pydata(new_co, [], faces); me.update()
        UNZIP_LOG[ob.name] = UNZIP_LOG.get(ob.name, 0) + changed
    return changed

COLOUR_STAGE = False
def closed_ok(m):
    return m["boundary_edges"] == 0 and m["flipped_edges"] == 0 and m["volume_m3"] > 0
OPEN_SLIVERS = []
def clean_open_islands(ob, vol_tol=1e-4):
    """Exact-solver coplanar coincidences can leave open (boundary-edged) zero-thickness sliver islands. Remove open
    islands whose |volume| < vol_tol m3 (1e-4 m3 = 0.007 mm3 at 1:240); closed islands are never touched."""
    me = ob.data
    if not len(me.polygons):
        return 0
    co = getco(ob)
    ed = np.empty(len(me.edges) * 2, dtype=np.int64); me.edges.foreach_get("vertices", ed); ed = ed.reshape(-1, 2)
    le = np.empty(len(me.loops), dtype=np.int64); me.loops.foreach_get("edge_index", le)
    fpe = np.bincount(le, minlength=len(me.edges))
    lab = islands(len(co), ed)
    open_lab = set(lab[ed[fpe != 2, 0]].tolist())
    if not open_lab:
        return 0
    me.calc_loop_triangles()
    tv = np.empty(len(me.loop_triangles) * 3, dtype=np.int64); me.loop_triangles.foreach_get("vertices", tv); tv = tv.reshape(-1, 3)
    vols = np.bincount(lab[tv[:, 0]], weights=np.einsum("ij,ij->i", co[tv[:, 0]], np.cross(co[tv[:, 1]], co[tv[:, 2]])) / 6.0, minlength=len(co))
    kill = {L for L in open_lab if abs(vols[L]) < vol_tol}
    if not kill:
        return 0
    for L in kill:
        OPEN_SLIVERS.append(dict(object=ob.name, volume_m3=float(vols[L]), at=co[lab == L].mean(0).round(3).tolist()))
    bm = bmesh.new(); bm.from_mesh(me); bm.verts.ensure_lookup_table()
    bmesh.ops.delete(bm, geom=[bm.verts[i] for i in range(len(co)) if int(lab[i]) in kill], context="VERTS")
    bm.to_mesh(me); bm.free(); me.update()
    return len(kill)
def triangulate(ob):
    bm = bmesh.new(); bm.from_mesh(ob.data)
    bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method="BEAUTY", ngon_method="BEAUTY")
    bm.to_mesh(ob.data); bm.free(); ob.data.update()
    unzip_nonmanifold(ob)          # a triangulation diagonal can land on an existing edge at a pinch: separate again
def nonplanar_faces(ob, tol=1e-3):      # 1 mm real = 0.004 mm printed; float noise (~2e-4 m) is ignored
    """faces deviating more than tol from their best-fit (least-squares) plane"""
    me = ob.data; co = getco(ob); n_ = 0
    for p_ in me.polygons:
        if len(p_.vertices) > 3:
            V = co[list(p_.vertices)]; c_ = V.mean(0)
            if float(np.abs((V - c_) @ np.linalg.svd(V - c_)[2][2]).max()) > tol:
                n_ += 1
    return n_
def face_planes(objs):
    """(normals, offsets, bbox_min, bbox_max) of every face of objs - the only planes a boolean result may lie on"""
    N, D, LO, HI = [], [], [], []
    for o in objs:
        me = o.data; co = getco(o); nf = len(me.polygons)
        if not nf:
            continue
        nr_ = np.empty(nf * 3); me.polygons.foreach_get("normal", nr_); nr_ = nr_.reshape(-1, 3)
        ls = np.empty(nf, dtype=np.int64); me.polygons.foreach_get("loop_start", ls)
        lt = np.empty(nf, dtype=np.int64); me.polygons.foreach_get("loop_total", lt)
        lv = np.empty(len(me.loops), dtype=np.int64); me.loops.foreach_get("vertex_index", lv)
        lo_ = np.minimum.reduceat(co[lv], ls, axis=0); hi_ = np.maximum.reduceat(co[lv], ls, axis=0)
        N.append(nr_); D.append(np.einsum("ij,ij->i", nr_, co[lv[ls]])); LO.append(lo_); HI.append(hi_)
    if not N:
        return None
    return np.vstack(N), np.concatenate(D), np.vstack(LO), np.vstack(HI)

REPAIR_LOG = defaultdict(lambda: dict(repaired=0, unresolved=[]))
def repair_nonplanar(ob, planes, label, tol=1e-3, fit=1e-3):
    """Blender's Manifold boolean sometimes merges output triangles from different planes into one NON-PLANAR n-gon.
    Every true output face lies on a face plane of the inputs, so each such n-gon is re-triangulated (minimum-weight
    polygon triangulation by dynamic programming) so that every triangle lies on one input plane (error <= fit)."""
    if planes is None:
        return
    Np, Dp, LOp, HIp = planes
    me = ob.data; co = getco(ob)
    faces = [list(p.vertices) for p in me.polygons]; changed = False; out = []
    for f in faces:
        if len(f) > 3:
            V = co[f]; c_ = V.mean(0); u_, s_, vt_ = np.linalg.svd(V - c_)
            if float(np.abs((V - c_) @ vt_[2]).max()) > tol:
                lo, hi = V.min(0) - 1e-3, V.max(0) + 1e-3
                sel = np.all(HIp >= lo, axis=1) & np.all(LOp <= hi, axis=1)
                Nc, Dc = Np[sel], Dp[sel]
                n = len(f)
                def w(i, j, k):
                    T = V[[i, j, k]]
                    if np.linalg.norm(np.cross(T[1] - T[0], T[2] - T[0])) < 1e-12:
                        return 0.0
                    return float(np.abs(T @ Nc.T - Dc).max(0).min()) if len(Nc) else 1e9
                C = [[0.0] * n for _ in range(n)]; K = [[-1] * n for _ in range(n)]
                for gap in range(2, n):
                    for i in range(n - gap):
                        j = i + gap; best, bk = 1e18, -1
                        for k in range(i + 1, j):
                            cst = max(C[i][k], C[k][j], w(i, k, j))
                            if cst < best:
                                best, bk = cst, k
                        C[i][j], K[i][j] = best, bk
                if C[0][n - 1] <= fit:
                    tris = []
                    def rec(i, j):
                        if j - i < 2:
                            return
                        k = K[i][j]; tris.append([f[i], f[k], f[j]]); rec(i, k); rec(k, j)
                    rec(0, n - 1)
                    out.extend(tris); changed = True; REPAIR_LOG[label]["repaired"] += 1
                    continue
                REPAIR_LOG[label]["unresolved"].append(dict(verts=n, err_m=round(C[0][n - 1], 5), at=c_.round(2).tolist()))
        out.append(f)
    if changed:
        me.clear_geometry(); me.from_pydata([tuple(c) for c in co], [], out); me.update()

def boolean(target, operands, op, label, allow_noop=False, unzip=False, tri=None):
    # v003 colour stage: Blender's Manifold solver output can contain NON-PLANAR n-gons (seen up to 2.8 m out of plane,
    # even for a single planar operand), whose triangulation cuts diagonal wedges through the colour regions. The colour
    # stage therefore uses the EXACT solver (every output face is an exact piece of a planar input face). The v002 part
    # geometry (body / site / canopy / sun-shade unions) is still built with Manifold exactly as in v002.
    if tri:
        for o_ in [target] + list(operands):
            triangulate(o_)
    ok_ = solid_ok
    bad =[o.name for o in operands + [target] if not ok_(metrics(o))]
    if bad:
        det = {o.name: {k: v for k, v in metrics(o).items() if k in ("boundary_edges", "nonmanifold_edges", "flipped_edges", "volume_m3", "islands", "tris")}
               for o in operands + [target] if not ok_(metrics(o))}
        if os.environ.get("V003_DEBUG_SAVE"):
            bpy.ops.wm.save_as_mainfile(filepath=os.environ["V003_DEBUG_SAVE"], copy=True, compress=True)
        raise SystemExit(f"[build] {label}: non-watertight boolean inputs {list(det.items())[:6]} - not saved")
    before = metrics(target)
    planes_ = face_planes([target] + list(operands)) if COLOUR_STAGE else None
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
    mod_solver = mod.solver
    target.modifiers.remove(mod)
    old = target.data; target.data = me; bpy.data.meshes.remove(old)
    if COLOUR_STAGE:
        repair_nonplanar(target, planes_, label)
    if unzip:
        unzip_nonmanifold(target)
    npl_ = nonplanar_faces(target) if COLOUR_STAGE else 0
    for o in list(tmp.objects):
        m_ = o.data; bpy.data.objects.remove(o); bpy.data.meshes.remove(m_)
    bpy.data.collections.remove(tmp)
    m = metrics(target)
    if not allow_noop and m["verts"] == before["verts"] and abs(m["volume_m3"] - before["volume_m3"]) < 1e-9:
        raise SystemExit(f"[build] {label}: boolean had no effect (solver refused?) - not saved")
    LOG["booleans"].append(dict(label=label, op=op, solver=mod_solver, nonplanar_out=npl_, operands=len(operands), seconds=round(time.time() - t, 2),
                                result_tris=m["tris"], islands=m["islands"], watertight=solid_ok(m),
                                volume_before=round(before["volume_m3"], 4), volume_after=round(m["volume_m3"], 4)))
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
# ---------------- v003: colour operands captured before the union consumes them
def dup(o, name):
    c = bpy.data.objects.new(name, o.data.copy()); WORK.objects.link(c); c["src"] = o.get("src", ""); return c
def colour_of_material(m):
    if m.startswith(("ACM-1", "ACM-4", "MTL-2", "TPO", "UNRES-colour_terrace_pavers", "PAINT_match_ACM-1")): return "WHITE"
    if m.startswith(("ACM-2", "ACM-3", "MTL-1", "MTL-3")): return "BLACK"
    if m.startswith("GLASS"): return "CLEAR"
    return "GRAY"          # BRK-1, BC-1/2, FRAME_YKK Beachstone Gray, UNRES parapet inner (follows the brick outer face), steel
COL_GRAY_FORCED, COL_CLEAR, COL_WHITE, COL_BLACK = [], [], [], []
for o in body_parts + [podium]:
    src = o.get("src", "")
    if src in FD_RIBS:
        (COL_WHITE if colour_of_material(mats(src)) == "WHITE" else COL_GRAY_FORCED).append(dup(o, "C_" + src))
    elif o.name == "P_NW_corner_post":
        COL_GRAY_FORCED.append(dup(o, "C_NW_corner_post"))
    elif src in RAILS:
        COL_CLEAR.append(dup(o, "C_" + src))
    elif src in DOOR_CANOPIES:
        {"WHITE": COL_WHITE, "BLACK": COL_BLACK}.get(colour_of_material(mats(src)), COL_GRAY_FORCED).append(dup(o, "C_" + src))
FW_NAMES = [o.name for o in COL_WHITE]; FB_NAMES = [o.name for o in COL_BLACK]; FG_COUNT = len(COL_GRAY_FORCED)
BODY_OPS = [dup(o, "O_" + o.name) for o in body_parts + [podium]]     # un-consumed body operands (skin burial test)
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
CAN_CLEAR = [dup(o, "C_can_" + o.get("src", "")) for o in [carrier] + can_parts if "glass" in o.get("src", "")]
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


# ================================================================== v003 COLOUR PARTS (priority overlay on the exact v002 part)
# Design (2026-09-29): the exact v002 building body stays ONE gray part. The colour regions are separate parts that lie
# INSIDE the body (skins behind white / black faces, clear slabs behind glazing, glass rails, door canopies) and an explicit
# gray FRAMES part. In Bambu Studio a later part of the same object clips the earlier parts where they overlap (verified with
# the H2S CLI: coplanar 1 mm skins print at full volume in their own filament and are removed from the body), so the part
# ORDER is the colour priority: body (gray) < white < black < clear < frames (gray). The slicer resolves the overlaps per
# layer in 2D. No 3D boolean ever cuts the approved body: Blender's Manifold boolean returned non-planar n-gons (up to
# 4.4 m wrong) when partitioning the body into thin skins, which cut diagonal wedges through the colour regions.
COLOUR_STAGE = True
D_SKIN = pm(1.0)       # colour skin depth behind white / black faces          0.240 m
G_GLASS = pm(1.2)      # clear slab depth behind each glazing pane              0.288 m
B_BODY = bpy.data.objects["PRINT_building_body"]
BODY_BVH = bvh_of([B_BODY])
def _inside_bvh(bvh, pt):
    n_, o_ = 0, Vector(pt); d = Vector((0.00017, 0.00023, 1.0)).normalized()
    for _ in range(60):
        h = bvh.ray_cast(o_, d, 400.0)
        if h[0] is None:
            break
        n_ += 1; o_ = h[0] + d * 1e-5
    return n_ % 2 == 1

def _body_tris(ob):
    bm = bmesh.new(); bm.from_mesh(ob.data)
    bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method="BEAUTY", ngon_method="BEAUTY")
    T = np.array([[v.co[:] for v in f.verts] for f in bm.faces]); bm.free(); return T
BODY_TRI = _body_tris(B_BODY)
def winding(Tri, Q):
    """generalized winding number (robust inside test: a point ON an internal interface plane, where ray parity can
    miscount, still gets ~1)"""
    Q = np.atleast_2d(np.asarray(Q, float)); out = np.zeros(len(Q)); chunk = max(1, int(1.5e7 // (len(Tri) * 9)))
    for s in range(0, len(Q), chunk):
        R = Tri[None, :, :, :] - Q[s:s + chunk][:, None, None, :]
        a, b, c = R[..., 0, :], R[..., 1, :], R[..., 2, :]
        la, lb, lc = np.linalg.norm(a, axis=-1), np.linalg.norm(b, axis=-1), np.linalg.norm(c, axis=-1)
        num = np.einsum("mti,mti->mt", a, np.cross(b, c))
        den = la * lb * lc + np.einsum("mti,mti->mt", a, b) * lc + np.einsum("mti,mti->mt", b, c) * la + np.einsum("mti,mti->mt", c, a) * lb
        out[s:s + chunk] = (2 * np.arctan2(num, den)).sum(1) / (4 * np.pi)
    return out
def outside_body(points, tol, bvh=None, tri=None):
    """indices of points farther than tol from the body surface AND outside it (winding number < 0.5)"""
    bvh = bvh or BODY_BVH; tri = BODY_TRI if tri is None else tri
    far = [i for i, p in enumerate(points) if (lambda r: r[3] is not None and r[3] > tol)(bvh.find_nearest(Vector(p)))]
    if not far:
        return []
    w = winding(tri, np.array([points[i] for i in far]))
    return [i for i, wi in zip(far, w) if wi < 0.5]

def _hull_mesh(pts):
    bm = bmesh.new()
    vs = [bm.verts.new(tuple(p)) for p in pts]
    res = bmesh.ops.convex_hull(bm, input=vs, use_existing_faces=False)
    for g in res.get("geom_interior", []) + res.get("geom_unused", []):
        if isinstance(g, bmesh.types.BMVert) and g.is_valid and not g.link_faces:
            bm.verts.remove(g)
    return bm

def _dedupe(pts, tol=1e-6):
    out = []
    for p in pts:
        if all(np.linalg.norm(p - q) > tol for q in out):
            out.append(p)
    return out

def tri_prism(name, a, b, c, n, depth, clips):
    """Skin piece behind triangle abc: the right prism (abc swept 'depth' along -n) clipped by the mitre half-spaces
    {p : (p - pco) . pno <= 0}; convex hull of the clipped vertex set (always a clean convex solid)."""
    pts = [np.array(p, float) for p in (a, b, c, a - n * depth, b - n * depth, c - n * depth)]
    for pco, pno in clips:
        pco = np.asarray(pco, float); pno = np.asarray(pno, float)
        bm = _hull_mesh(pts)
        edges = [(np.array(e.verts[0].co), np.array(e.verts[1].co)) for e in bm.edges]
        verts = [np.array(v.co) for v in bm.verts]
        bm.free()
        dist = [float(np.dot(v - pco, pno)) for v in verts]
        keep = [v for v, d_ in zip(verts, dist) if d_ <= 1e-7]
        for p0, p1 in edges:
            d0, d1 = float(np.dot(p0 - pco, pno)), float(np.dot(p1 - pco, pno))
            if (d0 < -1e-7 and d1 > 1e-7) or (d0 > 1e-7 and d1 < -1e-7):
                keep.append(p0 + (p1 - p0) * (d0 / (d0 - d1)))
        keep = _dedupe(keep)
        if len(keep) < 4:
            return None
        pts = keep
    bm = _hull_mesh(pts)
    if len(bm.faces) < 4:
        bm.free(); return None
    ob = make_mesh(name, bm)
    m = fix_solid(ob)
    if not solid_ok(m) or m["volume_m3"] < 1e-7:
        me_ = ob.data; bpy.data.objects.remove(ob); bpy.data.meshes.remove(me_); return None
    return ob

# Burial test per body operand: a white/black face that is entirely covered by another body operand (a shared internal
# wall) gets no skin. 7 sample points per triangle (centroid, 3 inset corners, 3 inset edge midpoints): all covered -> skip.
# Partly covered faces keep their whole skin: the covered part of the skin lies inside the body, hidden.
OPS_BVH = []
for o in BODY_OPS:
    co_ = getco(o)
    OPS_BVH.append((o, o.get("src", ""), BVHTree.FromPolygons([tuple(c) for c in co_], [tuple(pp.vertices) for pp in o.data.polygons]),
                    co_.min(0) - 0.05, co_.max(0) + 0.05))
def burying_ops(pt, own):
    return [k for k, (o, s_, b, lo, hi) in enumerate(OPS_BVH) if s_ != own and np.all(pt >= lo) and np.all(pt <= hi) and _inside_bvh(b, pt)]
CLIP_LOG = []
def clip_convex_to_body(ob, tol=0.003, iters=6):
    """A convex colour piece (skin prism / glass slab) must lie inside the body. Where a vertex is outside (parapet corner
    mitres, the NW corner curtain wall), clip the piece by the half-space of the nearest body face and repeat. Pure convex
    clipping - no boolean against the approved body."""
    pts = [np.array(v.co) for v in ob.data.vertices]; v0 = metrics(ob)["volume_m3"]; clipped = 0
    # half-space clipping can slice diagonally across a large roof triangle (a 45-degree parapet chamfer face as the
    # nearest face), so every piece with a vertex outside is intersected with a body copy instead (removes only what is out)
    iters = 0
    for _ in range(iters):
        outs = []
        for p in pts:
            loc, nrm, idx, dist = BODY_BVH.find_nearest(Vector(p))
            if dist is not None and dist > tol and not _inside_bvh(BODY_BVH, p):
                outs.append((np.array(loc), np.array(nrm)))
        if not outs:
            break
        for loc, nrm in outs[:1]:
            bm = _hull_mesh(pts); edges = [(np.array(e.verts[0].co), np.array(e.verts[1].co)) for e in bm.edges]
            verts = [np.array(v.co) for v in bm.verts]; bm.free()
            keep = [v for v in verts if float(np.dot(v - loc, nrm)) <= 1e-7]
            for p0, p1 in edges:
                d0, d1 = float(np.dot(p0 - loc, nrm)), float(np.dot(p1 - loc, nrm))
                if (d0 < -1e-7 and d1 > 1e-7) or (d0 > 1e-7 and d1 < -1e-7):
                    keep.append(p0 + (p1 - p0) * (d0 / (d0 - d1)))
            pts = _dedupe(keep); clipped += 1
            if len(pts) < 4:
                name = ob.name; me_ = ob.data; bpy.data.objects.remove(ob); bpy.data.meshes.remove(me_)
                CLIP_LOG.append(dict(piece=name, volume_before_m3=round(v0, 5), volume_after_m3=0.0)); return None
    # vertices AND face centroids: a convex piece can have all corners inside yet cross a recess (glazing / door pocket)
    cens = [np.array(p.center) for p in ob.data.polygons] if not clipped else []
    still_out = bool(outside_body(list(pts) + cens, tol))
    if still_out:
        # concave notch (parapet corner steps): convex clipping cannot reach it - intersect this one small piece with a
        # copy of the body (the approved body itself is never cut)
        name = ob.name
        bc = bpy.data.objects.new(name + "_bodycopy", B_BODY.data.copy()); WORK.objects.link(bc)
        m = boolean(ob, [bc], "INTERSECT", f"clip_{name}", allow_noop=True, unzip=True)
        CLIP_LOG.append(dict(piece=name, method="intersect with body copy", volume_before_m3=round(v0, 5), volume_after_m3=round(m["volume_m3"], 5)))
        if m["tris"] == 0 or m["volume_m3"] < 1e-7 or not solid_ok(m):
            me_ = ob.data; bpy.data.objects.remove(ob); bpy.data.meshes.remove(me_); return None
        return ob
    if clipped:
        bm = _hull_mesh(pts); name = ob.name
        if len(bm.faces) < 4:
            bm.free(); me_ = ob.data; bpy.data.objects.remove(ob); bpy.data.meshes.remove(me_)
            CLIP_LOG.append(dict(piece=name, volume_before_m3=round(v0, 5), volume_after_m3=0.0)); return None
        me_new = bpy.data.meshes.new(name + "_clip"); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(me_new); bm.free()
        old = ob.data; ob.data = me_new; bpy.data.meshes.remove(old)
        m = fix_solid(ob)
        CLIP_LOG.append(dict(piece=name, clips=clipped, volume_before_m3=round(v0, 5), volume_after_m3=round(m["volume_m3"], 5)))
        if not solid_ok(m) or m["volume_m3"] < 1e-7:
            me_ = ob.data; bpy.data.objects.remove(ob); bpy.data.meshes.remove(me_); return None
    return ob

def local_depth(cen, ni):
    """skin depth limited by the body thickness behind the face (keeps every skin inside the body)"""
    h = BODY_BVH.ray_cast(Vector(cen - ni * 1e-4), Vector(-ni), D_SKIN + 1.0)
    if h[0] is None:
        return D_SKIN
    return min(D_SKIN, max(0.0, (h[0] - Vector(cen)).length - 0.002))

skins = {"WHITE": [], "BLACK": []}
skin_log = defaultdict(lambda: dict(tris=0, prisms=0, internal_skipped=0, underside_skipped=0, mitred_edges=0, partly_covered_kept=0,
                                    covered_by=[], dropped=[], depth_limited=[], mitre_oblique_corrected=0, mitre_rejected=0))
OP_OF = {o.get("src", ""): o for o in BODY_OPS}
SKIN_GEOM = {}
for n in MASSES + PARAPETS:
    src = bpy.data.objects[n]; me = src.data; me.calc_loop_triangles()
    Mw = np.array(src.matrix_world)
    co = np.array([v.co for v in me.vertices], float); co = co @ Mw[:3, :3].T + Mw[:3, 3]
    # skins follow the PRINT geometry: parapets thinner than 1.0 mm were thickened toward the roof in v002, which moved
    # their inner (TPO membrane) face; the body copy has the same topology, so its vertex positions are used
    op_ = OP_OF.get(n)
    if op_ is not None and len(op_.data.vertices) == len(me.vertices):
        co_op = getco(op_)
        SKIN_GEOM[n] = dict(source="print body operand", max_shift_m=round(float(np.abs(co_op - co).max()), 4))
        co = co_op
    else:
        SKIN_GEOM[n] = dict(source="v023 source (topology differs from the body operand)")
    slots = [sl.material.name if sl.material else "NONE" for sl in src.material_slots]
    tris = [(tuple(t.vertices), t.material_index) for t in me.loop_triangles]
    cols = [colour_of_material(slots[mi]) if mi < len(slots) else "GRAY" for _, mi in tris]
    key = np.round(co, 5); uk, weld = np.unique(key, axis=0, return_inverse=True); weld = weld.ravel()
    P = uk.astype(float)
    tv = np.array([[weld[i] for i in t] for t, _ in tris])
    nr = np.cross(P[tv[:, 1]] - P[tv[:, 0]], P[tv[:, 2]] - P[tv[:, 0]]); ar = np.linalg.norm(nr, axis=1)
    nr = nr / np.maximum(ar, 1e-30)[:, None]
    emap = defaultdict(list)
    for i, t in enumerate(tv):
        for u, w in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):
            emap[(min(u, w), max(u, w))].append(i)
    for i, t in enumerate(tv):
        c = cols[i]
        if c not in skins or ar[i] < 1e-8:
            continue
        L = skin_log[n]; L["tris"] += 1
        ni = nr[i]
        if ni[2] < -0.5:
            L["underside_skipped"] += 1; continue
        cen = P[t].mean(0)
        samp = [cen] + [P[v] + (cen - P[v]) * 0.08 for v in t] + [(P[t[a_]] + P[t[b_]]) / 2 * 0.92 + cen * 0.08 for a_, b_ in ((0, 1), (1, 2), (2, 0))]
        cover = set(); ncov = 0
        if abs(ni[2]) < 0.7:          # walls only: roof / deck skin under a parapet is hidden, and long roof slivers
            for s_ in samp:           # running into a parapet corner can have every sample under the parapet
                ks = burying_ops(s_ + ni * 0.02, n)
                if ks:
                    ncov += 1; cover.update(ks)
        if samp and ncov == len(samp):
            # confirm on a dense barycentric grid (28 points) before skipping: a large triangle can be covered at the
            # 7 coarse samples yet still show an exposed strip
            grid = [P[t[0]] * a_ + P[t[1]] * b_ + P[t[2]] * (1 - a_ - b_) for a_ in np.linspace(0.04, 0.92, 7)
                    for b_ in np.linspace(0.04, 0.92, 7) if a_ + b_ <= 0.96]
            if not all(burying_ops(g_ + ni * 0.02, n) for g_ in grid):
                ncov = -1                                     # partly exposed: keep the whole skin
        if samp and ncov == len(samp):
            L["internal_skipped"] += 1
            if ar[i] / 2 > 0.5:
                L["dropped"].append(dict(why="internal", colour=c, area_m2=round(float(ar[i] / 2), 3), centroid=cen.round(2).tolist(), normal=ni.round(2).tolist()))
            continue
        if cover:
            L["partly_covered_kept"] += 1
            for k in cover:
                if OPS_BVH[k][1] not in L["covered_by"]:
                    L["covered_by"].append(OPS_BVH[k][1])
        # convex edge to a different finish: mitre on the bisector plane through the edge, so the neighbour face keeps
        # its own colour right up to the edge (a right prism's side wall would lie IN the neighbour face)
        clips = []
        for u, w in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):
            for j in emap[(min(u, w), max(u, w))]:
                if j == i or cols[j] == c:
                    continue
                q = [x for x in tv[j] if x not in (u, w)]
                if not q or float(np.dot(P[q[0]] - P[u], ni)) >= -1e-6:
                    continue
                pn = nr[j] - ni
                ed_ = P[w] - P[u]; ed_ = ed_ / np.linalg.norm(ed_)
                if abs(float(np.dot(pn, ed_))) > 1e-6:
                    pn = pn - np.dot(pn, ed_) * ed_; L["mitre_oblique_corrected"] += 1
                ln = np.linalg.norm(pn)
                if ln > 1e-6:
                    pn = pn / ln
                    opp = [x for x in t if x not in (u, w)][0]
                    if float(np.dot(P[opp] - P[u], pn)) > 1e-6:
                        L["mitre_rejected"] += 1; continue
                    clips.append((P[u], pn)); L["mitred_edges"] += 1
        dep = local_depth(cen, ni)
        if dep < D_SKIN - 1e-6:
            L["depth_limited"].append(dict(depth_m=round(dep, 4), at=cen.round(2).tolist()))
        if dep < 0.01:
            L["dropped"].append(dict(why="no body thickness behind face", colour=c, at=cen.round(2).tolist())); continue
        pr = tri_prism(f"S_{c}_{n}_{i}", P[t[0]], P[t[1]], P[t[2]], ni, dep, clips)
        if pr is not None:
            pr = clip_convex_to_body(pr)
        if pr is None:
            L["dropped"].append(dict(why="empty after mitre", colour=c, area_m2=round(float(ar[i] / 2), 3), centroid=cen.round(2).tolist(),
                                     normal=ni.round(2).tolist(), clips=len(clips)))
            continue
        skins[c].append(pr); L["prisms"] += 1

# clear slabs behind each glazing pane (vision + spandrel): from the back of its recess G_GLASS into the wall
glass_log = {}
for n in GLAZING + FD_SPANDREL:
    a, b = wbox(n); k = cutter_for(a, b)
    if k is None:
        glass_log[n] = "no opening found"; continue
    op = openings[k]; ax, sgn, back = op["axis"], op["out_sign"], op["back"]
    lo, hi = a.copy(), b.copy()
    lo[ax], hi[ax] = sorted((back - sgn * G_GLASS, back))
    bx = make_box("G_" + n, lo[0], hi[0], lo[1], hi[1], lo[2], hi[2]); bx["src"] = n
    # a slab can cross a neighbouring glazing pocket (NW curtain-wall corner): intersect it with a copy of the body
    bc = bpy.data.objects.new(bx.name + "_bodycopy", B_BODY.data.copy()); WORK.objects.link(bc)
    m_ = boolean(bx, [bc], "INTERSECT", f"slab_in_body_{n}", allow_noop=True, unzip=True)
    if m_["tris"] == 0 or m_["volume_m3"] < 1e-7 or not solid_ok(m_):
        me_ = bx.data; bpy.data.objects.remove(bx); bpy.data.meshes.remove(me_)
        glass_log[n] = "slab outside body (dropped)"; continue
    COL_CLEAR.append(bx); glass_log[n] = k

def clone(o):
    c = bpy.data.objects.new(o.name + "_c", o.data.copy()); WORK.objects.link(c); return c
JOIN_LOG = {}
def union_all(objs, label, name, coll):
    """JOIN (no boolean) the closed colour pieces into one part: a set of closed shells that may overlap or touch.
    Bambu Studio fills overlapping / touching shells of one part as their union (verified with the H2S CLI: two
    half-overlapping 10 mm cubes print exactly the filament of one 15 x 10 x 10 mm box). A Blender union of hundreds of
    touching skin prisms left internal walls that could not be triangulated cleanly."""
    objs = list(objs)
    GUARD_TOL = 0.02 if name.endswith("FRAMES") else 0.003      # frames: documented 0.02 m (see containment)
    def _outside(o, tol=GUARD_TOL):
        bm_ = bmesh.new(); bm_.from_mesh(o.data)
        bmesh.ops.triangulate(bm_, faces=bm_.faces[:], quad_method="BEAUTY", ngon_method="BEAUTY")
        pts_ = [np.array(v.co[:]) for v in bm_.verts] + [np.array(f.calc_center_median()[:]) for f in bm_.faces]; bm_.free()
        return bool(outside_body(pts_, tol))
    if not name.startswith("PRINT_canopy"):
        kept = []
        for o in objs:
            if _outside(o):
                nm = o.name
                bc = bpy.data.objects.new(nm + "_bodycopy2", B_BODY.data.copy()); WORK.objects.link(bc)
                m = boolean(o, [bc], "INTERSECT", f"guard_{nm}", allow_noop=True, unzip=True)
                if m["tris"] == 0 or not solid_ok(m) or _outside(o):
                    CLIP_LOG.append(dict(piece=nm, method="join guard: dropped (outside the body)")); me_ = o.data
                    bpy.data.objects.remove(o); bpy.data.meshes.remove(me_); continue
                CLIP_LOG.append(dict(piece=nm, method="join guard: intersected with body copy", volume_after_m3=round(m["volume_m3"], 5)))
            kept.append(o)
        objs = kept
    V, F = [], []
    for o in objs:
        co_ = getco(o); off = len(V); V.extend(map(tuple, co_))
        F.extend([tuple(i + off for i in p.vertices) for p in o.data.polygons])
    me = bpy.data.meshes.new(name + "_mesh"); me.from_pydata(V, [], F); me.update()
    ob = bpy.data.objects.new(name, me); coll.objects.link(ob)
    for o in objs:
        m_ = o.data; bpy.data.objects.remove(o); bpy.data.meshes.remove(m_)
    JOIN_LOG[name] = dict(shells=len(objs), label=label)
    return ob

t_col = time.time()
for o_ in COL_GRAY_FORCED + COL_CLEAR + COL_WHITE + COL_BLACK + CAN_CLEAR:     # leaf operands as triangles
    triangulate(o_)
P_FRAMES = union_all([clone(o) for o in COL_GRAY_FORCED], "frames_union", "PRINT_building_body_FRAMES", C_BODY)
P_CLEAR = union_all(COL_CLEAR, "clear_union", "PRINT_building_body_CLEAR", C_BODY)
P_BLACK = union_all(skins["BLACK"] + COL_BLACK, "black_union", "PRINT_building_body_BLACK", C_BODY)
P_WHITE = union_all(skins["WHITE"] + COL_WHITE, "white_union", "PRINT_building_body_WHITE", C_BODY)
C_REF = bpy.data.objects["PRINT_canopy_dropoff"]
PC_CLEAR = union_all(CAN_CLEAR, "canopy_clear_union", "PRINT_canopy_dropoff_CLEAR", C_CAN)

def containment(part, ref, tol=0.003):
    """every vertex of a colour part must lie inside its reference part or on its surface (<= tol)"""
    bvh = bvh_of([ref]); co = getco(part); out = []
    bm_ = bmesh.new(); bm_.from_mesh(part.data)                                   # BEAUTY triangulation (as exported)
    bmesh.ops.triangulate(bm_, faces=bm_.faces[:], quad_method="BEAUTY", ngon_method="BEAUTY")
    cen_ = np.array([f.calc_center_median() for f in bm_.faces]) if len(bm_.faces) else np.zeros((0, 3)); bm_.free()
    pts = np.vstack([co, cen_])                    # vertices AND face centroids (a face can cross air)
    for i in outside_body(list(pts), tol, bvh=bvh, tri=_body_tris(ref)):
        dist = bvh.find_nearest(Vector(pts[i]))[3]
        out.append(dict(at=np.round(pts[i], 3).tolist(), dist_m=round(float(dist), 4) if dist is not None else None))
    return out
CONTAIN = {o.name: containment(o, B_BODY) for o in (P_WHITE, P_BLACK, P_CLEAR)}
# FRAMES are copies of the body's own frame operands; the approved v002 body mesh deviates from them by up to ~1 cm on the
# north facade (0.05 mm printed, below the 0.12 mm layer height) - documented tolerance 0.02 m (0.08 mm printed)
CONTAIN[P_FRAMES.name] = containment(P_FRAMES, B_BODY, tol=0.02)
LOG["containment_max_excursion_m"] = {}
CONTAIN[PC_CLEAR.name] = containment(PC_CLEAR, C_REF)

LOG["colour_partition"] = dict(
    method="priority overlay: exact v002 body (gray) + colour parts inside it; later part wins in Bambu Studio",
    part_order_building=["PRINT_building_body (3 gray)", "PRINT_building_body_WHITE (1)", "PRINT_building_body_BLACK (2)",
                         "PRINT_building_body_CLEAR (4)", "PRINT_building_body_FRAMES (3 gray)"],
    part_order_canopy=["PRINT_canopy_dropoff (3 gray)", "PRINT_canopy_dropoff_CLEAR (4)"],
    mapping={"1 WHITE": "white metal paneling ACM-1/ACM-4, MTL-2 coping, white TPO roofs + terrace tops, sun-shade (paint match ACM-1)",
             "2 BLACK": "black metal paneling ACM-2/ACM-3, MTL-1/MTL-3 copings",
             "3 GRAY": "gray brick BRK-1 + brick caps, storefront/curtain-wall frames (Beachstone Gray), canopy steel, interior core, site base",
             "4 CLEAR": "vision + spandrel glass (as recess-back slabs), glass railings, canopy glass"},
    skin_depth_m=D_SKIN, glass_slab_depth_m=G_GLASS, skins={k: dict(v) for k, v in skin_log.items()},
    prisms={k: len(v) for k, v in skins.items()}, glass_slabs=glass_log,
    forced_gray=FG_COUNT, forced_white=FW_NAMES, forced_black=FB_NAMES,
    pinch_vertices_unzipped=dict(UNZIP_LOG), clipped_to_body=CLIP_LOG, skin_geometry=SKIN_GEOM, joined_shells=JOIN_LOG,
    manifold_nonplanar_ngon_repair={k: dict(v) for k, v in REPAIR_LOG.items()},
    containment_violations={k: v[:20] for k, v in CONTAIN.items()}, containment_violation_counts={k: len(v) for k, v in CONTAIN.items()},
    seconds=round(time.time() - t_col, 1))
for o in BODY_OPS:
    if o.name in bpy.data.objects:
        me_ = o.data; bpy.data.objects.remove(o); bpy.data.meshes.remove(me_)
print(f"[build] colour parts in {time.time()-t_col:.1f}s; containment violations {LOG['colour_partition']['containment_violation_counts']}")

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
                                     for n in ("PRINT_building_body", "PRINT_site_base", "PRINT_canopy_dropoff", "PRINT_sunshade",
                                               "PRINT_building_body_WHITE", "PRINT_building_body_BLACK", "PRINT_building_body_CLEAR",
                                               "PRINT_building_body_FRAMES", "PRINT_canopy_dropoff_CLEAR")}

# ================================================================== finalise: keep only PRINT parts
final = {"PRINT_building_body": C_BODY, "PRINT_building_body_WHITE": C_BODY, "PRINT_building_body_BLACK": C_BODY,
         "PRINT_building_body_CLEAR": C_BODY, "PRINT_building_body_FRAMES": C_BODY,
         "PRINT_canopy_dropoff": C_CAN, "PRINT_canopy_dropoff_CLEAR": C_CAN,
         "PRINT_sunshade": C_SUN, "PRINT_site_base": C_SITE}
SLOT = {"WHITE": (1, (0.93, 0.93, 0.91, 1.0)), "BLACK": (2, (0.06, 0.06, 0.07, 1.0)), "GRAY": (3, (0.50, 0.51, 0.50, 1.0)),
        "CLEAR": (4, (0.72, 0.84, 0.90, 0.55))}
PART_COLOUR = {"PRINT_building_body": "GRAY", "PRINT_building_body_WHITE": "WHITE", "PRINT_building_body_BLACK": "BLACK",
               "PRINT_building_body_CLEAR": "CLEAR", "PRINT_building_body_FRAMES": "GRAY",
               "PRINT_canopy_dropoff": "GRAY", "PRINT_canopy_dropoff_CLEAR": "CLEAR",
               "PRINT_sunshade": "WHITE", "PRINT_site_base": "GRAY"}
PART_ORDER = {"PRINT_building_body": 1, "PRINT_building_body_WHITE": 2, "PRINT_building_body_BLACK": 3, "PRINT_building_body_CLEAR": 4,
              "PRINT_building_body_FRAMES": 5, "PRINT_canopy_dropoff": 1, "PRINT_canopy_dropoff_CLEAR": 2, "PRINT_sunshade": 1, "PRINT_site_base": 1}
for name in final:
    o = bpy.data.objects[name]
    cname = PART_COLOUR[name]; slot, rgba = SLOT[cname]
    mat = bpy.data.materials.get("PRINT_" + cname) or bpy.data.materials.new("PRINT_" + cname)
    mat.diffuse_color = rgba
    o.color = rgba
    o["filament_slot"] = slot; o["filament_colour"] = cname; o["part_order"] = PART_ORDER[name]
    o["note"] = {"PRINT_building_body": "exact v002 building body (unchanged geometry) - gray base; colour parts overlay it",
                 "PRINT_canopy_dropoff": "exact v002 drop-off canopy (unchanged geometry) - gray base; the clear glass part overlays it"}.get(
        name, "colour overlay part inside its base part; later part wins in Bambu Studio" if name.endswith(("_WHITE", "_BLACK", "_CLEAR", "_FRAMES")) else "exact v002 part")
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
    if c.name not in ("PRINT_v003",) and c.name not in {cc.name for cc in final.values()}:
        bpy.data.collections.remove(c)
bpy.data.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
sc["print_derivative"] = json.dumps({"version": "print_v003 (multicolor of v002 geometry, priority-overlay colour parts)",
                                      "source": "building_shell_v023.blend (via pristine audit copy)",
                                      "scale": f"1:{SCALE}", "units": "metres (real)", "openings": openings,
                                      "crop_window": CROP, "built": time.strftime("%Y-%m-%d %H:%M")})
LOG["nonplanar_faces"] = {name: nonplanar_faces(bpy.data.objects[name]) for name in final}
LOG["final_parts"] = {name: metrics(bpy.data.objects[name]) for name in final}
LOG["runtime_s"] = round(time.time() - T0, 1)
COLOUR_PARTS = ("PRINT_building_body_WHITE", "PRINT_building_body_BLACK", "PRINT_building_body_CLEAR", "PRINT_building_body_FRAMES",
                "PRINT_canopy_dropoff_CLEAR")
bad = [n for n, m in LOG["final_parts"].items() if not (solid_ok(m) and (m["islands"] == 1 or n in COLOUR_PARTS))]
bad += [f"{n}: {k} non-planar faces" for n, k in LOG["nonplanar_faces"].items() if k and n in COLOUR_PARTS]
bad += [f"{n}: {k} vertices outside its base part" for n, k in LOG["colour_partition"]["containment_violation_counts"].items() if k]
V2 = json.load(open(os.path.join(VAL, "print_prep_v002_build_log.json"), encoding="utf-8"))["final_parts"]
LOG["unchanged_vs_v002"] = {n: dict(tris=(LOG["final_parts"][n]["tris"], V2[n]["tris"]),
                                    volume_m3=(round(LOG["final_parts"][n]["volume_m3"], 6), round(V2[n]["volume_m3"], 6)))
                            for n in ("PRINT_building_body", "PRINT_site_base", "PRINT_canopy_dropoff", "PRINT_sunshade") if n in V2}
for n, v in LOG["unchanged_vs_v002"].items():
    if v["tris"][0] != v["tris"][1] or abs(v["volume_m3"][0] - v["volume_m3"][1]) > 1e-6 * max(1.0, abs(v["volume_m3"][1])):
        bad.append(f"{n}: differs from v002")
def island_report(ob):
    me = ob.data; co = getco(ob)
    ed = np.empty(len(me.edges) * 2, dtype=np.int64); me.edges.foreach_get("vertices", ed); ed = ed.reshape(-1, 2)
    lab = islands(len(co), ed)
    return [dict(verts=int((lab == L).sum()), bbox_min=co[lab == L].min(0).round(3).tolist(), bbox_max=co[lab == L].max(0).round(3).tolist())
            for L in np.unique(lab)]
LOG["island_report"] = {n: island_report(bpy.data.objects[n]) for n in bad if n in bpy.data.objects}
LOG["save_gate_failures"] = bad
os.makedirs(VAL, exist_ok=True)
with open(os.path.join(VAL, "print_prep_v003_build_log.json"), "w", encoding="utf-8") as f:
    json.dump(LOG, f, indent=1, default=lambda x: x.tolist() if hasattr(x, "tolist") else str(x))
if bad:
    raise SystemExit(f"[build] NOT SAVED - save gate: {bad}")
bpy.ops.wm.save_mainfile(filepath=BLEND, compress=True)
print(f"[build] saved {BLEND} in {time.time()-T0:.1f}s")
