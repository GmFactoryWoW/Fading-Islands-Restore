"""Hardluck ferries: Booty Bay <-> Hardluck and Ratchet <-> Hardluck. Idempotent (rebuilds from the originals saved in orig/)."""
import struct, math, os, sys, shutil, ctypes
sys.path[:0] = ['C:/CoA-Build/tools']
B = 'C:/CoA-Build/boats/'
SRV = 'C:/CoA-Repack/Data/dbc/'
# dock end (screenshot) and tuning
EX, EY, EZ, EO = 893.87, -3620.84, -7.23, 2.218
SHIP_ORIGIN = 3.09     # home ports: scaled ship keel at the water, deck (+0.45) ~5.65 = Ratchet dock height 5.2-5.7
HOME_Z = SHIP_ORIGIN               # ports sit at sea level 0
WATER_Z = -6.3    # Hardluck: origin 2.0 above the sea (stern deck 1.0 above the pier top, lower cabin floor stays above water)
HL_DELAY = 45
HOME_DELAY = {'booty': 70, 'ratchet': 70}
ORDER = {'booty': 'home_first', 'ratchet': 'hl_first'}
EXTRA = {'booty': 253.5, 'ratchet': 288.8}   # exit-run yards: fine-tunes the cycle to 231.112 s (= Maiden's Fancy)
STOP_DIST = 19.0        # ship centre to dock end
PATH_IDS = {'booty': 2001, 'ratchet': 2002}
PASS_MAP = {'booty': 592, 'ratchet': 596}   # own passenger-set ids (593 belongs to the Maiden's Fancy crew/chairs)
GO_IDS = {'booty': 9900101, 'ratchet': 9900102}
names = {'booty': 'Ship (Hardluck Ferry, Booty Bay)', 'ratchet': 'Ship (Hardluck Ferry, Ratchet)'}
f2u = lambda f: struct.unpack('<I', struct.pack('<f', f))[0]
u2f = lambda u: struct.unpack('<f', struct.pack('<I', u))[0]

def parse(d):
    m, n, fc, rs, ss = struct.unpack_from('<4sIIII', d, 0)
    return [list(struct.unpack_from('<%dI' % fc, d, 20 + i * rs)) for i in range(n)], d[20 + n * rs:], fc, rs
def build(rows, st, fc, rs):
    return struct.pack('<4sIIII', b'WDBC', len(rows), fc, rs, len(st)) + b''.join(struct.pack('<%dI' % fc, *r) for r in rows) + st

os.makedirs(B + 'orig', exist_ok=True)
for n in ('TaxiPath', 'TaxiPathNode'):
    if not os.path.exists(B + 'orig/%s.dbc' % n): shutil.copy(SRV + n + '.dbc', B + 'orig/%s.dbc' % n)
nodes, nst, nfc, nrs = parse(open(B + 'orig/TaxiPathNode.dbc', 'rb').read())
paths, pst, pfc, prs = parse(open(B + 'orig/TaxiPath.dbc', 'rb').read())
src = sorted([r for r in nodes if r[1] == 241], key=lambda r: r[2])   # Booty Bay <-> Ratchet loop
ratchet = [r for r in src if r[3] == 1]; booty = [r for r in src if r[3] == 0]

d = (math.cos(EO), math.sin(EO)); p = (-d[1], d[0])
def at(k, side=0.0): return (EX + d[0] * k + p[0] * side, EY + d[1] * k + p[1] * side)
# Hardluck leg on map 907: real-map route (route2.py): swing-in approach, berth alongside the pier, straight exit to open sea
import route2
def hardluck(k):
    out = []
    for x, y, kind in route2.build(EXTRA[k]):
        out.append((907, x, y, WATER_Z, 2 if kind else 0, HL_DELAY if kind else 0, 16397 if kind else 0))
    return out
