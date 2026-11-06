import sys,math,io,contextlib
sys.path.insert(0,'C:/CoA-Build/boats')
with contextlib.redirect_stdout(io.StringIO()):
    import shoot
shoot.RS=(18,22,28,35,50,70,100)
H=127.6;a=(math.cos(math.radians(H)),math.sin(math.radians(H)));n=(a[1],-a[0]);C=(898.43,-3626.76)
for side,lat,lon in (('NW',12.0,4.0),('NW',12.0,6.0),('NW',9.5,4.0),('SE',-9.5,4.0),('SE',-12.0,2.0)):
    bx=C[0]+lat*n[0]+lon*a[0];by=C[1]+lat*n[1]+lon*a[1]
    r1=shoot.search(bx,by,H,False,n=60000,seed=8)
    print(side,lat,lon,(round(bx,1),round(by,1)),'APP',len(r1),r1[:1],flush=True)
