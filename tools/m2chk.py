import sys,struct
sys.path.insert(0,'C:/CoA-Build/boats')
import wmo_geo as g
BS=chr(92)
for n in (['creature','goblin_riverboat_creature','goblin_riverboat_creature.m2'],['creature','rowboat_vehicle','darkshoreboat_vehicle.m2']):
    p=BS.join(n);d=g.getfile(p)
    if not d: print(p,'missing');continue
    print(p,len(d),d[:4],struct.unpack_from('<I',d,4)[0],'bbox',[round(v,1) for v in struct.unpack_from('<6f',d,0xA0)],'colTris',struct.unpack_from('<I',d,0xD8)[0])
