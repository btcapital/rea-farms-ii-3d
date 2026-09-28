r"""Building I - FINAL EXTERIOR PRESENTATION REALISM baseline v013.

Opens the approved BI_entrance_finish_v012.blend (v010+v011+v012 = controlling exterior + site baseline) and, using
BI_presentation_data_v013.json, rebuilds ONLY the node trees of the existing materials (same names, same slot
assignments), the world (physical sky), colour management / exposure, render settings and the validation cameras.
Every mesh object's world-space vertices, per-face material indices, material slot names, every object transform and
every collection membership are hashed before and after and must be identical (scene_hash).  No geometry, plant, grade,
signage, people, vehicles or interiors.

New shader kinds over v009: "acm" (ACM panel with PVDF/SMP coat and legend-pattern reveal seams as bumps - pattern type
written on A4.02, pitch assumed), "glazing" (opaque low-E placeholder with clear-coat sky reflection and per-lite tone
variation), richer "brick" (three tones, iron-spot speckle, mortar recess), two-scale "ground" (asphalt / concrete / pavers /
lawn / mulch / TPO) and "foliage" with a leaf bump.

Run:  "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --background --python scripts/Building_I/BI_build_presentation_v013.py
Optional:  -- --no-render   |   -- --out <folder>   |   -- --samples N   |   -- --views a,b
Outputs (refuses to overwrite): models/Building_I/BI_presentation_v013.blend, renders/Building_I/BI_presentation_v013_<view>.png,
notes/Building_I/BI_presentation_v013_build_report.json
"""
import hashlib
import json
import math
import sys
import time
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parent.parent.parent
BASE = ROOT / "models" / "Building_I" / "BI_entrance_finish_v012.blend"
DATA = ROOT / "notes" / "Building_I" / "BI_presentation_data_v013.json"
STEM = "BI_presentation_v013"
FT = 0.3048
IN = 0.0254


def m(ft):
    return ft * FT


def scene_hash(exclude=()):
    """Geometry + assignment hash: every mesh's world vertices and face material indices, every material slot name,
    every object's transform and collections, every object's render visibility."""
    h = hashlib.sha256()
    for o in sorted(bpy.data.objects, key=lambda x: x.name):
        if o.name in exclude:
            continue
        h.update(o.name.encode())
        h.update(",".join(f"{v:.5f}" for row in o.matrix_world for v in row).encode())
        h.update("|".join(sorted(c.name for c in o.users_collection)).encode())
        h.update(f"{o.type}{o.hide_render}".encode())
        if o.type == "MESH":
            for v in o.data.vertices:
                w = o.matrix_world @ v.co
                h.update(f"{w.x:.5f},{w.y:.5f},{w.z:.5f};".encode())
            h.update(",".join(str(p.material_index) for p in o.data.polygons).encode())
            h.update("|".join(s.material.name if s.material else "-" for s in o.material_slots).encode())
    return h.hexdigest()


# ------------------------------------------------------------------ node helpers
def fresh(mat):
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return nt, bsdf


def setv(bsdf, name, value):
    if name in bsdf.inputs:
        sock = bsdf.inputs[name]
        if hasattr(sock.default_value, "__len__") and not isinstance(value, (int, float)):
            n = len(sock.default_value)
            sock.default_value = tuple(value)[:n] if len(value) >= n else (*value, 1.0)
        else:
            sock.default_value = value


def base_of(mat):
    """Existing base colour of the material (used when the data says base: null = keep placeholder colour)."""
    if mat.use_nodes and mat.node_tree and "Principled BSDF" in mat.node_tree.nodes:
        return tuple(mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value[:3])
    return (0.6, 0.6, 0.6)


def obj_coords(nt):
    tc = nt.nodes.new("ShaderNodeTexCoord")
    return tc.outputs["Object"]


def wall_uv(nt, vec):
    """(x+y, z) in metres: a stable 2-D coordinate on every axis-aligned wall face (v009 brick convention)."""
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(vec, sep.inputs["Vector"])
    add = nt.nodes.new("ShaderNodeMath")
    add.operation = "ADD"
    nt.links.new(sep.outputs["X"], add.inputs[0])
    nt.links.new(sep.outputs["Y"], add.inputs[1])
    return add.outputs["Value"], sep.outputs["Z"], sep


