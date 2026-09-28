"""Classify the shaded elevation raster into material classes per 1 ft x 1 ft cell.

Classes: BRK1, PNL1, PNL2, PNL3, TWS1 (from the drawing material tags, used as
calibration samples) plus GLASS (teal colour test). Output: rectangles in
(u0, u1, z0, z1) ft along the facade and a check image.
Usage: python facade_classify.py <scratch> <colorpng> <page> <y0> <y1> <lvl01> <name> <refbubble> <refval> <sign>
"""
import sys, re, json, math, collections
from PIL import Image, ImageDraw
sys.path.insert(0, sys.argv[1])
from words import words

SP, img, page = sys.argv[1], sys.argv[2], sys.argv[3]
y0, y1, lvl01 = float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6])
name, refb, refval, sign = sys.argv[7], sys.argv[8], float(sys.argv[9]), float(sys.argv[10])
S = 2.0            # px per pt (144 dpi)
PXFT = 9.0 * S     # px per ft
im = Image.open(img).convert("RGB")
px = im.load()
W, H = im.size
Wd = words(f"{SP}/bbox/{page}.html")
lab = re.compile(r'^\d{1,2}(\.\d)?$|^[A-N](\.\d)?$|^B7$')
bub = {w: cx for w, cx, cy, *r in Wd if lab.match(w) and y1 - 10 < cy < y1 + 140}
xref = bub[refb]
CLASSES = ["BRK1", "PNL1", "PNL2", "PNL3", "TWS1"]
tags = [(w, cx, cy, x0, y0w, x1, y1w) for w, cx, cy, x0, y0w, x1, y1w in Wd if w in CLASSES and y0 < cy < y1]


def lum(p):
    return 0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]


def is_glass(p):
    r, g, b = p
    return b > 100 and g > 100 and r < 170 and (b - r) > 25 and (g - r) > 15


def feats(X0, Y0, X1, Y1):
    vals = []; gx = []; gy = []; dark = 0; n = 0; glass = 0
    for Y in range(Y0, Y1, 2):
        for X in range(X0, X1, 2):
            if not (0 <= X < W - 2 and 0 <= Y < H - 2):
                continue
            p = px[X, Y]; L = lum(p); vals.append(L)
            gx.append(abs(lum(px[X + 2, Y]) - L)); gy.append(abs(lum(px[X, Y + 2]) - L))
            dark += L < 90; n += 1; glass += is_glass(p)
    if n == 0:
        return None
    mean = sum(vals) / n
    std = math.sqrt(sum((v - mean) ** 2 for v in vals) / n)
    return (mean, std, sum(gx) / n, sum(gy) / n, dark / n, glass / n)


# --- calibration from tags: patch 15..45 px below each tag box, 60 px wide
sig = collections.defaultdict(list)
for w, cx, cy, x0, ty0, x1, ty1 in tags:
    for dy in (14, 46):
        f = feats(int(cx * S) - 30, int(ty1 * S) + dy, int(cx * S) + 30, int(ty1 * S) + dy + 28)
        if f and f[5] < 0.2:
            sig[w].append(f)
sigm = {}
for k, v in sig.items():
    sigm[k] = tuple(sum(f[i] for f in v) / len(v) for i in range(5))
print("##", name, "calibration:", {k: (len(sig[k]), tuple(round(x, 1) for x in v)) for k, v in sigm.items()})
scale = (60.0, 25.0, 12.0, 12.0, 0.4)


def classify(f):
    if f[5] > 0.35:
        return "GLASS"
    best, bd = None, 1e9
    for k, s in sigm.items():
        d = sum(((f[i] - s[i]) / scale[i]) ** 2 for i in range(5))
        if d < bd:
            bd, best = d, k
    return best


