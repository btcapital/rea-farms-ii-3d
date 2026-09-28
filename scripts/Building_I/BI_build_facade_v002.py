"""Rea Farms Building I - facade / material baseline, v002.

Opens the APPROVED geometry baseline models/Building_I/BI_shell_v001.blend (never
saved back), keeps every v001 mesh's vertex coordinates untouched, and adds:
  * documented materials (names carry product / colour / confidence) assigned to
    the existing objects (material slots only - no vertex changes);
  * top faces of the shell prisms tagged as TPO roof (polygon material index only);
  * collection 07_Facade_overlay_v002: thin cladding panels 0.02 ft proud of the
    walls, one per classified facade rectangle in BI_facade_data_v002.json;
  * one extra close-up camera at the entry; six renders.
Every number/name is documented in notes/Building_I/BI_material_control_v002.md.

Run (from the project root):
  "C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe" --background --python scripts/Building_I/BI_build_facade_v002.py
Optional:  -- --no-render     save the .blend only
           -- --out <folder>  write every output into <folder> instead (trial runs)
The script refuses to overwrite any existing output file and verifies that the v001
geometry hash is unchanged before saving.
"""
from pathlib import Path
import hashlib
import json
import math
import sys
import time

import bpy
import bmesh
from mathutils import Vector

VERSION = "v002"
STEM = f"BI_facade_{VERSION}"
ROOT = Path(__file__).resolve().parent.parent.parent
BASE = ROOT / "models" / "Building_I" / "BI_shell_v001.blend"
GEOM = ROOT / "notes" / "Building_I" / "BI_geometry_data_v001.json"
DATA = ROOT / "notes" / "Building_I" / f"BI_facade_data_{VERSION}.json"
BLEND = ROOT / "models" / "Building_I" / f"{STEM}.blend"
REPORT = ROOT / "notes" / "Building_I" / f"{STEM}_build_report.json"
RENDER_DIR = ROOT / "renders" / "Building_I"
FT = 0.3048


def m(ft):
    return ft * FT


def geometry_hash(names=None):
    """SHA-256 over the world-space vertex coordinates of the named (v001) mesh objects."""
    h = hashlib.sha256()
    for o in sorted(bpy.data.objects, key=lambda o: o.name):
        if o.type != "MESH" or (names is not None and o.name not in names):
            continue
        h.update(o.name.encode())
        for v in o.data.vertices:
            p = o.matrix_world @ v.co
            h.update(f"{p.x:.4f},{p.y:.4f},{p.z:.4f};".encode())
    return h.hexdigest()


def clay(name, rgb, alpha=1.0, roughness=0.8):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    if alpha < 1.0:
        bsdf.inputs["Alpha"].default_value = alpha
    return mat


def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def clip_halfplane(poly, a, b, c):
    out = []
    n = len(poly)
    for i in range(n):
        p, q = poly[i], poly[(i + 1) % n]
        fp, fq = a * p[0] + b * p[1] - c, a * q[0] + b * q[1] - c
        if fp <= 1e-9:
            out.append(p)
        if (fp < 0) != (fq < 0) and abs(fp - fq) > 1e-12:
            t = fp / (fp - fq)
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    res = []
    for p in out:
        if not res or abs(p[0] - res[-1][0]) > 1e-6 or abs(p[1] - res[-1][1]) > 1e-6:
            res.append(p)
    if len(res) > 1 and abs(res[0][0] - res[-1][0]) < 1e-6 and abs(res[0][1] - res[-1][1]) < 1e-6:
        res.pop()
    return res


def face_coordinate(polys, facade, u):
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


def box(name, x0, y0, z0, x1, y1, z1, col, mat):
    bm = bmesh.new()
    vs = [bm.verts.new((m(x), m(y), m(z))) for x, y, z in
          [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]]
    for f in [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]:
        bm.faces.new([vs[i] for i in f])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    obj.data.materials.append(mat)
    col.objects.link(obj)
    return obj


