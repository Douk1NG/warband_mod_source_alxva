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

prepare_town_to_fight_scripts = [
(
   "prepare_town_to_fight",
   [
     (str_store_party_name_link, s9, "$g_starting_town"),
     (str_store_string, s2, "str_save_town_from_bandits"),
     (call_script, "script_start_quest", "qst_save_town_from_bandits", "$g_talk_troop"),

     (assign, "$g_mt_mode", tcm_default),
     (store_faction_of_party, ":town_faction", "$current_town"),
     (faction_get_slot, ":tier_2_troop", ":town_faction", slot_faction_tier_3_troop),
     (faction_get_slot, ":tier_3_troop", ":town_faction", slot_faction_tier_3_troop),
     (faction_get_slot, ":tier_4_troop", ":town_faction", slot_faction_tier_4_troop),

     (party_get_slot, ":town_scene", "$current_town", slot_town_center),

     (set_jump_mission,"mt_town_fight"), #dckplmc

     (modify_visitors_at_site, ":town_scene"),
     (reset_visitors),

     #people spawned at #32, #33, #34, #35, #36, #37, #38 and #39 are town walkers.
     (try_begin),
       #(eq, "$town_nighttime", 0),
       (try_for_range, ":walker_no", 0, num_town_walkers),
         (store_add, ":troop_slot", slot_center_walker_0_troop, ":walker_no"),
         (party_get_slot, ":walker_troop_id", "$current_town", ":troop_slot"),
         (gt, ":walker_troop_id", 0),
         (store_add, ":entry_no", town_walker_entries_start, ":walker_no"),

		 #dckplmc - add daggers and clubs
		 (mission_tpl_entry_set_override_flags, "mt_town_fight", ":entry_no", af_override_weapons),
		 (store_random_in_range, ":r", 0,2),
		 (try_begin),
			(eq, ":r", 0),
			(mission_tpl_entry_add_override_item, "mt_town_fight", ":entry_no", "itm_dagger"),
		 (else_try),
			(mission_tpl_entry_add_override_item, "mt_town_fight", ":entry_no", "itm_club"),
		 (try_end),

         (set_visitor, ":entry_no", ":walker_troop_id"),
       (try_end),
     (try_end),

     #guards will be spawned at #25, #26 and #27
     (set_visitors, 25, ":tier_2_troop", 1),
     (set_visitors, 26, ":tier_3_troop", 1),
     (set_visitors, 27, ":tier_4_troop", 1),

     (set_visitors, 10, "trp_looter", 1),
     (set_visitors, 11, "trp_bandit", 1),
     (set_visitors, 12, "trp_looter", 1),

     # (store_faction_of_party, ":starting_town_faction", "$g_starting_town"),
     #SB : add a few bandits alongside the looters
     (call_script, "script_center_get_bandits", "$g_starting_town", 0),
     (assign, ":bandit_troop", reg0),
     (call_script, "script_get_troop_of_merchant"),
     (assign, ":troop_of_merchant", reg0),
     (str_store_troop_name, s10, ":troop_of_merchant"),

     (set_visitors, 24, "trp_looter", 1),
     (set_visitors, 2, ":bandit_troop", 2),
     (set_visitors, 4, "trp_looter", 1),
     (set_visitors, 5, "trp_looter", 2),
     (set_visitors, 6, "trp_looter", 1),
     (set_visitors, 7, ":bandit_troop", 1),

	 #dckplmc
	 (mission_tpl_entry_set_override_flags, "mt_town_fight", 3, af_override_weapons),
	 (mission_tpl_entry_add_override_item, "mt_town_fight", 3, "itm_dagger"),
     (set_visitors, 3, ":troop_of_merchant", 1),


     #(set_jump_mission,"mt_town_fight"),
     (jump_to_scene, ":town_scene"),
     (change_screen_mission),
   ])
]
