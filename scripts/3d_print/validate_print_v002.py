"""Building II print derivative v002 - independent VALIDATION of the prepared print parts (read-only).

Run:  blender -b models/Building_II/print_derivatives/building_II_print_v002.blend \
            --python scripts/3d_print/validate_print_v002.py
Never saves. Writes exports/Building_II/3d_print/validation/print_validation_v001.json
and print_validation_v001_thin_regions.csv.
Checks: watertight / manifold / normals / components, physical size at 1:250 and H2S fit,
ray-cast wall thickness on every triangle, glazing-recess depth, assembly clearances and
overlaps between parts, and surfaces that would need print supports in the intended orientation.
"""
import bpy, bmesh, csv, json, math, os, time
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

T0 = time.time()
BLEND = bpy.data.filepath
ROOT = os.path.abspath(os.path.join(os.path.dirname(BLEND), "..", "..", ".."))
VAL = os.path.join(ROOT, "exports", "Building_II", "3d_print", "validation")
SCALE = 240.0
MM = 1000.0 / SCALE            # printed mm per real metre (4.1667)
BED = (340.0, 320.0, 340.0); MARGIN = 10.0
PARTS = ["PRINT_building_body", "PRINT_site_base", "PRINT_canopy_dropoff", "PRINT_sunshade"]
ORIENT = {"PRINT_building_body": "upright", "PRINT_site_base": "upright",
          "PRINT_canopy_dropoff": "on its south edge (rotated +90 deg about X: real +Y points up)",
          "PRINT_sunshade": "inverted (top face on bed)"}
ROT = {"PRINT_building_body": np.eye(3), "PRINT_site_base": np.eye(3),
       "PRINT_canopy_dropoff": np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]], float),
       "PRINT_sunshade": np.diag([1.0, -1.0, -1.0])}
info = json.loads(bpy.context.scene["print_derivative"])

def arrays(ob):
    me = ob.data; me.calc_loop_triangles()
    co = np.empty(len(me.vertices) * 3); me.vertices.foreach_get("co", co); co = co.reshape(-1, 3)
    M = np.array(ob.matrix_world); co = co @ M[:3, :3].T + M[:3, 3]
    ed = np.empty(len(me.edges) * 2, dtype=np.int64); me.edges.foreach_get("vertices", ed); ed = ed.reshape(-1, 2)
    lv = np.empty(len(me.loops), dtype=np.int64); me.loops.foreach_get("vertex_index", lv)
    le = np.empty(len(me.loops), dtype=np.int64); me.loops.foreach_get("edge_index", le)
    tv = np.empty(len(me.loop_triangles) * 3, dtype=np.int64); me.loop_triangles.foreach_get("vertices", tv)
    return co, ed, lv, le, tv.reshape(-1, 3)

def islands(nv, ed):
    lab = np.arange(nv); a, b = ed[:, 0], ed[:, 1]
    while True:
        old = lab.copy(); m = np.minimum(lab[a], lab[b])
        np.minimum.at(lab, a, m); np.minimum.at(lab, b, m); lab = lab[lab]
        if np.array_equal(lab, old):
            return lab

def rot_fit(a, b, A, B):
    for deg in np.arange(0, 90.01, 0.5):
        t = math.radians(deg); w = a * math.cos(t) + b * math.sin(t); h = a * math.sin(t) + b * math.cos(t)
        if (w <= A and h <= B) or (w <= B and h <= A):
            return float(deg)
    return None

