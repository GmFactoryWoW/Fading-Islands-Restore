"""scale_up: scale the already scaled+fixed out/wmo/goblinshipfinal*.wmo again by S (final ship scale = 0.45*S)."""
import sys,struct,os
sys.path.insert(0,'C:/CoA-Build/boats')
import wmo_geo as g
S=float(sys.argv[1]) if len(sys.argv)>1 else 0.95/0.45   # extra factor applied to the already scaled+fixed files in out/wmo
BS=chr(92);base=BS.join(['world','wmo','kalimdor','lostisles','goblinshipfinal'])
OUT='C:/CoA-Build/boats/out/wmo/';os.makedirs(OUT,exist_ok=True)
def sc(d,off,n):
    for i in range(n):
        v=struct.unpack_from('<f',d,off+i*4)[0];struct.pack_into('<f',d,off+i*4,v*S)
for gi in range(4):
    d=bytearray(open(OUT+'goblinshipfinal_%03d.wmo'%gi,'rb').read())
    for t,o,s in g.chunks(bytes(d)):
        if t!=b'MOGP':continue
        sc(d,o+12,6)
        sub={tt:(oo,ss) for tt,oo,ss in g.chunks(bytes(d),o+68)}
        vo,vs=sub[b'MOVT'];sc(d,vo,vs//4)
        bo,bs=sub[b'MOBN']
        for i in range(bs//16):
            fl=struct.unpack_from('<H',d,bo+i*16)[0]
            if not fl&4:sc(d,bo+i*16+12,1)
        ao,as_=sub[b'MOBA']
        for i in range(as_//24):
            bb=struct.unpack_from('<6h',d,ao+i*24);struct.pack_into('<6h',d,ao+i*24,*[int(round(x*S)) for x in bb])
    open(OUT+'goblinshipfinal_%03d.wmo'%gi,'wb').write(bytes(d))
r=bytearray(open(OUT+'goblinshipfinal.wmo','rb').read())
for t,o,s in g.chunks(bytes(r)):
    if t==b'MOHD':sc(r,o+36,6)
    elif t==b'MOPV':sc(r,o,s//4)
    elif t==b'MOPT':
        for i in range(s//20):sc(r,o+i*20+16,1)
    elif t==b'MODD':
        for i in range(s//40):sc(r,o+i*40+4,3);sc(r,o+i*40+32,1)
    elif t==b'MFOG':
        for i in range(s//48):sc(r,o+i*48+4,3);sc(r,o+i*48+16,3)
open(OUT+'goblinshipfinal.wmo','wb').write(bytes(r))
print('scaled up x',S,sorted(os.listdir(OUT)))
