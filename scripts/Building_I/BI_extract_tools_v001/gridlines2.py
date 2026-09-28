import sys, collections, re
sys.path.insert(0, sys.argv[2]); from words import words
segs=[l.rstrip("\n").split("\t") for l in open(sys.argv[1])][1:]
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
W=words(sys.argv[3])
num=re.compile(r'^\d{1,2}(\.\d)?$'); let=re.compile(r'^[A-N](\.\d)?$|^B7$|^B\.7$|^I$')
nb=[(w,cx,cy) for w,cx,cy,*r in W if (num.match(w) or w=="I") and (cy<300 or cy>1950)]
lb=[(w,cx,cy) for w,cx,cy,*r in W if let.match(w) and (cx<300 or 2100<cx<2300)]
print("X grid candidates (vertical lines, len>=800) with bubble within 3pt:")
for x,L in merge(V,800):
    c=[b for b in nb if abs(b[1]-x)<3]
    if c: print(f"  x={x:9.2f} len={L:6.0f} -> {','.join(sorted(set(b[0] for b in c)))}")
print("Y grid candidates (horizontal lines, len>=800) with bubble within 3pt:")
for y,L in merge(H,800):
    c=[b for b in lb if abs(b[2]-y)<3]
    if c: print(f"  y={y:9.2f} len={L:6.0f} -> {','.join(sorted(set(b[0] for b in c)))}")
print("bubbles without a detected line:")
xs=[x for x,L in merge(V,800)]; ys=[y for y,L in merge(H,800)]
print("  X:", sorted(set(b[0] for b in nb if not any(abs(b[1]-x)<3 for x in xs))))
print("  Y:", sorted(set(b[0] for b in lb if not any(abs(b[2]-y)<3 for y in ys))))