R = {"blend": BLEND, "scale": "1:240", "printer_bed_mm": BED, "planning_margin_mm": MARGIN, "parts": {}, "assembly": {}}
data = {}
thin_rows = []
for name in PARTS:
    ob = bpy.data.objects[name]
    co, ed, lv, le, tv = arrays(ob)
    ne = len(ed)
    fpe = np.bincount(le, minlength=ne)
    sign = np.where(lv == ed[le, 0], 1, -1); ssum = np.bincount(le, weights=sign, minlength=ne)
    p0, p1, p2 = co[tv[:, 0]], co[tv[:, 1]], co[tv[:, 2]]
    cr = np.cross(p1 - p0, p2 - p0); area = 0.5 * np.linalg.norm(cr, axis=1)
    nrm = cr / np.maximum(np.linalg.norm(cr, axis=1), 1e-30)[:, None]
    vol = float(np.einsum("ij,ij->i", p0, np.cross(p1, p2)).sum() / 6.0)
    lab = islands(len(co), ed)
    lo, hi = co.min(0), co.max(0); size = hi - lo; mm = size * MM
    bvh = BVHTree.FromPolygons([tuple(v) for v in co], [tuple(t) for t in tv], epsilon=0.0)
    data[name] = dict(co=co, tv=tv, bvh=bvh, nrm=nrm, area=area)
    # ray-cast wall thickness from every triangle centroid, inward
    cen = (p0 + p1 + p2) / 3.0
    th = np.full(len(tv), np.nan)
    for i in range(len(tv)):
        if area[i] < 1e-10:
            continue
        o = Vector(cen[i] - nrm[i] * 1e-4); d = Vector(-nrm[i])
        hit = bvh.ray_cast(o, d, 100.0)
        if hit[0] is not None:
            th[i] = hit[3] + 1e-4
    valid = ~np.isnan(th) & (area >= 1e-10)
    th_mm = th * MM
    a_tot = area[valid].sum()
    def frac(lim):
        m = valid & (th_mm < lim - 0.02); return float(area[m].sum() / a_tot), int(m.sum())
    nh = (area >= 1e-10) & np.isnan(th)
    no_hit = int(nh.sum()); no_hit_area_mm2 = float(area[nh].sum()) * MM * MM
    # cluster thin triangles (< 0.8 mm) by 0.5 m cells for the report
    thin = valid & (th_mm < 0.98)
    cells = {}
    for i in np.where(thin)[0]:
        k = tuple(np.floor(cen[i] / 0.5).astype(int))
        c = cells.setdefault(k, dict(n=0, area=0.0, min_mm=9e9, xyz=cen[i].copy()))
        c["n"] += 1; c["area"] += area[i]; c["min_mm"] = min(c["min_mm"], th_mm[i])
    for k, c in sorted(cells.items(), key=lambda kv: kv[1]["min_mm"]):
        thin_rows.append(dict(part=name, x=round(c["xyz"][0], 2), y=round(c["xyz"][1], 2), z=round(c["xyz"][2], 2),
                              triangles=c["n"], area_m2=round(c["area"], 4), min_thickness_mm=round(c["min_mm"], 3)))
    # support analysis in intended print orientation
    def support_area(Rm):
        nz = (nrm @ Rm.T)[:, 2]; cz = (cen @ Rm.T)[:, 2]
        down = (nz < -math.cos(math.radians(45))) & (cz > cz.min() + 0.01)
        return round(float(area[down].sum()) * MM * MM, 1)
    R["parts"][name] = dict(
        vertices=len(co), triangles=len(tv), boundary_edges=int((fpe == 1).sum()), nonmanifold_edges=int((fpe > 2).sum()),
        wire_edges=int((fpe == 0).sum()), inconsistent_normal_edges=int(((fpe == 2) & (np.abs(ssum) == 2)).sum()),
        volume_m3_real=round(vol, 3), volume_cm3_printed=round(vol * MM ** 3 / 1000.0, 2), outward_normals=vol > 0,
        disconnected_components=int(len(np.unique(lab))), zero_area_triangles=int((area < 1e-10).sum()),
        bbox_real_m=dict(min=lo.round(3).tolist(), max=hi.round(3).tolist(), size=size.round(3).tolist()),
        printed_size_mm=mm.round(1).tolist(),
        fits_bed_mm=bool(rot_fit(mm[0], mm[1], BED[0], BED[1]) is not None and mm[2] <= BED[2]),
        fits_with_margin=bool(rot_fit(mm[0], mm[1], BED[0] - 2 * MARGIN, BED[1] - 2 * MARGIN) is not None and mm[2] <= BED[2] - MARGIN),
        bed_margin_each_side_mm=[round((BED[0] - mm[0]) / 2, 1), round((BED[1] - mm[1]) / 2, 1)],
        thickness_rays=dict(triangles_tested=int(valid.sum()), rays_without_exit=no_hit, rays_without_exit_area_mm2=round(no_hit_area_mm2, 3),
                            min_mm=round(float(np.nanmin(th_mm[valid])), 3),
                            p1_mm=round(float(np.nanpercentile(th_mm[valid], 1)), 3),
                            area_fraction_below_0_4mm=frac(0.4)[0], area_fraction_below_0_5mm=frac(0.5)[0],
                            area_fraction_below_0_8mm=frac(0.8)[0], triangles_below_0_4mm=frac(0.4)[1],
                            triangles_below_0_8mm=frac(0.8)[1], thin_cells_0_5m=len(cells)),
        print_orientation=ORIENT[name],
        support_needed_area_mm2=support_area(ROT[name]),
        support_area_upright_mm2=support_area(np.eye(3)), support_area_inverted_mm2=support_area(np.diag([1.0, -1.0, -1.0])),
        area_fraction_below_0_7mm=frac(0.7)[0], area_fraction_below_1_0mm=frac(1.0)[0],
        watertight=bool((fpe == 1).sum() == 0 and (fpe > 2).sum() == 0 and ((fpe == 2) & (np.abs(ssum) == 2)).sum() == 0 and vol > 0))
    print(f"[validate] {name}: {R['parts'][name]['printed_size_mm']} mm, thin<0.8mm tris {R['parts'][name]['thickness_rays']['triangles_below_0_8mm']}  ({time.time()-T0:.1f}s)")

