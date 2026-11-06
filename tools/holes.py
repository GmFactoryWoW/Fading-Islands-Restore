import struct,numpy as np
tris=[]
for gi in range(4):
    d=open('out/wmo/goblinshipfinal_%03d.wmo'%gi,'rb').read()
    i=0
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
    for k,(a,b,c) in enumerate(I):
        if P[k][1]==0xFF: continue
        tris.append((V[a],V[b],V[c]))
def raster(z0,z1,res=0.25,X=(-14,16),Y=(-8,6)):
    xs=np.arange(X[0],X[1],res);ys=np.arange(Y[0],Y[1],res)
    G=np.zeros((len(ys),len(xs)),bool)
    for A,B,C in tris:
        n=np.cross(B-A,C-A);ln=np.linalg.norm(n)
        if ln<1e-9 or abs(n[2])/ln<0.7:continue
        zc=(A[2]+B[2]+C[2])/3
        if not z0<=zc<=z1:continue
        x0=max(int((min(A[0],B[0],C[0])-X[0])/res),0);x1=min(int((max(A[0],B[0],C[0])-X[0])/res)+1,len(xs))
        y0=max(int((min(A[1],B[1],C[1])-Y[0])/res),0);y1=min(int((max(A[1],B[1],C[1])-Y[0])/res)+1,len(ys))
        if x0>=x1 or y0>=y1:continue
        gx,gy=np.meshgrid(xs[x0:x1],ys[y0:y1])
        d=(B[1]-C[1])*(A[0]-C[0])+(C[0]-B[0])*(A[1]-C[1])
        if abs(d)<1e-12:continue
        l1=((B[1]-C[1])*(gx-C[0])+(C[0]-B[0])*(gy-C[1]))/d
        l2=((C[1]-A[1])*(gx-C[0])+(A[0]-C[0])*(gy-C[1]))/d
        G[y0:y1,x0:x1]|=(l1>=-1e-6)&(l2>=-1e-6)&(1-l1-l2>=-1e-6)
    return xs,ys,G
if __name__=='__main__':
    for nm,(a,b) in (('main deck',(0.2,1.5)),('hold',(-2.5,-0.2))):
        xs,ys,G=raster(a,b);print(nm,'x from',xs[0],'step .5')
        for yi in range(len(ys)-1,-1,-2):print('%5.1f '%ys[yi]+''.join('#' if G[yi,xi] else '.' for xi in range(0,len(xs),2)))
