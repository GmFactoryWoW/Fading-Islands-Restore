-- Fading Island (map 907): spirit healer + graveyard. Players who die on the island release here.
-- Needs the core patch island-graveyard-zone0 (map 907 has no AreaTable rows, zone/area = 0).
DELETE FROM creature WHERE guid=9900300;
DROP TEMPORARY TABLE IF EXISTS tmp_sh;
CREATE TEMPORARY TABLE tmp_sh SELECT * FROM creature WHERE id=6491 AND map=0 LIMIT 1;
UPDATE tmp_sh SET guid=9900300, map=907, position_x=905.4983, position_y=-4820.654, position_z=326.3246, orientation=2.4467669, phaseMask=1, spawntimesecs=300;
INSERT INTO creature SELECT * FROM tmp_sh;
DROP TEMPORARY TABLE tmp_sh;
DELETE FROM game_graveyard WHERE ID=9900301;
INSERT INTO game_graveyard (ID,Map,x,y,z,Comment) VALUES (9900301,907,905.4983,-4820.654,326.3246,'Fading Island');
DELETE FROM graveyard_zone WHERE ID=9900301;
INSERT INTO graveyard_zone (ID,GhostZone,Faction,Comment) VALUES (9900301,0,0,'Fading Island (zone 0 on map 907)');
