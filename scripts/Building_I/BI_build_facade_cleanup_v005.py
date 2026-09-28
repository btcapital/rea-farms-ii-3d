r"""Building I - facade cleanup v005.

Opens BI_landscape_v004.blend, verifies every non-overlay mesh object is unchanged (vertex + material hash over
shell, openings, site and landscape), removes the 1,580 raster-classified overlay boxes of 07_Facade_overlay_v002
(in the NEW file only), and builds clean finish regions (07_Facade_regions_v005) from BI_facade_regions_v005.json:
  * every exterior wall face of the shell prisms and parapet screens is covered by continuous regions,
  * regions are clipped to the real face polygon, v001 opening placeholders on the same plane are subtracted,
  * faces are single planes 0.03 ft proud of the wall (no boxes), one object per (facade, region).
Saves models/Building_I/BI_landscape_v005.blend and renders renders/Building_I/BI_facade_v005_*.png.

Run:  "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --background --python scripts/Building_I/BI_build_facade_cleanup_v005.py
Optional:  -- --no-render   |   -- --out <folder>
"""
import hashlib
import json
import sys
import time
from pathlib import Path

import bmesh
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parent.parent.parent
BASE = ROOT / "models" / "Building_I" / "BI_landscape_v004.blend"
DATA = ROOT / "notes" / "Building_I" / "BI_facade_regions_v005.json"
STEM = "BI_facade_v005"
FT = 0.3048


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
        h.update(",".join(str(p.material_index) for p in o.data.polygons).encode())
    return h.hexdigest()


# ---------- rectangle algebra (u,z) ----------
def rect_minus(r, cut):
    """r minus cut -> list of rects (both (u0,u1,z0,z1))."""
    u0, u1, z0, z1 = r
    c0, c1, d0, d1 = cut
    if c0 >= u1 or c1 <= u0 or d0 >= z1 or d1 <= z0:
        return [r]
    out = []
    if z0 < d0:
        out.append((u0, u1, z0, min(d0, z1)))
    if d1 < z1:
        out.append((u0, u1, max(d1, z0), z1))
    zl, zh = max(z0, d0), min(z1, d1)
    if u0 < c0:
        out.append((u0, min(c0, u1), zl, zh))
    if c1 < u1:
        out.append((max(c1, u0), u1, zl, zh))
    return [q for q in out if q[1] - q[0] > 1e-4 and q[3] - q[2] > 1e-4]


def rects_minus(rects, cut):
    out = []
    for r in rects:
        out += rect_minus(r, cut)
    return out


