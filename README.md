# Fading Islands Restore

![Fading Island](images/fading-island.jpg)

Restores the Fading Island (map 907) for a WoW 3.3.5a / CoA server:

- **2 working boats** – Booty Bay <-> Hardluck and Ratchet <-> Hardluck (goblin ships, GO 9900101 / 9900102, taxi paths 2001 / 2002)
- **3 working elevators** replacing static Noggit doodads: Ironforge-style (GO 9900110, path 2003), Coilfang platform (GO 9900111, path 2004, up the cliff to z 390) and Valkyr entrance (GO 9900112, path 2005, up to z 891)
- **Goblin passenger NPCs on the boats** (party outfits, random dance/emotes/voices). No allied or hostile NPCs on the island itself
- **Map edits** (31 ADT tiles) with the missing-texture cubes and floating blocks removed
- **All teleport points** for map 907 (32 `game_tele` rows)
- Scripts used to generate everything (`tools/`)

This repo holds only the Fading Island work, not the client or the server.

## Layout
| Path | Content |
|---|---|
| `map/world/maps/azzararchipelago/` | edited ADT tiles |
| `server/dbc/` | `TaxiPath.dbc`, `TaxiPathNode.dbc` (server copy) |
| `server/sql/hardluck_ferries.sql` | boats, elevator, NPCs, SmartAI |
| `server/sql/fading_islands_teleports.sql` | map 907 teleports |
| `server/core-patches/` | two small core patches (see below) |
| `tools/`, `data/` | generator scripts (hardcoded local paths: reference only) |

## Standalone full-map client patch (any 3.3.5a client)
`patch-ZZZZZB.MPQ` (727 MB, release asset) is self-contained: all 118 map tiles + WDT/WDL, the fixed goblin ships, the DBC changes, plus every model (M2/skins/anims), WMO and texture the map references, taken from the CoA client. Drop it in `Data/` and the full Fading Island (map 907) loads without CoA's other patches. Nothing else is needed on the client. (`patch-ZZZZZA.MPQ` is the small version for clients that already have the base map assets.)
About 380 doodads referenced by the map do not exist in the CoA client either, so they stay invisible; see `data/models-missing-from-client.txt`.

## Editing in Noggit
`FadingIsland-Noggit-Project-v1.0.zip` is the project folder, made with ShadowWorld-Noggit v1.4.6 (the fork that loads `patch-[4-9]/[A-Z]` archives). Put `patch-ZZZZZB.MPQ` in your Noggit client's `Data/`, set `ClientPath` in `Fading island.noggitproj`, open it. Keep `uid.ini`. Note: the project still contains the three static elevator doodads (tiles 39_27, 39_26, 37_26) placed as visual markers; the working elevators are server transports, so the client patch shrinks those static copies to nothing. Do the same (or delete it) before exporting tiles, or you will see two elevators. Ground-effect doodads, textures and models are all bundled in ZZZZZB.
`FadingIsland-OptionalClientDBCs-v1.0.zip`: the client DBCs holding map 907 rows (Map, AreaTable, Light*, ...), only for clients that lack them.

## Install
Release assets: `patch-ZZZZZA.MPQ` (client) and `FadingIslandsRestore-v1.0.zip` (everything).
1. Client: put `patch-ZZZZZA.MPQ` in `Data/`. The client moves transports from its own DBC copy, so it must match the server.
2. Server: copy `server/dbc/*.dbc` into your server `dbc` folder, apply both SQL files to the world DB, apply the core patches and rebuild.
3. Restart the server; `.tele FadingIsland` to visit.

Core patches: `transport-animation-kick` (makes the custom transports start animating) and `ferry-detach-on-fall` (detaches players who fall off the ship).

## Credits / notes
jealous-sound, the CoAC team, svenbledt and Pitho.

Game assets belong to Blizzard Entertainment. scaled and fixed with the included tools..
