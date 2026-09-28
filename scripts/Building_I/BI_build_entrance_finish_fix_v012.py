"""Building I v012 - targeted facade-FINISH correction on the lobby-tower north face (above the porte cochere).

Finding (audit BI_entrance_finish_audit_v012.md): the v005 region N1 (BRK1) was extended over the lobby-band north face
y 74.38 from the tower's west corner (x 28.5) to grid 3.7 (x 40), full height.  A4.02 North Elevation (Rev 14) shows the
tower's north face as one element from x 28.5 to x 71: CW1 curtain wall from grade to its head (24.6 ft) and PNL1 above
it to the sloping top - the BRK1 tags there belong to the wing's north face (y 54.2, x 10.67-28.5) drawn beside it.
The 2026-07-28 drone photograph (validation only) shows the same continuous white tower with no brick on its front.

Correction (finish regions only - NO vertex is moved, added or removed; the wall, the curtain-wall placeholders, the
canopy, the vestibule, the v010 site and the v011 west-face regions are untouched):
  * the 12 faces of FR_NORTH_BRK1_N1 that lie on the band face (plane y 74.41, x 28.5-40) leave that object:
      - the face above the curtain-wall head (z >= 24.08) becomes the new object FR_NORTH_PNL1_N3b (PNL1 Bone White);
      - the 11 faces below it (the piers between the CW1 lite placeholders) become FR_NORTH_GLZ_N2b (curtain-wall
        backdrop placeholder, as N2 uses for x 40.7-70.3);
  * the three PNL1 slivers of FR_NORTH_PNL1_N3 at x 40-40.7 below the head (an artifact of the v001 lite-detection
    boundary) move into FR_NORTH_GLZ_N2b as well (the CW1 is continuous from x 28.8 to 70.2 on A4.02).
BRK1 stays on the wing north face (y 54.2), the wing west face, and everywhere else N1 applies.

Run:  blender --background --python scripts/Building_I/BI_build_entrance_finish_fix_v012.py [-- --no-render --samples N --views a,b --out DIR]
Outputs (refuses to overwrite): models/Building_I/BI_entrance_finish_v012.blend, renders/Building_I/BI_entrance_finish_v012_*.png
(including *_before_* renders through the same cameras from the untouched v011 scene), notes/Building_I/BI_entrance_finish_v012_build_report.json
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
BASE = ROOT / "models" / "Building_I" / "BI_entrance_facade_v011.blend"
STEM = "BI_entrance_finish_v012"
FT = 0.3048
TOUCH = ["FR_NORTH_BRK1_N1", "FR_NORTH_PNL1_N3"]
NEW = {"FR_NORTH_PNL1_N3b": "PNL1_Alucobond_PLUS_PVDF_Bone_White", "FR_NORTH_GLZ_N2b": "GLZ_Viracon_VZE1-42_in_EFCO_framing_placeholder"}
PLANE_Y = 74.41           # finish regions sit 0.03 ft in front of the band face y 74.38
X0, X1 = 28.5, 40.7       # band face west of the existing N2 backdrop (40.7-70.3)
HEAD = 24.08              # head of the westernmost CW1 lite placeholders (the N2 region uses 24.6 = CW1 head)
CAMS = {   # validation cameras (added; every other camera untouched)
    "BI_cam_photo_match_drone_2026-07-28a": {"loc": [-235.0, 265.0, 62.0], "target": [35.0, 85.0, 14.0], "lens": 32.0},   # approximate vantage of drone_2026-07-28_a.jpg (north-west of the entrance, looking south-east)   # approximate vantage of drone_2026-07-28_a.jpg (north-west of the entrance, ~45 ft up, looking south-east)
}
VIEWS = {  # name: (camera, resolution)
    "1_photo_match_drone": ("BI_cam_photo_match_drone_2026-07-28a", (2000, 1125)),
    "2_entrance_oblique": ("BI_cam_entrance_oblique", (2000, 1400)),
    "3_tower_closeup": ("BI_cam_tower_closeup", (2000, 1400)),
    "4_tower_corner_side": ("BI_cam_tower_side_depth", (2000, 1400)),
}
BEFORE_VIEWS = ["1_photo_match_drone", "2_entrance_oblique", "3_tower_closeup", "4_tower_corner_side"]


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


def vertex_set(o):
    """sorted world-space vertex coordinates (mm) - to prove no vertex moved, appeared or disappeared"""
    return sorted(tuple(round(c * 1000) for c in (o.matrix_world @ v.co)) for v in o.data.vertices)


def face_rects(o):
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
                    "area": p.area / FT / FT, "nsign": 1 if n[ax] > 0 else -1, "mat": me.materials[p.material_index].name if me.materials else "-"})
    return out


def union_area(rects):
    xs = sorted({r[0] for r in rects} | {r[1] for r in rects})
    ys = sorted({r[2] for r in rects} | {r[3] for r in rects})
    total = 0.0
    for i in range(len(xs) - 1):
        for j in range(len(ys) - 1):
            cx, cy = (xs[i] + xs[i + 1]) / 2, (ys[j] + ys[j + 1]) / 2
            if any(r[0] <= cx <= r[1] and r[2] <= cy <= r[3] for r in rects):
                total += (xs[i + 1] - xs[i]) * (ys[j + 1] - ys[j])
    return total


def overlaps(a, b):
    if a["axis"] != b["axis"] or abs(a["plane"] - b["plane"]) >= 0.05:
        return 0.0
    ou = min(a["u1"], b["u1"]) - max(a["u0"], b["u0"])
    ov = min(a["v1"], b["v1"]) - max(a["v0"], b["v0"])
    return ou * ov if ou > 0.01 and ov > 0.01 else 0.0


def move_faces(src, dst_name, dst_mat, pick, col, sig):
    """move the faces of src selected by pick(rect) into a new object dst_name (same vertex coordinates), return records"""
    rects = face_rects(src)
    chosen = [r for r in rects if pick(r)]
    if not chosen:
        return []
    idx = {r["index"] for r in chosen}
    bm = bmesh.new()
    bm.from_mesh(src.data)
    bm.faces.ensure_lookup_table()
    dst_bm = bmesh.new()
    for i in sorted(idx):
        f = bm.faces[i]
        vs = [dst_bm.verts.new(src.matrix_world @ v.co) for v in f.verts]
        nf = dst_bm.faces.new(vs)
        nf.normal_update()
        if nf.normal.dot(src.matrix_world.to_3x3() @ f.normal) < 0:
            nf.normal_flip()
    bmesh.ops.remove_doubles(dst_bm, verts=dst_bm.verts, dist=0.0005)
    bmesh.ops.delete(bm, geom=[bm.faces[i] for i in idx], context="FACES_ONLY")
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context="VERTS")
    bm.to_mesh(src.data)
    bm.free()
    src.data.update()
    if dst_name in bpy.data.objects:
        dst = bpy.data.objects[dst_name]
        cur = bmesh.new()
        cur.from_mesh(dst.data)
        for f in dst_bm.faces:
            vs = [cur.verts.new(v.co) for v in f.verts]
            cur.faces.new(vs)
        bmesh.ops.remove_doubles(cur, verts=cur.verts, dist=0.0005)
        cur.to_mesh(dst.data)
        cur.free()
        dst_bm.free()
    else:
        mesh = bpy.data.meshes.new(dst_name)
        dst_bm.to_mesh(mesh)
        dst_bm.free()
        dst = bpy.data.objects.new(dst_name, mesh)
        dst.data.materials.append(bpy.data.materials[dst_mat])
        col.objects.link(dst)
        dst["basis"] = "T"
        dst["note"] = sig
    dst.data.update()
    return [{"from": src.name, "to": dst_name, "old_material": r["mat"], "new_material": dst_mat, "x": [round(r["u0"], 2), round(r["u1"], 2)],
             "z": [round(r["v0"], 2), round(r["v1"], 2)], "sqft": round(r["area"], 1)} for r in chosen]


def add_cam(name, loc, target, lens=35.0):
    cam = bpy.data.cameras.new(name)
    cam.lens = lens
    cam.clip_end = 2000.0
    o = bpy.data.objects.new(name, cam)
    o.location = Vector([m(c) for c in loc])
    o.rotation_euler = (Vector([m(c) for c in target]) - o.location).to_track_quat("-Z", "Y").to_euler()
    bpy.data.collections["90_Cameras"].objects.link(o)
    return o


def render_views(scene, objs, render_dir, names, prefix, times):
    ctx_bii = [o for o in objs if o.name.startswith("CTX_") and "II" in o.name]
    for view in names:
        cam, (rx, ry) = VIEWS[view]
        for o in ctx_bii:      # the Building II context mass is hidden in the photo-match view only (the July 2026 photo predates it)
            o.hide_render = view == "1_photo_match_drone"
        scene.camera = objs[cam]
        scene.render.resolution_x, scene.render.resolution_y = rx, ry
        path = render_dir / f"{STEM}_{prefix}{view}.png"
        if path.exists():
            raise SystemExit(f"refusing to overwrite existing render: {path}")
        scene.render.filepath = str(path)
        t0 = time.time()
        bpy.ops.render.render(write_still=True)
        times[prefix + view] = round(time.time() - t0, 1)


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
    views = [v for v in VIEWS if not only or v in only]
    before_views = [v for v in BEFORE_VIEWS if v in views]

    bpy.ops.wm.open_mainfile(filepath=str(BASE))
    scene = bpy.context.scene
    objs = bpy.data.objects
    mats_before = {mt.name: mat_sig(mt) for mt in bpy.data.materials}
    keep_names = [o.name for o in objs if o.type == "MESH" and o.name not in TOUCH]
    h_before = geometry_hash(keep_names)
    verts_before = {n: vertex_set(objs[n]) for n in TOUCH}
    cams_before = sorted(o.name for o in objs if o.type == "CAMERA")
    col = objs[TOUCH[0]].users_collection[0]
    report = {"version": "v012", "base": str(BASE), "touched_objects": TOUCH, "new_objects": list(NEW), "kept_mesh_objects": len(keep_names), "geometry_hash_kept": h_before}
    rects0 = {n: face_rects(objs[n]) for n in TOUCH}
    report["before"] = {n: {"faces": len(rects0[n]), "sqft": round(sum(r["area"] for r in rects0[n]), 1),
                            "faces_on_band_face_x28_5_40_7": [{"index": r["index"], "x": [round(r["u0"], 2), round(r["u1"], 2)], "z": [round(r["v0"], 2), round(r["v1"], 2)], "sqft": round(r["area"], 1), "material": r["mat"]}
                                                              for r in rects0[n] if r["axis"] == 1 and abs(r["plane"] - PLANE_Y) < 0.05 and r["u0"] >= X0 - 0.05 and r["u1"] <= X1 + 0.05]} for n in TOUCH}

    for name, c in CAMS.items():
        assert name not in objs, name
        add_cam(name, c["loc"], c["target"], c["lens"])
    times = {}
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
        scene.cycles.samples = samples
        render_views(scene, objs, render_dir, before_views, "before_", times)

    # ---- the correction (faces change object / material only)
    on_band = lambda r: r["axis"] == 1 and abs(r["plane"] - PLANE_Y) < 0.05 and r["u0"] >= X0 - 0.05 and r["u1"] <= X1 + 0.05
    moved = []
    moved += move_faces(objs["FR_NORTH_BRK1_N1"], "FR_NORTH_PNL1_N3b", NEW["FR_NORTH_PNL1_N3b"], lambda r: on_band(r) and r["v0"] >= HEAD - 0.05, col,
                        "A4.02 North Elevation: PNL1 tower face continuous from x 28.5 to 71 above the CW1 head; BRK1 tags belong to the wing north face y 54.2 (v012)")
    moved += move_faces(objs["FR_NORTH_BRK1_N1"], "FR_NORTH_GLZ_N2b", NEW["FR_NORTH_GLZ_N2b"], lambda r: on_band(r) and r["v1"] <= HEAD + 0.05, col,
                        "A4.02 / A7.26: CW1 continuous from x 28.8 to 70.2, 0-24.6; curtain-wall backdrop placeholder as N2 (v012)")
    moved += move_faces(objs["FR_NORTH_PNL1_N3"], "FR_NORTH_GLZ_N2b", NEW["FR_NORTH_GLZ_N2b"], lambda r: on_band(r) and r["v1"] <= 24.6 + 0.05, col, "")
    report["faces_moved"] = moved
    for n in TOUCH:
        left = [r for r in face_rects(objs[n]) if on_band(r)]
        assert not left or n == "FR_NORTH_PNL1_N3" and all(r["v0"] >= 24.5 for r in left), (n, left)

    # ---- verification: no vertex moved / added / removed across the four objects
    after_union = []
    for n in TOUCH + list(NEW):
        after_union += vertex_set(objs[n])
    before_union = verts_before["FR_NORTH_BRK1_N1"] + verts_before["FR_NORTH_PNL1_N3"]
    report["vertex_multiset_identical"] = sorted(set(after_union)) == sorted(set(before_union))
    assert report["vertex_multiset_identical"]
    # coverage of the band face x 28.5-71, z 0-40 by regions + opening placeholders (plane y 74.38/74.41)
    regs = []
    for o in objs:
        if o.type == "MESH" and o.name.startswith("FR_NORTH_"):
            regs += [(r["u0"], r["u1"], r["v0"], r["v1"]) for r in face_rects(o) if r["axis"] == 1 and abs(r["plane"] - PLANE_Y) < 0.05 and r["u1"] > 28.5 and r["u0"] < 71.0]
    ops = []
    for o in objs:
        if o.type == "MESH" and o.name.startswith("BI_open_NORTH_"):
            pts = [o.matrix_world @ Vector(c) for c in o.bound_box]
            y0, y1 = min(p.y for p in pts) / FT, max(p.y for p in pts) / FT
            if abs((y0 + y1) / 2 - 74.38) < 0.35:
                x0, x1 = min(p.x for p in pts) / FT, max(p.x for p in pts) / FT
                z0, z1 = min(p.z for p in pts) / FT, max(p.z for p in pts) / FT
                ops.append((max(x0, 28.5), min(x1, 71.0), max(z0, 0.0), min(z1, 40.0)))
    cov = union_area([(max(r[0], 28.5), min(r[1], 71.0), max(r[2], 0.0), min(r[3], 40.0)) for r in regs] + ops)
    report["band_north_face_coverage"] = {"regions_plus_openings_sqft": round(cov, 1), "face_sqft": 42.5 * 40.0, "openings_on_plane": len(ops)}
    # overlaps between the north-face region objects
    allr = []
    for o in objs:
        if o.type == "MESH" and o.name.startswith("FR_NORTH_"):
            allr += [dict(r, obj=o.name) for r in face_rects(o) if r["axis"] == 1 and abs(r["plane"] - PLANE_Y) < 0.05 and r["u1"] > 28.5 and r["u0"] < 71.0]
    pairs = [(a["obj"], a["index"], b["obj"], b["index"], round(overlaps(a, b), 2)) for i, a in enumerate(allr) for b in allr[i + 1:] if overlaps(a, b) > 0.05]
    report["coplanar_overlaps_on_band_face"] = pairs
    assert not pairs, pairs
    report["after"] = {n: {"faces": len(objs[n].data.polygons), "sqft": round(sum(r["area"] for r in face_rects(objs[n])), 1), "materials": [mt.name for mt in objs[n].data.materials]} for n in TOUCH + list(NEW)}
    report["materials_by_face_on_band_face"] = {}
    for o in objs:
        if o.type == "MESH" and o.name.startswith("FR_NORTH_"):
            for r in face_rects(o):
                if r["axis"] == 1 and abs(r["plane"] - PLANE_Y) < 0.05 and r["u1"] > 28.5 and r["u0"] < 40.8:
                    report["materials_by_face_on_band_face"].setdefault(o.name, []).append({"x": [round(r["u0"], 2), round(r["u1"], 2)], "z": [round(r["v0"], 2), round(r["v1"], 2)], "material": r["mat"], "sqft": round(r["area"], 1)})

    assert geometry_hash(keep_names) == h_before, "unrelated geometry changed - aborting"
    assert {mt.name: mat_sig(mt) for mt in bpy.data.materials} == mats_before, "material node trees changed - aborting"
    report["unrelated_geometry_unchanged"] = True
    report["material_node_trees_unchanged"] = True
    report["cameras_added"] = sorted(set(o.name for o in objs if o.type == "CAMERA") - set(cams_before))
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))
    if do_render:
        render_views(scene, objs, render_dir, views, "", times)
        report["render_seconds"] = times
        for o in objs:
            if o.name.startswith("CTX_") and "II" in o.name:
                o.hide_render = False
        scene.camera = objs["BI_cam_entrance_oblique"]
        bpy.ops.wm.save_mainfile()
        assert geometry_hash(keep_names) == h_before
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("BUILD_REPORT=" + json.dumps(report))


if __name__ == "__main__":
    main()
