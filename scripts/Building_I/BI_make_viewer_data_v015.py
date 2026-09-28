"""Building I v015 - build the viewer data JSON and the plan underlays for viewer_BI_v015 (system python + Pillow).

Inputs (all read-only):
  notes/Building_I/BI_interior_base_viewer_v014.json      approved v014 structured data (levels, columns, shafts, stairs, fixed rooms, tenant zones, constraints, areas)
  notes/Building_I/BI_interior_base_data_v014.json        approved v014 build data (wall rectangles, CNSA rectangles, L2 slab rectangles, gallery polygon, columns, doors)
  notes/Building_I/BI_viewer_glb_v015_export_report.json  GLB export report (groups per object, extracted collision primitives, material colours)
  <words html>   pdftotext -bbox-layout output of Rev 14 pages 26-27 (A1.01 / A1.02) -> documented room number + name tags
  <plans dir>    pdftocairo -png -r 150 -f 26 -l 27 renders of the same pages (p-026.png, p-027.png) -> plan underlays (cropped only, never rescaled)
Outputs (refuses to overwrite):
  notes/Building_I/BI_viewer_data_v015.json  and a copy in viewer_BI_v015/data/
  viewer_BI_v015/plans/BI_underlay_L1_A1.01_rev14_150dpi.jpg, BI_underlay_L2_A1.02_rev14_150dpi.jpg
Run:  python scripts/Building_I/BI_make_viewer_data_v015.py <words html> <plans dir>
"""
import json, os, re, sys, shutil, math
from xml.etree import ElementTree as ET
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
N = os.path.join(ROOT, "notes", "Building_I")
VIEWER = os.path.join(ROOT, "viewer_BI_v015")
OUT_JSON = os.path.join(N, "BI_viewer_data_v015.json")
WORDS, PLANS = sys.argv[1], sys.argv[2]
for p in (OUT_JSON, os.path.join(VIEWER, "data", "BI_viewer_data_v015.json")):
    if os.path.exists(p):
        raise SystemExit(f"refusing to overwrite {p}")
V14 = json.load(open(os.path.join(N, "BI_interior_base_viewer_v014.json"), encoding="utf-8"))
D14 = json.load(open(os.path.join(N, "BI_interior_base_data_v014.json"), encoding="utf-8"))
REP = json.load(open(os.path.join(N, "BI_viewer_glb_v015_export_report.json"), encoding="utf-8"))
EX = REP["extract"]
REG = {"L1": (199.81, 6.7500, 1795.91, 6.7502), "L2": (197.71, 6.7500, 1796.00, 6.7502)}     # x_pt = a + b x ; y_pt = c - d y  (v008 grid-bubble fits, RMS 0.027 ft)
def pt_to_ft(level, X, Y):
    a, b, c, d = REG[level]
    return round((X - a) / b, 2), round((c - Y) / d, 2)

