import re, sys, html
def words(path):
    t=open(path,encoding="utf-8").read()
    out=[]
    for m in re.finditer(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>', t):
        x0,y0,x1,y1=map(float,m.groups()[:4]); w=html.unescape(m.group(5))
        out.append((w,(x0+x1)/2,(y0+y1)/2,x0,y0,x1,y1))
    return out
if __name__=="__main__":
    p=sys.argv[1]; W=words(p)
    print(len(W),"words")
    num=re.compile(r'^\d{1,2}(\.\d)?$'); let=re.compile(r'^[A-N](\.\d)?$|^B7$')
    for w,cx,cy,x0,y0,x1,y1 in W:
        if num.match(w) and (cy<220 or cy>1250): print("NUM",w,round(cx,1),round(cy,1))
    for w,cx,cy,x0,y0,x1,y1 in W:
        if let.match(w) and (cx>2000 or cx<200): print("LET",w,round(cx,1),round(cy,1))
