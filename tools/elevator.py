# find the user's Ironforge elevator doodad in the Noggit project -> elevator.json (world coords, yaw, scale)
import struct,glob,os,json
P='C:/Users/ilusi/OneDrive/Documents/custom map Fading Island/world/maps/azzararchipelago/'
out=None
for f in sorted(glob.glob(P+'*.adt')):
    d=open(f,'rb').read();i=0;ch={}
    while i<len(d):
        t=d[i:i+4][::-1];s=struct.unpack_from('<I',d,i+4)[0]
        if t in(b'MMDX',b'MMID',b'MDDF'):ch[t]=(i+8,s)
        i+=8+s
    if b'MDDF' not in ch:continue
    o,s=ch[b'MMDX'];nm=d[o:o+s];oo,ss=ch[b'MMID'];offs=struct.unpack_from('<%dI'%(ss//4),d,oo)
    names=[nm[x:nm.index(b'\0',x)].decode().lower() for x in offs]
    o,s=ch[b'MDDF']
    for k in range(s//36):
        nid,uid=struct.unpack_from('<II',d,o+k*36)
        if names[nid].endswith('ironforgeelevator.m2'):
            pos=struct.unpack_from('<3f',d,o+k*36+8);rot=struct.unpack_from('<3f',d,o+k*36+20);sc=struct.unpack_from('<H',d,o+k*36+32)[0]
            out={'x':17066.6666-pos[2],'y':17066.6666-pos[0],'z':pos[1],'rotY':rot[1],'scale':sc/1024.0,'tile':os.path.basename(f).split('azzararchipelago_')[1][:-4],'uid':uid}
if out:
    json.dump(out,open('C:/CoA-Build/boats/elevator.json','w'));print(out)
else:print('no elevator in project')
