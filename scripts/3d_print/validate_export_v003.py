"""Building II print v003 (multicolor) - independent validation of the exported 3MF files + Bambu Studio CLI slice test.
Pure Python + numpy (system Python); reads every file FROM DISK. Never touches a .blend.

Run:  python scripts/3d_print/validate_export_v003.py            (add --no-slice to skip the Bambu CLI)
Checks per 3MF: structure (generic 3MF + Metadata/model_settings.config), part names / order / filament per part,
per-part closed shells (every edge used by exactly two triangles, consistent orientation), placement on the H2S bed
(340 x 320, lowest point Z = 0), and the four v002 base parts compared vertex-for-vertex and triangle-for-triangle with
the printed v002 3MF files (after each file's own item transform).
Bambu CLI: slices each file with the SYSTEM H2S 0.4 machine + 0.12 mm High Quality process and four flattened filaments
(PLA Matte White / Black / Gray, PLA Translucent Clear - colour only overridden); records per-filament grams, filament
changes, time; extracts Bambu's own plate renders into validation/previews_v003/bambu_*.png.
Writes exports/Building_II/3d_print/validation/print_export_v003_validation.json
"""
import hashlib, json, os, re, subprocess, sys, zipfile
import xml.etree.ElementTree as ET
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import bambu_3mf_v003 as B3
EXP = os.path.join(ROOT, "exports", "Building_II", "3d_print"); MF = os.path.join(EXP, "3mf"); VAL = os.path.join(EXP, "validation")
import tempfile
PRE = os.path.join(VAL, "previews_v003")
# CLI working files (sliced check projects + G-code, ~450 MB, NOT printable: the CLI leaves the machine change-filament
# template unresolved) stay OUTSIDE the project; the results are recorded in print_export_v003_validation.json
WORK = os.path.join(tempfile.gettempdir(), "rea_farms_II_bambu_cli_v003")
os.makedirs(WORK, exist_ok=True)
NS = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02", "p": "http://schemas.microsoft.com/3dmanufacturing/production/2015/06"}
BED = (340.0, 320.0, 340.0)
def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

def parse_mesh(el):
    vs = el.findall("m:mesh/m:vertices/m:vertex", NS); ts = el.findall("m:mesh/m:triangles/m:triangle", NS)
    co = np.array([[float(v.get("x")), float(v.get("y")), float(v.get("z"))] for v in vs])
    tv = np.array([[int(t.get("v1")), int(t.get("v2")), int(t.get("v3"))] for t in ts], dtype=np.int64)
    return co, tv
def T34(s):
    t = [float(x) for x in s.split()]
    return np.array(t[:9]).reshape(3, 3), np.array(t[9:])            # 3MF: v' = v * M (rows), then + t
def apply(co, T):
    M, t = T; return co @ M + t

def read_multipart(p):
    z = zipfile.ZipFile(p); root = ET.fromstring(z.read("3D/3dmodel.model"))
    subs = {}
    for n in z.namelist():
        if n.startswith("3D/Objects/") and n.endswith(".model"):
            sr = ET.fromstring(z.read(n))
            for o in sr.findall("m:resources/m:object", NS):
                subs[o.get("id")] = parse_mesh(o)
    cfg = ET.fromstring(z.read("Metadata/model_settings.config"))
    part_cfg = {pp.get("id"): {m.get("key"): m.get("value") for m in pp.findall("metadata")} for pp in cfg.iter("part")}
    objs = []
    for o in root.findall("m:resources/m:object", NS):
        comps = o.findall("m:components/m:component", NS)
        if not comps:
            continue
        parts = []
        for c in comps:
            pid = c.get("objectid"); co, tv = subs[pid]
            parts.append(dict(id=pid, name=part_cfg[pid]["name"], extruder=int(part_cfg[pid]["extruder"]), co=co, tv=tv))
        objs.append(dict(id=o.get("id"), parts=parts))
    items = {i.get("objectid"): T34(i.get("transform")) for i in root.findall("m:build/m:item", NS)}
    meta = {m.get("name"): m.text for m in root.findall("m:metadata", NS)}
    return dict(objects=objs, items=items, meta=meta, files=z.namelist())

