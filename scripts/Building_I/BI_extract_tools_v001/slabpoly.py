import re, sys, json, collections
sys.path.insert(0, sys.argv[1]); from words import words
from PIL import Image, ImageDraw
SP=sys.argv[1]
def clips(svg):
    s=open(svg,encoding="utf-8",errors="replace").read()
    out=[]
    for cid,d in re.findall(r'<clipPath id="([^"]+)">\s*<path[^>]*d="([^"]+)"', s):
        polys=[]; cur=[]
        for op,x,y in re.findall(r'([MLZ])\s*([-\d.]+)?\s*([-\d.]+)?', d):
            if op=="M":
                if len(cur)>2: polys.append(cur)
                cur=[(float(x),float(y))]
            elif op=="L": cur.append((float(x),float(y)))
            elif op=="Z":
                if len(cur)>2: polys.append(cur)
                cur=[]
        if len(cur)>2: polys.append(cur)
        polys=[p for p in polys if len(p)>=4]
        if polys: out.append((cid,polys))
    return out
def gridlines(segtsv, bboxhtml):
    segs=[l.rstrip("\n").split("\t") for l in open(segtsv)][1:]
    V=collections.defaultdict(float); H=collections.defaultdict(float)
    for x0,y0,x1,y1,sw,c in segs:
        x0,y0,x1,y1=map(float,(x0,y0,x1,y1))
        if abs(x0-x1)<0.05 and abs(y0-y1)>0.5: V[round(x0,1)]+=abs(y1-y0)
        elif abs(y0-y1)<0.05 and abs(x0-x1)>0.5: H[round(y0,1)]+=abs(x1-x0)
    def merge(D, minlen):
        keys=sorted(k for k,v in D.items()); out=[]
        for k in keys:
            if out and k-out[-1][0][-1]<=0.6: out[-1][0].append(k); out[-1][1]+=D[k]
            else: out.append([[k],D[k]])
        return [(sum(ks)/len(ks), L) for ks,L in out if L>=minlen]
    W=words(bboxhtml)
    num=re.compile(r'^\d{1,2}(\.\d)?$'); let=re.compile(r'^[A-N](\.\d)?$|^B7$|^B\.7$')
    nb=[(w,cx,cy) for w,cx,cy,*r in W if num.match(w) and (cy<300 or cy>1950)]
    lb=[(w,cx,cy) for w,cx,cy,*r in W if let.match(w) and (cx<300 or 2100<cx<2400)]
    gx={}; gy={}
    for x,L in merge(V,800):
        c=[b for b in nb if abs(b[1]-x)<2.5]
        for b in c: gx.setdefault(b[0],[]).append((L,x))
    for y,L in merge(H,800):
        c=[b for b in lb if abs(b[2]-y)<2.5]
        for b in c: gy.setdefault(b[0],[]).append((L,y))
    return {k:max(v)[1] for k,v in gx.items()}, {k:max(v)[1] for k,v in gy.items()}
if __name__=="__main__":
    page=sys.argv[2]
    gx,gy=gridlines(f"{SP}/svg/{page}.seg.tsv", f"{SP}/bbox/{page}.html")
    print("grid x (pt):", {k:round(v,2) for k,v in sorted(gx.items())})
    print("grid y (pt):", {k:round(v,2) for k,v in sorted(gy.items())})
    cl=clips(f"{SP}/svg/{page}.svg")
    big=[(cid,polys) for cid,polys in cl if max(max(x for x,y in p)-min(x for x,y in p) for p in polys)>60 and min(min(x for x,y in p) for p in polys)<2600]
    print("large clip regions:", [(cid,len(polys),sum(len(p) for p in polys)) for cid,polys in big])
    json.dump({"gx":gx,"gy":gy,"clips":[(cid,polys) for cid,polys in big]}, open(f"{SP}/{page}_slab.json","w"))
    img=Image.new("RGB",(3024,2160),"white"); d=ImageDraw.Draw(img)
    cols=["#ffb3b3","#b3d9ff","#b3ffb3","#ffe0b3","#e0b3ff","#b3ffff","#ffffb3","#d9d9d9","#ffc0e0","#c0ffc0","#c0c0ff","#ffd0a0"]
    for i,(cid,polys) in enumerate(big):
        for p in polys: d.polygon(p, fill=cols[i%len(cols)], outline="black")
    for k,x in gx.items(): d.line([(x,0),(x,2160)], fill="red"); d.text((x+2,30),k,fill="red")
    for k,y in gy.items(): d.line([(0,y),(3024,y)], fill="blue"); d.text((2300,y-10),k,fill="blue")
    img=img.crop((100,250,2450,2000)).resize((1880,1400)); img.save(f"{SP}/png/{page}_slabcheck.png"); print("saved")
