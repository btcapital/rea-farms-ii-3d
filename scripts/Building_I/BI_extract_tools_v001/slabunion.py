"""Union of edge-of-slab clip polygons (L1 pieces from A1.00a + L2 slab from A1.00b), registered to the grid, traced to a polygon in feet."""
import json, sys
from PIL import Image, ImageDraw
SP=sys.argv[1]; S=4  # px per pt
def load(page):
    d=json.load(open(f"{SP}/{page}_slab.json")); return d
d23=load("p023"); d24=load("p024")
# registration per sheet: use grid 2 (12.333 ft) and grid 9 (150 ft) for x-scale check, grid N for y
def reg(d):
    gx,gy=d["gx"],d["gy"]; sx=(gx["9"]-gx["2"])/(150-12.3333); 
    return gx["2"], gy["N"], sx
r23=reg(d23); r24=reg(d24); print("scale pt/ft A1.00a %.4f  A1.00b %.4f"%(r23[2],r24[2]))
def toft(p, r): x2,yn,s=r; return ((p[0]-x2)/s+12.3333, 198.53-(p[1]-yn)/s)
# canvas in ft: x -20..300, y -20..220 at S px/ft? use 8 px/ft
F=8; W=int(320*F); H=int(240*F)
def px(pt): return ((pt[0]+20)*F, (220-pt[1])*F)
img=Image.new("L",(W,H),0); dr=ImageDraw.Draw(img)
for cid,polys in d23["clips"]:
    if cid in ("clip-24","clip-26","clip-28","clip-22"): continue  # title-block detail regions (x>2200)
    for p in polys:
        q=[px(toft(v,r23)) for v in p]
        if max(x for x,y in q)-min(x for x,y in q)<2: continue
        dr.polygon(q, fill=255)
for cid,polys in d24["clips"]:
    for p in polys:
        q=[px(toft(v,r24)) for v in p]; dr.polygon(q, fill=255)
img.save(f"{SP}/png/slab_union_raw.png")
# trace outer boundary of the largest component
p=img.load()
# fill holes: flood exterior, everything not exterior = building
ext=img.copy(); ImageDraw.floodfill(ext,(0,0),128); e=ext.load()
mask=Image.new("L",(W,H),0); m=mask.load()
for y in range(H):
    for x in range(W):
        if e[x,y]!=128: m[x,y]=255
def inside(x,y): return 0<=x<W and 0<=y<H and m[x,y]==255
start=None
for y in range(H):
    for x in range(W):
        if m[x,y]==255: start=(x,y); break
    if start: break
dirs=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
cur=start; b=7; contour=[cur]
for _ in range(500000):
    found=False
    for k in range(8):
        dd=(b+k)%8; nx,ny=cur[0]+dirs[dd][0],cur[1]+dirs[dd][1]
        if inside(nx,ny): cur=(nx,ny); b=(dd+5)%8; contour.append(cur); found=True; break
    if not found or cur==start: break
def dp(pts,eps):
    if len(pts)<3: return pts
    a,bb=pts[0],pts[-1]; dx,dy=bb[0]-a[0],bb[1]-a[1]; L=(dx*dx+dy*dy)**.5 or 1
    dm,im=0,0
    for i,q in enumerate(pts[1:-1],1):
        dist=abs(dy*(q[0]-a[0])-dx*(q[1]-a[1]))/L
        if dist>dm: dm,im=dist,i
    if dm>eps: return dp(pts[:im+1],eps)[:-1]+dp(pts[im:],eps)
    return [a,bb]
half=len(contour)//2; simp=dp(contour[:half+1],0.25*F)[:-1]+dp(contour[half:],0.25*F)[:-1]
ft=[(x/F-20, 220-y/F) for x,y in simp]
json.dump(ft, open(f"{SP}/slab_union_ft.json","w"))
print("contour px", len(contour), "vertices", len(ft))
xs=[v[0] for v in ft]; ys=[v[1] for v in ft]
print("extent X %.2f..%.2f (%.2f)  Y %.2f..%.2f (%.2f)"%(min(xs),max(xs),max(xs)-min(xs),min(ys),max(ys),max(ys)-min(ys)))
chk=Image.new("RGB",(W,H),"white"); cd=ImageDraw.Draw(chk); cd.polygon(simp, fill=(255,225,225), outline="red")
for gname,gxft in {"1":0,"2":12.333,"3":30,"4":45,"5":60,"6":72,"7":90,"8":120,"9":150,"10":180,"11":210,"12":240,"12.9":268,"13":270,"14":280}.items():
    x=(gxft+20)*F; cd.line([(x,0),(x,H)],fill=(255,0,0)); cd.text((x+2,4),gname,fill=(255,0,0))
for gname,gyft in {"A":0,"B":4,"B.7":21.667,"C":30,"C.6":42,"C.9":50,"D":52.333,"E":61.5,"F":70.583,"G":80.53,"H.1":98.7,"J":102.03,"K":119.28,"K.7":133.78,"L":138.53,"L.6":154.53,"M":168.53,"M.7":187.11,"N":198.53}.items():
    y=(220-gyft)*F; cd.line([(0,y),(W,y)],fill=(0,0,255)); cd.text((4,y-10),gname,fill=(0,0,255))
chk.save(f"{SP}/png/slab_union_check.png")
