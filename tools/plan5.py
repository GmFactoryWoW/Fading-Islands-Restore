import sys,math,pickle,time
sys.path.insert(0,'C:/CoA-Build/boats')
import plan2
from plan2 import *
cands=[(953,-3604,141),(963,-3610,144),(981,-3619,126),(989,-3629,117),(901,-3597,129),(880,-3627,126),(875,-3617,123)]
starts=[(840,-3560),(900,-3480),(1000,-3500),(1050,-3520)]
for bx,by,deg in cands:
    h0=int(round(deg/STEP))%NH
    best=None;t=time.time()
    for T in starts:
        for sh in range(0,NH,10):
            if ok(T[0],T[1],sh):
                app=astar((T[0],T[1],sh),(bx,by,h0),gtol=6.0,maxn=1200000)
                if app:best=(T,app);break
        if best:break
    print((bx,by,deg),'approach',None if not best else (best[0],int(len(best[1])*L)),'%.0fs'%(time.time()-t),flush=True)
    if best: pickle.dump(best,open('C:/CoA-Build/boats/app_%d_%d.pkl'%(bx,by),'wb'))
