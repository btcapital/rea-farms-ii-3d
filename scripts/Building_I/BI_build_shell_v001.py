"""Rea Farms Building I (Sports Medicine Center) - geometry validation shell, v001.

Procedural build driven by notes/Building_I/BI_geometry_data_v001.json. Every number
is documented in notes/Building_I/BI_geometry_control_v001.md (source sheet and
confidence code W/V/R/I/A). Nothing is modeled by hand.

Run (from the project root):
  "C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe" --background --python scripts/Building_I/BI_build_shell_v001.py
Optional:  -- --no-render     build and save the .blend only
           -- --out <folder>  write every output into <folder> instead (trial runs)

Units: DATA values are decimal feet in the Building I coordinate system
  origin = grid 1 x grid A at Level 01 finish floor (FFE 661.75), +X east, +Y north, +Z up.
  Blender scene is metric at true scale (FT = 0.3048 m).
The script refuses to overwrite any existing output file. It never touches Building II files.
"""
from pathlib import Path
import json
import math
import sys
import time

import bpy
import bmesh
from mathutils import Vector

VERSION = "v001"
STEM = f"BI_shell_{VERSION}"
ROOT = Path(__file__).resolve().parent.parent.parent
DATA_FILE = ROOT / "notes" / "Building_I" / f"BI_geometry_data_{VERSION}.json"
BLEND = ROOT / "models" / "Building_I" / f"{STEM}.blend"
REPORT = ROOT / "notes" / "Building_I" / f"{STEM}_build_report.json"
RENDER_DIR = ROOT / "renders" / "Building_I"
FT = 0.3048


def m(ft):
    return ft * FT


# ------------------------------------------------------------------ 2D helpers
def clip_halfplane(poly, a, b, c):
    """Sutherland-Hodgman clip of polygon (list of (x,y)) to a*x + b*y <= c."""
    out = []
    n = len(poly)
    for i in range(n):
        p = poly[i]
        q = poly[(i + 1) % n]
        fp = a * p[0] + b * p[1] - c
        fq = a * q[0] + b * q[1] - c
        if fp <= 1e-9:
            out.append(p)
        if (fp < 0) != (fq < 0) and abs(fp - fq) > 1e-12:
            t = fp / (fp - fq)
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    # remove duplicate consecutive points
    res = []
    for p in out:
        if not res or abs(p[0] - res[-1][0]) > 1e-6 or abs(p[1] - res[-1][1]) > 1e-6:
            res.append(p)
    if len(res) > 1 and abs(res[0][0] - res[-1][0]) < 1e-6 and abs(res[0][1] - res[-1][1]) < 1e-6:
        res.pop()
    return res


def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def poly_area(poly):
    return 0.5 * sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1]
                     for i in range(len(poly)))


# ------------------------------------------------------------------ mesh helpers
def new_object(name, bm, col, mat):
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    obj.data.materials.append(mat)
    col.objects.link(obj)
    return obj


def prism(name, poly, z0, ztop, col, mat):
    """Extrude a (possibly concave) polygon in ft from z0 to ztop (number or f(x,y))."""
    if poly_area(poly) < 0:
        poly = poly[::-1]
    bm = bmesh.new()
    verts = [bm.verts.new((m(x), m(y), m(z0))) for x, y in poly]
    face = bm.faces.new(verts)
    bmesh.ops.triangulate(bm, faces=[face], ngon_method="EAR_CLIP")
    bm.faces.ensure_lookup_table()
    res = bmesh.ops.extrude_face_region(bm, geom=list(bm.faces))
    top = [g for g in res["geom"] if isinstance(g, bmesh.types.BMVert)]
    for v in top:
        x, y = v.co.x / FT, v.co.y / FT
        v.co.z = m(ztop(x, y) if callable(ztop) else ztop)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return new_object(name, bm, col, mat)


def box(name, x0, y0, z0, x1, y1, z1, col, mat):
    return prism(name, rect(x0, y0, x1, y1), z0, z1, col, mat)


def slab_strip(name, p0, p1, inward, thick, z0, z1a, z1b, col, mat):
    """Wall strip along edge p0->p1 (ft), 'inward' unit vector, top z1a at p0 and z1b at p1."""
    (x0, y0), (x1, y1) = p0, p1
    ix, iy = inward
    poly = [(x0, y0), (x1, y1), (x1 + ix * thick, y1 + iy * thick), (x0 + ix * thick, y0 + iy * thick)]

    def ztop(x, y):
        L = math.hypot(x1 - x0, y1 - y0)
        t = 0 if L == 0 else max(0.0, min(1.0, ((x - x0) * (x1 - x0) + (y - y0) * (y1 - y0)) / (L * L)))
        return z1a + t * (z1b - z1a)
    return prism(name, poly, z0, ztop, col, mat)


