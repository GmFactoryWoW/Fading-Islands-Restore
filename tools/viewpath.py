import sys,math,pickle
sys.path.insert(0,'C:/CoA-Build/boats')
import numpy as np
from PIL import Image,ImageDraw
import plan1_lib as P
from app2 import back
from dep2 import arc,ok
def build(bx,by,deg,aturn,aR,att,ast,dturn,dR,dtt,run=250):
    A=back(bx,by,deg,aturn,aR,att,straight=ast,run=run)[::-1]
    D=arc(bx,by,deg,dturn,dR,dtt,run=run)
    return A,D
def render(A,D,berth,out):
    S=3
    a=np.zeros((P.H,P.W,3),np.uint8);a[:]=(15,35,90)
    a[P.shal]=(40,100,160);a[P.land]=(80,140,60);a[P.struct]=(150,150,150);a[P.pier]=(240,220,80)
    img=Image.fromarray(a).resize((P.W*S,P.H*S),Image.NEAREST);d=ImageDraw.Draw(img)
    px=lambda x,y:((P.Y1-y)*S,(P.X1-x)*S)
    def hullat(x,y,h,col):
        th=math.radians(h)+math.pi;c,s=math.cos(th),math.sin(th)
        d.polygon([px(x+c*lx-s*ly,y+s*lx+c*ly) for lx,ly in P.hull],outline=col)
    for i in range(0,len(A),10):hullat(*A[i],(255,120,120))
    for i in range(0,len(D),10):hullat(*D[i],(120,255,120))
    hullat(*berth,(255,0,255))
    d.line([px(x,y) for x,y,h in A+D],fill=(255,255,255))
    img.crop((0,0,P.W*S,P.H*S)).save(out)
if __name__=='__main__':
    A,D=build(953,-3604,141,-1,45,30,0,1,110,45)
    render(A,D,(953,-3604,141),'C:/CoA-Build/boats/path1.png')
    print(len(A),len(D),A[0],D[-1])
