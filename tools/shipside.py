import sys
sys.path.insert(0,'C:/CoA-Build/boats')
from wmo_geo import *
from PIL import Image,ImageDraw
tris=load(sys.argv[1]);S=8
vs=[v for t in tris for v in t]
mn=[min(v[i] for v in vs) for i in range(3)];mx=[max(v[i] for v in vs) for i in range(3)]
W=int((mx[0]-mn[0])*S)+20;H=int((mx[2]-mn[2])*S)+20
img=Image.new('RGB',(W,H),(15,15,20));d=ImageDraw.Draw(img)
P=lambda v:((v[0]-mn[0])*S+10,(mx[2]-v[2])*S+10)
for t in tris: d.polygon([P(v) for v in t],outline=(120,160,220))
y0=(mx[2]-0)*S+10;d.line([0,y0,W,y0],fill=(255,0,0));d.text((5,5),'side view, X+ right, red=z0',fill=(255,255,255))
img.save(sys.argv[2])
