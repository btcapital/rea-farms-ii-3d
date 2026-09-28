r"""Building I - entrance geometry correction v006.

Opens the approved BI_landscape_v005.blend and applies exactly two corrections (see BI_entrance_geometry_control_v006.md):
  A. the 12 curtain-wall placeholders BI_open_NORTH_* floating on the vestibule plane (y 83.58) above the 9-ft vestibule
     are translated -9.20 ft to the E-F.2 band face (y 74.38), the curtain-wall plane per A5.18 A2 / A1.02 / A7.26;
  B. the cap faces of BI_Z4b_north_block_south_part are re-tessellated (ear clip) so no face bridges the entrance notch
     (the false overhang); vertices unchanged.
Then the v005 finish regions are regenerated with the unchanged BI_facade_regions_v005.json so the moved glazing is
subtracted from the band-face regions. Everything else is hashed before/after and must be identical.
Saves models/Building_I/BI_landscape_v006.blend and renders renders/Building_I/BI_entrance_v006_*.png.

Run:  "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --background --python scripts/Building_I/BI_build_entrance_fix_v006.py
Optional:  -- --no-render   |   -- --out <folder>
"""
import hashlib
import importlib.util
import json
import sys
import time
from pathlib import Path

import bmesh
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parent.parent.parent
BASE = ROOT / "models" / "Building_I" / "BI_landscape_v005.blend"
REGIONS = ROOT / "notes" / "Building_I" / "BI_facade_regions_v005.json"
STEM = "BI_entrance_v006"
FT = 0.3048
DY_FT = -9.20          # 83.58 -> 74.38
SRC_PLANE, DST_PLANE = 83.58, 74.38

spec = importlib.util.spec_from_file_location("v5", ROOT / "scripts" / "Building_I" / "BI_build_facade_cleanup_v005.py")
v5 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v5)      # helper functions only; its main() is not called
m, rects_minus, clip_poly = v5.m, v5.rects_minus, v5.clip_poly


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


def bbox_ft(o):
    bb = [o.matrix_world @ Vector(c) for c in o.bound_box]
    return [min(q.x for q in bb) / FT, min(q.y for q in bb) / FT, min(q.z for q in bb) / FT, max(q.x for q in bb) / FT, max(q.y for q in bb) / FT, max(q.z for q in bb) / FT]


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