# ------------------------------------------------------------------------------------------------------ 1. documented room tags
def room_tags(words_html):
    html = re.sub(r"<!DOCTYPE[^>]*>", "", open(words_html, encoding="utf-8").read()).replace('xmlns="http://www.w3.org/1999/xhtml"', "")
    pages = ET.fromstring(html).findall(".//page")
    assert len(pages) == 2
    rooms = []
    for level, page in zip(("L1", "L2"), pages):
        lines = []
        for line in page.iter("line"):
            ws = line.findall("word")
            lines.append((" ".join(w.text for w in ws), min(float(w.get("xMin")) for w in ws), min(float(w.get("yMin")) for w in ws),
                          max(float(w.get("xMax")) for w in ws), max(float(w.get("yMax")) for w in ws)))
        isnum = lambda t: re.fullmatch(r"[12]\d\d[a-zA-Z]?", t) is not None
        for (num, x0, y0, x1, y1) in [l for l in lines if isnum(l[0])]:
            h = y1 - y0
            if h < 10.5:          # 9 pt = door tags, 4.2 pt = small door tags; room tags are 11.7 pt
                continue
            cx = (x0 + x1) / 2
            name_lines = []
            top = y0
            for _ in range(3):
                cand = [l for l in lines if l[4] <= top + 1 and l[4] >= top - 1.8 * h and l[1] - 2 <= cx <= l[3] + 2
                        and abs((l[4] - l[2]) - h) < 0.5 * h and not isnum(l[0]) and not re.search(r"\d", l[0])]
                if not cand:
                    break
                cand.sort(key=lambda l: -l[4])
                name_lines.insert(0, cand[0][0]); top = cand[0][2]
            name = " ".join(name_lines) if name_lines else None
            x, y = pt_to_ft(level, cx, (y0 + y1) / 2)
            rooms.append({"number": num, "name": name, "level": level, "x": x, "y": y, "source": f"Rev 14 {'A1.01 p.26' if level == 'L1' else 'A1.02 p.27'} room tag (text)"})
    # de-duplicate: a number appearing twice on a page keeps the named one; 121 (courts, double height) is a Level 1 room
    seen = {}
    for r in rooms:
        k = (r["level"], r["number"])
        if k not in seen or (r["name"] and not seen[k]["name"]):
            seen[k] = r
    rooms = [r for k, r in seen.items() if not (k == ("L2", "121"))]
    for r in rooms:
        if r["number"] == "233":
            r["level"] = "MEZZ"; r["note"] = "Sports Science Lab 233 is drawn on the Level 2 plan; its floor is the 13'-0 1/4\" mezzanine (A5.01 / A6.13)"
    return sorted(rooms, key=lambda r: (r["level"], r["number"]))
rooms = room_tags(WORDS)
door_rooms = {d["door"]: d["room"] for d in D14["doors"]}

# ------------------------------------------------------------------------------------------------------ 2. spaces (clickable): zones + tags
LEVEL_Z = {"L1": 0.0, "MEZZ": 13.0208, "L2": 15.3333}
def zone_label(z):
    return z.replace("core_", "").replace("_", " ")
spaces = []
for fr in V14["fixed_rooms"]:
    spaces.append({"id": fr["zone"], "kind": "zone", "name": zone_label(fr["zone"]), "number": None, "level": fr["level"], "category": "BASE BUILDING",
                   "rect": [fr["x0"], fr["x1"], fr["y0"], fr["y1"]], "area_sqft": round((fr["x1"] - fr["x0"]) * (fr["y1"] - fr["y0"])),
                   "boundary": "interpreted (v014 core bounding zone - not a room boundary)", "source": "v014 core_zones (A1.01 / A1.02 room layout)"})
for tz in V14["tenant_zones"]:
    documented = tz["id"] == "CNSA_L1"
    spaces.append({"id": tz["id"], "kind": "zone", "name": {"CNSA_L1": "Existing CNSA - Level 1 (MOB Shell 150-S)", "CNSA_L2": "Existing CNSA - Level 2 (west part of MOB Shell 250-S)",
                                                              "MOB_shell_2300_L2": "MOB Shell 250-S remaining ('SHELL 2300') - available"}[tz["id"]],
                   "number": None, "level": tz["level"], "category": "EXISTING CNSA" if tz["id"].startswith("CNSA") else "BASE BUILDING",
                   "rect": [tz["x0"], tz["x1"], tz["y0"], tz["y1"]],
                   "area_sqft": {"CNSA_L1": V14["areas"]["CNSA_L1_tenant_zone_sqft"], "CNSA_L2": V14["areas"]["CNSA_L2_tenant_zone_sqft"], "MOB_shell_2300_L2": V14["areas"]["MOB_shell_L2_remaining_sqft"]}[tz["id"]],
                   "boundary": "documented (A1.01 MOB Shell 150-S extent between the exterior walls and the corridor 102 south wall)" if documented else "interpreted (east limit x ~185 read from CNSA A100, +-2 ft)",
                   "source": tz.get("note", ""), "status": tz.get("status", "")})
for r in rooms:
    spaces.append({"id": f"tag_{r['level']}_{r['number']}", "kind": "tag", "name": r["name"] or door_rooms.get(r["number"]) or "(name not read)", "number": r["number"], "level": r["level"],
                   "category": "BASE BUILDING", "point": [r["x"], r["y"]], "area_sqft": None,
                   "boundary": "not extracted (documented tag position only)", "source": r["source"], **({"note": r["note"]} if "note" in r else {})})

