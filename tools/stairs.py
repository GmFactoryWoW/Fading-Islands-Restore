import sys,struct
sys.path.insert(0,'C:/CoA-Build/boats')
import wmo_geo as g
BS=chr(92)
p=BS.join(['World','Generic','Human','Passive Doodads','WoodenStairs','WoodenStairs02.m2']);d=g.getfile(p)
ni,oi,nv,ov=struct.unpack_from('<IIII',d,0xD8)
idx=struct.unpack_from('<%dH'%ni,d,oi);vt=[struct.unpack_from('<3f',d,ov+i*12) for i in range(nv)]
print('tris',ni//3,'verts',nv)
import collections
prof=collections.defaultdict(float)
for k in range(ni//3):
    a,b,c=[vt[i] for i in idx[k*3:k*3+3]]
    u=[b[i]-a[i] for i in range(3)];w=[c[i]-a[i] for i in range(3)]
    nz=u[0]*w[1]-u[1]*w[0]
    if abs(nz)>1e-3:
        print('up-ish tri verts',[tuple(round(x,1) for x in v) for v in (a,b,c)])