# ------------------------------------------------------------------ glazing recess depth per opening
body = data["PRINT_building_body"]; bb = body["bvh"]
rec = {}
for k, op in info["openings"].items():
    a, b = np.array(op["min"]), np.array(op["max"]); ax, s = op["axis"], op["out_sign"]
    pa = 1 - ax
    out_face = []
    for off in ((a[pa] - 0.15, (a[2] + b[2]) / 2), (b[pa] + 0.15, (a[2] + b[2]) / 2), ((a[pa] + b[pa]) / 2, b[2] + 0.15)):
        p = np.zeros(3); p[pa] = off[0]; p[2] = off[1]; p[ax] = op["back"] + s * 3.0
        d = np.zeros(3); d[ax] = -s
        hit = bb.ray_cast(Vector(p), Vector(d), 6.0)
        if hit[0] is not None:
            out_face.append(hit[0][ax] * s)
    backs = []
    for u in np.linspace(0.1, 0.9, 9):
        for v in np.linspace(0.1, 0.9, 7):
            p = np.zeros(3); p[pa] = a[pa] + u * (b[pa] - a[pa]); p[2] = a[2] + v * (b[2] - a[2]); p[ax] = op["back"] + s * 3.0
            d = np.zeros(3); d[ax] = -s
            hit = bb.ray_cast(Vector(p), Vector(d), 6.0)
            if hit[0] is not None:
                backs.append(hit[0][ax] * s)
    if out_face and backs:
        face = float(max(out_face)); deepest = min(backs)   # facade plane = outermost surface beside the opening
        rec[k] = dict(recess_depth_m=round(face - deepest, 4), recess_depth_mm=round((face - deepest) * MM, 2),
                      rib_or_back_hits=len(backs))
R["glazing_recess"] = dict(openings=len(info["openings"]), measured=len(rec),
                           min_depth_mm=min(v["recess_depth_mm"] for v in rec.values()),
                           max_depth_mm=max(v["recess_depth_mm"] for v in rec.values()), per_opening=rec)

# ------------------------------------------------------------------ assembly: overlaps and clearances
def overlap_volume(a, b):
    """Volume of A ∩ B using a temporary boolean on in-memory copies (never saved)."""
    A = bpy.data.objects[a].copy(); A.data = bpy.data.objects[a].data.copy()
    B = bpy.data.objects[b].copy(); B.data = bpy.data.objects[b].data.copy()
    bpy.context.scene.collection.objects.link(A); bpy.context.scene.collection.objects.link(B)
    m = A.modifiers.new("i", "BOOLEAN"); m.operation = "INTERSECT"; m.object = B; m.solver = "MANIFOLD"
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(A.evaluated_get(dg)); me.calc_loop_triangles()
    co = np.array([v.co for v in me.vertices]).reshape(-1, 3)
    tv = np.array([t.vertices[:] for t in me.loop_triangles]).reshape(-1, 3)
    v = float(np.einsum("ij,ij->i", co[tv[:, 0]], np.cross(co[tv[:, 1]], co[tv[:, 2]])).sum() / 6.0) if len(tv) else 0.0
    for o in (A, B):
        d_ = o.data; bpy.data.objects.remove(o); bpy.data.meshes.remove(d_)
    bpy.data.meshes.remove(me)
    return v