# ------------------------------------------------------------------------------------------------------ 3. collision primitives (documented solid geometry only)
def col_rect(c):
    d, f = c["depth_ft"], c["flange_ft"]      # web parallel to y (assumption A recorded in v014): depth along y, flange along x
    return [round(c["x"] - f / 2, 3), round(c["x"] + f / 2, 3), round(c["y"] - d / 2, 3), round(c["y"] + d / 2, 3), 0.0, c.get("z_top", 30.0), "column " + c["mark"]]
hw = D14["elevator"]["hoistway_inside"]; t = D14["elevator"]["wall_thickness_ft"]
collision = {
    "note": "all primitives in Building I feet; rect = [x0,x1,y0,y1,z0,z1,label]; segment = [x0,y0,x1,y1,z0,z1]. Documented solid geometry only: no doors or openings were invented - the gaps between the v014 wall rectangles are the openings as drawn on A1.01/A1.02 (door swings interrupt the wall pair); exterior lites are solid (closed); stairs are blocked footprints (not climbable in v015).",
    "walker": {"radius_ft": 1.0, "eye_ft": 5.5, "body_z0_ft": 0.5, "body_z1_ft": 6.5, "substep_ft": 0.2, "speed_ft_s": 9.0, "shift_speed_ft_s": 18.0},
    "walls": {"L1": [[w["x0"], w["x1"], w["y0"], w["y1"], 0.0, 14.79 if w["core"] else 10.0, w["core"] or "partition"] for w in D14["walls_L1"]],
              "L2": [[w["x0"], w["x1"], w["y0"], w["y1"], 15.333, 30.0 if w["core"] else 25.333, w["core"] or "partition"] for w in D14["walls_L2"]]},
    "cnsa": {"L1": [[r[0], r[1], r[2], r[3], 0.0, 10.0, "CNSA partition"] for r in D14["cnsa"]["rects_L1"]],
             "L2": [[r[0], r[1], r[2], r[3], 15.333, 25.333, "CNSA partition"] for r in D14["cnsa"]["rects_L2"]]},
    "columns": [col_rect(c) for c in D14["columns"]],
    "hoistway": [[hw["x0"] - t, hw["x1"] + t, hw["y0"] - t, hw["y1"] + t, -5.0, 33.0, "elevator hoistway (8 in shaft wall)"]],
    "stairs": [[s["bbox"][0], s["bbox"][3], s["bbox"][1], s["bbox"][4], s["bbox"][2], s["bbox"][5] + 7.0, s["name"]] for s in EX["stairs"]],
    "exterior_segments": EX["exterior_inner_face_segments"],
    "opening_lites": [[o["bbox"][0], o["bbox"][3], o["bbox"][1], o["bbox"][4], o["bbox"][2], o["bbox"][5], o["name"]] for o in EX["opening_lites"]],
    "walkable": {
        "L1": {"z": 0.0, "polygons": EX["slab_on_grade_outline_loops"], "source": "v014 BB_L1_slab_on_grade top-face outline (= union of the v008 shell footprints)"},
        "L2": {"z": 15.3333, "rects": [[r[1], r[2], r[3], r[4]] for r in D14["l2_slab_rects"]], "polygons": [D14["gallery_polygon"]], "source": "v014 A1.00b Level 2 edge-of-slab rectangles + gallery polygon"},
        "MEZZ": {"z": 13.0208, "rects": [[EX["mezzanine_slab_bbox"][0], EX["mezzanine_slab_bbox"][3], EX["mezzanine_slab_bbox"][1], EX["mezzanine_slab_bbox"][4]]], "polygons": [], "source": "v014 BB_mezzanine_slab_233 extent (A1.00b clip-3)"},
    },
    "route_origins": {"L1": {"x": 50.0, "y": 70.0, "why": "lobby inside the entry vestibule 100 (main entrance, A1.01)"},
                      "L2": {"x": 86.0, "y": 66.0, "why": "corridor 202 at the elevator (documented vertical circulation: elevator + lobby stair arrive here)"},
                      "MEZZ": {"x": 195.0, "y": 194.0, "why": "mezzanine floor between the east and west mezzanine stairs (A6.13)"}},
}