def read_plain(p):
    z = zipfile.ZipFile(p); root = ET.fromstring(z.read("3D/3dmodel.model"))
    o = root.find("m:resources/m:object", NS); co, tv = parse_mesh(o)
    return co, tv, T34(root.find("m:build/m:item", NS).get("transform"))

def shell_checks(co, tv):
    e = np.concatenate([tv[:, [0, 1]], tv[:, [1, 2]], tv[:, [2, 0]]])
    und = np.sort(e, axis=1); _, cnt = np.unique(und, axis=0, return_counts=True); _, dcnt = np.unique(e, axis=0, return_counts=True)
    p0, p1, p2 = co[tv[:, 0]], co[tv[:, 1]], co[tv[:, 2]]
    area = 0.5 * np.linalg.norm(np.cross(p1 - p0, p2 - p0), axis=1)
    lab = np.arange(len(co))
    while True:
        old = lab.copy(); m = np.minimum(lab[und[:, 0]], lab[und[:, 1]]); np.minimum.at(lab, und[:, 0], m); np.minimum.at(lab, und[:, 1], m); lab = lab[lab]
        if np.array_equal(lab, old):
            break
    tl = lab[tv[:, 0]]
    vols = np.bincount(tl, weights=np.einsum("ij,ij->i", p0, np.cross(p1, p2)) / 6.0, minlength=len(co))
    shells = np.unique(tl)
    return dict(triangles=int(len(tv)), shells=int(len(shells)), open_edges=int((cnt == 1).sum()), nonmanifold_edges=int((cnt > 2).sum()),
                orientation_conflicts=int((dcnt > 1).sum()), degenerate_triangles=int((area < 1e-10).sum()),
                negative_volume_shells=int((vols[shells] < -1e-9).sum()), volume_mm3=round(float(vols[shells].sum()), 3))

REP = {"files": {}}
FILES = {"multicolor_building": ["1 body", "2 white", "3 black", "4 glazing", "5 storefront"], "dropoff_canopy": ["1 canopy", "2 canopy glass"],
         "sunshade": ["sun-shade"], "site_base": ["site base"]}
EXPECT_EXT = {"multicolor_building": [3, 1, 2, 4, 3], "dropoff_canopy": [3, 4], "sunshade": [1], "site_base": [3]}
V002 = {"multicolor_building": "building_body", "dropoff_canopy": "dropoff_canopy", "sunshade": "sunshade", "site_base": "site_base"}
for comp in FILES:
    p = os.path.join(MF, f"building_II_v003_1-240_{comp}.3mf"); r = read_multipart(p)
    ob = r["objects"][0]; T = r["items"][ob["id"]]
    parts = []
    allco = []
    for part in ob["parts"]:
        c = shell_checks(part["co"], part["tv"]); w = apply(part["co"], T); allco.append(w)
        parts.append(dict(name=part["name"], filament=part["extruder"], **c))
    W = np.vstack(allco); lo, hi = W.min(0), W.max(0)
    # base part vs the printed v002 file
    co2, tv2, T2 = read_plain(os.path.join(MF, f"building_II_v002_1-240_{V002[comp]}.3mf"))
    b = ob["parts"][0]; wb = apply(b["co"], T); w2 = apply(co2, T2)
    same_tri = b["tv"].shape == tv2.shape and np.array_equal(b["tv"], tv2)
    dv = float(np.abs(wb - w2).max()) if wb.shape == w2.shape else None
    REP["files"][comp] = dict(
        path=os.path.relpath(p, ROOT), sha256=sha(p), generic_3mf="Application" not in r["meta"],
        has_model_settings="Metadata/model_settings.config" in r["files"], objects=len(r["objects"]),
        part_order_ok=[pp["name"].split(" - ")[0] for pp in parts] == [pp["name"].split(" - ")[0] for pp in parts] and
                      all(pp["name"].startswith(pref) for pp, pref in zip(parts, FILES[comp])),
        filaments_ok=[pp["filament"] for pp in parts] == EXPECT_EXT[comp], parts=parts,
        on_bed=dict(min_mm=lo.round(3).tolist(), max_mm=hi.round(3).tolist(), size_mm=(hi - lo).round(3).tolist(),
                    inside_bed=bool(lo[0] >= 0 and lo[1] >= 0 and hi[0] <= BED[0] and hi[1] <= BED[1] and hi[2] <= BED[2]), z_min_mm=round(float(lo[2]), 6)),
        base_part_vs_printed_v002=dict(v002_file=f"building_II_v002_1-240_{V002[comp]}.3mf", same_triangles=bool(same_tri),
                                       max_vertex_diff_mm=dv, identical=bool(same_tri and dv is not None and dv < 2e-5)))
    print("[export-check]", comp, REP["files"][comp]["filaments_ok"], REP["files"][comp]["on_bed"]["size_mm"], REP["files"][comp]["base_part_vs_printed_v002"])

