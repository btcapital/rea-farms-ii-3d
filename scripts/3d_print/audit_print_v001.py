"""Building II 3D-print derivative - printability AUDIT v001 (read-only).

Run:
  blender -b models/Building_II/print_derivatives/building_II_print_v001.blend \
          --python scripts/3d_print/audit_print_v001.py

The script NEVER saves the .blend. It measures the evaluated meshes (modifiers applied
in memory only) and writes:
  exports/Building_II/3d_print/validation/print_audit_v001.json
  exports/Building_II/3d_print/validation/print_audit_v001_objects.csv

Geometry units: the model stores METRES in Blender units (build scripts use FT = 0.3048);
the scene only DISPLAYS feet (unit system IMPERIAL, scale_length 1.0).
"""
import bpy, bmesh, csv, json, math, os, sys, time
import numpy as np
from collections import Counter, defaultdict
from mathutils.bvhtree import BVHTree

T0 = time.time()
BLEND = bpy.data.filepath
ROOT = os.path.abspath(os.path.join(os.path.dirname(BLEND), "..", "..", ".."))
OUT = os.path.join(ROOT, "exports", "Building_II", "3d_print", "validation")
FT = 0.3048
PRINTER = {"name": "Bambu Lab H2S", "build_volume_mm": [340.0, 320.0, 340.0],
           "planning_margin_mm": 10.0}
SCALES = [200, 250, 300]
ZERO_T = 1e-5          # m  - thickness below this = zero-thickness surface
CONTACT_TOL = 0.01     # m  - 1 cm real (0.05 mm at 1:200) counts as touching

# ------------------------------------------------------------------ categories
parent = {}
def _walk(c):
    for ch in c.children:
        parent[ch.name] = c.name
        _walk(ch)
_walk(bpy.context.scene.collection)

def chain(cname):
    out = [cname]
    while out[-1] in parent:
        out.append(parent[out[-1]])
    return out

def category(o):
    if o.type in ("CAMERA", "LIGHT"):
        return "NONPRINT_camera_light"
    if o.type == "FONT":
        return "NONPRINT_text_label"
    names = set()
    for c in o.users_collection:
        names.update(chain(c.name))
    n = o.name
    if "zz_Cutters" in names: return "NONPRINT_boolean_cutters"
    if "13_Presentation_v010" in names: return "NONPRINT_presentation_backdrop"
    if "14_Context_v011" in names: return "CONTEXT_offsite"
    if "TENANT_CONCEPTS" in names: return "INTERIOR_tenant_concept"
    if "INT_LOBBY_CONCEPT_A" in names: return "INTERIOR_lobby"
    if "BASE_Exterior" in names or "BASE_Terraces" in names: return "INTERIOR_hollow_shell_alt"
    if "Building_II" in names: return "INTERIOR_base_building"
    if "01_Masses" in names: return "EXT_masses_and_roof"
    if "02_Parapets" in names: return "EXT_parapets"
    if "03_Opening_panels" in names: return "EXT_glazing"
    if "04_DropOff_Canopy" in names:
        return "EXT_canopy_dropoff_glass" if "glass" in n else "EXT_canopy_dropoff_steel"
    if "05_Door_Side_Canopies" in names: return "EXT_canopy_door_side"
    if "06_SunShade" in names: return "EXT_sunshade"
    if "07_Glass_Railings" in names: return "EXT_glass_railings"
    if "08_Utility_Yard" in names: return "EXT_utility_yard_walls"
    if "11_Facade_Detail_v004" in names:
        if "spandrel" in n: return "EXT_glazing"
        if "HM_door" in n: return "EXT_doors"
        return "EXT_mullions_frames"
    if "12_Landscape_v008" in names:
        mats = " ".join(s.material.name for s in o.material_slots if s.material)
        return "VEG_plants" if ("VEG_" in mats) else "SITE_beds_lawn"
    if "09_Site_context" in names:
        if "Terrain" in n: return "SITE_terrain"
        return "SITE_hardscape_stairs_walls"
    if "15_Site_Detail_v013" in names:
        if "_ctx_" in n or "Striping" in n: return "SITE_detail_parking_context"
        return "SITE_detail"
    return "UNCLASSIFIED"