# ------------------------------------------------------------------------------------------------------ 4. plan underlays (crop only)
S = 150.0 / 72.0
underlays = []
os.makedirs(os.path.join(VIEWER, "plans"), exist_ok=True)
for level, page, sheet in (("L1", "p-026.png", "A1.01"), ("L2", "p-027.png", "A1.02")):
    a, b, c, d = REG[level]
    win = (-25.0, 305.0, -25.0, 225.0)      # ft window around the building
    px0 = int(math.floor((a + b * win[0]) * S)); px1 = int(math.ceil((a + b * win[1]) * S))
    py0 = int(math.floor((c - d * win[3]) * S)); py1 = int(math.ceil((c - d * win[2]) * S))
    im = Image.open(os.path.join(PLANS, page))
    px0, py0 = max(px0, 0), max(py0, 0); px1, py1 = min(px1, im.width), min(py1, im.height)
    crop = im.crop((px0, py0, px1, py1)).convert("RGB")
    out = os.path.join(VIEWER, "plans", f"BI_underlay_{level}_{sheet}_rev14_150dpi.jpg")
    if os.path.exists(out):
        raise SystemExit(f"refusing to overwrite {out}")
    crop.save(out, "JPEG", quality=82, optimize=True)
    # exact ft extents of the integer pixel crop (inverse of the registration; no rescaling anywhere)
    x0 = (px0 / S - a) / b; x1 = (px1 / S - a) / b; y1 = (c - py0 / S) / d; y0 = (c - py1 / S) / d
    underlays.append({"id": sheet, "level": level, "file": f"plans/{os.path.basename(out)}", "x0": round(x0, 4), "x1": round(x1, 4), "y0": round(y0, 4), "y1": round(y1, 4),
                      "px": [crop.width, crop.height], "px_per_ft": [round(b * S, 4), round(d * S, 4)],
                      "source": f"Rev 14 {sheet} (p.{26 if level == 'L1' else 27}) rendered at 150 dpi (pdftocairo), cropped to pixels {px0}-{px1} x {py0}-{py1}; registration = v008 grid-bubble fit x_pt = {a} + {b} x, y_pt = {c} - {d} y (RMS 0.027 ft); no rescaling or distortion applied",
                      "floors": ["L1"] if level == "L1" else ["L2", "MEZZ"]})

# ------------------------------------------------------------------------------------------------------ 5. viewpoints
EYE = 5.5
def vp(id_, label, floor, x, y, lx, ly, lz=None, mode="walk", note=""):
    z = LEVEL_Z[floor] + EYE if floor in LEVEL_Z else 0.0
    return {"id": id_, "label": label, "mode": mode, "floor": floor, "eye": [x, y, round(z, 3)], "look_at": [lx, ly, lz if lz is not None else round(z - 0.3, 3)], "note": note}
