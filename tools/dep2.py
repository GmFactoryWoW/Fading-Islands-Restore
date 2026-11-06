import sys,math
sys.path.insert(0,'C:/CoA-Build/boats')
import numpy as np
import plan1_lib as P
DSOLL=P.distance_transform_edt(~P.land)
FR={}
def fr(h):
    if h not in FR: FR[h]=P.corr((DSOLL<2.0)|(P.DPIER<1.0),P.kernel(P.hull,math.radians(h*3)+math.pi))<0.5
    return FR[h]
def ok(x,y,hd):
    r=int(round(P.X1-x));c=int(round(P.Y1-y))
    if r<0 or c<0 or r>=P.H or c>=P.W:return True
    return bool(fr(int(round(hd/3))%120)[r,c])
def arc(bx,by,deg,turn,R,tt,run=200):
    x,y,h=bx,by,deg;pts=[(x,y,h)];ds=3.0
    for s in range(14): x+=ds*math.cos(math.radians(h));y+=ds*math.sin(math.radians(h));pts.append((x,y,h))
    t=0
    while t<tt:
        dh=math.degrees(ds/R);h+=turn*dh;t+=dh;x+=ds*math.cos(math.radians(h));y+=ds*math.sin(math.radians(h));pts.append((x,y,h))
    for s in range(int(run/ds)): x+=ds*math.cos(math.radians(h));y+=ds*math.sin(math.radians(h));pts.append((x,y,h))
    return pts
if __name__=='__main__':
    for bx,by,deg in ((992,-3644,303),(983,-3628,330),(883,-3640,303),(880,-3627,126),(953,-3604,141)):
        found=[]
        for turn in (1,-1):
            for R in (45,60,80,110,150):
                for tt in (45,90,135,180,225):
                    p=arc(bx,by,deg,turn,R,tt)
                    if all(ok(*q) for q in p): found.append((turn,R,tt))
        print((bx,by,deg),'departures',found[:6],'berth ok',ok(bx,by,deg))
