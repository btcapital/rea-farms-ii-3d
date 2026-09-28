r"""Render the v008 footprint validation views from any Building I model (used for the v007 'before' images and for checks).
Adds the v008 plan cameras if the file does not have them (they are not saved). Never overwrites an existing image.

Run:  blender --background --python scripts/Building_I/BI_render_footprint_views_v008.py -- <blend> <out_dir> <prefix> [samples] [view,view,...]
"""
import importlib.util
import sys
import time
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parent.parent.parent
spec = importlib.util.spec_from_file_location("v8", ROOT / "scripts" / "Building_I" / "BI_build_footprint_fix_v008.py")
v8 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v8)
FT = 0.3048


def m(ft):
    return ft * FT


def main():
    argv = sys.argv[sys.argv.index("--") + 1:]
    blend, out_dir, prefix = Path(argv[0]), Path(argv[1]), argv[2]
    samples = int(argv[3]) if len(argv) > 3 else 64
    only = argv[4].split(",") if len(argv) > 4 else None
    out_dir.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.open_mainfile(filepath=str(blend))
    scene = bpy.context.scene
    camcol = bpy.data.collections["90_Cameras"]

    def add_cam(name, loc, target, lens=35.0, ortho=None):
        if name in bpy.data.objects:
            return bpy.data.objects[name]
        c = bpy.data.cameras.new(name); c.lens = lens; c.clip_end = 3000
        if ortho:
            c.type = "ORTHO"; c.ortho_scale = m(ortho)
        o = bpy.data.objects.new(name, c)
        o.location = Vector((m(loc[0]), m(loc[1]), m(loc[2])))
        d = Vector((m(target[0]), m(target[1]), m(target[2]))) - o.location
        o.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
        camcol.objects.link(o)
        return o
    for name, (cx, cy, w) in v8.PLAN_CAMS.items():
        add_cam(name, (cx, cy, 300.0), (cx, cy, 0.0), ortho=w)
    add_cam("BI_cam_oblique_southeast", (470.0, -330.0, 150.0), (150.0, 80.0, 12.0), lens=35.0)
    try:
        prefs = bpy.context.preferences.addons["cycles"].preferences
        prefs.compute_device_type = "OPTIX"; prefs.get_devices()
        for d_ in prefs.devices:
            d_.use = d_.type in ("OPTIX", "CPU")
        scene.cycles.device = "GPU"
    except Exception:  # noqa
        pass
    scene.cycles.samples = samples; scene.cycles.use_denoising = True
    scene.render.image_settings.file_format = "PNG"; scene.view_settings.view_transform = "Standard"
    for view, (cam, (rx, ry)) in v8.VIEWS.items():
        if only and view not in only:
            continue
        scene.camera = bpy.data.objects[cam]
        scene.render.resolution_x, scene.render.resolution_y = rx, ry
        path = out_dir / f"{prefix}_{view}.png"
        if path.exists():
            raise SystemExit(f"refusing to overwrite existing render: {path}")
        scene.render.filepath = str(path)
        t0 = time.time(); bpy.ops.render.render(write_still=True)
        print(f"RENDERED {path.name} {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
