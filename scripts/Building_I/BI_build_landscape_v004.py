r"""Building I - landscape / immediate-context baseline v004 (skill gate: landscape + context).

Opens the OWNER-APPROVED BI_site_v003.blend, verifies every v003 mesh object is unchanged (vertex + material hash),
adds collection 09_Landscape_v004 with objects prefixed LS_ (documented plantings) and CTX_ (existing street trees),
and saves models/Building_I/BI_landscape_v004.blend plus renders/Building_I/BI_landscape_v004_*.png.
Data: notes/Building_I/BI_landscape_data_v004.json (plants, ground-cover patches, parking islands, schedule).
Nothing from v001-v003 is moved or edited. Refuses to overwrite existing outputs.

Run:  "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --background --python scripts/Building_I/BI_build_landscape_v004.py
Optional:  -- --no-render   |   -- --out <folder>  (trial runs)
"""
import hashlib
import json
import math
import sys
import time
from pathlib import Path

import bmesh
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parent.parent.parent
BASE = ROOT / "models" / "Building_I" / "BI_site_v003.blend"
DATA = ROOT / "notes" / "Building_I" / "BI_landscape_data_v004.json"
GEOM = ROOT / "notes" / "Building_I" / "BI_geometry_data_v001.json"
SITE = ROOT / "notes" / "Building_I" / "BI_site_data_v003.json"
VERSION = "v004"
STEM = "BI_landscape_v004"
FT = 0.3048
FFE = 661.75


def m(ft):
    return ft * FT


def geometry_hash(names):
    h = hashlib.sha256()
    for n in sorted(names):
        o = bpy.data.objects[n]
        h.update(n.encode())
        for v in o.data.vertices:
            w = o.matrix_world @ v.co
            h.update(f"{w.x:.5f},{w.y:.5f},{w.z:.5f};".encode())
        h.update(",".join(s.material.name if s.material else "-" for s in o.material_slots).encode())
    return h.hexdigest()


def material(name, rgb, rough=0.9):
    mat = bpy.data.materials.get(name)
    if mat:
        return mat
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    return mat


def new_object(name, bm, col, mat):
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    obj.data.materials.append(mat)
    col.objects.link(obj)
    return obj


def point_in_poly(x, y, poly):
    inside = False
    n = len(poly)
    for i in range(n):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % n]
        if (y0 > y) != (y1 > y):
            xi = x0 + (y - y0) * (x1 - x0) / (y1 - y0)
            if xi > x:
                inside = not inside
    return inside


def push_outside(x, y, poly, clearance):
    """If (x,y) lies inside poly, move it outward across the nearest edge by (distance + clearance)."""
    if not point_in_poly(x, y, poly):
        return x, y, 0.0
    best = None
    n = len(poly)
    for i in range(n):
        ax, ay = poly[i]
        bx, by = poly[(i + 1) % n]
        dx, dy = bx - ax, by - ay
        L2 = dx * dx + dy * dy or 1e-9
        t = max(0.0, min(1.0, ((x - ax) * dx + (y - ay) * dy) / L2))
        px, py = ax + t * dx, ay + t * dy
        d = math.hypot(x - px, y - py)
        if best is None or d < best[0]:
            best = (d, px, py)
    d, px, py = best
    if d < 1e-6:
        return x, y, 0.0
    ux, uy = (px - x) / d, (py - y) / d
    nx, ny = x + ux * (d + clearance), y + uy * (d + clearance)
    if point_in_poly(nx, ny, poly):  # pushed across a thin part: try the opposite direction
        nx, ny = x - ux * (d + clearance), y - uy * (d + clearance)
    return nx, ny, d + clearance


def add_sphere(bm, cx, cy, cz, rx, ry, rz, seg=10, ring=6):
    r = bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=ring, radius=1.0)
    for v in r["verts"]:
        v.co = Vector((cx + v.co.x * rx, cy + v.co.y * ry, cz + v.co.z * rz))


def add_cylinder(bm, cx, cy, z0, z1, r, seg=8):
    r_ = bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r, depth=z1 - z0)
    for v in r_["verts"]:
        v.co = Vector((cx + v.co.x, cy + v.co.y, (z0 + z1) / 2 + v.co.z))