# ------------------------------------------------------------------ mesh metrics
dg = bpy.context.evaluated_depsgraph_get()

def mesh_arrays(o):
    oe = o.evaluated_get(dg)
    me = oe.to_mesh()
    try:
        me.calc_loop_triangles()
        nv, ne, npo, nl, nt = len(me.vertices), len(me.edges), len(me.polygons), len(me.loops), len(me.loop_triangles)
        co = np.empty(nv * 3); me.vertices.foreach_get("co", co); co = co.reshape(-1, 3)
        ed = np.empty(ne * 2, dtype=np.int64); me.edges.foreach_get("vertices", ed); ed = ed.reshape(-1, 2)
        lv = np.empty(nl, dtype=np.int64); me.loops.foreach_get("vertex_index", lv)
        le = np.empty(nl, dtype=np.int64); me.loops.foreach_get("edge_index", le)
        ps = np.empty(npo, dtype=np.int64); me.polygons.foreach_get("loop_start", ps)
        pt = np.empty(npo, dtype=np.int64); me.polygons.foreach_get("loop_total", pt)
        tv = np.empty(nt * 3, dtype=np.int64); me.loop_triangles.foreach_get("vertices", tv); tv = tv.reshape(-1, 3)
        tp = np.empty(nt, dtype=np.int64); me.loop_triangles.foreach_get("polygon_index", tp)
    finally:
        oe.to_mesh_clear()
    M = np.array(o.matrix_world)
    w = co @ M[:3, :3].T + M[:3, 3] if nv else co
    return w, ed, lv, le, ps, pt, tv, tp

def islands_of(nv, ed):
    lab = np.arange(nv)
    if len(ed) == 0:
        return lab
    a, b = ed[:, 0], ed[:, 1]
    while True:
        old = lab.copy()
        m = np.minimum(lab[a], lab[b])
        np.minimum.at(lab, a, m); np.minimum.at(lab, b, m)
        lab = lab[lab]
        if np.array_equal(lab, old):
            return lab

