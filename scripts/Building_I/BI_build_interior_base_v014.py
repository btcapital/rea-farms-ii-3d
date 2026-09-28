r"""Building I v014 - INTERIOR BASE-BUILDING framework.

Opens the approved BI_presentation_v013.blend read-only (every existing object, transform, collection membership, render
flag and material node tree is hashed before and after and must be identical) and ADDS, under a new collection tree

    Building_I
      BASE_BUILDING          (slabs, columns, exterior-wall inner faces + window reveals, core walls, stairs, elevator,
                              FMK-documented program partitions, roof-deck underside plates)
      EXISTING_TENANT / CNSA (tenant partitions and tenant zone plates from the CNSA A100 plan - black lines only)
      FUTURE_CONCEPTS / Concept_A, Concept_B, Concept_C   (empty)

from notes/Building_I/BI_interior_base_data_v014.json.  Nothing exterior is moved or edited.

Interior validation renders hide the exterior shell prisms, parapet screens and facade regions at COLLECTION level for the
duration of the render only (restored before saving; the object-level flags are part of the hash).  The shell prisms are
solids, so from inside the envelope the modeled "inner faces" (BB_extwall_inner_*) and the roof-deck plates stand in for
the inside of the exterior walls and the roof.

Run:  "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --background --python scripts/Building_I/BI_build_interior_base_v014.py
Optional:  -- --no-render   |   -- --out <folder>   |   -- --samples N   |   -- --views a,b
Outputs (refuse to overwrite): models/Building_I/BI_interior_base_v014.blend, renders/Building_I/BI_interior_base_v014_<view>.png,
notes/Building_I/BI_interior_base_v014_build_report.json, notes/Building_I/BI_interior_base_viewer_v014.json
"""
import hashlib
import importlib.util
import json
import math
import sys
import time
from pathlib import Path

import bmesh
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parent.parent.parent
BASE = ROOT / "models" / "Building_I" / "BI_presentation_v013.blend"
DATA = ROOT / "notes" / "Building_I" / "BI_interior_base_data_v014.json"
REGIONS = ROOT / "notes" / "Building_I" / "BI_facade_regions_v008.json"
STEM = "BI_interior_base_v014"
FT = 0.3048


def m(ft):
    return ft * FT


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / "Building_I" / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


v5 = _load("v5", "BI_build_facade_cleanup_v005.py")     # rects_minus, clip_poly


# ------------------------------------------------------------------ verification helpers
def snapshot():
    """per-object hash of geometry, transform, collections, render flags, material slots + material node signatures"""
    geo = {}
    for o in bpy.data.objects:
        h = hashlib.sha256()
        h.update(",".join(f"{v:.5f}" for row in o.matrix_world for v in row).encode())
        h.update("|".join(sorted(c.name for c in o.users_collection)).encode())
        h.update(f"{o.type}{o.hide_render}{o.hide_viewport}".encode())
        if o.type == "MESH":
            for v in o.data.vertices:
                w = o.matrix_world @ v.co
                h.update(f"{w.x:.5f},{w.y:.5f},{w.z:.5f};".encode())
            h.update(",".join(str(p.material_index) for p in o.data.polygons).encode())
            h.update("|".join(s.material.name if s.material else "-" for s in o.material_slots).encode())
        geo[o.name] = h.hexdigest()
    mats = {}
    for mt in bpy.data.materials:
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
        mats[mt.name] = h.hexdigest()
    cols = {c.name: (c.hide_render, c.hide_viewport, sorted(ch.name for ch in c.children)) for c in bpy.data.collections}
    return geo, mats, cols


# ------------------------------------------------------------------ geometry helpers
def new_mat(name, rgb, rough=0.7, metallic=0.0, emission=0.0):
    mt = bpy.data.materials.new(name)
    mt.use_nodes = True
    b = mt.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1.0)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metallic
    if emission > 0:
        b.inputs["Emission Color"].default_value = (*rgb, 1.0)
        b.inputs["Emission Strength"].default_value = emission
    mt.diffuse_color = (*rgb, 1.0)          # Workbench colour for the technical (cutaway / section) views
    return mt


def new_obj(name, bm, col, mat, props=None):
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    o = bpy.data.objects.new(name, mesh)
    if mat is not None:
        o.data.materials.append(mat)
    col.objects.link(o)
    for k, v in (props or {}).items():
        o[k] = v
    return o


def box_bm(bm, x0, x1, y0, y1, z0, z1):
    vs = [bm.verts.new((m(x), m(y), m(z))) for z in (z0, z1) for y in (y0, y1) for x in (x0, x1)]
    # vs order: z0:(y0:x0,x1) (y1:x0,x1) ; z1 same
    f = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    for a, b, c, d in f:
        bm.faces.new((vs[a], vs[b], vs[c], vs[d]))
    return bm


def box(name, x0, x1, y0, y1, z0, z1, col, mat, props=None):
    bm = bmesh.new()
    box_bm(bm, x0, x1, y0, y1, z0, z1)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return new_obj(name, bm, col, mat, props)


def boxes(name, rects, z0, z1, col, mat, props=None):
    """many axis-aligned boxes in ONE object (rects = (x0,x1,y0,y1))"""
    bm = bmesh.new()
    for x0, x1, y0, y1 in rects:
        box_bm(bm, x0, x1, y0, y1, z0, z1)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return new_obj(name, bm, col, mat, props)


def prism(name, poly, z0, z1, col, mat, props=None):
    bm = bmesh.new()
    vs = [bm.verts.new((m(x), m(y), m(z0))) for x, y in poly]
    f = bm.faces.new(vs)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    if f.normal.z > 0:
        f.normal_flip()
    r = bmesh.ops.extrude_face_region(bm, geom=[f])
    for v in [g for g in r["geom"] if isinstance(g, bmesh.types.BMVert)]:
        v.co.z = m(z1)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return new_obj(name, bm, col, mat, props)


