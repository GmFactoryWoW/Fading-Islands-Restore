import sys,math,struct,io,contextlib
sys.path.insert(0,'C:/CoA-Build/boats')
with contextlib.redirect_stdout(io.StringIO()):
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
        out.append((names[nid],K-pz,K-px,py,ry))
    return out
sx,sy=-14277.8,582.9;tx,ty=math.cos(math.radians(-18)),math.sin(math.radians(-18));lx,ly=-ty,tx
rows=[]
for bx,by in ((30,58),(30,57),(29,58),(31,58)):
    d=H.adt('Azeroth',bx,by)
    if not d:continue
    for n,x,y,z,ry in doodads(d):
        dx,dy=x-sx,y-sy;al=dx*tx+dy*ty;la=dx*lx+dy*ly
        if abs(al)<60 and abs(la)<60:rows.append((round(la),round(al),round(z,1),n.split(H.BS)[-1][:34]))
rows.sort()
print(len(rows));
for r in rows:
    if any(k in r[3].lower() for k in ('ramp','plank','gang','stair','dock','pier','bay','boat','ship','wood')):print(r)
