import sys
sys.path.insert(0,'C:/CoA-Build/boats')
import shoot
from shoot import *
shoot.RS=(12,16,20,25,35,50,80)
for bx,by,deg in ((901,-3616,135),(892,-3616,24),(905,-3621,138),(903,-3618,114)):
    r1=search(bx,by,deg,False,n=30000,seed=4);r2=search(bx,by,deg,True,n=30000,seed=5)
    print((bx,by,deg),'APP',len(r1),r1[:1],'DEP',len(r2),r2[:1],flush=True)
