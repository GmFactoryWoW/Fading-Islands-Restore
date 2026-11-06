import sys,struct
sys.path.insert(0,'C:/CoA-Build/boats')
import wmo_geo as g
BS=chr(92)
for n in (['World','Generic','Human','Passive Doodads','WoodenStairs','WoodenStairs02.m2'],['World','Generic','PassiveDoodads','Ships','ShipRamps','shipramp_horde_01.m2'],['World','Generic','PassiveDoodads','Ships','ShipRamps','shipramp_alliance_01.m2'],['world','generic','passivedoodads','ships','shipramps','shipramp01.m2'],['World','Generic','Goblin','PassiveDoodads','LaunchRamp','goblin_horde_launchramp_02.m2']):
    p=BS.join(n);d=g.getfile(p)
    if not d: print('missing',p);continue
    print(n[-1],len(d),'bbox',[round(v,1) for v in struct.unpack_from('<6f',d,0xA0)],'colTris',struct.unpack_from('<I',d,0xD8)[0])
t=g.load(BS.join(['world','wmo','azeroth','buildings','stranglethorn_bootybay','bootybayplank.wmo']))
if t:
    vs=[v for x in t for v in x];print('bootybayplank',len(t),[(round(min(v[i] for v in vs),1),round(max(v[i] for v in vs),1)) for i in range(3)])
else:print('bootybayplank missing')
