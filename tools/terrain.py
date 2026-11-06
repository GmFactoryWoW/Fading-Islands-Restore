"""Read AzzarArchipelago ADTs -> terrain height + water level grid (server coords). shortcut: MH2O flat level per chunk, no per-vertex depth."""
import struct, os, math
D = 'C:/CoA-Build/boats/map907/'
T = 533.33333; C = T / 16
def tile(bx, by):
    for n in ('AzzarArchipelago_%d_%d.adt', 'azzararchipelago_%d_%d.adt'):
        p = D + n % (bx, by)
        if os.path.exists(p): return open(p, 'rb').read()
def load(bx, by):
    d = tile(bx, by)
    if not d: return None
    chunks = []; i = 0; mh2o = None
    while i < len(d):
        t = d[i:i + 4][::-1]; s = struct.unpack_from('<I', d, i + 4)[0]
        if t == b'MCNK': chunks.append(i)
        if t == b'MH2O': mh2o = i + 8
        i += 8 + s
    out = {}
    for ci, off in enumerate(chunks):
        ix, iy = struct.unpack_from('<II', d, off + 8 + 4)
        ofsH = struct.unpack_from('<I', d, off + 8 + 20)[0]
        z0 = struct.unpack_from('<f', d, off + 8 + 0x70)[0]
        hv = struct.unpack_from('<145f', d, off + ofsH + 8)
        wl = None
        if mh2o:
            oi, lc, oa = struct.unpack_from('<III', d, mh2o + ci * 12)
            if lc:
                lt, lvf, mn, mx = struct.unpack_from('<HHff', d, mh2o + oi)
                wl = mn
        out[(ix, iy)] = (hv, z0, wl)
    return out
def grid(txs, tys, step=8.0):
    """returns dict (ix,iy)->(terrain_z, water_z) sampled at outer vertices; ix = global chunk col, iy = global chunk row"""
    pts = {}
    for bx in txs:
        for by in tys:
            ch = load(bx, by)
            if not ch: continue
            for (ix, iy), (hv, z0, wl) in ch.items():
                x0 = (32 - by) * T - iy * C; y0 = (32 - bx) * T - ix * C
                for r in range(9):
                    for c in range(9):
                        h = hv[r * 17 + c]
                        pts[(round(x0 - r * C / 8, 2), round(y0 - c * C / 8, 2))] = (h + z0, wl)
    return pts
if __name__ == '__main__':
    pts = grid([37, 38, 39], [29, 30, 31])
    print(len(pts))
    near = sorted(pts.items(), key=lambda kv: (kv[0][0] - 893.87) ** 2 + (kv[0][1] + 3620.84) ** 2)[:6]
    for k, v in near: print(k, v)
