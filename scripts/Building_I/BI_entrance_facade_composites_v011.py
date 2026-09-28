"""Before/after composites for the v011 entrance-facade correction (system python + Pillow).
Left = v010 (same camera, rendered from the untouched scene by the v011 build script before the fix), right = v011.
Writes renders/Building_I/BI_entrance_facade_v011_before_after_{1_entrance_eye_level,2_tower_closeup,4_tower_west_elevation_ortho}.png
(refuses to overwrite).  Run:  python scripts/Building_I/BI_entrance_facade_composites_v011.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent.parent
R = ROOT / "renders" / "Building_I"
STEM = "BI_entrance_facade_v011"
try:
    font = ImageFont.truetype("arial.ttf", 34)
except OSError:
    font = ImageFont.load_default()
for view, label in (("1_entrance_eye_level", "main entrance, eye level (v010 view 2)"), ("2_tower_closeup", "lobby tower west face above the porte cochere"),
                    ("4_tower_west_elevation_ortho", "straight-on west elevation of the tower (orthographic)")):
    out = R / f"{STEM}_before_after_{view}.png"
    if out.exists():
        raise SystemExit(f"refusing to overwrite {out}")
    a = Image.open(R / f"{STEM}_before_{view}.png").convert("RGB")
    b = Image.open(R / f"{STEM}_{view}.png").convert("RGB")
    assert a.size == b.size
    W, H = a.size
    pair = Image.new("RGB", (W * 2 + 20, H + 60), (30, 30, 30))
    pair.paste(a, (0, 60)); pair.paste(b, (W + 20, 60))
    d = ImageDraw.Draw(pair)
    d.text((20, 12), f"BEFORE - v010: {label} (duplicate coplanar PNL1 face -> Cycles self-occlusion, black)", fill=(255, 255, 255), font=font)
    d.text((W + 40, 12), "AFTER - v011: duplicate and buried faces removed, one continuous PNL1 plane (A4.02 / A5.24)", fill=(255, 255, 255), font=font)
    pair.save(out)
    print("wrote", out.name)
