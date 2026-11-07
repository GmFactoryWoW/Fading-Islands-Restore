import struct,glob,os,json,re
P='C:/Users/ilusi/OneDrive/Documents/custom map Fading Island/world/maps/azzararchipelago/'
want=('ironforgeelevator.m2','cf_elevatorplatform.m2','fading_island_valkyr_entrance_elevator_01.m2')
out=[];allm=[]
for f in sorted(glob.glob(P+'*.adt')):
    d=open(f,'rb').read();i=0;ch={}
    while i<len(d):
        t=d[i:i+4][::-1];s=struct.unpack_from('<I',d,i+4)[0]
        if t in(b'MMDX',b'MMID',b'MDDF',b'MWMO',b'MWID',b'MODF'):ch[t]=(i+8,s)
        i+=8+s
    if b'MDDF' not in ch:continue
    o,s=ch[b'MMDX'];nm=d[o:o+s];oo,ss=ch[b'MMID'];offs=struct.unpack_from('<%dI'%(ss//4),d,oo)
    names=[re.sub(r'\.(mdx|mdl)$','.m2',nm[x:nm.index(b'\0',x)].decode().lower()) for x in offs]
    o,s=ch[b'MDDF']
    for k in range(s//36):
        nid,uid=struct.unpack_from('<II',d,o+k*36)
        pos=struct.unpack_from('<3f',d,o+k*36+8);rot=struct.unpack_from('<3f',d,o+k*36+20);sc=struct.unpack_from('<H',d,o+k*36+32)[0]
        e={'model':names[nid],'x':17066.6666-pos[2],'y':17066.6666-pos[0],'z':pos[1],'rot':rot,'scale':sc/1024.0,'tile':os.path.basename(f).split('azzararchipelago_')[1][:-4],'uid':uid}
        allm.append(e)
        if names[nid].endswith(want):out.append(e)
for e in out:print(e)
json.dump(out,open('elevscan.json','w'));json.dump(allm,open('allm.json','w'))