def noise(nt, vec, scale, detail=3.0, rough=0.5):
    n = nt.nodes.new("ShaderNodeTexNoise")
    n.inputs["Scale"].default_value = scale
    n.inputs["Detail"].default_value = detail
    n.inputs["Roughness"].default_value = rough
    nt.links.new(vec, n.inputs["Vector"])
    return n


def mix_rgb(nt, blend, fac, a, b):
    mx = nt.nodes.new("ShaderNodeMix")
    mx.data_type = "RGBA"
    mx.blend_type = blend
    if hasattr(fac, "links") or hasattr(fac, "default_value"):
        nt.links.new(fac, mx.inputs["Factor"])
    else:
        mx.inputs["Factor"].default_value = fac
    for sock, val in (("A", a), ("B", b)):
        if hasattr(val, "default_value") or hasattr(val, "links"):
            nt.links.new(val, mx.inputs[sock])
        else:
            mx.inputs[sock].default_value = (*val, 1.0)
    return mx


def math_node(nt, op, a, b=None, c=None):
    n = nt.nodes.new("ShaderNodeMath")
    n.operation = op
    for i, v in enumerate((a, b, c)):
        if v is None:
            continue
        if hasattr(v, "links") or hasattr(v, "default_value"):
            nt.links.new(v, n.inputs[i])
        else:
            n.inputs[i].default_value = v
    return n.outputs["Value"]


def bump(nt, height_sock, strength, distance):
    bp = nt.nodes.new("ShaderNodeBump")
    bp.inputs["Strength"].default_value = strength
    bp.inputs["Distance"].default_value = distance
    nt.links.new(height_sock, bp.inputs["Height"])
    return bp


def two_scale_noise(nt, vec, s1, s2, amount, base):
    """base colour modulated by a coarse and a fine noise (mean tone preserved), returns (colour socket, fine-noise fac)"""
    n1 = noise(nt, vec, s1, 4.0, 0.55)
    n2 = noise(nt, vec, s2, 2.0, 0.5)
    mx1 = mix_rgb(nt, "MULTIPLY", amount, base, n1.outputs["Color"])
    mx2 = mix_rgb(nt, "MULTIPLY", amount * 0.6, mx1.outputs["Result"], n2.outputs["Color"])
    g = 1.0 + amount * 0.6 + amount * 0.36     # ~inverse of the two multiplies by ~0.5-grey noise
    gain = mix_rgb(nt, "MULTIPLY", 1.0, mx2.outputs["Result"], (g, g, g))
    return gain.outputs["Result"], n2.outputs["Fac"], n1.outputs["Fac"]


def seam_mask(nt, u, v, pitch_u, pitch_v, width):
    """1 inside a reveal seam, 0 elsewhere; vertical seams every pitch_u (m), optional horizontal every pitch_v"""
    fu = math_node(nt, "MODULO", u, pitch_u)
    fu = math_node(nt, "ABSOLUTE", fu)
    mu = math_node(nt, "LESS_THAN", fu, width)
    if pitch_v and pitch_v > 0:
        fv = math_node(nt, "MODULO", v, pitch_v)
        fv = math_node(nt, "ABSOLUTE", fv)
        mv = math_node(nt, "LESS_THAN", fv, width)
        return math_node(nt, "MAXIMUM", mu, mv)
    return mu


# ------------------------------------------------------------------ material kinds
def mat_painted(mat, p):
    base = tuple(p["base"]) if p.get("base") else base_of(mat)
    nt, b = fresh(mat)
    setv(b, "Base Color", base)
    setv(b, "Roughness", p["rough"])
    setv(b, "Metallic", p.get("metallic", 0.0))
    setv(b, "Specular IOR Level", p.get("spec", 0.5))
    return {"base": [round(c, 3) for c in base], "rough": p["rough"], "metallic": p.get("metallic", 0.0)}