def profile_value(profile, x):
    xs = [p[0] for p in profile]
    if x <= xs[0]:
        return profile[0][1]
    for (xa, za), (xb, zb) in zip(profile, profile[1:]):
        if xa <= x <= xb:
            return za if xb == xa else za + (zb - za) * (x - xa) / (xb - xa)
    return profile[-1][1]


def clay(name, rgb):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.85
    return mat


def look_at(obj, target_ft):
    direction = Vector([m(c) for c in target_ft]) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def add_camera(name, loc_ft, target_ft, col, ortho_ft=None, lens=35.0):
    cam = bpy.data.cameras.new(name)
    cam.clip_start, cam.clip_end = 0.5, 3000.0
    if ortho_ft:
        cam.type = "ORTHO"
        cam.ortho_scale = m(ortho_ft)
    else:
        cam.lens = lens
    obj = bpy.data.objects.new(name, cam)
    obj.location = [m(c) for c in loc_ft]
    col.objects.link(obj)
    look_at(obj, target_ft)
    return obj


def setup_gpu(scene):
    scene.render.engine = "CYCLES"
    info = {"backend": "CPU", "devices": []}
    try:
        prefs = bpy.context.preferences.addons["cycles"].preferences
        for backend in ("OPTIX", "CUDA"):
            try:
                prefs.compute_device_type = backend
            except TypeError:
                continue
            prefs.refresh_devices()
            gpus = [d for d in prefs.devices if d.type == backend]
            if gpus:
                for d in prefs.devices:
                    d.use = d.type == backend
                scene.cycles.device = "GPU"
                info = {"backend": backend, "devices": [d.name for d in gpus]}
                break
    except Exception as exc:
        info["error"] = str(exc)
    return info


def bbox_ft(obj):
    pts = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    return ([round(min(p[i] for p in pts) / FT, 3) for i in range(3)],
            [round(max(p[i] for p in pts) / FT, 3) for i in range(3)])


# ------------------------------------------------------------------ opening placement
def face_coordinate(polys, facade, u):
    """Outermost boundary coordinate hit by a ray from the facade side at position u."""
    best = None
    for poly in polys:
        n = len(poly)
        for i in range(n):
            (xa, ya), (xb, yb) = poly[i], poly[(i + 1) % n]
            if facade in ("SOUTH", "NORTH"):
                if abs(ya - yb) < 1e-6 and min(xa, xb) - 1e-6 <= u <= max(xa, xb) + 1e-6:
                    v = ya
                    if best is None or (facade == "SOUTH" and v < best) or (facade == "NORTH" and v > best):
                        best = v
            else:
                if abs(xa - xb) < 1e-6 and min(ya, yb) - 1e-6 <= u <= max(ya, yb) + 1e-6:
                    v = xa
                    if best is None or (facade == "WEST" and v < best) or (facade == "EAST" and v > best):
                        best = v
    return best


