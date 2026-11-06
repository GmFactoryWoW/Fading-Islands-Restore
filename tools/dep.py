import sys,math
sys.path.insert(0,'C:/CoA-Build/boats')
from plan2 import ok,STEP,NH
def pose_ok(x,y,hd):
    return ok(x,y,int(round(hd/STEP))%NH)
def arc(bx,by,deg,turn,R,tot_turn,run=300):
    x,y,h=bx,by,deg;pts=[(x,y,h)];ds=3.0
    for s in range(int(40/ds)):   # 40 yd straight first
        x+=ds*math.cos(math.radians(h));y+=ds*math.sin(math.radians(h));pts.append((x,y,h))
    turned=0
    while turned<tot_turn:
        dh=math.degrees(ds/R);h+=turn*dh;turned+=dh
        x+=ds*math.cos(math.radians(h));y+=ds*math.sin(math.radians(h));pts.append((x,y,h))
    for s in range(int(run/ds)):
        x+=ds*math.cos(math.radians(h));y+=ds*math.sin(math.radians(h));pts.append((x,y,h))
    return pts
for bx,by,deg in ((992,-3644,303),(983,-3628,330),(883,-3640,303)):
    for turn in (+1,-1):
        for R in (50,70,90,120):
            for tt in (60,90,135,180):
                p=arc(bx,by,deg,turn,R,tt)
                bad=[i for i,(x,y,h) in enumerate(p) if not pose_ok(x,y,h)]
                if not bad: print('OK',(bx,by,deg),'turn',turn,'R',R,'by',tt)
        print((bx,by,deg),'turn',turn,'done')
