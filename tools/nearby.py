import json,math
A=json.load(open('allm.json'));E=json.load(open('elevscan.json'))
for e in E:
    print('==',e['model'].split(chr(92))[-1],round(e['x'],1),round(e['y'],1),round(e['z'],1))
    near=[(math.hypot(a['x']-e['x'],a['y']-e['y']),a) for a in A if a is not e and math.hypot(a['x']-e['x'],a['y']-e['y'])<40]
    for dd,a in sorted(near,key=lambda t:-t[1]['z'])[:12]:
        print('  d%5.1f z%7.1f %s'%(dd,a['z'],a['model'].split(chr(92))[-1]))