def mat_acm(mat, p):
    base = tuple(p["base"]) if p.get("base") else base_of(mat)
    nt, b = fresh(mat)
    vec = obj_coords(nt)
    u, v, _ = wall_uv(nt, vec)
    # gentle low-frequency tonal variation (panel-to-panel colour and oil-canning read)
    nz = noise(nt, vec, 0.6, 2.0, 0.5)
    col = mix_rgb(nt, "MULTIPLY", p.get("tone_var", 0.03), base, nz.outputs["Color"])
    gain = 1.0 + p.get("tone_var", 0.03) * 0.5
    col = mix_rgb(nt, "MULTIPLY", 1.0, col.outputs["Result"], (gain, gain, gain))
    colour = col.outputs["Result"]
    rec = {"base": list(base), "rough": p["rough"], "coat": p.get("coat", 0.0), "pattern": p.get("pattern", "none")}
    if p.get("pattern", "none") != "none":
        pu = p["pitch_u_ft"] * FT
        pv = p.get("pitch_v_ft", 0.0) * FT if p.get("pattern") == "grid" else 0.0
        w = p["seam_in"] * IN
        mask = seam_mask(nt, u, v, pu, pv, w)
        dark = mix_rgb(nt, "MULTIPLY", 1.0, colour, (p["seam_darken"],) * 3)
        colour = mix_rgb(nt, "MIX", mask, colour, dark.outputs["Result"]).outputs["Result"]
        inv = math_node(nt, "SUBTRACT", 1.0, mask)
        bp = bump(nt, inv, p["seam_depth"], 0.012)
        nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
        rec.update({"seam_pitch_ft": [p["pitch_u_ft"], p.get("pitch_v_ft", 0.0)], "seam_width_in": p["seam_in"]})
    nt.links.new(colour, b.inputs["Base Color"])
    setv(b, "Roughness", p["rough"])
    setv(b, "Metallic", p.get("metallic", 0.0))
    setv(b, "Specular IOR Level", p.get("spec", 0.5))
    setv(b, "Coat Weight", p.get("coat", 0.0))
    setv(b, "Coat Roughness", p.get("coat_rough", 0.1))
    setv(b, "Coat IOR", 1.5)
    return rec


def mat_brick(mat, p):
    nt, b = fresh(mat)
    vec = obj_coords(nt)
    u, v, _ = wall_uv(nt, vec)
    comb = nt.nodes.new("ShaderNodeCombineXYZ")
    nt.links.new(u, comb.inputs["X"])
    nt.links.new(v, comb.inputs["Y"])
    br = nt.nodes.new("ShaderNodeTexBrick")
    br.offset = 0.3333
    br.offset_frequency = 2
    br.squash = 1.0
    br.squash_frequency = 2
    br.inputs["Scale"].default_value = 1.0
    br.inputs["Brick Width"].default_value = 0.3048
    br.inputs["Row Height"].default_value = 0.1016
    br.inputs["Mortar Size"].default_value = 0.0095
    br.inputs["Mortar Smooth"].default_value = 0.12
    br.inputs["Bias"].default_value = 0.0
    br.inputs["Color1"].default_value = (*p["brick1"], 1.0)
    br.inputs["Color2"].default_value = (*p["brick2"], 1.0)
    br.inputs["Mortar"].default_value = (*p["mortar"], 1.0)
    nt.links.new(comb.outputs["Vector"], br.inputs["Vector"])
    # third tone: per-brick blotch from a low-frequency noise sampled on the brick grid
    nz3 = noise(nt, vec, 1.2, 2.0, 0.5)
    col3 = mix_rgb(nt, "MIX", 0.5, br.outputs["Color"], tuple(p.get("brick3", p["brick1"])))
    blotch = mix_rgb(nt, "MIX", nz3.outputs["Fac"], br.outputs["Color"], col3.outputs["Result"])
    # keep the mortar colour where the brick node says mortar
    keep_mortar = mix_rgb(nt, "MIX", br.outputs["Fac"], blotch.outputs["Result"], tuple(p["mortar"]))
    nz = noise(nt, vec, 3.0, 4.0, 0.6)
    mottle = mix_rgb(nt, "MULTIPLY", p["mottle"], keep_mortar.outputs["Result"], nz.outputs["Color"])
    spot = noise(nt, vec, 90.0, 1.0, 0.4)                   # iron-spot speckle
    spotted = mix_rgb(nt, "MULTIPLY", p.get("ironspot", 0.15), mottle.outputs["Result"], spot.outputs["Color"])
    g = 1.0 + p["mottle"] * 0.5 + p.get("ironspot", 0.15) * 0.5
    gain = mix_rgb(nt, "MULTIPLY", 1.0, spotted.outputs["Result"], (g, g, g))
    nt.links.new(gain.outputs["Result"], b.inputs["Base Color"])
    rough = nt.nodes.new("ShaderNodeMapRange")
    rough.inputs["To Min"].default_value = p["rough_brick"]
    rough.inputs["To Max"].default_value = p["rough_mortar"]
    nt.links.new(br.outputs["Fac"], rough.inputs["Value"])
    nt.links.new(rough.outputs["Result"], b.inputs["Roughness"])
    inv = math_node(nt, "SUBTRACT", 1.0, br.outputs["Fac"])
    fine = math_node(nt, "MULTIPLY_ADD", spot.outputs["Fac"], 0.15, inv)
    bp = bump(nt, fine, p["bump"], p.get("mortar_depth_m", 0.006))
    nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    setv(b, "Specular IOR Level", 0.4)
    return {"module_m": [0.3048, 0.1016, 0.0095], "brick1": p["brick1"], "brick2": p["brick2"], "brick3": p.get("brick3"), "mortar": p["mortar"], "rough": [p["rough_brick"], p["rough_mortar"]]}


