import sys,math,pickle
sys.path.insert(0,'C:/CoA-Build/boats')
from plan2 import *
from plan1_lib import *
import numpy as np
sideA=[(x,-14.6) for x in np.arange(-3,34,1.0)];sideB=[(x,9.4) for x in np.arange(-3,34,1.0)]
def pk(pl,th):
    c,s=math.cos(th),math.sin(th);k=np.zeros((2*KS+1,2*KS+1),np.float32)
    for lx,ly in pl:
        r=int(round(KS-(c*lx-s*ly)));q=int(round(KS-(s*lx+c*ly)))
        if 0<=r<2*KS+1 and 0<=q<2*KS+1:k[r,q]+=1
    return k
band=(DPIER>=0.8)&(DPIER<=3.2)
out=[]
for deg in range(0,360,3):
    th=math.radians(deg)+math.pi
    fr=freemap(deg,solclear=2.0,pierclear=0.8)
    for nm,sd in (('A',sideA),('B',sideB)):
        sc=corr(band,pk(sd,th));okm=fr&(sc>=14)
        rr,cc=np.nonzero(okm)
        a=math.radians(deg);h=int(round(deg/STEP))%NH
        for r,c in zip(rr,cc):
            x=X1-r;y=Y1-c
            # straight run-out 60 yd ahead (bow side) must be free; straight run-in 60 yd behind must be free
            ahead=all(ok(x+t*math.cos(a),y+t*math.sin(a),h) for t in (20,40,60))
            behind=all(ok(x-t*math.cos(a),y-t*math.sin(a),h) for t in (20,40,60))
            out.append((int(ahead)+int(behind),sc[r,c],deg,nm,x,y,ahead,behind))
out.sort(reverse=True)
print(len(out))
seen=[]
for o in out:
    if any(abs(o[4]-a)<10 and abs(o[5]-b)<10 and abs(o[2]-g)<15 for a,b,g in seen):continue
    seen.append((o[4],o[5],o[2]));print('runs %d score %.0f heading %d side %s origin (%.0f,%.0f) ahead %s behind %s'%o)
    if len(seen)>=14:break