viewpoints = [
    vp("vp_lobby", "1. Main entrance lobby (Level 1)", "L1", 33.0, 67.0, 62.0, 59.0, 7.0, note="west end of the double-height lobby band, looking east along the lobby stair (A6.11) toward the core"),
    vp("vp_core_L1", "2. Level 1 core - corridor 102 at the elevator", "L1", 84.0, 66.0, 96.0, 76.0, 5.2, note="corridor 102 looking north-east at the elevator hoistway and elec 103/104"),
    vp("vp_cnsa_L1", "3. Existing CNSA - Level 1 (MOB Shell 150-S)", "L1", 140.0, 30.0, 60.0, 30.0, 5.2, note="middle of the CNSA Level 1 upfit, looking west (CNSA A100 rev 8 partitions when CNSA is ON)"),
    vp("vp_courts", "4. Training courts 121 (Level 1)", "L1", 196.0, 128.0, 196.0, 200.0, 12.0, note="courts floor looking north to the Sports Science Lab 233 mezzanine"),
    vp("vp_L2_office", "5. Level 2 office area (Taylor Capital suite 210-226)", "L2", 86.0, 140.0, 86.0, 100.0, 20.5, note="circulation between the offices 212-216 (west) and Taylor Capital 210 / printer 226 (east), looking south toward reception 222"),
    vp("vp_cnsa_L2", "6. Existing CNSA - Level 2 (MOB Shell 250-S west)", "L2", 100.0, 30.0, 180.0, 30.0, 20.5, note="CNSA Level 2 looking east toward the remaining shell 2300"),
    vp("vp_mezz", "7. Mezzanine - Sports Science Lab 233", "MEZZ", 195.0, 194.0, 195.0, 120.0, 10.0, note="mezzanine floor at 13'-0 1/4\" looking south over the courts"),
    vp("vp_shell_L2", "8. Base-building shell - MOB Shell 250-S east ('SHELL 2300', Level 2)", "L2", 230.0, 30.0, 268.0, 30.0, 20.5, note="unfinished shell east of the CNSA Level 2 upfit: slab, columns, exterior wall inner faces"),
    vp("vp_gallery", "9. Gallery 234 (Level 2)", "L2", 266.0, 104.0, 266.0, 150.0, 20.0, note="west edge of the east gallery (cantilever over the courts east side) looking north along the gallery"),
    {"id": "vp_ext_entrance", "label": "10. Exterior - porte cochere / main entrance (orbit)", "mode": "orbit", "floor": "BOTH", "eye": [-72.0, 212.0, 13.0], "look_at": [40.0, 86.0, 12.0], "note": "v013 hero camera position"},
    {"id": "vp_ext_aerial", "label": "11. Exterior - north-west aerial (orbit)", "mode": "orbit", "floor": "BOTH", "eye": [-140.0, 330.0, 150.0], "look_at": [145.0, 100.0, 10.0], "note": "site overview"},
    {"id": "vp_plan_L1", "label": "12. Plan - Level 1", "mode": "plan", "floor": "L1", "eye": [147.0, 100.0, 300.0], "look_at": [147.0, 100.0, 0.0], "note": ""},
    {"id": "vp_plan_L2", "label": "13. Plan - Level 2", "mode": "plan", "floor": "L2", "eye": [147.0, 100.0, 300.0], "look_at": [147.0, 100.0, 0.0], "note": ""},
]

