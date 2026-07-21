# ======================================================================
# SHARED DEPENDENCY
# Entity: faction_inflict_war_damage_on_faction (script)
# Called by menus in 2 domains: castle, village
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

faction_inflict_war_damage_on_faction_scripts = [
#SB : possibly lower controversy of attacker npc?
("faction_inflict_war_damage_on_faction",
    [
	(store_script_param, ":actor_faction", 1),
	(store_script_param, ":target_faction", 2),
	(store_script_param, ":amount", 3),


	(store_add, ":slot_war_damage", ":target_faction", slot_faction_war_damage_inflicted_on_factions_begin),
	(val_sub, ":slot_war_damage", kingdoms_begin),
	##diplomacy start+ Due to aberrant behavior, non-standard kingdoms
	##like fac_commoners can end up with parties on the map, and possibly
	##could end up inflicting or receiving war damage.  Guard against this.
	(try_begin),
	(is_between, ":slot_war_damage", slot_faction_war_damage_inflicted_on_factions_begin, slot_faction_war_damage_inflicted_on_factions_end),
	(gt, ":actor_faction", 0),
	##diplomacy end+
	(faction_get_slot, ":cur_war_damage", ":actor_faction", ":slot_war_damage"),

	(val_add, ":cur_war_damage", ":amount"),
	(faction_set_slot, ":actor_faction", ":slot_war_damage", ":cur_war_damage"),
	##diplomacy start+ Close added if-statement
	(else_try),
	   #For use in cheat-mode below
	   (assign, ":cur_war_damage", 0),
	(try_end),
	##diplomacy end+


	(try_begin),
	  (ge, "$cheat_mode", 1),
	  (str_store_faction_name, s4, ":actor_faction"),
	  (str_store_faction_name, s5, ":target_faction"),
	  (assign, reg3, ":cur_war_damage"),
	  (assign, reg4, ":amount"),
	  (display_message, "@{!}{s4} inflicts {reg4} damage on {s5}, raising total inflicted to {reg3}"),
	(try_end),


	(faction_get_slot, ":faction_marshal", ":target_faction", slot_faction_marshall),
	(try_begin),
		(ge, ":faction_marshal", 0),
		(gt, ":amount", 0),

		(troop_get_slot, ":controversy", ":faction_marshal", slot_troop_controversy),
		(val_add, ":controversy", ":amount"),
		(val_min, ":controversy", 100),
		(troop_set_slot, ":faction_marshal", slot_troop_controversy, ":controversy"),

		(try_begin),
			(ge, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":faction_marshal"),
			(assign, reg4, ":amount"),
			(assign, reg5, ":controversy"),
			(display_message, "@{!}War damage raises {s4}'s controversy by {reg4} to {reg5}"),
		(try_end),
	(try_end),

	(faction_get_slot, ":faction_marshal", ":actor_faction", slot_faction_marshall),
	(try_begin),
		(ge, ":faction_marshal", 0),
		(val_div, ":amount", 3),
		(gt, ":amount", 0),


		(troop_get_slot, ":controversy", ":faction_marshal", slot_troop_controversy),
		(val_sub, ":controversy", ":amount"),
		(val_max, ":controversy", 0),
		(troop_set_slot, ":faction_marshal", slot_troop_controversy, ":controversy"),

		(try_begin),
			(ge, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":faction_marshal"),
			(assign, reg4, ":amount"),
			(assign, reg5, ":controversy"),
			(display_message, "@{!}War damage lowers {s4}'s controversy by {reg4} to {reg5}"),
		(try_end),
	(try_end),



	])
]
