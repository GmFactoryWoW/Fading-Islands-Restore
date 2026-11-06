import sys
sys.path.insert(0,'C:/CoA-Build/boats')
from shoot import *
for bx,by,deg in ((901,-3616,135),(905,-3621,138),(903,-3618,114),(888,-3625,114),(891,-3630,117),(892,-3631,300),(892,-3616,24)):
    r1=search(bx,by,deg,False,n=8000,seed=1);r2=search(bx,by,deg,True,n=8000,seed=2)
    print((bx,by,deg),'APP',len(r1),r1[:1],'DEP',len(r2),r2[:1],flush=True)
