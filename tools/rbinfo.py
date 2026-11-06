import sys,struct
sys.path.insert(0,'C:/CoA-Build/boats')
import wmo_geo as g
BS=chr(92)
base=BS.join(['world','wmo','kalimdor','lostisles','goblin_riverboat'])
r=g.getfile(base+'.wmo')
print('root',len(r),[ (t.decode(),s) for t,o,s in g.chunks(r)])
d=g.getfile(base+'_000.wmo')
for t,o,s in g.chunks(d):
    print('grp',t.decode(),s)
    if t==b'MOGP':
        print(' sub',[(tt.decode(),ss) for tt,oo,ss in g.chunks(d,o+68)])