def cp(r): return (r[3], u2f(r[4]), u2f(r[5]), u2f(r[6]), r[7], r[8], r[9])
DOCK_SHIFT = {'ratchet': (-1.0, {-2: .35, -1: .7, 0: 1, 1: .7, 2: .35}), 'booty': (-4.6, {-3: .35, -2: .7, -1: 1, 0: 1, 1: 1, 2: .7, 3: .35})}  # +left / -right of travel, yards at the stop (dock edge: Ratchet 17.4 left, Booty ~27 right of the big ferry's track)
FWD = {'booty': 1.0, 'ratchet': 0.0}   # yards further along the track before stopping
def shifted(rows, k):
    pts = [list(cp(r)) for r in rows]
    si = [i for i, r in enumerate(rows) if r[7] == 2][0]; amt, w = DOCK_SHIFT[k]
    base = [(p[1], p[2]) for p in pts]
    for off, f in w.items():
        i = si + off
        if 0 < i < len(pts) - 1:
            tx, ty = base[i + 1][0] - base[i - 1][0], base[i + 1][1] - base[i - 1][1]; L = math.hypot(tx, ty); lx, ly = -ty / L, tx / L
            pts[i][1] += lx * amt * f + tx / L * FWD[k] * f; pts[i][2] += ly * amt * f + ty / L * FWD[k] * f
    return pts
def home(rows, k):
    return [(m, x, y, z + HOME_Z, af, HOME_DELAY[k] if af == 2 else dl, ev) for (m, x, y, z, af, dl, ev) in shifted(rows, k)]
routes = {}
for k, rows in (('booty', booty), ('ratchet', ratchet)):
    HL = hardluck(k)
    routes[k] = home(rows, k) + HL if ORDER[k] == 'home_first' else HL + home(rows, k)
# the original loops already contain their own approach before the stop: ratchet nodes start at the approach, booty nodes too
nid = max(r[0] for r in nodes) + 1
nodes = [r for r in nodes if r[1] not in PATH_IDS.values()]; paths = [r for r in paths if r[0] not in PATH_IDS.values()]
nid = max(r[0] for r in nodes) + 1
for k, route in routes.items():
    for i, (m, x, y, z, af, dl, ev) in enumerate(route):
        nodes.append([nid, PATH_IDS[k], i, m, f2u(x), f2u(y), f2u(z), af, dl, ev, 0]); nid += 1
    paths.append([PATH_IDS[k], 34, 80, 0])

# --- Fading Island elevators (Noggit doodads as moving transports: straight up to the top floor, stop, come back) ---
import json as _jj
EL_WAIT = 20
# model suffix -> path id, GO entry, GODI display id, floor height above the model origin (collision mesh, before scale), top floor feet z (None = ironforge .gps), speed, name
ELEVS = [('ironforgeelevator.m2', 2003, 9900110, 561, 1.1, 190.2109, 22, 'Fading Island Elevator'),
         ('cf_elevatorplatform.m2', 2004, 9900111, 7043, 1.5, 390.0, 63, 'Fading Island Elevator (Coilfang)'),
         ('fading_island_valkyr_entrance_elevator_01.m2', 2005, 9900112, 1041789, 0.5, 891.0, 27, 'Fading Island Elevator (Valkyr Entrance)')]
_scan = _jj.load(open(B + 'elevscan.json')) if os.path.exists(B + 'elevscan.json') else []
ELS = []
for (suf, pid, go, disp, foff, top, spd, nm) in ELEVS:
    m = [e for e in _scan if e['model'].endswith(suf)]
    if m: ELS.append((m[0], pid, go, disp, foff, top, spd, nm))
