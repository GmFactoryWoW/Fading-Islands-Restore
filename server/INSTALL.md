# Server install (CoA / TrinityCore 3.3.5 core)

1. **Core (required, boats break without it):** apply `core-patches/*.patch` to `src/server/game` (`git apply --ignore-whitespace`), or copy the full files from `core-patched-files/` over `Entities/Transport/Transport.cpp|.h` and `Handlers/MovementHandler.cpp` (made against the CoA core; on another core use the patches). Rebuild worldserver.
2. **DBCs:** copy `dbc/TaxiPath.dbc` and `dbc/TaxiPathNode.dbc` into the server `dbc` folder. The client needs the same two files (they are inside `patch-ZZZZZA.MPQ` / `patch-ZZZZZB.MPQ`).
3. **SQL (world DB), in this order:** `sql/hardluck_ferries.sql`, then `sql/fading_islands_teleports.sql`. Both are re-runnable.
4. Restart the server. `.tele FadingIsland` goes to the island; the boats start at Booty Bay and Ratchet.
No map/vmap/mmap data for map 907 is needed.
