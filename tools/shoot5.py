import sys,math,random,io,contextlib
sys.path.insert(0,'C:/CoA-Build/boats')
import shoot
bx,by,deg=953,-3604,141
rnd=random.Random(5);best=[]
for i in range(120000):
    segs=[('A',-1,rnd.choice((30,35,40,45)),rnd.choice((120,135,150,165,180)))]
    if rnd.random()<0.7:segs.append(('A',rnd.choice((1,-1)),rnd.choice((65,90,130,200)),rnd.choice((20,45,70,90))))
    segs.append(('S',rnd.choice((250,350,450))))
    p=shoot.gen(bx,by,deg,segs,False)
    if not shoot.far_open(p):continue
    if not all(shoot.okb(x,y,h) for x,y,h in p[::4]):continue
    if shoot.valid(p):
        mx=max(x for x,y,h in p)
        best.append((mx,segs,[round(v) for v in p[-1]]))
        if len(best)>=25:break
best.sort(key=lambda b:b[0]);print(len(best))
for b in best[:5]:print(round(b[0]),b[1],b[2])
