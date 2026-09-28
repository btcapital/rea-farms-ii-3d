"""Plan overlays for the v014 interior base-building model (system python + Pillow):
the Level 1 / Level 2 top-down cutaway renders (orthographic, 320 ft over 2400 px = 7.5 px/ft, centre (147,100))
composited at 50 % over the controlling Rev 14 plans A1.01 / A1.02 (72-dpi page renders, registered with the v008
grid-bubble fits).  Writes renders/Building_I/BI_interior_base_v014_overlay_{L1_A1.01,L2_A1.02}.png (refuses to overwrite).
Run:  python scripts/Building_I/BI_interior_base_overlays_v014.py <A1.01 page png> <A1.02 page png>
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent.parent
R = ROOT / "renders" / "Building_I"
STEM = "BI_interior_base_v014"
K = 7.5                       # render px per ft
CX, CY, W, H = 147.0, 100.0, 2400, 1700
REG = {"L1": (199.81, 6.7500, 1795.91, 6.7502), "L2": (197.71, 6.7500, 1796.00, 6.7502)}   # x_pt = a + b x ; y_pt = c - d y (v008)
try:
    font = ImageFont.truetype("arial.ttf", 30)
except OSError:
    font = ImageFont.load_default()
for level, view, page in (("L1", "1_L1_plan_cutaway", sys.argv[1]), ("L2", "2_L2_plan_cutaway", sys.argv[2])):
    out = R / f"{STEM}_overlay_{level}_{'A1.01' if level == 'L1' else 'A1.02'}.png"
    if out.exists():
        raise SystemExit(f"refusing to overwrite {out}")
    render = Image.open(R / f"{STEM}_{view}.png").convert("RGBA")
    plan = Image.open(page).convert("RGBA")
    a, b, c, d = REG[level]
    # render px = (x - (CX - W/2K)) * K ; plan X = a + b x  ->  x = (X - a)/b
    # affine mapping plan -> render:  px = K*((X - a)/b - CX + W/(2K)) ; py = K*((CY + H/(2K)) - (c - Y)/d)
    sx, sy = K / b, K / d
    ox = K * (-a / b - CX) + W / 2
    oy = K * (CY - c / d) + H / 2
    # PIL affine takes the inverse mapping (output -> input): X = (px - ox)/sx ; Y = (py - oy)/sy
    plan_t = plan.transform((W, H), Image.AFFINE, (1 / sx, 0, -ox / sx, 0, 1 / sy, -oy / sy), resample=Image.BILINEAR)
    base = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    base.alpha_composite(plan_t)
    render_half = render.copy()
    render_half.putalpha(140)
    base.alpha_composite(render_half)
    dr = ImageDraw.Draw(base)
    dr.rectangle([20, 20, 1180, 70], fill=(0, 0, 0, 170))
    dr.text((30, 28), f"{level}: v014 interior cutaway render (55 %) over Rev 14 {'A1.01' if level == 'L1' else 'A1.02'} (v008 bubble registration)", fill=(255, 255, 255, 255), font=font)
    base.convert("RGB").save(out)
    print("wrote", out.name)
