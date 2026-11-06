import sys,math
sys.path.insert(0,'C:/CoA-Build/boats')
from dep2 import ok
from app2 import back
from dep2 import arc
import pickle
res=pickle.load(open('C:/CoA-Build/boats/berths.pkl','rb'))
cands=[(953,-3604,141),(963,-3610,144),(973,-3609,129),(955,-3600,126),(981,-3619,126),(989,-3629,117),(986,-3619,111),(904,-3603,156),(901,-3597,129),(880,-3627,126),(875,-3617,123)]
for bx,by,deg in cands:
    A=[];D=[]
    for st in (0,10,20,40):
      for turn in (1,-1):
        for R in (40,50,60,80):
            for tt in (60,90,120,150,180,210,240,270):
                p=back(bx,by,deg,turn,R,tt,straight=st,run=120)
                # require far end reaches open sea region inside raster (x<1000,y>-3500) 
                x,y,h=p[-1]
                if all(ok(*q) for q in p) and P_ok(x,y) if False else all(ok(*q) for q in p): A.append((st*3,turn,R,tt,round(x),round(y)))
    for turn in (1,-1):
        for R in (40,50,60,80,110):
            for tt in (45,90,135,180,225,270):
                p=arc(bx,by,deg,turn,R,tt,run=120)
                x,y,h=p[-1]
                if all(ok(*q) for q in p): D.append((turn,R,tt,round(x),round(y)))
    print((bx,by,deg),'APP',A[:4],'DEP',D[:4],flush=True)