# ------------------------------------------------------------------ main
def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    do_render = "--no-render" not in argv
    global BLEND, REPORT, RENDER_DIR
    if "--out" in argv:
        out = Path(argv[argv.index("--out") + 1]).resolve()
        BLEND, REPORT, RENDER_DIR = out / BLEND.name, out / REPORT.name, out
    for target in (BLEND, REPORT):
        if target.exists():
            raise SystemExit(f"refusing to overwrite existing file: {target}")
    BLEND.parent.mkdir(parents=True, exist_ok=True)
    RENDER_DIR.mkdir(parents=True, exist_ok=True)
    D = json.loads(DATA_FILE.read_text(encoding="utf-8"))

    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "IMPERIAL"
    scene.unit_settings.length_unit = "FEET"
    scene.unit_settings.scale_length = 1.0

    root = bpy.data.collections.new(f"Building_I_{VERSION}")
    scene.collection.children.link(root)
    cols = {}
    for name in ("01_Shell", "02_Parapet_screens", "03_Canopy", "04_Openings", "05_Grid_control", "06_Reference", "90_Cameras"):
        c = bpy.data.collections.new(name)
        root.children.link(c)
        cols[name] = c

    mat_clay = clay("BI_clay", (0.78, 0.76, 0.72))
    mat_screen = clay("BI_clay_screen", (0.70, 0.68, 0.64))
    mat_glass = clay("BI_glass_placeholder", (0.25, 0.30, 0.34))
    mat_canopy = clay("BI_canopy_glass", (0.45, 0.55, 0.60))
    mat_steel = clay("BI_steel", (0.35, 0.35, 0.36))
    mat_grid = clay("BI_grid", (0.75, 0.15, 0.10))
    mat_ground = clay("BI_ground", (0.55, 0.55, 0.53))
    mat_slab = clay("BI_slab", (0.62, 0.60, 0.58))

    fp = [tuple(p) for p in D["footprint_union"]]
    W = D["wing"]
    split = W["split_y"]
    se = D["se_block_13_14"]
    band = D["band_E_F2"]
    ves = D["vestibule_100"]

    # ---- zone polygons (2D, ft)
    wing_poly = clip_halfplane(clip_halfplane(fp, 0, 1, split), 1, 0, se["x0"])
    north_a = clip_halfplane(fp, 0, -1, -se["y1"])                     # y >= 97.75
    north_b = clip_halfplane(clip_halfplane(clip_halfplane(fp, 0, -1, -split), 0, 1, se["y1"]), 1, 0, se["x0"])
    band_poly = rect(band["x0"], band["y0"], band["x1"], band["y1"])
    ves_poly = rect(ves["x0"], ves["y0"], ves["x1"], ves["y1"])
    se_poly = rect(se["x0"], se["y0"], se["x1"], se["y1"])

    def north_top(x, y):
        return 33.15 + (y - 80.5) * 0.0535

    def band_top(x, y):
        t = max(0.0, min(1.0, (x - 30.0) / (band["x1"] - 30.0)))
        return band["top_at_x30"] + t * (band["top_at_x71"] - band["top_at_x30"])

    shell = cols["01_Shell"]
    objs = {}
    objs["Z1_south_wing"] = prism("BI_Z1_south_wing", wing_poly, 0.0, W["parapet_top"], shell, mat_clay)
    objs["Z2_band_E_F2"] = prism("BI_Z2_band_E_F2", band_poly, 0.0, band_top, shell, mat_clay)
    objs["Z3_vestibule_100"] = prism("BI_Z3_vestibule_100", ves_poly, 0.0, ves["top"], shell, mat_clay)
    objs["Z4a_north_block"] = prism("BI_Z4a_north_block", north_a, 0.0, north_top, shell, mat_clay)
    objs["Z4b_north_block_south_part"] = prism("BI_Z4b_north_block_south_part", north_b, 0.0, north_top, shell, mat_clay)
    objs["Z5_end_block_13_14"] = prism("BI_Z5_end_block_13_14", se_poly, 0.0, se["top"], shell, mat_clay)
    ms = D["mech_screen"]
    objs["Z6_mech_screen"] = box("BI_Z6_mech_screen", ms["x0"], ms["y0"], ms["z0"], ms["x1"], ms["y1"], ms["z1"], shell, mat_screen)
    l2 = D["level2_slab"]
    objs["L2_floor_slab"] = prism("BI_L2_floor_slab", wing_poly, l2["z_top"] - l2["thickness"], l2["z_top"], cols["06_Reference"], mat_slab)

    # ---- parapet screen strips on the south wing faces (R profiles)
    sc = cols["02_Parapet_screens"]
    t = W["screen_thickness"]
    n_strip = 0
    for i in range(len(wing_poly)):
        (xa, ya), (xb, yb) = wing_poly[i], wing_poly[(i + 1) % len(wing_poly)]
        if abs(ya - yb) < 1e-6 and ya < 0.0:                       # south face edges
            lo, hi = sorted((xa, xb))
            prof = W["south_screen_profile"]
            lo2, hi2 = max(lo, prof[0][0]), min(hi, prof[-1][0])
            if hi2 - lo2 > 0.5:
                xs = [lo2] + [p[0] for p in prof if lo2 < p[0] < hi2] + [hi2]
                for x0, x1 in zip(xs, xs[1:]):
                    if x1 - x0 < 0.05:
                        continue
                    n_strip += 1
                    slab_strip(f"BI_screen_south_{n_strip:02d}", (x0, ya), (x1, ya), (0, 1), t, W["parapet_top"],
                               profile_value(prof, x0), profile_value(prof, x1), sc, mat_screen)
        elif abs(xa - xb) < 1e-6 and xa > se["x0"] - 0.01:          # east face of the wing
            lo, hi = sorted((ya, yb))
            e = W["east_screen"]
            lo2, hi2 = max(lo, e["y0"]), min(hi, e["y1"])
            if hi2 - lo2 > 0.5:
                n_strip += 1
                slab_strip(f"BI_screen_east_{n_strip:02d}", (xa, lo2), (xa, hi2), (-1, 0), t, W["parapet_top"], e["top"], e["top"], sc, mat_screen)
        elif abs(xa - xb) < 1e-6 and xa < 7.0:                        # west face of the wing
            lo, hi = sorted((ya, yb))
            w = W["west_screen"]
            lo2, hi2 = max(lo, w["y0"]), min(hi, w["y1"])
            if hi2 - lo2 > 0.5:
                n_strip += 1
                slab_strip(f"BI_screen_west_{n_strip:02d}", (xa, lo2), (xa, hi2), (1, 0), t, W["parapet_top"], w["top"], w["top"], sc, mat_screen)

    # ---- entry canopy (A1.13)
    cp = D["canopy"]
    cc = cols["03_Canopy"]
    gz = cp["gutter_z"]
    yc = cp["column_y"]
    for k, cx in enumerate(cp["column_x"]):
        s = cp["column_size"] / 2
        box(f"BI_canopy_column_{k+1:02d}", cx - s, yc - s, 0.0, cx + s, yc + s, cp["column_top"], cc, mat_steel)
    box("BI_canopy_gutter_beam", cp["x0"], yc - 0.5, gz - 1.0, cp["x1"], yc + 0.5, gz, cc, mat_steel)
    for name, y1, sign in (("north", yc + cp["wing_north_len"], 1), ("south", yc - cp["wing_south_len"], -1)):
        rise = abs(y1 - yc) * cp["slope"]
        bm = bmesh.new()
        pts = [(cp["x0"], yc, gz), (cp["x1"], yc, gz), (cp["x1"], y1, gz + rise), (cp["x0"], y1, gz + rise)]
        vs = [bm.verts.new((m(x), m(y), m(z))) for x, y, z in pts]
        bm.faces.new(vs)
        res = bmesh.ops.extrude_face_region(bm, geom=list(bm.faces))
        for v in [g for g in res["geom"] if isinstance(g, bmesh.types.BMVert)]:
            v.co.z += m(cp["glass_t"])
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        new_object(f"BI_canopy_glass_{name}", bm, cc, mat_canopy)

    # ---- openings: flush placeholder panels
    zone_polys = [wing_poly, north_a, north_b, band_poly, ves_poly, se_poly]
    oc = cols["04_Openings"]
    placed, skipped = 0, 0
    panel_mesh = None
    for facade, boxes in D["openings"].items():
        for j, (u0, u1, z0, z1) in enumerate(boxes):
            uc = (u0 + u1) / 2
            face = face_coordinate(zone_polys, facade, uc)
            if face is None:
                skipped += 1
                continue
            w, h = u1 - u0, z1 - z0
            d = 0.15
            if facade == "SOUTH":
                b = box(f"BI_open_{facade}_{j+1:03d}", u0, face - 0.05, z0, u1, face - 0.05 + d, z1, oc, mat_glass)
            elif facade == "NORTH":
                b = box(f"BI_open_{facade}_{j+1:03d}", u0, face + 0.05 - d, z0, u1, face + 0.05, z1, oc, mat_glass)
            elif facade == "EAST":
                b = box(f"BI_open_{facade}_{j+1:03d}", face + 0.05 - d, u0, z0, face + 0.05, u1, z1, oc, mat_glass)
            else:
                b = box(f"BI_open_{facade}_{j+1:03d}", face - 0.05, u0, z0, face - 0.05 + d, u1, z1, oc, mat_glass)
            placed += 1

    # ---- grid control lines and reference planes
    gc = cols["05_Grid_control"]
    gx, gy = D["grid_x"], D["grid_y"]
    ymin, ymax = min(gy.values()) - 15, max(gy.values()) + 15
    xmin, xmax = min(gx.values()) - 15, max(gx.values()) + 15
    for g, x in gx.items():
        box(f"BI_grid_{g}", x - 0.08, ymin, 0.02, x + 0.08, ymax, 0.12, gc, mat_grid)
    for g, y in gy.items():
        box(f"BI_grid_{g}", xmin, y - 0.08, 0.02, xmax, y + 0.08, 0.12, gc, mat_grid)
    gp = D["grade_plane_z"]
    box("BI_grade_plane_660", -80, -80, gp - 0.2, 360, 280, gp, cols["06_Reference"], mat_ground)

    # ---- lighting (neutral validation)
    sun = bpy.data.lights.new("BI_sun", "SUN")
    sun.energy = 3.0
    sun.angle = math.radians(3)
    sun_obj = bpy.data.objects.new("BI_sun", sun)
    sun_obj.rotation_euler = (math.radians(50), 0, math.radians(-35))
    cols["90_Cameras"].objects.link(sun_obj)
    world = bpy.data.worlds.new("BI_world")
    scene.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.75, 0.78, 0.82, 1.0)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.9

    # ---- cameras: front = north face
    cx, cy = 140.0, 100.0
    cams = {
        "front_north": (add_camera("BI_cam_front_north", (cx, 900.0, 60.0), (cx, cy, 15.0), cols["90_Cameras"], ortho_ft=340.0), (2400, 900)),
        "rear_south": (add_camera("BI_cam_rear_south", (cx, -800.0, 60.0), (cx, cy, 15.0), cols["90_Cameras"], ortho_ft=340.0), (2400, 900)),
        "left_west": (add_camera("BI_cam_left_west", (-800.0, cy, 60.0), (cx, cy, 15.0), cols["90_Cameras"], ortho_ft=260.0), (2400, 900)),
        "right_east": (add_camera("BI_cam_right_east", (1000.0, cy, 60.0), (cx, cy, 15.0), cols["90_Cameras"], ortho_ft=260.0), (2400, 900)),
        "oblique_northwest": (add_camera("BI_cam_oblique_northwest", (-260.0, 420.0, 190.0), (cx, cy, 10.0), cols["90_Cameras"], lens=32.0), (2000, 1400)),
    }
    scene.camera = cams["oblique_northwest"][0]

    # ---- report / assertions
    lo, hi = [1e9] * 3, [-1e9] * 3
    for o in shell.objects:
        a, b = bbox_ft(o)
        lo = [min(lo[i], a[i]) for i in range(3)]
        hi = [max(hi[i], b[i]) for i in range(3)]
    report = {
        "version": VERSION, "data_file": str(DATA_FILE), "blend": str(BLEND),
        "shell_extent_ft": {"min": lo, "max": hi, "size": [round(hi[i] - lo[i], 3) for i in range(3)]},
        "expected_ft": {"x_union": 280.12, "y_union": 207.25, "max_top": 40.1},
        "objects_per_collection": {c.name: len(c.objects) for c in root.children_recursive},
        "zone_bboxes_ft": {k: bbox_ft(v) for k, v in objs.items()},
        "openings_placed": placed, "openings_skipped": skipped, "screen_strips": n_strip,
        "wing_polygon_vertices": len(wing_poly), "north_polygon_vertices": [len(north_a), len(north_b)],
    }
    assert abs((hi[0] - lo[0]) - 280.12) < 0.05, "overall X extent check failed"
    assert abs((hi[1] - lo[1]) - 207.25) < 0.05, "overall Y extent check failed"
    assert abs(hi[2] - 40.1) < 0.05, "highest element check failed (mechanical screen 40.1)"

    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))

    if do_render:
        report["gpu"] = setup_gpu(scene)
        scene.cycles.samples = 48
        scene.cycles.use_denoising = True
        scene.render.image_settings.file_format = "PNG"
        scene.view_settings.view_transform = "Standard"
        times = {}
        for view, (cam, (rx, ry)) in cams.items():
            scene.camera = cam
            scene.render.resolution_x, scene.render.resolution_y = rx, ry
            path = RENDER_DIR / f"{STEM}_{view}.png"
            if path.exists():
                raise SystemExit(f"refusing to overwrite existing render: {path}")
            scene.render.filepath = str(path)
            t0 = time.time()
            bpy.ops.render.render(write_still=True)
            times[view] = round(time.time() - t0, 1)
        report["render_seconds"] = times
        scene.camera = cams["oblique_northwest"][0]
        bpy.ops.wm.save_mainfile()

    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("BUILD_REPORT=" + json.dumps(report))


if __name__ == "__main__":
    main()
