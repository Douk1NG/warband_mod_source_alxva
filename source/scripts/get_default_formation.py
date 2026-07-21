# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from module_constants import *
from header_parties import *
from header_skills import *
from header_mission_templates import *
from header_items import *
from header_triggers import *
from header_terrain_types import *
from header_music import *
from header_map_icons import *
from ID_animations import *

get_default_formation_scripts = [
("get_default_formation", [
      (store_script_param, ":fteam", 1),
      (team_get_slot, ":ffaction", ":fteam", slot_team_faction),
      (try_begin),
        (this_or_next | eq, ":ffaction", fac_player_supporters_faction),
        (eq, ":ffaction", fac_player_faction),
        (is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
        (assign, ":ffaction", "$players_kingdom"),
      (try_end),

      (try_begin),
        (is_between, ":ffaction", "fac_player_faction", kingdoms_end),
        (faction_slot_ge, ":ffaction", slot_faction_culture, 1),
        (faction_get_slot, ":ffaction", ":ffaction", slot_faction_culture),
      (try_end),

      #assign default formation
      (try_begin),
        (eq, ":ffaction", fac_kingdom_1),	#Swadians
        (assign, reg0, formation_shield),	#use shields, stabby weapons
      (else_try),
        (eq, ":ffaction", fac_kingdom_2),	#Vaegirs
        (assign, reg0, formation_ranks),	#have a mix, so favor those nasty axes
      (else_try),
        (eq, ":ffaction", fac_kingdom_3),	#Khergit
        (assign, reg0, formation_none),	#Khergit have underdeveloped infantry
      (else_try),
        (eq, ":ffaction", fac_kingdom_4),	#Nords
        (assign, reg0, formation_ranks),	#favor swung weapons
      (else_try),
        (eq, ":ffaction", fac_kingdom_5),	#Rhodoks
        (assign, reg0, formation_shield),	#have a mix, so favor those big shields and pikes
      (else_try),
        (eq, ":ffaction", fac_kingdom_6),	#Sarranid
        (assign, reg0, formation_shield),
      (else_try),
        (this_or_next | eq, ":ffaction", fac_player_supporters_faction),
        (eq, ":ffaction", fac_player_faction),	#independent player
        (assign, reg0, formation_ranks),
      (else_try),
        (assign, reg0, formation_none),	#riffraff don't use formations
      (try_end),])
]
