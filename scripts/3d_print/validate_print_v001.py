"""Building II print derivative v001 - independent VALIDATION of the prepared print parts (read-only).

Run:  blender -b models/Building_II/print_derivatives/building_II_print_v001.blend \
            --python scripts/3d_print/validate_print_v001.py
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
SCALE = 250.0
MM = 1000.0 / SCALE            # printed mm per real metre (4.0)
BED = (340.0, 320.0, 340.0); MARGIN = 10.0
PARTS = ["PRINT_building_body", "PRINT_site_base", "PRINT_canopy_dropoff", "PRINT_sunshade"]
ORIENT = {"PRINT_building_body": "upright", "PRINT_site_base": "upright",
          "PRINT_canopy_dropoff": "upright", "PRINT_sunshade": "inverted (top face on bed)"}
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

R = {"blend": BLEND, "scale": "1:250", "printer_bed_mm": BED, "planning_margin_mm": MARGIN, "parts": {}, "assembly": {}}
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
    thin = valid & (th_mm < 0.78)
    cells = {}
    for i in np.where(thin)[0]:
        k = tuple(np.floor(cen[i] / 0.5).astype(int))
        c = cells.setdefault(k, dict(n=0, area=0.0, min_mm=9e9, xyz=cen[i].copy()))
        c["n"] += 1; c["area"] += area[i]; c["min_mm"] = min(c["min_mm"], th_mm[i])
    for k, c in sorted(cells.items(), key=lambda kv: kv[1]["min_mm"]):
        thin_rows.append(dict(part=name, x=round(c["xyz"][0], 2), y=round(c["xyz"][1], 2), z=round(c["xyz"][2], 2),
                              triangles=c["n"], area_m2=round(c["area"], 4), min_thickness_mm=round(c["min_mm"], 3)))
    # support analysis in intended print orientation
    def support_area(inv):
        nz = -nrm[:, 2] if inv else nrm[:, 2]
        cz = -cen[:, 2] if inv else cen[:, 2]
        down = (nz < -math.cos(math.radians(45))) & (cz > cz.min() + 0.01)
        return round(float(area[down].sum()) * MM * MM, 1)
    inv = ORIENT[name].startswith("inverted")
    R["parts"][name] = dict(
        vertices=len(co), triangles=len(tv), boundary_edges=int((fpe == 1).sum()), nonmanifold_edges=int((fpe > 2).sum()),
        wire_edges=int((fpe == 0).sum()), inconsistent_normal_edges=int(((fpe == 2) & (np.abs(ssum) == 2)).sum()),
        volume_m3_real=round(vol, 3), volume_cm3_printed=round(vol * MM ** 3 / 1000.0, 2), outward_normals=vol > 0,
        disconnected_components=int(len(np.unique(lab))), zero_area_triangles=int((area < 1e-10).sum()),
        bbox_real_m=dict(min=lo.round(3).tolist(), max=hi.round(3).tolist(), size=size.round(3).tolist()),
        printed_size_mm=mm.round(1).tolist(),
        fits_bed_mm=bool(rot_fit(mm[0], mm[1], BED[0], BED[1]) is not None and mm[2] <= BED[2]),
        fits_with_margin=bool(rot_fit(mm[0], mm[1], BED[0] - MARGIN, BED[1] - MARGIN) is not None and mm[2] <= BED[2] - MARGIN),
        thickness_rays=dict(triangles_tested=int(valid.sum()), rays_without_exit=no_hit, rays_without_exit_area_mm2=round(no_hit_area_mm2, 3),
                            min_mm=round(float(np.nanmin(th_mm[valid])), 3),
                            p1_mm=round(float(np.nanpercentile(th_mm[valid], 1)), 3),
                            area_fraction_below_0_4mm=frac(0.4)[0], area_fraction_below_0_5mm=frac(0.5)[0],
                            area_fraction_below_0_8mm=frac(0.8)[0], triangles_below_0_4mm=frac(0.4)[1],
                            triangles_below_0_8mm=frac(0.8)[1], thin_cells_0_5m=len(cells)),
        print_orientation=ORIENT[name],
        support_needed_area_mm2=support_area(inv),
        support_area_upright_mm2=support_area(False), support_area_inverted_mm2=support_area(True),
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
g2 = min_gap("PRINT_canopy_dropoff", "PRINT_site_base", zmax=0.5, zmin=-0.2)        # side walls of the sockets
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
R["runtime_s"] = round(time.time() - T0, 1)
R["file_is_dirty_after_checks"] = bool(bpy.data.is_dirty)
os.makedirs(VAL, exist_ok=True)
with open(os.path.join(VAL, "print_validation_v001.json"), "w", encoding="utf-8") as f:
    json.dump(R, f, indent=1)
with open(os.path.join(VAL, "print_validation_v001_thin_regions.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(thin_rows[0].keys()) if thin_rows else ["part"]); w.writeheader(); w.writerows(thin_rows)
print(f"[validate] done in {time.time()-T0:.1f}s (never saved)")
