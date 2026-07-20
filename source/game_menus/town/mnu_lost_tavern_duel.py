# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

lost_tavern_duel_menu = [
("lost_tavern_duel",mnf_disable_all_keys,
    "{s11}{s12}",
    "none",
    [
    (str_clear, s11),
    (str_clear, s12),
    #use s11 as primary indicator string
	(try_begin),
		(agent_get_troop_id, ":type", "$g_main_attacker_agent"),
		(eq, ":type", "trp_belligerent_drunk"),
		(try_begin),
			(eq, "$g_sexual_content", 2),
			(this_or_next|eq, "$character_gender", 1),(eq, "$g_nohomo", 0),
			(agent_get_entry_no, ":entry_no", "$g_main_attacker_agent"),
			(troop_get_slot, ":dna", "trp_temp_array_c", ":entry_no"), #I really don't know why this won't work.
			(troop_set_slot, "trp_temp_array_a", 0, "trp_player"),
			(troop_set_slot, "trp_temp_array_b", 0, -1),
			(troop_set_slot, "trp_temp_array_a", 1, ":type"),
			(troop_set_slot, "trp_temp_array_b", 1, ":dna"),
			(assign, "$g_sex_position", 1),
			(assign, "$f_encountertype", 1),
			(assign, "$f_cons1", -1), #Non-con
			(assign, "$f_cons2", 0), #Con
			(str_store_string, s11, "@You slump to the floor, stunned by the drunk's last blow. Your attacker's rage seems unending. He flails about and flips a table as the other tavern-goers beat a hasty retreat. Suddenly, he grabs you by the leg and drags you up to the rooms..."),
		(else_try),
			(str_store_string, s11, "str_lost_tavern_duel_ordinary"),
		(try_end),
	(else_try),
		(agent_get_troop_id, ":type", "$g_main_attacker_agent"),
		(eq, ":type", "trp_hired_assassin"),
		(str_store_string, s11, "str_lost_tavern_duel_assassin"),
	(try_end),
	(troop_set_slot, "trp_hired_assassin", slot_troop_cur_center, -1),
	(troop_set_slot, "trp_belligerent_drunk", slot_troop_cur_center, -1), #remove him for now

    #use s12 for additional info like lost purse, etc
    #SB : penalty for fighting while disguised
    (try_begin),
      (gt, "$sneaked_into_town", disguise_none),
      (store_random_in_range, ":random_no", -100, 200),
      # (ge, ":random_no", "$g_player_luck"),
      (ge, ":random_no", 0),
      (str_store_string, s12, "@ Unfortunately, when the guards inquired about the tavern brawl, your description was recognized and you were in no condition to fight them off."),
    (try_end),
    ],
    [
      ("continue",[(eq, "$sneaked_into_town", disguise_none),],"Continue...",
       [
		(try_begin), # Drunk barfight loss scene
			(eq, "$g_sexual_content", 2),
			(this_or_next|eq, "$character_gender", 1),(eq, "$g_nohomo", 0),
			(call_script, "script_change_troop_renown", "trp_player", -5),
			(call_script, "script_start_fucking", 2, "scn_tavern"),
		(else_try),
        (jump_to_menu, "mnu_town"),
        (troop_set_health, "trp_player", 25),
        #SB : renown loss, less than losing to bandits
        (call_script, "script_change_troop_renown", "trp_player", -1),
		(try_end),
       ]),

      ("surrender",[(gt, "$sneaked_into_town", disguise_none),],"Surrender...",
       [
         (jump_to_menu, "mnu_captivity_castle_taken_prisoner"),
       ]),
    ]
  )
]
