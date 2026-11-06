"""1-yd obstacle raster for the dock area. layers: LAND (terrain above water-0.5), SHALLOW (terrain above keel depth), STRUCT (any WMO tri overlapping ship vertical band), PIER (dock deck/pillar tris)."""
import sys,math,pickle
sys.path.insert(0,'C:/CoA-Build/boats')
import numpy as np
from wmo_geo import *
from objs import objs,K
import terrain as T
from PIL import Image,ImageDraw
X0,X1,Y0,Y1=450,1300,-4100,-2950
WL=-8.56
H=X1-X0;W=Y1-Y0
def rc(x,y): return (Y1-y),(X1-x)   # (col,row) in px, 1px = 1yd
land=np.zeros((H,W),bool);shal=np.zeros((H,W),bool);terr=np.full((H,W),-999.0)
txs=range(int(32-Y1/T.T)-1,int(32-Y0/T.T)+2);tys=range(int(32-X1/T.T)-1,int(32-X0/T.T)+2)
pts=T.grid(list(txs),list(tys))
for (x,y),(h,wl) in pts.items():
    if X0<=x<X1 and Y0<=y<Y1:
        c=int(Y1-y);r=int(X1-x)
        if 0<=r<H and 0<=c<W: terr[r,c]=max(terr[r,c],h)
# fill gaps from sparse samples (4yd grid) by max-dilation
from scipy.ndimage import maximum_filter
terr=maximum_filter(terr,size=5)
land=terr>WL-0.3
shal=terr>WL-13      # keel at -11.65 below water
img_struct=Image.new('L',(W,H),0);ds=ImageDraw.Draw(img_struct)
img_pier=Image.new('L',(W,H),0);dp=ImageDraw.Draw(img_pier)
cache={}
seen=set();bad=0
for bx in txs:
  for by in tys:
    try:w,_=objs(bx,by)
    except Exception:continue
    for n,sx,sy,sz,rot,bb in w:
        key=(n,round(sx),round(sy))
        if key in seen:continue
        seen.add(key)
        lo=(K-bb[5],K-bb[3]);hi=(K-bb[2],K-bb[0])
        if hi[0]<X0 or lo[0]>X1 or hi[1]<Y0 or lo[1]>Y1:continue
        nm=n.upper();isd='DOCK' in nm
        zlo,zhi=bb[1],bb[4]
        if zhi<WL-14 or zlo>WL+8: continue         # not in the ship's vertical band
        tilted=abs(abs(rot[0])-180)>3 or abs(abs(rot[2])-180)>3
        if tilted or nm not in cache and False:
            a1,b1=rc(lo[0],lo[1]);a2,b2=rc(hi[0],hi[1])
            ds.rectangle([min(a1,a2),min(b1,b2),max(a1,a2),max(b1,b2)],fill=255);continue
        if nm not in cache: cache[nm]=load(n)
        tris=cache[nm]
        if not tris: 
            a1,b1=rc(lo[0],lo[1]);a2,b2=rc(hi[0],hi[1]);ds.rectangle([min(a1,a2),min(b1,b2),max(a1,a2),max(b1,b2)],fill=255);continue
        ps=math.radians(-(rot[1]+90));c,s=math.cos(ps),math.sin(ps)
        pxf,pyf,pzf=K-sy,sz,K-sx
        for t in tris:
            P=[]
            for v in t:
                Xf=pxf+c*v[0]-s*v[1];Zf=pzf+s*v[0]+c*v[1];P.append((K-Zf,K-Xf,pyf+v[2]))
            zs=[p[2] for p in P]
            if max(zs)<WL-14 or min(zs)>WL+8:continue
            poly=[rc(p[0],p[1]) for p in P]
            (dp if isd else ds).polygon(poly,fill=255)
struct=np.array(img_struct)>0;pier=np.array(img_pier)>0
np.savez_compressed('C:/CoA-Build/boats/obs.npz',land=land,shal=shal,struct=struct,pier=pier,terr=terr,X0=X0,X1=X1,Y0=Y0,Y1=Y1)
print('saved',land.sum(),shal.sum(),struct.sum(),pier.sum())
