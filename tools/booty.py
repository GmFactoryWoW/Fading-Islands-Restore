import sys,math
sys.path.insert(0,'C:/CoA-Build/boats')
from homedock import *
sx,sy=-14277.8,582.9
for dbx in (29,30,31):
    for dby in (57,58,59):
        d=adt('Azeroth',dbx,dby)
        if not d:continue
        for n,x,y,z,r,bb in wmos(d):
            if math.hypot(x-sx,y-sy)<120:print(dbx,dby,n.split(BS)[-1],'pos %.0f %.0f z %.1f'%(x,y,z),'dist %.0f'%math.hypot(x-sx,y-sy))
