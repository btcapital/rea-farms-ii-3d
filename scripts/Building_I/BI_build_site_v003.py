"""Rea Farms Building I - site / grading baseline, v003.

Opens the APPROVED BI_facade_v002.blend (never saved back), keeps every v002 object's
vertex coordinates and material slots untouched, and adds collection 08_Site_v003:
  * terrain: inverse-distance interpolation through the CG-101 spot elevations (INTERPOLATED)
  * hardscape slabs: asphalt parking/drives, walks, entry plaza (polygons from CS-101, M)
  * 6" curbs implied by raising walk/island slabs 0.5 ft above the asphalt surface
  * brick landscape retaining wall (TW 661.00, RFI 78), dumpster enclosure (A0.04 size, CS-101 position)
  * street bands at the right-of-way positions (context), Building II context mass (shared-site register)
  * foundation skirt below the building so the terrain never shows through the shell
Every number is documented in notes/Building_I/BI_site_control_v003.md and BI_site_data_v003.json.

Run (from the project root):
  "C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe" --background --python scripts/Building_I/BI_build_site_v003.py
Optional:  -- --no-render   |   -- --out <folder>  (trial runs)
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

VERSION = "v003"
STEM = f"BI_site_{VERSION}"
ROOT = Path(__file__).resolve().parent.parent.parent
BASE = ROOT / "models" / "Building_I" / "BI_facade_v002.blend"
GEOM = ROOT / "notes" / "Building_I" / "BI_geometry_data_v001.json"
DATA = ROOT / "notes" / "Building_I" / f"BI_site_data_{VERSION}.json"
BLEND = ROOT / "models" / "Building_I" / f"{STEM}.blend"
REPORT = ROOT / "notes" / "Building_I" / f"{STEM}_build_report.json"
RENDER_DIR = ROOT / "renders" / "Building_I"
FT = 0.3048


def m(ft):
    return ft * FT


def geometry_hash(names):
    h = hashlib.sha256()
    for o in sorted(bpy.data.objects, key=lambda o: o.name):
        if o.type != "MESH" or o.name not in names:
            continue
        h.update(o.name.encode())
        for v in o.data.vertices:
            p = o.matrix_world @ v.co
            h.update(f"{p.x:.4f},{p.y:.4f},{p.z:.4f};".encode())
        h.update(",".join(s.material.name if s.material else "-" for s in o.material_slots).encode())
    return h.hexdigest()


def clay(name, rgb, roughness=0.9):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    return mat


def new_object(name, bm, col, mat):
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    obj.data.materials.append(mat)
    col.objects.link(obj)
    return obj


def poly_area(poly):
    return 0.5 * sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1] for i in range(len(poly)))


def clean(poly):
    out = []
    for p in poly:
        if not out or abs(p[0] - out[-1][0]) > 0.02 or abs(p[1] - out[-1][1]) > 0.02:
            out.append((p[0], p[1]))
    if len(out) > 2 and abs(out[0][0] - out[-1][0]) < 0.02 and abs(out[0][1] - out[-1][1]) < 0.02:
        out.pop()
    return out


def slab(name, poly, zfunc, thick, col, mat, holes=None):
    """Polygon slab whose top follows zfunc(x, y); bottom = top - thick."""
    poly = clean(poly)
    if poly_area(poly) < 0:
        poly = poly[::-1]
    bm = bmesh.new()
    verts = [bm.verts.new((m(x), m(y), m(zfunc(x, y)))) for x, y in poly]
    face = bm.faces.new(verts)
    bmesh.ops.triangulate(bm, faces=[face], ngon_method="EAR_CLIP")
    # subdivide until no edge is longer than 12 ft, re-sampling z from zfunc, so large slabs follow the
    # interpolated terrain instead of spanning it as flat planes (which buried the parking lot)
    for _ in range(10):
        long_edges = [e for e in bm.edges if (e.verts[0].co - e.verts[1].co).length > m(6.0)]
        if not long_edges:
            break
        bmesh.ops.subdivide_edges(bm, edges=long_edges, cuts=1, use_grid_fill=True)
    for v in bm.verts:
        v.co.z = m(zfunc(v.co.x / FT, v.co.y / FT))
    res = bmesh.ops.extrude_face_region(bm, geom=list(bm.faces))
    for v in [g for g in res["geom"] if isinstance(g, bmesh.types.BMVert)]:
        v.co.z -= m(thick)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return new_object(name, bm, col, mat)


def box(name, x0, y0, z0, x1, y1, z1, col, mat):
    bm = bmesh.new()
    vs = [bm.verts.new((m(x), m(y), m(z))) for x, y, z in
          [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]]
    for f in [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]:
        bm.faces.new([vs[i] for i in f])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return new_object(name, bm, col, mat)


def point_in_poly(x, y, poly):
    inside = False
    n = len(poly)
    for i in range(n):
        (xa, ya), (xb, yb) = poly[i], poly[(i + 1) % n]
        if (ya > y) != (yb > y):
            xi = xa + (y - ya) * (xb - xa) / (yb - ya)
            if xi > x:
                inside = not inside
    return inside


def look_at(obj, target_ft):
    direction = Vector([m(c) for c in target_ft]) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def add_camera(name, loc_ft, target_ft, col, lens=35.0, ortho_ft=None):
    cam = bpy.data.cameras.new(name)
    cam.clip_start, cam.clip_end = 0.5, 4000.0
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
    v002_names = {o.name for o in bpy.data.objects if o.type == "MESH"}
    h_before = geometry_hash(v002_names)
    D = json.loads(DATA.read_text(encoding="utf-8"))
    G = json.loads(GEOM.read_text(encoding="utf-8"))
    FFE = D["datum"]["ffe"]

    root = bpy.data.collections["Building_I_v001"]
    col = bpy.data.collections.new(f"08_Site_{VERSION}")
    root.children.link(col)
    sub = {}
    for name in ("terrain", "hardscape", "walls_structures", "context", "reference"):
        c = bpy.data.collections.new(f"08_Site_{VERSION}_{name}")
        col.children.link(c)
        sub[name] = c
    mats = {k: clay(v["name"], v["rgb"]) for k, v in D["materials"].items()}

    # ---- terrain: IDW through the documented spots (surface INTERPOLATED), building footprint excluded
    spots = [(s["x"], s["y"], s["z"] - FFE) for s in D["spots"]]
    fp = [tuple(p) for p in G["footprint_union"]]
    band = D["exclusions"]["band"]
    ves = D["exclusions"]["vestibule"]
    ex_polys = [fp, [(band[0], band[1]), (band[2], band[1]), (band[2], band[3]), (band[0], band[3])],
                [(ves[0], ves[1]), (ves[2], ves[1]), (ves[2], ves[3]), (ves[0], ves[3])]]
    T = D["terrain"]
    x0, y0, x1, y1, step = T["x0"], T["y0"], T["x1"], T["y1"], T["step"]

    def idw(x, y):
        num = den = 0.0
        best = None
        for sx, sy, sz in spots:
            d2 = (sx - x) ** 2 + (sy - y) ** 2
            if d2 < 0.01:
                return sz
            w = 1.0 / (d2 ** 1.5)
            num += w * sz
            den += w
        return num / den

    # terrain cells that lie entirely under an asphalt surface (dz == 0 hardscape, street bands) are omitted so the
    # asphalt slab is the only surface there (no z-fighting); cells straddling an asphalt edge are kept
    asph_polys = [[tuple(q) for q in hs["polygon"]] for hs in D["hardscape"] if hs.get("dz", 0.0) == 0.0]
    asph_polys += [[(st["x0"], st["y0"]), (st["x1"], st["y0"]), (st["x1"], st["y1"]), (st["x0"], st["y1"])] for st in D["streets"]]
    nx = int((x1 - x0) / step) + 1
    ny = int((y1 - y0) / step) + 1
    bm = bmesh.new()
    grid = {}
    for j in range(ny):
        for i in range(nx):
            x = x0 + i * step
            y = y0 + j * step
            grid[(i, j)] = bm.verts.new((m(x), m(y), m(idw(x, y))))
    bm.verts.ensure_lookup_table()
    n_faces = 0
    for j in range(ny - 1):
        for i in range(nx - 1):
            cx = x0 + (i + 0.5) * step
            cy = y0 + (j + 0.5) * step
            if any(point_in_poly(cx, cy, p) for p in ex_polys):
                continue
            corners = [(x0 + i * step, y0 + j * step), (x0 + (i + 1) * step, y0 + j * step),
                       (x0 + (i + 1) * step, y0 + (j + 1) * step), (x0 + i * step, y0 + (j + 1) * step)]
            if any(all(point_in_poly(px, py, p) for px, py in corners) for p in asph_polys):
                continue
            bm.faces.new([grid[(i, j)], grid[(i + 1, j)], grid[(i + 1, j + 1)], grid[(i, j + 1)]])
            n_faces += 1
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.001)
    unused = [v for v in bm.verts if not v.link_faces]
    bmesh.ops.delete(bm, geom=unused, context="VERTS")
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    terrain = new_object("SITE_terrain_IDW_INTERPOLATED", bm, sub["terrain"], mats["lawn"])
    terrain["note"] = "Inverse-distance interpolation through CG-101 spot elevations. Entire surface is INTERPOLATED except at the spots."

    # ---- hardscape slabs (top follows the interpolated terrain + documented offset)
    def zt(dz):
        return lambda x, y: idw(x, y) + dz

    made = {}
    for k, hs in enumerate(D["hardscape"]):
        dz = hs.get("dz", 0.0)
        if dz == 0.0:
            dz = 0.1 + 0.01 * k   # render offset (staggered so overlapping asphalt slabs do not z-fight): asphalt nominally AT terrain level; 0.1 ft keeps it from z-fighting the terrain mesh
        obj = slab(f"SITE_{hs['name']}", [tuple(p) for p in hs["polygon"]], zt(dz), hs.get("thickness", 0.5), sub["hardscape"], mats[hs["material"]])
        obj["source"] = hs["source"]
        made[hs["name"]] = obj
    # ---- walls / structures
    for w in D["walls"]:
        o = box(f"SITE_{w['name']}", w["x0"], w["y0"], w["z0"] - FFE, w["x1"], w["y1"], w["z1"] - FFE, sub["walls_structures"], mats[w["material"]])
        o["source"] = w["source"]
    # ---- foundation skirt (hides terrain under the shell; documented assumption)
    sk = D["foundation_skirt"]
    slab("SITE_foundation_skirt_A", fp, lambda x, y: sk["z_top"], sk["depth"], sub["walls_structures"], mats["skirt"])
    slab("SITE_foundation_skirt_band_A", ex_polys[1], lambda x, y: sk["z_top"], sk["depth"], sub["walls_structures"], mats["skirt"])
    slab("SITE_foundation_skirt_vestibule_A", ex_polys[2], lambda x, y: sk["z_top"], sk["depth"], sub["walls_structures"], mats["skirt"])
    # ---- context: streets and Building II
    for k, s in enumerate(D["streets"]):
        slab(f"CTX_{s['name']}", [(s["x0"], s["y0"]), (s["x1"], s["y0"]), (s["x1"], s["y1"]), (s["x0"], s["y1"])], zt(0.1 + 0.01 * k), 0.5, sub["context"], mats["asphalt"])
    b2 = D["building_ii_context"]
    o = box("CTX_Building_II_mass_from_BII_CS-101_rev6", b2["x0"], b2["y0"], b2["ffe"] - FFE, b2["x1"], b2["y1"], b2["ffe"] - FFE + b2["height"], sub["context"], mats["context"])
    o["source"] = b2["source"]
    # grade plane of v002 stays but is hidden (superseded by terrain)
    gp = bpy.data.objects.get("BI_grade_plane_660")
    if gp:
        gp.hide_render = True
        gp.hide_viewport = True

    # ---- cameras: elevated site oblique
    camcol = bpy.data.collections["90_Cameras"]
    add_camera("BI_cam_site_elevated", (560.0, -390.0, 320.0), (80.0, 160.0, 0.0), camcol, lens=28.0)
    # v001 grid-control lines sit just below the old flat 660 grade plane; with real terrain they would show
    # through wherever grade < 659.75. Hidden at collection level for render only (objects untouched).
    gc = bpy.data.collections.get("05_Grid_control")
    if gc:
        gc.hide_render = True

    h_after = geometry_hash(v002_names)
    assert h_before == h_after, "v002 geometry/material state changed - aborting"
    report = {"version": VERSION, "base": str(BASE), "v002_mesh_objects": len(v002_names), "geometry_hash_v002": h_before, "geometry_unchanged": True,
              "terrain_faces": n_faces, "spots_used": len(spots), "hardscape": list(made), "objects_per_collection": {c.name: len(c.objects) for c in col.children_recursive}}
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
                 "oblique_northwest": ("BI_cam_oblique_northwest", (2000, 1400)), "site_elevated": ("BI_cam_site_elevated", (2000, 1400))}
        times = {}
        for view, (cam, (rx, ry)) in views.items():
            scene.camera = o[cam]
            scene.render.resolution_x, scene.render.resolution_y = rx, ry
            path = RENDER_DIR / f"{STEM}_{view}.png"
            if path.exists():
                raise SystemExit(f"refusing to overwrite existing render: {path}")
            scene.render.filepath = str(path)
            ctx = o["CTX_Building_II_mass_from_BII_CS-101_rev6"]
            ctx.hide_render = (view == "left_west")   # Building II stands between this camera and Building I
            t0 = time.time()
            bpy.ops.render.render(write_still=True)
            ctx.hide_render = False
            times[view] = round(time.time() - t0, 1)
        report["render_seconds"] = times
        scene.camera = o["BI_cam_site_elevated"]
        bpy.ops.wm.save_mainfile()
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("BUILD_REPORT=" + json.dumps(report))


if __name__ == "__main__":
    main()
