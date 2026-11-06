import sys,math,io,contextlib,pickle
sys.path.insert(0,'C:/CoA-Build/boats')
import numpy as np
from PIL import Image,ImageDraw
from shoot import *
import plan1_lib as P
bx,by,deg=953,-3604,141
appsegs=[('A',-1,40,150),('A',-1,130,45),('S',350)]
depsegs=[('S',80),('S',350)]
A=gen(bx,by,deg,appsegs,False)[::-1]      # travel order: far start -> berth
D=gen(bx,by,deg,depsegs,True)               # berth -> far end
print('approach pts',len(A),'start',[round(v) for v in A[0]],'depart pts',len(D),'end',[round(v) for v in D[-1]])
# clearance incl. crude struct boxes
dS=P.distance_transform_edt(~(P.land|P.struct))
dL=P.distance_transform_edt(~P.land)
def clr(path):
    m=1e9;ms=1e9
    for x,y,h in path:
        r=int(round(P.X1-x));c=int(round(P.Y1-y))
        if 0<=r<P.H and 0<=c<P.W:m=min(m,dL[r,c]);ms=min(ms,dS[r,c])
    return m,ms
print('centerline clearance land %.0f / land+structboxes %.0f yd'%clr(A+D))
pickle.dump((A,D,(bx,by,deg)),open('C:/CoA-Build/boats/route.pkl','wb'))
S=1
a=np.zeros((P.H,P.W,3),np.uint8);a[:]=(15,35,90)
a[P.shal]=(40,100,160);a[P.land]=(80,140,60);a[P.struct]=(150,150,150);a[P.pier]=(240,220,80)
img=Image.fromarray(a);d=ImageDraw.Draw(img)
px=lambda x,y:((P.Y1-y)*S,(P.X1-x)*S)
def hullat(x,y,h,col):
    th=math.radians(h)+math.pi;c,s=math.cos(th),math.sin(th)
    d.polygon([px(x+c*lx-s*ly,y+s*lx+c*ly) for lx,ly in P.hull],outline=col)
for i in range(0,len(A),12):hullat(*A[i],(255,110,110))
for i in range(0,len(D),12):hullat(*D[i],(110,255,110))
hullat(bx,by,deg,(255,0,255))
for gx in range(500,1300,100):
    _,r=px(gx,P.Y1);d.line([0,r,P.W,r],fill=(70,70,70));d.text((2,r),'x=%d'%gx,fill=(255,255,255))
for gy in range(-4000,-2900,100):
    c,_=px(P.X1,gy);d.line([c,0,c,P.H],fill=(70,70,70));d.text((c+2,2),'y=%d'%gy,fill=(255,255,255))
img.crop((250,200,1000,700)).resize((1500,1000)).save('C:/CoA-Build/boats/route.png')
