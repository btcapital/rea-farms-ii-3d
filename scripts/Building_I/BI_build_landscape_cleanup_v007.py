r"""Building I - landscape / site coordination cleanup v007.

Opens the approved BI_landscape_v006.blend and, using BI_landscape_data_v007.json:
  * rebuilds the four plant groups that contain plants returned to their documented positions (G-9 / G-10 zones),
  * rebuilds the species-unresolved symbol object (117 symbols),
  * adds the resolved EMRA (26 + 11), ABFR (+2) and LOJA (+2) groups with mulch discs,
  * adds 42 existing street trees documented on the Building II LP-100 rev 2 (N Rea Park Ln, N Old Springs Rd).
Everything else is hashed before/after and must be identical. Saves models/Building_I/BI_landscape_v007.blend and renders
renders/Building_I/BI_landscape_v007_*.png.

Run:  "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --background --python scripts/Building_I/BI_build_landscape_cleanup_v007.py
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
BASE = ROOT / "models" / "Building_I" / "BI_landscape_v006.blend"
DATA = ROOT / "notes" / "Building_I" / "BI_landscape_data_v007.json"
GEOM = ROOT / "notes" / "Building_I" / "BI_geometry_data_v001.json"
SITE = ROOT / "notes" / "Building_I" / "BI_site_data_v003.json"
STEM = "BI_landscape_v007"
FT = 0.3048
FFE = 661.75

spec = importlib.util.spec_from_file_location("v4", ROOT / "scripts" / "Building_I" / "BI_build_landscape_v004.py")
v4 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v4)   # helpers only (m, geometry_hash, material, new_object, point_in_poly, push_outside, add_sphere, add_cylinder, add_disc)
m, geometry_hash, new_object = v4.m, v4.geometry_hash, v4.new_object
push_outside, add_sphere, add_cylinder, add_disc = v4.push_outside, v4.add_sphere, v4.add_cylinder, v4.add_disc


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
    S = json.loads(SITE.read_text(encoding="utf-8"))
    fp = [tuple(p) for p in G["footprint_union"]]
    SZ = D["sizes_for_model"]
    sched = D["schedule"]
    M = {k: bpy.data.materials[f"LS_{k}"] for k in D["materials"]}
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
    surfaces = [o for o in bpy.data.objects if o.type == "MESH" and o.name.startswith(("SITE_terrain", "SITE_asphalt", "SITE_walk", "SITE_entry", "SITE_plaza"))]

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
        return best if best is not None else m(idw(x, y))
    islands = D["parking_islands"]["items"]

    def on_island(x, y):
        return any(abs(x - i["x"]) <= i["w"] / 2 and abs(y - i["y"]) <= i["h"] / 2 for i in islands)

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

    cols = {c.name: c for c in bpy.data.collections}
    sub = {k: cols[f"09_Landscape_v004_{k}"] for k in ("trees", "shrubs", "groundcover", "beds_islands", "context")}

    # ---- which group objects must be rebuilt: groups holding kept-documented plants
    groups = {}
    for p in D["plants"]:
        groups.setdefault((p["code"], p["sheet"], p["callout_n"]), []).append(p)
    rebuild_keys = sorted({(p["code"], p["sheet"], p["callout_n"]) for p in D["plants"] if p.get("keep_documented")})
    new_keys = sorted({(p["code"], p["sheet"], p["callout_n"]) for p in D["plants"] if p["callout_n"] == 0 or p["code"] == "EMRA"})
    to_remove = []
    for code, sheet, n in rebuild_keys:
        t = sched[code]["type"]
        for nm in (f"LS_{t}_{code}_{sheet}_n{n}", f"LS_mulch_{code}_{sheet}_n{n}_INTERPRETED"):
            if nm in bpy.data.objects:
                to_remove.append(nm)
    to_remove.append("LS_shrub_UNRESOLVED_species_documented_symbol")
    keep_names = [o.name for o in bpy.data.objects if o.type == "MESH" and o.name not in to_remove]
    h_before = geometry_hash(keep_names)
    for nm in to_remove:
        o = bpy.data.objects[nm]
        me = o.data
        bpy.data.objects.remove(o, do_unlink=True)
        if me.users == 0:
            bpy.data.meshes.remove(me)

    shifted, kept = [], []
    built = []

    def build_group(code, sheet, n, items, suffix=""):
        info = sched[code]
        t = info["type"]
        h = info.get("height_in_min", 18) / 12 if t == "shrub" else (0.6 if t == "annual" else (0.8 if code in ("MUHL", "CARZ", "CARE", "RUSS", "CATM") else 0.6))
        w = min(info.get("spacing_ft", 3), 1.3 * h) if t == "shrub" else (1.0 if t == "annual" else min(info.get("spacing_in", 24) / 12, 2.0))
        bm = bmesh.new()
        bmm = bmesh.new()
        for p in items:
            if p.get("keep_documented"):
                x, y = p["x"], p["y"]
                kept.append({"code": code, "x": x, "y": y, "why": p["keep_documented"]})
            else:
                x, y, dshift = push_outside(p["x"], p["y"], fp, 1.2)
                if dshift:
                    shifted.append({"code": code, "from": [p["x"], p["y"]], "to": [round(x, 2), round(y, 2)], "shift_ft": round(dshift, 2)})
            z = grade(x, y) + (m(0.5) if on_island(x, y) else 0.0)
            add_sphere(bm, m(x), m(y), z + m(h * 0.5), m(w / 2), m(w / 2), m(h * 0.55), seg=8, ring=5)
            add_disc(bmm, m(x), m(y), z + m(0.06), m(SZ["mulch_disc_radius_ft"]))
        name = f"LS_{t}_{code}_{sheet}_n{n}{suffix}"
        o = new_object(name, bm, sub["shrubs" if t == "shrub" else "groundcover"], foliage_mat(code))
        o["conf"] = ",".join(sorted(set(p["conf"] for p in items)))
        o["source"] = f"{sheet} callout ({n}) {code}" if n else f"{sheet} {items[0].get('basis', '')}"
        o["schedule"] = json.dumps(info)
        om = new_object(f"LS_mulch_{code}_{sheet}_n{n}{suffix}_INTERPRETED", bmm, sub["beds_islands"], M["mulch"])
        om["note"] = "mulch disc per documented plant; bed outline not modeled (I)"
        built.append(name)

    for key in rebuild_keys:
        build_group(*key, groups[key])
    for key in new_keys:
        code, sheet, n = key
        build_group(code, sheet, n, groups[key], suffix="" if n else "_adj")

    # ---- unresolved symbols (117)
    bm = bmesh.new()
    for u in D["unassigned_symbols"]:
        x, y, dshift = push_outside(u["x"], u["y"], fp, 1.2)
        z = grade(x, y) + (m(0.5) if on_island(x, y) else 0.0)
        add_sphere(bm, m(x), m(y), z + m(0.75), m(1.4), m(1.4), m(0.8), seg=8, ring=5)
    o = new_object("LS_shrub_UNRESOLVED_species_documented_symbol", bm, sub["shrubs"], bpy.data.materials["LS_unresolved_grey_green"])
    o["note"] = f"{len(D['unassigned_symbols'])} plant symbols drawn on LP-100/LP-101 not linked to a callout leader; species unresolved (U)"

    # ---- street trees from the Building II LP-100 rev 2 (shared streets)
    H, C, T = SZ["tree_existing"]["height_ft"], SZ["tree_existing"]["canopy_ft"], SZ["tree_existing"]["trunk_in"] / 12
    counters = {}
    for t in D["existing_street_trees"]["items_v007_added"]:
        counters[t["street"]] = counters.get(t["street"], 0) + 1
        bm = bmesh.new()
        z = grade(t["x"], t["y"])
        add_cylinder(bm, m(t["x"]), m(t["y"]), z, z + m(H * 0.4), m(T / 2))
        add_sphere(bm, m(t["x"]), m(t["y"]), z + m(H * 0.68), m(C / 2), m(C / 2), m(H * 0.32))
        o = new_object(f"CTX_existing_street_tree_{t['street']}_{counters[t['street']]:02d}_BII-LP100", bm, sub["context"], M["trunk"])
        o.data.materials.append(M["foliage_existing"])
        for f in o.data.polygons:
            f.material_index = 1 if (o.matrix_world @ o.data.vertices[f.vertices[0]].co).z > z + m(H * 0.4) + 1e-4 else 0
        o["source"] = t["source"]

    h_after = geometry_hash(keep_names)
    assert h_before == h_after, "unrelated geometry changed - aborting"
    report = {"version": "v007", "base": str(BASE), "kept_mesh_objects": len(keep_names), "geometry_hash_kept": h_before, "unrelated_geometry_unchanged": True,
              "objects_removed_and_rebuilt": to_remove, "objects_built": built, "plants_kept_at_documented_position": kept, "plants_pushed_in_rebuilt_groups": shifted,
              "unresolved_symbols": len(D["unassigned_symbols"]), "street_trees_added": counters, "v007_changes": D["meta"]["v007_changes"]}
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
        views = {"front_north_elevation": ("BI_cam_north_elevation_ortho", (3000, 1000)), "entrance_oblique": ("BI_cam_entrance_oblique", (2000, 1400)),
                 "oblique_northwest": ("BI_cam_oblique_northwest", (2000, 1400)), "site_elevated": ("BI_cam_site_elevated", (2000, 1400)),
                 "landscape_entry": ("BI_cam_landscape_entry", (2000, 1400)), "rear_south": ("BI_cam_rear_south", (2400, 900))}
        times = {}
        for view, (cam, (rx, ry)) in views.items():
            scene.camera = o[cam]
            scene.render.resolution_x, scene.render.resolution_y = rx, ry
            path = render_dir / f"{STEM}_{view}.png"
            if path.exists():
                raise SystemExit(f"refusing to overwrite existing render: {path}")
            scene.render.filepath = str(path)
            ctx = o["CTX_Building_II_mass_from_BII_CS-101_rev6"]
            ctx.hide_render = False
            t0 = time.time()
            bpy.ops.render.render(write_still=True)
            times[view] = round(time.time() - t0, 1)
        report["render_seconds"] = times
        scene.camera = o["BI_cam_landscape_entry"]
        bpy.ops.wm.save_mainfile()
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("BUILD_REPORT=" + json.dumps({k: v for k, v in report.items() if k not in ("plants_kept_at_documented_position", "plants_pushed_in_rebuilt_groups")}))


if __name__ == "__main__":
    main()
