"""Detect glazing (teal) regions in the shaded elevation rasters; report boxes in ft (u along facade from a reference bubble, z above LVL-01)."""
import sys, re, json
from PIL import Image, ImageDraw
sys.path.insert(0, sys.argv[1]); from words import words
SP=sys.argv[1]; img=sys.argv[2]; page=sys.argv[3]; y0,y1,lvl01=float(sys.argv[4]),float(sys.argv[5]),float(sys.argv[6]); name=sys.argv[7]; refb=sys.argv[8]; refval=float(sys.argv[9]); sign=float(sys.argv[10])
S=2.0
im=Image.open(img).convert("RGB"); px=im.load(); W,H=im.size
Wd=words(f"{SP}/bbox/{page}.html")
lab=re.compile(r'^\d{1,2}(\.\d)?$|^[A-N](\.\d)?$|^B7$')
bub={w:cx for w,cx,cy,*r in Wd if lab.match(w) and y1-10<cy<y1+120}
if refb not in bub: print("ref bubble not found", refb, bub); sys.exit()
xref=bub[refb]
mask=Image.new("L",(W,H),0); mp=mask.load()
X0,X1,Y0,Y1=int(90*S),int(2950*S),int(y0*S),int(y1*S)
for Y in range(Y0,Y1):
    for X in range(X0,X1):
        r,g,b=px[X,Y]
        if b>100 and g>100 and r<170 and (b-r)>25 and (g-r)>15: mp[X,Y]=255
boxes=[]
for Y in range(Y0,Y1,2):
    for X in range(X0,X1,2):
        if mp[X,Y]==255:
            ImageDraw.floodfill(mask,(X,Y),128)
            # bbox of this component via scan (cheap: scan a window)
            xs=[];ys=[]
            for yy in range(max(Y0,Y-10), Y1):
                row=[xx for xx in range(X0,X1) if mp[xx,yy]==128]
                if not row:
                    if yy>Y+10: break
                    continue
                xs+= [min(row),max(row)]; ys.append(yy)
            ImageDraw.floodfill(mask,(X,Y),64)
            if xs:
                bx0,bx1,by0,by1=min(xs),max(xs),min(ys),max(ys)
                wft=(bx1-bx0)/S/9; hft=(by1-by0)/S/9
                if wft>=2 and hft>=2:
                    u0=refval+sign*(bx0/S-xref)/9; u1=refval+sign*(bx1/S-xref)/9
                    boxes.append((min(u0,u1),max(u0,u1),(lvl01-by1/S)/9,(lvl01-by0/S)/9))
boxes.sort()
print("##",name,"ref",refb,"=",refval,"; boxes (u0,u1,z0,z1) ft:")
for b in boxes: print("   u %7.2f-%7.2f   z %5.2f-%5.2f   (w %.1f h %.1f)"%(b[0],b[1],b[2],b[3],b[1]-b[0],b[3]-b[2]))
json.dump(boxes, open(f"{SP}/glass_{name.split()[0]}.json","w"))
