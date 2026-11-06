"""Rotate goblin_riverboat.wmo by -90 deg about the vertical axis: (x,y)->(y,-x). Bow moves from -Y to -X (the direction the core sails a transport)."""
import sys,struct,math,os
sys.path.insert(0,'C:/CoA-Build/boats')
import wmo_geo as g
BS=chr(92)
base=BS.join(['world','wmo','kalimdor','lostisles','goblin_riverboat'])
OUT='C:/CoA-Build/boats/out/wmo/'
os.makedirs(OUT,exist_ok=True)
rot=lambda x,y:(y,-x)
def qmul(a,b):
    ax,ay,az,aw=a;bx,by,bz,bw=b
    return (aw*bx+ax*bw+ay*bz-az*by,aw*by-ax*bz+ay*bw+az*bx,aw*bz+ax*by-ay*bx+az*bw,aw*bw-ax*bx-ay*by-az*bz)
QR=(0,0,math.sin(-math.pi/4),math.cos(-math.pi/4))
# group
d=bytearray(g.getfile(base+'_000.wmo'))
for t,o,s in g.chunks(bytes(d)):
    if t!=b'MOGP':continue
    sub={tt:(oo,ss) for tt,oo,ss in g.chunks(bytes(d),o+68)}
    for name in (b'MOVT',b'MONR'):
        vo,vs=sub[name]
        for i in range(vs//12):
            x,y,z=struct.unpack_from('<3f',d,vo+i*12);nx,ny=rot(x,y);struct.pack_into('<3f',d,vo+i*12,nx,ny,z)
    vo,vs=sub[b'MOVT'];vt=[struct.unpack_from('<3f',d,vo+i*12) for i in range(vs//12)]
    mn=[min(v[k] for v in vt) for k in range(3)];mx=[max(v[k] for v in vt) for k in range(3)]
    struct.pack_into('<6f',d,o+12,*mn,*mx)
    bo,bs=sub[b'MOBN'];axes={}
    for i in range(bs//16):
        off=bo+i*16;fl,neg,pos,nf,fs,pd=struct.unpack_from('<HhhHIf',d,off)
        if not fl&4:
            ax=fl&3;axes[ax]=axes.get(ax,0)+1
            if ax==0: fl=(fl&~3)|1;neg,pos=pos,neg;pd=-pd
            elif ax==1: fl=(fl&~3)|0
            struct.pack_into('<HhhHIf',d,off,fl,neg,pos,nf,fs,pd)
    print('bsp axes',axes)
open(OUT+'goblin_riverboat_000.wmo','wb').write(bytes(d))
# root
r=bytearray(g.getfile(base+'.wmo'))
for t,o,s in g.chunks(bytes(r)):
    if t==b'MOHD':
        a=struct.unpack_from('<6f',r,o+36);struct.pack_into('<6f',r,o+36,a[1],-a[3],a[2],a[4],-a[0],a[5]);
        # min=(y_min,-x_max,z_min) max=(y_max,-x_min,z_max)
        mn=(a[1],-a[3],a[2]);mx=(a[4],-a[0],a[5]);struct.pack_into('<6f',r,o+36,*mn,*mx)
    if t==b'MODD':
        for i in range(s//40):
            off=o+i*40;x,y,z=struct.unpack_from('<3f',r,off+4);q=struct.unpack_from('<4f',r,off+16)
            nx,ny=rot(x,y);struct.pack_into('<3f',r,off+4,nx,ny,z);struct.pack_into('<4f',r,off+16,*qmul(QR,q))
    if t==b'MFOG':
        for i in range(s//48):
            off=o+i*48;x,y,z=struct.unpack_from('<3f',r,off+4);nx,ny=rot(x,y);struct.pack_into('<3f',r,off+4,nx,ny,z)
open(OUT+'goblin_riverboat.wmo','wb').write(bytes(r))
print('written',os.listdir(OUT))
