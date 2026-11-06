import numpy as np
from PIL import Image,ImageDraw
d=np.load('C:/CoA-Build/boats/obs.npz');X0,X1,Y0,Y1=[int(d[k]) for k in('X0','X1','Y0','Y1')]
H,W=d['land'].shape
a=np.zeros((H,W,3),np.uint8);a[:]=(15,35,90)
a[d['shal']]=(40,100,160);a[d['land']]=(80,140,60);a[d['struct']]=(170,170,170);a[d['pier']]=(240,220,80)
img=Image.fromarray(a).resize((W*2,H*2),Image.NEAREST);dr=ImageDraw.Draw(img)
for gx in range(X0//50*50+50,X1,50):
    r=(X1-gx)*2;dr.line([0,r,W*2,r],fill=(80,80,80));dr.text((2,r),'x=%d'%gx,fill=(255,255,255))
for gy in range(Y0//50*50+50,Y1,50):
    c=(Y1-gy)*2;dr.line([c,0,c,H*2],fill=(80,80,80));dr.text((c+2,2),'y=%d'%gy,fill=(255,255,255))
c,r=(Y1+3620.84)*2,(X1-893.87)*2;dr.ellipse([c-5,r-5,c+5,r+5],outline=(255,0,255),width=2)
img.save('C:/CoA-Build/boats/obs.png');print(img.size)