for (EL, EL_PATH, EL_GO, EL_DISPLAY, foff, top, spd, nm) in ELS:
    z0 = EL['z']; z1 = top - foff * EL['scale']
    o_t = math.radians(EL['rot'][1] + 180.0)         # server orientation of the doodad (derived from Noggit's model matrix: rotY + 180 deg)
    ua = o_t - math.pi                              # the core faces atan2(dir)+pi: a tiny drift along this direction keeps the yaw fixed
    ux, uy = math.cos(ua), math.sin(ua)
    nodes = [r for r in nodes if r[1] != EL_PATH]; paths = [r for r in paths if r[0] != EL_PATH]
    nid = max(r[0] for r in nodes) + 1
    # few long segments with a drift of 5 cm per step (a smaller step is lost in float precision and the yaw jitters = shaking)
    D = 0.05
    seq = [(0.0, z0, 0, 0), (D, z0 + 0.05, 2, EL_WAIT), (2 * D, z1, 2, EL_WAIT), (3 * D, (z0 + z1) / 2, 0, 0), (4 * D, z0 + 0.05, 0, 0), (5 * D, z0 + 0.05, 0, 0)]   # the core drops the last node's segment: the real bottom is the one before it; the bottom stop is not the first/last frame (the core ignores those)
    for i, (e, z, af, dl) in enumerate(seq):
        nodes.append([nid, EL_PATH, i, 907, f2u(EL['x'] + ux * e), f2u(EL['y'] + uy * e), f2u(z), af, dl, 0, 0]); nid += 1
    paths.append([EL_PATH, 34, 80, 0])
nodes.sort(key=lambda r: r[0]); paths.sort(key=lambda r: r[0])
os.makedirs(B + 'out', exist_ok=True)
open(B + 'out/TaxiPathNode.dbc', 'wb').write(build(nodes, nst, nfc, nrs))
open(B + 'out/TaxiPath.dbc', 'wb').write(build(paths, pst, pfc, prs))
print({k: len(v) for k, v in routes.items()})
# SQL
sql = ['-- Hardluck ferries (Booty Bay and Ratchet to Hardluck, map 907). Needs the TaxiPath/TaxiPathNode DBCs with paths 2001/2002.',
       'DELETE FROM gameobject_template WHERE entry IN (9900101,9900102);', 'DELETE FROM gameobject_template_addon WHERE entry IN (9900101,9900102);', 'DELETE FROM transports WHERE entry IN (9900101,9900102);']
for k in routes:
    sql.append("INSERT INTO gameobject_template (entry,type,displayId,name,IconName,castBarCaption,unk1,size,Data0,Data1,Data2,Data3,Data4,Data5,Data6,AIName,ScriptName,VerifiedBuild) VALUES (%d,15,1009923,'%s','','','',1,%d,30,1,0,0,1,%d,'','',12340);" % (GO_IDS[k], names[k], PATH_IDS[k], PASS_MAP[k]))
    sql.append("INSERT INTO gameobject_template_addon (entry,faction,flags,mingold,maxgold,artkit0,artkit1,artkit2,artkit3) VALUES (%d,0,40,0,0,0,0,0,0);" % GO_IDS[k])
    sql.append("INSERT INTO transports (guid,entry,name,ScriptName) SELECT IFNULL(MAX(guid),0)+1,%d,'%s','' FROM transports;" % (GO_IDS[k], names[k]))


for (EL, EL_PATH, EL_GO, EL_DISPLAY, foff, top, spd, nm) in ELS:
    sql += ["DELETE FROM gameobject_template WHERE entry=%d;" % EL_GO, "DELETE FROM gameobject_template_addon WHERE entry=%d;" % EL_GO, "DELETE FROM transports WHERE entry=%d;" % EL_GO,
            "INSERT INTO gameobject_template (entry,type,displayId,name,IconName,castBarCaption,unk1,size,Data0,Data1,Data2,Data3,Data4,Data5,Data6,AIName,ScriptName,VerifiedBuild) VALUES (%d,15,%d,'%s','','','',%.4f,%d,%d,1,0,0,1,0,'','',12340);" % (EL_GO, EL_DISPLAY, nm, EL['scale'], EL_PATH, spd),
            "INSERT INTO gameobject_template_addon (entry,faction,flags,mingold,maxgold,artkit0,artkit1,artkit2,artkit3) VALUES (%d,0,40,0,0,0,0,0,0);" % EL_GO,
            "INSERT INTO transports (guid,entry,name,ScriptName) SELECT IFNULL(MAX(guid),0)+1,%d,'%s','' FROM transports;" % (EL_GO, nm)]

