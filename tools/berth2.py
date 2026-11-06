import sys,math,io,contextlib
sys.path.insert(0,'C:/CoA-Build/boats')
with contextlib.redirect_stdout(io.StringIO()):
    import shoot
from shoot import *
H=127.6;a=(math.cos(math.radians(H)),math.sin(math.radians(H)));n=(a[1],-a[0])
C=(898.43,-3626.76)
for lat in (8.4,8.8):
    for lon in (0.0,1.0):
        bx=C[0]+lat*n[0]+lon*a[0];by=C[1]+lat*n[1]+lon*a[1]
        r1=search(bx,by,H,False,n=25000,seed=4);r2=search(bx,by,H,True,n=25000,seed=5)
        print(lat,lon,(round(bx,2),round(by,2)),'berth ok',okb(bx,by,H),'APP',len(r1),r1[:1],'DEP',len(r2),r2[:1],flush=True)
