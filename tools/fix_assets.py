# post-process scaled ship: swap doodads whose textures/models are missing in this client, shrink the display bbox
import struct,sys
sys.path.insert(0,'C:/CoA-Build/boats')
p='C:/CoA-Build/boats/out/wmo/goblinshipfinal.wmo'
d=bytearray(open(p,'rb').read())
i=0
while i<len(d):
    t=bytes(d[i:i+4])[::-1];s=struct.unpack_from('<I',d,i+4)[0]
    if t==b'MODN':
        blob=bytes(d[i+8:i+8+s])
        for a,b in ((b'goblin_barricade_02.MDX',b'goblin_crate_05.MDX\0\0\0\0'),(b'goblin_keg_green_01',b'goblin_keg_brown_01'),(b'goblin_tent_03',b'goblin_tent_01'),(b'goblin_lamppost_02',b'goblin_lamppost_03'),(b'goblin_lamppost_04',b'goblin_lamppost_03'),(b'goblin_barricade_02',b'goblin_crate_05\0\0\0\0')):
            assert len(a)==len(b); blob=blob.replace(a,b); blob=blob.replace(a.upper(),b.upper())
        d[i+8:i+8+s]=blob
    i+=8+s
open(p,'wb').write(d)
g=bytearray(open('C:/CoA-Build/boats/wmo/godi_client.dbc','rb').read())
n,nf,rs,ss=struct.unpack_from('<4I',g,4)
for r in range(n):
    o=20+r*rs
    if struct.unpack_from('<I',g,o)[0]==1009923:
        for k in range(6): struct.pack_into('<f',g,o+48+k*4,struct.unpack_from('<f',g,o+48+k*4)[0]*0.95)
        print('GODI bbox',struct.unpack_from('<6f',g,o+48))
open('C:/CoA-Build/boats/out/GameObjectDisplayInfo.dbc','wb').write(g)

