# copy the user's Noggit-saved tiles (only those whose objects differ from the original) into out/adt for pack.py
import os,re,glob,shutil,sys
exec(open('C:/CoA-Build/boats/cmpadt.py').read().split("P='C:/Users")[0])
P='C:/Users/ilusi/OneDrive/Documents/custom map Fading Island/world/maps/azzararchipelago/'
O='C:/CoA-Build/boats/map907/AzzarArchipelago_'
def norm(s):return {(re.sub(r'\.(mdx|mdl)$','.m2',n),p) for n,p in s}
shutil.rmtree('C:/CoA-Build/boats/out/adt',ignore_errors=True);os.makedirs('C:/CoA-Build/boats/out/adt')
n=0
for f in sorted(glob.glob(P+'azzararchipelago_*.adt')):
    t=os.path.basename(f).split('azzararchipelago_')[1][:-4];of=O+t+'.adt'
    if os.path.exists(of):
        a,_=parse(of);b,_=parse(f)
        if norm(a['mddf'])==norm(b['mddf']) and norm(a['modf'])==norm(b['modf']):continue
    shutil.copy(f,'C:/CoA-Build/boats/out/adt/AzzarArchipelago_'+t+'.adt');n+=1;print('map tile',t)
print('tiles taken from your Noggit project:',n)

# the elevator doodad is replaced by the moving server transport: shrink the static copy to nothing
import json,struct
if os.path.exists('C:/CoA-Build/boats/elevator.json'):
    el=json.load(open('C:/CoA-Build/boats/elevator.json'));fn='C:/CoA-Build/boats/out/adt/AzzarArchipelago_%s.adt'%el['tile']
    if os.path.exists(fn):
        d=bytearray(open(fn,'rb').read());i=0
        while i<len(d):
            t=bytes(d[i:i+4])[::-1];sz=struct.unpack_from('<I',d,i+4)[0]
            if t==b'MDDF':
                for k in range(sz//36):
                    if struct.unpack_from('<I',d,i+8+k*36+4)[0]==el['uid']:struct.pack_into('<H',d,i+8+k*36+32,1);print('static elevator doodad hidden in tile',el['tile'])
            i+=8+sz
        open(fn,'wb').write(d)
