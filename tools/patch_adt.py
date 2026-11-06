# hide retail-only doodads/WMOs (missing in this client = giant checker cubes) in Hardluck's ADTs; same-size edits
import struct,glob,os,sys
sys.path.insert(0,'C:/CoA-Build/boats')
import wmo_geo as g
BS=chr(92);os.makedirs('out/adt',exist_ok=True);res={}
nm_ok={}
def has(n):
    k=n.lower().replace('.mdx','.m2')
    if k not in nm_ok: nm_ok[k]=bool(g.getfile(k))
    return nm_ok[k]
tm=tw=0
for f in sorted(glob.glob('map907/*.adt')):
    base=os.path.basename(f);mp=BS.join(['World','Maps','AzzarArchipelago',base])
    PRJ=r'C:/Users/ilusi/OneDrive/Documents/custom map Fading Island/world/maps/azzararchipelago/'+base.lower()   # user's Noggit edits (pier tile only has real changes)
    d=bytearray(open(PRJ,'rb').read() if base in ('AzzarArchipelago_38_30.adt',) and os.path.exists(PRJ) else (g.getfile(mp) or open(f,'rb').read()));i=0;ch={}
    while i<len(d):
        t=bytes(d[i:i+4])[::-1];s=struct.unpack_from('<I',d,i+4)[0]
        if t in(b'MMDX',b'MMID',b'MDDF',b'MWMO',b'MWID',b'MODF'):ch[t]=(i+8,s)
        i+=8+s
    ch_=0
    if b'MDDF' in ch and b'MMDX' in ch:
        o,s=ch[b'MMDX'];nm=bytes(d[o:o+s]);oo,ss=ch[b'MMID'];offs=struct.unpack_from('<%dI'%(ss//4),d,oo)
        names=[nm[x:nm.index(b'\0',x)].decode() for x in offs]
        o,s=ch[b'MDDF']
        for k in range(s//36):
            if not has(names[struct.unpack_from('<I',d,o+k*36)[0]]): struct.pack_into('<H',d,o+k*36+32,1);tm+=1;ch_+=1
    if b'MODF' in ch and b'MWMO' in ch:
        o,s=ch[b'MWMO'];nm=bytes(d[o:o+s]);oo,ss=ch[b'MWID'];offs=struct.unpack_from('<%dI'%(ss//4),d,oo)
        names=[nm[x:nm.index(b'\0',x)].decode() for x in offs]
        o,s=ch[b'MODF']
        for k in range(s//64):
            n=names[struct.unpack_from('<I',d,o+k*64)[0]]
            if not has(n):
                print('missing WMO',n,base); struct.pack_into('<3f',d,o+k*64+8,0,-30000,0); tw+=1; ch_+=1   # park far below the map
    if ch_: open('out/adt/'+base,'wb').write(d);res[base]=ch_
print('adts patched',len(res),'doodads hidden',tm,'wmos moved',tw)