def add_disc(bm, cx, cy, z, r, seg=12):
    r_ = bmesh.ops.create_circle(bm, cap_ends=True, segments=seg, radius=r)
    for v in r_["verts"]:
        v.co = Vector((cx + v.co.x, cy + v.co.y, z))


def add_prism(bm, poly, z0, z1):
    verts = [bm.verts.new((m(x), m(y), z0)) for x, y in poly]
    try:
        f = bm.faces.new(verts)
    except ValueError:
        return
    res = bmesh.ops.extrude_face_region(bm, geom=[f])
    for v in [g for g in res["geom"] if isinstance(g, bmesh.types.BMVert)]:
        v.co.z = z1
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)


def add_camera(name, loc, target, col, lens=35.0):
    cam = bpy.data.cameras.new(name)
    cam.lens = lens
    cam.clip_end = 3000
    o = bpy.data.objects.new(name, cam)
    o.location = Vector((m(loc[0]), m(loc[1]), m(loc[2])))
    d = Vector((m(target[0]), m(target[1]), m(target[2]))) - o.location
    o.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    col.objects.link(o)
    return o


def setup_gpu(scene):
    try:
        prefs = bpy.context.preferences.addons["cycles"].preferences
        for backend in ("OPTIX", "CUDA", "HIP", "ONEAPI", "METAL"):
            try:
                prefs.compute_device_type = backend
            except TypeError:
                continue
            prefs.get_devices()
            devs = [d for d in prefs.devices if d.type == backend]
            if devs:
                for d in prefs.devices:
                    d.use = d.type in (backend, "CPU")
                scene.cycles.device = "GPU"
                return {"backend": backend, "devices": [d.name for d in devs]}
    except Exception as e:  # noqa
        return {"backend": "CPU", "error": str(e)}
    return {"backend": "CPU"}


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
    v003_names = [o.name for o in bpy.data.objects if o.type == "MESH"]
    h_before = geometry_hash(v003_names)

    D = json.loads(DATA.read_text(encoding="utf-8"))
    G = json.loads(GEOM.read_text(encoding="utf-8"))
    S = json.loads(SITE.read_text(encoding="utf-8"))
    fp = [tuple(p) for p in G["footprint_union"]]
    band = S["exclusions"]["band"]
    ves = S["exclusions"]["vestibule"]
    footprint_polys = [fp, [(band[0], band[1]), (band[2], band[1]), (band[2], band[3]), (band[0], band[3])],
                       [(ves[0], ves[1]), (ves[2], ves[1]), (ves[2], ves[3]), (ves[0], ves[3])]]
    walls = [(w["x0"], w["y0"], w["x1"], w["y1"]) for w in S["walls"].values()] if isinstance(S.get("walls"), dict) else []

    # ---- grade lookup: ray-cast the v003 terrain / hardscape; fall back to IDW through the v003 spots
    spots = [(s_["x"], s_["y"], s_["z"] - FFE) for s_ in S["spots"]]

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

    surfaces = [bpy.data.objects[n] for n in v003_names if n.startswith("SITE_terrain") or n.startswith("SITE_asphalt") or n.startswith("SITE_walk") or n.startswith("SITE_entry") or n.startswith("SITE_plaza")]

    def grade(x, y):
        """z (metres, FFE = 0) of the highest v003 surface under (x,y) ft; IDW if none."""
        best = None
        origin = Vector((m(x), m(y), m(200.0)))
        for o in surfaces:
            inv = o.matrix_world.inverted()
            hit, loc, _n, _i = o.ray_cast(inv @ origin, (inv.to_3x3() @ Vector((0, 0, -1))).normalized())
            if hit:
                z = (o.matrix_world @ loc).z
                if best is None or z > best:
                    best = z
        return best if best is not None else m(idw(x, y))

    # ---- collections
    col = bpy.data.collections.new("09_Landscape_v004")
    scene.collection.children.link(col)
    sub = {}
    for name in ("trees", "shrubs", "groundcover", "beds_islands", "context"):
        c = bpy.data.collections.new(f"09_Landscape_v004_{name}")
        col.children.link(c)
        sub[name] = c
    M = {k: material(f"LS_{k}", v) for k, v in D["materials"].items()}
    SZ = D["sizes_for_model"]
    sched = D["schedule"]

    def foliage_mat(code):
        t = sched.get(code, {}).get("type", "shrub")
        if t == "tree":
            return M["foliage_tree"]
        if code in ("LOPE", "LOJA", "CORA"):
            return M["shrub_purple"]
        if code in ("BLON", "BUNN", "MUHL", "CARZ", "CARE"):
            return M["shrub_grass"]
        if t == "groundcover":
            return M["groundcover"]
        if t == "annual":
            return M["annual"]
        return M["shrub_green"]

    report = {"version": VERSION, "base": str(BASE), "v003_mesh_objects": len(v003_names), "geometry_hash_v003": h_before}
    shifted = []
    placed = {"trees": 0, "shrubs": 0, "groundcover_plants": 0, "unassigned_symbols": 0}

    # ---- plants
    groups = {}
    for p in D["plants"]:
        groups.setdefault((p["code"], p["sheet"], p["callout_n"]), []).append(p)
    islands = D["parking_islands"]["items"]

    def on_island(x, y):
        return any(abs(x - i["x"]) <= i["w"] / 2 and abs(y - i["y"]) <= i["h"] / 2 for i in islands)

    for (code, sheet, n), items in sorted(groups.items()):
        info = sched.get(code, {"type": "shrub"})
        t = info["type"]
        if t == "tree":
            for k, p in enumerate(items):
                x, y, dshift = push_outside(p["x"], p["y"], fp, 3.0)
                if dshift:
                    shifted.append({"code": code, "from": [p["x"], p["y"]], "to": [round(x, 2), round(y, 2)], "shift_ft": round(dshift, 2)})
                z = grade(x, y) + (m(0.5) if on_island(x, y) else 0.0)
                bm = bmesh.new()
                H, C, T = SZ["tree_new"]["height_ft"], SZ["tree_new"]["canopy_ft"], SZ["tree_new"]["trunk_in"] / 12
                add_cylinder(bm, m(x), m(y), z, z + m(H * 0.45), m(T / 2))
                add_sphere(bm, m(x), m(y), z + m(H * 0.68), m(C / 2), m(C / 2), m(H * 0.32))
                o = new_object(f"LS_tree_{code}_{sheet}_{k + 1:02d}", bm, sub["trees"], M["trunk"])
                o.data.materials.append(M["foliage_tree"])
                for f in o.data.polygons:
                    f.material_index = 1 if (o.matrix_world @ o.data.vertices[f.vertices[0]].co).z > z + m(H * 0.45) + 1e-4 else 0
                o["conf"] = p["conf"]
                o["source"] = sheet
                o["schedule"] = json.dumps(info)
                placed["trees"] += 1
        else:
            bm = bmesh.new()
            bmm = bmesh.new()
            if t in ("shrub",):
                h = info.get("height_in_min", 18) / 12
                w = min(info.get("spacing_ft", 3), 1.3 * h)
            elif t == "annual":
                h, w = 0.6, 1.0
            else:
                h = 0.8 if code in ("MUHL", "CARZ", "CARE", "RUSS", "CATM") else 0.6
                w = min(info.get("spacing_in", 24) / 12, 2.0)
            for p in items:
                x, y, dshift = push_outside(p["x"], p["y"], fp, 1.2)
                if dshift:
                    shifted.append({"code": code, "from": [p["x"], p["y"]], "to": [round(x, 2), round(y, 2)], "shift_ft": round(dshift, 2)})
                z = grade(x, y) + (m(0.5) if on_island(x, y) else 0.0)
                add_sphere(bm, m(x), m(y), z + m(h * 0.5), m(w / 2), m(w / 2), m(h * 0.55), seg=8, ring=5)
                add_disc(bmm, m(x), m(y), z + m(0.06), m(SZ["mulch_disc_radius_ft"]))
                placed["shrubs" if t == "shrub" else "groundcover_plants"] += 1
            o = new_object(f"LS_{t}_{code}_{sheet}_n{n}", bm, sub["shrubs" if t == "shrub" else "groundcover"], foliage_mat(code))
            o["conf"] = ",".join(sorted(set(p["conf"] for p in items)))
            o["source"] = f"{sheet} callout ({n}) {code}"
            o["schedule"] = json.dumps(info)
            om = new_object(f"LS_mulch_{code}_{sheet}_n{n}_INTERPRETED", bmm, sub["beds_islands"], M["mulch"])
            om["note"] = "mulch disc per documented plant; bed outline not modeled (I)"

    # unassigned documented symbols: generic shrub, species unresolved
    if D["unassigned_symbols"]:
        bm = bmesh.new()
        for u in D["unassigned_symbols"]:
            x, y, dshift = push_outside(u["x"], u["y"], fp, 1.2)
            z = grade(x, y) + (m(0.5) if on_island(x, y) else 0.0)
            add_sphere(bm, m(x), m(y), z + m(0.75), m(1.4), m(1.4), m(0.8), seg=8, ring=5)
            placed["unassigned_symbols"] += 1
        o = new_object("LS_shrub_UNRESOLVED_species_documented_symbol", bm, sub["shrubs"], material("LS_unresolved_grey_green", (0.35, 0.40, 0.30)))
        o["note"] = "plant symbol drawn on LP-100/LP-101 but not linked to a callout leader; species unresolved (U)"

    # ---- ground-cover patches (hatched areas, INTERPRETED extent). A disc whose centre lands on a v003 hardscape
    # surface (asphalt, walk, plaza) is NOT modeled: the leader direction was ambiguous there; it is reported instead.
    hard = [bpy.data.objects[n] for n in v003_names if n.startswith(("SITE_asphalt", "SITE_walk", "SITE_entry", "SITE_plaza"))]

    def on_hardscape(x, y):
        origin = Vector((m(x), m(y), m(200.0)))
        for o in hard:
            inv = o.matrix_world.inverted()
            hit, _l, _n, _i = o.ray_cast(inv @ origin, (inv.to_3x3() @ Vector((0, 0, -1))).normalized())
            if hit:
                return o.name
        return None

    skipped_patches = []
    for k, h in enumerate(D["groundcover_patches"]):
        poly = [(x, y) for x, y in h["polygon"]]
        cx = sum(p[0] for p in poly) / len(poly)
        cy = sum(p[1] for p in poly) / len(poly)
        hs = on_hardscape(cx, cy)
        if hs:
            skipped_patches.append({"code": h["code"], "n": h["n"], "sheet": h["sheet"], "centre": [round(cx, 1), round(cy, 1)], "on": hs})
            continue
        bm = bmesh.new()
        zc = sum(grade(x, y) for x, y in poly) / len(poly)
        hp = SZ["annual_patch_height_ft"] if h["code"] == "SEAS" else SZ["groundcover_patch_height_ft"]
        add_prism(bm, poly, zc + m(0.05), zc + m(hp))
        o = new_object(f"LS_gcpatch_{h['code']}_{h['sheet']}_n{h['n']}_{h['status']}_INTERPRETED", bm, sub["groundcover"], foliage_mat(h["code"]))
        o["area_sqft"] = h["area_sqft"]
        o["expected_area_sqft"] = h.get("expected_area_sqft", 0)

    # ---- parking islands (LP-100 ovals: 37 x 10 ft, curb +0.5 ft, mulch top)
    for k, i in enumerate(islands):
        bm = bmesh.new()
        pts = []
        r = i["h"] / 2
        for j in range(12):
            a = math.pi / 2 - math.pi * j / 11
            pts.append((i["x"] + i["w"] / 2 - r + r * math.cos(a), i["y"] + r * math.sin(a)))
        for j in range(12):
            a = math.pi / 2 + math.pi * j / 11
            pts.append((i["x"] - i["w"] / 2 + r + r * math.cos(a), i["y"] + r * math.sin(a)))
        zc = grade(i["x"], i["y"])
        add_prism(bm, pts, zc - m(0.3), zc + m(0.5))
        o = new_object(f"LS_parking_island_{k + 1:02d}_LP-100", bm, sub["beds_islands"], M["mulch"])
        o["source"] = "LP-100 island curb ovals (V), 6 in curb per planting note 8"

    # ---- existing street trees to remain (context)
    for k, t in enumerate(D["existing_street_trees"]["items"]):
        bm = bmesh.new()
        z = grade(t["x"], t["y"])
        H, C, T = SZ["tree_existing"]["height_ft"], SZ["tree_existing"]["canopy_ft"], SZ["tree_existing"]["trunk_in"] / 12
        add_cylinder(bm, m(t["x"]), m(t["y"]), z, z + m(H * 0.4), m(T / 2))
        add_sphere(bm, m(t["x"]), m(t["y"]), z + m(H * 0.68), m(C / 2), m(C / 2), m(H * 0.32))
        o = new_object(f"CTX_existing_street_tree_{t['street']}_{k + 1:02d}_LP-100", bm, sub["context"], M["trunk"])
        o.data.materials.append(M["foliage_existing"])
        for f in o.data.polygons:
            f.material_index = 1 if (o.matrix_world @ o.data.vertices[f.vertices[0]].co).z > z + m(H * 0.4) + 1e-4 else 0
        o["source"] = "LP-100 existing tree symbol, 'to remain' (position V, size I from photos)"

    # ---- camera: landscape-focused view of the west entry beds and drop-off
    camcol = bpy.data.collections["90_Cameras"]
    add_camera("BI_cam_landscape_entry", (-48.0, 205.0, 26.0), (38.0, 100.0, 5.0), camcol, lens=32.0)

    h_after = geometry_hash(v003_names)
    assert h_before == h_after, "v003 geometry/material state changed - aborting"
    report.update({"geometry_unchanged": True, "placed": placed, "plants_shifted_out_of_footprint": len(shifted), "shifted": shifted,
                   "groundcover_patches": len(D["groundcover_patches"]) - len(skipped_patches), "groundcover_patches_skipped_on_hardscape": skipped_patches,
                   "parking_islands": len(islands),
                   "existing_street_trees": len(D["existing_street_trees"]["items"]),
                   "objects_per_collection": {c.name: len(c.objects) for c in col.children_recursive}})
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))

    if do_render:
        report["gpu"] = setup_gpu(scene)
        scene.cycles.samples = 64
        scene.cycles.use_denoising = True
        scene.render.image_settings.file_format = "PNG"
        scene.view_settings.view_transform = "Standard"
        o = bpy.data.objects
        views = {"front_north": ("BI_cam_front_north", (2400, 900)), "rear_south": ("BI_cam_rear_south", (2400, 900)),
                 "left_west": ("BI_cam_left_west", (2400, 900)), "right_east": ("BI_cam_right_east", (2400, 900)),
                 "oblique_northwest": ("BI_cam_oblique_northwest", (2000, 1400)), "site_elevated": ("BI_cam_site_elevated", (2000, 1400)),
                 "landscape_entry": ("BI_cam_landscape_entry", (2000, 1400))}
        times = {}
        for view, (cam, (rx, ry)) in views.items():
            scene.camera = o[cam]
            scene.render.resolution_x, scene.render.resolution_y = rx, ry
            path = render_dir / f"{STEM}_{view}.png"
            if path.exists():
                raise SystemExit(f"refusing to overwrite existing render: {path}")
            scene.render.filepath = str(path)
            ctx = o["CTX_Building_II_mass_from_BII_CS-101_rev6"]
            ctx.hide_render = (view == "left_west")
            t0 = time.time()
            bpy.ops.render.render(write_still=True)
            ctx.hide_render = False
            times[view] = round(time.time() - t0, 1)
        report["render_seconds"] = times
        scene.camera = o["BI_cam_landscape_entry"]
        bpy.ops.wm.save_mainfile()
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("BUILD_REPORT=" + json.dumps({k: v for k, v in report.items() if k != "shifted"}))


if __name__ == "__main__":
    main()
