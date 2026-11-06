import sys,math,random,io,contextlib
sys.path.insert(0,'C:/CoA-Build/boats')
import shoot
ex,ey,eh=622.0,-3336.0,141.0   # end of DEP in route2 (approx; take exact from gen)
rnd=random.Random(2);found=[]
for i in range(40000):
    segs=[];tot=0
    while tot<500:
        if rnd.random()<0.4:
            L=rnd.choice((60,100,150,200));segs.append(('S',L));tot+=L
        else:
            R=rnd.choice((60,90,130,200));ang=rnd.choice((20,40,60,90));segs.append(('A',rnd.choice((1,-1)),R,ang));tot+=R*math.radians(ang)
    if not 500<=tot<=620:continue
    p=shoot.gen(ex,ey,eh,segs,True)
    if all(shoot.okb(x,y,h) for x,y,h in p[::3]):
        L2=sum(math.hypot(b[0]-a[0],b[1]-a[1]) for a,b in zip(p,p[1:]))
        found.append((abs(L2-530),segs,[round(v) for v in p[-1]],round(L2)))
        if len(found)>=15:break
found.sort(key=lambda f:f[0])
for f in found[:4]:print(f[1:],)