# ------------------------------------------------------------------------------------------------------ 6. groups / floors / concepts
groups = [
    {"id": "EXTERIOR_SHELL", "label": "Exterior shell / facade", "category": "exterior", "default": True},
    {"id": "EXTERIOR_GLAZING", "label": "Exterior glazing (lite placeholders)", "category": "exterior", "default": True},
    {"id": "ROOF", "label": "Roof (membrane, parapet screens, mech screen)", "category": "exterior", "default": True},
    {"id": "SITE", "label": "Site / paving / terrain", "category": "site", "default": True},
    {"id": "LANDSCAPE", "label": "Landscape (trees, shrubs, beds)", "category": "site", "default": True},
    {"id": "CONTEXT", "label": "Context (roads, Building II mass)", "category": "site", "default": True},
    {"id": "GRID", "label": "Column grid (v001 control)", "category": "reference", "default": False},
    {"id": "BASE_L1", "label": "Base building - Level 1 (slab, core walls, FMK partitions)", "category": "base", "default": True},
    {"id": "BASE_L2", "label": "Base building - Level 2 + mezzanine (slabs, core walls, FMK partitions)", "category": "base", "default": True},
    {"id": "BASE_ENVELOPE", "label": "Base building - exterior wall inner faces + reveals", "category": "base", "default": True},
    {"id": "BASE_VERTICAL", "label": "Base building - stairs, guards, elevator hoistway + pit", "category": "base", "default": True},
    {"id": "STRUCTURE", "label": "Structure - columns (S601) + roof T.O.S. plates", "category": "base", "default": True},
    {"id": "CNSA", "label": "Existing tenant - CNSA (partitions + zone plates)", "category": "tenant", "default": True},
    {"id": "CONCEPT_A", "label": "Future Concept A (empty)", "category": "concept", "default": False},
    {"id": "CONCEPT_B", "label": "Future Concept B (empty)", "category": "concept", "default": False},
    {"id": "CONCEPT_C", "label": "Future Concept C (empty)", "category": "concept", "default": False},
]
floors = [
    {"id": "L1", "label": "Level 1", "z": 0.0, "clip_z": 10.0, "underlay": "A1.01"},
    {"id": "L2", "label": "Level 2", "z": 15.3333, "clip_z": 26.0, "underlay": "A1.02"},
    {"id": "MEZZ", "label": "Mezzanine", "z": 13.0208, "clip_z": 20.5, "underlay": "A1.02"},
    {"id": "BOTH", "label": "Both / Exterior", "z": 0.0, "clip_z": None, "underlay": None},
]
concepts = [
    {"id": "base", "label": "None / Base Building", "groups": [], "empty": False, "note": "v014 base-building condition (BASE_* + STRUCTURE groups)"},
    {"id": "cnsa", "label": "Existing CNSA", "groups": ["CNSA"], "empty": False, "note": "CNSA A100 rev 8 (2/18/2026) partitions and zone plates - separate GLB group, not baked into the base building"},
    {"id": "concept_a", "label": "Concept A (not modeled)", "groups": ["CONCEPT_A"], "empty": True, "note": "empty placeholder - a future tenant plan is modeled in FUTURE_CONCEPTS/Concept_A, re-exported into this group and this entry is switched to empty:false"},
    {"id": "concept_b", "label": "Concept B (not modeled)", "groups": ["CONCEPT_B"], "empty": True, "note": "empty placeholder"},
    {"id": "concept_c", "label": "Concept C (not modeled)", "groups": ["CONCEPT_C"], "empty": True, "note": "empty placeholder"},
]
objects = {name: {"group": o["group"], "level": o["level"]} for name, o in REP["objects"].items()}
data = {
    "meta": {"version": "v015", "date": "2026-09-25", "building": V14["building"], "units": V14["units"], "model": "models/Building_I/BI_interior_base_v014.blend (owner-approved INTERIOR BASE-BUILDING BASELINE, read-only)",
             "glb": REP["glb"], "glb_sha256": REP["glb_sha256"], "glb_bytes": REP["glb_bytes"], "axes": "glTF Y-up metres: three.js (x, y, z) = (X ft, Z ft, -Y ft) x 0.3048 - the viewer scales the scene by 1/0.3048 and converts",
             "coordinate_note": "Building I feet; origin grid 1 x grid A at FFE 661.75; +X east, +Y north; z above LVL-01"},
    "levels": V14["levels"], "floors": floors, "groups": groups, "concepts": concepts, "objects": objects,
    "materials": REP["materials"], "spaces": spaces, "viewpoints": viewpoints, "underlays": underlays, "collision": collision,
    "columns": V14["columns"], "shafts": V14["shafts"], "stairs": V14["stairs"], "areas": V14["areas"], "clear_heights": V14["clear_heights"],
    "constraints": V14["constraints"], "open_items": ["I-1 mezzanine east stair tread count", "I-2 MOB shell inner gypsum by tenant", "I-3 gallery datum 11'-0\" vs Gallery 234", "I-4 braced-frame grid lines by section reading",
                                                       "exterior/site items carried unchanged (G-1..G-6, G-15, F-1..F-9, SC-1, SC-3, LC-2)"],
}
json.dump(data, open(OUT_JSON, "w", encoding="utf-8"), indent=1)
os.makedirs(os.path.join(VIEWER, "data"), exist_ok=True)
shutil.copyfile(OUT_JSON, os.path.join(VIEWER, "data", "BI_viewer_data_v015.json"))
print(f"rooms tags {len(rooms)} (named {sum(1 for r in rooms if r['name'])}), spaces {len(spaces)}, walls L1 {len(collision['walls']['L1'])} L2 {len(collision['walls']['L2'])}, cnsa {len(collision['cnsa']['L1'])}/{len(collision['cnsa']['L2'])}, "
      f"columns {len(collision['columns'])}, ext segs {len(collision['exterior_segments'])}, lites {len(collision['opening_lites'])}, stairs {len(collision['stairs'])}, underlays {[(u['id'], u['px']) for u in underlays]}")
for r in rooms:
    print("  ", r["level"], r["number"], r["name"], r["x"], r["y"])
