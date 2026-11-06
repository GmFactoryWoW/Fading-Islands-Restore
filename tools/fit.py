import sys,math,itertools
sys.path.insert(0,'C:/CoA-Build/boats')
from wmo_geo import *
from objs import objs,K
w,_=objs(38,30)
inst=[x for x in w if x[0].upper().endswith('DOCKS_NARROW02.WMO') and math.hypot(x[1]-898,x[2]+3627)<3][0]
n,sx,sy,sz,rot,bb=inst
print(n,sx,sy,sz,rot,bb)
tris=load(n.replace(chr(92),chr(92)))
print(len(tris))
vs=[v for t in tris for v in t]
print('local bbox',[ (round(min(v[i] for v in vs),2),round(max(v[i] for v in vs),2)) for i in range(3)])
px,py,pz=K-sy,sz,K-sx   # file pos
best=[]
for swap in (0,1):
  for s1 in (1,-1):
    for s2 in (1,-1):
      for psi0 in (rot[1],-rot[1],rot[1]+180,-rot[1]+180,rot[1]+90,-rot[1]+90,rot[1]-90,-rot[1]-90):
        ps=math.radians(psi0);c,s=math.cos(ps),math.sin(ps)
        X=[];Z=[]
        for v in vs:
            u,vv=(v[0],v[1]) if not swap else (v[1],v[0])
            u*=s1;vv*=s2
            X.append(px+c*u-s*vv);Z.append(pz+s*u+c*vv)
        err=abs(min(X)-bb[0])+abs(max(X)-bb[3])+abs(min(Z)-bb[2])+abs(max(Z)-bb[5])
        best.append((err,swap,s1,s2,psi0))
best.sort();print(best[:4])
