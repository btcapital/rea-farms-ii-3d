"""Raster skyline: topmost dark pixel per column inside an elevation view, converted to ft above LVL-01 using the vector datum line."""
import sys, re
from PIL import Image
sys.path.insert(0, sys.argv[1]); from words import words
SP=sys.argv[1]; img=sys.argv[2]; page=sys.argv[3]; y0,y1,lvl01=float(sys.argv[4]),float(sys.argv[5]),float(sys.argv[6]); name=sys.argv[7]
skip=[float(v) for v in sys.argv[8].split(",")] if len(sys.argv)>8 else []
S=2.0  # px per pt at 144 dpi
im=Image.open(img); px=im.load(); W,H=im.size
Wd=words(f"{SP}/bbox/{page}.html")
lab=re.compile(r'^\d{1,2}(\.\d)?$|^[A-N](\.\d)?$|^B7$')
bubbles=sorted([(cx,w) for w,cx,cy,*r in Wd if lab.match(w) and y1-10<cy<y1+140], key=lambda t:t[0])
def near(xpt):
    if not bubbles: return ""
    b=min(bubbles,key=lambda t:abs(t[0]-xpt)); return f"{b[1]}{'+' if xpt>b[0] else '-'}{abs(xpt-b[0])/9:.1f}"
skiprows=set()
for z in skip:
    yc=(lvl01-z*9.0)*S
    for dy in range(-3,4): skiprows.add(int(yc)+dy)
runs=[]
for X in range(int(90*S), int(2950*S), 2):
    top=None
    for Y in range(int(y0*S), int(y1*S)):
        if Y in skiprows: continue
        if px[X,Y]<235:
            dark=sum(1 for k in range(1,5) if Y+k<H and px[X,Y+k]<235)
            if dark>=1 and (lvl01-Y/S)/9.0<=41.0: top=Y; break
    z=None if top is None else (lvl01-top/S)/9.0
    xpt=X/S
    if z is None: continue
    if runs and abs(runs[-1][2]-z)<0.12: runs[-1][1]=xpt
    else: runs.append([xpt,xpt,z])
print("##",name)
for a,b,z in runs:
    if b-a>=12: print(f"   x {a:6.0f}-{b:6.0f} pt  ({near(a):>9} .. {near(b):>9})  top = {z:6.2f} ft")
