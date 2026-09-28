"""Building I v011 - targeted entrance-facade correction (lobby tower west face above the porte cochere).

Cause (audit BI_entrance_facade_audit_v011.md): the v008 finish-region builder generated one PNL1 panel per exterior
zone face; on the lobby-tower west plane x 28.5 two zone faces coincide (the lobby band 54.2-74.38 x 0-40 and the
south-wing Level 2 prism 54.2-70.58 x 13.5-33.3), so FR_WEST_PNL1_W2b received two coplanar overlapping faces
(54.2-70.58 x 24.6-33.3 inside 54.2-74.38 x 24.6-40).  Cycles cannot offset a shading point away from a *different*
coplanar triangle, so every light path from the inner face is blocked by the outer one: a solid black patch, whatever
the material (verified with a white material override).  FR_WEST_GLZ_W2 (the curtain-wall backdrop below 24.6) carries
the same duplicates, and both objects also carry faces at x 70.97 (y 70.58-74.38) that lie inside the lobby band prism.

Correction: rebuild ONLY these two finish-region objects from their own faces:
  * drop every face whose rectangle lies inside another coplanar face of the same object (the duplicates);
  * drop the faces at x 70.97 between y 70.58 and 74.38 (buried inside BI_Z2_band_E_F2);
  * keep everything else exactly (vertex positions, offset 0.03 ft, material, collection).
Nothing else is touched: every other mesh object is hash-verified identical, material node trees identical.
The documented condition (A4.02 west elevation, A5.18 A2 / A5.24 A3, A1.01 / A1.02) is one continuous plane: CW1 to the
24.6 ft head, PNL1 above to the tower top (40 ft at x 30, R) - no opening, no recess in this face; the recess the eye
reads is the documented 17.8 ft step from the wing west face (x 10.67) to the tower face (x 28.5) at y 54.2 (v008 G-9).

Run:  blender --background --python scripts/Building_I/BI_build_entrance_facade_fix_v011.py [-- --no-render --samples N --views a,b --out DIR]
Outputs (refuses to overwrite): models/Building_I/BI_entrance_facade_v011.blend, renders/Building_I/BI_entrance_facade_v011_*.png
(including *_before_* renders of the same cameras taken from the untouched v010 scene), notes/Building_I/BI_entrance_facade_v011_build_report.json
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
BASE = ROOT / "models" / "Building_I" / "BI_entrance_site_v010.blend"
STEM = "BI_entrance_facade_v011"
FT = 0.3048
FFE = 661.75
TOUCH = ["FR_WEST_PNL1_W2b", "FR_WEST_GLZ_W2"]
BURIED_PLANE_X = 70.97          # faces on this plane between y 70.58 and 74.38 sit inside the lobby band prism
BURIED_Y = (70.58, 74.38)
CAMS = {   # validation cameras (added; every other camera untouched)
    "BI_cam_tower_closeup": {"loc": [-52.0, 122.0, 14.0], "target": [28.5, 64.0, 27.0], "lens": 55.0},
    "BI_cam_tower_side_depth": {"loc": [-30.0, 140.0, 24.0], "target": [22.0, 58.0, 20.0], "lens": 40.0},
    "BI_cam_tower_west_elevation_ortho": {"loc": [-42.0, 64.3, 20.0], "target": [28.5, 64.3, 20.0], "ortho": 60.0},   # in the plaza between the buildings (x -44.5 is the Building II east face)
}
VIEWS = {  # name: (camera, resolution)
    "1_entrance_eye_level": ("BI_cam_entrance_eye_level", (2000, 1400)),
    "2_tower_closeup": ("BI_cam_tower_closeup", (2000, 1400)),
    "3_tower_side_depth": ("BI_cam_tower_side_depth", (2000, 1400)),
    "4_tower_west_elevation_ortho": ("BI_cam_tower_west_elevation_ortho", (1600, 1600)),
    "5_v009_entrance_camera": ("BI_cam_entrance_oblique", (2000, 1400)),
}
BEFORE_VIEWS = ["1_entrance_eye_level", "2_tower_closeup", "4_tower_west_elevation_ortho"]


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / "Building_I" / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


v4 = _load("v4", "BI_build_landscape_v004.py")   # geometry_hash
m = v4.m
geometry_hash = v4.geometry_hash


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


def face_rects(o):
    """axis-aligned rectangles (plane axis, plane coord, u0,u1,v0,v1, area, normal sign) of every face, in ft"""
    me = o.data
    mw = o.matrix_world
    out = []
    for p in me.polygons:
        n = (mw.to_3x3() @ p.normal).normalized()
        ax = max(range(3), key=lambda i: abs(n[i]))
        pts = [mw @ me.vertices[i].co for i in p.vertices]
        c = sum(q[ax] for q in pts) / len(pts) / FT
        oth = [i for i in range(3) if i != ax]
        u = [q[oth[0]] / FT for q in pts]
        v = [q[oth[1]] / FT for q in pts]
        out.append({"index": p.index, "axis": ax, "plane": round(c, 3), "u0": min(u), "u1": max(u), "v0": min(v), "v1": max(v),
                    "area": p.area / FT / FT, "nsign": 1 if n[ax] > 0 else -1, "nz": abs(n[2])})
    return out


def inside(a, b, tol=0.02):
    return (a["axis"] == b["axis"] and abs(a["plane"] - b["plane"]) < 0.05 and a["u0"] >= b["u0"] - tol and a["u1"] <= b["u1"] + tol
            and a["v0"] >= b["v0"] - tol and a["v1"] <= b["v1"] + tol and a["area"] < b["area"] - 1e-6)


def overlaps(a, b):
    if a["axis"] != b["axis"] or abs(a["plane"] - b["plane"]) >= 0.05:
        return 0.0
    ou = min(a["u1"], b["u1"]) - max(a["u0"], b["u0"])
    ov = min(a["v1"], b["v1"]) - max(a["v0"], b["v0"])
    return ou * ov if ou > 0.01 and ov > 0.01 else 0.0


def union_area(rects):
    """exact area of the union of axis-aligned rectangles (sweep on a merged grid)"""
    xs = sorted({r[0] for r in rects} | {r[1] for r in rects})
    ys = sorted({r[2] for r in rects} | {r[3] for r in rects})
    total = 0.0
    for i in range(len(xs) - 1):
        for j in range(len(ys) - 1):
            cx, cy = (xs[i] + xs[i + 1]) / 2, (ys[j] + ys[j + 1]) / 2
            if any(r[0] <= cx <= r[1] and r[2] <= cy <= r[3] for r in rects):
                total += (xs[i + 1] - xs[i]) * (ys[j + 1] - ys[j])
    return total


def add_cam(name, loc, target, lens=35.0, ortho=None):
    cam = bpy.data.cameras.new(name)
    if ortho:
        cam.type = "ORTHO"
        cam.ortho_scale = m(ortho)
    else:
        cam.lens = lens
    cam.clip_end = 2000.0
    o = bpy.data.objects.new(name, cam)
    o.location = Vector([m(c) for c in loc])
    d = Vector([m(c) for c in target]) - o.location
    o.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    bpy.data.collections["90_Cameras"].objects.link(o)
    return o


def setup_gpu(scene, report):
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


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    do_render = "--no-render" not in argv
    out = Path(argv[argv.index("--out") + 1]).resolve() if "--out" in argv else None
    if out:
        out.mkdir(parents=True, exist_ok=True)
    model_dir = out or (ROOT / "models" / "Building_I")
    render_dir = out or (ROOT / "renders" / "Building_I")
    note_dir = out or (ROOT / "notes" / "Building_I")
    BLEND = model_dir / f"{STEM}.blend"
    REPORT = note_dir / f"{STEM}_build_report.json"
    for p in (BLEND, REPORT):
        if p.exists():
            raise SystemExit(f"refusing to overwrite existing file: {p}")
    samples = int(argv[argv.index("--samples") + 1]) if "--samples" in argv else 256
    only = argv[argv.index("--views") + 1].split(",") if "--views" in argv else None

    bpy.ops.wm.open_mainfile(filepath=str(BASE))
    scene = bpy.context.scene
    objs = bpy.data.objects
    mats_before = {mt.name: mat_sig(mt) for mt in bpy.data.materials}
    keep_names = [o.name for o in objs if o.type == "MESH" and o.name not in TOUCH]
    h_before = geometry_hash(keep_names)
    building_names = [n for n in keep_names if n.startswith(("BI_", "FR_")) and not n.startswith("BI_cam")]
    h_building = geometry_hash(building_names)
    cams_before = sorted(o.name for o in objs if o.type == "CAMERA")
    report = {"version": "v011", "base": str(BASE), "touched_objects": TOUCH, "kept_mesh_objects": len(keep_names), "geometry_hash_kept": h_before,
              "building_hash_excluding_touched": h_building, "objects": {}}

    # ---- cameras first (so the "before" renders use exactly the same views)
    for name, c in CAMS.items():
        assert name not in objs, name
        add_cam(name, c["loc"], c["target"], c.get("lens", 35.0), c.get("ortho"))
    times = {}
    if do_render:
        setup_gpu(scene, report)
        scene.cycles.samples = samples
        for view in BEFORE_VIEWS:
            if only and view not in only:
                continue
            cam, (rx, ry) = VIEWS[view]
            scene.camera = objs[cam]
            scene.render.resolution_x, scene.render.resolution_y = rx, ry
            path = render_dir / f"{STEM}_before_{view}.png"
            if path.exists():
                raise SystemExit(f"refusing to overwrite existing render: {path}")
            scene.render.filepath = str(path)
            t0 = time.time()
            bpy.ops.render.render(write_still=True)
            times[f"before_{view}"] = round(time.time() - t0, 1)

    # ---- the correction
    for name in TOUCH:
        o = objs[name]
        rects = face_rects(o)
        before = {"faces": len(rects), "area_sqft": round(sum(r["area"] for r in rects), 1),
                  "coplanar_overlap_pairs": sum(1 for i in range(len(rects)) for j in range(i + 1, len(rects)) if overlaps(rects[i], rects[j]) > 0.01)}
        drop = {}
        for a in rects:
            if a["axis"] == 0 and abs(a["plane"] - BURIED_PLANE_X) < 0.1 and a["u0"] >= BURIED_Y[0] - 0.05 and a["u1"] <= BURIED_Y[1] + 0.05:
                drop[a["index"]] = f"buried inside BI_Z2_band_E_F2 (plane x {a['plane']}, y {a['u0']:.2f}-{a['u1']:.2f}, z {a['v0']:.2f}-{a['v1']:.2f}, {a['area']:.1f} sq ft)"
        for a in rects:
            if a["index"] in drop:
                continue
            for b in rects:
                if b["index"] != a["index"] and b["index"] not in drop and inside(a, b):
                    drop[a["index"]] = f"duplicate inside face {b['index']} (plane x {a['plane']}, y {a['u0']:.2f}-{a['u1']:.2f}, z {a['v0']:.2f}-{a['v1']:.2f}, {a['area']:.1f} sq ft)"
                    break
        bm = bmesh.new()
        bm.from_mesh(o.data)
        bm.faces.ensure_lookup_table()
        bmesh.ops.delete(bm, geom=[bm.faces[i] for i in drop], context="FACES_ONLY")
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context="VERTS")
        bm.to_mesh(o.data)
        bm.free()
        o.data.update()
        after = face_rects(o)
        pairs = [(a["index"], b["index"], round(overlaps(a, b), 2)) for i, a in enumerate(after) for b in after[i + 1:] if overlaps(a, b) > 0.01]
        zero = [a["index"] for a in after if a["area"] < 1e-3]
        wrong_normal = [a["index"] for a in after if not (a["axis"] == 0 and a["nsign"] == -1)]
        on_plane = [a for a in after if a["axis"] == 0 and abs(a["plane"] - 28.47) < 0.05]
        cover = union_area([(a["u0"], a["u1"], a["v0"], a["v1"]) for a in on_plane])
        report["objects"][name] = {"before": before, "faces_dropped": {str(k): v for k, v in drop.items()},
                                   "after": {"faces": len(after), "area_sqft": round(sum(a["area"] for a in after), 1), "coplanar_overlap_pairs": pairs,
                                             "zero_area_faces": zero, "faces_not_facing_west": wrong_normal, "faces_on_plane_x28_47": len(on_plane),
                                             "union_coverage_on_x28_47_sqft": round(cover, 1)}}
        assert not pairs and not zero and not wrong_normal, name

    # ---- coverage check of the tower west face (x 28.5, y 54.2-74.38): W2b above 24.6, W2 below (minus the openings on that plane)
    w2b = report["objects"]["FR_WEST_PNL1_W2b"]["after"]["union_coverage_on_x28_47_sqft"]
    exp_w2b = (74.38 - 54.2) * (40.0 - 24.6)
    op = []
    for o in objs:
        if o.name.startswith("BI_open_WEST_") and o.type == "MESH":
            pts = [o.matrix_world @ Vector(c) for c in o.bound_box]
            x0, x1 = min(p.x for p in pts) / FT, max(p.x for p in pts) / FT
            if abs((x0 + x1) / 2 - 28.5) < 0.35:
                y0, y1 = min(p.y for p in pts) / FT, max(p.y for p in pts) / FT
                z0, z1 = min(p.z for p in pts) / FT, max(p.z for p in pts) / FT
                if y1 > 54.2 and y0 < 74.38 and z0 < 24.6:
                    op.append((max(y0, 54.2), min(y1, 74.38), max(z0, 0.0), min(z1, 24.6)))
    exp_w2 = (74.38 - 54.2) * 24.6 - union_area(op)
    w2 = report["objects"]["FR_WEST_GLZ_W2"]["after"]["union_coverage_on_x28_47_sqft"]
    report["coverage_check"] = {"W2b_union_sqft": w2b, "W2b_expected_band_face_above_24_6": round(exp_w2b, 1),
                                "W2_union_sqft": w2, "W2_expected_face_below_24_6_minus_openings": round(exp_w2, 1), "openings_on_plane": len(op)}
    assert abs(w2b - exp_w2b) < 0.5 and abs(w2 - exp_w2) < 1.0, report["coverage_check"]

    # ---- shell check around the tower: the lobby band prism is closed and outward
    band = objs["BI_Z2_band_E_F2"]
    bm = bmesh.new()
    bm.from_mesh(band.data)
    report["band_prism"] = {"faces": len(bm.faces), "manifold": all(e.is_manifold for e in bm.edges), "boundary_edges": sum(1 for e in bm.edges if e.is_boundary)}
    bm.free()

    # ---- verification
    h_after = geometry_hash(keep_names)
    assert h_before == h_after, "unrelated geometry changed - aborting"
    assert geometry_hash(building_names) == h_building
    assert {mt.name: mat_sig(mt) for mt in bpy.data.materials} == mats_before, "materials changed - aborting"
    report["unrelated_geometry_unchanged"] = True
    report["materials_unchanged"] = True
    report["cameras_added"] = sorted(set(o.name for o in objs if o.type == "CAMERA") - set(cams_before))
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))

    if do_render:
        for view, (cam, (rx, ry)) in VIEWS.items():
            if only and view not in only:
                continue
            scene.camera = objs[cam]
            scene.render.resolution_x, scene.render.resolution_y = rx, ry
            path = render_dir / f"{STEM}_{view}.png"
            if path.exists():
                raise SystemExit(f"refusing to overwrite existing render: {path}")
            scene.render.filepath = str(path)
            t0 = time.time()
            bpy.ops.render.render(write_still=True)
            times[view] = round(time.time() - t0, 1)
        report["render_seconds"] = times
        scene.camera = objs["BI_cam_entrance_oblique"]
        bpy.ops.wm.save_mainfile()
        assert geometry_hash(keep_names) == h_before
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("BUILD_REPORT=" + json.dumps(report))


if __name__ == "__main__":
    main()
