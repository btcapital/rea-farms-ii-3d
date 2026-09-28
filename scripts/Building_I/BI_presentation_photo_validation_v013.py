"""Photo-validation composite for v013 (system python + Pillow): the genuine drone photograph 2026-07-28 (validation only)
beside the v013 render from the approximate matching vantage, plus paired crops of the entrance tower and of the
court-building west facade.  Writes renders/Building_I/BI_presentation_v013_photo_validation.png (refuses to overwrite).
Run:  python scripts/Building_I/BI_presentation_photo_validation_v013.py <path to drone_2026-07-28_a.jpg>
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent.parent
R = ROOT / "renders" / "Building_I"
out = R / "BI_presentation_v013_photo_validation.png"
if out.exists():
    raise SystemExit(f"refusing to overwrite {out}")
try:
    font = ImageFont.truetype("arial.ttf", 30)
except OSError:
    font = ImageFont.load_default()
photo = Image.open(sys.argv[1]).convert("RGB")
render = Image.open(R / "BI_presentation_v013_2_photo_match_drone.png").convert("RGB")
W = 1600
ph = photo.resize((W, round(photo.height * W / photo.width)))
rd = render.resize((W, round(render.height * W / render.width)))
# crops: tower (photo ~ x 0.55-0.85, y 0.33-0.60) and courts west facade (photo ~ x 0.05-0.45, y 0.30-0.62); render at the same fractions
def crop(im, fx0, fy0, fx1, fy1, w):
    c = im.crop((int(im.width * fx0), int(im.height * fy0), int(im.width * fx1), int(im.height * fy1)))
    return c.resize((w, round(c.height * w / c.width)))
tp, tr = crop(ph, 0.55, 0.33, 0.85, 0.60, 780), crop(rd, 0.55, 0.33, 0.85, 0.60, 780)
cp, cr = crop(ph, 0.05, 0.30, 0.45, 0.62, 780), crop(rd, 0.05, 0.30, 0.45, 0.62, 780)
H = max(ph.height, rd.height)
im = Image.new("RGB", (W * 2 + 20, H + 60 + 40 + max(tp.height, tr.height) + 40 + max(cp.height, cr.height) + 20), (30, 30, 30))
d = ImageDraw.Draw(im)
d.text((20, 12), "PHOTO drone 2026-07-28 (genuine, validation only)", fill=(255, 255, 255), font=font)
d.text((W + 40, 12), "v013 render, approximate same vantage (Building II mass hidden: photo predates it)", fill=(255, 255, 255), font=font)
im.paste(ph, (0, 60)); im.paste(rd, (W + 20, 60))
y = 60 + H + 40
d.text((20, y - 32), "entrance tower: photo | render", fill=(255, 255, 255), font=font)
im.paste(tp, (0, y)); im.paste(tr, (800, y))
d.text((W + 40, y - 32), "court building west facade: photo | render", fill=(255, 255, 255), font=font)
im.paste(cp, (W + 20, y)); im.paste(cr, (W + 20 + 800, y))
im.save(out)
print("wrote", out.name)