def analyse(o):
    w, ed, lv, le, ps, pt, tv, tp = mesh_arrays(o)
    nv, ne, npo, nt = len(w), len(ed), len(ps), len(tv)
    r = {"verts": nv, "faces": npo, "tris": nt}
    if nv == 0:
        r.update(empty=True); return r
    fpe = np.bincount(le, minlength=ne)                       # faces per edge
    r["boundary_edges"] = int((fpe == 1).sum())
    r["nonmanifold_edges_gt2"] = int((fpe > 2).sum())
    r["wire_edges"] = int((fpe == 0).sum())
    used = np.zeros(nv, bool); used[ed.ravel()] = True
    r["loose_verts"] = int((~used).sum())
    # winding consistency on 2-face edges
    if npo:
        pidx = np.repeat(np.arange(npo), pt)
        pos = np.arange(len(lv)) - ps[pidx]
        nxt = ps[pidx] + (pos + 1) % pt[pidx]
        sign = np.where(lv == ed[le, 0], 1, -1)
        ssum = np.bincount(le, weights=sign, minlength=ne)
        r["flipped_winding_edges"] = int(((fpe == 2) & (np.abs(ssum) == 2)).sum())
    else:
        r["flipped_winding_edges"] = 0
    # triangles, areas, zero-area polygons
    if nt:
        p0, p1, p2 = w[tv[:, 0]], w[tv[:, 1]], w[tv[:, 2]]
        cr = np.cross(p1 - p0, p2 - p0)
        ta = 0.5 * np.linalg.norm(cr, axis=1)
        parea = np.bincount(tp, weights=ta, minlength=npo)
        r["zero_area_faces"] = int((parea < 1e-10).sum())
        r["surface_area_m2"] = float(ta.sum())
    else:
        r["zero_area_faces"] = 0; r["surface_area_m2"] = 0.0
    zl = np.linalg.norm(w[ed[:, 0]] - w[ed[:, 1]], axis=1) < 1e-7 if ne else np.array([])
    r["zero_length_edges"] = int(zl.sum()) if ne else 0
    # islands
    lab = islands_of(nv, ed)
    uniq = np.unique(lab[used]) if used.any() else np.array([], dtype=np.int64)
    bad_edge_v = np.zeros(nv, bool)
    be = ed[(fpe == 1) | (fpe > 2)]
    bad_edge_v[be.ravel()] = True
    tri_isl = lab[tv[:, 0]] if nt else np.array([], dtype=np.int64)
    thick, closed, zero_t, neg_vol, isl_dims = [], 0, 0, 0, []
    vol_total = 0.0
    for L in uniq:
        vm = lab == L
        vs = w[vm]
        tmask = tri_isl == L
        is_closed = not bad_edge_v[vm].any() and tmask.any()
        # thickness = min extent along the island's own face normals (exact for prisms/plates)
        t = float("inf")
        if tmask.any():
            n = cr[tmask]; a = ta[tmask]
            ok = a > 1e-12
            n = n[ok] / (np.linalg.norm(n[ok], axis=1)[:, None])
            if len(n):
                key = np.round(np.abs(n), 3)
                _, idx, inv = np.unique(key, axis=0, return_index=True, return_inverse=True)
                wsum = np.bincount(inv.ravel(), weights=a[ok])
                top = np.argsort(-wsum)[:48]
                for k in top:
                    d = n[idx[k]]
                    pr = vs @ d
                    t = min(t, float(pr.max() - pr.min()))
        if t == float("inf"):
            t = 0.0
        dims = vs.max(0) - vs.min(0)
        isl_dims.append(dims)
        thick.append(t)
        if t < ZERO_T: zero_t += 1
        if is_closed:
            closed += 1
            q0, q1, q2 = w[tv[tmask, 0]], w[tv[tmask, 1]], w[tv[tmask, 2]]
            v = float(np.einsum("ij,ij->i", q0, np.cross(q1, q2)).sum() / 6.0)
            vol_total += v
            if v < 0: neg_vol += 1
    r["islands"] = int(len(uniq))
    r["closed_islands"] = int(closed)
    r["open_islands"] = int(len(uniq) - closed)
    r["zero_thickness_islands"] = int(zero_t)
    r["inverted_islands"] = int(neg_vol)
    r["volume_closed_m3"] = vol_total
    r["min_thickness_m"] = float(min(thick)) if thick else 0.0
    r["median_island_thickness_m"] = float(np.median(thick)) if thick else 0.0
    r["watertight"] = bool(len(uniq) and closed == len(uniq) and r["flipped_winding_edges"] == 0)
    bb0, bb1 = w.min(0), w.max(0)
    r["bbox_min"] = [float(x) for x in bb0]; r["bbox_max"] = [float(x) for x in bb1]
    r["_w"] = w; r["_tv"] = tv
    return r

# ------------------------------------------------------------------ run
objs = [o for o in bpy.context.scene.objects]
rows, data = [], {}
for o in objs:
    cat = category(o)
    row = {"name": o.name, "type": o.type, "category": cat,
           "collections": "|".join(c.name for c in o.users_collection),
           "hide_viewport": bool(o.hide_viewport), "hide_render": bool(o.hide_render),
           "hidden_in_viewlayer": bool(o.hide_get()),
           "modifiers": "|".join(m.type for m in o.modifiers),
           "materials": "|".join(s.material.name for s in o.material_slots if s.material)}
    if o.type == "MESH":
        r = analyse(o)
        data[o.name] = r
        row.update({k: v for k, v in r.items() if not k.startswith("_")})
    rows.append(row)
print(f"[audit] measured {len(data)} meshes in {time.time()-T0:.1f}s")

# ------------------------------------------------------------------ extents
def extent(cats, exclude_names=()):
    lo = np.full(3, np.inf); hi = np.full(3, -np.inf); n = 0
    for row in rows:
        if row["category"] in cats and row["name"] in data and not data[row["name"]].get("empty") \
           and row["name"] not in exclude_names:
            r = data[row["name"]]; lo = np.minimum(lo, r["bbox_min"]); hi = np.maximum(hi, r["bbox_max"]); n += 1
    return {"objects": n, "min_m": lo.tolist(), "max_m": hi.tolist(), "size_m": (hi - lo).tolist()}

