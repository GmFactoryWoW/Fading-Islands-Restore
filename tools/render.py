import sys,math
sys.path.insert(0,'C:/CoA-Build/boats')
from wmo_geo import *
from objs import objs,K
import terrain as T
from PIL import Image,ImageDraw
X0,X1,Y0,Y1=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]);S=float(sys.argv[5]);out=sys.argv[6]
W=int((Y1-Y0)*S);H=int((X1-X0)*S)
img=Image.new('RGB',(W,H),(20,60,110));dr=ImageDraw.Draw(img)
def px(x,y): return ((Y1-y)*S,(X1-x)*S)
txs=range(int(32-(Y1)/T.T.__float__() )-1,int(32-(Y0)/T.T)+2); tys=range(int(32-X1/T.T)-1,int(32-X0/T.T)+2)
pts=T.grid(list(txs),list(tys))
for (x,y),(h,wl) in pts.items():
    if X0<=x<=X1 and Y0<=y<=Y1:
        a,b=px(x,y)
        if wl is None or h>wl-0.5: dr.rectangle([a-S*2,b-S*2,a+S*2,b+S*2],fill=(70,120,60) if h<30 else (120,110,70))
        elif h>wl-12: dr.rectangle([a-S*2,b-S*2,a+S*2,b+S*2],fill=(40,100,150))
cache={}
allw=[]
for bx in txs:
    for by in tys:
        try: w,_=objs(bx,by)
        except Exception: continue
        allw+=w
seen=set()
for n,sx,sy,sz,rot,bb in allw:
    if (n,round(sx),round(sy)) in seen: continue
    seen.add((n,round(sx),round(sy)))
    lo=(K-bb[5],K-bb[3]);hi=(K-bb[2],K-bb[0])
    if hi[0]<X0 or lo[0]>X1 or hi[1]<Y0 or lo[1]>Y1: continue
    a1,b1=px(lo[0],lo[1]);a2,b2=px(hi[0],hi[1])
    nm=n.upper()
    isdock='DOCK' in nm
    if not isdock:
        dr.rectangle([min(a1,a2),min(b1,b2),max(a1,a2),max(b1,b2)],outline=(200,200,200))
        continue
    if nm not in cache: cache[nm]=load(n)
    tris=cache[nm]
    if not tris: continue
    ps=math.radians(-(rot[1]+90));c,s=math.cos(ps),math.sin(ps)
    pxf,pyf,pzf=K-sy,sz,K-sx
    for t in tris:
        P=[]
        for v in t:
            u,vv=v[0],v[1]
            Xf=pxf+c*u-s*vv;Zf=pzf+s*u+c*vv;hz=pyf+v[2]
            P.append((K-Zf,K-Xf,hz))
        ux,uy,uz=[P[1][i]-P[0][i] for i in range(3)];vx,vy,vz=[P[2][i]-P[0][i] for i in range(3)]
        nz=ux*vy-uy*vx
        zc=sum(p[2] for p in P)/3
        col=None
        if 'PILLAR' in nm: col=(220,60,60)
        elif -9<zc<-5.5: col=(240,220,80)
        else: col=(200,140,60)
        dr.polygon([px(p[0],p[1]) for p in P],fill=col)
d=ImageDraw.Draw(img)
a,b=px(893.87,-3620.84);d.ellipse([a-4,b-4,a+4,b+4],outline=(255,0,255),width=2)
for gx in range((X0//100+1)*100,X1,100):
    a,b=px(gx,Y1);d.line([0,b,W,b],fill=(255,255,255,40));d.text((2,b),'x=%d'%gx,fill=(255,255,255))
for gy in range((Y0//100+1)*100,Y1,100):
    a,b=px(X1,gy);d.line([a,0,a,H],fill=(255,255,255,40));d.text((a+2,2),'y=%d'%gy,fill=(255,255,255))
img.save(out);print(img.size)