def mat_ground(mat, p):
    base = tuple(p["base"]) if p.get("base") else base_of(mat)
    nt, b = fresh(mat)
    vec = obj_coords(nt)
    colour, fine, coarse = two_scale_noise(nt, vec, p["noise_scale"], p.get("noise_scale2", p["noise_scale"] * 10), p["noise_amount"], base)
    nt.links.new(colour, b.inputs["Base Color"])
    setv(b, "Roughness", p["rough"])
    setv(b, "Specular IOR Level", 0.3)
    if p.get("bump", 0) > 0:
        h = math_node(nt, "MULTIPLY_ADD", coarse, 0.5, fine)
        bp = bump(nt, h, p["bump"] * 10, 0.01)
        nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    return {"base": [round(c, 3) for c in base], "rough": p["rough"], "noise": [p["noise_scale"], p.get("noise_scale2")]}


def mat_translucent(mat, p):
    nt, b = fresh(mat)
    vec = obj_coords(nt)
    nz = noise(nt, vec, 0.8, 2.0, 0.5)
    col = mix_rgb(nt, "MULTIPLY", p.get("tone_var", 0.03), tuple(p["base"]), nz.outputs["Color"])
    g = 1.0 + p.get("tone_var", 0.03) * 0.5
    col = mix_rgb(nt, "MULTIPLY", 1.0, col.outputs["Result"], (g, g, g))
    nt.links.new(col.outputs["Result"], b.inputs["Base Color"])
    setv(b, "Roughness", p["rough"])
    setv(b, "Transmission Weight", p["transmission"])
    setv(b, "IOR", 1.45)
    setv(b, "Alpha", 1.0)
    return {"base": p["base"], "transmission": p["transmission"], "rough": p["rough"]}


def mat_glazing(mat, p):
    nt, b = fresh(mat)
    info = nt.nodes.new("ShaderNodeObjectInfo")
    var = nt.nodes.new("ShaderNodeMapRange")
    var.inputs["To Min"].default_value = 1.0 - p["lite_var"] / 2
    var.inputs["To Max"].default_value = 1.0 + p["lite_var"] / 2
    nt.links.new(info.outputs["Random"], var.inputs["Value"])
    hsv = nt.nodes.new("ShaderNodeHueSaturation")
    hsv.inputs["Color"].default_value = (*p["base"], 1.0)
    nt.links.new(var.outputs["Result"], hsv.inputs["Value"])
    nt.links.new(hsv.outputs["Color"], b.inputs["Base Color"])
    setv(b, "Roughness", p["rough"])
    setv(b, "Specular IOR Level", p.get("spec", 0.5))
    setv(b, "IOR", 1.5)
    setv(b, "Metallic", 0.0)
    setv(b, "Coat Weight", p.get("coat", 0.5))
    setv(b, "Coat Roughness", p.get("coat_rough", 0.03))
    setv(b, "Coat IOR", 1.52)
    setv(b, "Coat Tint", tuple(p.get("coat_tint", (1, 1, 1))))
    return {"base": p["base"], "rough": p["rough"], "coat": p.get("coat"), "lite_var": p["lite_var"]}


