import sys,math,io,contextlib
sys.path.insert(0,'C:/CoA-Build/boats')
import numpy as np
import plan1_lib as P
with contextlib.redirect_stdout(io.StringIO()):
    import dep2
from dep2 import ok
def pk(pl,th):
    c,s=math.cos(th),math.sin(th);k=np.zeros((2*P.KS+1,2*P.KS+1),np.float32)
    for lx,ly in pl:
        r=int(round(P.KS-(c*lx-s*ly)));q=int(round(P.KS-(s*lx+c*ly)))
        if 0<=r<2*P.KS+1 and 0<=q<2*P.KS+1:k[r,q]+=1
    return k
band=(P.DPIER>=0.6)&(P.DPIER<=2.2)
sideA=[(x,-3.7) for x in np.arange(-5,6,1.0)];sideB=[(x,3.7) for x in np.arange(-5,6,1.0)]
tip=(893.87,-3620.84)
out=[]
for deg in range(0,360,3):
    th=math.radians(deg)+math.pi
    fr=P.corr((dep2.DSOLL<1.5)|(P.DPIER<0.6),P.kernel(P.hull,th))<0.5
    for nm,sd in (('A',sideA),('B',sideB)):
        sc=P.corr(band,pk(sd,th));m=fr&(sc>=8)
        rr,cc=np.nonzero(m)
        for r,c in zip(rr,cc):
            x=P.X1-r;y=P.Y1-c
            dd=math.hypot(x-tip[0],y-tip[1])
            if dd<45:out.append((dd,sc[r,c],deg,nm,x,y))
out.sort()
seen=[]
for o in out:
    if any(abs(o[4]-a)<5 and abs(o[5]-b)<5 and abs(o[2]-g)<20 for a,b,g in seen):continue
    seen.append((o[4],o[5],o[2]));print('dist %.0f score %.0f heading %d side %s origin (%.1f,%.1f)'%o)
    if len(seen)>=12:break
