# ======================================================================
# SHARED DEPENDENCY
# Entity: change_center_prosperity (script)
# Called by menus in 3 domains: castle, center_management, cheats
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

change_center_prosperity_scripts = [
#script_get_troop_item_amount
# INPUT: arg1 = center_no, arg2 = difference
# OUTPUT: none
("change_center_prosperity",
    [(store_script_param, ":center_no", 1),
     (store_script_param, ":difference", 2),
     (party_get_slot, ":old_prosperity", ":center_no", slot_town_prosperity),
     (store_add, ":new_prosperity", ":old_prosperity", ":difference"),
     (val_clamp, ":new_prosperity", 0, 100),
     (store_div, ":old_state", ":old_prosperity", 20),
     (store_div, ":new_state", ":new_prosperity", 20),

     (try_begin),
       (neq, ":old_state", ":new_state"),
	   (neg|is_between, ":center_no", castles_begin, castles_end),

       (str_store_party_name_link, s2, ":center_no"),
       (call_script, "script_get_prosperity_text_to_s50", ":center_no"),
       (str_store_string, s3, s50),
       (party_set_slot, ":center_no", slot_town_prosperity, ":new_prosperity"),
       (call_script, "script_get_prosperity_text_to_s50", ":center_no"),
       (str_store_string, s4, s50),
       (try_begin),
         (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
         (display_message, "@Prosperity of {s2} has changed from {s3} to {s4}."),
       (try_end),
       (call_script, "script_update_center_notes", ":center_no"),
     (else_try),
       (party_set_slot, ":center_no", slot_town_prosperity, ":new_prosperity"),
     (try_end),

	 (try_begin),
		(store_current_hours, ":hours"),
		(gt, ":hours", 1),
		(store_sub, ":actual_difference", ":new_prosperity", ":old_prosperity"),
		(try_begin),
			(lt, ":actual_difference", 0),
			(val_add, "$newglob_total_prosperity_losses", ":actual_difference"),
	    (else_try),
			(gt, ":actual_difference", 0),
			(val_add, "$newglob_total_prosperity_gains", ":actual_difference"),
		(try_end),
	 (try_end),

	 #This will add up all non-trade prosperity
	 (try_begin),
		(eq, "$cheat_mode", 3),
		(assign, reg4, "$newglob_total_prosperity_from_bandits"),
		(assign, reg5, "$newglob_total_prosperity_from_caravan_trade"),
	    (assign, reg7, "$newglob_total_prosperity_from_villageloot"),
	    (assign, reg8, "$newglob_total_prosperity_from_townloot"),
	    (assign, reg9, "$newglob_total_prosperity_from_village_trade"),
	    (assign, reg10, "$newglob_total_prosperity_from_convergence"),
	    (assign, reg11, "$newglob_total_prosperity_losses"),
	    (assign, reg12, "$newglob_total_prosperity_gains"),
		(display_message, "@{!}DEBUG: Total prosperity actual losses: {reg11}"),
		(display_message, "@{!}DEBUG: Total prosperity actual gains: {reg12}"),

		(display_message, "@{!}DEBUG: Prosperity changes from random bandits: {reg4}"),
		(display_message, "@{!}DEBUG: Prosperity changes from caravan trades: {reg5}"),
		(display_message, "@{!}DEBUG: Prosperity changes from farmer trades: {reg9}"),
		(display_message, "@{!}DEBUG: Prosperity changes from looted villages: {reg7}"),
		(display_message, "@{!}DEBUG: Prosperity changes from sieges: {reg8}"),
		(display_message, "@{!}DEBUG: Theoretical prosperity changes from convergence: {reg10}"),
	 (try_end),

     ])
]
