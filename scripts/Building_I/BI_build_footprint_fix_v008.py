r"""Building I - footprint correction v008 (after BI_footprint_audit_v008.md).

Opens BI_landscape_v007.blend (v006 approved shell + v007 landscape) and, using BI_footprint_data_v008.json:
  * replaces the v001 zone prisms whose outline came from the hatch-clip bounding rectangles (south wing, lobby band,
    end block, north block) with prisms built on the documented outside face of wall (A1.01 / A1.02 / S101 / A1.00a / A1.00b),
    split by level where Level 1 and Level 2 differ (one-storey storefront projections, Level 2 bay, gallery cantilever,
    north-face overhang);
  * re-places every v001 opening placeholder on the corrected wall faces (same extents, level-aware);
  * rebuilds the parapet screen strips, the Level 2 slab reference and the foundation skirts on the new outline;
  * regenerates the v005 finish regions (BI_facade_regions_v008.json) on the new faces;
  * rebuilds the landscape groups that hold plants pushed out of the wrong v001 footprint, against the corrected footprint.
Everything else (canopy, vestibule, mechanical screen, grid, site, other landscape, materials, cameras) is hashed before/after
and must be identical. Saves models/Building_I/BI_footprint_v008.blend and renders renders/Building_I/BI_footprint_v008_*.png.

Run:  "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --background --python scripts/Building_I/BI_build_footprint_fix_v008.py
Optional:  -- --no-render   |   -- --out <folder>
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
BASE = ROOT / "models" / "Building_I" / "BI_landscape_v007.blend"
DATA = ROOT / "notes" / "Building_I" / "BI_footprint_data_v008.json"
GEOM = ROOT / "notes" / "Building_I" / "BI_geometry_data_v001.json"
REGIONS = ROOT / "notes" / "Building_I" / "BI_facade_regions_v008.json"
LAND = ROOT / "notes" / "Building_I" / "BI_landscape_data_v007.json"
LAND_V004_REPORT = ROOT / "notes" / "Building_I" / "BI_landscape_v004_build_report.json"
LAND_V007_REPORT = ROOT / "notes" / "Building_I" / "BI_landscape_v007_build_report.json"
SITE = ROOT / "notes" / "Building_I" / "BI_site_data_v003.json"
STEM = "BI_footprint_v008"
FT = 0.3048
FFE = 661.75


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / "Building_I" / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


v1 = _load("v1", "BI_build_shell_v001.py")          # prism, rect, slab_strip, profile_value, m
v3 = _load("v3", "BI_build_site_v003.py")           # slab (terrain-following slab used for the skirts)
v4 = _load("v4", "BI_build_landscape_v004.py")      # point_in_poly, push_outside, add_sphere, add_disc, new_object, geometry_hash
v5 = _load("v5", "BI_build_facade_cleanup_v005.py")  # rect_minus, rects_minus, clip_poly
m = v1.m
geometry_hash = v4.geometry_hash

ZONE_TOPS = {"Z1_L1": 13.5, "Z1_L2": 33.3, "bay": 27.333, "band": 40.0, "ves": 9.0, "se": 32.0, "Z4b": 36.0, "Z4a_L1": 9.0, "Z4a_mid": 14.833, "Z4a_L2": 40.0}


def bbox_ft(o):
    pts = [o.matrix_world @ Vector(c) for c in o.bound_box]
    return [min(p.x for p in pts) / FT, min(p.y for p in pts) / FT, min(p.z for p in pts) / FT,
            max(p.x for p in pts) / FT, max(p.y for p in pts) / FT, max(p.z for p in pts) / FT]


def poly_area(poly):
    return abs(sum(poly[i - 1][0] * poly[i][1] - poly[i][0] * poly[i - 1][1] for i in range(len(poly)))) / 2


def clean_poly(poly):
    """Remove duplicate and collinear vertices; return CCW."""
    pts = [tuple(p) for p in poly]
    out = []
    for p in pts:
        if not out or abs(p[0] - out[-1][0]) > 1e-6 or abs(p[1] - out[-1][1]) > 1e-6:
            out.append(p)
    if len(out) > 1 and abs(out[0][0] - out[-1][0]) < 1e-6 and abs(out[0][1] - out[-1][1]) < 1e-6:
        out.pop()
    changed = True
    while changed and len(out) > 3:
        changed = False
        for i in range(len(out)):
            a, b, c = out[i - 1], out[i], out[(i + 1) % len(out)]
            if abs((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])) < 1e-6:
                del out[i]
                changed = True
                break
    if sum(out[i - 1][0] * out[i][1] - out[i][0] * out[i - 1][1] for i in range(len(out))) < 0:
        out.reverse()
    return out


def ear_clip(pts):
    """Robust ear clipping of a simple CCW polygon -> list of index triangles."""
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    def blocked(p, a, b, c):
        inside = cross(a, b, p) > 1e-9 and cross(b, c, p) > 1e-9 and cross(c, a, p) > 1e-9
        if inside:
            return True
        if abs(cross(a, c, p)) < 1e-9 and min(a[0], c[0]) - 1e-9 <= p[0] <= max(a[0], c[0]) + 1e-9 and min(a[1], c[1]) - 1e-9 <= p[1] <= max(a[1], c[1]) + 1e-9:
            return True   # lies on the diagonal a-c
        return False
    idx = list(range(len(pts)))
    tris = []
    guard = 0
    while len(idx) > 3:
        guard += 1
        if guard > 100000:
            raise RuntimeError("ear clipping stalled")
        n = len(idx)
        found = False
        for i in range(n):
            ia, ib, ic = idx[i - 1], idx[i], idx[(i + 1) % n]
            a, b, c = pts[ia], pts[ib], pts[ic]
            if cross(a, b, c) <= 1e-9:
                continue
            if any(blocked(pts[j], a, b, c) for j in idx if j not in (ia, ib, ic)):
                continue
            tris.append((ia, ib, ic))
            del idx[i]
            found = True
            break
        if not found:
            raise RuntimeError("polygon is not simple - no ear found")
    tris.append(tuple(idx))
    return tris


def prism_robust(name, poly, z0, ztop, col, mat):
    """Prism on a simple polygon with a verified cap triangulation (no bridged notches, no overlapping triangles)."""
    pts = clean_poly(poly)
    tris = ear_clip(pts)
    area_poly = poly_area(pts)
    area_tri = sum(abs((pts[b][0] - pts[a][0]) * (pts[c][1] - pts[a][1]) - (pts[b][1] - pts[a][1]) * (pts[c][0] - pts[a][0])) / 2 for a, b, c in tris)
    assert abs(area_tri - area_poly) < 1e-3 * max(1.0, area_poly), f"{name}: triangulation area {area_tri:.2f} != polygon area {area_poly:.2f}"
    for a, b, c in tris:
        cx = (pts[a][0] + pts[b][0] + pts[c][0]) / 3
        cy = (pts[a][1] + pts[b][1] + pts[c][1]) / 3
        assert v4.point_in_poly(cx, cy, pts), f"{name}: cap triangle outside the polygon"
    bm = bmesh.new()
    bot = [bm.verts.new((m(x), m(y), m(z0))) for x, y in pts]
    top = [bm.verts.new((m(x), m(y), m(ztop(x, y) if callable(ztop) else ztop))) for x, y in pts]
    for a, b, c in tris:
        bm.faces.new((bot[c], bot[b], bot[a]))
        bm.faces.new((top[a], top[b], top[c]))
    n = len(pts)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new((bot[i], bot[j], top[j], top[i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return v1.new_object(name, bm, col, mat)


def boundary_hit(zones, facade, u):
    """Outermost boundary of the candidate zone polygons along the facade ray at position u.
    Returns (coordinate, edge (a, b)) or (None, None). Handles diagonal edges."""
    best = None
    for poly in zones:
        n = len(poly)
        for i in range(n):
            a, b = poly[i], poly[(i + 1) % n]
            if facade in ("SOUTH", "NORTH"):
                if abs(a[0] - b[0]) < 1e-9:
                    continue
                if min(a[0], b[0]) - 1e-6 <= u <= max(a[0], b[0]) + 1e-6:
                    v = a[1] + (u - a[0]) * (b[1] - a[1]) / (b[0] - a[0])
                    if best is None or (facade == "SOUTH" and v < best[0]) or (facade == "NORTH" and v > best[0]):
                        best = (v, (a, b))
            else:
                if abs(a[1] - b[1]) < 1e-9:
                    continue
                if min(a[1], b[1]) - 1e-6 <= u <= max(a[1], b[1]) + 1e-6:
                    v = a[0] + (u - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
                    if best is None or (facade == "WEST" and v < best[0]) or (facade == "EAST" and v > best[0]):
                        best = (v, (a, b))
    return best if best else (None, None)


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

    bpy.ops.wm.open_mainfile(filepath=str(BASE))
    scene = bpy.context.scene
    D = json.loads(DATA.read_text(encoding="utf-8"))
    G = json.loads(GEOM.read_text(encoding="utf-8"))
    R = json.loads(REGIONS.read_text(encoding="utf-8"))
    L = json.loads(LAND.read_text(encoding="utf-8"))
    S = json.loads(SITE.read_text(encoding="utf-8"))
    V4R = json.loads(LAND_V004_REPORT.read_text(encoding="utf-8"))
    V7R = json.loads(LAND_V007_REPORT.read_text(encoding="utf-8"))
    H = D["heights"]
    Z = D["zones"]
    objs = bpy.data.objects
    cols = {c.name: c for c in bpy.data.collections}

    # ------------------------------------------------------------------ 1. what is replaced
    shell_old = ["BI_Z1_south_wing", "BI_Z2_band_E_F2", "BI_Z4a_north_block", "BI_Z4b_north_block_south_part", "BI_Z5_end_block_13_14"]
    screen_old = sorted(o.name for o in objs if o.name.startswith("BI_screen_"))
    slab_old = ["BI_L2_floor_slab"]
    open_old = sorted(o.name for o in cols["04_Openings"].objects)
    fr_old = sorted(o.name for o in objs if o.name.startswith("FR_"))
    skirt_old = sorted(o.name for o in objs if o.name.startswith("SITE_foundation_skirt"))
    sched = L["schedule"]
    groups = {}
    for p in L["plants"]:
        groups.setdefault((p["code"], p["sheet"], p["callout_n"]), []).append(p)
    shifted_keys = {(s["code"], round(s["from"][0], 2), round(s["from"][1], 2)) for s in V4R["shifted"]}
    shifted_keys |= {(s["code"], round(s["from"][0], 2), round(s["from"][1], 2)) for s in V7R.get("plants_pushed_in_rebuilt_groups", [])}
    affected = sorted({(p["code"], p["sheet"], p["callout_n"]) for p in L["plants"]
                       if (p["code"], round(p["x"], 2), round(p["y"], 2)) in shifted_keys or p.get("keep_documented")})
    land_old = []
    for code, sheet, n in affected:
        t = sched[code]["type"]
        suffix = "" if n else "_adj"
        for nm in (f"LS_{t}_{code}_{sheet}_n{n}{suffix}", f"LS_mulch_{code}_{sheet}_n{n}{suffix}_INTERPRETED"):
            if nm in objs:
                land_old.append(nm)
    land_old.append("LS_shrub_UNRESOLVED_species_documented_symbol")
    remove = shell_old + screen_old + slab_old + open_old + fr_old + skirt_old + land_old
    missing = [n for n in remove if n not in objs]
    assert not missing, f"objects expected in v007 not found: {missing}"

    # materials / collections captured from the replaced objects
    def mat_pair(o):
        side = top = None
        for p in o.data.polygons:
            nrm = (o.matrix_world.to_3x3() @ p.normal).normalized()
            if nrm.z > 0.9:
                top = o.material_slots[p.material_index].material if o.material_slots else None
            elif abs(nrm.z) < 0.1:
                side = o.material_slots[p.material_index].material if o.material_slots else None
        return side, top
    zone_mats = {n: mat_pair(objs[n]) for n in shell_old}
    screen_mat = objs[screen_old[0]].material_slots[0].material
    slab_mat = objs["BI_L2_floor_slab"].material_slots[0].material
    open_mat = objs[open_old[0]].material_slots[0].material
    skirt_mat = objs[skirt_old[0]].material_slots[0].material
    skirt_col = objs[skirt_old[0]].users_collection[0]
    old_open_bbox = {n: bbox_ft(objs[n]) for n in open_old}
    old_zone_bbox = {n: [round(v, 2) for v in bbox_ft(objs[n])] for n in shell_old}
    old_fr_hash = {}
    for n in fr_old:
        h = hashlib.sha256()
        for v in objs[n].data.vertices:
            w = objs[n].matrix_world @ v.co
            h.update(f"{w.x:.4f},{w.y:.4f},{w.z:.4f};".encode())
        old_fr_hash[n] = h.hexdigest()
    keep_names = [o.name for o in objs if o.type == "MESH" and o.name not in set(remove)]
    h_before = geometry_hash(keep_names)
    for nm in remove:
        o = objs[nm]
        me = o.data
        bpy.data.objects.remove(o, do_unlink=True)
        if me.users == 0:
            bpy.data.meshes.remove(me)

    # ------------------------------------------------------------------ 2. corrected zone polygons
    fp1 = [tuple(p) for p in G["footprint_union"]]
    i0 = [i for i, p in enumerate(fp1) if abs(p[0] - 71.0) < 1e-6 and abs(p[1] - 120.38) < 1e-6][0]
    i1 = [i for i, p in enumerate(fp1) if abs(p[0] - 148.25) < 1e-6 and abs(p[1] - 197.5) < 1e-6][0]
    west_side = fp1[i0:i1 + 1]
    assert len(west_side) == 40, f"unexpected v001 west-side vertex count {len(west_side)}"
    Z1L1 = [tuple(p) for p in Z["Z1_L1_south_block"]["poly"]]
    Z1L2 = [tuple(p) for p in Z["Z1_L2_south_block"]["poly"]]
    bay = Z["P3_L2_south_bay"]
    bay_poly = v1.rect(bay["x0"], bay["y0"], bay["x1"], bay["y1"])
    bd = Z["Z2_band_lobby"]
    band_poly = v1.rect(bd["x0"], bd["y0"], bd["x1"], bd["y1"])
    ves = G["vestibule_100"]
    ves_poly = v1.rect(ves["x0"], ves["y0"], ves["x1"], ves["y1"])
    se = Z["Z5_end_block_13_14"]
    se_poly = v1.rect(se["x0"], se["y0"], se["x1"], se["y1"])
    z4b = Z["Z4b_north_block_south_part"]
    z4b_poly = v1.rect(z4b["x0"], z4b["y0"], z4b["x1"], z4b["y1"])
    z4a = Z["Z4a_north_block"]
    z4a_polys = {}
    for key in ("L1_north_east", "mid_north_east", "L2_north_east"):
        z4a_polys[key] = [(71.0, 97.75)] + list(west_side) + [tuple(p) for p in z4a[key]]

    def north_top(x, y):
        return 33.15 + (y - 80.5) * 0.0535

    def band_top(x, y):
        b = G["band_E_F2"]
        t = max(0.0, min(1.0, (x - 30.0) / (b["x1"] - 30.0)))
        return b["top_at_x30"] + t * (b["top_at_x71"] - b["top_at_x30"])

    shell = cols["01_Shell"]

    def make(name, poly, z0, ztop, matkey):
        side, top = zone_mats[matkey]
        o = prism_robust(name, poly, z0, ztop, shell, side)
        if top is not None and top != side:
            o.data.materials.append(top)
            for p in o.data.polygons:
                nrm = (o.matrix_world.to_3x3() @ p.normal).normalized()
                p.material_index = 1 if nrm.z > 0.9 else 0
        return o

    new_zones = {}
    new_zones["Z1_L1"] = make("BI_Z1_south_wing_L1", Z1L1, Z["Z1_L1_south_block"]["z0"], Z["Z1_L1_south_block"]["z1"], "BI_Z1_south_wing")
    new_zones["Z1_L2"] = make("BI_Z1_south_wing_L2", Z1L2, Z["Z1_L2_south_block"]["z0"], Z["Z1_L2_south_block"]["z1"], "BI_Z1_south_wing")
    new_zones["bay"] = make("BI_Z1_L2_storefront_projection_bay", bay_poly, bay["z0"], bay["z1"], "BI_Z1_south_wing")
    new_zones["band"] = make("BI_Z2_band_E_F2", band_poly, 0.0, band_top, "BI_Z2_band_E_F2")
    new_zones["se"] = make("BI_Z5_end_block_13_14", se_poly, se["z0"], se["z1"], "BI_Z5_end_block_13_14")
    new_zones["Z4b"] = make("BI_Z4b_north_block_south_part", z4b_poly, z4b["z0"], north_top, "BI_Z4b_north_block_south_part")
    new_zones["Z4a_L1"] = make("BI_Z4a_north_block_L1", z4a_polys["L1_north_east"], 0.0, H["gallery_soffit"]["z"], "BI_Z4a_north_block")
    new_zones["Z4a_mid"] = make("BI_Z4a_north_block_mid", z4a_polys["mid_north_east"], H["gallery_soffit"]["z"], H["L2_slab_underside"]["z"], "BI_Z4a_north_block")
    new_zones["Z4a_L2"] = make("BI_Z4a_north_block_L2", z4a_polys["L2_north_east"], H["L2_slab_underside"]["z"], north_top, "BI_Z4a_north_block")
    for o in new_zones.values():
        o["source"] = "BI_footprint_data_v008.json"
    zone_polys = {"Z1_L1": Z1L1, "Z1_L2": Z1L2, "bay": bay_poly, "band": band_poly, "ves": ves_poly, "se": se_poly, "Z4b": z4b_poly,
                  "Z4a_L1": z4a_polys["L1_north_east"], "Z4a_mid": z4a_polys["mid_north_east"], "Z4a_L2": z4a_polys["L2_north_east"]}
    zone_z0 = {"Z1_L1": 0.0, "Z1_L2": 13.5, "bay": bay["z0"], "band": 0.0, "ves": 0.0, "se": 0.0, "Z4b": 0.0, "Z4a_L1": 0.0, "Z4a_mid": H["gallery_soffit"]["z"], "Z4a_L2": H["L2_slab_underside"]["z"]}
    # cap tessellation sanity: every zone polygon must be simple (no self-intersection) -> area equals the sum of its cap triangles
    tess = {}
    for k, o in new_zones.items():
        area_top = sum(p.area for p in o.data.polygons if p.normal.z > 0.9) / FT / FT
        area_bot = sum(p.area for p in o.data.polygons if p.normal.z < -0.9) / FT / FT
        tess[k] = {"cap_area_top_sqft": round(area_top, 1), "cap_area_bottom_sqft": round(area_bot, 1), "polygon_area_sqft": round(poly_area(zone_polys[k]), 1)}
    print("TESSELLATION=" + json.dumps(tess))
    for k, v in tess.items():
        # sloped tops (formula) are slightly larger than the plan area; the flat bottom cap must match the polygon exactly
        assert abs(v["cap_area_bottom_sqft"] - v["polygon_area_sqft"]) < 1.0, f"cap tessellation of {k} does not match its polygon: {v}"

    # ------------------------------------------------------------------ 3. parapet screen strips on the Level 2 south-block faces
    W = G["wing"]
    sc = cols["02_Parapet_screens"]
    prof = W["south_screen_profile"]
    t = W["screen_thickness"]
    n_strip = 0
    strips = []
    if poly_area(Z1L2) and sum(Z1L2[i - 1][0] * Z1L2[i][1] - Z1L2[i][0] * Z1L2[i - 1][1] for i in range(len(Z1L2))) < 0:
        Z1L2_ccw = Z1L2[::-1]
    else:
        Z1L2_ccw = Z1L2
    for i in range(len(Z1L2_ccw)):
        (xa, ya), (xb, yb) = Z1L2_ccw[i], Z1L2_ccw[(i + 1) % len(Z1L2_ccw)]
        if min(ya, yb) >= 54.2 - 1e-6:      # north edge and the edge buried in the lobby band
            continue
        dx, dy = xb - xa, yb - ya
        Ln = math.hypot(dx, dy)
        inward = (-dy / Ln, dx / Ln)   # left-hand normal of a CCW polygon points inward
        if abs(ya - yb) < 1e-6 and ya < 5:                       # south-facing edges (y -1.46 / 2.88 / 2.91)
            lo, hi = sorted((xa, xb))
            lo2, hi2 = max(lo, prof[0][0]), min(hi, prof[-1][0])
            if hi2 - lo2 > 0.5:
                xs = [lo2] + [p[0] for p in prof if lo2 < p[0] < hi2] + [hi2]
                for x0, x1 in zip(xs, xs[1:]):
                    if x1 - x0 < 0.05:
                        continue
                    n_strip += 1
                    nm = f"BI_screen_south_{n_strip:02d}"
                    v1.slab_strip(nm, (x0, ya), (x1, ya), (0, 1), t, W["parapet_top"], v1.profile_value(prof, x0), v1.profile_value(prof, x1), sc, screen_mat)
                    strips.append(nm)
        elif abs(xa - xb) < 1e-6 and max(ya, yb) <= 5:          # recess returns (x 91.66 / 118.33 / 241.67) facing east or west
            n_strip += 1
            nm = f"BI_screen_south_return_{n_strip:02d}"
            zt = v1.profile_value(prof, xa)
            v1.slab_strip(nm, (xa, ya), (xb, yb), inward, t, W["parapet_top"], zt, zt, sc, screen_mat)
            strips.append(nm)
        elif abs(xa - xb) < 1e-6 and xa > 271:                    # east face of the south block (x 271.29)
            e = W["east_screen"]
            lo, hi = sorted((ya, yb))
            lo2, hi2 = max(lo, e["y0"]), min(hi, se["y0"])
            if hi2 - lo2 > 0.5:
                n_strip += 1
                nm = f"BI_screen_east_{n_strip:02d}"
                v1.slab_strip(nm, (xa, lo2), (xa, hi2), (-1, 0), t, W["parapet_top"], e["top"], e["top"], sc, screen_mat)
                strips.append(nm)
        elif abs(xa - xb) < 1e-6 and xa < 11:                     # west face of the wing (x 10.67)
            w = W["west_screen"]
            lo, hi = sorted((ya, yb))
            lo2, hi2 = max(lo, w["y0"]), min(hi, 54.2)
            if hi2 - lo2 > 0.5:
                n_strip += 1
                nm = f"BI_screen_west_{n_strip:02d}"
                v1.slab_strip(nm, (xa, lo2), (xa, hi2), (1, 0), t, W["parapet_top"], w["top"], w["top"], sc, screen_mat)
                strips.append(nm)

    # ------------------------------------------------------------------ 4. openings re-placed on the corrected faces
    oc = cols["04_Openings"]
    placed, skipped, rotated = 0, 0, 0
    open_rec = []
    for facade, boxes in G["openings"].items():
        for j, (u0, u1, z0, z1) in enumerate(boxes):
            name = f"BI_open_{facade}_{j+1:03d}"
            uc, zc = (u0 + u1) / 2, (z0 + z1) / 2
            cands = [zone_polys[k] for k in zone_polys if zone_z0[k] - 0.01 <= zc <= ZONE_TOPS[k] + 0.01]
            coord, edge = boundary_hit(cands, facade, uc)
            if coord is None:
                skipped += 1
                open_rec.append({"object": name, "facade": facade, "u": [u0, u1], "z": [z0, z1], "plane_before": None, "plane_after": None, "skipped": True})
                continue
            a, b = edge
            axis_aligned = abs(a[0] - b[0]) < 1e-9 or abs(a[1] - b[1]) < 1e-9
            d = 0.15
            if axis_aligned:
                if facade == "SOUTH":
                    v1.box(name, u0, coord - 0.05, z0, u1, coord - 0.05 + d, z1, oc, open_mat)
                elif facade == "NORTH":
                    v1.box(name, u0, coord + 0.05 - d, z0, u1, coord + 0.05, z1, oc, open_mat)
                elif facade == "EAST":
                    v1.box(name, coord + 0.05 - d, u0, z0, coord + 0.05, u1, z1, oc, open_mat)
                else:
                    v1.box(name, coord - 0.05, u0, z0, coord - 0.05 + d, u1, z1, oc, open_mat)
            else:  # diagonal edge (canted storefront): panel aligned with the edge
                rotated += 1
                if facade in ("SOUTH", "NORTH"):
                    def pt(u):
                        return (u, a[1] + (u - a[0]) * (b[1] - a[1]) / (b[0] - a[0]))
                else:
                    def pt(u):
                        return (a[0] + (u - a[1]) * (b[0] - a[0]) / (b[1] - a[1]), u)
                p0, p1 = pt(u0), pt(u1)
                ex, ey = p1[0] - p0[0], p1[1] - p0[1]
                Ln = math.hypot(ex, ey)
                nx, ny = ey / Ln, -ex / Ln          # right-hand normal
                outward = {"SOUTH": (0, -1), "NORTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}[facade]
                if nx * outward[0] + ny * outward[1] < 0:
                    nx, ny = -nx, -ny
                poly = [(p0[0] + nx * 0.05, p0[1] + ny * 0.05), (p1[0] + nx * 0.05, p1[1] + ny * 0.05),
                        (p1[0] - nx * (d - 0.05), p1[1] - ny * (d - 0.05)), (p0[0] - nx * (d - 0.05), p0[1] - ny * (d - 0.05))]
                v1.prism(name, poly, z0, z1, oc, open_mat)
            ob = old_open_bbox.get(name)
            if ob is not None:
                before = (ob[1] + ob[4]) / 2 if facade in ("SOUTH", "NORTH") else (ob[0] + ob[3]) / 2
            else:
                before = None
            open_rec.append({"object": name, "facade": facade, "u": [u0, u1], "z": [z0, z1], "plane_before": None if before is None else round(before, 2),
                             "plane_after": round(coord, 2), "diagonal": not axis_aligned})
            placed += 1
    moved = [r for r in open_rec if r.get("plane_before") is not None and abs(r["plane_before"] - r["plane_after"]) > 0.05]

    # ------------------------------------------------------------------ 5. Level 2 slab reference + foundation skirts
    l2 = H["level2_slab"]
    prism_robust("BI_L2_floor_slab", Z1L2, l2["z_top"] - l2["thickness"], l2["z_top"], cols["06_Reference"], slab_mat)
    sk = S["foundation_skirt"]
    skirts = []
    for key, poly in (("Z1", Z1L1), ("band", band_poly), ("vestibule", ves_poly), ("end_block", se_poly), ("Z4b", z4b_poly), ("Z4a", z4a_polys["L1_north_east"])):
        nm = f"SITE_foundation_skirt_{key}_A"
        prism_robust(nm, poly, sk["z_top"] - sk["depth"], sk["z_top"], skirt_col, skirt_mat)
        skirts.append(nm)

    # ------------------------------------------------------------------ 6. finish regions (v005 algorithm, v008 data) on the new faces
    OFF = R["meta"]["offset_ft"]
    col = cols["07_Facade_regions_v005"]
    faces = []
    zone_objs = [o for c in R["face_collections"] for o in bpy.data.collections[c].objects if o.type == "MESH" and o.name not in R["skip_objects"]]
    for o in zone_objs:
        mw = o.matrix_world
        for p in o.data.polygons:
            n = (mw.to_3x3() @ p.normal).normalized()
            if abs(n.z) > 0.01:
                continue
            pts = [mw @ o.data.vertices[i].co for i in p.vertices]
            if abs(n.x) > 0.99:
                dd = "EAST" if n.x > 0 else "WEST"
                faces.append({"dir": dd, "plane": sum(q.x for q in pts) / len(pts) / FT, "poly": [(q.y / FT, q.z / FT) for q in pts], "obj": o.name, "n": n})
            elif abs(n.y) > 0.99:
                dd = "NORTH" if n.y > 0 else "SOUTH"
                faces.append({"dir": dd, "plane": sum(q.y for q in pts) / len(pts) / FT, "poly": [(q.x / FT, q.z / FT) for q in pts], "obj": o.name, "n": n})
    solids = list(new_zones.values())

    def buried(f):
        cx = sum(q[0] for q in f["poly"]) / len(f["poly"])
        cz = sum(q[1] for q in f["poly"]) / len(f["poly"])
        pt = (Vector((m(f["plane"]), m(cx), m(cz))) if f["dir"] in ("EAST", "WEST") else Vector((m(cx), m(f["plane"]), m(cz)))) + f["n"] * m(0.2)
        for s in solids:
            if s.name == f["obj"]:
                continue
            inv = s.matrix_world.inverted()
            o_ = inv @ pt
            direction = (inv.to_3x3() @ Vector((0, 0, 1))).normalized()
            hits = 0
            for _ in range(20):
                hit, loc, nrm, idx = s.ray_cast(o_, direction)
                if not hit:
                    break
                hits += 1
                o_ = loc + direction * 1e-4
            if hits % 2 == 1:
                return True
        return False
    faces = [f for f in faces if not buried(f)]
    diag_faces = [o for o in oc.objects]  # openings (axis-aligned bbox used for subtraction, as v005)
    op = []
    for o in diag_faces:
        b = bbox_ft(o)
        if (b[3] - b[0]) < (b[4] - b[1]):
            op.append({"axis": "x", "plane": (b[0] + b[3]) / 2, "rect": (b[1], b[4], b[2], b[5])})
        else:
            op.append({"axis": "y", "plane": (b[1] + b[4]) / 2, "rect": (b[0], b[3], b[2], b[5])})
    mats = {k: bpy.data.materials[v] for k, v in R["materials"].items()}
    regs = R["regions"]
    new_fr_hash = {}
    area_by_mat = {}
    for i, r in enumerate(regs):
        later = [q for q in regs[i + 1:] if q["facade"] == r["facade"]]
        bm = bmesh.new()
        area = 0.0
        for f in faces:
            if f["dir"] != r["facade"]:
                continue
            fu0 = min(q[0] for q in f["poly"]); fu1 = max(q[0] for q in f["poly"])
            fz0 = min(q[1] for q in f["poly"]); fz1 = max(q[1] for q in f["poly"])
            base = (max(r["u0"], fu0), min(r["u1"], fu1), max(r["z0"], fz0), min(r["z1"], fz1))
            if base[1] - base[0] < 0.05 or base[3] - base[2] < 0.05:
                continue
            rects = [base]
            for q in later:
                rects = v5.rects_minus(rects, (q["u0"], q["u1"], q["z0"], q["z1"]))
            axis = "x" if r["facade"] in ("EAST", "WEST") else "y"
            for oo in op:
                if oo["axis"] == axis and abs(oo["plane"] - f["plane"]) < 0.35:
                    rects = v5.rects_minus(rects, oo["rect"])
            for (u0, u1, z0, z1) in rects:
                poly = v5.clip_poly(f["poly"], u0, u1, z0, z1)
                if not poly:
                    continue
                verts = []
                for (u, z) in poly:
                    p3 = (Vector((m(f["plane"]), m(u), m(z))) if axis == "x" else Vector((m(u), m(f["plane"]), m(z)))) + f["n"] * m(OFF)
                    verts.append(bm.verts.new(p3))
                try:
                    face = bm.faces.new(verts)
                except ValueError:
                    continue
                if face.normal.dot(f["n"]) < 0:
                    face.normal_flip()
                area += abs(sum(poly[k - 1][0] * poly[k][1] - poly[k][0] * poly[k - 1][1] for k in range(len(poly)))) / 2
        if len(bm.faces) == 0:
            bm.free()
            continue
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0005)
        name = f"FR_{r['facade']}_{r['mat']}_{r['id']}"
        mesh = bpy.data.meshes.new(name)
        bm.to_mesh(mesh)
        bm.free()
        obj = bpy.data.objects.new(name, mesh)
        obj.data.materials.append(mats[r["mat"]])
        obj["basis"] = r["basis"]; obj["note"] = r["note"]; obj["region_ft"] = json.dumps([r["u0"], r["u1"], r["z0"], r["z1"]])
        col.objects.link(obj)
        h = hashlib.sha256()
        for v in obj.data.vertices:
            w = obj.matrix_world @ v.co
            h.update(f"{w.x:.4f},{w.y:.4f},{w.z:.4f};".encode())
        new_fr_hash[name] = h.hexdigest()
        area_by_mat[r["mat"]] = round(area_by_mat.get(r["mat"], 0) + area, 1)
    fr_changed = sorted(n for n in new_fr_hash if old_fr_hash.get(n) != new_fr_hash[n])
    fr_missing = sorted(n for n in old_fr_hash if n not in new_fr_hash)
    fr_added = sorted(n for n in new_fr_hash if n not in old_fr_hash)

    # ------------------------------------------------------------------ 7. landscape groups against the corrected Level 1 footprint
    L1_polys = [Z1L1, band_poly, ves_poly, se_poly, z4b_poly, z4a_polys["L1_north_east"]]
    SZ = L["sizes_for_model"]
    M = {k: bpy.data.materials[f"LS_{k}"] for k in L["materials"]}
    spots = [(s_["x"], s_["y"], s_["z"] - FFE) for s_ in S["spots"]]

    def idw(x, y):
        num = den = 0.0
        for sx, sy, sz in spots:
            d2 = (sx - x) ** 2 + (sy - y) ** 2
            if d2 < 0.01:
                return sz
            w_ = 1.0 / (d2 ** 1.5)
            num += w_ * sz
            den += w_
        return num / den
    surfaces = [o for o in objs if o.type == "MESH" and o.name.startswith(("SITE_terrain", "SITE_asphalt", "SITE_walk", "SITE_entry", "SITE_plaza"))]

    def grade(x, y):
        best = None
        origin = Vector((m(x), m(y), m(200.0)))
        for o in surfaces:
            inv = o.matrix_world.inverted()
            hit, loc, _n, _i = o.ray_cast(inv @ origin, (inv.to_3x3() @ Vector((0, 0, -1))).normalized())
            if hit:
                zz = (o.matrix_world @ loc).z
                if best is None or zz > best:
                    best = zz
        return best if best is not None else m(idw(x, y))
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

    def push(x, y):
        total = 0.0
        for poly in L1_polys:
            if v4.point_in_poly(x, y, poly):
                x, y, dsh = v4.push_outside(x, y, poly, 1.2)
                total += dsh
        return x, y, total
    sub = {k: cols[f"09_Landscape_v004_{k}"] for k in ("trees", "shrubs", "groundcover", "beds_islands", "context")}
    restored, still_pushed, built = [], [], []

    def build_group(code, sheet, n, items):
        info = sched[code]
        tp = info["type"]
        hh = info.get("height_in_min", 18) / 12 if tp == "shrub" else (0.6 if tp == "annual" else (0.8 if code in ("MUHL", "CARZ", "CARE", "RUSS", "CATM") else 0.6))
        ww = min(info.get("spacing_ft", 3), 1.3 * hh) if tp == "shrub" else (1.0 if tp == "annual" else min(info.get("spacing_in", 24) / 12, 2.0))
        bm = bmesh.new()
        bmm = bmesh.new()
        for p in items:
            x, y, dsh = push(p["x"], p["y"])
            was_shifted = (code, round(p["x"], 2), round(p["y"], 2)) in shifted_keys or p.get("keep_documented")
            if dsh:
                still_pushed.append({"code": code, "from": [p["x"], p["y"]], "to": [round(x, 2), round(y, 2)], "shift_ft": round(dsh, 2)})
            elif was_shifted:
                restored.append({"code": code, "x": p["x"], "y": p["y"]})
            zz = grade(x, y) + (m(0.5) if on_island(x, y) else 0.0)
            v4.add_sphere(bm, m(x), m(y), zz + m(hh * 0.5), m(ww / 2), m(ww / 2), m(hh * 0.55), seg=8, ring=5)
            v4.add_disc(bmm, m(x), m(y), zz + m(0.06), m(SZ["mulch_disc_radius_ft"]))
        suffix = "" if n else "_adj"
        name = f"LS_{tp}_{code}_{sheet}_n{n}{suffix}"
        o = v4.new_object(name, bm, sub["shrubs" if tp == "shrub" else "groundcover"], foliage_mat(code))
        o["conf"] = ",".join(sorted(set(p["conf"] for p in items)))
        o["source"] = f"{sheet} callout ({n}) {code}" if n else f"{sheet} {items[0].get('basis', '')}"
        o["schedule"] = json.dumps(info)
        om = v4.new_object(f"LS_mulch_{code}_{sheet}_n{n}{suffix}_INTERPRETED", bmm, sub["beds_islands"], M["mulch"])
        om["note"] = "mulch disc per documented plant; bed outline not modeled (I)"
        built.append(name)
    for key in affected:
        build_group(*key, groups[key])
    bm = bmesh.new()
    unres_pushed = 0
    for u in L["unassigned_symbols"]:
        x, y, dsh = push(u["x"], u["y"])
        unres_pushed += 1 if dsh else 0
        zz = grade(x, y) + (m(0.5) if on_island(x, y) else 0.0)
        v4.add_sphere(bm, m(x), m(y), zz + m(0.75), m(1.4), m(1.4), m(0.8), seg=8, ring=5)
    o = v4.new_object("LS_shrub_UNRESOLVED_species_documented_symbol", bm, sub["shrubs"], bpy.data.materials["LS_unresolved_grey_green"])
    o["note"] = f"{len(L['unassigned_symbols'])} plant symbols drawn on LP-100/LP-101 not linked to a callout leader; species unresolved (U)"
    plant_count = sum(len(v) for v in groups.values())

    # ------------------------------------------------------------------ 8. validation cameras
    camcol = cols["90_Cameras"]

    def add_cam(name, loc, target, lens=35.0, ortho=None):
        c = bpy.data.cameras.new(name); c.lens = lens; c.clip_end = 3000
        if ortho:
            c.type = "ORTHO"; c.ortho_scale = m(ortho)
        o_ = bpy.data.objects.new(name, c)
        o_.location = Vector((m(loc[0]), m(loc[1]), m(loc[2])))
        dv = Vector((m(target[0]), m(target[1]), m(target[2]))) - o_.location
        o_.rotation_euler = dv.to_track_quat("-Z", "Y").to_euler()
        camcol.objects.link(o_)
        return o_
    for name, (cx, cy, w) in PLAN_CAMS.items():
        add_cam(name, (cx, cy, 300.0), (cx, cy, 0.0), ortho=w)
    add_cam("BI_cam_oblique_southeast", (470.0, -330.0, 150.0), (150.0, 80.0, 12.0), lens=35.0)

    h_after = geometry_hash(keep_names)
    assert h_before == h_after, "unrelated geometry changed - aborting"
    ext = [1e9, 1e9, 1e9, -1e9, -1e9, -1e9]
    for o in shell.objects:
        b = bbox_ft(o)
        ext = [min(ext[0], b[0]), min(ext[1], b[1]), min(ext[2], b[2]), max(ext[3], b[3]), max(ext[4], b[4]), max(ext[5], b[5])]
    report = {"version": "v008", "base": str(BASE), "kept_mesh_objects": len(keep_names), "geometry_hash_kept": h_before, "unrelated_geometry_unchanged": True,
              "shell_objects_replaced": {k: v for k, v in old_zone_bbox.items()}, "shell_objects_built": {k: [round(v, 2) for v in bbox_ft(o)] for k, o in new_zones.items()},
              "shell_extent_ft": [round(v, 2) for v in ext], "cap_tessellation_check": tess,
              "screens": {"removed": len(screen_old), "built": len(strips)}, "openings": {"placed": placed, "skipped": skipped, "rotated_on_canted_wall": rotated, "moved_gt_0_05ft": len(moved)},
              "openings_moved": moved, "skirts": skirts,
              "facade_regions": {"regenerated": len(new_fr_hash), "changed": len(fr_changed), "removed": fr_missing, "added": fr_added, "area_by_mat_sqft": area_by_mat},
              "landscape": {"groups_rebuilt": [list(k) for k in affected], "objects_built": built, "plants_total_in_data": plant_count, "plants_restored_to_documented_position": len(restored),
                            "plants_still_pushed": len(still_pushed), "still_pushed_detail": still_pushed, "unresolved_symbols": len(L["unassigned_symbols"]), "unresolved_symbols_pushed": unres_pushed},
              "cameras_added": list(PLAN_CAMS) + ["BI_cam_oblique_southeast"]}
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
        scene.cycles.samples = 64; scene.cycles.use_denoising = True
        scene.render.image_settings.file_format = "PNG"; scene.view_settings.view_transform = "Standard"
        times = {}
        for view, (cam, (rx, ry)) in VIEWS.items():
            scene.camera = objs[cam]
            scene.render.resolution_x, scene.render.resolution_y = rx, ry
            path = render_dir / f"{STEM}_{view}.png"
            if path.exists():
                raise SystemExit(f"refusing to overwrite existing render: {path}")
            scene.render.filepath = str(path)
            t0 = time.time(); bpy.ops.render.render(write_still=True); times[view] = round(time.time() - t0, 1)
        report["render_seconds"] = times
        scene.camera = objs["BI_cam_oblique_southeast"]
        bpy.ops.wm.save_mainfile()
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("BUILD_REPORT=" + json.dumps({k: v for k, v in report.items() if k not in ("openings_moved", "landscape")}))
    print("LANDSCAPE=" + json.dumps({k: v for k, v in report["landscape"].items() if k != "still_pushed_detail"}))


# top-down orthographic validation cameras: name -> (centre x, centre y, ortho width ft)
PLAN_CAMS = {"BI_cam_plan_top": (147.0, 100.0, 340.0), "BI_cam_plan_G8_south": (140.0, 2.0, 300.0),
             "BI_cam_plan_G9_wing_north": (30.0, 52.0, 90.0), "BI_cam_plan_G10_northeast": (262.0, 178.0, 80.0)}
VIEWS = {"plan_top": ("BI_cam_plan_top", (3000, 2200)), "plan_G8_south": ("BI_cam_plan_G8_south", (3000, 700)),
         "plan_G9_wing_north": ("BI_cam_plan_G9_wing_north", (1800, 1800)), "plan_G10_northeast": ("BI_cam_plan_G10_northeast", (1800, 1800)),
         "oblique_northwest": ("BI_cam_oblique_northwest", (2000, 1400)), "oblique_southeast": ("BI_cam_oblique_southeast", (2000, 1400)),
         "site_elevated": ("BI_cam_site_elevated", (2000, 1400)), "rear_south": ("BI_cam_rear_south", (2400, 900)), "right_east": ("BI_cam_right_east", (2400, 900))}

if __name__ == "__main__":
    main()
