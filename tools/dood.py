import struct,sys
d=open('out/wmo/goblinshipfinal.wmo','rb').read()
i=0;ch={}
while i<len(d):
    t=d[i:i+4][::-1];s=struct.unpack_from('<I',d,i+4)[0];ch[t]=(i+8,s);i+=8+s
o,s=ch[b'MODN'];names=d[o:o+s]
o,s=ch[b'MODD']
for k in range(s//40):
    no,*r=struct.unpack_from('<I3f4ff',d,o+k*40)[0:1]+struct.unpack_from('<3f',d,o+k*40+4),
    n=names[no&0xffffff:names.index(b'\0',no&0xffffff)].decode()
    sc=struct.unpack_from('<f',d,o+k*40+36)[0]
    print(k,n.split(chr(92))[-1],[round(x,1) for x in r[0]],round(sc,2))
o,s=ch[b'MOTX'];print(d[o:o+s].replace(b'\0',b'|').decode(errors='replace')[:1500])
