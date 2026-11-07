import json,math,sys
import terrain as t
t.D='C:/Users/ilusi/OneDrive/Documents/custom map Fading Island/world/maps/azzararchipelago/'
E=json.load(open('elevscan.json'))
for e in E:
    bx,by=map(int,e['tile'].split('_'))
    pts=t.grid([bx-1,bx,bx+1],[by-1,by,by+1])
    print('==',e['model'].split(chr(92))[-1],round(e['x'],1),round(e['y'],1),round(e['z'],1),len(pts))
    def h(x,y):
        k=min(pts,key=lambda p:(p[0]-x)**2+(p[1]-y)**2);return pts[k][0]
    for R in (0,10,20,30,45,60,80):
        print(' R%3d'%R,[round(h(e['x']+R*math.cos(a*math.pi/4),e['y']+R*math.sin(a*math.pi/4))) for a in range(8)] if R else round(h(e['x'],e['y'])))
    # highest terrain ring within 60
