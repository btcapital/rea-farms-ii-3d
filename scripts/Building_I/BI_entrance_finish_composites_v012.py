"""Composites for the v012 finish correction (system python + Pillow):
  * BI_entrance_finish_v012_photo_vs_render.png : the genuine drone photograph 2026-07-28 (validation only, source_documents) beside
    the v012 render from the approximate matching vantage (and the v011 "before" render of the same camera)
  * BI_entrance_finish_v012_before_after_{2_entrance_oblique,3_tower_closeup,4_tower_corner_side}.png : v011 | v012, same cameras
Refuses to overwrite.  Run:  python scripts/Building_I/BI_entrance_finish_composites_v012.py <path to drone_2026-07-28_a.jpg>
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent.parent
R = ROOT / "renders" / "Building_I"
STEM = "BI_entrance_finish_v012"
try:
    font = ImageFont.truetype("arial.ttf", 34)
except OSError:
    font = ImageFont.load_default()


def pair(a, b, la, lb, out):
    if out.exists():
        raise SystemExit(f"refusing to overwrite {out}")
    W, H = a.size
    b = b.resize((W, H))
    im = Image.new("RGB", (W * 2 + 20, H + 60), (30, 30, 30))
    im.paste(a, (0, 60)); im.paste(b, (W + 20, 60))
    d = ImageDraw.Draw(im)
    d.text((20, 12), la, fill=(255, 255, 255), font=font)
    d.text((W + 40, 12), lb, fill=(255, 255, 255), font=font)
    im.save(out)
    print("wrote", out.name)


photo = Image.open(sys.argv[1]).convert("RGB")
render = Image.open(R / f"{STEM}_1_photo_match_drone.png").convert("RGB")
before = Image.open(R / f"{STEM}_before_1_photo_match_drone.png").convert("RGB")
W = 1600
ph = photo.resize((W, round(photo.height * W / photo.width)))
rd = render.resize((W, round(render.height * W / render.width)))
bf = before.resize((W, round(before.height * W / before.width)))
out = R / f"{STEM}_photo_vs_render.png"
if out.exists():
    raise SystemExit(f"refusing to overwrite {out}")
H = max(ph.height, rd.height)
im = Image.new("RGB", (W * 3 + 40, H + 60), (30, 30, 30))
im.paste(ph, (0, 60)); im.paste(bf, (W + 20, 60)); im.paste(rd, (2 * W + 40, 60))
d = ImageDraw.Draw(im)
d.text((20, 12), "PHOTO drone 2026-07-28 (genuine, validation only)", fill=(255, 255, 255), font=font)
d.text((W + 40, 12), "v011 model, approximate same vantage (brick strip at the tower's front-left)", fill=(255, 255, 255), font=font)
d.text((2 * W + 60, 12), "v012 model, same vantage (tower front PNL1 + CW1 to its west corner, A4.02)", fill=(255, 255, 255), font=font)
im.save(out)
print("wrote", out.name)
for view, label in (("2_entrance_oblique", "entrance oblique (v009 camera)"), ("3_tower_closeup", "lobby tower closeup"), ("4_tower_corner_side", "tower north-west corner / side")):
    pair(Image.open(R / f"{STEM}_before_{view}.png").convert("RGB"), Image.open(R / f"{STEM}_{view}.png").convert("RGB"),
         f"BEFORE - v011: {label} (N1 brick extended over the tower front x 28.5-40)", "AFTER - v012: tower front PNL1 above the CW1 head, curtain wall below (A4.02 / A7.26)",
         R / f"{STEM}_before_after_{view}.png")
