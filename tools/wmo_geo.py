import sys,struct,glob,os,math,itertools
sys.path[:0]=['C:/CoA-Build/eunoia','C:/CoA-Build/boats']
import storm
BS=chr(92)
_mp=None
def mpqs():
    global _mp
    if _mp is None: _mp=[storm.open_mpq(p) for p in sorted(glob.glob('C:/Ascension Local/Data/*.[Mm][Pp][Qq]'),reverse=True) if 'ZZZZZA' not in p]
    return _mp
_cache={}
def getfile(name):
    k=name.lower()
    if k in _cache: return _cache[k]
    for h in mpqs():
        if storm.S.SFileHasFile(h,name.encode()):
            tmp='C:/CoA-Build/boats/wmo/_t.bin'; storm.extract(h,name,tmp); d=open(tmp,'rb').read(); _cache[k]=d; return d
    _cache[k]=None; return None
def chunks(d,start=0):
    i=start
    while i<len(d):
        t=d[i:i+4][::-1];s=struct.unpack_from('<I',d,i+4)[0]
        yield t,i+8,s
        i+=8+s
def load(wmo):
    r=getfile(wmo)
    if not r: return None
    ng=0
    for t,o,s in chunks(r):
        if t==b'MOHD': ng=struct.unpack_from('<I',r,o+4)[0]
    tris=[]
    base=wmo[:-4]
    for g in range(ng):
        d=getfile(base+'_%03d.wmo'%g)
        if not d: continue
        for t,o,s in chunks(d):
            if t!=b'MOGP':continue
            sub={tt:(oo,ss) for tt,oo,ss in chunks(d,o+68)}
            vo,vs=sub[b'MOVT'];vt=[struct.unpack_from('<3f',d,vo+i*12) for i in range(vs//12)]
            io,isz=sub[b'MOVI'];idx=struct.unpack_from('<%dH'%(isz//2),d,io)
            for k in range(len(idx)//3): tris.append(tuple(vt[x] for x in idx[k*3:k*3+3]))
    return tris
