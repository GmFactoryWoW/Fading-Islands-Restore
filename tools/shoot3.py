import sys,math,io,contextlib,random
sys.path.insert(0,'C:/CoA-Build/boats')
import numpy as np
import plan1_lib as P
import shoot
from scipy.ndimage import distance_transform_edt
DS=distance_transform_edt(~(P.land|P.struct))
FR={}
def fr(h):
    if h not in FR: FR[h]=P.corr((DS<2.0)|(P.DPIER<1.0),P.kernel(P.hull,math.radians(h*3)+math.pi))<0.5
    return FR[h]
def ok2(x,y,hd):
    r=int(round(P.X1-x));c=int(round(P.Y1-y))
    if r<0 or c<0 or r>=P.H or c>=P.W:return False
    return bool(fr(int(round(hd/3))%120)[r,c])
shoot.okb=ok2
if __name__=='__main__':
    bx,by,deg=953,-3604,141
    print('berth ok (struct 6yd):',ok2(bx,by,deg))
    for fw,nm in ((False,'APPROACH'),(True,'DEPART')):
        r=shoot.search(bx,by,deg,fw,n=60000,seed=3)
        print(nm,len(r));[print(x) for x in r[:3]]