EXT = ["EXT_masses_and_roof", "EXT_parapets", "EXT_glazing", "EXT_canopy_dropoff_glass",
       "EXT_canopy_dropoff_steel", "EXT_canopy_door_side", "EXT_sunshade", "EXT_glass_railings",
       "EXT_utility_yard_walls", "EXT_mullions_frames", "EXT_doors"]
SITE = ["SITE_terrain", "SITE_hardscape_stairs_walls", "SITE_beds_lawn", "SITE_detail", "VEG_plants"]
extents = {
    "building_masses_only": extent(["EXT_masses_and_roof"]),
    "building_exterior_all": extent(EXT),
    "building_plus_site_pad": extent(EXT + SITE),
    "site_terrain_only": extent(["SITE_terrain"]),
    "building_site_plus_parking_context_detail": extent(EXT + SITE + ["SITE_detail_parking_context"]),
    "interior_base_building": extent(["INTERIOR_base_building"]),
    "everything_incl_context": extent(EXT + SITE + ["SITE_detail_parking_context", "CONTEXT_offsite"]),
}

def fit(size_m, scale):
    mm = [s * 1000.0 / scale for s in size_m]
    bv = PRINTER["build_volume_mm"]; mg = PRINTER["planning_margin_mm"]
    xy = sorted(mm[:2], reverse=True)
    fits_raw = (xy[0] <= max(bv[:2]) and xy[1] <= min(bv[:2]) and mm[2] <= bv[2])
    fits_m = (xy[0] <= max(bv[:2]) - mg and xy[1] <= min(bv[:2]) - mg and mm[2] <= bv[2] - mg)
    return {"mm": [round(v, 1) for v in mm], "fits_build_volume": fits_raw, "fits_with_margin": fits_m}

scale_table = {k: {f"1:{s}": fit(v["size_m"], s) for s in SCALES} for k, v in extents.items() if v["objects"]}

# ------------------------------------------------------------------ floating / support analysis
PRINT_SET = EXT + SITE
cand = [n for n in data if not data[n].get("empty") and category(bpy.data.objects[n]) in PRINT_SET]
bvh = {}
def get_bvh(n):
    if n not in bvh:
        r = data[n]
        bvh[n] = BVHTree.FromPolygons([tuple(v) for v in r["_w"]], [tuple(t) for t in r["_tv"]], epsilon=0.0)
    return bvh[n]
