import sys
sys.path.insert(0,'C:/CoA-Build/boats')
import terrain as T, numpy as np
from PIL import Image,ImageDraw
X0,X1,Y0,Y1=-100,1900,-4900,-2900
S=0.5
txs=range(int(32-Y1/T.T)-1,int(32-Y0/T.T)+2);tys=range(int(32-X1/T.T)-1,int(32-X0/T.T)+2)
print(list(txs),list(tys))
pts=T.grid(list(txs),list(tys))
W=int((Y1-Y0)*S);H=int((X1-X0)*S)
a=np.zeros((H,W,3),np.uint8);a[:]=(15,30,70)
for (x,y),(h,wl) in pts.items():
    if X0<=x<=X1 and Y0<=y<=Y1:
        c=int((Y1-y)*S);r=int((X1-x)*S)
        if c>=W or r>=H:continue
        w=-8.56 if wl is None else wl
        if h>w-0.5: a[r,c]=(80,140,60) if h<w+40 else (150,130,80)
        elif h>w-15: a[r,c]=(40,100,160)
        elif h>w-30: a[r,c]=(25,60,120)
img=Image.fromarray(a);d=ImageDraw.Draw(img)
def px(x,y): return ((Y1-y)*S,(X1-x)*S)
for gx in range(0,1900,200):
    _,b=px(gx,Y1);d.line([0,b,W,b],fill=(90,90,90));d.text((2,b),'x=%d'%gx,fill=(255,255,255))
for gy in range(-4800,-2900,200):
    a_,_=px(X1,gy);d.line([a_,0,a_,H],fill=(90,90,90));d.text((a_+2,2),'y=%d'%gy,fill=(255,255,255))
a_,b=px(893.87,-3620.84);d.ellipse([a_-5,b-5,a_+5,b+5],outline=(255,0,255),width=2)
img.save('C:/CoA-Build/boats/bigmap.png');print(img.size)
