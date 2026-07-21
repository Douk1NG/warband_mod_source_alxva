# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

lord_relations_menu = [
("lord_relations",0,
   "{s1}",
   "none",
   [
    ##diplomacy start+
	 #Avoid unnecessary iterations, since below we only use slto_kingdom_hero troops.
    (assign, ":met_lord_count", 0),
    #Add support for promoted kingdom ladies.
    #(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
    (try_for_range, ":active_npc", heroes_begin, heroes_end),
      (troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
      (troop_slot_ge, ":active_npc", slot_troop_met, 1),
      (val_add, ":met_lord_count", 1),
    ##diplomacy end+
		(troop_set_slot, ":active_npc", slot_troop_temp_slot, 0),
	(try_end),

	(str_clear, s1),
    ##diplomacy start+
    #Add support for promoted kingdom ladies.
    #(try_for_range, ":unused", active_npcs_begin, active_npcs_end),#<- changed
    #We counted the number of heroes, so we can cut down on the number of
    #iterations (since expanding this from active_npcs to heroes means that
    #a lot of them will not be lords).
    (try_for_range, ":unused", 0, ":met_lord_count"),#<- added
		(assign, ":score_to_beat", -100),
		(assign, ":best_relation_remaining_npc", -1),
		#Add support for promoted kingdom ladies
		#(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),#<-changed
		(try_for_range, ":active_npc", heroes_begin, heroes_end),#<-added
	##diplomacy end+
			(troop_slot_eq, ":active_npc", slot_troop_temp_slot, 0),
			(troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
			(troop_slot_ge, ":active_npc", slot_troop_met, 1),

			(call_script, "script_troop_get_player_relation", ":active_npc"),
			(assign, ":relation_with_player", reg0),
			(ge, ":relation_with_player", ":score_to_beat"),

			(assign, ":score_to_beat", ":relation_with_player"),
			(assign, ":best_relation_remaining_npc", ":active_npc"),
		(try_end),
		(gt, ":best_relation_remaining_npc", -1),

		(str_store_troop_name_link, s4, ":best_relation_remaining_npc"),
		(assign, reg4, ":score_to_beat"),
		(str_store_string, s1, "@{!}{s1}^{s4}: {reg4}"),
		(troop_set_slot, ":best_relation_remaining_npc", slot_troop_temp_slot, 1),
	(try_end),


    ],
    [
      ("continue",[],"Continue...",
       [(jump_to_menu, "mnu_reports"),
        ]
       ),
      ]
  )
]
