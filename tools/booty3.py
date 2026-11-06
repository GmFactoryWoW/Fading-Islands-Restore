import sys,math,struct
sys.path.insert(0,'C:/CoA-Build/boats')
import homedock as H
K=H.K
def doodads(d):
    i=0;ch={}
    while i<len(d):
        tg=d[i:i+4][::-1];s=struct.unpack_from('<I',d,i+4)[0];ch[tg]=(i+8,s);i+=8+s
    xo,xs=ch[b'MMID'];mid=struct.unpack_from('<%dI'%(xs//4),d,xo);mx,ms=ch[b'MMDX']
    names=[d[mx+x:d.index(b'\0',mx+x)].decode() for x in mid]
    o,s=ch[b'MDDF'];out=[]
    for k in range(s//36):
        nid,uid,px,py,pz,rx,ry,rz,sc,fl=struct.unpack_from('<II3f3fHH',d,o+k*36)
        out.append((names[nid],K-pz,K-px,py))
    return out
def scan(map_,stop,prev,nxt,tiles,label):
    sx,sy=stop;tx,ty=nxt[0]-prev[0],nxt[1]-prev[1];L=math.hypot(tx,ty);tx/=L;ty/=L;lx,ly=-ty,tx
    print(label)
    rows=[]
    for bx,by in tiles:
        d=H.adt(map_,bx,by)
        if not d:continue
        for n,x,y,z in doodads(d):
            dx,dy=x-sx,y-sy;al=dx*tx+dy*ty;la=dx*lx+dy*ly
            if abs(al)<45 and abs(la)<45 and any(k in n.upper() for k in ('DOCK','PIER','PLANK','BOOTYBAY','WHARF','PILING','POST')):
                rows.append((round(la,1),round(al,1),round(z,1),n.split(H.BS)[-1][:30]))
    rows.sort();[print(r) for r in rows[:40]];print(len(rows))
scan('Azeroth',(-14277.8,582.9),(-14342.5,635.4),(-14171.9,578.4),[(30,58),(30,57),(29,58),(31,58)],'BOOTY')
scan('Kalimdor',(-1005.6,-3841.6),(-1058.5,-3818.9),(-956.4,-3877.1),[(39,33),(39,34),(38,33)],'RATCHET')
