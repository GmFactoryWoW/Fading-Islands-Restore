import sys,math
sys.path.insert(0,'C:/CoA-Build/boats')
from dep2 import ok
def back(bx,by,deg,turn,R,tt,straight=14,run=200):
    x,y,h=bx,by,deg;pts=[(x,y,h)];ds=3.0
    for s in range(straight):
        x-=ds*math.cos(math.radians(h));y-=ds*math.sin(math.radians(h));pts.append((x,y,h))
    t=0
    while t<tt:
        dh=math.degrees(ds/R);h-=turn*dh;t+=dh   # earlier heading differs by -turn
        x-=ds*math.cos(math.radians(h));y-=ds*math.sin(math.radians(h));pts.append((x,y,h))
    for s in range(int(run/ds)):
        x-=ds*math.cos(math.radians(h));y-=ds*math.sin(math.radians(h));pts.append((x,y,h))
    return pts
for bx,by,deg in ((880,-3627,126),(953,-3604,141),(875,-3617,123),(901,-3597,129),(981,-3619,126)):
    f=[]
    for st in (0,14,30):
      for turn in (1,-1):
        for R in (45,60,80,110,150):
            for tt in (30,60,90,135,180):
                p=back(bx,by,deg,turn,R,tt,straight=st)
                if all(ok(*q) for q in p): f.append((st*3,turn,R,tt))
    print((bx,by,deg),'approaches',f[:6])