def ear_clip(pts):
    """Triangulate a simple 2-D polygon (list of (x,y)); returns index triples. Works for concave outlines."""
    n = len(pts)
    idx = list(range(n))
    area = sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n))
    if area < 0:
        idx.reverse()
    def cross(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    def inside_tri(p, a, b, c):
        return cross(a, b, p) >= -1e-9 and cross(b, c, p) >= -1e-9 and cross(c, a, p) >= -1e-9
    tris = []
    guard = 0
    while len(idx) > 3 and guard < 10000:
        guard += 1
        found = False
        for k in range(len(idx)):
            i0, i1, i2 = idx[k - 1], idx[k], idx[(k + 1) % len(idx)]
            a, b, c = pts[i0], pts[i1], pts[i2]
            if cross(a, b, c) <= 1e-9:
                continue
            if any(inside_tri(pts[j], a, b, c) for j in idx if j not in (i0, i1, i2)):
                continue
            tris.append((i0, i1, i2))
            idx.pop(k)
            found = True
            break
        if not found:
            raise RuntimeError("ear clipping failed (polygon not simple?)")
    tris.append(tuple(idx))
    return tris


def retessellate_caps(o):
    """Clean BI_Z4b_north_block_south_part.
    The v001 Level-2 trace gave this prism a self-overlapping outline west of x = 71: a 0.5-ft 'U' sliver hugging the
    E-F.2 band (inside BI_Z2_band_E_F2) whose north face at y = 74.5 stands 0.12 ft proud of the band wall over the
    curtain wall, and whose cap tessellation bridged the entrance notch (the false overhang).
    Correction: delete the sliver faces (all vertices at x <= 71.01, y <= 74.51, except the long south face), close the
    prism's west side on its existing vertices (71,70.58)-(71,74.5), rebuild the caps as the simple rectangle
    (71,70.58)-(271.38,70.58)-(271.38,97.75)-(71,97.75), and remove the vertices left unused. No vertex is moved and
    no new vertex is created."""
    me = o.data
    bm = bmesh.new()
    bm.from_mesh(me)
    bm.verts.ensure_lookup_table()
    zmin = min(v.co.z for v in bm.verts)
    caps = [f for f in bm.faces if abs(f.normal.z) > 0.5]
    n_caps_before = len(caps)
    sliver = [f for f in bm.faces if abs(f.normal.z) <= 0.5 and all(v.co.x / FT <= 71.01 and v.co.y / FT <= 74.51 for v in f.verts)]
    n_sliver = len(sliver)
    bmesh.ops.delete(bm, geom=caps + sliver, context="FACES_ONLY")

    def vert_at(x, y, top):
        cands = [v for v in bm.verts if (v.co.z > zmin + 0.01) == top]
        best = min(cands, key=lambda v: (v.co.x / FT - x) ** 2 + (v.co.y / FT - y) ** 2)
        if (best.co.x / FT - x) ** 2 + (best.co.y / FT - y) ** 2 > 0.05 ** 2:
            raise RuntimeError(f"vertex {(x, y)} not found")
        return best
    RECT = [(71.0, 70.58), (271.38, 70.58), (271.38, 97.75), (71.0, 97.75)]
    top = [vert_at(x, y, True) for x, y in RECT]
    bot = [vert_at(x, y, False) for x, y in RECT]
    bm.faces.new(top)
    bm.faces.new(list(reversed(bot)))
    # west closure between the existing west face (71,74.5)-(71,97.75) and the south-west corner (71,70.58)
    w0b, w0t = vert_at(71.0, 70.58, False), vert_at(71.0, 70.58, True)
    w1b, w1t = vert_at(71.0, 74.5, False), vert_at(71.0, 74.5, True)
    bm.faces.new([w0b, w1b, w1t, w0t])
    loose = [v for v in bm.verts if not v.link_faces]
    n_loose = len(loose)
    bmesh.ops.delete(bm, geom=loose, context="VERTS")
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()
    me.update()
    return n_caps_before, n_sliver, n_loose


def notch_triangles(o):
    me = o.data
    me.calc_loop_triangles()
    bad = 0
    for t in me.loop_triangles:
        vs = [o.matrix_world @ me.vertices[i].co for i in t.vertices]
        cx = sum(v.x for v in vs) / 3 / FT
        cy = sum(v.y for v in vs) / 3 / FT
        if 30 < cx < 71 and 74.6 < cy < 97.7:
            bad += 1
    return bad


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
    BLEND = model_dir / "BI_landscape_v006.blend"
    REPORT = note_dir / f"{STEM}_build_report.json"
    for p in (BLEND, REPORT):
        if p.exists():
            raise SystemExit(f"refusing to overwrite existing file: {p}")

    bpy.ops.wm.open_mainfile(filepath=str(BASE))
    scene = bpy.context.scene
    D = json.loads(REGIONS.read_text(encoding="utf-8"))
    OFF = D["meta"]["offset_ft"]

    # ---- A. floating placeholders
    moved = []
    for o in bpy.data.collections["04_Openings"].objects:
        b = bbox_ft(o)
        if abs((b[1] + b[4]) / 2 - SRC_PLANE) < 0.3 and b[2] >= 9.0:
            moved.append(o)
    assert len(moved) == 12, f"expected 12 floating placeholders, found {len(moved)}"
    z4b = bpy.data.objects["BI_Z4b_north_block_south_part"]
    fr_names = [o.name for o in bpy.data.objects if o.name.startswith("FR_")]
    keep_names = [o.name for o in bpy.data.objects if o.type == "MESH" and o.name not in {q.name for q in moved} and o.name != z4b.name and o.name not in fr_names]
    h_before = geometry_hash(keep_names)
    z4b_verts_before = sorted((round(v.co.x, 5), round(v.co.y, 5), round(v.co.z, 5)) for v in z4b.data.vertices)
    notch_before = notch_triangles(z4b)
    rec_moved = []
    for o in moved:
        before = bbox_ft(o)
        o.location.y += m(DY_FT)
        after = bbox_ft(o)
        rec_moved.append({"object": o.name, "x_ft": [round(before[0], 2), round(before[3], 2)], "z_ft": [round(before[2], 2), round(before[5], 2)],
                          "plane_before_ft": round((before[1] + before[4]) / 2, 2), "plane_after_ft": round((after[1] + after[4]) / 2, 2), "shift_ft": DY_FT})

    # ---- B. false overhang: re-tessellate Z4b caps
    caps_before, sliver_faces, loose_removed = retessellate_caps(z4b)
    z4b_verts_after = sorted((round(v.co.x, 5), round(v.co.y, 5), round(v.co.z, 5)) for v in z4b.data.vertices)
    assert set(z4b_verts_after) <= set(z4b_verts_before), "Z4b gained or moved vertices"
    z4b_removed_verts = sorted(set(z4b_verts_before) - set(z4b_verts_after))
    notch_after = notch_triangles(z4b)
    assert notch_after == 0, f"notch triangles remain: {notch_after}"

    # ---- C. regenerate finish regions (same data, same algorithm as v005)
    old_fr = [bpy.data.objects[n] for n in fr_names]
    old_hashes = {}
    for o in old_fr:
        h = hashlib.sha256()
        for v in o.data.vertices:
            w = o.matrix_world @ v.co
            h.update(f"{w.x:.4f},{w.y:.4f},{w.z:.4f};".encode())
        old_hashes[o.name] = h.hexdigest()
    for o in old_fr:
        me = o.data
        bpy.data.objects.remove(o, do_unlink=True)
        if me.users == 0:
            bpy.data.meshes.remove(me)
    col = bpy.data.collections["07_Facade_regions_v005"]
    faces = []
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
                faces.append({"dir": d, "plane": sum(q.x for q in pts) / len(pts) / FT, "poly": [(q.y / FT, q.z / FT) for q in pts], "obj": o.name, "n": n})
            elif abs(n.y) > 0.99:
                d = "NORTH" if n.y > 0 else "SOUTH"
                faces.append({"dir": d, "plane": sum(q.y for q in pts) / len(pts) / FT, "poly": [(q.x / FT, q.z / FT) for q in pts], "obj": o.name, "n": n})
    solids = [bpy.data.objects[nm] for nm in ("BI_Z1_south_wing", "BI_Z2_band_E_F2", "BI_Z4a_north_block", "BI_Z4b_north_block_south_part", "BI_Z5_end_block_13_14")]

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
    op = []
    for o in bpy.data.collections["04_Openings"].objects:
        b = bbox_ft(o)
        if (b[3] - b[0]) < (b[4] - b[1]):
            op.append({"axis": "x", "plane": (b[0] + b[3]) / 2, "rect": (b[1], b[4], b[2], b[5])})
        else:
            op.append({"axis": "y", "plane": (b[1] + b[4]) / 2, "rect": (b[0], b[3], b[2], b[5])})
    mats = {k: bpy.data.materials[v] for k, v in D["materials"].items()}
    regs = D["regions"]
    new_hashes = {}
    for i, r in enumerate(regs):
        later = [q for q in regs[i + 1:] if q["facade"] == r["facade"]]
        bm = bmesh.new()
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
                    rects = rects_minus(rects, oo["rect"])
            for (u0, u1, z0, z1) in rects:
                poly = clip_poly(f["poly"], u0, u1, z0, z1)
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
        new_hashes[name] = h.hexdigest()
    fr_changed = sorted(n for n in new_hashes if old_hashes.get(n) != new_hashes[n])
    fr_missing = sorted(n for n in old_hashes if n not in new_hashes)

    # ---- validation cameras
    camcol = bpy.data.collections["90_Cameras"]

    def add_cam(name, loc, target, lens=35.0, ortho=None):
        c = bpy.data.cameras.new(name); c.lens = lens; c.clip_end = 3000
        if ortho:
            c.type = "ORTHO"; c.ortho_scale = m(ortho)
        o = bpy.data.objects.new(name, c)
        o.location = Vector((m(loc[0]), m(loc[1]), m(loc[2])))
        d = Vector((m(target[0]), m(target[1]), m(target[2]))) - o.location
        o.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
        camcol.objects.link(o)
        return o
    add_cam("BI_cam_entrance_elevation_ortho", (52.0, 320.0, 16.0), (52.0, 80.0, 16.0), ortho=110.0)
    add_cam("BI_cam_entrance_oblique", (-40.0, 165.0, 24.0), (50.0, 82.0, 12.0), lens=35.0)
    add_cam("BI_cam_entrance_side_depth", (-30.0, 104.0, 17.0), (50.0, 80.0, 14.0), lens=32.0)

    h_after = geometry_hash(keep_names)
    assert h_before == h_after, "unrelated geometry changed - aborting"
    report = {"version": "v006", "base": str(BASE), "kept_mesh_objects": len(keep_names), "geometry_hash_kept": h_before, "unrelated_geometry_unchanged": True,
              "A_placeholders_moved": rec_moved, "A_count": len(rec_moved), "A_shift_ft": DY_FT,
              "B_z4b": {"cap_faces_before": caps_before, "sliver_faces_removed": sliver_faces, "unused_vertices_removed": loose_removed,
                        "removed_vertices_ft": [[round(v[0] / FT, 2), round(v[1] / FT, 2), round(v[2] / FT, 2)] for v in z4b_removed_verts],
                        "notch_triangles_before": notch_before, "notch_triangles_after": notch_after, "vertices_moved_or_added": 0,
                        "vertex_count_before": len(z4b_verts_before), "vertex_count_after": len(z4b_verts_after)},
              "C_facade_regions": {"regenerated": len(new_hashes), "changed": fr_changed, "removed": fr_missing},
              "canopy_changed": False, "cameras_added": ["BI_cam_entrance_elevation_ortho", "BI_cam_entrance_oblique", "BI_cam_entrance_side_depth"]}
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
        o = bpy.data.objects
        views = {"entrance_closeup": ("BI_cam_entrance_closeup", (2000, 1400)), "entrance_elevation_ortho": ("BI_cam_entrance_elevation_ortho", (2000, 1400)),
                 "entrance_oblique": ("BI_cam_entrance_oblique", (2000, 1400)), "entrance_side_depth": ("BI_cam_entrance_side_depth", (2000, 1400)),
                 "front_north_elevation": ("BI_cam_north_elevation_ortho", (3000, 1000))}
        times = {}
        for view, (cam, (rx, ry)) in views.items():
            scene.camera = o[cam]
            scene.render.resolution_x, scene.render.resolution_y = rx, ry
            path = render_dir / f"{STEM}_{view}.png"
            if path.exists():
                raise SystemExit(f"refusing to overwrite existing render: {path}")
            scene.render.filepath = str(path)
            t0 = time.time(); bpy.ops.render.render(write_still=True); times[view] = round(time.time() - t0, 1)
        report["render_seconds"] = times
        scene.camera = o["BI_cam_entrance_closeup"]
        bpy.ops.wm.save_mainfile()
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("BUILD_REPORT=" + json.dumps({k: v for k, v in report.items() if k != "A_placeholders_moved"}))


if __name__ == "__main__":
    main()