bb = {n: (np.array(data[n]["bbox_min"]) - CONTACT_TOL, np.array(data[n]["bbox_max"]) + CONTACT_TOL) for n in cand}
adj = defaultdict(set)
pairs_checked = 0
for i, a in enumerate(cand):
    a0, a1 = bb[a]
    for b in cand[i + 1:]:
        b0, b1 = bb[b]
        if (a0 <= b1).all() and (b0 <= a1).all():
            pairs_checked += 1
            ta_, tb_ = get_bvh(a), get_bvh(b)
            touch = bool(ta_.overlap(tb_))
            if not touch:
                for src, dst in ((a, tb_), (b, ta_)):
                    vs = data[src]["_w"]
                    step = max(1, len(vs) // 1500)
                    for v in vs[::step]:
                        hit = dst.find_nearest(tuple(v), CONTACT_TOL)
                        if hit[0] is not None:
                            touch = True; break
                    if touch: break
            if touch:
                adj[a].add(b); adj[b].add(a)
roots = [n for n in ("Site_Terrain_INTERPOLATED", "Site_Foundation_skirt_podium", "L1_Podium") if n in data]
seen, stack = set(roots), list(roots)
while stack:
    x = stack.pop()
    for y in adj[x]:
        if y not in seen:
            seen.add(y); stack.append(y)
floating = sorted(n for n in cand if n not in seen)
isolated = sorted(n for n in cand if not adj[n])
print(f"[audit] contact pairs checked {pairs_checked}, floating {len(floating)} in {time.time()-T0:.1f}s")

# ------------------------------------------------------------------ per-category summary
def cat_summary():
    out = {}
    by = defaultdict(list)
    for row in rows: by[row["category"]].append(row)
    for cat, rs in sorted(by.items()):
        ms = [data[r["name"]] for r in rs if r["name"] in data and not data[r["name"]].get("empty")]
        s = {"objects": len(rs), "mesh_objects": len(ms),
             "types": dict(Counter(r["type"] for r in rs)),
             "hidden_viewport": sum(r["hide_viewport"] for r in rs),
             "hidden_render": sum(r["hide_render"] for r in rs)}
        if ms:
            th = np.array([m["min_thickness_m"] for m in ms])
            s.update({
                "tris": int(sum(m["tris"] for m in ms)),
                "watertight_objects": int(sum(m["watertight"] for m in ms)),
                "objects_with_boundary_edges": int(sum(m["boundary_edges"] > 0 for m in ms)),
                "boundary_edges": int(sum(m["boundary_edges"] for m in ms)),
                "nonmanifold_edges_gt2": int(sum(m["nonmanifold_edges_gt2"] for m in ms)),
                "flipped_winding_edges": int(sum(m["flipped_winding_edges"] for m in ms)),
                "zero_area_faces": int(sum(m["zero_area_faces"] for m in ms)),
                "zero_thickness_objects": int(sum(m["zero_thickness_islands"] > 0 for m in ms)),
                "inverted_islands": int(sum(m["inverted_islands"] for m in ms)),
                "islands": int(sum(m["islands"] for m in ms)),
                "min_thickness_m": float(th.min()), "median_thickness_m": float(np.median(th)),
                "max_thickness_m": float(th.max()),
            })
            for sc in SCALES:
                mm = th * 1000.0 / sc
                s[f"thinnest_mm_1:{sc}"] = round(float(mm.min()), 3)
                s[f"objects_below_0.8mm_1:{sc}"] = int((mm < 0.8).sum())
                s[f"objects_below_1.2mm_1:{sc}"] = int((mm < 1.2).sum())
            fl = [r["name"] for r in rs if r["name"] in floating]
            if cat in PRINT_SET:
                s["floating_objects"] = len(fl)
                s["floating_examples"] = fl[:12]
        out[cat] = s
    return out

summary = {
    "audit": "Building II print audit v001 (read-only; file not saved)",
    "blend": BLEND,
    "blender_version": bpy.app.version_string,
    "units": {"system": bpy.context.scene.unit_settings.system,
              "length_unit_display": bpy.context.scene.unit_settings.length_unit,
              "scale_length": bpy.context.scene.unit_settings.scale_length,
              "geometry_storage": "metres (Blender units); build scripts convert with FT = 0.3048"},
    "printer": PRINTER,
    "object_counts": dict(Counter(o.type for o in objs)),
    "extents": extents,
    "scale_fit": scale_table,
    "categories": cat_summary(),
    "support_analysis": {"method": "true mesh contact (BVH overlap, or any vertex within 1 cm of the other surface) "
                                   "among exterior+site print-candidate objects; grounded = connected to terrain/foundation skirt/podium",
                         "candidates": len(cand), "pairs_checked": pairs_checked,
                         "floating_count": len(floating), "floating": floating,
                         "isolated_no_contact_count": len(isolated)},
    "modifiers": dict(Counter(m.type for o in objs for m in o.modifiers)),
    "runtime_s": round(time.time() - T0, 1),
}
# ------------------------------------------------------------------ targeted probes
from mathutils import Vector
def combined_bvh(names):
    V, T, off = [], [], 0
    for n in names:
        r = data[n]; V.extend(tuple(v) for v in r["_w"]); T.extend(tuple(int(i) + off for i in t) for t in r["_tv"]); off += len(r["_w"])
    return BVHTree.FromPolygons(V, T, epsilon=0.0)
names_by_cat = defaultdict(list)
for row in rows:
    if row["name"] in data and not data[row["name"]].get("empty"):
        names_by_cat[row["category"]].append(row["name"])
probes = {}
# (a) masses
probes["masses"] = {n: {"min_m": [round(x, 3) for x in data[n]["bbox_min"]], "max_m": [round(x, 3) for x in data[n]["bbox_max"]]}
                    for n in names_by_cat["EXT_masses_and_roof"]}
# (b) which objects set the exterior extents
ext_names = [n for c in EXT for n in names_by_cat[c]]
probes["exterior_extreme_objects"] = {
    f"{'min' if k == 0 else 'max'}_{'xyz'[ax]}": (min if k == 0 else max)(ext_names, key=lambda n: data[n]["bbox_min" if k == 0 else "bbox_max"][ax])
    for ax in range(3) for k in (0, 1)}
# (c) glazing recess and (d) mullion projection
mass_bvh = combined_bvh(names_by_cat["EXT_masses_and_roof"])
def thin_axis(n):
    w = data[n]["_w"]; ext = w.max(0) - w.min(0)
    ax = int(np.argmin(ext[:2])); v = np.zeros(3); v[ax] = 1.0
    return v, (w.max(0) + w.min(0)) / 2, ext
glass = {}
for n in names_by_cat["EXT_glazing"]:
    nrm, c, ext = thin_axis(n)
    inplane = np.array([nrm[1], nrm[0], 0.0])
    hw = float(ext @ np.abs(inplane)) / 2; hh = float(ext[2]) / 2
    fs = []
    for off in (inplane * (hw + 0.12), -inplane * (hw + 0.12), np.array([0, 0, hh + 0.12]), np.array([0, 0, -(hh + 0.12)])):
        p = c + off
        for sgn in (1, -1):
            o = p + sgn * nrm * 3.0
            hit = mass_bvh.ray_cast(Vector(o), Vector(-sgn * nrm), 6.0)
            if hit[0] is not None:
                fs.append(float((np.array(hit[0]) - c) @ nrm))
    if fs:
        f = float(np.median(fs)); glass[n] = {"normal": nrm, "c": c, "facade_offset_m": f, "out": 1.0 if f > 0 else -1.0,
                                              "recess_m": abs(f)}
probes["glazing_recess_m"] = {n: round(g["recess_m"], 4) for n, g in glass.items()}
mull = {}
gnames = list(glass)
gcent = np.array([glass[g]["c"] for g in gnames]) if gnames else np.zeros((0, 3))
for n in names_by_cat["EXT_mullions_frames"] + names_by_cat["EXT_doors"]:
    w = data[n]["_w"]; c = (w.max(0) + w.min(0)) / 2
    if not len(gcent): break
    g = glass[gnames[int(np.argmin(np.linalg.norm(gcent - c, axis=1)))]]
    proj = (w - g["c"]) @ g["normal"] * g["out"]           # + = outward from glass centre
    mull[n] = {"proud_of_glass_m": round(float(proj.max()) - 0.0076, 4),
               "proud_of_facade_m": round(float(proj.max()) - g["recess_m"], 4),
               "face_width_m": round(float(sorted((w.max(0) - w.min(0)))[1]), 4)}
probes["mullions_frames"] = mull
# (e) canopy glass gap to steel
steel = names_by_cat["EXT_canopy_dropoff_steel"]
if steel:
    sb = combined_bvh(steel)
    probes["canopy_glass_gap_to_steel_m"] = {n: round(min(sb.find_nearest(Vector(v))[3] for v in data[n]["_w"]), 4)
                                             for n in names_by_cat["EXT_canopy_dropoff_glass"]}
# (f,g) plants / beds / drains: gap between object bottom and ground below its centre
ground = names_by_cat["SITE_terrain"] + names_by_cat["SITE_hardscape_stairs_walls"] + names_by_cat["SITE_beds_lawn"]
def ground_gap(n, excl):
    gb = combined_bvh([g for g in ground if g != excl])
    return gb
gb_all = combined_bvh(ground)
def gap(n):
    w = data[n]["_w"]; c = (w.max(0) + w.min(0)) / 2
    top = w[:, 2].max() + 0.001
    best = None
    for o in (c, c + [0.05, 0, 0], c - [0.05, 0, 0], c + [0, 0.05, 0], c - [0, 0.05, 0]):
        hit = gb_all.ray_cast(Vector((o[0], o[1], top)), Vector((0, 0, -1)), 50.0)
        # skip self hits for ground-category objects
        if hit[0] is not None:
            gz = hit[0][2]
            if best is None or gz > best: best = gz
    return None if best is None else float(w[:, 2].min() - best)
vg = {n: gap(n) for n in names_by_cat["VEG_plants"]}
vv = np.array([v for v in vg.values() if v is not None])
probes["vegetation"] = {
    "objects": len(vg), "tris": int(sum(data[n]["tris"] for n in vg)), "islands": int(sum(data[n]["islands"] for n in vg)),
    "bottom_gap_to_ground_m": {"min": float(vv.min()), "median": float(np.median(vv)), "max": float(vv.max()),
                                "count_gap_gt_1cm": int((vv > 0.01).sum()), "count_embedded_lt_-1cm": int((vv < -0.01).sum())},
    "height_m": {"min": float(min(data[n]["bbox_max"][2] - data[n]["bbox_min"][2] for n in vg)),
                 "max": float(max(data[n]["bbox_max"][2] - data[n]["bbox_min"][2] for n in vg))},
    "plan_size_m": {"min": float(min(max(np.array(data[n]["bbox_max"][:2]) - data[n]["bbox_min"][:2]) for n in vg)),
                    "max": float(max(max(np.array(data[n]["bbox_max"][:2]) - data[n]["bbox_min"][:2]) for n in vg))},
}
others = {}
for n in names_by_cat["SITE_detail"] + names_by_cat["SITE_beds_lawn"]:
    w = data[n]["_w"]; c = (w.max(0) + w.min(0)) / 2
    gb = combined_bvh([g for g in ground if g != n])
    hit = gb.ray_cast(Vector((c[0], c[1], w[:, 2].max() + 0.001)), Vector((0, 0, -1)), 50.0)
    others[n] = None if hit[0] is None else round(float(w[:, 2].min() - hit[0][2]), 4)
probes["site_detail_bottom_gap_m"] = others
# (h) interior enclosed in the solid masses
mlo = np.min([data[n]["bbox_min"] for n in names_by_cat["EXT_masses_and_roof"]], axis=0)
mhi = np.max([data[n]["bbox_max"] for n in names_by_cat["EXT_masses_and_roof"]], axis=0)
enc = {}
for cat in ("INTERIOR_base_building", "INTERIOR_lobby", "INTERIOR_tenant_concept", "INTERIOR_hollow_shell_alt"):
    ns = names_by_cat[cat]
    inside = sum(1 for n in ns if (np.array(data[n]["bbox_min"]) >= mlo - 0.05).all() and (np.array(data[n]["bbox_max"]) <= mhi + 0.05).all())
    enc[cat] = {"objects": len(ns), "within_building_envelope_bbox": inside}
probes["interior_enclosure"] = enc
slab = [n for n in data if n.startswith("INT_L2_slab")]
probes["level2_slab"] = {n: {"z_min": round(data[n]["bbox_min"][2], 4), "z_max": round(data[n]["bbox_max"][2], 4)} for n in slab}
# (i) rotated fit of footprints on the H2S bed
def rotated_fit(a, b, A=340.0, B=320.0, margin=0.0):
    A -= margin; B -= margin
    for deg in np.arange(0, 90.01, 0.25):
        t = math.radians(deg); w_ = a * math.cos(t) + b * math.sin(t); h_ = a * math.sin(t) + b * math.cos(t)
        if (w_ <= A and h_ <= B) or (w_ <= B and h_ <= A):
            return float(deg)
    return None
probes["rotated_fit_deg"] = {k: {f"1:{s}": {"raw": rotated_fit(*(np.array(v["size_m"][:2]) * 1000 / s)),
                                            "margin10": rotated_fit(*(np.array(v["size_m"][:2]) * 1000 / s), margin=10.0)}
                                 for s in SCALES} for k, v in extents.items() if v["objects"]}
summary["probes"] = probes
os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, "print_audit_v001.json"), "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=1)
keys = []
for r in rows:
    for k in r:
        if k not in keys: keys.append(k)
keys.append("floating")
with open(os.path.join(OUT, "print_audit_v001_objects.csv"), "w", newline="", encoding="utf-8") as f:
    wr = csv.DictWriter(f, fieldnames=keys)
    wr.writeheader()
    for r in rows:
        r["floating"] = r["name"] in floating
        wr.writerow(r)
print(f"[audit] done in {time.time()-T0:.1f}s; is_dirty={bpy.data.is_dirty} (never saved)")
