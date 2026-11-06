import sys,math,io,contextlib
sys.path.insert(0,'C:/CoA-Build/boats')
with contextlib.redirect_stdout(io.StringIO()):
    import shoot
shoot.RS=(12,14,16,18,22,28,35,50)
C=(898.43,-3626.76)
for H in (127.6,135.0,142.0,120.0):
    a=(math.cos(math.radians(H)),math.sin(math.radians(H)));n=(a[1],-a[0])
    for lat,lon in ((11.0,4.0),(12.5,6.0),(10.0,2.0)):
        bx=C[0]+lat*n[0]+lon*a[0];by=C[1]+lat*n[1]+lon*a[1]
        if not shoot.okb(bx,by,H):continue
        r1=shoot.search(bx,by,H,False,n=30000,seed=9)
        r2=shoot.search(bx,by,H,True,n=3000,seed=9)
        print(H,lat,lon,(round(bx,1),round(by,1)),'APP',len(r1),r1[:1],'DEP',len(r2),r2[:1],flush=True)