def mat_clear_glass(mat, p):
    nt, b = fresh(mat)
    setv(b, "Base Color", tuple(p["base"]))
    setv(b, "Roughness", p["rough"])
    setv(b, "Transmission Weight", 1.0)
    setv(b, "IOR", p["ior"])
    return {"base": p["base"], "ior": p["ior"]}


def mat_foliage(mat, p):
    base = tuple(p["base"]) if p.get("base") else base_of(mat)
    nt, b = fresh(mat)
    info = nt.nodes.new("ShaderNodeObjectInfo")
    hsv = nt.nodes.new("ShaderNodeHueSaturation")
    hsv.inputs["Color"].default_value = (*base, 1.0)
    hue = nt.nodes.new("ShaderNodeMapRange")
    hue.inputs["To Min"].default_value = 0.5 - p["hue_var"] / 2
    hue.inputs["To Max"].default_value = 0.5 + p["hue_var"] / 2
    nt.links.new(info.outputs["Random"], hue.inputs["Value"])
    nt.links.new(hue.outputs["Result"], hsv.inputs["Hue"])
    val = nt.nodes.new("ShaderNodeMapRange")
    val.inputs["To Min"].default_value = 1.0 - p["val_var"] / 2
    val.inputs["To Max"].default_value = 1.0 + p["val_var"] / 2
    nt.links.new(info.outputs["Random"], val.inputs["Value"])
    nt.links.new(val.outputs["Result"], hsv.inputs["Value"])
    vec = obj_coords(nt)
    nz = noise(nt, vec, 12.0, 3.0, 0.5)
    mx = mix_rgb(nt, "MULTIPLY", 0.3, hsv.outputs["Color"], nz.outputs["Color"])
    gain = mix_rgb(nt, "MULTIPLY", 1.0, mx.outputs["Result"], (1.18, 1.18, 1.18))
    nt.links.new(gain.outputs["Result"], b.inputs["Base Color"])
    leaf = noise(nt, vec, p.get("leaf_scale", 18.0), 4.0, 0.6)
    bp = bump(nt, leaf.outputs["Fac"], p.get("leaf_bump", 0.3), 0.03)
    nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    setv(b, "Roughness", p["rough"])
    setv(b, "Specular IOR Level", p.get("spec", 0.3))
    setv(b, "Subsurface Weight", p["sss"])
    setv(b, "Subsurface Radius", (0.2, 0.4, 0.1))
    setv(b, "Subsurface Scale", 0.02)
    return {"base": [round(c, 3) for c in base], "hue_var": p["hue_var"], "val_var": p["val_var"], "sss": p["sss"], "leaf_bump": p.get("leaf_bump")}


def mat_bark(mat, p):
    nt, b = fresh(mat)
    vec = obj_coords(nt)
    nz = noise(nt, vec, 20.0, 5.0, 0.6)
    mx = mix_rgb(nt, "MULTIPLY", 0.4, tuple(p["base"]), nz.outputs["Color"])
    gain = mix_rgb(nt, "MULTIPLY", 1.0, mx.outputs["Result"], (1.24, 1.24, 1.24))
    nt.links.new(gain.outputs["Result"], b.inputs["Base Color"])
    setv(b, "Roughness", p["rough"])
    setv(b, "Specular IOR Level", 0.2)
    bp = bump(nt, nz.outputs["Fac"], p["bump"] * 10, 0.02)
    nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    return {"base": p["base"], "rough": p["rough"]}


KINDS = {"painted": mat_painted, "acm": mat_acm, "brick": mat_brick, "ground": mat_ground, "translucent": mat_translucent,
         "glazing": mat_glazing, "clear_glass": mat_clear_glass, "foliage": mat_foliage, "bark": mat_bark}