def surface_samples(name, step=0.05):
    co, tv = data[name]["co"], data[name]["tv"]; pts = [co]
    rng = np.random.default_rng(0)
    for t in tv:
        p0, p1, p2 = co[t[0]], co[t[1]], co[t[2]]
        a = 0.5 * np.linalg.norm(np.cross(p1 - p0, p2 - p0))
        n = int(min(400, a / (step * step)))
        if n:
            u = rng.random((n, 2)); m = u.sum(1) > 1; u[m] = 1 - u[m]
            pts.append(p0 + u[:, :1] * (p1 - p0) + u[:, 1:] * (p2 - p0))
    return np.vstack(pts)

def min_gap(src, dst, zmax=None, zmin=None, lateral_only=False):
    co = surface_samples(src); bv = data[dst]["bvh"]
    sel = np.ones(len(co), bool)
    if zmax is not None: sel &= co[:, 2] < zmax
    if zmin is not None: sel &= co[:, 2] > zmin
    best = 9e9
    for v in co[sel]:
        hit = bv.find_nearest(Vector(v), 5.0)
        if hit[0] is not None:
            best = min(best, hit[3])
    return None if best == 9e9 else best

pairs = [("PRINT_building_body", "PRINT_site_base"), ("PRINT_canopy_dropoff", "PRINT_site_base"),
         ("PRINT_canopy_dropoff", "PRINT_building_body"), ("PRINT_sunshade", "PRINT_building_body"),
         ("PRINT_sunshade", "PRINT_canopy_dropoff")]
for a, b in pairs:
    R["assembly"][f"{a} x {b}"] = dict(overlap_volume_m3=round(overlap_volume(a, b), 6))
zf = R["parts"]["PRINT_building_body"]["bbox_real_m"]["min"][2]
g1 = min_gap("PRINT_building_body", "PRINT_site_base", zmax=5.0, zmin=zf + 0.3)      # side walls of the pocket
g2 = min_gap("PRINT_canopy_dropoff", "PRINT_site_base", zmax=-0.20, zmin=-0.40)     # socket side walls (below the lead-in flare, above the foot chamfer)
g3 = min_gap("PRINT_canopy_dropoff", "PRINT_building_body")
g4 = min_gap("PRINT_sunshade", "PRINT_building_body")
def gp(g): return dict(m=None if g is None else round(g, 4), mm=None if g is None else round(g * MM, 3))
R["assembly"]["body_to_base_pocket_wall_gap"] = gp(g1)
R["assembly"]["canopy_column_to_socket_wall_gap"] = gp(g2)
R["assembly"]["canopy_to_body_min_gap"] = gp(g3)
R["assembly"]["sunshade_to_body_contact_gap"] = gp(g4)
R["assembly"]["body_bottom_z"] = zf
R["assembly"]["pocket_floor_z"] = zf
allco = np.vstack([data[p]["co"] for p in PARTS]); lo, hi = allco.min(0), allco.max(0)
R["assembly"]["assembled_size_real_m"] = (hi - lo).round(3).tolist()
R["assembly"]["assembled_size_mm"] = ((hi - lo) * MM).round(1).tolist()

# ------------------------------------------------------------------ v002-specific checks
import bmesh
def section_area(ob, y0, y1, z0=-100.0, z1=100.0):
    """material cross-section (m2) of `ob` in the slab y0..y1 (between z0 and z1) = volume / thickness"""
    A = ob.copy(); A.data = ob.data.copy(); bpy.context.scene.collection.objects.link(A)
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = Vector((-100 if v.co.x < 0 else 200, y0 if v.co.y < 0 else y1, z0 if v.co.z < 0 else z1))
    me = bpy.data.meshes.new("slab"); bm.to_mesh(me); bm.free()
    S = bpy.data.objects.new("slab", me); bpy.context.scene.collection.objects.link(S)
    m = A.modifiers.new("i", "BOOLEAN"); m.operation = "INTERSECT"; m.object = S; m.solver = "MANIFOLD"
    dg = bpy.context.evaluated_depsgraph_get(); r = bpy.data.meshes.new_from_object(A.evaluated_get(dg))
    bmr = bmesh.new(); bmr.from_mesh(r); vol = abs(bmr.calc_volume()); bmr.free()
    for o in (A, S):
        d_ = o.data; bpy.data.objects.remove(o); bpy.data.meshes.remove(d_)
    bpy.data.meshes.remove(r)
    return vol / (y1 - y0)

