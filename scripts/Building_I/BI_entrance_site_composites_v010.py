"""Comparison composites for the v010 entrance-site correction (plain python + Pillow, run with the system python):
  * renders/Building_I/BI_entrance_site_v010_5_before_after_v009_camera.png : v009 entrance oblique (left) | v010 same camera (right)
  * renders/Building_I/BI_entrance_site_v010_overlay_plan_top.png           : the v010 top-down entrance plan with
        blue  = CS-101 rev 13 curb chains (registered vector geometry, the documented curb lines)
        red   = v009 (v003) asphalt outline that was replaced
        green = v010 polygons (drive, island oval outer/inner, paved nose, end island, plaza, walks)
        plus the regrade window (dashed white) and a 20 ft scale bar.
Refuses to overwrite existing outputs.  Run:  python scripts/Building_I/BI_entrance_site_composites_v010.py
"""
import json
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent.parent
R = ROOT / "renders" / "Building_I"
D = json.loads((ROOT / "notes" / "Building_I" / "BI_entrance_site_data_v010.json").read_text(encoding="utf-8"))
CHAINS = Path(sys.argv[1]) if len(sys.argv) > 1 else None      # optional: scratch cs101_chains.json (curb chains by stroke class)

out_pair = R / "BI_entrance_site_v010_5_before_after_v009_camera.png"
out_over = R / "BI_entrance_site_v010_overlay_plan_top.png"
for p in (out_pair, out_over):
    if p.exists():
        raise SystemExit(f"refusing to overwrite {p}")

# ---- 1. before / after from the v009 entrance camera
a = Image.open(R / "BI_presentation_v009_2_entrance_oblique.png").convert("RGB")
b = Image.open(R / "BI_entrance_site_v010_5_v009_entrance_camera.png").convert("RGB")
assert a.size == b.size, (a.size, b.size)
W, H = a.size
pair = Image.new("RGB", (W * 2 + 20, H + 60), (30, 30, 30))
pair.paste(a, (0, 60)); pair.paste(b, (W + 20, 60))
dr = ImageDraw.Draw(pair)
try:
    font = ImageFont.truetype("arial.ttf", 34)
except OSError:
    font = ImageFont.load_default()
dr.text((20, 12), "BEFORE - v009 (v003 site: flood-filled asphalt, terrain pit from storm-chart values, no loop / island)", fill=(255, 255, 255), font=font)
dr.text((W + 40, 12), "AFTER - v010 (CS-101 curb lines: drop-off loop, median island, plaza, curbs; CG-101 gutter / curb-top grades)", fill=(255, 255, 255), font=font)
pair.save(out_pair)

# ---- 2. plan overlay
cam = D["cameras_new"]["BI_cam_entrance_plan_top"]
cx, cy, width = cam["loc"][0], cam["loc"][1], cam["ortho"]
img = Image.open(R / "BI_entrance_site_v010_1_entrance_plan_top.png").convert("RGBA")
IW, IH = img.size
k = IW / width                       # px per ft (2400 / 240 = 10)


def px(x, y):
    return ((x - cx) * k + IW / 2, IH / 2 - (y - cy) * k)


ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
d = ImageDraw.Draw(ov)


def poly(pts, colour, w=3, closed=True):
    q = [px(x, y) for x, y in pts]
    if closed:
        q.append(q[0])
    d.line(q, fill=colour, width=w)


P = D["polygons"]
BLUE, RED, GREEN = (40, 110, 255, 255), (255, 50, 50, 255), (40, 220, 60, 255)
if CHAINS and CHAINS.exists():
    ch = json.loads(CHAINS.read_text(encoding="utf-8"))
    for cls in ("6_0%",):                 # stroke class of the curb lines on CS-101
        for chain in ch.get(cls, []):
            if len(chain) > 1:
                poly(chain, BLUE, 3, closed=False)
poly(P["drive_old_v003"], RED, 3)
for key in ("drive_merged", "island_oval_outer", "island_oval_inner", "island_nose_paved", "end_island_12_20", "plaza_pavers", "walk_diagonal_pavers", "walk_aisle_concrete"):
    poly(P[key], GREEN, 3)
Wn = D["meta"]["regrade_window"]
wx0, wy0 = px(Wn["x0"], Wn["y1"]); wx1, wy1 = px(Wn["x1"], Wn["y0"])
for i in range(0, int(wx1 - wx0), 24):
    d.line([(wx0 + i, wy0), (min(wx0 + i + 12, wx1), wy0)], fill=(255, 255, 255, 220), width=2)
    d.line([(wx0 + i, wy1), (min(wx0 + i + 12, wx1), wy1)], fill=(255, 255, 255, 220), width=2)
for j in range(0, int(wy1 - wy0), 24):
    d.line([(wx0, wy0 + j), (wx0, min(wy0 + j + 12, wy1))], fill=(255, 255, 255, 220), width=2)
    d.line([(wx1, wy0 + j), (wx1, min(wy0 + j + 12, wy1))], fill=(255, 255, 255, 220), width=2)
# legend + scale
d.rectangle([20, 20, 700, 190], fill=(0, 0, 0, 170))
d.line([(40, 50), (120, 50)], fill=BLUE, width=5); d.text((135, 38), "CS-101 rev 13 curb lines (registered vector geometry)", fill=(255, 255, 255, 255), font=font)
d.line([(40, 90), (120, 90)], fill=RED, width=5); d.text((135, 78), "v009 asphalt outline (replaced)", fill=(255, 255, 255, 255), font=font)
d.line([(40, 130), (120, 130)], fill=GREEN, width=5); d.text((135, 118), "v010 site polygons (drive, island, nose, plaza, walks)", fill=(255, 255, 255, 255), font=font)
d.line([(40, 170), (40 + 20 * k, 170)], fill=(255, 255, 255, 255), width=5); d.text((50 + 20 * k, 158), "20 ft   (dashed = regrade window)", fill=(255, 255, 255, 255), font=font)
Image.alpha_composite(img, ov).convert("RGB").save(out_over)
print("wrote", out_pair.name, out_over.name)