def build_world(scene, S):
    world = scene.world
    world.use_nodes = True
    wnt = world.node_tree
    for n in list(wnt.nodes):
        wnt.nodes.remove(n)
    wout = wnt.nodes.new("ShaderNodeOutputWorld")
    bg = wnt.nodes.new("ShaderNodeBackground")
    bg.inputs["Strength"].default_value = S["strength"]
    sky = wnt.nodes.new("ShaderNodeTexSky")
    sky.sky_type = S["type"]
    sky.sun_disc = S["sun_disc"]
    sky.sun_intensity = S["sun_intensity"]
    sky.sun_elevation = math.radians(S["sun_elevation_deg"])
    sky.sun_rotation = math.radians(S["sun_rotation_deg"])
    sky.altitude = S["altitude_m"]
    sky.air_density = S["air_density"]
    sky.aerosol_density = S["aerosol_density"]
    sky.ozone_density = S["ozone_density"]
    wnt.links.new(sky.outputs["Color"], bg.inputs["Color"])
    gnd = S.get("ground_below_horizon")
    if gnd:
        tc = wnt.nodes.new("ShaderNodeTexCoord")
        sep = wnt.nodes.new("ShaderNodeSeparateXYZ")
        wnt.links.new(tc.outputs["Generated"], sep.inputs["Vector"])
        below = wnt.nodes.new("ShaderNodeMath")
        below.operation = "LESS_THAN"
        below.inputs[1].default_value = 0.0
        wnt.links.new(sep.outputs["Z"], below.inputs[0])
        gbg = wnt.nodes.new("ShaderNodeBackground")
        gbg.inputs["Color"].default_value = (*gnd["color"], 1.0)
        gbg.inputs["Strength"].default_value = gnd["strength"]
        mixs = wnt.nodes.new("ShaderNodeMixShader")
        wnt.links.new(below.outputs["Value"], mixs.inputs["Fac"])
        wnt.links.new(bg.outputs["Background"], mixs.inputs[1])
        wnt.links.new(gbg.outputs["Background"], mixs.inputs[2])
        wnt.links.new(mixs.outputs["Shader"], wout.inputs["Surface"])
    else:
        wnt.links.new(bg.outputs["Background"], wout.inputs["Surface"])


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
    D = json.loads(DATA.read_text(encoding="utf-8"))
    samples = int(argv[argv.index("--samples") + 1]) if "--samples" in argv else D["render"]["samples"]
    only = argv[argv.index("--views") + 1].split(",") if "--views" in argv else None

    bpy.ops.wm.open_mainfile(filepath=str(BASE))
    scene = bpy.context.scene
    objs = bpy.data.objects
    n_obj_before = len(objs)
    h_before = scene_hash()
    mat_names_before = sorted(mt.name for mt in bpy.data.materials)
    users_before = {mt.name: mt.users for mt in bpy.data.materials}

    # ---- materials: node trees rebuilt in place (names and assignments untouched)
    applied = {}
    missing = []
    for name, p in D["materials"].items():
        mt = bpy.data.materials.get(name)
        if mt is None:
            missing.append(name)
            continue
        applied[name] = {"kind": p["kind"], "conf": p.get("conf"), **KINDS[p["kind"]](mt, p)}
    assert not missing, f"materials not found in v012: {missing}"
    untouched = sorted(n for n in mat_names_before if n not in applied)
    assert sorted(mt.name for mt in bpy.data.materials) == mat_names_before
    assert {mt.name: mt.users for mt in bpy.data.materials} == users_before

    # ---- world, colour management, render settings
    S = D["sky"]
    build_world(scene, S)
    sun = objs.get("BI_sun")
    if sun:
        sun.hide_render = True
    V, R = D["view"], D["render"]
    scene.render.engine = R["engine"]
    scene.view_settings.view_transform = V["transform"]
    scene.view_settings.look = V["look"]
    scene.view_settings.exposure = V["exposure"]
    scene.view_settings.gamma = V["gamma"]
    scene.cycles.samples = samples
    scene.cycles.use_adaptive_sampling = True
    scene.cycles.adaptive_threshold = R.get("adaptive_threshold", 0.01)
    scene.cycles.use_denoising = R["denoise"]
    try:
        scene.cycles.denoiser = R.get("denoiser", "OPTIX")
    except TypeError:
        pass
    scene.cycles.caustics_reflective = R["caustics"]
    scene.cycles.caustics_refractive = R["caustics"]
    scene.cycles.sample_clamp_indirect = R["clamp_indirect"]
    scene.cycles.use_light_tree = R.get("light_tree", True)
    scene.render.use_persistent_data = R["persistent_data"]
    scene.render.filter_size = R["filter_px"]
    scene.render.use_motion_blur = False
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_depth = "8"

    # ---- smooth shading flags (presentation setting only; vertices untouched) - same rule as v009
    smoothed = 0
    for o in objs:
        if o.type != "MESH":
            continue
        if o.name.startswith(tuple(D["shade_smooth"]["all_faces_prefixes"])):
            for pg in o.data.polygons:
                pg.use_smooth = True
            smoothed += 1
        elif o.name.startswith(tuple(D["shade_smooth"]["top_faces_prefixes"])):
            for pg in o.data.polygons:
                pg.use_smooth = pg.normal.z > 0.5
            smoothed += 1

    # ---- cameras
    camcol = bpy.data.collections["90_Cameras"]
    for name, c in D["cameras_new"].items():
        assert name not in objs, name
        cam = bpy.data.cameras.new(name)
        cam.lens = c["lens"]
        cam.clip_end = 3000
        cam.dof.use_dof = False
        o = bpy.data.objects.new(name, cam)
        o.location = Vector((m(c["loc"][0]), m(c["loc"][1]), m(c["loc"][2])))
        d = Vector((m(c["target"][0]), m(c["target"][1]), m(c["target"][2]))) - o.location
        o.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
        camcol.objects.link(o)
    for o in objs:
        if o.type == "CAMERA":
            o.data.dof.use_dof = False

    # ---- verification: nothing but materials / world / settings / new cameras changed
    h_after = scene_hash(exclude=set(D["cameras_new"]))
    assert h_before == h_after, "geometry, transforms, collections, visibility or material assignments changed - aborting"
    assert len(objs) == n_obj_before + len(D["cameras_new"]), "unexpected object count"
    report = {"version": "v013", "base": str(BASE), "scene_hash_geometry_and_assignments": h_before, "geometry_unchanged": True,
              "objects_before": n_obj_before, "objects_after": len(objs), "objects_added": list(D["cameras_new"]),
              "materials_refined": applied, "materials_untouched": untouched, "sky": S, "view": V,
              "render": {**R, "samples": samples}, "sun_lamp_hidden_for_render": bool(sun), "objects_shade_smooth": smoothed}
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
        ctx_bii = [o for o in objs if o.name.startswith("CTX_") and "II" in o.name]
        times = {}
        for view, (cam, (rx, ry)) in D["views"].items():
            if only and view not in only:
                continue
            for o in ctx_bii:      # the Building II context mass is hidden in the photo-match view only (the July 2026 photo predates it)
                o.hide_render = view in D.get("views_hide_building_ii_mass", [])
            scene.camera = objs[cam]
            scene.render.resolution_x, scene.render.resolution_y = rx, ry
            scene.render.resolution_percentage = 100
            path = render_dir / f"{STEM}_{view}.png"
            if path.exists():
                raise SystemExit(f"refusing to overwrite existing render: {path}")
            scene.render.filepath = str(path)
            t0 = time.time()
            bpy.ops.render.render(write_still=True)
            times[view] = round(time.time() - t0, 1)
        for o in ctx_bii:
            o.hide_render = False
        report["render_seconds"] = times
        scene.camera = objs["BI_cam_hero_porte_cochere"]
        bpy.ops.wm.save_mainfile()
        assert scene_hash(exclude=set(D["cameras_new"])) == h_before, "hash changed during rendering"
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("BUILD_REPORT=" + json.dumps({k: v for k, v in report.items() if k != "materials_refined"}))


if __name__ == "__main__":
    main()
