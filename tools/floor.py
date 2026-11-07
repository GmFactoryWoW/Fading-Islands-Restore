import struct,sys,collections
sys.path.insert(0,'C:/CoA-Build/boats')
import wmo_geo as g
BS=chr(92)
for n in (BS.join(['world','expansion01','doodads','coilfang','activedoodads','elevator','cf_elevatorplatform.m2']),BS.join(['world','expansiona01','doodads','eos','fadingisland','fading_island_valkyr_entrance_elevator_01.m2']),BS.join(['world','khazmodan','ironforge','passivedoodads','elevators','ironforgeelevator.m2'])):
    d=g.getfile(n)
    if d is None: print('NOFILE',n);continue
    nt,ot,nv,ov=struct.unpack_from('<IIII',d,0xD8)
    idx=struct.unpack_from('<%dH'%nt,d,ot);V=[struct.unpack_from('<3f',d,ov+i*12) for i in range(nv)]
    ar=collections.Counter()
    for i in range(0,nt,3):
        a,b,c=[V[j] for j in idx[i:i+3]]
        ux,uy,uz=b[0]-a[0],b[1]-a[1],b[2]-a[2];vx,vy,vz=c[0]-a[0],c[1]-a[1],c[2]-a[2]
        nz=ux*vy-uy*vx;area=abs(nz)/2
        if abs(nz)>0 and abs(nz)/ (((uy*vz-uz*vy)**2+(uz*vx-ux*vz)**2+nz**2)**.5) >0.9:
            ar[round(sum(p[2] for p in (a,b,c))/3,1)]+=area
    zs=[v[2] for v in V]
    print(n.split(BS)[-1],'collision verts',nv,'z range',round(min(zs),2),round(max(zs),2),'xy',round(min(v[0] for v in V),1),round(max(v[0] for v in V),1),round(min(v[1] for v in V),1),round(max(v[1] for v in V),1))
    print('  flat surfaces by z (area):',[(z,round(a)) for z,a in ar.most_common(6)])
