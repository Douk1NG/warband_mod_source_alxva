# ======================================================================
# SHARED DEPENDENCY
# Entity: start_fucking (script)
# Called by menus in 2 domains: dickplomacy, town
# ======================================================================

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

start_fucking_scripts = [
# value
#OUTPUT:
# none
("start_fucking",
   [
     (store_script_param, ":training_param", 1),
     (store_script_param, ":scene", 2),

		  (set_jump_mission,"mt_fucking"),
		  (modify_visitors_at_site, ":scene"),
		  (reset_visitors),

       (try_for_range, ":i", 0, ":training_param"),
         (troop_get_slot, ":cur_troop", "trp_temp_array_a", ":i"),
         (troop_get_slot, ":cur_troop_dna", "trp_temp_array_b", ":i"),
		 (ge, ":cur_troop", 0),

		(call_script, "script_dplmc_store_troop_is_female_reg", ":cur_troop", 65),
		(assign, ":is_female", reg65),

        (try_begin),
            (eq, "$g_player_is_captive", 1),
            (mission_tpl_entry_set_override_flags, "mt_fucking", 2, af_override_horse|af_override_body|af_override_weapons),
            (mission_tpl_entry_set_override_flags, "mt_fucking", 3, af_override_horse|af_override_body),
            (mission_tpl_entry_set_override_flags, "mt_fucking", 4, af_override_horse|af_override_body),
        (try_end),

		 #(neq, ":cur_troop", "bandit_leaders_end"),
		 (try_begin),
			(eq, ":i", 0),
			(assign, ":cur_entry_point", 1),
		 (else_try),
			(eq, ":i", 1),
			(try_begin),
				(eq, "$g_sex_position", 0),
				(assign, ":cur_entry_point", 2),
			(else_try),
				(assign, ":cur_entry_point", 3),
			(try_end),
			(try_begin),
				(eq, ":is_female", 1),
				(mission_tpl_entry_add_override_item,"mt_fucking",":cur_entry_point","itm_strapon"),
			(try_end),
		 (else_try),
			(eq, ":i", 2),
			(assign, ":cur_entry_point", 5),
		 (else_try),
			(eq, ":i", 3),
			(assign, ":cur_entry_point", 4),
			(try_begin),
				(eq, ":is_female", 1),
				(mission_tpl_entry_add_override_item,"mt_fucking",":cur_entry_point","itm_strapon"),
			(try_end),
		 (else_try),
			(assign, ":cur_entry_point", 0),
		 (try_end),


         (try_begin),
            (troop_get_type, ":type", ":cur_troop"),
            (lt, ":type", 2),
            (val_add, ":type", 2),
            (troop_set_type, ":cur_troop", ":type"),
         (try_end),
         (try_begin),
           (this_or_next|troop_is_hero, ":cur_troop"),
            (lt, ":cur_troop_dna", 0),
            (set_visitor, ":cur_entry_point", ":cur_troop"),
         (else_try),
            (set_visitor, ":cur_entry_point", ":cur_troop", ":cur_troop_dna"),
         (try_end),
       (try_end),

		(set_visitor, 0, "trp_bandit_leaders_end"),

		  (jump_to_scene,":scene"),
		  (change_screen_mission),



     ])
]