def union_into(name, objs, col, mat, props=None):
    """exact boolean union of a list of temporary objects -> one object (temps removed)"""
    base = objs[0]
    for o in objs[1:]:
        md = base.modifiers.new("u", "BOOLEAN")
        md.operation = "UNION"
        md.object = o
        md.solver = "EXACT"
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(base.evaluated_get(dg))
    for o in objs:
        d = o.data
        bpy.data.objects.remove(o, do_unlink=True)
        bpy.data.meshes.remove(d)
    o = bpy.data.objects.new(name, me)
    if mat is not None:
        me.materials.clear()
        me.materials.append(mat)
    col.objects.link(o)
    for k, v in (props or {}).items():
        o[k] = v
    return o


def poly_area(pts):
    return abs(sum(pts[i - 1][0] * pts[i][1] - pts[i][0] * pts[i - 1][1] for i in range(len(pts)))) / 2


def roof_tos(x, y, zone):
    """top-of-steel elevation (ft) at (x,y) for the zone that owns the point (written datums, linear between them)"""
    if zone == "wing":
        return 30.0 + max(0.0, min(y, 70.583)) * (1.5 / 70.583)
    if zone == "band":
        return 31.5
    if zone == "end_block":
        return 28.0
    if zone == "north":
        return 31.5 + max(0.0, y - 70.583) * (5.7917 / 127.945)
    if zone == "bay":
        return 27.333
    if zone == "vestibule":
        return 9.0
    return 30.0


