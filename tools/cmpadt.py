import struct,glob,os,sys,collections
def parse(path):
    d=open(path,'rb').read();i=0;ch={}
    while i<len(d):
        t=d[i:i+4][::-1];s=struct.unpack_from('<I',d,i+4)[0]
        ch.setdefault(t,[]).append((i+8,s));i+=8+s
    out={'mddf':set(),'modf':set()}
    if b'MMDX' in ch and b'MDDF' in ch:
        o,s=ch[b'MMDX'][0];nm=d[o:o+s];oo,ss=ch[b'MMID'][0];offs=struct.unpack_from('<%dI'%(ss//4),d,oo)
        names=[nm[x:nm.index(b'\0',x)].decode().lower() for x in offs]
        o,s=ch[b'MDDF'][0]
        for k in range(s//36):
            nid,uid=struct.unpack_from('<II',d,o+k*36);p=struct.unpack_from('<3f',d,o+k*36+8)
            out['mddf'].add((names[nid],tuple(round(x,1) for x in p)))
    if b'MWMO' in ch and b'MODF' in ch:
        o,s=ch[b'MWMO'][0];nm=d[o:o+s];oo,ss=ch[b'MWID'][0];offs=struct.unpack_from('<%dI'%(ss//4),d,oo)
        names=[nm[x:nm.index(b'\0',x)].decode().lower() for x in offs]
        o,s=ch[b'MODF'][0]
        for k in range(s//64):
            nid,uid=struct.unpack_from('<II',d,o+k*64);p=struct.unpack_from('<3f',d,o+k*64+8)
            out['modf'].add((names[nid],tuple(round(x,1) for x in p)))
    return out,d
P='C:/Users/ilusi/OneDrive/Documents/custom map Fading Island/world/maps/azzararchipelago/'
O='C:/CoA-Build/boats/map907/AzzarArchipelago_'
for f in sorted(glob.glob(P+'*.adt')):
    t=f.split('azzararchipelago_')[1]
    of=O+t
    if not os.path.exists(of):print(t,'NEW tile');continue
    a,da=parse(of);b,db=parse(f)
    rm=len(a['mddf']-b['mddf']);ad=len(b['mddf']-a['mddf']);wr=len(a['modf']-b['modf']);wa=len(b['modf']-a['modf'])
    print(t,len(da),len(db),'doodads -%d +%d  wmo -%d +%d'%(rm,ad,wr,wa))
