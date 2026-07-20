# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from module_constants import *
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

game_get_morale_of_troops_from_faction_scripts = [
# This script is called from the game engine
# Input:
# param1: faction_no,
# Output: reg0: extra morale x 100
("game_get_morale_of_troops_from_faction",
    [
      (store_script_param_1, ":troop_no"),

      (store_troop_faction, ":faction_no", ":troop_no"),

      (try_begin),
        (is_between, ":faction_no", npc_kingdoms_begin, npc_kingdoms_end),

        (faction_get_slot, reg0, ":faction_no",  slot_faction_morale_of_player_troops),

        #(assign, reg1, ":faction_no"),
        #(assign, reg2, ":troop_no"),
        #(assign, reg3, reg0),
        #(display_message, "@extra morale for troop {reg2} of faction {reg1} is {reg3}"),
      (else_try),
        (assign, reg0, 0),
      (try_end),
      ##diplomacy start+
      #If there is no current morale penalty, then there will be a minor morale bonus
		#if the player has his own faction and his culture matches the source kingdom.
		(try_begin),
		   (eq, reg0, 0),
			(is_between,"$g_player_culture", npc_kingdoms_begin, npc_kingdoms_end),
			(eq, "$g_player_culture", ":faction_no"),
			#xxx TODO: pick a number less arbitrarily
			(assign, reg0, 100),
		(try_end),
      ##diplomacy end+
      (val_div, reg0, 100),

      (party_get_morale, reg1, "p_main_party"),

      (val_add, reg0, reg1),

      (set_trigger_result, reg0),
  ])
]
