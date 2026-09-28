"""Rea Farms II 3D - v018: viewer DATA export (no geometry export).

Reads models/building_shell_v015.blend read-only (never saved) to build the Level 2 walk grid from the approved Level 2
base-building geometry, and restructures the approved v016 viewer data (Level 1 grid, rooms, viewpoints, underlay - copied
unchanged) into a multi-concept layout for viewer_v018. The GLB is NOT re-exported: viewer_v018 uses a byte-identical copy
of exports/building_II_CNSA_ASC_v016.glb.

Writes (refuses to overwrite):  viewer_v018/assets/viewer_data_v018.json
Run (Blender 5.2):  blender --background --python scripts/export_viewer_data_v018.py
"""
import hashlib
import json
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "models" / "building_shell_v015.blend"
V016 = ROOT / "viewer" / "assets" / "viewer_data_v016.json"
OUT = ROOT / "viewer_v018" / "assets" / "viewer_data_v018.json"
FT = 0.3048
L2_FF = 16.0                      # W: Level 02 finish floor 16'-0"
WALK_LOW, WALK_HIGH = 0.5, 6.5    # same blocking band as v016 (feet above the floor)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def bbox_ft(obj):
    pts = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    return [min(p[i] for p in pts) / FT for i in range(3)], [max(p[i] for p in pts) / FT for i in range(3)]


def rle_rows(blocked, nx, ny):
    rows = []
    for j in range(ny):
        runs, cur, n = [], 0, 0
        for i in range(nx):
            v = blocked[j * nx + i]
            if v == cur:
                n += 1
            else:
                runs.append(n)
                cur, n = v, 1
        runs.append(n)
        rows.append(runs)
    return rows


def main():
    if OUT.exists():
        raise SystemExit(f"Refusing to overwrite existing file: {OUT}")
    v16 = json.loads(V016.read_text(encoding="utf-8"))
    g1 = v16["walk_grid"]
    cell, x0, y0, nx, ny = g1["cell_ft"], g1["x0_ft"], g1["y0_ft"], g1["nx"], g1["ny"]
    src_hash = sha256(SRC)
    assert src_hash == v16["source_model_sha256"], "v015 model differs from the one v016 was exported from"
    bpy.ops.wm.open_mainfile(filepath=str(SRC))

    # ---- Level 2 floor: cells under an upward face of the approved Level 2 slab at 16'-0" ----
    has_floor = bytearray(nx * ny)
    slab = bpy.data.objects["INT_L2_slab"]
    floor_faces = 0
    for poly in slab.data.polygons:
        n = slab.matrix_world.to_3x3() @ poly.normal
        if n.z < 0.9:
            continue
        pts = [slab.matrix_world @ slab.data.vertices[i].co for i in poly.vertices]
        if abs(pts[0].z / FT - L2_FF) > 0.01:
            continue
        floor_faces += 1
        fx0, fx1 = min(p.x for p in pts) / FT, max(p.x for p in pts) / FT
        fy0, fy1 = min(p.y for p in pts) / FT, max(p.y for p in pts) / FT
        for j in range(max(0, int((fy0 - y0) / cell)), min(ny - 1, int((fy1 - y0) / cell)) + 1):
            cy = y0 + (j + 0.5) * cell
            if not (fy0 <= cy <= fy1):
                continue
            for i in range(max(0, int((fx0 - x0) / cell)), min(nx - 1, int((fx1 - x0) / cell)) + 1):
                cx = x0 + (i + 0.5) * cell
                if fx0 <= cx <= fx1:
                    has_floor[j * nx + i] = 1

    # ---- Level 2 blockers: any base-building or tenant solid between 16.5 ft and 22.5 ft (same rule as Level 1, shifted up) ----
    blocked = bytearray(1 if not has_floor[k] else 0 for k in range(nx * ny))
    blockers = []
    for o in bpy.data.objects:
        if o.type != "MESH" or not (o.name.startswith("INT_") or o.name.startswith("TEN_")):
            continue
        low = o.name.lower()
        if "slab" in low or "ceiling" in low or "future_room" in low or "roof_deck" in low or "underlay" in low:
            continue
        lo, hi = bbox_ft(o)
        if hi[2] <= L2_FF + WALK_LOW or lo[2] >= L2_FF + WALK_HIGH:
            continue
        blockers.append(o.name)
        i0, i1 = int((lo[0] - x0) / cell), int((hi[0] - x0) / cell)
        j0, j1 = int((lo[1] - y0) / cell), int((hi[1] - y0) / cell)
        for j in range(max(0, j0), min(ny - 1, j1) + 1):
            for i in range(max(0, i0), min(nx - 1, i1) + 1):
                blocked[j * nx + i] = 1
    open_cells = nx * ny - sum(blocked)

    grid2 = {"cell_ft": cell, "x0_ft": x0, "y0_ft": y0, "nx": nx, "ny": ny, "floor_z_ft": L2_FF, "floor_faces": floor_faces,
             "blocking_objects": len(blockers), "open_cells": open_cells, "encoding": g1["encoding"],
             "rule": "open = under an upward face of the approved Level 2 slab (INT_L2_slab, 16 ft 0 in.) and no base-building or tenant "
                     "solid between 16.5 ft and 22.5 ft; voids (lobby open-to-below, stair well, hoistway, shafts) have no floor; no openings were added",
             "rows": rle_rows(blocked, nx, ny)}
    grid1 = dict(g1, floor_z_ft=0.0)

    concept = v16["concept"]
    data = {"version": "v018", "source_model": v16["source_model"], "source_model_sha256": src_hash, "glb": v16["glb"], "glb_bytes": v16["glb_bytes"],
            "units": v16["units"], "groups": v16["groups"], "eye_height_ft": 5.5,
            "walk": {"normal_ft_per_s": 9.0, "fast_ft_per_s": 18.0, "substep_ft": 0.2, "note": "approved v017 values"},
            "floors": {"L1": {"label": "Level 1", "floor_z_ft": 0.0, "grid": "level1", "default_walk_ft": [129.9, 79.0], "default_forward": [0.0, -1.0, 0.0]},
                       "L2": {"label": "Level 2", "floor_z_ft": L2_FF, "grid": "level2", "default_walk_ft": [118.0, 69.0], "default_forward": [0.0, 1.0, 0.0]}},
            "walk_grids": {"level1": grid1, "level2": grid2},
            "concepts": [{"id": concept["id"], "label": "CNSA ASC — Concept A", "tenant": concept["tenant"], "group": "GRP_Concept_A_CNSA_ASC",
                          "floor": "L1", "source": concept["source"], "areas": concept["areas"], "warning": concept["warning"],
                          "viewpoints": [dict(v, floor="L1") for v in v16["viewpoints"]], "rooms": v16["rooms"], "underlay": v16["underlay"]}],
            "concept_architecture": "Each entry in 'concepts' carries its own GLB group node, floor, rooms, viewpoints, underlay and warning. "
                                    "A future Concept B / C or another tenant is one more entry (and its group in a future GLB); nothing is fabricated here."}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, separators=(",", ":")), encoding="utf-8")
    assert sha256(SRC) == src_hash
    print("DATA_REPORT=" + json.dumps({"level2_floor_faces": floor_faces, "level2_blockers": len(blockers), "level2_open_cells": open_cells,
                                       "level1_open_cells": g1["open_cells"], "blockers_sample": sorted(blockers)[:12]}))


if __name__ == "__main__":
    main()
