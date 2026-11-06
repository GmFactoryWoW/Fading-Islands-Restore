import struct,numpy as np,collections,sys,json
exec(open('sc.py').read().split("def hits")[0])   # loads col (collidable tris, final geometry)
R=0.5
up=collections.defaultdict(list);wall=collections.defaultdict(list);slope=collections.defaultdict(list)
def cells(A,B,C):
    xs=[A[0],B[0],C[0]];ys=[A[1],B[1],C[1]]
    for ix in range(int(np.floor(min(xs)/R)),int(np.floor(max(xs)/R))+1):
        for iy in range(int(np.floor(min(ys)/R)),int(np.floor(max(ys)/R))+1):yield ix,iy
def zat(A,B,C,x,y):
    d=(B[1]-C[1])*(A[0]-C[0])+(C[0]-B[0])*(A[1]-C[1])
    if abs(d)<1e-12:return None
    l1=((B[1]-C[1])*(x-C[0])+(C[0]-B[0])*(y-C[1]))/d;l2=((C[1]-A[1])*(x-C[0])+(A[0]-C[0])*(y-C[1]))/d
    if l1>=-1e-6 and l2>=-1e-6 and 1-l1-l2>=-1e-6:return l1*A[2]+l2*B[2]+(1-l1-l2)*C[2]
tris=[]
for A,B,C,m,f in col:
    n=np.cross(B-A,C-A);l=np.linalg.norm(n)
    if l<1e-9:continue
    nz=abs(n[2])/l;tris.append((A,B,C,nz))
    for c in cells(A,B,C):
        if nz>0.85:up[c].append((A,B,C))
        elif nz<0.5:wall[c].append((min(A[2],B[2],C[2]),max(A[2],B[2],C[2])))
        else:slope[c].append(((A[2]+B[2]+C[2])/3))
def floors(x,y):
    out=[]
    for A,B,C in up.get((int(np.floor(x/R)),int(np.floor(y/R))),[]):
        z=zat(A,B,C,x,y)
        if z is not None:out.append(z)
    return sorted(out)
# doodads (final root wmo)
d=open('out/wmo/goblinshipfinal.wmo','rb').read();i=0;ch={}
while i<len(d):
    t=d[i:i+4][::-1];s=struct.unpack_from('<I',d,i+4)[0];ch[t]=(i+8,s);i+=8+s
o,s=ch[b'MODD'];doods=[struct.unpack_from('<3f',d,o+k*40+4) for k in range(s//40)]
def ok(x,y,f,above=3.0,m=5):
    fl=floors(x,y)
    if any(f+0.05<z<f+above for z in fl):return False       # ceiling / platform overhead
    if sum(1 for z in fl if abs(z-f)<0.2)==0:return False
    for dx in range(-m,m+1):
        for dy in range(-m,m+1):
            c=(int(np.floor(x/R))+dx,int(np.floor(y/R))+dy)
            if any(f-0.3<zz<f+1.5 for zz in slope.get(c,[])):return False   # stairs / ramps within ~1 yd
            if abs(dx)<=m and abs(dy)<=m:
                for z0,z1 in wall.get(c,[]):
                    if z1>f+0.3 and z0<f+2.0:return False   # wall within ~1 yd
    for ex,ey in ((2,0),(-2,0),(0,2),(0,-2),(1.5,1.5),(1.5,-1.5),(-1.5,1.5),(-1.5,-1.5)):   # no drop-off / open edge within 2 yd
        if not any(abs(z-f)<0.5 for z in floors(x+ex,y+ey)):return False
    for p in doods:
        if abs(p[0]-x)<1.7 and abs(p[1]-y)<1.7 and p[2]<f+3 and p[2]>f-2.5:return False
    return True
zones=[(0.0,'x')]
def zones_fn(x,y):   # no-go: stairwell covers, lids, ladder hatches, stair corridor, stair landing in front of doors
    K=0.95/0.45
    for (cx0,cx1,cy0,cy1) in ((-0.55,1.2,-5.0,-3.7),(-0.55,1.2,1.4,2.65),(-4.2,-0.5,-2.2,-0.2),(-8.8,-3.3,-3.4,1.4)):
        pass
    return True
res=collections.defaultdict(list)
levels={'main':(1.2,2.2),'second':(6.4,6.9),'upper':(10.4,11.2),'roof':(14.0,14.9)}
for name,(lo,hi) in levels.items():
    for x in np.arange(-26,9.6,0.5):
        for y in np.arange(-13,9,0.5):
            for z in floors(x,y):
                if lo<=z<=hi and ok(x,y,z,m=(3 if name=='second' else 4)):res[name].append((round(float(x),2),round(float(y),2),round(float(z),2)));break
for k,v in res.items():print(k,len(v),v[:5])
json.dump(res,open('npc_cands.json','w'))
