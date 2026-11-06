import sys,math,random
sys.path.insert(0,'C:/CoA-Build/boats')
import numpy as np
import plan1_lib as P
import shoot
from scipy.ndimage import distance_transform_edt
DS=distance_transform_edt(~(P.land|P.struct))
CL={}
def frc(h,c):
    k=(h,c)
    if k not in CL: CL[k]=P.corr((DS<c)|(P.DPIER<1.0),P.kernel(P.hull,math.radians(h*3)+math.pi))<0.5
    return CL[k]
def okc(c):
    def f(x,y,hd):
        r=int(round(P.X1-x));cc=int(round(P.Y1-y))
        if r<0 or cc<0 or r>=P.H or cc>=P.W:return False
        return bool(frc(int(round(hd/3))%120,c)[r,cc])
    return f
def clearance(p):
    best=0
    for c in (0.5,1,2,3,4,5,6,8):
        f=okc(c)
        if all(f(*q) for q in p):best=c
        else:break
    return best
bx,by,deg=953,-3604,141
shoot.okb=okc(0.5)
rnd=random.Random(11);cands=[]
import itertools
for i in range(150000):
    segs=[]
    for k in range(rnd.choice((1,2,3))):
        if rnd.random()<0.3:segs.append(('S',rnd.choice((20,40,80,120,200))))
        else:segs.append(('A',rnd.choice((1,-1)),rnd.choice((40,50,65,90,130)),rnd.choice((20,45,70,90,120,150,180))))
    segs.append(('S',rnd.choice((250,350,450))))
    p=shoot.gen(bx,by,deg,segs,False)
    if not shoot.far_open(p):continue
    if not all(shoot.okb(x,y,h) for x,y,h in p[::4]):continue
    if shoot.valid(p):
        cands.append((clearance(p),segs,[round(v) for v in p[-1]]))
        if len(cands)>=30:break
cands.sort(key=lambda c:-c[0])
for c in cands[:6]:print(c)
