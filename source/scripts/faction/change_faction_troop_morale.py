# ======================================================================
# SHARED DEPENDENCY
# Entity: change_faction_troop_morale (script)
# Called by menus in 4 domains: camp, dickplomacy, tournament, village
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

change_faction_troop_morale_scripts = [
##"script_cf_dplmc_player_party_meets_autoloot_conditions"
#input - faction, change, display mode
#output - a colored message
("change_faction_troop_morale",
	  [(store_script_param, ":faction_no", 1),
	   (store_script_param, ":morale_change", 2),
	   (store_script_param, ":display", 3),
	   (try_begin),
		 (eq, ":display", 1),
		 (neg|faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
		 (assign, ":display", 0),
	   (try_end),
	   #check if main party has troop of type before displaying
	   (try_begin),
		 (eq, ":display", 1),
		 (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
		 (try_for_range, ":stack", 1, ":num_stacks"),
		   (party_stack_get_troop_id, ":troop", "p_main_party", ":stack"),
		   (store_troop_faction, ":fac", ":troop"),
		   (eq, ":fac", ":faction_no"),
		   (assign, ":num_stacks", 1), #break
		 (try_end),
		 (neq, ":num_stacks", 1), #none found
		 (assign, ":display", 0),
	   (try_end),
	   #effects are still applied regardless - the displayed morale is divided by 100
	   (faction_get_slot, ":morale", ":faction_no", slot_faction_morale_of_player_troops),
	   (store_div, reg1, ":morale", 100),
	   (val_add, ":morale", ":morale_change"),
	   (store_div, reg2, ":morale", 100),
	   (faction_set_slot, ":faction_no", slot_faction_morale_of_player_troops, ":morale"),

	   # (try_begin),
		 # (store_sub, ":diff", reg2, reg1),
		 # (eq, ":diff", 0), #negligible
		 # (assign, ":display", 0),
	   # (try_end),

	   #actual output
	   (try_begin),
		 (eq, ":display", 1),
         (neq, reg1, reg2), #non-zero difference
		 #set up s1
		 #(faction_get_slot, ":adjective", ":faction_no", slot_faction_adjective),
         (str_store_faction_name, s1, ":faction_no"),
		 #(str_store_string, s1, ":adjective"),
		 (str_store_string, s1, "@{s1} troops"),
		 #get increase/decrease, either string will work
		 (assign, ":string", "str_troop_relation_detoriated"),
		 (try_begin),
		   (gt, ":morale_change", 0),
		   (assign, ":string", "str_troop_relation_increased"),
		 (try_end),
		 #get color
		 (faction_get_color, ":color", ":faction_no"),
		 (display_message, ":string", ":color"),
	   (try_end),
	  ]
	)
]
