import sys,math
sys.path.insert(0,'C:/CoA-Build/boats')
import homedock as H
sx,sy=-14277.8,582.9
res=[]
for dbx in (29,30,31):
    for dby in (57,58,59):
        d=H.adt('Azeroth',dbx,dby)
        if not d:print('no tile',dbx,dby);continue
        for n,x,y,z,r,bb in H.wmos(d):
            res.append((math.hypot(x-sx,y-sy),n.split(H.BS)[-1],round(x),round(y),round(z,1)))
res.sort();print(len(res));[print(r) for r in res[:8]]
