import sys,math
sys.path.insert(0,'C:/CoA-Build/boats')
from objs import *
BS=chr(92)
res=[]
for bx,by in ((37,29),(37,30),(37,31),(38,29),(38,30),(38,31),(39,29),(39,30),(39,31)):
    try: w,dd=objs(bx,by)
    except Exception as e: continue
    for n,x,y,z,r,bb in w:
        lo=(K-bb[5],K-bb[3],bb[1]);hi=(K-bb[2],K-bb[0],bb[4])  # server (x,y,z) box
        res.append((n,x,y,z,r,lo,hi))
seen=set()
for n,x,y,z,r,lo,hi in res:
    if math.hypot(x-894,y+3620)<260 and (n,round(x),round(y)) not in seen:
        seen.add((n,round(x),round(y)))
        print(n.split(BS)[-1][:42].ljust(42),'pos %.0f %.0f %.1f yaw %.0f'%(x,y,z,r[1]),'box x %.0f..%.0f y %.0f..%.0f z %.1f..%.1f'%(lo[0],hi[0],lo[1],hi[1],lo[2],hi[2]))
