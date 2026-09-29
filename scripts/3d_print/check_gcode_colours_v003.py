"""Building II print v003 - does the SLICED G-code print each facade point in the intended filament? (read-only)

Run:  python scripts/3d_print/check_gcode_colours_v003.py
Input : <system temp>/rea_farms_II_bambu_cli_v003/multicolor_building/sliced_check.3mf (from validate_export_v003.py - Bambu Studio CLI,
        system H2S 0.4 / 0.12 mm High Quality, four flattened filaments) and validation/print_validation_v003_samples.npz
        (area-weighted facade samples with the colour intended by the model and the colour of the v023 finish there).
Method: the G-code is parsed into OUTER-WALL extrusion segments per layer with the active filament (M1020 S<n>:
        S0 = slot 1 White, S1 = 2 Black, S2 = 3 Gray, S3 = 4 Clear). Every wall sample (|normal z| < 0.3) is mapped to
        printed millimetres with the export's item transform; the nearest outer-wall segment on its layer (<= 0.35 mm)
        gives the filament that the printer will actually lay on that spot.
Writes validation/print_gcode_colour_check_v003.json
"""
import json, os, re, zipfile
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
VAL = os.path.join(ROOT, "exports", "Building_II", "3d_print", "validation")
K = 1000.0 / 240.0
FIL = {0: "WHITE", 1: "BLACK", 2: "GRAY", 3: "CLEAR"}
import tempfile
# run validate_export_v003.py first: it writes the sliced check project to the system temp folder (outside the project)
g = zipfile.ZipFile(os.path.join(tempfile.gettempdir(), "rea_farms_II_bambu_cli_v003", "multicolor_building", "sliced_check.3mf")).read("Metadata/plate_1.gcode").decode(errors="ignore")
segs = {}                                   # layer top z -> list of (x0, y0, x1, y1, fil)
fil, z, feat, x, y = None, 0.0, "", None, None
rx = re.compile(r"X(-?[\d.]+)"); ry = re.compile(r"Y(-?[\d.]+)"); re_ = re.compile(r"E(-?[\d.]+)")
for line in g.splitlines():
    if line.startswith("M1020 S"):
        fil = int(line[7:].split()[0])
    elif line.startswith("; Z_HEIGHT:"):
        z = float(line.split(":")[1])
    elif line.startswith("; FEATURE:"):
        feat = line[10:].strip()
    elif line.startswith(("G1 ", "G0 ", "G2 ", "G3 ")):
        mx, my, me = rx.search(line), ry.search(line), re_.search(line)
        nx = float(mx.group(1)) if mx else x; ny = float(my.group(1)) if my else y
        if me and float(me.group(1)) > 0 and feat in ("Outer wall", "Overhang wall") and x is not None and fil is not None and line.startswith("G1"):
            segs.setdefault(round(z, 3), []).append((x, y, nx, ny, fil))
        x, y = nx, ny
layers = np.array(sorted(segs)); S = {k: np.array(v) for k, v in segs.items()}
d = np.load(os.path.join(VAL, "print_validation_v003_samples.npz"))
P, N, EFF, EXP = d["P"], d["N"], d["EFF"], d["EXP"]
T = json.load(open(os.path.join(VAL, "print_export_v003_written.json")))["files"]["multicolor_building"]["transform"]
M = np.array(T[:9]).reshape(3, 3); t = np.array(T[9:])
walls = np.abs(N[:, 2]) < 0.3
Q0 = (P[walls] * K) @ M + t; eff = EFF[walls]; exp = EXP[walls]
# Bambu Studio may re-orient the object on load (the CLI turned the building 90 deg about its centre on the H2S plate):
# find the rigid rotation about the footprint centre that puts the samples on the printed walls
allseg = np.vstack(list(S.values()))
gc = np.array([(allseg[:, [0, 2]].min() + allseg[:, [0, 2]].max()) / 2, (allseg[:, [1, 3]].min() + allseg[:, [1, 3]].max()) / 2])
body_mm = (P * K) @ M + t
qc = (body_mm[:, :2].min(0) + body_mm[:, :2].max(0)) / 2
def locate(Q):
    out = []
    for q in Q:
        i = np.searchsorted(layers, q[2] - 1e-6)
        if i >= len(layers):
            out.append(None); continue
        s = S[layers[i]]
        a, b = s[:, :2], s[:, 2:4]; ab = b - a; L2 = (ab ** 2).sum(1); L2[L2 == 0] = 1e-12
        u = np.clip(((q[:2] - a) * ab).sum(1) / L2, 0, 1); dd = np.linalg.norm(a + u[:, None] * ab - q[:2], axis=1)
        j = int(np.argmin(dd))
        out.append((FIL[int(s[j, 4])], float(dd[j])) if dd[j] <= 0.35 else None)
    return out
best = None
for ang in (0, 90, -90, 180):
    c, s_ = np.cos(np.radians(ang)), np.sin(np.radians(ang)); Rz = np.array([[c, -s_], [s_, c]])
    Q = Q0.copy(); Q[:, :2] = (Q0[:, :2] - qc) @ Rz.T + gc
    trial = locate(Q[::25])
    n_ok = sum(1 for r in trial if r is not None)
    if best is None or n_ok > best[0]:
        best = (n_ok, ang, Q)
ROT_DEG = best[1]; res = locate(best[2])
hit = [(r, e1, e2) for r, e1, e2 in zip(res, eff, exp) if r is not None]
def agree(pairs):
    return round(100.0 * sum(1 for a, b in pairs if a == b) / max(1, len(pairs)), 2)
conf = {}
for r, e1, e2 in hit:
    conf.setdefault(e2, {}).setdefault(r[0], 0); conf[e2][r[0]] += 1
REP = dict(outer_wall_segments=int(sum(len(v) for v in S.values())), layers=int(len(layers)), wall_samples=int(walls.sum()),
           bambu_reoriented_object_deg=ROT_DEG,
           matched_to_an_outer_wall_within_0p35mm=len(hit),
           gcode_vs_model_intended_pct=agree([(r[0], e1) for r, e1, e2 in hit]),
           gcode_vs_v023_finish_pct=agree([(r[0], e2) for r, e1, e2 in hit if e2 != "UNMATCHED"]),
           confusion_v023_finish_to_gcode_filament=conf,
           filament_code="M1020 S0..S3 = slot 1 White, 2 Black, 3 Gray, 4 Clear")
json.dump(REP, open(os.path.join(VAL, "print_gcode_colour_check_v003.json"), "w"), indent=1)
print(json.dumps(REP, indent=1))
