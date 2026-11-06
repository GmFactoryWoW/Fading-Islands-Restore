import sys,math,io,contextlib
sys.path.insert(0,'C:/CoA-Build/boats')
with contextlib.redirect_stdout(io.StringIO()):
    import shoot
shoot.RS=(10,12,16,20,25,35,50)
H=127.6;a=(math.cos(math.radians(H)),math.sin(math.radians(H)));n=(a[1],-a[0]);C=(898.43,-3626.76)
for lat,lon in ((8.2,2.5),(8.2,3.5),(8.4,3.0),(8.6,2.5)):
    bx=C[0]+lat*n[0]+lon*a[0];by=C[1]+lat*n[1]+lon*a[1]
    r1=shoot.search(bx,by,H,False,n=20000,seed=4);r2=shoot.search(bx,by,H,True,n=8000,seed=5)
    print(lat,lon,(round(bx,2),round(by,2)),'ok',shoot.okb(bx,by,H),'APP',len(r1),r1[:1],'DEP',len(r2),r2[:1],flush=True)
