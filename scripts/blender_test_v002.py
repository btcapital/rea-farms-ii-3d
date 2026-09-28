"""Rea Farms 3D: arbitrary cube workflow test, never building geometry.

Run with the Python bundled with Blender (no packages required):
  <Blender folder>/5.2/python/bin/python.exe <this script>
The launcher selects unused versioned paths, captures Blender's full console
output, and writes a report with its actual process exit code. Re-running makes
a new revision, including a copy of this script; existing files are preserved.
"""
from pathlib import Path
import argparse
import datetime
import json
import re
import struct
import subprocess
import sys
import time
import traceback

BLENDER = Path(r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe")
ROOT = Path(__file__).resolve().parent.parent
EXPECTED_ROOT = Path(r"C:\Users\Brandon\OneDrive - Taylor Capital\Shared - Documents\Dormie Equity Partners, LP\11425 Golf Links Drive, LLC\Rea Farms II 3D")
MARKER = "REA_TEST_RESULT="


def paths_for(version):
    stem = f"blender_test_v{version:03d}"
    return {key: ROOT / folder / (stem + suffix) for key, folder, suffix in (
        ("script", "scripts", ".py"), ("blend", "models", ".blend"),
        ("png", "renders", ".png"), ("glb", "exports", ".glb"),
        ("report", "notes", ".md"), ("log", "notes", ".log"))}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def assert_new(path):
    require(not path.exists(), f"Refusing to overwrite: {path}")


def worker(version):
    import bpy
    from mathutils import Vector
    paths = paths_for(version)
    result = {"blender_version": bpy.app.version_string,
              "backend": "not configured", "devices": [], "render_seconds": None,
              "modeling": "not run", "rendering": "not run", "export": "not run",
              "reopen": "not run", "errors": [],
              "paths": {k: str(v) for k, v in paths.items()}}
    try:
        for key in ("blend", "png", "glb", "report"):
            assert_new(paths[key])
        prefs = bpy.context.preferences.addons["cycles"].preferences
        prefs.refresh_devices()
        # Record every detected entry, then disable all of them before selection.
        for device in prefs.devices:
            device.use = False
        result["devices"] = [{"name": d.name, "type": d.type, "id": d.id,
                              "enabled": bool(d.use)} for d in prefs.devices]
        print("DETECTED_DEVICES=" + json.dumps(result["devices"]), flush=True)
        try:
            prefs.compute_device_type = "OPTIX"
        except Exception as exc:
            raise RuntimeError("OptiX is unavailable; no CPU fallback permitted") from exc
        targets = [d for d in prefs.devices if d.type == "OPTIX" and
                   "NVIDIA" in d.name.upper() and "RTX A1000" in d.name.upper()]
        require(bool(targets), "NVIDIA RTX A1000 OptiX device unavailable; stopping")
        for device in targets:
            device.use = True
        result["devices"] = [{"name": d.name, "type": d.type, "id": d.id,
                              "enabled": bool(d.use)} for d in prefs.devices]
        result["backend"] = prefs.compute_device_type
        require(prefs.get_num_gpu_devices() == len(targets), "Enabled GPU count mismatch")
        require(all(not d.use for d in prefs.devices if d.type == "CPU"), "CPU must be disabled")
        print("ENABLED_DEVICES=" + json.dumps(result["devices"]), flush=True)

        bpy.ops.object.select_all(action="SELECT")
        bpy.ops.object.delete(use_global=False)
        scene = bpy.context.scene
        scene.unit_settings.system = "METRIC"
        scene.unit_settings.scale_length = 1.0
        scene.unit_settings.length_unit = "METERS"
        scene.render.engine = "CYCLES"
        scene.cycles.device = "GPU"
        scene.cycles.samples = 32
        scene.cycles.use_adaptive_sampling = False
        scene.cycles.use_denoising = True
        scene.cycles.denoiser = "OPTIX"
        scene.render.resolution_x = 800
        scene.render.resolution_y = 600
        scene.render.resolution_percentage = 100
        scene.render.image_settings.file_format = "PNG"
        scene.render.image_settings.color_mode = "RGBA"
        scene.render.filepath = str(paths["png"])
        scene.render.film_transparent = False
        scene.world.color = (0.18, 0.18, 0.18)

        def material(name, color):
            mat = bpy.data.materials.new(name)
            mat.use_nodes = True
            mat.diffuse_color = (*color, 1)
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            bsdf.inputs["Base Color"].default_value = (*color, 1)
            bsdf.inputs["Roughness"].default_value = 0.55
            return mat

        bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
        cube = bpy.context.object
        cube.name = "TestCube_2m"
        cube["purpose"] = "Arbitrary 2m test cube; not building dimensions"
        cube.data.materials.append(material("Test blue", (0.07, 0.28, 0.52)))
        bpy.ops.mesh.primitive_plane_add(size=12, location=(0, 0, 0))
        ground = bpy.context.object
        ground.name = "TestGround"
        ground.data.materials.append(material("Test ground", (0.38, 0.40, 0.43)))
        bpy.ops.object.camera_add(location=(6, -8, 5.5))
        camera = bpy.context.object
        camera.name = "TestCamera"
        camera.rotation_euler = (Vector((0, 0, 0.9)) - camera.location).to_track_quat("-Z", "Y").to_euler()
        camera.data.lens = 52
        scene.camera = camera
        for name, location, energy, size in (
                ("TestKey", (2, -4, 7), 1200, 5),
                ("TestFill", (-4, -1, 4), 500, 4)):
            bpy.ops.object.light_add(type="AREA", location=location)
            light = bpy.context.object
            light.name = name
            light.data.energy = energy
            light.data.shape = "DISK"
            light.data.size = size
            light.rotation_euler = (Vector((0, 0, 1)) - light.location).to_track_quat("-Z", "Y").to_euler()
        bpy.context.view_layer.update()
        require(all(abs(d - 2) < 1e-6 for d in cube.dimensions), "Initial cube size mismatch")
        result["modeling"] = "passed: 2 x 2 x 2 meter cube, ground, camera, two area lights"
        print("RENDER_CONFIG=" + json.dumps({"engine": scene.render.engine,
              "backend": prefs.compute_device_type, "device": scene.cycles.device,
              "resolution": [800, 600], "samples": 32, "denoising": True,
              "denoiser": scene.cycles.denoiser}), flush=True)
        assert_new(paths["png"])
        render_start = time.perf_counter()
        try:
            bpy.ops.render.render(write_still=True)
        finally:
            result["render_seconds"] = round(time.perf_counter() - render_start, 4)
        require(paths["png"].is_file() and paths["png"].stat().st_size > 0, "PNG missing or empty")
        png = paths["png"].read_bytes()
        require(png[:8] == b"\x89PNG\r\n\x1a\n", "Invalid PNG signature")
        require(struct.unpack(">II", png[16:24]) == (800, 600), "PNG resolution mismatch")
        result["rendering"] = "passed: Cycles GPU/OPTIX, RTX A1000 only, CPU rendering disabled"
        result["render_settings"] = {"resolution": [800, 600], "max_samples": 32,
                                     "denoising": True, "denoiser": "OPTIX"}

        assert_new(paths["blend"])
        bpy.ops.wm.save_as_mainfile(filepath=str(paths["blend"]), check_existing=True)
        bpy.ops.object.select_all(action="DESELECT")
        cube.select_set(True)
        ground.select_set(True)
        bpy.context.view_layer.objects.active = cube
        # Blender's bundled exporter only. No installation or preference save.
        require(hasattr(bpy.ops.export_scene, "gltf"), "Bundled glTF exporter unavailable")
        assert_new(paths["glb"])
        bpy.ops.export_scene.gltf(filepath=str(paths["glb"]), export_format="GLB",
                                  use_selection=True, export_cameras=False,
                                  export_lights=False, export_yup=True)
        require(paths["glb"].is_file() and paths["glb"].stat().st_size > 0, "GLB missing or empty")
        glb = paths["glb"].read_bytes()
        magic, glb_version, total = struct.unpack("<4sII", glb[:12])
        require(magic == b"glTF" and glb_version == 2 and total == len(glb), "Invalid GLB header")
        chunk_size, chunk_type = struct.unpack("<II", glb[12:20])
        require(chunk_type == 0x4E4F534A, "GLB JSON chunk missing")
        document = json.loads(glb[20:20 + chunk_size])
        require(len(document.get("meshes", [])) == 2, "Expected cube and plane in GLB")
        result["export"] = "passed: GLB 2.0, two meshes (cube and ground), header validated"

        bpy.ops.wm.open_mainfile(filepath=str(paths["blend"]), load_ui=False)
        reopened = bpy.data.objects.get("TestCube_2m")
        require(reopened is not None, "Cube missing after reopening blend")
        bpy.context.view_layer.update()
        dimensions = list(reopened.dimensions)
        require(all(abs(d - 2) < 1e-6 for d in dimensions), "Saved cube is not 2m per side")
        require(bpy.context.scene.unit_settings.scale_length == 1, "Saved unit scale mismatch")
        require(bpy.context.scene.cycles.device == "GPU", "Saved scene GPU mode mismatch")
        result["reopened_cube_dimensions_m"] = dimensions
        result["reopen"] = "passed"
        result["output_bytes"] = {key: paths[key].stat().st_size for key in ("blend", "png", "glb")}
        print("REOPENED_CUBE_DIMENSIONS_M=" + json.dumps(dimensions), flush=True)
    except Exception:
        result["errors"].append(traceback.format_exc())
        raise
    finally:
        print(MARKER + json.dumps(result), flush=True)


def launcher():
    require(BLENDER.is_file(), f"Blender missing: {BLENDER}")
    own = Path(__file__).resolve()
    version = int(re.search(r"_v(\d+)\.py$", own.name).group(1))
    while True:
        paths = paths_for(version)
        if not any(p.exists() for k, p in paths.items() if not (k == "script" and p == own)) and not (ROOT / "notes" / f"blender_test_v{version:03d}_runtime").exists():
            break
        version += 1
    if paths["script"] != own:
        with paths["script"].open("x", encoding="utf-8") as output:
            output.write(own.read_text(encoding="utf-8"))
    command = [str(BLENDER), "--background", "--factory-startup", "--disable-autoexec",
               "--debug-cycles", "--python-exit-code", "17", "--python", str(paths["script"]),
               "--", "--worker", "--version", str(version)]
    runtime = ROOT / "notes" / f"blender_test_v{version:03d}_runtime"
    runtime.mkdir(exist_ok=False)
    start = time.perf_counter()
    result = None
    launch_error = None
    # Opening exclusively reserves the revision before the Blender child starts.
    with paths["log"].open("x", encoding="utf-8", buffering=1) as log:
        log.write("UTC: " + datetime.datetime.now(datetime.timezone.utc).isoformat() + "\n")
        log.write("COMMAND: " + subprocess.list2cmdline(command) + "\n")
        try:
            process = subprocess.Popen(command, cwd=str(runtime), stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT, text=True,
                                       encoding="utf-8", errors="replace")
            for line in process.stdout:
                log.write(line)
                if line.startswith(MARKER):
                    result = json.loads(line[len(MARKER):])
                elif any(key in line for key in ("DETECTED_DEVICES=", "ENABLED_DEVICES=", "RENDER_CONFIG=", "REOPENED_CUBE", "Error", "Saved:")):
                    print(line.rstrip(), flush=True)
            exit_code = process.wait()
        except Exception:
            launch_error = traceback.format_exc()
            log.write(launch_error)
            exit_code = -1
        elapsed = time.perf_counter() - start
        log.write(f"\nBLENDER_PROCESS_EXIT_CODE={exit_code}\nPROCESS_SECONDS={elapsed:.4f}\n")
    result = result or {"errors": [launch_error or "Blender exited without a structured result; inspect console log."]}
    lines = ["# Rea Farms 3D - Blender workflow test", "", f"Project: {ROOT}", "",
             "Arbitrary test geometry only. No source documents were accessed or analyzed.", "",
             f"- Blender: {result.get('blender_version', 'unknown')} ({BLENDER})",
             f"- Modeling: {result.get('modeling', 'not completed')}",
             f"- GPU rendering: {result.get('rendering', 'not completed')}",
             f"- Export: {result.get('export', 'not completed')}",
             f"- Reopened saved scene: {result.get('reopen', 'not completed')}",
             f"- Reopened cube dimensions in meters: {result.get('reopened_cube_dimensions_m', 'unavailable')}",
             f"- Rendering backend: {result.get('backend', 'unavailable')}",
             f"- Render settings: {result.get('render_settings', 'not completed')}",
             f"- Render duration (wall time, including initialization and denoising): {result.get('render_seconds')} seconds",
             f"- Blender process exit code: {exit_code}",
             f"- Total Blender process duration: {elapsed:.4f} seconds", "",
             "## Detected and enabled Cycles devices", "",
             "| Device | Backend/type | Enabled | ID |", "| --- | --- | --- | --- |"]
    for device in result.get("devices", []):
        lines.append(f"| {device['name']} | {device['type']} | {device['enabled']} | {device['id']} |")
    lines += ["", "## GPU evidence", "",
              "The log records the detected devices, exclusive RTX A1000 OptiX selection, CPU rendering disabled, GPU scene mode, and Cycles diagnostic output. No CPU fallback is implemented. CPU activity for scene preparation or file export is separate from CPU rendering.", ""]
    log_text = paths["log"].read_text(encoding="utf-8")
    evidence = [line for line in log_text.splitlines() if not line.startswith(MARKER) and
                any(word in line.lower() for word in ("optix", "device_impl", "device.cpp", "using device"))]
    lines += ["```text", *evidence[:60], "```", "", "## Outputs", ""]
    for key, path in paths.items():
        size = f"{path.stat().st_size} bytes" if path.exists() else "this report" if key == "report" else "not created"
        lines.append(f"- {key}: {path} ({size})")
    lines += ["", "## Script exceptions", "", "```text", *(result.get("errors") or ["None"]), "```", "",
              "## Reuse", "", "Run this script with the Python bundled with Blender. It chooses the next unused version across all six outputs and copies itself to that version. It refuses to overwrite outputs.", "", "```powershell",
              f"& '{BLENDER.parent / '5.2/python/bin/python.exe'}' '{paths['script']}'", "```", "",
              "Preferences are changed only in the child process. No global preferences or startup file are saved. The GLB uses Blender's bundled exporter. No add-ons, software, or assets are installed or downloaded.", "",
              "## Single next step", "", "Review the rendered test image. No building modeling has begun."]
    diagnostics = [line for line in log_text.splitlines()
                   if not line.startswith(MARKER) and
                   any(term in line.lower() for term in ("warning", "| error", "traceback"))]
    traced = "Path tracing on: NVIDIA RTX A1000 (OptiX)" in log_text
    denoised = "Denoising on: NVIDIA RTX A1000 (OptiX)" in log_text
    lines += ["", "## Verified GPU execution",
              "", f"- Cycles explicitly names RTX A1000 OptiX for path tracing: {traced}",
              f"- Cycles explicitly names RTX A1000 OptiX for denoising: {denoised}",
              "- GPU evidence: " + ("confirmed" if traced and denoised else "inconclusive"),
              "", "## Console warnings and errors", "", "~~~text",
              *(diagnostics or ["None"]), "~~~", "",
              "Console diagnostics are retained even when Blender exits successfully. A failed thumbnail write concerns Blender's file thumbnail, not the requested render PNG. Detection of unavailable HIP does not affect the selected OptiX backend.",
              "", "## Incidental runtime files", "",
              f"Blender runs in {runtime} so any fallback OptiX cache stays separate from previous runs. No prior cache file is overwritten.",
              "The earlier v001 outputs are preserved. This revision adds complete console diagnostic reporting.",
              "", "## Completion checks", ""]
    for key in ("script", "blend", "png", "glb", "log"):
        lines.append(f"- {key}: exists={paths[key].is_file()}, bytes={paths[key].stat().st_size if paths[key].is_file() else 0}")
    if result.get("rendering", "").startswith("passed") and not (traced and denoised):
        lines.append("- Rendering completed, but GPU execution evidence is inconclusive.")
    with paths["report"].open("x", encoding="utf-8") as report:
        report.write("\n".join(lines) + "\n")
    print(f"BLENDER_PROCESS_EXIT_CODE={exit_code}", flush=True)
    print(f"REPORT={paths['report']}", flush=True)
    return exit_code if 0 <= exit_code <= 255 else 1


if __name__ == "__main__":
    require(ROOT == EXPECTED_ROOT, f"Wrong project folder: {ROOT}; refusing to create files")
    if "--" in sys.argv:
        parser = argparse.ArgumentParser()
        parser.add_argument("--worker", action="store_true")
        parser.add_argument("--version", type=int, required=True)
        args = parser.parse_args(sys.argv[sys.argv.index("--") + 1:])
        require(args.worker, "Worker flag required inside Blender")
        worker(args.version)
    else:
        sys.exit(launcher())