def zone_of(x, y):
    if 38.25 <= x <= 62.25 and 74.54 <= y <= 83.58:
        return "vestibule"
    if 28.5 <= x <= 71.0 and 54.2 <= y <= 74.38:
        return "band"
    if x >= 271.29 and 44.21 <= y <= 97.75:
        return "end_block"
    if y >= 70.583 and x >= 71.0:
        return "north"
    if y < -1.46:
        return "bay"
    return "wing"


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
    VIEWER = note_dir / "BI_interior_base_viewer_v014.json"
    for p in (BLEND, REPORT, VIEWER):
        if p.exists():
            raise SystemExit(f"refusing to overwrite existing file: {p}")
    D = json.loads(DATA.read_text(encoding="utf-8"))
    R = json.loads(REGIONS.read_text(encoding="utf-8"))
    samples = int(argv[argv.index("--samples") + 1]) if "--samples" in argv else 256
    only = argv[argv.index("--views") + 1].split(",") if "--views" in argv else None

    bpy.ops.wm.open_mainfile(filepath=str(BASE))
    scene = bpy.context.scene
    objs = bpy.data.objects
    geo0, mats0, cols0 = snapshot()
    names0 = set(o.name for o in objs)
    report = {"version": "v014", "base": str(BASE), "objects_before": len(objs), "materials_before": len(bpy.data.materials)}

    # ---------------------------------------------------------------- collections
    root = bpy.data.collections.new("Building_I")
    scene.collection.children.link(root)
    BB = bpy.data.collections.new("BASE_BUILDING"); root.children.link(BB)
    ET = bpy.data.collections.new("EXISTING_TENANT"); root.children.link(ET)
    FC = bpy.data.collections.new("FUTURE_CONCEPTS"); root.children.link(FC)
    CN = bpy.data.collections.new("CNSA"); ET.children.link(CN)
    for cname in ("Concept_A", "Concept_B", "Concept_C"):
        FC.children.link(bpy.data.collections.new(cname))
    sub = {}
    for cname in ("BB_10_slabs", "BB_11_columns", "BB_12_exterior_wall_inner_faces", "BB_13_core_walls", "BB_14_stairs", "BB_15_elevator", "BB_16_fmk_program_partitions", "BB_17_roof_deck_underside"):
        sub[cname] = bpy.data.collections.new(cname); BB.children.link(sub[cname])
    for cname in ("CNSA_L1_partitions", "CNSA_L2_partitions", "CNSA_tenant_zones"):
        sub[cname] = bpy.data.collections.new(cname); CN.children.link(sub[cname])

    # ---------------------------------------------------------------- materials (new only)
    MAT = {"conc": new_mat("BB_concrete_slab", (0.55, 0.54, 0.52), 0.85), "steel": new_mat("BB_steel_structure", (0.32, 0.33, 0.35), 0.5, 0.6),
           "gwb": new_mat("BB_gwb_partition", (0.86, 0.85, 0.82), 0.8), "shaft": new_mat("BB_shaft_wall", (0.72, 0.71, 0.69), 0.85),
           "liner": new_mat("BB_exterior_wall_inner_face", (0.80, 0.79, 0.76), 0.8), "stair": new_mat("BB_stair_steel_pan", (0.28, 0.28, 0.29), 0.55, 0.5),
           "guard": new_mat("BB_stair_guard", (0.12, 0.12, 0.13), 0.4, 0.7), "roof": new_mat("BB_roof_deck_underside", (0.78, 0.78, 0.76), 0.75),
           "cnsa": new_mat("TENANT_CNSA_partition", (0.78, 0.84, 0.90), 0.8), "zone": new_mat("TENANT_CNSA_zone_plate", (0.55, 0.70, 0.85), 0.9),
           "tws1": new_mat("BB_exterior_wall_inner_face_TWS1_translucent", (0.92, 0.92, 0.90), 0.6, 0.0, emission=6.0)}
    built = {}

    # ---------------------------------------------------------------- exterior envelope union (temporary copies of the shell prisms)
    shell_names = ["BI_Z1_south_wing_L1", "BI_Z1_south_wing_L2", "BI_Z1_L2_storefront_projection_bay", "BI_Z2_band_E_F2", "BI_Z3_vestibule_100",
                   "BI_Z4a_north_block_L1", "BI_Z4a_north_block_mid", "BI_Z4a_north_block_L2", "BI_Z4b_north_block_south_part", "BI_Z5_end_block_13_14"]
    temps = []
    for n in shell_names:
        src = objs[n]
        me = src.data.copy()
        o = bpy.data.objects.new("TMP_" + n, me)
        o.matrix_world = src.matrix_world.copy()
        scene.collection.objects.link(o)
        temps.append(o)
    U = union_into("TMP_envelope_union", temps, scene.collection, None)
    bm = bmesh.new()
    bm.from_mesh(U.data)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0005)
    bmesh.ops.dissolve_limit(bm, angle_limit=math.radians(0.5), verts=bm.verts, edges=bm.edges)
    bm.faces.ensure_lookup_table()
    side, bottom, top = [], [], []
    for f in bm.faces:
        n = f.normal
        pts = [(v.co.x / FT, v.co.y / FT, v.co.z / FT) for v in f.verts]
        if n.z < -0.9 and abs(pts[0][2]) < 0.01:
            bottom.append(pts)
        elif n.z > 0.9 and pts[0][2] > 5.0:
            top.append((pts, (n.x, n.y, n.z)))
        elif abs(n.z) < 0.05:
            side.append((pts, (n.x, n.y, n.z)))
    bm.free()
    report["envelope_union"] = {"bottom_faces": len(bottom), "side_faces": len(side), "top_faces": len(top)}

    # ---- L1 slab on grade: footprint = the union's bottom cap (z = 0), 4 in thick
    T_SOG = D["slabs"]["L1_slab_on_grade"]["thickness_ft"]
    bm = bmesh.new()
    l1_area = 0.0
    for pts in bottom:
        poly = [(p[0], p[1]) for p in pts]
        l1_area += poly_area(poly)
        vs = [bm.verts.new((m(x), m(y), 0.0)) for x, y in poly]
        f = bm.faces.new(vs)
        f.normal_update()
        if f.normal.z < 0:
            f.normal_flip()
    r = bmesh.ops.extrude_face_region(bm, geom=list(bm.faces))
    for v in [g for g in r["geom"] if isinstance(g, bmesh.types.BMVert)]:
        v.co.z = -m(T_SOG)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    sog = new_obj("BB_L1_slab_on_grade", bm, sub["BB_10_slabs"], MAT["conc"], {"source": D["slabs"]["L1_slab_on_grade"]["source"], "code": "W thickness / V extent (v008 footprint)"})
    built["BB_L1_slab_on_grade_sqft"] = round(l1_area, 1)

    # ---- exterior wall inner faces + window reveals
    TH = D["exterior_wall_thickness_ft"]
    regs = R["regions"]

    def mat_at(facade, u, z):
        mt = "UNRES"
        for q in regs:
            if q["facade"] == facade and q["u0"] - 0.05 <= u <= q["u1"] + 0.05 and q["z0"] - 0.05 <= z <= q["z1"] + 0.05:
                mt = q["mat"]
        return mt
    openings = []
    for o in objs:
        if o.name.startswith("BI_open_") and o.type == "MESH":
            pts = [o.matrix_world @ Vector(c) for c in o.bound_box]
            b = [min(p.x for p in pts) / FT, min(p.y for p in pts) / FT, min(p.z for p in pts) / FT, max(p.x for p in pts) / FT, max(p.y for p in pts) / FT, max(p.z for p in pts) / FT]
            if (b[3] - b[0]) < (b[4] - b[1]):
                openings.append({"axis": "x", "plane": (b[0] + b[3]) / 2, "rect": (b[1], b[4], b[2], b[5])})
            else:
                openings.append({"axis": "y", "plane": (b[1] + b[4]) / 2, "rect": (b[0], b[3], b[2], b[5])})
    bm_in = bmesh.new()
    bm_tws = bmesh.new()
    bm_rev = bmesh.new()
    liner_rec = []
    plan_segments = []           # (x0,y0,x1,y1) of exterior faces in plan, for the partition filter
    for pts, n in side:
        nx, ny = n[0], n[1]
        if abs(nx) >= abs(ny):
            facade = "EAST" if nx > 0 else "WEST"
            axis = "x"
            uz = [(p[1], p[2]) for p in pts]
            plane = sum(p[0] for p in pts) / len(pts)
        else:
            facade = "NORTH" if ny > 0 else "SOUTH"
            axis = "y"
            uz = [(p[0], p[2]) for p in pts]
            plane = sum(p[1] for p in pts) / len(pts)
        u0, u1 = min(q[0] for q in uz), max(q[0] for q in uz)
        z0, z1 = min(q[1] for q in uz), max(q[1] for q in uz)
        if u1 - u0 < 0.05 or z1 - z0 < 0.05:
            continue
        zs = min(z1, max(z0, 5.0)) if z0 < 5.0 else (z0 + z1) / 2
        mt = mat_at(facade, (u0 + u1) / 2, zs)
        t = TH.get(mt, TH["UNRES"])
        zb = [p for p in pts if p[2] < z0 + 0.01]
        if len(zb) >= 2:
            plan_segments.append((zb[0][0], zb[0][1], zb[1][0], zb[1][1]))
        ops = [o["rect"] for o in openings if o["axis"] == axis and abs(o["plane"] - plane) < 0.35 and o["rect"][1] > u0 and o["rect"][0] < u1 and o["rect"][3] > z0 and o["rect"][2] < z1]
        rects = [(u0, u1, z0, z1)]
        for oo in ops:
            rects = v5.rects_minus(rects, oo)
        nv = Vector(n)

        def p3(u, z, depth):
            base = Vector((m(plane), m(u), m(z))) if axis == "x" else Vector((m(u), m(plane), m(z)))
            return base - nv * m(depth)
        target = bm_tws if mt == "TWS1" else bm_in
        for (a, b, c, d) in rects:
            poly = v5.clip_poly(uz, a, b, c, d)
            if len(poly) < 3:
                continue
            vs = [target.verts.new(p3(u, z, t)) for u, z in poly]
            try:
                f = target.faces.new(vs)
            except ValueError:
                continue
            f.normal_update()
            if f.normal.dot(nv) > 0:       # inner face looks inward (opposite the outward normal)
                f.normal_flip()
        for (a, b, c, d) in ops:
            a2, b2, c2, d2 = max(a, u0), min(b, u1), max(c, z0), min(d, z1)
            if b2 - a2 < 0.05 or d2 - c2 < 0.05:
                continue
            for (ua, za, ub, zb_) in ((a2, c2, a2, d2), (b2, c2, b2, d2), (a2, c2, b2, c2), (a2, d2, b2, d2)):     # jambs, sill, head
                vs = [bm_rev.verts.new(p3(ua, za, 0.02)), bm_rev.verts.new(p3(ub, zb_, 0.02)), bm_rev.verts.new(p3(ub, zb_, t)), bm_rev.verts.new(p3(ua, za, t))]
                try:
                    bm_rev.faces.new(vs)
                except ValueError:
                    pass
        liner_rec.append({"facade": facade, "plane": round(plane, 2), "u": [round(u0, 2), round(u1, 2)], "z": [round(z0, 2), round(z1, 2)], "material": mt, "thickness_ft": t, "openings": len(ops)})
    bmesh.ops.remove_doubles(bm_in, verts=bm_in.verts, dist=0.0005)
    liner = new_obj("BB_extwall_inner_faces", bm_in, sub["BB_12_exterior_wall_inner_faces"], MAT["liner"], {"code": "V faces (v008 envelope) / W thickness (A0.21) / I material lookup (v008 regions)", "note": "inside face of every exterior wall = outside face minus the wall-type thickness; openings cut where the v001 lite placeholders are"})
    for pg in liner.data.polygons:
        pg.use_smooth = False
    reveals = new_obj("BB_extwall_window_reveals", bm_rev, sub["BB_12_exterior_wall_inner_faces"], MAT["liner"], {"code": "I (jamb/head/sill faces between the outside plane and the inside face)"})
    bmesh.ops.remove_doubles(bm_tws, verts=bm_tws.verts, dist=0.0005)
    new_obj("BB_extwall_inner_faces_TWS1_translucent", bm_tws, sub["BB_12_exterior_wall_inner_faces"], MAT["tws1"], {"code": "V faces / W Kingspan Unigrid Verti-Lite translucent wall (A7.27)", "note": "inside face of the translucent wall; emissive placeholder so the courts read as daylit (light transmission not simulated)"})
    built["exterior_faces_lined"] = len(liner_rec)
    built["exterior_faces_by_material"] = {}
    for q in liner_rec:
        built["exterior_faces_by_material"][q["material"]] = built["exterior_faces_by_material"].get(q["material"], 0) + 1
    l1_wall_deduct = 0.0
    for (x0, y0, x1, y1), q in zip(plan_segments, [q for q in liner_rec]):
        pass
    # L1 interior area = footprint minus the exterior wall zone (sum of face length x thickness for faces present at z 0-13)
    for q in liner_rec:
        if q["z"][0] < 1.0:
            l1_wall_deduct += (q["u"][1] - q["u"][0]) * q["thickness_ft"]
    built["L1_interior_area_inside_exterior_walls_sqft"] = round(l1_area - l1_wall_deduct, 0)

    # ---- roof deck underside plates (T.O.S. by zone, written datums linearly between them)
    bm = bmesh.new()
    for pts, n in top:
        cx = sum(p[0] for p in pts) / len(pts); cy = sum(p[1] for p in pts) / len(pts)
        zone = zone_of(cx, cy)
        if pts[0][2] < 12.0 and zone != "vestibule":
            continue                      # the L1 wing cap at 13.5 is an internal prism face, not a roof
        vs = [bm.verts.new((m(p[0]), m(p[1]), m(roof_tos(p[0], p[1], zone)))) for p in pts]
        try:
            f = bm.faces.new(vs)
        except ValueError:
            continue
        f.normal_update()
        if f.normal.z > 0:
            f.normal_flip()
    roof = new_obj("BB_roof_deck_underside_TOS", bm, sub["BB_17_roof_deck_underside"], MAT["roof"], {"code": "W datums (T.O.S. A 30.0, F 31.5, N 37.29, col 14 28.0; bay top 27.33; vestibule 9.0) / I linear between", "note": "plate at top-of-steel; joists/trusses/deck not modeled"})
    # remove the temporary union
    ud = U.data
    bpy.data.objects.remove(U, do_unlink=True)
    bpy.data.meshes.remove(ud)

    # ---- Level 2 and mezzanine slabs (A1.00b hatch regions)
    L2Z, TL2 = D["slabs"]["L2_composite"]["z_top"], D["slabs"]["L2_composite"]["thickness_ft"]
    temps = []
    l2_area = 0.0
    for i, (clip, x0, x1, y0, y1) in enumerate(D["l2_slab_rects"]):
        if clip == "clip-3":
            continue
        temps.append(box(f"TMP_l2_{i}", x0, x1, y0, y1, L2Z - TL2, L2Z, scene.collection, None))
        l2_area += (x1 - x0) * (y1 - y0)
    gp = [tuple(p) for p in D["gallery_polygon"]]
    temps.append(prism("TMP_l2_gallery", gp, L2Z - TL2, L2Z, scene.collection, None))
    l2_area += poly_area(gp)
    l2 = union_into("BB_L2_composite_slab", temps, sub["BB_10_slabs"], MAT["conc"], {"source": D["slabs"]["L2_composite"]["source"], "code": "W thickness / V extent (A1.00b)"})
    l2_top = sum(p.area for p in l2.data.polygons if p.normal.z > 0.9) / FT / FT
    built["BB_L2_composite_slab_sqft_union"] = round(l2_top, 1)
    MZ, TMZ = D["slabs"]["MEZZ_composite"]["z_top"], D["slabs"]["MEZZ_composite"]["thickness_ft"]
    temps = []
    for i, (clip, x0, x1, y0, y1) in enumerate(D["l2_slab_rects"]):
        if clip == "clip-3":
            temps.append(box(f"TMP_mz_{i}", x0, x1, y0, y1, MZ - TMZ, MZ, scene.collection, None))
    mz = union_into("BB_mezzanine_slab_233", temps, sub["BB_10_slabs"], MAT["conc"], {"source": D["slabs"]["MEZZ_composite"]["source"], "code": "V extent / W level / A thickness"})
    built["BB_mezzanine_slab_sqft"] = round(sum(p.area for p in mz.data.polygons if p.normal.z > 0.9) / FT / FT, 1)

    # ---- columns
    bm = bmesh.new()
    col_rec = []
    for c in D["columns"]:
        zone = zone_of(c["x"], c["y"])
        zt = roof_tos(c["x"], c["y"], zone)
        if zone == "vestibule":
            zt = 31.5
        d, bf = c["depth_ft"], c["flange_ft"]
        box_bm(bm, c["x"] - bf / 2, c["x"] + bf / 2, c["y"] - d / 2, c["y"] + d / 2, 0.0, zt)
        col_rec.append({**c, "z_top_ft": round(zt, 2), "zone": zone})
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    new_obj("BB_columns_S601", bm, sub["BB_11_columns"], MAT["steel"], {"code": "W (S601 marks and sizes) / grid intersections", "note": "box placeholders d x bf; web parallel to y assumed; splices ignored; top at the roof T.O.S. formula"})
    built["columns"] = len(col_rec)

    # ---- elevator
    E = D["elevator"]
    hx0, hx1, hy0, hy1 = E["hoistway_inside"]["x0"], E["hoistway_inside"]["x1"], E["hoistway_inside"]["y0"], E["hoistway_inside"]["y1"]
    tw = E["wall_thickness_ft"]
    ring = [(hx0 - tw, hx0, hy0 - tw, hy1 + tw), (hx1, hx1 + tw, hy0 - tw, hy1 + tw), (hx0, hx1, hy0 - tw, hy0), (hx0, hx1, hy1, hy1 + tw)]
    boxes("BB_elevator_hoistway_walls", ring, -E["pit_depth_ft"], E["top_ft"], sub["BB_15_elevator"], MAT["shaft"], {"code": "V position / W inside 7'-0\" x 8'-8\", pit -5'-0\" (A6.01)", "note": E["walls"]})
    box("BB_elevator_pit_slab", hx0 - tw, hx1 + tw, hy0 - tw, hy1 + tw, -E["pit_depth_ft"] - 0.67, -E["pit_depth_ft"], sub["BB_15_elevator"], MAT["conc"], {"code": "W pit depth / A slab thickness"})
    built["elevator_hoistway_inside_ft"] = [round(hx1 - hx0, 2), round(hy1 - hy0, 2)]

    # ---- partitions (FMK plans): drop rectangles on the exterior wall line and inside the hoistway; core vs program
    def near_exterior(cx, cy, tol=1.6):
        for x0, y0, x1, y1 in plan_segments:
            dx, dy = x1 - x0, y1 - y0
            L2 = dx * dx + dy * dy
            if L2 < 1e-6:
                continue
            tt = max(0.0, min(1.0, ((cx - x0) * dx + (cy - y0) * dy) / L2))
            px, py = x0 + tt * dx, y0 + tt * dy
            if math.hypot(cx - px, cy - py) < tol:
                return True
        return False
    hoist_box = (hx0 - tw - 0.5, hx1 + tw + 0.5, hy0 - tw - 0.5, hy1 + tw + 0.5)
    wall_stats = {}
    for level, key, z0, z_prog in (("L1", "walls_L1", 0.0, 10.0), ("L2", "walls_L2", L2Z, L2Z + 10.0)):
        core_r, prog_r, dropped = [], [], 0
        for w in D[key]:
            cx, cy = (w["x0"] + w["x1"]) / 2, (w["y0"] + w["y1"]) / 2
            if near_exterior(cx, cy) or (hoist_box[0] <= cx <= hoist_box[1] and hoist_box[2] <= cy <= hoist_box[3]):
                dropped += 1
                continue
            (core_r if w["core"] else prog_r).append((w["x0"], w["x1"], w["y0"], w["y1"]))
        # core walls: to the deck (L2 slab underside where an L2 slab exists above, else roof); built per rectangle height class
        bm = bmesh.new()
        for x0, x1, y0, y1 in core_r:
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
            zone = zone_of(cx, cy)
            if level == "L1":
                over_l2 = any(rx0 <= cx <= rx1 and ry0 <= cy <= ry1 for _, rx0, rx1, ry0, ry1 in D["l2_slab_rects"]) or (28.5 <= cx <= 71 and 53.4 <= cy <= 55.0)
                zt = (L2Z - TL2) if over_l2 else roof_tos(cx, cy, zone)
            else:
                zt = roof_tos(cx, cy, zone)
            box_bm(bm, x0, x1, y0, y1, z0, zt)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        new_obj(f"BB_core_walls_{level}", bm, sub["BB_13_core_walls"], MAT["shaft"], {"code": "V (A1.01/A1.02 wall pairs) / A height to deck", "zones": json.dumps(D["core_zones_" + level])})
        boxes(f"BB_fmk_program_partitions_{level}", prog_r, z0, z_prog, sub["BB_16_fmk_program_partitions"], MAT["gwb"], {"code": "V (A1.01/A1.02) / A height 10 ft", "note": "FMK-documented interior fit-out partitions of the sports-medicine program (offices, training, PT, lockers, storage) - documented in the base set but not structure/core; kept separate so a test fit can treat them as movable"})
        wall_stats[level] = {"core_rects": len(core_r), "program_rects": len(prog_r), "dropped_on_exterior_or_hoistway": dropped,
                             "core_wall_plan_sqft": round(sum((r[1] - r[0]) * (r[3] - r[2]) for r in core_r), 1), "program_wall_plan_sqft": round(sum((r[1] - r[0]) * (r[3] - r[2]) for r in prog_r), 1)}
    built["partitions"] = wall_stats

    # ---- stairs
    S = D["stairs"]
    stair_rec = {}

    def build_stair(name, sd, mirror_x=None):
        bmt, bmg = bmesh.new(), bmesh.new()
        Rr, Tt = sd["riser_ft"], sd["tread_ft"]

        def mx(x):
            return 2 * mirror_x - x if mirror_x is not None else x
        top_z = 0.0
        for seg in sd["segments"]:
            if seg["kind"] == "landing":
                x0, x1 = seg["x0"], seg["x1"]
                if mirror_x is not None:
                    x0, x1 = mx(x1), mx(x0)
                y1 = seg.get("y1_fix", seg["y1"])
                box_bm(bmt, x0, x1, seg["y0"], y1, seg["z"] - 0.5, seg["z"])
                top_z = max(top_z, seg["z"])
                continue
            n_r, n_t, z0 = seg["risers"], seg["treads"], seg["z0"]
            if seg["dir"] in ("+x", "-x"):
                s = seg["x_start"]; y0, y1 = seg["y0"], seg["y1"]
                sgn = 1 if seg["dir"] == "+x" else -1
                for i in range(n_t):
                    a, b = s + sgn * i * Tt, s + sgn * (i + 1) * Tt
                    xa, xb = (mx(max(a, b)), mx(min(a, b))) if mirror_x is not None else (min(a, b), max(a, b))
                    box_bm(bmt, xa, xb, y0, y1, z0 + (i + 1) * Rr - 0.35, z0 + (i + 1) * Rr)
                # guards along both sides of the flight (sloped plates 3.5 ft high)
                xa, xb = s, s + sgn * n_t * Tt
                za, zb = z0 + Rr, z0 + n_t * Rr
                for yy in (y0, y1):
                    vs = [bmg.verts.new((m(mx(xa)), m(yy), m(za))), bmg.verts.new((m(mx(xb)), m(yy), m(zb))), bmg.verts.new((m(mx(xb)), m(yy), m(zb + 3.5))), bmg.verts.new((m(mx(xa)), m(yy), m(za + 3.5)))]
                    bmg.faces.new(vs)
                top_z = max(top_z, z0 + n_r * Rr)
            else:
                s = seg["y_start"]; x0, x1 = seg["x0"], seg["x1"]
                if mirror_x is not None:
                    x0, x1 = mx(x1), mx(x0)
                sgn = 1 if seg["dir"] == "+y" else -1
                for i in range(n_t):
                    a, b = s + sgn * i * Tt, s + sgn * (i + 1) * Tt
                    box_bm(bmt, x0, x1, min(a, b), max(a, b), z0 + (i + 1) * Rr - 0.35, z0 + (i + 1) * Rr)
                ya, yb = s, s + sgn * n_t * Tt
                za, zb = z0 + Rr, z0 + n_t * Rr
                for xx in (x0, x1):
                    vs = [bmg.verts.new((m(xx), m(ya), m(za))), bmg.verts.new((m(xx), m(yb), m(zb))), bmg.verts.new((m(xx), m(yb), m(zb + 3.5))), bmg.verts.new((m(xx), m(ya), m(za + 3.5)))]
                    bmg.faces.new(vs)
                top_z = max(top_z, z0 + n_r * Rr)
        bmesh.ops.recalc_face_normals(bmt, faces=bmt.faces)
        new_obj(f"BB_stair_{name}", bmt, sub["BB_14_stairs"], MAT["stair"], {"code": sd["code"], "note": sd.get("note", ""), "levels": ",".join(sd["levels"]), "risers": sd["risers_total"]})
        new_obj(f"BB_stair_{name}_guards", bmg, sub["BB_14_stairs"], MAT["guard"], {"code": "A (42 in guard, rail type per A6.21 recorded)"})
        return round(top_z, 3)
    for name, sd in S.items():
        if "mirror_of" in sd:
            src = S[sd["mirror_of"]]
            stair_rec[name] = {"top_z_ft": build_stair(name, src, mirror_x=sd["mirror_x"]), "levels": src["levels"], "risers": src["risers_total"]}
        else:
            stair_rec[name] = {"top_z_ft": build_stair(name, sd), "levels": sd["levels"], "risers": sd["risers_total"]}
    built["stairs"] = stair_rec

    # ---- CNSA (existing tenant)
    C = D["cnsa"]
    zl2 = C["zone_L2"]
    cn1 = [tuple(r) for r in C["rects_L1"]]
    cn2 = [tuple(r) for r in C["rects_L2"] if r[0] <= zl2["x1"] + 1.0]
    boxes("CNSA_partitions_L1", cn1, 0.0, C["height_ft"], sub["CNSA_L1_partitions"], MAT["cnsa"], {"code": "V (CNSA A100 rev 8, black lines) / A height 10 ft", "source": C["source"]})
    boxes("CNSA_partitions_L2", cn2, L2Z, L2Z + C["height_ft"], sub["CNSA_L2_partitions"], MAT["cnsa"], {"code": "V (CNSA A100 rev 8) / A height", "source": C["source"]})
    z1 = C["zone_L1"]
    box("CNSA_tenant_zone_L1", z1["x0"], z1["x1"], z1["y0"], z1["y1"], 0.01, 0.03, sub["CNSA_tenant_zones"], MAT["zone"], {"note": z1["note"], "sqft": round((z1["x1"] - z1["x0"]) * (z1["y1"] - z1["y0"]), 0)})
    box("CNSA_tenant_zone_L2", zl2["x0"], zl2["x1"], zl2["y0"], zl2["y1"], L2Z + 0.01, L2Z + 0.03, sub["CNSA_tenant_zones"], MAT["zone"], {"note": zl2["note"], "sqft": round((zl2["x1"] - zl2["x0"]) * (zl2["y1"] - zl2["y0"]), 0)})
    built["cnsa"] = {"L1_rects": len(cn1), "L2_rects": len(cn2), "zone_L1_sqft": round((z1["x1"] - z1["x0"]) * (z1["y1"] - z1["y0"]), 0), "zone_L2_sqft": round((zl2["x1"] - zl2["x0"]) * (zl2["y1"] - zl2["y0"]), 0)}

    # ---- cameras
    camcol = bpy.data.collections["90_Cameras"]
    for name, c in D["cameras"].items():
        assert name not in objs, name
        cam = bpy.data.cameras.new(name)
        if c["type"] == "ortho":
            cam.type = "ORTHO"
            cam.ortho_scale = m(c["ortho"])
        else:
            cam.lens = c["lens"]
        cam.clip_start = m(c.get("clip_start_ft", 0.3))
        cam.clip_end = 3000.0
        cam.dof.use_dof = False
        o = bpy.data.objects.new(name, cam)
        o.location = Vector([m(v) for v in c["loc"]])
        d = Vector([m(v) for v in c["target"]]) - o.location
        o.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
        camcol.objects.link(o)

    # ---------------------------------------------------------------- verification
    geo1, mats1, cols1 = snapshot()
    changed = [n for n in geo0 if geo0[n] != geo1.get(n)]
    assert not changed, f"existing objects changed: {changed[:10]}"
    assert all(n in geo1 for n in geo0), "existing object missing"
    assert all(mats0[k] == mats1.get(k) for k in mats0), "existing material node trees changed"
    for cname, v in cols0.items():
        assert cols1[cname][:2] == v[:2] and cols1[cname][2] == v[2], f"existing collection changed: {cname}"
    new_names = sorted(set(o.name for o in objs) - names0)
    allowed_roots = {"Building_I", "BASE_BUILDING", "EXISTING_TENANT", "CNSA", "FUTURE_CONCEPTS"} | set(sub) | {"90_Cameras"}
    for n in new_names:
        o = objs[n]
        cn = [c.name for c in o.users_collection]
        assert all(c in allowed_roots for c in cn) and (o.type == "CAMERA" or "90_Cameras" not in cn), f"new object {n} outside the interior collections: {cn}"
    # empty future concepts
    for cname in ("Concept_A", "Concept_B", "Concept_C"):
        assert len(bpy.data.collections[cname].all_objects) == 0
    # no tenant object in BASE_BUILDING and vice versa
    assert not [o.name for o in BB.all_objects if o.name.startswith(("CNSA", "TENANT"))]
    assert not [o.name for o in ET.all_objects if o.name.startswith("BB_")]

    # ---------------------------------------------------------------- areas
    core_zone_area = sum((b - a) * (d - c) for a, b, c, d in D["core_zones_L1"].values())
    areas = {"L1_footprint_gross_sqft_v008_envelope": round(l1_area, 0), "L1_interior_inside_exterior_walls_sqft": built["L1_interior_area_inside_exterior_walls_sqft"],
             "L2_slab_modeled_sqft_A1_00b": built["BB_L2_composite_slab_sqft_union"], "mezzanine_slab_sqft": built["BB_mezzanine_slab_sqft"],
             "L1_core_zones_bounding_sqft": round(core_zone_area, 0), "L1_courts_121_open_sqft_approx": round((271.0 - 121.0) * (185.9 - 71.5), 0),
             "CNSA_L1_tenant_zone_sqft": built["cnsa"]["zone_L1_sqft"], "CNSA_L2_tenant_zone_sqft": built["cnsa"]["zone_L2_sqft"],
             "MOB_shell_L2_remaining_sqft": round((271.0 - zl2["x1"]) * (61.5 + 0.95), 0),
             "published": D["published_areas_for_check"]}
    areas["modeled_total_L1_plus_L2_plus_mezz_sqft"] = round(l1_area + built["BB_L2_composite_slab_sqft_union"] + built["BB_mezzanine_slab_sqft"], 0)
    areas["code_total_sqft"] = D["published_areas_for_check"]["code_total_sf"]
    areas["difference_modeled_minus_code_sqft"] = round(areas["modeled_total_L1_plus_L2_plus_mezz_sqft"] - areas["code_total_sqft"], 0)
    report.update({"built": built, "areas": areas, "columns": col_rec, "liner_faces": liner_rec, "objects_after": len(objs), "objects_added": new_names,
                   "materials_added": sorted(set(bpy.data.materials.keys()) - set(mats0)), "existing_objects_identical": True, "existing_materials_identical": True})

    # ---------------------------------------------------------------- viewer JSON
    viewer = {"building": "Building I - Rea Farms Sports Medicine Center", "units": "ft, origin grid 1 x A at FFE 661.75, +X east, +Y north", "model": str(BLEND.name),
              "levels": [{"id": k, "z_ft": v["z"], "code": v["code"], "source": v["source"]} for k, v in D["levels"].items()],
              "slabs": D["slabs"], "clear_heights": D["heights"],
              "columns": [{"mark": c["mark"], "x": c["x"], "y": c["y"], "size": c["size"], "z_top": c["z_top_ft"]} for c in col_rec],
              "shafts": [{"id": "elevator_hoistway", "x0": hx0, "x1": hx1, "y0": hy0, "y1": hy1, "z0": -E["pit_depth_ft"], "z1": E["top_ft"], "note": E["car"]}],
              "elevator": E, "stairs": {k: {"levels": v["levels"], "risers": v["risers"], "top_z_ft": v["top_z_ft"], "footprint": {"x": [min(s.get("x0", s.get("x_start", 999)) for s in S[k if "mirror_of" not in S[k] else S[k]["mirror_of"]]["segments"]), None]}} for k, v in stair_rec.items()},
              "fixed_rooms": [{"zone": k, "x0": a, "x1": b, "y0": c, "y1": d, "level": "L1"} for k, (a, b, c, d) in D["core_zones_L1"].items()] + [{"zone": k, "x0": a, "x1": b, "y0": c, "y1": d, "level": "L2"} for k, (a, b, c, d) in D["core_zones_L2"].items()],
              "tenant_zones": [{"id": "CNSA_L1", **z1, "level": "L1", "status": "existing tenant (CNSA upfit rev 8, 2/18/2026)"}, {"id": "CNSA_L2", **zl2, "level": "L2", "status": "existing tenant"},
                               {"id": "MOB_shell_2300_L2", "x0": zl2["x1"], "x1": 271.0, "y0": -0.95, "y1": 61.5, "level": "L2", "status": "shell - available for a future concept"}],
              "constraints": {"braced_frames": D["braced_frames"], "shafts_and_cores": "elevator hoistway; stairs (lobby, south, gallery, mezzanine E/W); restroom cores 105-112 / 127-130 / 207-208; elec 103/104/203/225; tele 145/245; riser 129; corridor 102/202 rated walls",
                              "floor_openings": "lobby band x 28.5-71 y 53.5-74.4 (no Level 2 slab: double-height lobby + lobby stair); courts x 121-271 y 71.5-186 open to roof; training area 119/120 x 71-121 y 170-198 open to roof; elevator hoistway; south stair well x 275-281 y 79.7-96; gallery stair",
                              "low_clearance": "Level 1 under the Level 2 wing/west-block slab: 13.5-13.6 ft to structure (W14/W16 beams); Level 2 under the roof: 12.7-14.2 ft; gallery cantilever soffit 9.0 ft (M)",
                              "doors_base_building": [d for d in D["doors"] if d["category"] == "base_building"]},
              "exterior_wall_thickness_ft": D["exterior_wall_thickness_ft"], "areas": areas}
    VIEWER.write_text(json.dumps(viewer, indent=1), encoding="utf-8")

    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))

    # ---------------------------------------------------------------- renders (shell hidden at collection level for the interior views only)
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
        hide_cols = ["01_Shell", "02_Parapet_screens", "07_Facade_regions_v005", "03_Canopy"]
        saved = {c: bpy.data.collections[c].hide_render for c in hide_cols + ["04_Openings"]}
        for c in hide_cols:
            bpy.data.collections[c].hide_render = True
        engine0 = scene.render.engine
        L2_objs = ["BB_L2_composite_slab", "BB_mezzanine_slab_233", "BB_core_walls_L2", "BB_fmk_program_partitions_L2", "CNSA_partitions_L2", "CNSA_tenant_zone_L2"]
        VIEW_SETUP = {   # engine, collections hidden in addition, objects hidden
            "1_L1_plan_cutaway": ("BLENDER_WORKBENCH", [], L2_objs + ["BB_roof_deck_underside_TOS"]),
            "2_L2_plan_cutaway": ("BLENDER_WORKBENCH", [], ["BB_roof_deck_underside_TOS"]),
            "3_longitudinal_section": ("BLENDER_WORKBENCH", [], []),
            "4_transverse_section": ("BLENDER_WORKBENCH", [], []),
            "5_lobby_core": ("CYCLES", ["04_Openings"], []),
            "6_courts_interior": ("CYCLES", ["04_Openings"], []),
            "7_structure_core_oblique": ("CYCLES", ["04_Openings"], ["BB_extwall_inner_faces", "BB_extwall_inner_faces_TWS1_translucent", "BB_extwall_window_reveals", "BB_roof_deck_underside_TOS"]),
        }
        sh = scene.display.shading
        sh.light = "STUDIO"
        sh.color_type = "MATERIAL"
        sh.show_cavity = True
        sh.show_shadows = False
        sh.show_object_outline = True
        vs = scene.view_settings
        view0 = (vs.view_transform, vs.look, vs.exposure)
        # interior fill: a large, dim, uniform world is what an unlit interior needs to read; the v013 physical sky (world) is
        # kept for the exterior, so a temporary sun-less hemisphere light is added for the interior views only and removed after
        fill = bpy.data.lights.new("TMP_interior_fill", "SUN")
        fill.energy = 0.0
        fill_o = bpy.data.objects.new("TMP_interior_fill", fill)
        scene.collection.objects.link(fill_o)
        world0_strength = None
        wnodes = scene.world.node_tree.nodes if scene.world and scene.world.use_nodes else None
        bgs = [n for n in wnodes if n.bl_idname == "ShaderNodeBackground"] if wnodes else []
        times = {}
        try:
            for view, (cam, (rx, ry)) in D["views"].items():
                if only and view not in only:
                    continue
                engine, xcols, xobjs = VIEW_SETUP[view]
                scene.render.engine = engine
                if engine == "BLENDER_WORKBENCH":
                    vs.view_transform, vs.look, vs.exposure = "Standard", "None", 0.0
                else:
                    vs.view_transform, vs.look, vs.exposure = "AgX", "None", -1.3      # interiors: 3 stops brighter than the v013 exterior setting (unlit interior, daylight through the apertures only)
                    for bg in bgs:
                        bg.inputs["Strength"].default_value = bg.inputs["Strength"].default_value * 1.0
                for c in xcols:
                    bpy.data.collections[c].hide_render = True
                for n in xobjs:
                    objs[n].hide_render = True
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
                for c in xcols:
                    bpy.data.collections[c].hide_render = saved[c]
                for n in xobjs:
                    objs[n].hide_render = False
        finally:
            for c, v in saved.items():
                bpy.data.collections[c].hide_render = v
            scene.render.engine = engine0
            vs.view_transform, vs.look, vs.exposure = view0
            bpy.data.objects.remove(fill_o, do_unlink=True)
            bpy.data.lights.remove(fill)
        report["render_seconds"] = times
        report["render_exposure"] = {"workbench_views": "Standard, exposure 0", "cycles_interiors": "AgX, exposure -1.3 (v013 exterior setting -4.35 restored in the saved file)"}
        report["render_note"] = ("interior views rendered with collections 01_Shell, 02_Parapet_screens, 07_Facade_regions_v005 and 03_Canopy hidden (collection flags, restored before saving); "
                                 "cutaways and sections use the Workbench engine (studio light, material colours, camera clipping at the cut plane; the L1 cutaway also hides the Level 2 / mezzanine objects and the roof plates); "
                                 "perspective interiors use Cycles with the opaque lite placeholders (04_Openings) hidden so daylight enters through the window apertures; the structure oblique also hides the inner-face liner and roof plates")
        scene.camera = objs["BI_cam_int_lobby_core"]
        bpy.ops.wm.save_mainfile()
        geo2, mats2, cols2 = snapshot()
        assert all(geo0[n] == geo2[n] for n in geo0) and cols2 == {**cols2, **{k: cols1[k] for k in cols0}}
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("BUILD_REPORT=" + json.dumps({k: v for k, v in report.items() if k not in ("columns", "liner_faces", "objects_added")}))


if __name__ == "__main__":
    main()
