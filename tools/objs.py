import sys,struct,math
sys.path.insert(0,'C:/CoA-Build/boats')
import terrain as t
K=17066.666
BS=chr(92)
def objs(bx,by):
    d=t.tile(bx,by);i=0;ch={}
    while i<len(d):
        tg=d[i:i+4][::-1];s=struct.unpack_from('<I',d,i+4)[0];ch[tg]=(i+8,s);i+=8+s
    o,s=ch[b'MWID'];ids=struct.unpack_from('<%dI'%(s//4),d,o)
    mo,ms=ch[b'MWMO']
    names=[d[mo+x:d.index(b'\0',mo+x)].decode() for x in ids]
    o,s=ch[b'MODF'];out=[]
    for k in range(s//64):
        nid,uid,px,py,pz,rx,ry,rz,*bb=struct.unpack_from('<II3f3f6f',d,o+k*64)
        out.append((names[nid],K-pz,K-px,py,(rx,ry,rz),bb))
    xo,xs=ch[b'MMID'];mid=struct.unpack_from('<%dI'%(xs//4),d,xo);mx,msz=ch[b'MMDX']
    mnames=[d[mx+x:d.index(b'\0',mx+x)].decode() for x in mid]
    o,s=ch[b'MDDF'];dd=[]
    for k in range(s//36):
        nid,uid,px,py,pz,rx,ry,rz,sc,fl=struct.unpack_from('<II3f3fHH',d,o+k*36)
        dd.append((mnames[nid],K-pz,K-px,py,(rx,ry,rz),sc/1024))
    return out,dd
if __name__=='__main__':
    w,dd=objs(38,30)
    print('WMO',len(w),'M2',len(dd))
    for n,x,y,z,r,bb in w:
        if math.hypot(x-893.87,y+3620.84)<400: print('WMO',n,round(x,1),round(y,1),round(z,1),[round(v,1) for v in r])
    for n,x,y,z,r,sc in dd:
        if math.hypot(x-893.87,y+3620.84)<120: print('M2',n.split(BS)[-1],round(x,1),round(y,1),round(z,1),round(r[1],1),sc)
