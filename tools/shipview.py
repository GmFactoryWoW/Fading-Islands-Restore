import sys
sys.path.insert(0,'C:/CoA-Build/boats')
from wmo_geo import *
from PIL import Image,ImageDraw
name=sys.argv[1];out=sys.argv[2]
tris=load(name);print(len(tris))
vs=[v for t in tris for v in t]
mn=[min(v[i] for v in vs) for i in range(3)];mx=[max(v[i] for v in vs) for i in range(3)];print(mn,mx)
S=8
W=int((mx[0]-mn[0])*S)+20;H=int((mx[1]-mn[1])*S)+20
img=Image.new('RGB',(W,H),(15,15,20));d=ImageDraw.Draw(img)
def P(v): return ((v[0]-mn[0])*S+10,(mx[1]-v[1])*S+10)
# floors colored by height
for t in tris:
    ux,uy,uz=[t[1][i]-t[0][i] for i in range(3)];vx,vy,vz=[t[2][i]-t[0][i] for i in range(3)]
    nx,ny,nz=uy*vz-uz*vy,uz*vx-ux*vz,ux*vy-uy*vx;L=(nx*nx+ny*ny+nz*nz)**.5
    if L<1e-9:continue
    zc=sum(v[2] for v in t)/3
    if nz/L>0.9 and -1<zc<4: d.polygon([P(v) for v in t],fill=(60,140,60))
    elif nz/L>0.9 and 4<=zc<9: d.polygon([P(v) for v in t],fill=(60,100,160))
    elif nz/L>0.9: d.polygon([P(v) for v in t],fill=(140,100,60))
for t in tris:
    ux,uy,uz=[t[1][i]-t[0][i] for i in range(3)];vx,vy,vz=[t[2][i]-t[0][i] for i in range(3)]
    nx,ny,nz=uy*vz-uz*vy,uz*vx-ux*vz,ux*vy-uy*vx;L=(nx*nx+ny*ny+nz*nz)**.5
    if L<1e-9:continue
    zs=[v[2] for v in t]
    if abs(nz/L)<0.3 and min(zs)<4 and max(zs)>2.5 and min(zs)>-1: d.line([P(t[0]),P(t[1]),P(t[2]),P(t[0])],fill=(255,80,80))
d.text((5,5),'X+ = bow (right).  green deck z-1..4 blue 4..9 brown>9  red=rails/walls',fill=(255,255,255))
img.save(out);print(img.size)
