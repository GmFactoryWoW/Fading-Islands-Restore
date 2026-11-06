import sys,math,pickle,heapq
sys.path.insert(0,'C:/CoA-Build/boats')
import numpy as np
from plan1_lib import *
STEP=3                      # heading bin (deg)
NH=360//STEP
FREE={}
def free(h):
    if h not in FREE: FREE[h]=freemap(h*STEP)
    return FREE[h]
def ok(x,y,h):
    r=int(round(X1-x));c=int(round(Y1-y))
    if r<0 or c<0 or r>=H or c>=W:return True   # outside raster = open (assumed sea; checked separately)
    return bool(free(h)[r,c])
L=10.0
def astar(start,goal,gtol=8.0,maxn=400000,limit=None):
    sx,sy,sh=start;gx,gy,gh=goal
    key=lambda x,y,h:(int(round(x/2)),int(round(y/2)),h)
    pq=[(0,0,sx,sy,sh)];came={};g={key(sx,sy,sh):0};par={}
    n=0
    while pq and n<maxn:
        f,gc,x,y,h=heapq.heappop(pq);n+=1
        if math.hypot(x-gx,y-gy)<gtol and min((h-gh)%NH,(gh-h)%NH)<=1:
            path=[(x,y,h)];k=key(x,y,h)
            while k in par:
                px,py,ph,k=par[k];path.append((px,py,ph))
            return path[::-1]
        if gc>g.get(key(x,y,h),1e18)+1e-6:continue
        for dh in (-3,-2,-1,0,1,2,3):
            nh=(h+dh)%NH;a=math.radians(nh*STEP)
            nx=x+L*math.cos(a);ny=y+L*math.sin(a)
            if not ok(nx,ny,nh):continue
            r=int(round(X1-nx));c=int(round(Y1-ny))
            sh_pen=3.0 if (0<=r<H and 0<=c<W and shal[r,c]) else 0
            nc=gc+L+0.6*abs(dh)*STEP+sh_pen
            k=key(nx,ny,nh)
            if nc<g.get(k,1e18)-1e-6:
                g[k]=nc;par[k]=(x,y,h,key(x,y,h))
                heapq.heappush(pq,(nc+math.hypot(nx-gx,ny-gy),nc,nx,ny,nh))
    print('astar fail nodes',n);return None
if __name__=='__main__':
    res=pickle.load(open('C:/CoA-Build/boats/berths.pkl','rb'))
    sc,deg,nm,bx,by=res[0];print('berth',sc,deg,nm,bx,by)
    h0=int(round(deg/STEP))%NH;a=math.radians(h0*STEP)
    # pre-berth point 40yd before the berth along the heading, and post-berth 40 yd after
    pre=(bx-40*math.cos(a),by-40*math.sin(a),h0);post=(bx+40*math.cos(a),by+40*math.sin(a),h0)
    print('pre ok',ok(*pre),'post ok',ok(*post))
    print('berth ok',ok(bx,by,h0))
    # approach: from open sea W/S of the dock
    for st in ((850,-3450),(700,-3500),(800,-3700),(1000,-3500)):
        for sh in range(0,NH,10):
            if ok(st[0],st[1],sh):
                p=astar((st[0],st[1],sh),pre);print('approach from',st,'->',None if p is None else len(p)*L);break
    q=astar(post,(700,-3500,0),gtol=40)  # any heading goal ignored via tolerance? see below