def clip_poly(poly, u0, u1, z0, z1):
    """Sutherland-Hodgman clip of polygon [(u,z)] to a rectangle."""
    def clip(pts, keep, inter):
        res = []
        for i in range(len(pts)):
            a, b = pts[i - 1], pts[i]
            ka, kb = keep(a), keep(b)
            if kb:
                if not ka:
                    res.append(inter(a, b))
                res.append(b)
            elif ka:
                res.append(inter(a, b))
        return res
    def x_int(c):
        return lambda a, b: (c, a[1] + (b[1] - a[1]) * (c - a[0]) / (b[0] - a[0]))
    def z_int(c):
        return lambda a, b: (a[0] + (b[0] - a[0]) * (c - a[1]) / (b[1] - a[1]), c)
    p = poly
    p = clip(p, lambda q: q[0] >= u0, x_int(u0)) if p else p
    p = clip(p, lambda q: q[0] <= u1, x_int(u1)) if p else p
    p = clip(p, lambda q: q[1] >= z0, z_int(z0)) if p else p
    p = clip(p, lambda q: q[1] <= z1, z_int(z1)) if p else p
    # drop degenerate
    if len(p) < 3:
        return []
    area = abs(sum(p[i - 1][0] * p[i][1] - p[i][0] * p[i - 1][1] for i in range(len(p)))) / 2
    return p if area > 0.05 else []


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
    BLEND = model_dir / "BI_landscape_v005.blend"
    REPORT = note_dir / f"{STEM}_build_report.json"
    for p in (BLEND, REPORT):
        if p.exists():
            raise SystemExit(f"refusing to overwrite existing file: {p}")

    bpy.ops.wm.open_mainfile(filepath=str(BASE))
    scene = bpy.context.scene
    D = json.loads(DATA.read_text(encoding="utf-8"))
    OFF = D["meta"]["offset_ft"]

    keep_names = [o.name for o in bpy.data.objects if o.type == "MESH" and not o.name.startswith("FD_")]
    h_before = geometry_hash(keep_names)
    fd = [o for o in bpy.data.objects if o.name.startswith("FD_")]
    n_removed = len(fd)
    fd_areas = {}
    for o in fd:
        mat = o.material_slots[0].material.name[:4] if o.material_slots else "-"
        fd_areas[mat] = fd_areas.get(mat, 0) + 1
    for o in fd:
        mesh = o.data
        bpy.data.objects.remove(o, do_unlink=True)
        if mesh.users == 0:
            bpy.data.meshes.remove(mesh)
    old = bpy.data.collections.get("07_Facade_overlay_v002")
    if old and len(old.objects) == 0:
        bpy.data.collections.remove(old)

    # ---- wall faces from the shell prisms and parapet screens
    faces = []  # dict: dir, plane, poly[(u,z)], obj, normal
    zone_objs = [o for c in D["face_collections"] for o in bpy.data.collections[c].objects if o.type == "MESH" and o.name not in D["skip_objects"]]
    for o in zone_objs:
        mw = o.matrix_world
        for p in o.data.polygons:
            n = (mw.to_3x3() @ p.normal).normalized()
            if abs(n.z) > 0.01:
                continue
            pts = [mw @ o.data.vertices[i].co for i in p.vertices]
            if abs(n.x) > 0.99:
                d = "EAST" if n.x > 0 else "WEST"
                plane = sum(q.x for q in pts) / len(pts) / FT
                poly = [(q.y / FT, q.z / FT) for q in pts]
            elif abs(n.y) > 0.99:
                d = "NORTH" if n.y > 0 else "SOUTH"
                plane = sum(q.y for q in pts) / len(pts) / FT
                poly = [(q.x / FT, q.z / FT) for q in pts]
            else:
                continue
            faces.append({"dir": d, "plane": plane, "poly": poly, "obj": o.name, "n": n})

    # skip faces buried inside another prism (offset point inside a closed mesh -> parity of upward ray hits)
    solids = [bpy.data.objects[nm] for nm in ("BI_Z1_south_wing", "BI_Z2_band_E_F2", "BI_Z4a_north_block", "BI_Z4b_north_block_south_part", "BI_Z5_end_block_13_14") if nm in bpy.data.objects]

    def buried(f):
        cx = sum(q[0] for q in f["poly"]) / len(f["poly"])
        cz = sum(q[1] for q in f["poly"]) / len(f["poly"])
        if f["dir"] in ("EAST", "WEST"):
            pt = Vector((m(f["plane"]), m(cx), m(cz))) + f["n"] * m(0.2)
        else:
            pt = Vector((m(cx), m(f["plane"]), m(cz))) + f["n"] * m(0.2)
        for s in solids:
            if s.name == f["obj"]:
                continue
            inv = s.matrix_world.inverted()
            origin = inv @ pt
            direction = (inv.to_3x3() @ Vector((0, 0, 1))).normalized()
            hits = 0
            o_ = origin.copy()
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

    # ---- openings by plane
    op = []
    for o in bpy.data.collections["04_Openings"].objects:
        bb = [o.matrix_world @ Vector(c) for c in o.bound_box]
        x0, x1 = min(q.x for q in bb) / FT, max(q.x for q in bb) / FT
        y0, y1 = min(q.y for q in bb) / FT, max(q.y for q in bb) / FT
        z0, z1 = min(q.z for q in bb) / FT, max(q.z for q in bb) / FT
        if (x1 - x0) < (y1 - y0):
            op.append({"axis": "x", "plane": (x0 + x1) / 2, "rect": (y0, y1, z0, z1)})
        else:
            op.append({"axis": "y", "plane": (y0 + y1) / 2, "rect": (x0, x1, z0, z1)})

    # ---- collections / materials
    col = bpy.data.collections.new("07_Facade_regions_v005")
    scene.collection.children.link(col)
    mats = {k: bpy.data.materials[v] for k, v in D["materials"].items()}

    # ---- build regions per face: painter's order -> per region, rects = region rect minus later regions minus openings
    regs = D["regions"]
    made = {}
    stats = {"faces": len(faces), "faces_by_dir": {}, "region_objects": 0, "polygons": 0, "openings_subtracted": 0, "area_by_mat_sqft": {}}
    for f in faces:
        stats["faces_by_dir"][f["dir"]] = stats["faces_by_dir"].get(f["dir"], 0) + 1
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
                rects = rects_minus(rects, (q["u0"], q["u1"], q["z0"], q["z1"]))
            axis = "x" if r["facade"] in ("EAST", "WEST") else "y"
            for oo in op:
                if oo["axis"] == axis and abs(oo["plane"] - f["plane"]) < 0.35:
                    before = len(rects)
                    rects = rects_minus(rects, oo["rect"])
                    if len(rects) != before or True:
                        stats["openings_subtracted"] += 1
            for (u0, u1, z0, z1) in rects:
                poly = clip_poly(f["poly"], u0, u1, z0, z1)
                if not poly:
                    continue
                verts = []
                for (u, z) in poly:
                    if axis == "x":
                        p3 = Vector((m(f["plane"]), m(u), m(z))) + f["n"] * m(OFF)
                    else:
                        p3 = Vector((m(u), m(f["plane"]), m(z))) + f["n"] * m(OFF)
                    verts.append(bm.verts.new(p3))
                try:
                    face = bm.faces.new(verts)
                except ValueError:
                    continue
                # orient outward
                if face.normal.dot(f["n"]) < 0:
                    face.normal_flip()
                area += abs(sum(poly[k - 1][0] * poly[k][1] - poly[k][0] * poly[k - 1][1] for k in range(len(poly)))) / 2
                stats["polygons"] += 1
        if len(bm.faces) == 0:
            bm.free()
            continue
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0005)
        mesh = bpy.data.meshes.new(f"FR_{r['facade']}_{r['mat']}_{r['id']}")
        bm.to_mesh(mesh)
        bm.free()
        obj = bpy.data.objects.new(mesh.name, mesh)
        obj.data.materials.append(mats[r["mat"]])
        obj["basis"] = r["basis"]
        obj["note"] = r["note"]
        obj["region_ft"] = json.dumps([r["u0"], r["u1"], r["z0"], r["z1"]])
        col.objects.link(obj)
        made[r["id"]] = round(area, 1)
        stats["region_objects"] += 1
        stats["area_by_mat_sqft"][r["mat"]] = round(stats["area_by_mat_sqft"].get(r["mat"], 0) + area, 1)

    # ---- cameras for the validation views
    camcol = bpy.data.collections["90_Cameras"]

    def add_cam(name, loc, target, lens=35.0, ortho=None):
        c = bpy.data.cameras.new(name)
        c.lens = lens
        c.clip_end = 3000
        if ortho:
            c.type = "ORTHO"
            c.ortho_scale = m(ortho)
        o = bpy.data.objects.new(name, c)
        o.location = Vector((m(loc[0]), m(loc[1]), m(loc[2])))
        d = Vector((m(target[0]), m(target[1]), m(target[2]))) - o.location
        o.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
        camcol.objects.link(o)
        return o
    add_cam("BI_cam_north_elevation_ortho", (147.0, 600.0, 22.0), (147.0, 100.0, 22.0), ortho=330.0)
    add_cam("BI_cam_entrance_closeup", (30.0, 175.0, 20.0), (52.0, 82.0, 14.0), lens=40.0)
    add_cam("BI_cam_oblique_northeast", (480.0, 420.0, 90.0), (150.0, 100.0, 15.0), lens=35.0)

    h_after = geometry_hash(keep_names)
    assert h_before == h_after, "non-overlay geometry changed - aborting"
    report = {"version": "v005", "base": str(BASE), "kept_mesh_objects": len(keep_names), "geometry_hash_kept": h_before, "geometry_unchanged": True,
              "overlay_objects_removed": n_removed, "removed_by_material": fd_areas, "wall_faces_used": stats, "regions_built": made,
              "region_count": stats["region_objects"], "offset_ft": OFF}
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))

    if do_render:
        try:
            prefs = bpy.context.preferences.addons["cycles"].preferences
            prefs.compute_device_type = "OPTIX"
            prefs.get_devices()
            for d_ in prefs.devices:
                d_.use = d_.type in ("OPTIX", "CPU")
            scene.cycles.device = "GPU"
            report["gpu"] = "OPTIX"
        except Exception as e:  # noqa
            report["gpu"] = f"CPU ({e})"
        scene.cycles.samples = 64
        scene.cycles.use_denoising = True
        scene.render.image_settings.file_format = "PNG"
        scene.view_settings.view_transform = "Standard"
        o = bpy.data.objects
        views = {"front_north_elevation": ("BI_cam_north_elevation_ortho", (3000, 1000)), "entrance_closeup": ("BI_cam_entrance_closeup", (2000, 1400)),
                 "oblique_northwest": ("BI_cam_oblique_northwest", (2000, 1400)), "oblique_northeast": ("BI_cam_oblique_northeast", (2000, 1400)),
                 "rear_south": ("BI_cam_rear_south", (2400, 900)), "site_elevated": ("BI_cam_site_elevated", (2000, 1400))}
        times = {}
        for view, (cam, (rx, ry)) in views.items():
            scene.camera = o[cam]
            scene.render.resolution_x, scene.render.resolution_y = rx, ry
            path = render_dir / f"{STEM}_{view}.png"
            if path.exists():
                raise SystemExit(f"refusing to overwrite existing render: {path}")
            scene.render.filepath = str(path)
            t0 = time.time()
            bpy.ops.render.render(write_still=True)
            times[view] = round(time.time() - t0, 1)
        report["render_seconds"] = times
        scene.camera = o["BI_cam_entrance_closeup"]
        bpy.ops.wm.save_mainfile()
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("BUILD_REPORT=" + json.dumps({k: v for k, v in report.items() if k != "regions_built"}))


if __name__ == "__main__":
    main()