# ---------------------------------------------------------------- Bambu Studio CLI
EXE = r"C:\Program Files\Bambu Studio\bambu-studio.exe"
SYS = os.path.join(os.environ.get("APPDATA", ""), "BambuStudio", "system", "BBL")
if "--no-slice" not in sys.argv and os.path.exists(EXE):
    sysm = os.path.join(SYS, "machine", "Bambu Lab H2S 0.4 nozzle.json"); sysp = os.path.join(SYS, "process", "0.12mm High Quality @BBL H2S.json")
    FIL = [("Bambu PLA Matte @BBL H2S", "#FFFFFF", "White"), ("Bambu PLA Matte @BBL H2S", "#000000", "Black"),
           ("Bambu PLA Matte @BBL H2S", "#8E9089", "Gray"), ("Bambu PLA Translucent @BBL H2S", "#DDEBF2", "Clear")]
    flat = []
    for i, (name, col, lab) in enumerate(FIL, 1):
        j = B3._load_chain(SYS, "filament", name); j.pop("inherits", None); j["filament_colour"] = [col]
        fp = os.path.join(WORK, f"filament_slot{i}_{lab}.json"); json.dump(j, open(fp, "w"), indent=1); flat.append(fp)
    ver = None
    REP["bambu_cli"] = dict(machine="Bambu Lab H2S 0.4 nozzle (system)", process="0.12mm High Quality @BBL H2S (system)",
                            filaments={f"slot {i}": f"{n} - colour {c} ({l})" for i, (n, c, l) in enumerate(FIL, 1)}, results={})
    for comp in FILES:
        src = os.path.join(MF, f"building_II_v003_1-240_{comp}.3mf"); o = os.path.join(WORK, comp); os.makedirs(o, exist_ok=True)
        rp = os.path.join(o, "result.json")
        if os.path.exists(rp):
            os.remove(rp)
        pr = subprocess.run([EXE, "--slice", "0", "--load-settings", f"{sysm};{sysp}", "--load-filaments", ";".join(flat),
                             "--outputdir", o, "--export-3mf", "sliced_check.3mf", src], capture_output=True, text=True, timeout=3600)
        res = json.load(open(rp)) if os.path.exists(rp) else None
        entry = dict(return_code=pr.returncode, result=None)
        if res:
            pl = res.get("sliced_plates", [{}])[0]
            entry.update(result=res.get("error_string"), cli_return_code=res.get("return_code"),
                         filament_used_g={f"slot {f['id']}": round(f["total_used_g"], 2) for f in pl.get("filaments", [])})
            sz = os.path.join(o, "sliced_check.3mf")
            if os.path.exists(sz):
                z = zipfile.ZipFile(sz)
                si = z.read("Metadata/slice_info.config").decode(errors="ignore")
                m = re.search(r'key="prediction" value="(\d+)"', si); entry["predicted_time_h"] = round(int(m.group(1)) / 3600, 2) if m else None
                m = re.search(r'key="weight" value="([\d.]+)"', si); entry["weight_g"] = float(m.group(1)) if m else None
                g = z.read("Metadata/plate_1.gcode").decode(errors="ignore")
                hdr = "\n".join(g.splitlines()[:300])
                m = re.search(r"; total filament change: (\d+)", hdr) or re.search(r"filament change times[^\d]*(\d+)", hdr)
                entry["filament_changes"] = int(m.group(1)) if m else pl.get("filament_change_times")
                m = re.search(r"; total layers count = (\d+)", g) or re.search(r"; total layer number: (\d+)", hdr)
                entry["layers"] = int(m.group(1)) if m else None
                for n_, tag in (("Metadata/plate_1.png", "plate"), ("Metadata/top_1.png", "top")):
                    if n_ in z.namelist():
                        open(os.path.join(PRE, f"bambu_v003_{comp}_{tag}.png"), "wb").write(z.read(n_))
            entry["filament_change_times"] = pl.get("filament_change_times")
        REP["bambu_cli"]["results"][comp] = entry
        print("[bambu]", comp, entry)
    # reference: the approved single-colour v002 building, same machine / process, gray filament only
    o = os.path.join(WORK, "v002_single_colour_reference"); os.makedirs(o, exist_ok=True); rp = os.path.join(o, "result.json")
    if os.path.exists(rp):
        os.remove(rp)
    subprocess.run([EXE, "--slice", "0", "--load-settings", f"{sysm};{sysp}", "--load-filaments", flat[2], "--outputdir", o,
                    "--export-3mf", "sliced_check.3mf", os.path.join(MF, "building_II_v002_1-240_building_body.3mf")],
                   capture_output=True, text=True, timeout=3600)
    if os.path.exists(rp):
        res = json.load(open(rp)); si = zipfile.ZipFile(os.path.join(o, "sliced_check.3mf")).read("Metadata/slice_info.config").decode(errors="ignore")
        m = re.search(r'key="prediction" value="(\d+)"', si)
        REP["bambu_cli"]["v002_single_colour_building_reference"] = dict(
            result=res.get("error_string"), filament_used_g=round(sum(f["total_used_g"] for f in res["sliced_plates"][0]["filaments"]), 2),
            predicted_time_h=round(int(m.group(1)) / 3600, 2) if m else None)
        print("[bambu] v002 reference", REP["bambu_cli"]["v002_single_colour_building_reference"])
REP["summary"] = dict(all_files_generic_multipart=all(v["generic_3mf"] and v["has_model_settings"] for v in REP["files"].values()),
                      filament_assignment_ok=all(v["filaments_ok"] for v in REP["files"].values()),
                      all_parts_closed=all(pp["open_edges"] == 0 and pp["nonmanifold_edges"] == 0 and pp["orientation_conflicts"] == 0
                                           and pp["negative_volume_shells"] == 0 for v in REP["files"].values() for pp in v["parts"]),
                      all_on_bed=all(v["on_bed"]["inside_bed"] and abs(v["on_bed"]["z_min_mm"]) < 1e-6 for v in REP["files"].values()),
                      base_parts_identical_to_printed_v002=all(v["base_part_vs_printed_v002"]["identical"] for v in REP["files"].values()),
                      bambu_slices_ok=all((r.get("cli_return_code") == 0) for r in REP.get("bambu_cli", {}).get("results", {}).values()) if "bambu_cli" in REP else None)
json.dump(REP, open(os.path.join(VAL, "print_export_v003_validation.json"), "w"), indent=1)
print("[export-check] summary", REP["summary"])
