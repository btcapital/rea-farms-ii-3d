r"""Building I - main entrance / porte-cochere site correction v010 (after BI_entrance_site_audit_v010.md).

Opens BI_presentation_v009.blend (v008 approved building + v009 materials) and, using BI_entrance_site_data_v010.json:
  * replaces SITE_asphalt_west_drive_dropoff with the documented drive loop (CS-101 face-of-curb lines + the correct v003 part),
  * adds the median island (planted oval + paved nose), the 12.20 ft parking end island, the canopy plaza pavers, the
    diagonal 7 ft walk and the aisle 8/8.5 ft walk (CS-101), all terrain-following as in v003,
  * regrades the interpolated terrain inside the window x -130..90, y 60..215 from the spot set cleaned of the 42
    storm-drainage-chart values, omitting cells under pavement,
  * rebuilds every landscape object whose bounding box intersects the window at its documented x,y with the corrected grade
    (z only; every plant's z_old -> z_new is recorded),
  * adds three validation cameras.
Everything else (building, openings, canopy, facade regions, all other site and landscape objects, every material node tree)
is hashed before/after and must be identical. Saves models/Building_I/BI_entrance_site_v010.blend and renders
renders/Building_I/BI_entrance_site_v010_*.png with the v009 presentation settings.

Run:  "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --background --python scripts/Building_I/BI_build_entrance_site_v010.py
Optional:  -- --no-render   |   -- --out <folder>   |   -- --samples N   |   -- --views a,b
"""
import hashlib
import importlib.util
import json
import math
import sys
import time
from pathlib import Path

import bmesh
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parent.parent.parent
BASE = ROOT / "models" / "Building_I" / "BI_presentation_v009.blend"
DATA = ROOT / "notes" / "Building_I" / "BI_entrance_site_data_v010.json"
SITE = ROOT / "notes" / "Building_I" / "BI_site_data_v003.json"
LAND = ROOT / "notes" / "Building_I" / "BI_landscape_data_v007.json"
FOOT = ROOT / "notes" / "Building_I" / "BI_footprint_data_v008.json"
GEOM = ROOT / "notes" / "Building_I" / "BI_geometry_data_v001.json"
STEM = "BI_entrance_site_v010"
FT = 0.3048
FFE = 661.75


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / "Building_I" / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


v4 = _load("v4", "BI_build_landscape_v004.py")   # point_in_poly, push_outside, add_sphere, add_disc, add_cylinder, add_prism, new_object, geometry_hash
v8 = _load("v8", "BI_build_footprint_fix_v008.py")  # clean_poly, ear_clip, v1.rect
m = v4.m
geometry_hash = v4.geometry_hash
point_in_poly = v4.point_in_poly


def mat_sig(mt):
    h = hashlib.sha256()
    if mt.use_nodes and mt.node_tree:
        for n in sorted(mt.node_tree.nodes, key=lambda x: x.name):
            h.update(n.bl_idname.encode())
            for i in n.inputs:
                dv = getattr(i, "default_value", None)
                try:
                    h.update(json.dumps(list(dv) if hasattr(dv, "__len__") else dv).encode())
                except TypeError:
                    pass
        for l in mt.node_tree.links:
            h.update(f"{l.from_node.bl_idname}.{l.from_socket.name}->{l.to_node.bl_idname}.{l.to_socket.name}".encode())
    return h.hexdigest()


def bbox_ft(o):
    pts = [o.matrix_world @ Vector(c) for c in o.bound_box]
    return [min(p.x for p in pts) / FT, min(p.y for p in pts) / FT, min(p.z for p in pts) / FT,
            max(p.x for p in pts) / FT, max(p.y for p in pts) / FT, max(p.z for p in pts) / FT]


def ear_clip_tolerant(pts):
    """v008 ear clipping; if it stalls on a raster-traced outline, drop the most degenerate remaining vertex and retry."""
    pts = list(pts)
    for _ in range(50):
        try:
            return pts, v8.ear_clip(pts)
        except RuntimeError:
            n = len(pts)
            worst = min(range(n), key=lambda i: abs((pts[i][0] - pts[i - 1][0]) * (pts[(i + 1) % n][1] - pts[i - 1][1]) - (pts[i][1] - pts[i - 1][1]) * (pts[(i + 1) % n][0] - pts[i - 1][0])))
            del pts[worst]
    raise RuntimeError("polygon could not be triangulated")


def slab_robust(name, poly, zfunc, thick, col, mat, maxedge=6.0):
    """Terrain-following slab (as v003 slab()) but with a verified ear-clip triangulation of the outline."""
    pts = v8.clean_poly(poly)
    pts, tris = ear_clip_tolerant(pts)
    area_poly = v8.poly_area(pts)
    area_tri = sum(abs((pts[b][0] - pts[a][0]) * (pts[c][1] - pts[a][1]) - (pts[b][1] - pts[a][1]) * (pts[c][0] - pts[a][0])) / 2 for a, b, c in tris)
    assert abs(area_tri - area_poly) < 5e-3 * max(1.0, area_poly), f"{name}: triangulation area {area_tri:.1f} != polygon {area_poly:.1f}"
    bm = bmesh.new()
    vs = [bm.verts.new((m(x), m(y), 0.0)) for x, y in pts]
    for a, b, c in tris:
        bm.faces.new((vs[a], vs[b], vs[c]))
    for _ in range(12):
        long_edges = [e for e in bm.edges if (e.verts[0].co - e.verts[1].co).length > m(maxedge)]
        if not long_edges:
            break
        bmesh.ops.subdivide_edges(bm, edges=long_edges, cuts=1, use_grid_fill=True)
    bmesh.ops.beautify_fill(bm, faces=list(bm.faces), edges=list(bm.edges), use_restrict_tag=False, method="ANGLE")   # flip away the long thin ear-clip triangles
    for v in bm.verts:
        v.co.z = m(zfunc(v.co.x / FT, v.co.y / FT))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    for f in bm.faces:
        if f.normal.z < 0:
            f.normal_flip()
    res = bmesh.ops.extrude_face_region(bm, geom=list(bm.faces))
    for v in [g for g in res["geom"] if isinstance(g, bmesh.types.BMVert)]:
        v.co.z -= m(thick)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return v4.new_object(name, bm, col, mat), round(area_poly, 1)