HOME_NAME = {'booty': 'Booty Bay', 'ratchet': 'Ratchet'}
_SC = "INSERT INTO smart_scripts (entryorguid,source_type,id,link,event_type,event_phase_mask,event_chance,event_flags,event_param1,event_param2,event_param3,event_param4,event_param5,event_param6,action_type,action_param1,action_param2,action_param3,action_param4,action_param5,action_param6,target_type,target_param1,target_param2,target_param3,target_param4,target_x,target_y,target_z,target_o,comment) VALUES (%d,%d,%d,0,%d,0,100,0,%d,%d,%d,%d,0,0,%d,%d,%d,0,0,0,0,1,0,0,0,0,0,0,0,0,'%s');"
import json as _json
_NP = _json.load(open(B + 'npc_positions.json'))
def _p(p, o): return (p[0], p[1], p[2] + 0.05, o)
CREW = {'booty': [(9900211, 'Booty Bay Traveler', _p(_NP['main'][0], 3.14)), (9900212, 'Fading Island Traveler', _p(_NP['main'][1], 1.57))],
        'ratchet': [(9900213, 'Ratchet Traveler', _p(_NP['main'][0], 3.14)), (9900214, 'Fading Island Traveler', _p(_NP['main'][1], 1.57))]}
OLD_CREW = (9900201, 9900202, 9900203, 9900204)   # renamed crews got new ids (the client cached the old names)
for e in OLD_CREW:
    sql += ["DELETE FROM creature_template WHERE entry=%d;" % e, "DELETE FROM creature_template_model WHERE CreatureID=%d;" % e, "DELETE FROM smart_scripts WHERE entryorguid=%d AND source_type=0;" % e,
            "DELETE FROM creature_text WHERE CreatureID=%d;" % e, "DELETE FROM conditions WHERE SourceTypeOrReferenceId=22 AND SourceEntry=%d;" % e]
