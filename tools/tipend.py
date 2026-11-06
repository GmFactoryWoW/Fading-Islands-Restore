import sys,math,io,contextlib
sys.path.insert(0,'C:/CoA-Build/boats')
with contextlib.redirect_stdout(io.StringIO()):
    import shoot
shoot.RS=(10,12,16,20,25,35,50)
a=math.radians(127.6);d=(math.cos(a),math.sin(a));tip=(893.74,-3620.65)
for gap in (1.0,2.0,3.0):
    o=(tip[0]+(gap+8.3)*d[0],tip[1]+(gap+8.3)*d[1],307.6)
    r1=shoot.search(*o,False,n=3000,seed=1);r2=shoot.search(*o,True,n=30000,seed=2)
    print('gap',gap,'origin',[round(v,2) for v in o],'berth ok',shoot.okb(*o),'APP',len(r1),r1[:1],'DEP',len(r2),r2[:1],flush=True)
