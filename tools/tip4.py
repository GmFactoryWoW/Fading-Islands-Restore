import sys,math,io,contextlib
sys.path.insert(0,'C:/CoA-Build/boats')
with contextlib.redirect_stdout(io.StringIO()):
    import shoot
shoot.RS=(18,22,28,35,50,70)
H=127.6;a=(math.cos(math.radians(H)),math.sin(math.radians(H)));n=(a[1],-a[0]);C=(898.43,-3626.76)
# n = toward NW (+) ; hull y range -7.1..4.8 (local +Y = right of travel). pier half width 3.4
res=[]
for side,lat in (('NW',3.4+1.3+7.1),('NW2',3.4+1.3+4.8),('SE',-(3.4+1.3+4.8)),('SE2',-(3.4+1.3+7.1))):
    for lon in (-2.0,0.0,2.0,4.0,6.0):
        bx=C[0]+lat*n[0]+lon*a[0];by=C[1]+lat*n[1]+lon*a[1]
        okb=shoot.okb(bx,by,H)
        if not okb: continue
        r1=shoot.search(bx,by,H,False,n=6000,seed=4);r2=shoot.search(bx,by,H,True,n=4000,seed=5)
        print(side,lon,(round(bx,1),round(by,1)),'APP',len(r1),r1[:1],'DEP',len(r2),r2[:1],flush=True)