# --- silhouette top per column from the raster (reuse: topmost dark pixel below the dashed levels)
def top_at(X):
    for Y in range(int(y0 * S), int(y1 * S)):
        L = lum(px[X, Y])
        if L < 235 and (lvl01 - Y / S) / 9.0 <= 41.0:
            if sum(1 for k in range(1, 5) if lum(px[X, Y + k]) < 235) >= 1:
                return Y
    return None


# --- cell grid (1 ft) over the facade band
cells = {}
umin, umax = 1e9, -1e9
X0, X1 = int(90 * S), int(2950 * S)
for X in range(X0, X1, int(PXFT)):
    t = top_at(X + int(PXFT / 2))
    if t is None:
        continue
    Ybot = int(lvl01 * S)
    for Y in range(Ybot - int(PXFT), t, -int(PXFT)):
        f = feats(X + 2, Y + 2, X + int(PXFT) - 2, Y + int(PXFT) - 2)
        if f is None:
            continue
        c = classify(f)
        uc = refval + sign * (X / S - xref) / 9.0
        z = (lvl01 - Y / S) / 9.0
        cells[(round(uc, 2), round(z, 2))] = c
        umin, umax = min(umin, uc), max(umax, uc)
# --- majority filter (3x3)
keys = list(cells)
smooth = {}
for (u, z) in keys:
    votes = collections.Counter()
    for du in (-1, 0, 1):
        for dz in (-1, 0, 1):
            k = (round(u + du * sign, 2), round(z + dz, 2))
            if k in cells:
                votes[cells[k]] += 2 if (du == 0 and dz == 0) else 1
    smooth[(u, z)] = votes.most_common(1)[0][0]
# --- merge into rectangles: rows of equal class along u, then merge vertically
us = sorted(set(u for u, z in smooth)); zs = sorted(set(z for u, z in smooth))
rects = []
for z in zs:
    run = None
    for u in sorted(us, key=lambda v: v):
        c = smooth.get((u, z))
        if run and c == run[0] and abs(u - run[2]) < 1.5:
            run[2] = u
        else:
            if run:
                rects.append(run)
            run = [c, u, u, z] if c else None
    if run:
        rects.append(run)
# vertical merge
merged = []
rects.sort(key=lambda r: (r[0], r[1], r[2], r[3]))
by = collections.defaultdict(list)
for c, u0, u1, z in rects:
    by[(c, u0, u1)].append(z)
for (c, u0, u1), zl in by.items():
    zl.sort()
    a = zl[0]; prev = zl[0]
    for z in zl[1:] + [None]:
        if z is not None and abs(z - prev) < 1.5:
            prev = z
        else:
            merged.append((c, min(u0, u1) - 0.5, max(u0, u1) + 0.5, a, prev + 1.0))
            if z is not None:
                a = prev = z
out = [(c, round(a, 2), round(b, 2), round(z0, 2), round(z1, 2)) for c, a, b, z0, z1 in merged if c != "GLASS"]
json.dump(out, open(f"{SP}/facade_{name}.json", "w"))
areas = collections.Counter()
for c, a, b, z0, z1 in out:
    areas[c] += (b - a) * (z1 - z0)
print("   rectangles:", len(out), " area by class (sq ft):", {k: round(v) for k, v in areas.items()})
# --- check image
cols = {"BRK1": (120, 60, 40), "PNL1": (250, 250, 240), "PNL2": (30, 30, 30), "PNL3": (150, 150, 150), "TWS1": (200, 215, 230), "GLASS": (60, 120, 160)}
chk = im.copy().convert("RGB")
d = ImageDraw.Draw(chk, "RGBA")
for (u, z), c in smooth.items():
    X = int((xref + sign * (u - refval) * 9.0) * S)
    Y = int((lvl01 - z * 9.0) * S)
    d.rectangle([X, Y - int(PXFT), X + int(PXFT), Y], fill=cols.get(c, (255, 0, 255)) + (150,))
chk = chk.crop((X0, int(y0 * S), X1, int(y1 * S) + 60))
chk.thumbnail((2000, 2000))
chk.save(f"{SP}/png/facade_{name}_check.png")
