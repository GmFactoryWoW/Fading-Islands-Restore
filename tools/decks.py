import sys,collections
sys.path.insert(0,'C:/CoA-Build/boats')
import wmo_geo as g
BS=chr(92)
def decks(path,n=6):
    t=g.load(BS.join(path));lv=collections.defaultdict(lambda:[0,1e9,-1e9,1e9,-1e9])
    for a,b,c in t:
        u=[b[i]-a[i] for i in range(3)];w=[c[i]-a[i] for i in range(3)]
        nx=u[1]*w[2]-u[2]*w[1];ny=u[2]*w[0]-u[0]*w[2];nz=u[0]*w[1]-u[1]*w[0];L=(nx*nx+ny*ny+nz*nz)**.5
        if L>1e-6 and nz/L>.95:
            z=round((a[2]+b[2]+c[2])/3*4)/4;e=lv[z];e[0]+=L/2
            for p in (a,b,c):e[1]=min(e[1],p[0]);e[2]=max(e[2],p[0]);e[3]=min(e[3],p[1]);e[4]=max(e[4],p[1])
    return sorted(lv.items(),key=lambda x:-x[1][0])[:n]
for nm,p in (('wooden',['world','wmo','transports','transport_ship','transportship.wmo']),('riverboat',['world','wmo','kalimdor','lostisles','goblin_riverboat.wmo'])):
    print(nm)
    for z,e in decks(p):print('  z=%.2f area=%d x %.1f..%.1f y %.1f..%.1f'%(z,e[0],e[1],e[2],e[3],e[4]))
