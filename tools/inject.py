"""Add invisible collision triangles (flag 0x08, material 0xFF) to a WMO group file and register them in its BSP (MOBN/MOBR)."""
import struct
def inject(path, tris, vis_mat=None):
    d = bytearray(open(path, 'rb').read())
    i = 0
    while i < len(d):
        tg = bytes(d[i:i+4])[::-1]; sz = struct.unpack_from('<I', d, i+4)[0]
        if tg == b'MOGP': break
        i += 8 + sz
    head = i; hdr = bytes(d[i+8:i+8+68]); j = i + 8 + 68; end = i + 8 + sz
    subs = []
    while j < end:
        tg = bytes(d[j:j+4]); s = struct.unpack_from('<I', d, j+4)[0]; subs.append([tg, bytearray(d[j+8:j+8+s])]); j += 8 + s
    S = {t[::-1]: x for t, x in subs}
    nv = len(S[b'MOVT']) // 12; nt = len(S[b'MOVI']) // 6
    newv = []; newi = []
    for (a, b, c) in tris:
        base = nv + len(newv); newv += [a, b, c]; newi.append((base, base+1, base+2))
    for v in newv:
        S[b'MOVT'] += struct.pack('<3f', *v); S[b'MONR'] += struct.pack('<3f', 0, 0, 1); S[b'MOTV'] += struct.pack('<2f', v[0]*0.5, v[1]*0.5) if vis_mat is not None else struct.pack('<2f', 0, 0)
        if b'MOCV' in S: S[b'MOCV'] += struct.pack('<4B', 128, 128, 128, 255)
    for t in newi: S[b'MOVI'] += struct.pack('<3H', *t)
    for _ in newi: S[b'MOPY'] += bytes([0x21, vis_mat]) if vis_mat is not None else bytes([0x08, 0xFF])
    hdr = bytearray(hdr)
    if vis_mat is not None:   # visible tris need a render batch: append one (internal batches, last) and bump the count
        xs = [v for v in newv]; lo = [int(min(v[a] for v in xs)) - 1 for a in range(3)]; hi = [int(max(v[a] for v in xs)) + 1 for a in range(3)]
        S[b'MOBA'] += struct.pack('<6hIHHHBB', *lo, *hi, nt * 3, len(newi) * 3, nv, nv + len(newv) - 1, 0, vis_mat)
        struct.pack_into('<H', hdr, 42, struct.unpack_from('<H', hdr, 42)[0] + 1)
    hdr = bytes(hdr)
    # BSP: collect leaves overlapping each triangle
    nodes = [list(struct.unpack_from('<HhhHIf', S[b'MOBN'], k*16)) for k in range(len(S[b'MOBN'])//16)]
    mobr = list(struct.unpack('<%dH' % (len(S[b'MOBR'])//2), bytes(S[b'MOBR'])))
    extra = {}
    for k, tri in enumerate(newi):
        vs = [newv[x - nv] for x in tri]; lo = [min(v[a] for v in vs) for a in range(3)]; hi = [max(v[a] for v in vs) for a in range(3)]
        stack = [0]
        while stack:
            n = nodes[stack.pop()]
            if n[0] & 4: extra.setdefault(id(n), (n, []))[1].append(nt + k); continue
            ax = n[0] & 3; dist = n[5]
            if lo[ax] < dist and n[1] >= 0: stack.append(n[1])
            if hi[ax] >= dist and n[2] >= 0: stack.append(n[2])
    leaves = sorted([n for n in nodes if n[0] & 4], key=lambda n: n[4]); out = []
    for n in leaves:
        faces = mobr[n[4]:n[4]+n[3]] + extra.get(id(n), (n, []))[1]
        n[4] = len(out); n[3] = len(faces); out += faces
    S[b'MOBN'] = bytearray(b''.join(struct.pack('<HhhHIf', *n) for n in nodes))
    S[b'MOBR'] = bytearray(struct.pack('<%dH' % len(out), *out))
    body = hdr + b''.join(t + struct.pack('<I', len(S[t[::-1]])) + bytes(S[t[::-1]]) for t, _ in subs)
    d[head:end] = b'PGOM' + struct.pack('<I', len(body)) + body
    open(path, 'wb').write(d)
    return len(newi), sum(len(v[1]) for v in extra.values())
