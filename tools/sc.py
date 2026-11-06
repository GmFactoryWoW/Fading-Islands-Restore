import struct,numpy as np
d=open('out/wmo/goblinshipfinal_000.wmo','rb').read();i=0
while i<len(d):
    tg=d[i:i+4][::-1];s=struct.unpack_from('<I',d,i+4)[0]
    if tg==b'MOGP': base=i+8+68;break
    i+=8+s
ch={};j=base
while j<len(d):
    tg=d[j:j+4][::-1];s=struct.unpack_from('<I',d,j+4)[0];ch[tg]=(j+8,s);j+=8+s
vo,vs=ch[b'MOVT'];V=np.frombuffer(d[vo:vo+vs],'<f4').reshape(-1,3).astype(float)
io_,isz=ch[b'MOVI'];I=np.frombuffer(d[io_:io_+isz],'<u2').reshape(-1,3)
po,ps=ch[b'MOPY'];P=np.frombuffer(d[po:po+ps],'u1').reshape(-1,2)
col=[];wall=[]
for k,(a,b,c) in enumerate(I):
    f,m=P[k]
    if (f&0x08) or ((f&0x20) and not f&0x04): col.append((V[a],V[b],V[c],m,f))
def hits(x,y,lo=-0.5,hi=7):
    out=[]
    for A,B,C,m,f in col:
        d_=(B[1]-C[1])*(A[0]-C[0])+(C[0]-B[0])*(A[1]-C[1])
        if abs(d_)<1e-9:continue
        l1=((B[1]-C[1])*(x-C[0])+(C[0]-B[0])*(y-C[1]))/d_;l2=((C[1]-A[1])*(x-C[0])+(A[0]-C[0])*(y-C[1]))/d_
        if l1>=0 and l2>=0 and l1+l2<=1:out.append(round(l1*A[2]+l2*B[2]+(1-l1-l2)*C[2],1))
    return sorted(set(z for z in out if lo<z<hi))