def look_at(obj, target_ft):
    direction = Vector([m(c) for c in target_ft]) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def add_camera(name, loc_ft, target_ft, col, lens=35.0):
    cam = bpy.data.cameras.new(name)
    cam.clip_start, cam.clip_end = 0.5, 3000.0
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
    RENDER_DIR.mkdir(parents=True, exist_ok=True)

    bpy.ops.wm.open_mainfile(filepath=str(BASE))
    scene = bpy.context.scene
    v001_names = {o.name for o in bpy.data.objects if o.type == "MESH"}
    h_before = geometry_hash(v001_names)
    D = json.loads(DATA.read_text(encoding="utf-8"))
    G = json.loads(GEOM.read_text(encoding="utf-8"))
    M = D["materials"]
    mats = {k: clay(v["name"], v["rgb"], alpha=(0.55 if k == "TWS1" else 1.0), roughness=(0.15 if k in ("GLASS", "CANOPY_GLASS") else 0.8))
            for k, v in M.items()}

    # ---- re-assign materials on the v001 objects (slots only; vertices untouched)
    o = bpy.data.objects
    swap = {"BI_clay": "UNRES_BASE", "BI_clay_screen": "UNRES_BASE", "BI_glass_placeholder": "GLASS",
            "BI_canopy_glass": "CANOPY_GLASS", "BI_steel": "STEEL", "BI_grid": "GRID", "BI_ground": "GROUND", "BI_slab": "SLAB"}
    for obj in o:
        if obj.type != "MESH":
            continue
        for slot in obj.material_slots:
            if slot.material and slot.material.name in swap:
                slot.material = mats[swap[slot.material.name]]
    o["BI_Z6_mech_screen"].material_slots[0].material = mats["SCREEN"]
    o["BI_Z3_vestibule_100"].material_slots[0].material = mats["UNRES_VESTIBULE"]
    # roof (top faces) of the shell prisms -> TPO
    for name in ("BI_Z1_south_wing", "BI_Z2_band_E_F2", "BI_Z4a_north_block", "BI_Z4b_north_block_south_part", "BI_Z5_end_block_13_14"):
        obj = o[name]
        obj.data.materials.append(mats["TPO"])
        idx = len(obj.data.materials) - 1
        for p in obj.data.polygons:
            if p.normal.z > 0.7:
                p.material_index = idx

    # ---- facade overlay panels
    root = bpy.data.collections[f"Building_I_v001"]
    col = bpy.data.collections.new(f"07_Facade_overlay_{VERSION}")
    root.children.link(col)
    fp = [tuple(p) for p in G["footprint_union"]]
    W = G["wing"]; se = G["se_block_13_14"]; band = G["band_E_F2"]; ves = G["vestibule_100"]
    wing_poly = clip_halfplane(clip_halfplane(fp, 0, 1, W["split_y"]), 1, 0, se["x0"])
    north_a = clip_halfplane(fp, 0, -1, -se["y1"])
    north_b = clip_halfplane(clip_halfplane(clip_halfplane(fp, 0, -1, -W["split_y"]), 0, 1, se["y1"]), 1, 0, se["x0"])
    zone_polys = [wing_poly, north_a, north_b, rect(band["x0"], band["y0"], band["x1"], band["y1"]),
                  rect(ves["x0"], ves["y0"], ves["x1"], ves["y1"]), rect(se["x0"], se["y0"], se["x1"], se["y1"])]
    off, th = D["overlay"]["offset_out"], D["overlay"]["thickness"]
    placed = {}; skipped = 0; area = {}
    for facade, rects in D["facade_rectangles"].items():
        for j, (cls, u0, u1, z0, z1) in enumerate(rects):
            uc = (u0 + u1) / 2
            face = face_coordinate(zone_polys, facade, uc)
            if face is None or cls not in mats:
                skipped += 1
                continue
            nm = f"FD_{facade}_{cls}_{j+1:03d}"
            if facade == "SOUTH":
                box(nm, u0, face - off - th, z0, u1, face - off, z1, col, mats[cls])
            elif facade == "NORTH":
                box(nm, u0, face + off, z0, u1, face + off + th, z1, col, mats[cls])
            elif facade == "EAST":
                box(nm, face + off, u0, z0, face + off + th, u1, z1, col, mats[cls])
            else:
                box(nm, face - off - th, u0, z0, face - off, u1, z1, col, mats[cls])
            placed[cls] = placed.get(cls, 0) + 1
            area[cls] = round(area.get(cls, 0) + (u1 - u0) * (z1 - z0), 1)

    # ---- close-up camera at the entry (north-west, eye level +6 ft)
    camcol = bpy.data.collections["90_Cameras"]
    close = add_camera("BI_cam_closeup_entry", (-60.0, 150.0, 9.0), (45.0, 82.0, 12.0), camcol, lens=28.0)

    h_after = geometry_hash(v001_names)
    report = {"version": VERSION, "base": str(BASE), "v001_mesh_objects": len(v001_names), "geometry_hash_v001_loaded": h_before, "geometry_hash_after_material_pass": h_after,
              "geometry_unchanged": h_before == h_after, "overlay_panels": placed, "overlay_area_sqft": area, "overlay_skipped": skipped,
              "materials": {k: v["name"] for k, v in M.items()},
              "objects_per_collection": {c.name: len(c.objects) for c in root.children_recursive}}
    assert h_before == h_after, "v001 geometry changed - aborting"
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))

    if do_render:
        report["gpu"] = setup_gpu(scene)
        scene.cycles.samples = 64
        scene.cycles.use_denoising = True
        scene.render.image_settings.file_format = "PNG"
        scene.view_settings.view_transform = "Standard"
        views = {"front_north": ("BI_cam_front_north", (2400, 900)), "rear_south": ("BI_cam_rear_south", (2400, 900)),
                 "left_west": ("BI_cam_left_west", (2400, 900)), "right_east": ("BI_cam_right_east", (2400, 900)),
                 "oblique_northwest": ("BI_cam_oblique_northwest", (2000, 1400)), "closeup_entry": ("BI_cam_closeup_entry", (2000, 1400))}
        times = {}
        for view, (cam, (rx, ry)) in views.items():
            scene.camera = o[cam]
            scene.render.resolution_x, scene.render.resolution_y = rx, ry
            path = RENDER_DIR / f"{STEM}_{view}.png"
            if path.exists():
                raise SystemExit(f"refusing to overwrite existing render: {path}")
            scene.render.filepath = str(path)
            t0 = time.time()
            bpy.ops.render.render(write_still=True)
            times[view] = round(time.time() - t0, 1)
        report["render_seconds"] = times
        scene.camera = o["BI_cam_oblique_northwest"]
        bpy.ops.wm.save_mainfile()
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("BUILD_REPORT=" + json.dumps(report))


if __name__ == "__main__":
    main()
