import sys,math,pickle
sys.path.insert(0,'C:/CoA-Build/boats')
import numpy as np
from scipy.signal import fftconvolve
from scipy.ndimage import distance_transform_edt, binary_dilation
from PIL import Image,ImageDraw
from wmo_geo import load
BS=chr(92)
d=np.load('C:/CoA-Build/boats/obs.npz');X0,X1,Y0,Y1=[int(d[k]) for k in('X0','X1','Y0','Y1')]
land,shal,struct,pier=d['land'],d['shal'],d['struct'],d['pier']
H,W=land.shape
# hull outline (convex hull of waterline-band vertices, excludes bowsprit/masts)
tris=load(BS.join(['world','wmo','kalimdor','lostisles','goblinshipfinal.wmo']))
pts=np.array([(v[0],v[1]) for t in tris for v in t if -9<v[2]<3.5])
from scipy.spatial import ConvexHull
hull=pts[ConvexHull(pts).vertices]
print('hull x',hull[:,0].min(),hull[:,0].max(),'y',hull[:,1].min(),hull[:,1].max())
pickle.dump(hull,open('C:/CoA-Build/boats/hull.pkl','wb'))
DPIER=distance_transform_edt(~pier)           # yd to nearest pier pixel
SOL=land|struct
DSOL=distance_transform_edt(~SOL)
KS=61  # kernel half size
def kernel(poly_local,theta):
    c,s=math.cos(theta),math.sin(theta)
    img=Image.new('L',(2*KS+1,2*KS+1),0);dr=ImageDraw.Draw(img)
    P=[]
    for lx,ly in poly_local:
        wx=c*lx-s*ly;wy=s*lx+c*ly      # world offset (x north, y west)
        P.append((KS-wy,KS-wx))          # col=-dy, row=-dx
    dr.polygon(P,fill=255);return np.array(img)>0
def pts_kernel(ptlist,theta):
    c,s=math.cos(theta),math.sin(theta);k=np.zeros((2*KS+1,2*KS+1),np.float32)
    for lx,ly in ptlist:
        wx=c*lx-s*ly;wy=s*lx+c*ly
        r=int(round(KS-wx));q=int(round(KS-wy))
        if 0<=r<2*KS+1 and 0<=q<2*KS+1:k[r,q]+=1
    return k
def corr(A,K): return fftconvolve(A.astype(np.float32),K[::-1,::-1],mode='same')
obsSol=(DSOL<3.0)                 # hull must stay 3 yd from land/structures
obsPier=(DPIER<0.8)               # and never touch the pier
band=((DPIER>=0.8)&(DPIER<=3.0))  # gap band along the pier edge
res=[]
sideA=[(x,-14.6) for x in np.arange(-3,34,1.0)]; sideB=[(x,9.4) for x in np.arange(-3,34,1.0)]
for deg in range(0,360,3):
    phi=math.radians(deg);th=phi+math.pi
    k=kernel(hull,th)
    bad=corr(obsSol|obsPier,k.astype(np.float32))
    free=bad<0.5
    # also all hull pixels must avoid land entirely: covered by obsSol
    for nm,sd in (('A',sideA),('B',sideB)):
        sc=corr(band,pts_kernel(sd,th))
        ok=free&(sc>=26)
        rr,cc=np.nonzero(ok)
        for r,c in zip(rr,cc): res.append((sc[r,c],deg,nm,X1-r,Y1-c))
res.sort(reverse=True)
print(len(res))
pickle.dump(res,open('C:/CoA-Build/boats/berths.pkl','wb'))
seen=[]
for sc,deg,nm,x,y in res[:4000]:
    if any(abs(x-a)<12 and abs(y-b)<12 and abs(deg-g)<20 for a,b,g in seen):continue
    seen.append((x,y,deg));print('score %.0f heading %d side %s origin x %.0f y %.0f'%(sc,deg,nm,x,y))
    if len(seen)>=12:break
