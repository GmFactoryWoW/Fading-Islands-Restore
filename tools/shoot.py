import sys,math,io,contextlib,random,pickle
sys.path.insert(0,'C:/CoA-Build/boats')
import numpy as np
import plan1_lib as P
with contextlib.redirect_stdout(io.StringIO()):
    import dep2
from dep2 import ok
def okb(x,y,h):
    r=int(round(P.X1-x));c=int(round(P.Y1-y))
    if r<0 or c<0 or r>=P.H or c>=P.W:return False
    return ok(x,y,h)
ds=3.0
RS=(40,50,65,90,130)
def gen(bx,by,deg,segs,forward):
    """segs: list of (kind,val): ('S',len) straight / ('A',turn,R,angle). forward=True goes ahead from berth (departure); False goes backwards (approach). returns pose list in travel order"""
    x,y,h=bx,by,deg;pts=[(x,y,h)]
    sg=1 if forward else -1
    for sgm in segs:
        if sgm[0]=='S':
            n=int(sgm[1]/ds)
            for i in range(n):
                x+=sg*ds*math.cos(math.radians(h));y+=sg*ds*math.sin(math.radians(h));pts.append((x,y,h))
        else:
            _,turn,R,ang=sgm;t=0
            while t<ang:
                dh=math.degrees(ds/R);t+=dh
                if forward:
                    h+=turn*dh
                    x+=ds*math.cos(math.radians(h));y+=ds*math.sin(math.radians(h))
                else:
                    h-=turn*dh
                    x-=ds*math.cos(math.radians(h));y-=ds*math.sin(math.radians(h))
                pts.append((x,y,h))
    return pts
def valid(p):
    return all(okb(*q) for q in p)
def far_open(p,tip=(894,-3621),dist=320):
    x,y,h=p[-1];return math.hypot(x-tip[0],y-tip[1])>dist
def search(bx,by,deg,forward,n=6000,seed=1):
    rnd=random.Random(seed);best=[]
    for _ in range(n):
        segs=[]
        for k in range(rnd.choice((1,2,3))):
            if rnd.random()<0.35:segs.append(('S',rnd.choice((20,40,80,120,200))))
            else:segs.append(('A',rnd.choice((1,-1)),rnd.choice(RS),rnd.choice((20,45,70,90,120,150,180))))
        segs.append(('S',rnd.choice((150,250,350,450))))
        p=gen(bx,by,deg,segs,forward)
        if not far_open(p):continue
        # cheap center test first
        if not all(okb(x,y,h) for x,y,h in p[::4]):continue
        if valid(p):best.append((len(p),segs,[round(v) for v in p[-1]]))
        if len(best)>=5:break
    best.sort(key=lambda b:b[0]);return best
if __name__=='__main__':
    bx,by,deg=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
    for fw,name in ((False,'APPROACH'),(True,'DEPART')):
        r=search(bx,by,deg,fw,n=int(sys.argv[4]) if len(sys.argv)>4 else 6000)
        print(name,len(r),r[:2],flush=True)
