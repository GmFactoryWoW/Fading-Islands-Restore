cd /c/CoA-Build/boats && python elevscan.py >/dev/null && python make_boats.py | tail -1 && python scale_gs.py >/dev/null && python fix_assets.py >/dev/null && python scale_up.py >/dev/null && python sync_map.py && python pack.py | tail -1
/c/CoA-Repack/mysql/bin/mysql.exe --defaults-extra-file=C:/CoA-Repack/mysql/admin-client.ini --default-character-set=utf8mb4 acore_world < /c/CoA-Build/boats/out/hardluck_ferries.sql && echo SQL_OK
cp out/TaxiPath.dbc out/TaxiPathNode.dbc /c/CoA-Repack/Data/dbc/; cp out/patch-ZZZZZA.MPQ "/c/Ascension Local/Data/patch-ZZZZZA.MPQ" && echo CLIENT_COPIED || echo CLIENT_BUSY
cd /c/CoA-Repack && Runtime/python/python.exe -B Scripts/manage.py stop-all 2>&1 | tail -1; bash /c/CoA-Build/fix_and_start.sh | head -1
grep -a "TRANSPORTPATH 200\|TRANSPORTSTOP 200" Core/Logs/world-console.log | tail -6 | cut -c1-100
