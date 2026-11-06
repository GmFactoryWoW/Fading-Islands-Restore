import os, sys, ctypes
sys.path[:0] = ['C:/CoA-Build/tools', 'C:/CoA-Build/eunoia']
import storm, mpqread
S = storm.S
S.SFileCreateArchive.argtypes = [ctypes.c_char_p, ctypes.c_uint32, ctypes.c_uint32, ctypes.POINTER(ctypes.c_void_p)]; S.SFileCreateArchive.restype = ctypes.c_bool
S.SFileAddFileEx.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32]; S.SFileAddFileEx.restype = ctypes.c_bool
O = 'C:/CoA-Build/boats/out/'
files = {'DBFilesClient'+chr(92)+'TaxiPath.dbc': O + 'TaxiPath.dbc', 'DBFilesClient'+chr(92)+'TaxiPathNode.dbc': O + 'TaxiPathNode.dbc'}
BS = chr(92)
for nm in ('goblinshipfinal.wmo', 'goblinshipfinal_000.wmo', 'goblinshipfinal_001.wmo', 'goblinshipfinal_002.wmo', 'goblinshipfinal_003.wmo'): files[BS.join(['world', 'wmo', 'kalimdor', 'lostisles', nm])] = O + 'wmo/' + nm
files['DBFilesClient'+chr(92)+'GameObjectDisplayInfo.dbc'] = O + 'GameObjectDisplayInfo.dbc'
for b in os.listdir(O + 'adt'): files[BS.join(['World', 'Maps', 'AzzarArchipelago', b])] = O + 'adt/' + b   # patch_adt.py output
arc = O + 'patch-ZZZZZA.MPQ'
if os.path.exists(arc): os.remove(arc)
h = ctypes.c_void_p()
assert S.SFileCreateArchive(arc.encode(), 0x01000000 | 0x00100000 | 0x00200000, 64, ctypes.byref(h))
for n, p in files.items(): assert S.SFileAddFileEx(h, p.encode(), n.encode(), 0x200 | 0x80000000, 2, 2), n
S.SFileCloseArchive(h)
m = mpqread.MPQ(arc)
for n, p in files.items(): assert m.read(n) == open(p, 'rb').read(), n
print('ok', arc, os.path.getsize(arc))