def slab_grid(name, poly, zfunc, thick, col, mat, cell=3.0):
    """Terrain-following slab whose top is a regular grid (cell ft) clipped exactly to the outline with the exact
    boolean (no long thin fan triangles -> no shading streaks).  The outline prism comes from the verified ear clip."""
    pts = v8.clean_poly(poly)
    pts, tris = ear_clip_tolerant(pts)
    area_poly = v8.poly_area(pts)
    area_tri = sum(abs((pts[b][0] - pts[a][0]) * (pts[c][1] - pts[a][1]) - (pts[b][1] - pts[a][1]) * (pts[c][0] - pts[a][0])) / 2 for a, b, c in tris)
    assert abs(area_tri - area_poly) < 5e-3 * max(1.0, area_poly), f"{name}: triangulation area {area_tri:.1f} != polygon {area_poly:.1f}"
    # outline prism (+-30 ft)
    bp = bmesh.new()
    vs = [bp.verts.new((m(x), m(y), m(30.0))) for x, y in pts]
    for a, b, c in tris:
        bp.faces.new((vs[a], vs[b], vs[c]))
    bmesh.ops.recalc_face_normals(bp, faces=bp.faces)
    for f in bp.faces:
        if f.normal.z < 0:
            f.normal_flip()
    r = bmesh.ops.extrude_face_region(bp, geom=list(bp.faces))
    for v in [g for g in r["geom"] if isinstance(g, bmesh.types.BMVert)]:
        v.co.z = m(-30.0)
    bmesh.ops.recalc_face_normals(bp, faces=bp.faces)
    prism = v4.new_object("TMP_prism_" + name, bp, col, None)
    # flat grid slab covering the outline
    x0, x1 = min(q[0] for q in pts) - cell, max(q[0] for q in pts) + cell
    y0, y1 = min(q[1] for q in pts) - cell, max(q[1] for q in pts) + cell
    nx, ny = int(math.ceil((x1 - x0) / cell)), int(math.ceil((y1 - y0) / cell))
    bg = bmesh.new()
    gv = [[bg.verts.new((m(x0 + i * cell), m(y0 + j * cell), 0.0)) for j in range(ny + 1)] for i in range(nx + 1)]
    for i in range(nx):
        for j in range(ny):
            bg.faces.new((gv[i][j], gv[i + 1][j], gv[i + 1][j + 1], gv[i][j + 1]))
    bmesh.ops.triangulate(bg, faces=list(bg.faces))
    bmesh.ops.recalc_face_normals(bg, faces=bg.faces)
    for f in bg.faces:
        if f.normal.z < 0:
            f.normal_flip()
    r = bmesh.ops.extrude_face_region(bg, geom=list(bg.faces))
    for v in [g for g in r["geom"] if isinstance(g, bmesh.types.BMVert)]:
        v.co.z = m(-thick)
    bmesh.ops.recalc_face_normals(bg, faces=bg.faces)
    grid_obj = v4.new_object("TMP_grid_" + name, bg, col, None)
    md = grid_obj.modifiers.new("clip", "BOOLEAN")
    md.operation = "INTERSECT"
    md.object = prism
    md.solver = "EXACT"
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(grid_obj.evaluated_get(dg))
    for o_ in (grid_obj, prism):
        me_ = o_.data
        bpy.data.objects.remove(o_, do_unlink=True)
        bpy.data.meshes.remove(me_)
    bm = bmesh.new()
    bm.from_mesh(me)
    bpy.data.meshes.remove(me)
    for v in bm.verts:
        v.co.z += m(zfunc(v.co.x / FT, v.co.y / FT))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    top_area = sum(f.calc_area() for f in bm.faces if f.normal.z > 0.5) / FT / FT
    assert abs(top_area - area_poly) < 2e-2 * max(1.0, area_poly), f"{name}: clipped top area {top_area:.1f} != polygon {area_poly:.1f}"
    obj = v4.new_object(name, bm, col, mat)
    for pg in obj.data.polygons:
        pg.use_smooth = pg.normal.z > 0.5
    return obj, round(area_poly, 1)


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    do_render = "--no-render" not in argv
    out = None
    if "--out" in argv:
        out = Path(argv[argv.index("--out") + 1]).resolve()
        out.mkdir(parents=True, exist_ok=True)
    model_dir = out or (ROOT / "models" / "Building_I")
    render_dir = out or (ROOT / "renders" / "Building_I")
    note_dir = out or (ROOT / "notes" / "Building_I")
    BLEND = model_dir / f"{STEM}.blend"
    REPORT = note_dir / f"{STEM}_build_report.json"
    for p in (BLEND, REPORT):
        if p.exists():
            raise SystemExit(f"refusing to overwrite existing file: {p}")
    D = json.loads(DATA.read_text(encoding="utf-8"))
    S = json.loads(SITE.read_text(encoding="utf-8"))
    L = json.loads(LAND.read_text(encoding="utf-8"))
    F8 = json.loads(FOOT.read_text(encoding="utf-8"))
    G = json.loads(GEOM.read_text(encoding="utf-8"))
    samples = int(argv[argv.index("--samples") + 1]) if "--samples" in argv else 256
    only = argv[argv.index("--views") + 1].split(",") if "--views" in argv else None
    Wn = D["meta"]["regrade_window"]
    WX0, WY0, WX1, WY1 = Wn["x0"], Wn["y0"], Wn["x1"], Wn["y1"]

    bpy.ops.wm.open_mainfile(filepath=str(BASE))
    scene = bpy.context.scene
    objs = bpy.data.objects
    cols = {c.name: c for c in bpy.data.collections}
    mats_before = {mt.name: mat_sig(mt) for mt in bpy.data.materials}
    P = {k: [tuple(p) for p in v] for k, v in D["polygons"].items()}

    # ------------------------------------------------------------------ what is touched
    terrain = objs["SITE_terrain_IDW_INTERPOLATED"]
    drive_old = objs["SITE_asphalt_west_drive_dropoff"]

    def in_window(o):
        b = bbox_ft(o)
        return b[3] > WX0 and b[0] < WX1 and b[4] > WY0 and b[1] < WY1
    land_touch = sorted(o.name for o in objs if o.type == "MESH" and o.name.startswith("LS_") and in_window(o) and not o.name.startswith("LS_parking_island_"))
    # LP-100 parking-lot islands (north lot, centres y > 210) only graze the window edge: untouched
    ctx_trees_touch = [o.name for o in objs if o.name.startswith("CTX_existing_street_tree") and in_window(o)]
    assert not ctx_trees_touch, f"street trees inside the regrade window: {ctx_trees_touch}"
    touched = set(land_touch) | {terrain.name, drive_old.name}
    keep_names = [o.name for o in objs if o.type == "MESH" and o.name not in touched]
    h_before = geometry_hash(keep_names)
    building_names = [n for n in keep_names if n.startswith(("BI_", "FR_"))]
    h_building = geometry_hash(building_names)
    old_drive_bbox = [round(v, 2) for v in bbox_ft(drive_old)]
    old_terrain_verts = len(terrain.data.vertices)
    old_terrain_faces = len(terrain.data.polygons)

    # ---- old grade at every plant position (for the record) : ray-cast the v009 surfaces
    surf_names_old = [o.name for o in objs if o.type == "MESH" and o.name.startswith(("SITE_terrain", "SITE_asphalt", "SITE_walk", "SITE_entry", "SITE_plaza"))]

    def make_grade(names):
        surfaces = [objs[n] for n in names if n in objs]

        def grade(x, y):
            best = None
            origin = Vector((m(x), m(y), m(200.0)))
            for o in surfaces:
                inv = o.matrix_world.inverted()
                hit, loc, _n, _i = o.ray_cast(inv @ origin, (inv.to_3x3() @ Vector((0, 0, -1))).normalized())
                if hit:
                    z = (o.matrix_world @ loc).z
                    if best is None or z > best:
                        best = z
            return best
        return grade
    _grade_old_fn = make_grade(surf_names_old)
    # old grade at every documented plant / patch-centre / symbol position, captured BEFORE any surface is touched
    zold = {}
    for p_ in L["plants"]:
        zold[(round(p_["x"], 2), round(p_["y"], 2))] = _grade_old_fn(p_["x"], p_["y"])
    for u_ in L["unassigned_symbols"]:
        zold[(round(u_["x"], 2), round(u_["y"], 2))] = _grade_old_fn(u_["x"], u_["y"])
    for h_ in L["groundcover_patches"]:
        poly_ = [(x, y) for x, y in h_["polygon"]]
        cx_ = sum(q[0] for q in poly_) / len(poly_); cy_ = sum(q[1] for q in poly_) / len(poly_)
        zold[(round(cx_, 2), round(cy_, 2))] = _grade_old_fn(cx_, cy_)

    def grade_old(x, y):
        return zold.get((round(x, 2), round(y, 2)))

    # ------------------------------------------------------------------ spot sets and interpolation
    # Two consistent fields from the cleaned spot set (chart values and pipe-invert labels dropped):
    #   G = gutter / pavement level  : TOC -> z - 0.50 ; BOC -> z ; unlabeled spot inside the drive polygon -> z (pavement) ; unlabeled outside -> z - 0.50 (ground = curb-top level)
    #   T = curb-top / ground level  : G + 0.50   (CG-101: every TOC/BOC pair differs by exactly 0.50)
    # Outside the regrade window both fields fade (over MARGIN ft) into the plain IDW so the untouched v003 terrain is met continuously.
    drive_poly_ = P["drive_merged"]

    def g_of(s):
        lab = s.get("label")
        if lab == "TOC":
            return s["z"] - 0.5
        if lab == "BOC":
            return s["z"]
        return s["z"] if point_in_poly(s["x"], s["y"], drive_poly_) else s["z"] - 0.5
    spots_raw = [(s["x"], s["y"], s["z"] - FFE) for s in D["spots_kept"]]
    spots_G = [(s["x"], s["y"], g_of(s) - FFE) for s in D["spots_kept"]]
    MARGIN = 8.0
    CURB_W = 1.5      # CS-101: back of curb 1.5 ft behind the face of curb
    CURB_H = 0.5      # CG-101: TOC - BOC = 0.50 everywhere

    def w_window(x, y):
        d = min(x - WX0, WX1 - x, y - WY0, WY1 - y)
        return max(0.0, min(1.0, d / MARGIN))

    def idw_of(spots):
        def idw(x, y):
            num = den = 0.0
            for sx, sy, sz in spots:
                d2 = (sx - x) ** 2 + (sy - y) ** 2
                if d2 < 0.01:
                    return sz
                w = 1.0 / (d2 ** 1.5)
                num += w * sz
                den += w
            return num / den
        return idw
    _idw_raw = idw_of(spots_raw)
    _idw_G = idw_of(spots_G)

    def idw_gutter(x, y):
        w = w_window(x, y)
        return w * _idw_G(x, y) + (1.0 - w) * _idw_raw(x, y)

    def idw_terrain(x, y):
        return idw_gutter(x, y) + CURB_H * w_window(x, y)

    # ------------------------------------------------------------------ 1. drive asphalt (replace)
    hs_col = cols["08_Site_v003_hardscape"]
    mat = {"asphalt": bpy.data.materials["SITE_asphalt"], "pavers": bpy.data.materials["SITE_pavers_Techo-Bloc_Westmount_Onyx_placeholder"],
           "concrete": bpy.data.materials["SITE_concrete_walk"], "mulch": bpy.data.materials["LS_mulch"]}
    me = drive_old.data
    bpy.data.objects.remove(drive_old, do_unlink=True)
    if me.users == 0:
        bpy.data.meshes.remove(me)
    built = {}
    o, a = slab_grid("SITE_asphalt_west_drive_dropoff", P["drive_merged"], lambda x, y: idw_gutter(x, y) + 0.1, 0.5, hs_col, mat["asphalt"], cell=4.0)
    o["source"] = "CS-101 rev 13 face-of-curb lines (V) merged with the correct v003 part; gutter grades from CG-101 / PCO 50 (W) interpolated (I)"
    built[o.name] = a

    def flat_cap(poly):
        pts = v8.clean_poly(poly)
        pts, tris = ear_clip_tolerant(pts)
        b = bmesh.new()
        vs = [b.verts.new((m(x), m(y), 0.0)) for x, y in pts]
        for a_, b_, c_ in tris:
            b.faces.new((vs[a_], vs[b_], vs[c_]))
        bmesh.ops.recalc_face_normals(b, faces=b.faces)
        for f in b.faces:
            if f.normal.z < 0:
                f.normal_flip()
        return b

    def offset_polygon(pts, w):
        """outward miter offset of a simple polygon (miter length limited to 3 w)"""
        n = len(pts)
        area2 = sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n))
        sgn = 1.0 if area2 > 0 else -1.0

        def nrm(a_, b_):
            dx, dy = b_[0] - a_[0], b_[1] - a_[1]
            L = math.hypot(dx, dy) or 1.0
            return (sgn * dy / L, -sgn * dx / L)
        out = []
        for i in range(n):
            p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % n]
            n1, n2 = nrm(p0, p1), nrm(p1, p2)
            bx, by = n1[0] + n2[0], n1[1] + n2[1]
            bl = math.hypot(bx, by)
            if bl < 1e-6:
                out.append((p1[0] + n1[0] * w, p1[1] + n1[1] * w))
                continue
            k = min(w / (bl / 2.0), 1.5 * w)
            out.append((p1[0] + bx / bl * k, p1[1] + by / bl * k))
        return out
    drive_pts = v8.clean_poly(P["drive_merged"])
    drive_back = offset_polygon(drive_pts, CURB_W)          # back-of-curb line

    def ring_bmesh(inner, outer):
        b = bmesh.new()
        vi = [b.verts.new((m(x), m(y), 0.0)) for x, y in inner]
        vo = [b.verts.new((m(x), m(y), 0.0)) for x, y in outer]
        n = len(inner)
        for i in range(n):
            j = (i + 1) % n
            try:
                b.faces.new((vi[i], vi[j], vo[j], vo[i]))
            except ValueError:
                pass
        bmesh.ops.recalc_face_normals(b, faces=b.faces)
        for f in b.faces:
            if f.normal.z < 0:
                f.normal_flip()
        return b

    def clip_to_window(b):
        for co, no in (((m(WX0), 0, 0), (1, 0, 0)), ((m(WX1), 0, 0), (-1, 0, 0)), ((0, m(WY0), 0), (0, 1, 0)), ((0, m(WY1), 0), (0, -1, 0))):
            geom = list(b.verts) + list(b.edges) + list(b.faces)
            bmesh.ops.bisect_plane(b, geom=geom, plane_co=co, plane_no=no, clear_inner=True)
        return b
    # curb ring: top of curb at T + 0.03 ft (covers the 1.5 ft lawn strip between the terrain cut at the face of curb and the
    # back of curb; the walks/plaza that start at the back of curb sit 1 cm lower, no coplanar faces), 0.9 ft deep into the asphalt slab
    b_ring = ring_bmesh(drive_pts, drive_back)
    clip_to_window(b_ring)
    for _ in range(8):
        long_edges = [e for e in b_ring.edges if (e.verts[0].co - e.verts[1].co).length > m(6.0)]
        if not long_edges:
            break
        bmesh.ops.subdivide_edges(b_ring, edges=long_edges, cuts=1, use_grid_fill=True)
    for v in b_ring.verts:
        v.co.z = m(idw_terrain(v.co.x / FT, v.co.y / FT) + 0.03)
    bmesh.ops.recalc_face_normals(b_ring, faces=b_ring.faces)
    for f in b_ring.faces:
        if f.normal.z < 0:
            f.normal_flip()
    ring_area = sum(f.calc_area() for f in b_ring.faces) / FT / FT
    res = bmesh.ops.extrude_face_region(b_ring, geom=list(b_ring.faces))
    for v in [g for g in res["geom"] if isinstance(g, bmesh.types.BMVert)]:
        v.co.z -= m(0.9)
    bmesh.ops.recalc_face_normals(b_ring, faces=b_ring.faces)
    curb = v4.new_object("SITE_curb_entrance_drive_CS101", b_ring, hs_col, mat["concrete"])
    curb["source"] = "CS-101 rev 13 double curb line (face / back of curb 1.5 ft apart) (V); height TOC - BOC = 0.50 from CG-101 / PCO 50 (W); clipped to the regrade window"
    built[curb.name] = round(ring_area, 1)
    # ------------------------------------------------------------------ 2. islands, plaza, walks (add)
    specs = [("SITE_entry_island_oval_bed_CS101", "island_oval_outer", "mulch", 0.5, 0.8), ("SITE_entry_island_nose_paved_CS101", "island_nose_paved", "concrete", 0.5, 0.8),
             ("SITE_parking_end_island_12ft_CS101", "end_island_12_20", "mulch", 0.5, 0.8), ("SITE_walk_canopy_plaza_pavers_CS101", "plaza_pavers", "pavers", 0.5, 0.5),
             ("SITE_walk_diagonal_pavers_CS101", "walk_diagonal_pavers", "pavers", 0.5, 0.5), ("SITE_walk_aisle_concrete_CS101", "walk_aisle_concrete", "concrete", 0.5, 0.5)]
    for name, key, mk, dz, thick in specs:
        o, a = slab_grid(name, P[key], (lambda dz_: (lambda x, y: idw_gutter(x, y) + dz_))(dz), thick, hs_col, mat[mk], cell=3.0)
        o["source"] = D["objects"][name].get("note", "CS-101 rev 13 (V)")
        built[name] = a

    # ------------------------------------------------------------------ 3. terrain regrade inside the window
    T = S["terrain"]
    step = T["step"]
    fp = [tuple(p) for p in G["footprint_union"]]
    i0 = [i for i, p in enumerate(fp) if abs(p[0] - 71.0) < 1e-6 and abs(p[1] - 120.38) < 1e-6][0]
    i1 = [i for i, p in enumerate(fp) if abs(p[0] - 148.25) < 1e-6 and abs(p[1] - 197.5) < 1e-6][0]
    Z = F8["zones"]
    rect = v8.v1.rect
    ex_polys = [[tuple(p) for p in Z["Z1_L1_south_block"]["poly"]], rect(Z["Z2_band_lobby"]["x0"], Z["Z2_band_lobby"]["y0"], Z["Z2_band_lobby"]["x1"], Z["Z2_band_lobby"]["y1"]),
                rect(G["vestibule_100"]["x0"], G["vestibule_100"]["y0"], G["vestibule_100"]["x1"], G["vestibule_100"]["y1"]),
                rect(Z["Z5_end_block_13_14"]["x0"], Z["Z5_end_block_13_14"]["y0"], Z["Z5_end_block_13_14"]["x1"], Z["Z5_end_block_13_14"]["y1"]),
                rect(Z["Z4b_north_block_south_part"]["x0"], Z["Z4b_north_block_south_part"]["y0"], Z["Z4b_north_block_south_part"]["x1"], Z["Z4b_north_block_south_part"]["y1"]),
                [(71.0, 97.75)] + fp[i0:i1 + 1] + [tuple(p) for p in Z["Z4a_north_block"]["L1_north_east"]]]
    asph_polys = [P["drive_merged"]] + [[tuple(q) for q in hs["polygon"]] for hs in S["hardscape"] if hs.get("dz", 0.0) == 0.0 and hs["name"] != "asphalt_west_drive_dropoff"]
    asph_polys += [[(st["x0"], st["y0"]), (st["x1"], st["y0"]), (st["x1"], st["y1"]), (st["x0"], st["y1"])] for st in S["streets"]]
    pave_polys = [P[k] for k in ("island_oval_outer", "island_nose_paved", "end_island_12_20", "plaza_pavers", "walk_diagonal_pavers", "walk_aisle_concrete")]

    # The window terrain is built as its own closed 2-ft slab (top = T field), cut by the pavement solids with the exact
    # boolean (drive face polygon + 1.5 ft curb ring, plaza, walks, v003 entry plaza), then joined back to the untouched
    # terrain outside the window.  No terrain face can therefore rise through a pavement slab, and the cut edge sits at
    # the back of curb at curb-top level, hidden by the curb ring / slab sides.
    bm = bmesh.new()
    bm.from_mesh(terrain.data)
    doomed = []
    for f in bm.faces:
        c = f.calc_center_median()
        if WX0 <= c.x / FT <= WX1 and WY0 <= c.y / FT <= WY1:
            doomed.append(f)
    n_del = len(doomed)
    bmesh.ops.delete(bm, geom=doomed, context="FACES_ONLY")
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context="VERTS")
    existing_z = {(round(v.co.x / FT, 3), round(v.co.y / FT, 3)): v.co.z for v in bm.verts}
    gx0, gy0 = T["x0"], T["y0"]
    i_lo, i_hi = int(math.floor((WX0 - gx0) / step)), int(math.ceil((WX1 - gx0) / step))
    j_lo, j_hi = int(math.floor((WY0 - gy0) / step)), int(math.ceil((WY1 - gy0) / step))
    wbm = bmesh.new()
    grid = {}
    boundary_dz = []

    def vert(i, j):
        key = (i, j)
        if key in grid:
            return grid[key]
        x, y = gx0 + i * step, gy0 + j * step
        z_new = idw_terrain(x, y)
        ez = existing_z.get((round(x, 3), round(y, 3)))
        if ez is not None:                       # window boundary: keep the v003 vertex height exactly (continuity), record the difference
            boundary_dz.append(abs(ez / FT - z_new))
            z = ez
        else:
            z = m(z_new)
        grid[key] = wbm.verts.new((m(x), m(y), z))
        return grid[key]
    n_new = 0
    for j in range(j_lo, j_hi):
        for i in range(i_lo, i_hi):
            cx, cy = gx0 + (i + 0.5) * step, gy0 + (j + 0.5) * step
            if not (WX0 <= cx <= WX1 and WY0 <= cy <= WY1):
                continue
            if any(point_in_poly(cx, cy, p) for p in ex_polys):
                continue
            corners = [(gx0 + i * step, gy0 + j * step), (gx0 + (i + 1) * step, gy0 + j * step), (gx0 + (i + 1) * step, gy0 + (j + 1) * step), (gx0 + i * step, gy0 + (j + 1) * step)]
            if any(all(point_in_poly(px, py, p) for px, py in corners) for p in asph_polys + pave_polys):
                continue
            try:
                wbm.faces.new([vert(i, j), vert(i + 1, j), vert(i + 1, j + 1), vert(i, j + 1)])
                n_new += 1
            except ValueError:
                pass
    bmesh.ops.triangulate(wbm, faces=list(wbm.faces))
    bmesh.ops.recalc_face_normals(wbm, faces=wbm.faces)
    for f in wbm.faces:
        if f.normal.z < 0:
            f.normal_flip()
    res = bmesh.ops.extrude_face_region(wbm, geom=list(wbm.faces))
    for v in [g for g in res["geom"] if isinstance(g, bmesh.types.BMVert)]:
        v.co.z -= m(2.0)
    bmesh.ops.recalc_face_normals(wbm, faces=wbm.faces)
    win_obj = v4.new_object("TMP_terrain_window", wbm, hs_col, None)

    def cutter(name, b, ztop=30.0, zbot=-30.0):
        for v in b.verts:
            v.co.z = m(ztop)
        r_ = bmesh.ops.extrude_face_region(b, geom=list(b.faces))
        for v in [g for g in r_["geom"] if isinstance(g, bmesh.types.BMVert)]:
            v.co.z = m(zbot)
        bmesh.ops.recalc_face_normals(b, faces=b.faces)
        return v4.new_object(name, b, hs_col, None)
    cutters = [cutter("TMP_cut_drive", flat_cap(drive_pts)), cutter("TMP_cut_plaza", flat_cap(P["plaza_pavers"])),
               cutter("TMP_cut_walk_diag", flat_cap(P["walk_diagonal_pavers"])), cutter("TMP_cut_walk_aisle", flat_cap(P["walk_aisle_concrete"]))]
    for hs in S["hardscape"]:
        if hs["name"] == "entry_plaza_pavers_Westmount_Onyx":       # v003 slab (y 27-74) reaches into the window: cut the terrain under it as well
            cutters.append(cutter("TMP_cut_v003_entry_plaza", flat_cap([tuple(q) for q in hs["polygon"]])))
    for c_ in cutters:
        md = win_obj.modifiers.new("cut_" + c_.name, "BOOLEAN")
        md.operation = "DIFFERENCE"
        md.object = c_
        md.solver = "EXACT"
    dg = bpy.context.evaluated_depsgraph_get()
    me_cut = bpy.data.meshes.new_from_object(win_obj.evaluated_get(dg))
    n_cut_faces = len(me_cut.polygons)
    # strip the bottom of the temporary slab BEFORE joining (the v003 terrain faces are wound downwards, and BMesh reuses
    # freed slots, so neither a normal test nor index slicing on the joined mesh can identify the added faces)
    bmc = bmesh.new()
    bmc.from_mesh(me_cut)
    bmesh.ops.delete(bmc, geom=[f for f in bmc.faces if f.normal.z < -0.9], context="FACES_ONLY")
    bmesh.ops.delete(bmc, geom=[v for v in bmc.verts if not v.link_faces], context="VERTS")
    bmc.to_mesh(me_cut)
    bmc.free()
    n_old_faces = len(bm.faces)
    bm.from_mesh(me_cut)
    assert len(bm.faces) == n_old_faces + len(me_cut.polygons)
    near = [v for v in bm.verts if min(abs(v.co.x / FT - WX0), abs(v.co.x / FT - WX1), abs(v.co.y / FT - WY0), abs(v.co.y / FT - WY1)) < 0.01]
    bmesh.ops.remove_doubles(bm, verts=near, dist=1e-4)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(terrain.data)
    bm.free()
    terrain.data.update()
    for pg in terrain.data.polygons:
        pg.use_smooth = abs(pg.normal.z) > 0.3          # v009 smooth flag kept on the (downward-wound) v003 faces; the vertical cut faces stay flat
    for o_ in [win_obj] + cutters:
        me_ = o_.data
        bpy.data.objects.remove(o_, do_unlink=True)
        bpy.data.meshes.remove(me_)
    n_joined = len(me_cut.polygons)
    bpy.data.meshes.remove(me_cut)
    terrain_rec = {"method": "window cells (4 ft, top = T field) as a closed slab, exact boolean difference with the pavement solids, joined to the untouched terrain",
                   "faces_removed": n_del, "cells_added": n_new, "faces_after_cut_incl_bottom": n_cut_faces, "faces_joined": n_joined, "vertices_before": old_terrain_verts, "vertices_after": len(terrain.data.vertices),
                   "faces_before": old_terrain_faces, "faces_after": len(terrain.data.polygons), "window_boundary_max_dz_ft": round(max(boundary_dz), 3) if boundary_dz else 0.0,
                   "window_boundary_mean_dz_ft": round(sum(boundary_dz) / len(boundary_dz), 3) if boundary_dz else 0.0, "cutters": ["drive_face_of_curb", "plaza", "walk_diag", "walk_aisle", "v003_entry_plaza"]}

    # ------------------------------------------------------------------ 4. landscape objects re-seated on the corrected grade
    surf_names_new = [o.name for o in objs if o.type == "MESH" and o.name.startswith(("SITE_terrain", "SITE_asphalt", "SITE_walk", "SITE_entry", "SITE_plaza", "SITE_parking_end_island", "SITE_curb"))]
    hard_names = [o.name for o in objs if o.type == "MESH" and o.name.startswith(("SITE_asphalt", "SITE_walk", "SITE_entry", "SITE_plaza", "SITE_entry_island_nose"))]
    _grade_new_fn = make_grade(surf_names_new + ["SITE_entry_island_oval_bed_CS101", "SITE_entry_island_nose_paved_CS101"])
    no_hit = []

    no_hit_outside = []
    _idw_v003 = idw_of([(s_["x"], s_["y"], s_["z"] - FFE) for s_ in S["spots"]])     # v004's own fallback (raw v003 spot set)

    def grade_new(x, y):
        if not (WX0 <= x <= WX1 and WY0 <= y <= WY1):      # outside the window nothing moved: keep the v009 grade exactly
            zo = grade_old(x, y)
            if zo is not None:
                return zo
            no_hit_outside.append([round(x, 2), round(y, 2)])
            return m(_idw_v003(x, y))
        z = _grade_new_fn(x, y)
        if z is None:                       # no surface under this point (terrain cell omitted, no slab): interpolated grade
            no_hit.append([round(x, 2), round(y, 2)])
            z = m(idw_terrain(x, y))
        return z
    _grade_hard_fn = make_grade(hard_names)
    oval = P["island_oval_outer"]

    def grade_hard(x, y):     # the planted oval is a bed, not hardscape (the asphalt slab continues underneath it)
        if point_in_poly(x, y, oval):
            return None
        return _grade_hard_fn(x, y)
    sched = L["schedule"]
    SZ = L["sizes_for_model"]
    M = {k: bpy.data.materials[f"LS_{k}"] for k in L["materials"]}
    sub = {k: cols[f"09_Landscape_v004_{k}"] for k in ("trees", "shrubs", "groundcover", "beds_islands", "context")}
    islands = L["parking_islands"]["items"]

    def on_island(x, y):
        return any(abs(x - i["x"]) <= i["w"] / 2 and abs(y - i["y"]) <= i["h"] / 2 for i in islands)

    def foliage_mat(code):
        tp = sched.get(code, {}).get("type", "shrub")
        if tp == "tree":
            return M["foliage_tree"]
        if code in ("LOPE", "LOJA", "CORA"):
            return M["shrub_purple"]
        if code in ("BLON", "BUNN", "MUHL", "CARZ", "CARE"):
            return M["shrub_grass"]
        if tp == "groundcover":
            return M["groundcover"]
        if tp == "annual":
            return M["annual"]
        return M["shrub_green"]
    L1_polys = ex_polys  # corrected footprint (v008) for the push rule; v008 found 0 pushes

    def push(x, y):
        total = 0.0
        for poly in L1_polys:
            if point_in_poly(x, y, poly):
                x, y, dsh = v4.push_outside(x, y, poly, 1.2)
                total += dsh
        return x, y, total
    groups = {}
    for p in L["plants"]:
        groups.setdefault((p["code"], p["sheet"], p["callout_n"]), []).append(p)
    z_records = []      # per plant: object, x, y, z_old, z_new
    rebuilt = []
    old_objs = {n: objs[n] for n in land_touch}

    def remove(name):
        o = objs[name]
        me = o.data
        bpy.data.objects.remove(o, do_unlink=True)
        if me.users == 0:
            bpy.data.meshes.remove(me)

    def rec(name, x, y, zo, zn):
        z_records.append({"object": name, "x": round(x, 2), "y": round(y, 2), "z_old": None if zo is None else round(zo / FT, 2), "z_new": None if zn is None else round(zn / FT, 2)})

    # groups (shrub / groundcover / annual) and their mulch discs
    done = set()
    for name in land_touch:
        if name in done:
            continue
        if name.startswith(("LS_shrub_", "LS_groundcover_", "LS_annual_")) and "_n" in name and not name.startswith("LS_shrub_UNRESOLVED"):
            code, sheet, n_ = None, None, None
            for (c, s, n) in groups:
                tp = sched[c]["type"]
                suffix = "" if n else "_adj"
                if name == f"LS_{tp}_{c}_{sheet if False else s}_n{n}{suffix}":
                    code, sheet, n_ = c, s, n
            assert code is not None, f"group not identified for {name}"
            items = groups[(code, sheet, n_)]
            info = sched[code]
            tp = info["type"]
            suffix = "" if n_ else "_adj"
            mulch_name = f"LS_mulch_{code}_{sheet}_n{n_}{suffix}_INTERPRETED"
            hh = info.get("height_in_min", 18) / 12 if tp == "shrub" else (0.6 if tp == "annual" else (0.8 if code in ("MUHL", "CARZ", "CARE", "RUSS", "CATM") else 0.6))
            ww = min(info.get("spacing_ft", 3), 1.3 * hh) if tp == "shrub" else (1.0 if tp == "annual" else min(info.get("spacing_in", 24) / 12, 2.0))
            zo_list = [grade_old(p["x"], p["y"]) for p in items]
            remove(name)
            if mulch_name in objs:
                remove(mulch_name)
            bm = bmesh.new(); bmm = bmesh.new()
            for p, zo in zip(items, zo_list):
                x, y, dsh = push(p["x"], p["y"])
                assert dsh == 0.0, f"plant pushed unexpectedly: {code} {p['x']},{p['y']}"
                zz = grade_new(x, y) + (m(0.5) if on_island(x, y) else 0.0)
                rec(name, x, y, zo, zz)
                v4.add_sphere(bm, m(x), m(y), zz + m(hh * 0.5), m(ww / 2), m(ww / 2), m(hh * 0.55), seg=8, ring=5)
                v4.add_disc(bmm, m(x), m(y), zz + m(0.06), m(SZ["mulch_disc_radius_ft"]))
            o = v4.new_object(name, bm, sub["shrubs" if tp == "shrub" else "groundcover"], foliage_mat(code))
            o["conf"] = ",".join(sorted(set(p["conf"] for p in items)))
            o["source"] = f"{sheet} callout ({n_}) {code}" if n_ else f"{sheet} {items[0].get('basis', '')}"
            o["schedule"] = json.dumps(info)
            om = v4.new_object(mulch_name, bmm, sub["beds_islands"], M["mulch"])
            om["note"] = "mulch disc per documented plant; bed outline not modeled (I)"
            for pg in list(o.data.polygons) + list(om.data.polygons):
                pg.use_smooth = True
            rebuilt += [name, mulch_name]
            done |= {name, mulch_name}
        elif name.startswith("LS_mulch_"):
            continue   # handled with its group (or below if the group itself is outside the window)
    # mulch discs whose group object was not in the window (group outside but disc inside): rebuild the pair anyway
    for name in land_touch:
        if name in done or not name.startswith("LS_mulch_"):
            continue
        grp = name.replace("LS_mulch_", "").replace("_INTERPRETED", "")
        cand = [n for n in objs if n.type == "MESH" and n.name.endswith(grp) and n.name.startswith(("LS_shrub_", "LS_groundcover_", "LS_annual_"))]
        assert cand, f"group for {name} not found"
        land_touch.append(cand[0].name)   # process in the next loop
    for name in land_touch:
        if name in done or not name.startswith(("LS_shrub_", "LS_groundcover_", "LS_annual_")) or name.startswith("LS_shrub_UNRESOLVED"):
            continue
        # same as above (group outside the window whose mulch disc touched it)
        for (c, s, n) in groups:
            tp = sched[c]["type"]
            suffix = "" if n else "_adj"
            if name == f"LS_{tp}_{c}_{s}_n{n}{suffix}":
                items = groups[(c, s, n)]; info = sched[c]
                mulch_name = f"LS_mulch_{c}_{s}_n{n}{suffix}_INTERPRETED"
                hh = info.get("height_in_min", 18) / 12 if tp == "shrub" else (0.6 if tp == "annual" else (0.8 if c in ("MUHL", "CARZ", "CARE", "RUSS", "CATM") else 0.6))
                ww = min(info.get("spacing_ft", 3), 1.3 * hh) if tp == "shrub" else (1.0 if tp == "annual" else min(info.get("spacing_in", 24) / 12, 2.0))
                zo_list = [grade_old(p["x"], p["y"]) for p in items]
                remove(name)
                if mulch_name in objs:
                    remove(mulch_name)
                bm = bmesh.new(); bmm = bmesh.new()
                for p, zo in zip(items, zo_list):
                    x, y, dsh = push(p["x"], p["y"])
                    zz = grade_new(x, y) + (m(0.5) if on_island(x, y) else 0.0)
                    rec(name, x, y, zo, zz)
                    v4.add_sphere(bm, m(x), m(y), zz + m(hh * 0.5), m(ww / 2), m(ww / 2), m(hh * 0.55), seg=8, ring=5)
                    v4.add_disc(bmm, m(x), m(y), zz + m(0.06), m(SZ["mulch_disc_radius_ft"]))
                o = v4.new_object(name, bm, sub["shrubs" if tp == "shrub" else "groundcover"], foliage_mat(c))
                o["conf"] = ",".join(sorted(set(p["conf"] for p in items)))
                o["source"] = f"{s} callout ({n}) {c}" if n else f"{s} {items[0].get('basis', '')}"
                o["schedule"] = json.dumps(info)
                om = v4.new_object(mulch_name, bmm, sub["beds_islands"], M["mulch"])
                om["note"] = "mulch disc per documented plant; bed outline not modeled (I)"
                for pg in list(o.data.polygons) + list(om.data.polygons):
                    pg.use_smooth = True
                rebuilt += [name, mulch_name]
                done |= {name, mulch_name}
                break
    # ground-cover leader-disc patches
    for name in land_touch:
        if name in done or not name.startswith("LS_gcpatch_"):
            continue
        h = None
        for hh_ in L["groundcover_patches"]:
            if name == f"LS_gcpatch_{hh_['code']}_{hh_['sheet']}_n{hh_['n']}_{hh_['status']}_INTERPRETED":
                h = hh_
        assert h is not None, f"patch data for {name} not found"
        poly = [(x, y) for x, y in h["polygon"]]
        cx = sum(p[0] for p in poly) / len(poly); cy = sum(p[1] for p in poly) / len(poly)
        zo = grade_old(cx, cy)
        remove(name)
        if grade_hard(cx, cy) is not None:
            rec(name, cx, cy, zo, None)
            rebuilt.append(name + " (centre now on hardscape -> not modeled, v004 rule)")
            done.add(name)
            continue
        bm = bmesh.new()
        zc = sum(grade_new(x, y) for x, y in poly) / len(poly)
        hp = SZ["annual_patch_height_ft"] if h["code"] == "SEAS" else SZ["groundcover_patch_height_ft"]
        v4.add_prism(bm, poly, zc + m(0.05), zc + m(hp))
        o = v4.new_object(name, bm, sub["groundcover"], foliage_mat(h["code"]))
        o["area_sqft"] = h["area_sqft"]; o["expected_area_sqft"] = h.get("expected_area_sqft", 0)
        for pg in o.data.polygons:
            pg.use_smooth = True
        rec(name, cx, cy, zo, zc)
        rebuilt.append(name); done.add(name)
    # trees
    for name in land_touch:
        if name in done or not name.startswith("LS_tree_"):
            continue
        parts = name.split("_")   # LS_tree_CODE_SHEET_kk
        code, sheet, kk = parts[2], parts[3], int(parts[4]) - 1
        items = [groups[k] for k in groups if k[0] == code and k[1] == sheet]
        items = [p for grp in items for p in grp]
        p = items[kk]
        zo = grade_old(p["x"], p["y"])
        remove(name)
        x, y, dsh = push(p["x"], p["y"])
        zz = grade_new(x, y) + (m(0.5) if on_island(x, y) else 0.0)
        bm = bmesh.new()
        H, Cc, Tt = SZ["tree_new"]["height_ft"], SZ["tree_new"]["canopy_ft"], SZ["tree_new"]["trunk_in"] / 12
        v4.add_cylinder(bm, m(x), m(y), zz, zz + m(H * 0.45), m(Tt / 2))
        v4.add_sphere(bm, m(x), m(y), zz + m(H * 0.68), m(Cc / 2), m(Cc / 2), m(H * 0.32))
        o = v4.new_object(name, bm, sub["trees"], M["trunk"])
        o.data.materials.append(M["foliage_tree"])
        for f in o.data.polygons:
            f.material_index = 1 if (o.matrix_world @ o.data.vertices[f.vertices[0]].co).z > zz + m(H * 0.45) + 1e-4 else 0
            f.use_smooth = True
        o["conf"] = p["conf"]; o["source"] = sheet; o["schedule"] = json.dumps(sched.get(code, {}))
        rec(name, x, y, zo, zz)
        rebuilt.append(name); done.add(name)
    # unresolved symbols
    if "LS_shrub_UNRESOLVED_species_documented_symbol" in land_touch:
        name = "LS_shrub_UNRESOLVED_species_documented_symbol"
        zo_list = [grade_old(u["x"], u["y"]) for u in L["unassigned_symbols"]]
        remove(name)
        bm = bmesh.new()
        for u, zo in zip(L["unassigned_symbols"], zo_list):
            x, y, dsh = push(u["x"], u["y"])
            zz = grade_new(x, y) + (m(0.5) if on_island(x, y) else 0.0)
            if WX0 <= x <= WX1 and WY0 <= y <= WY1:
                rec(name, x, y, zo, zz)
            v4.add_sphere(bm, m(x), m(y), zz + m(0.75), m(1.4), m(1.4), m(0.8), seg=8, ring=5)
        o = v4.new_object(name, bm, sub["shrubs"], bpy.data.materials["LS_unresolved_grey_green"])
        o["note"] = f"{len(L['unassigned_symbols'])} plant symbols drawn on LP-100/LP-101 not linked to a callout leader; species unresolved (U)"
        for pg in o.data.polygons:
            pg.use_smooth = True
        rebuilt.append(name); done.add(name)
    not_handled = [n for n in land_touch if n not in done and n in objs]
    assert not not_handled, f"landscape objects in the window not rebuilt: {not_handled}"

    # ------------------------------------------------------------------ 5. cameras
    camcol = cols["90_Cameras"]

    def add_cam(name, loc, target, lens=35.0, ortho=None):
        c = bpy.data.cameras.new(name); c.lens = lens; c.clip_end = 3000; c.dof.use_dof = False
        if ortho:
            c.type = "ORTHO"; c.ortho_scale = m(ortho)
        o_ = bpy.data.objects.new(name, c)
        o_.location = Vector((m(loc[0]), m(loc[1]), m(loc[2])))
        dv = Vector((m(target[0]), m(target[1]), m(target[2]))) - o_.location
        o_.rotation_euler = dv.to_track_quat("-Z", "Y").to_euler()
        camcol.objects.link(o_)
    for name, c in D["cameras_new"].items():
        add_cam(name, c["loc"], c["target"], c.get("lens", 35.0), c.get("ortho"))

    # ------------------------------------------------------------------ 6. verification and report
    h_after = geometry_hash(keep_names)
    assert h_before == h_after, "unrelated geometry changed - aborting"
    assert geometry_hash(building_names) == h_building, "building geometry changed - aborting"
    mats_after = {mt.name: mat_sig(mt) for mt in bpy.data.materials}
    assert mats_before == mats_after, "material node trees changed - aborting"
    changed_z = [r for r in z_records if r["z_old"] is not None and r["z_new"] is not None and abs(r["z_old"] - r["z_new"]) > 0.05]
    report = {"version": "v010", "base": str(BASE), "kept_mesh_objects": len(keep_names), "geometry_hash_kept": h_before, "unrelated_geometry_unchanged": True,
              "building_geometry_hash": h_building, "building_unchanged": True, "materials_unchanged": True,
              "drive_polygon_replaced": {"old_bbox_ft": old_drive_bbox, "new_vertices": len(P["drive_merged"]), "new_area_sqft": built["SITE_asphalt_west_drive_dropoff"]},
              "objects_built_sqft": built, "terrain": terrain_rec, "spots": {"kept": len(D["spots_kept"]), "dropped_chart_values": len(D["spots_dropped_chart_values"]), "dropped_pipe_inverts": len(D["spots_dropped_pipe_inverts"])},
              "grade_fields": {"G_gutter": "TOC-0.5 / BOC / pavement spot / ground spot-0.5, IDW 1/d^3", "T_ground": "G + 0.5", "fade_margin_ft": MARGIN, "curb_width_ft": CURB_W, "curb_height_ft": CURB_H},
              "landscape_objects_rebuilt": rebuilt, "plants_reseated": len(z_records), "plants_z_changed_gt_0_05ft": len(changed_z),
              "plants_xy_moved": 0, "plants_without_surface_hit_idw_used": no_hit, "plants_outside_window_v004_idw_fallback": no_hit_outside, "plant_z_records": z_records, "cameras_added": list(D["cameras_new"]),
              "dims": D["meta"]["dims_written"], "measured": D["meta"]["measured_check"]}
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))

    if do_render:
        try:
            prefs = bpy.context.preferences.addons["cycles"].preferences
            prefs.compute_device_type = "OPTIX"; prefs.get_devices()
            for d_ in prefs.devices:
                d_.use = d_.type in ("OPTIX", "CPU")
            scene.cycles.device = "GPU"; report["gpu"] = "OPTIX"
        except Exception as e:  # noqa
            report["gpu"] = f"CPU ({e})"
        scene.cycles.samples = samples
        times = {}
        for view, (cam, (rx, ry)) in D["views"].items():
            if only and view not in only:
                continue
            scene.camera = objs[cam]
            scene.render.resolution_x, scene.render.resolution_y = rx, ry
            path = render_dir / f"{STEM}_{view}.png"
            if path.exists():
                raise SystemExit(f"refusing to overwrite existing render: {path}")
            scene.render.filepath = str(path)
            t0 = time.time(); bpy.ops.render.render(write_still=True); times[view] = round(time.time() - t0, 1)
        report["render_seconds"] = times
        scene.camera = objs["BI_cam_entrance_oblique"]
        bpy.ops.wm.save_mainfile()
        assert geometry_hash(keep_names) == h_before
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("BUILD_REPORT=" + json.dumps({k: v for k, v in report.items() if k != "plant_z_records"}))


if __name__ == "__main__":
    main()