# porte cochere: material joining the south (rear) wing to the rest, measured in the open valley (y 34.43-34.65)
v001_path = os.path.join(os.path.dirname(BLEND), "building_II_print_v001.blend")
with bpy.data.libraries.load(v001_path, link=False) as (src, dst):
    dst.objects = ["PRINT_canopy_dropoff"]
can01 = dst.objects[0]; bpy.context.scene.collection.objects.link(can01)
can02 = bpy.data.objects["PRINT_canopy_dropoff"]
joint = {}
for tag, ob in (("v001", can01), ("v002", can02)):
    joint[tag] = dict(section_m2_at_valley_above_column_tops=round(section_area(ob, 34.50, 34.60, 4.62, 10.0), 4),
                      section_m2_at_valley_incl_columns=round(section_area(ob, 34.50, 34.60), 4))
# is the tie really under the valley along the whole length? rays down through the valley gap
cbvh = data["PRINT_canopy_dropoff"]["bvh"]; tie_hits = []
for x in np.linspace(24.0, 43.2, 25):
    h = cbvh.ray_cast(Vector((x, 34.54, 8.0)), Vector((0, 0, -1)), 20.0)
    tie_hits.append(None if h[0] is None else round(h[0][2], 3))
R["porte_cochere"] = dict(joint_section=joint,
                          note="above the column tops (z > 4.62 m) the v001 wings were not joined at all; the rear wing hung on the three column tops",
                          valley_rays_hit_tie_at_z=sorted(set(tie_hits)), valley_rays=len(tie_hits))
bpy.data.objects.remove(can01)

# sun-shade: measure bars and clear gaps along scan lines between the outriggers
sbvh = data["PRINT_sunshade"]["bvh"]
def scan(fixed_axis, fixed, a0, a1, step=0.002):
    hits = []
    for t in np.arange(a0, a1, step):
        p = [0, 0, 11.0]; p[fixed_axis] = fixed; p[1 - fixed_axis] = t
        h = sbvh.ray_cast(Vector(p), Vector((0, 0, -1)), 5.0)
        hits.append(h[0] is not None)
    runs, cur, n = [], hits[0], 0
    for hh in hits:
        if hh == cur: n += 1
        else: runs.append((cur, n * step)); cur, n = hh, 1
    runs.append((cur, n * step))
    inner = runs[1:-1]
    return dict(bars_m=[round(w, 3) for h, w in inner if h], gaps_m=[round(w, 3) for h, w in inner if not h])
sun = {"south (x=12.0)": scan(0, 12.0, 3.2, 6.95), "east (y=12.2)": scan(1, 12.2, 53.0, 56.9), "north (x=45.6)": scan(0, 45.6, 24.1, 27.9)}
allg = [g for v in sun.values() for g in v["gaps_m"]]; allb = [b for v in sun.values() for b in v["bars_m"]]
R["sunshade_scan"] = dict(lines=sun, min_gap_mm=round(min(allg) * MM, 3), max_gap_mm=round(max(allg) * MM, 3),
                          min_bar_mm=round(min(allb) * MM, 3), step_mm=round(0.002 * MM, 4))
R["runtime_s"] = round(time.time() - T0, 1)
R["file_is_dirty_after_checks"] = bool(bpy.data.is_dirty)
os.makedirs(VAL, exist_ok=True)
with open(os.path.join(VAL, "print_validation_v002.json"), "w", encoding="utf-8") as f:
    json.dump(R, f, indent=1)
with open(os.path.join(VAL, "print_validation_v002_thin_regions.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(thin_rows[0].keys()) if thin_rows else ["part"]); w.writeheader(); w.writerows(thin_rows)
print(f"[validate] done in {time.time()-T0:.1f}s (never saved)")
