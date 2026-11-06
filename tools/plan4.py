import sys,math,pickle,time
sys.path.insert(0,'C:/CoA-Build/boats')
import plan2
from plan2 import *
import heapq
def astar_any(start,goalpt,gtol,maxn=60000):
    # heading-free goal
    sx,sy,sh=start;gx,gy=goalpt
    key=lambda x,y,h:(int(round(x/2)),int(round(y/2)),h)
    pq=[(0,0,sx,sy,sh)];g={key(sx,sy,sh):0};par={};n=0
    while pq and n<maxn:
        f,gc,x,y,h=heapq.heappop(pq);n+=1
        if math.hypot(x-gx,y-gy)<gtol:
            path=[(x,y,h)];k=key(x,y,h)
            while k in par:
                px,py,ph,k=par[k];path.append((px,py,ph))
            return path[::-1]
        if gc>g.get(key(x,y,h),1e18)+1e-6:continue
        for dh in (-3,-2,-1,0,1,2,3):
            nh=(h+dh)%NH;a=math.radians(nh*STEP);nx=x+L*math.cos(a);ny=y+L*math.sin(a)
            if not ok(nx,ny,nh):continue
            r=int(round(X1-nx));c=int(round(Y1-ny))
            nc=gc+L+0.6*abs(dh)*STEP+(3 if (0<=r<H and 0<=c<W and shal[r,c]) else 0)
            k=key(nx,ny,nh)
            if nc<g.get(k,1e18)-1e-6:
                g[k]=nc;par[k]=(x,y,h,key(x,y,h));heapq.heappush(pq,(nc+math.hypot(nx-gx,ny-gy),nc,nx,ny,nh))
    return None
def astar_to(start,goalpose,maxn=60000):
    return plan2.astar(start,goalpose,gtol=6.0,maxn=maxn)
cands=[(880,-3627,126),(953,-3604,141),(875,-3617,123),(992,-3644,303),(901,-3597,129),(981,-3619,126),(989,-3629,117),(983,-3628,330),(883,-3640,303),(963,-3610,144)]
T=(840,-3560)
for bx,by,deg in cands:
    h0=int(round(deg/STEP))%NH;a=math.radians(h0*STEP)
    # departure from berth forward to the open sea target
    t=time.time()
    dep=astar_any((bx,by,h0),T,25,maxn=30000)
    # approach: reverse problem via forward search from many start headings near T
    app=None
    for sh in range(0,NH,6):
        if ok(T[0],T[1],sh):
            app=astar((T[0],T[1],sh),(bx,by,h0),gtol=6.0,maxn=30000)
            if app:break
    print((bx,by,deg),'depart',None if dep is None else int(len(dep)*L),'approach',None if app is None else int(len(app)*L),'%.0fs'%(time.time()-t))