# goblin passengers (party-outfit goblins: Booty Bay Reveler displays 15762/15763 male, 15764/15765 female); none in the rear third / engine (x>9.6)
PASSENGER_ENTRY = 9900221
PASSENGERS = [_p(p, 0.7 * (i + 1)) for i, p in enumerate(_NP['main'][2:] + _NP['second'] + _NP['upper'] + _NP['roof'])]
sql.append('DELETE FROM creature WHERE map IN (59901,59902);'); sql.append('DELETE FROM gameobject WHERE map IN (59901,59902);')
for k, crew in CREW.items():
    h = HOME_NAME[k]
    sql.append("DELETE FROM creature WHERE map=%d;" % PASS_MAP[k])
    for i, (eid, nm, pos) in enumerate(crew):
        txt = ([("Hardluck Docks, folks! We shove off for %s shortly - hop aboard!" % h), ("%s! Next stop: Hardluck Island in the Fading Isles. All aboard!" % h)] if i == 0 else
               [("Mind the pier! This ferry is heading back to %s." % h), ("Hardluck-bound! Hold onto your hats, we sail for the Fading Isles.")])
        sql += ["DELETE FROM creature_template WHERE entry=%d;" % eid, "DELETE FROM creature_template_model WHERE CreatureID=%d;" % eid,
                "DELETE FROM smart_scripts WHERE entryorguid=%d AND source_type=0;" % eid, "DELETE FROM creature_text WHERE CreatureID=%d;" % eid,
                "DELETE FROM conditions WHERE SourceTypeOrReferenceId=22 AND SourceEntry=%d;" % eid,
                "DROP TEMPORARY TABLE IF EXISTS tmpct;", "CREATE TEMPORARY TABLE tmpct AS SELECT * FROM creature_template WHERE entry=3453;",
                "UPDATE tmpct SET entry=%d, name='%s', subname='Hardluck Ferry', npcflag=0, AIName='SmartAI', ScriptName='', MovementType=0;" % (eid, nm),
                "INSERT INTO creature_template SELECT * FROM tmpct;",
                "INSERT INTO creature_template_model (CreatureID,Idx,CreatureDisplayID,DisplayScale,Probability,VerifiedBuild) SELECT %d,Idx,CreatureDisplayID,DisplayScale,Probability,VerifiedBuild FROM creature_template_model WHERE CreatureID=3453;" % eid,
                "INSERT INTO creature_text (CreatureID,GroupID,ID,Text,Type,Language,Probability,Emote,Duration,Sound,BroadcastTextId,TextRange,comment) VALUES (%d,0,0,'%s',12,0,100,0,0,0,0,0,'ferry crew: on Hardluck map');" % (eid, txt[0].replace("'", "''")),
                "INSERT INTO creature_text (CreatureID,GroupID,ID,Text,Type,Language,Probability,Emote,Duration,Sound,BroadcastTextId,TextRange,comment) VALUES (%d,1,0,'%s',12,0,100,0,0,0,0,0,'ferry crew: on home map');" % (eid, txt[1].replace("'", "''"))]
        for ev, grp in ((0, 0), (1, 1)):
            sql.append("INSERT INTO smart_scripts (entryorguid,source_type,id,link,event_type,event_phase_mask,event_chance,event_flags,event_param1,event_param2,event_param3,event_param4,event_param5,event_param6,action_type,action_param1,action_param2,action_param3,action_param4,action_param5,action_param6,target_type,target_param1,target_param2,target_param3,target_param4,target_x,target_y,target_z,target_o,comment) VALUES (%d,0,%d,0,10,0,100,0,0,25,45000,45000,0,0,1,%d,0,0,0,0,0,1,0,0,0,0,0,0,0,0,'ferry crew announces the destination');" % (eid, ev, grp))
            sql.append("INSERT INTO conditions (SourceTypeOrReferenceId,SourceGroup,SourceEntry,SourceId,ElseGroup,ConditionTypeOrReference,ConditionTarget,ConditionValue1,ConditionValue2,ConditionValue3,NegativeCondition,ErrorType,ErrorTextId,ScriptName,Comment) VALUES (22,%d,%d,0,0,22,0,907,0,0,%d,0,0,'','ferry crew: map 907 check');" % (ev + 1, eid, 0 if ev == 0 else 1))
        sql.append("INSERT INTO creature (guid,id,map,zoneId,areaId,spawnMask,phaseMask,equipment_id,position_x,position_y,position_z,orientation,spawntimesecs,wander_distance,currentwaypoint,curhealth,curmana,MovementType,npcflag,unit_flags,dynamicflags,ScriptName,VerifiedBuild,CreateObject,Comment) SELECT IFNULL(MAX(guid),0)+1,%d,%d,0,0,1,1,0,%.2f,%.2f,%.2f,%.2f,300,0,0,1,0,0,0,0,0,'',12340,0,'ferry crew' FROM creature;" % (eid, PASS_MAP[k], pos[0], pos[1], pos[2], pos[3]))
# goblin passengers: 5 male + 5 female per ferry, several outfits (Booty Bay / Brewfest / Winter revelers), 3 of 10 never dance (still emote)
MALE_D = (15762, 15763, 21854, 21855, 19342)
FEMALE_D = (15764, 15765, 21856, 21857, 19339)
ALLD = MALE_D + FEMALE_D
PASS_BASE = 9900240
def pass_entry(did, nodance): return PASS_BASE + ALLD.index(did) * 2 + (1 if nodance else 0)
sql += ["DELETE FROM creature_template WHERE entry BETWEEN %d AND %d OR entry=%d;" % (PASS_BASE, PASS_BASE + 19, PASSENGER_ENTRY),
        "DELETE FROM creature_template_model WHERE CreatureID BETWEEN %d AND %d OR CreatureID=%d;" % (PASS_BASE, PASS_BASE + 19, PASSENGER_ENTRY),
        "DELETE FROM smart_scripts WHERE source_type=0 AND (entryorguid BETWEEN %d AND %d OR entryorguid=%d);" % (PASS_BASE, PASS_BASE + 19, PASSENGER_ENTRY),
        "DELETE FROM smart_scripts WHERE source_type=9 AND entryorguid=%d;" % (PASSENGER_ENTRY * 100 + 1),
        "DELETE FROM creature_template_addon WHERE entry BETWEEN %d AND %d OR entry=%d;" % (PASS_BASE, PASS_BASE + 19, PASSENGER_ENTRY),
        "DROP TEMPORARY TABLE IF EXISTS tmpct;", "CREATE TEMPORARY TABLE tmpct AS SELECT * FROM creature_template WHERE entry=3453;"]
