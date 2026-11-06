"""Hardluck ferry route from the real map (see plan notes): approach swing-in, berth alongside the pier, straight departure. Returns node list (x,y,kind)"""
import sys,math,io,contextlib
sys.path.insert(0,'C:/CoA-Build/boats')
BERTH=(891.94,-3617.02,204.1)   # goblin ship x0.45, stern deck at the pier tip (0.9 yd from the edge), parallel to the pier
import math as _m
_R=3/_m.radians(18)
APP=[('A',-1,25,103.5),('S',250)]   # user's U-route: down the right line, swing left over the tip, stop at the angled berth
DEP=[('S',65),('A',-1,25,76.5),('S',250)]   # on out to the left, then up the left line
def build(extra):
    with contextlib.redirect_stdout(io.StringIO()):
        import shoot
    A=shoot.gen(*BERTH,APP,False)[::-1]; D=shoot.gen(*BERTH,DEP,True)
    def thin(p,step):
        out=[p[0]];acc=0;step0=step
        for a,b in zip(p,p[1:]):
            acc+=math.hypot(b[0]-a[0],b[1]-a[1])
            step=8 if math.hypot(b[0]-BERTH[0],b[1]-BERTH[1])<110 else step0
            if acc>=step:out.append(b);acc=0
        if out[-1]!=p[-1]:out.append(p[-1])
        return out
    x0,y0,h0=A[0];a0=math.radians(h0)
    nodes=[(x0-60*math.cos(a0),y0-60*math.sin(a0),0)]                 # far entry (skipped by the core at the teleport)
    nodes+= [(x,y,0) for x,y,h in thin(A,30)[:-1]]
    nodes.append((BERTH[0],BERTH[1],1))                                 # STOP
    xe,ye,he=D[-1];ae=math.radians(he)
    dn=[q for q in thin(D,40)[1:] if math.hypot(q[0]-xe,q[1]-ye)>25]
    nodes+=[(x,y,0) for x,y,h in dn]
    nodes+=[(xe+(0+extra)*math.cos(ae),ye+(0+extra)*math.sin(ae),0),(xe+(30+extra)*math.cos(ae),ye+(30+extra)*math.sin(ae),0)]
    return nodes
if __name__=='__main__':
    n=build(0);print(len(n));print([ (round(a),round(b),k) for a,b,k in n[:4]],[ (round(a),round(b),k) for a,b,k in n[-4:]])
