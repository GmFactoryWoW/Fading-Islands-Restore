import sys,struct,math,collections
sys.path.insert(0,'C:/CoA-Build/boats')
import wmo_geo as g
BS=chr(92)
K=17066.666
def adt(map_,bx,by):
    for nm in ('%s_%d_%d.adt'%(map_,bx,by),):
        d=g.getfile(BS.join(['World','Maps',map_,nm]))
        if d:return d
def wmos(d):
    i=0;ch={}
    while i<len(d):
        tg=d[i:i+4][::-1];s=struct.unpack_from('<I',d,i+4)[0];ch[tg]=(i+8,s);i+=8+s
    o,s=ch[b'MWID'];ids=struct.unpack_from('<%dI'%(s//4),d,o);mo,ms=ch[b'MWMO']
    names=[d[mo+x:d.index(b'\0',mo+x)].decode() for x in ids]
    o,s=ch[b'MODF'];out=[]
    for k in range(s//64):
        nid,uid,px,py,pz,rx,ry,rz,*bb=struct.unpack_from('<II3f3f6f',d,o+k*64)
        out.append((names[nid],K-pz,K-px,py,(rx,ry,rz),bb))
    return out
def analyse(map_,stop,prev,nxt,label):
    sx,sy=stop;tx,ty=nxt[0]-prev[0],nxt[1]-prev[1];L=math.hypot(tx,ty);tx/=L;ty/=L   # path tangent
    lx,ly=-ty,tx                                                                  # left of travel
    bx=int(32-sy/533.33333);by=int(32-sx/533.33333)
    print(label,'tile',bx,by,'tangent heading %.0f'%math.degrees(math.atan2(ty,tx)))
    pts=[]
    for dbx in (bx-1,bx,bx+1):
        for dby in (by-1,by,by+1):
            d=adt(map_,dbx,dby)
            if not d:continue
            for n,x,y,z,r,bb in wmos(d):
                if math.hypot(x-sx,y-sy)>90:continue
                tris=g.load(n)
                if not tris:continue
                ps=math.radians(-(r[1]+90));c,s=math.cos(ps),math.sin(ps);pxf,pyf,pzf=K-y,z,K-x
                for t in tris:
                    P=[]
                    for v in t:
                        Xf=pxf+c*v[0]-s*v[1];Zf=pzf+s*v[0]+c*v[1];P.append((K-Zf,K-Xf,pyf+v[2]))
                    u=[P[1][i]-P[0][i] for i in range(3)];w=[P[2][i]-P[0][i] for i in range(3)]
                    nz=u[0]*w[1]-u[1]*w[0];nx=u[1]*w[2]-u[2]*w[1];ny=u[2]*w[0]-u[0]*w[2];Ln=(nx*nx+ny*ny+nz*nz)**.5
                    if Ln<1e-6 or abs(nz)/Ln<0.9:continue
                    cx=sum(p[0] for p in P)/3;cy=sum(p[1] for p in P)/3;cz=sum(p[2] for p in P)/3
                    if not -1<cz<14:continue
                    dx,dy=cx-sx,cy-sy;along=dx*tx+dy*ty;lat=dx*lx+dy*ly
                    if abs(along)<14 and abs(lat)<40: pts.append((lat,along,cz,n.split(BS)[-1]))
    print(' deck points',len(pts))
    byz=collections.Counter((round(p[2]*2)/2, 'L' if p[0]>0 else 'R') for p in pts)
    print(' z histogram',sorted(byz.items(),key=lambda x:-x[1])[:8])
    for side,sg in (('left',1),('right',-1)):
        q=sorted([p for p in pts if p[0]*sg>0],key=lambda p:abs(p[0]))[:5]
        print(' nearest deck on',side,[(round(a,1),round(b,1),round(c,1),n[:22]) for a,b,c,n in q])
# Ratchet (map 1): stop node 6 (-1005.6,-3841.6), prev 5 (-1058.5,-3818.9), next 7 (-956.4,-3877.1)
analyse('Kalimdor',(-1005.6,-3841.6),(-1058.5,-3818.9),(-956.4,-3877.1),'RATCHET')
# Booty Bay (map 0): stop node 16 (-14277.8,582.9) prev 15 (-14342.5,635.4) next 17 (-14171.9,578.4)
analyse('Azeroth',(-14277.8,582.9),(-14342.5,635.4),(-14171.9,578.4),'BOOTY BAY')