for did in ALLD:
    for nd in (0, 1):
        e = pass_entry(did, nd)
        sql += ["UPDATE tmpct SET entry=%d, name='Goblin Passenger', subname='', npcflag=0, AIName='SmartAI', ScriptName='', MovementType=0;" % e,
                "INSERT INTO creature_template SELECT * FROM tmpct;",
                "INSERT INTO creature_template_model (CreatureID,Idx,CreatureDisplayID,DisplayScale,Probability,VerifiedBuild) VALUES (%d,0,%d,1,1,12340);" % (e, did)]
        emo = [(20000, 60000, 70000, 150000, 5, 11, 'laugh'), (30000, 90000, 90000, 200000, 5, 4, 'cheer'), (40000, 100000, 100000, 220000, 5, 275, 'train')]
        if not nd: emo.append((1000, 40000, 240000, 480000, 17, 10, 'dance'))   # starts dancing 1-40 s after spawn (staggered), re-asserted now and then
        VOICE = {11: (6913, 6908), 4: (2835, 2847), 275: (7641, 7640)}   # goblin /laugh /cheer /train voices (male, female) from EmotesTextSound
        _SCL = _SC.replace("VALUES (%d,%d,%d,0,%d", "VALUES (%d,%d,%d,%d,%d")
        for sid, (mn, mx, rmn, rmx, at, p1, nm_) in enumerate(emo):
            sql.append(_SC % (e, 0, sid, 1, mn, mx, rmn, rmx, at, p1, 0, 'passenger ' + nm_))          # silent emote, fairly often
        f = 0.6 + 0.2 * (ALLD.index(did) % 6) + 0.1 * nd                                              # different pace per NPC type
        for j, p1 in enumerate((11, 4, 275)):                                                            # rare emote WITH voice (every ~10-40 min each)
            sid = 20 + j
            sql.append(_SCL % (e, 0, sid, sid + 10, 1, int(600000 * f * (1 + j * 0.4)), int(2400000 * f * (1 + j * 0.3)), int(1500000 * f * (1 + j * 0.3)), int(3600000 * f * (1 + j * 0.2)), 5, p1, 0, 'passenger voiced %d' % p1))
            sql.append(_SCL % (e, 0, sid + 10, 0, 61, 0, 0, 0, 0, 4, VOICE[p1][0 if did in MALE_D else 1], 0, 'passenger voice %d' % p1))
NODANCE = (2, 5, 8)
for ki, k in enumerate(PASS_MAP):
    for i, (px_, py_, pz_, po_) in enumerate(PASSENGERS):
        did = (MALE_D if i % 2 == 0 else FEMALE_D)[(i // 2 + ki * 2) % 5]
        sql.append("INSERT INTO creature (guid,id,map,zoneId,areaId,spawnMask,phaseMask,equipment_id,position_x,position_y,position_z,orientation,spawntimesecs,wander_distance,currentwaypoint,curhealth,curmana,MovementType,npcflag,unit_flags,dynamicflags,ScriptName,VerifiedBuild,CreateObject,Comment) SELECT IFNULL(MAX(guid),0)+1,%d,%d,0,0,1,1,0,%.2f,%.2f,%.2f,%.2f,300,0,0,1,0,0,0,0,0,'',12340,0,'ferry passenger' FROM creature;" % (pass_entry(did, i in NODANCE), PASS_MAP[k], px_, py_, pz_, po_))
sql += ['DELETE FROM gameobject WHERE id=9900103;', 'DELETE FROM gameobject_template WHERE entry=9900103;']   # old ramp, removed

# crates over the ladder hatches so nobody walks onto the (collision-less) stairs
sql += ['DELETE FROM gameobject WHERE id=9900301;', 'DELETE FROM gameobject_template WHERE entry=9900301;']   # crates removed (missing-texture cubes); the invisible hatch lids in the WMO do the blocking
open(B + 'out/hardluck_ferries.sql', 'w').write('\n'.join(sql) + '\n')