# --- collision + grate fixes (user: phasing through stairs, see-through grill on deck) ---
O='C:/CoA-Build/boats/out/wmo/'
# group 0: flag 0x04 = DETAIL (no collision). Walkable surfaces (upward faces) that were marked detail, incl. stair treads, become solid render faces (0x21)
import numpy as np
d=bytearray(open(O+'goblinshipfinal_000.wmo','rb').read());i=0
while i<len(d):
    t=bytes(d[i:i+4])[::-1];s_=struct.unpack_from('<I',d,i+4)[0]
    if t==b'MOGP':
        j=i+8+68;c={}
        while j<len(d):
            tg=bytes(d[j:j+4])[::-1];sz=struct.unpack_from('<I',d,j+4)[0];c[tg]=(j+8,sz);j+=8+sz
        vo,vs=c[b'MOVT'];V=np.frombuffer(bytes(d[vo:vo+vs]),'<f4').reshape(-1,3)
        io_,isz=c[b'MOVI'];I=np.frombuffer(bytes(d[io_:io_+isz]),'<u2').reshape(-1,3)
        po,ps=c[b'MOPY'];n=0
        for k in range(ps//2):
            o=po+k*2
            if d[o+1]!=255 and d[o]&0x04 and d[o]&0x20:
                A,B_,C=V[I[k][0]],V[I[k][1]],V[I[k][2]];nn=np.cross(B_-A,C-A);ln=np.linalg.norm(nn)
                if ln>1e-6 and abs(nn[2])/ln>0.5 and ln/2>0.01: d[o]&=~0x04;n+=1
        print('detail->solid triangles:',n)
        n2=0
        for k in range(ps//2):
            o=po+k*2
            if d[o+1]==255 or not d[o]&0x20 or d[o]&0x04: continue
            A,B_,C=V[I[k][0]],V[I[k][1]],V[I[k][2]];nn=np.cross(B_-A,C-A);ln=np.linalg.norm(nn)
            if ln<1e-9 or abs(nn[2])/ln>=0.45: continue
            ct=(A+B_+C)/3
            if 0.95<ct[2]<3.5 and ((-3.2<ct[0]<1.4 and -2.0<ct[1]<-0.3) or (-4.5<ct[0]<-0.5 and 1.5<ct[1]<4.6)): d[o]|=0x04;n2+=1
        print('stair rail tris made walk-through:',n2)
        # cabin doorways at x~-3.7 were only 0.6-0.8 yd wide after scaling (player is 0.78): open the jambs/collision proxy to 1.5 yd around each door
        n3=0
        for k in range(ps//2):
            o=po+k*2
            A,B_,C=V[I[k][0]],V[I[k][1]],V[I[k][2]];nn=np.cross(B_-A,C-A);ln=np.linalg.norm(nn)
            if ln<1e-9 or abs(nn[2])/ln>=0.6: continue
            ct=(A+B_+C)/3
            if -4.4<ct[0]<-3.2 and 3.2<ct[2]<4.9 and any(abs(ct[1]-c)<0.75 for c in (-0.17,-1.8)):
                if d[o+1]==255: d[o]=0
                elif d[o]&0x20 and not d[o]&0x04: d[o]|=0x04
                else: continue
                n3+=1
        print('door jamb tris opened:',n3)
        # stern cabin doors (main deck, x~11.2): the lintel wall above the doorway made the opening only ~1 yd tall -> open the lintel above both doors
        n4=0
        for k in range(ps//2):
            o=po+k*2
            A,B_,C=V[I[k][0]],V[I[k][1]],V[I[k][2]];nn=np.cross(B_-A,C-A);ln=np.linalg.norm(nn)
            if ln<1e-9 or abs(nn[2])/ln>=0.6: continue
            ct=(A+B_+C)/3
            if 10.7<ct[0]<11.6 and 1.45<ct[2]<2.45 and any(abs(ct[1]-c)<0.5 for c in (-3.87,1.53)):
                if d[o+1]==255: d[o]=0
                elif d[o]&0x20 and not d[o]&0x04: d[o]|=0x04
                else: continue
                n4+=1
        print('stern door lintel tris opened:',n4)
        break
    i+=8+s_
open(O+'goblinshipfinal_000.wmo','wb').write(d)
# root: grate/bars materials -> opaque wood
r=bytearray(open(O+'goblinshipfinal.wmo','rb').read());i=0;ch={}
while i<len(r):
    t=bytes(r[i:i+4])[::-1];s=struct.unpack_from('<I',r,i+4)[0];ch[t]=(i+8,s);i+=8+s
mo,ms=ch[b'MOMT'];wood=struct.unpack_from('<I',r,mo+2*64+12)[0]   # material 2 = woodtrim03
for m in (35,40):
    b=mo+m*64
    print('mat',m,'flags %x shader %d blend %d'%(struct.unpack_from('<III',r,b)),'-> wood')
    struct.pack_into('<II',r,b+4,0,0)                                # diffuse shader, opaque blend
    struct.pack_into('<I',r,b+12,wood)
open(O+'goblinshipfinal.wmo','wb').write(r)

# invisible solid covers over the three ladder hatches on the bow deck (ladders are M2 doodads without collision)
import inject
lids=[]
for (cx,cy) in ((-7.1,0.0),(-5.5,0.6),(-4.2,-2.4)):
    z=5.12;h=0.7   # 0.7: bigger lid caught the stair top at (-3.3,-3.4)
    a,b,c,e=(cx-h,cy-h,z),(cx+h,cy-h,z),(cx+h,cy+h,z),(cx-h,cy+h,z)
    lids+=[(a,b,c),(a,c,e)]
print('lids injected (tris, leaf refs):',inject.inject(O+'goblinshipfinal_000.wmo',lids))
# visible solid wooden covers over the two deck stairwells (down to the hold)
cov=[]
for (x0,x1,y0,y1) in ((-0.55,1.2,-5.0,-3.7),(-0.55,1.2,1.4,2.65)):
    z=0.98;a,b,c,e=(x0,y0,z),(x1,y0,z),(x1,y1,z),(x0,y1,z)
    cov+=[(a,b,c),(a,c,e)]
print('covers injected:',inject.inject(O+'goblinshipfinal_000.wmo',cov,vis_mat=2))
