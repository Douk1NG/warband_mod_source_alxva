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

dplmc_faction_leader_splits_gold_scripts = [
##diplomacy end
# INPUT: arg1 = troop_id, arg2 = new faction_no
# OUTPUT: none
("dplmc_faction_leader_splits_gold",
    [
	(store_script_param_1, ":faction_no"),
    (store_script_param_2, ":king_gold"),
	(assign, ":push_reg0", reg0),#revert register value at end of script
	(assign, ":push_reg1", reg1),#revert register value at end of script

	(faction_get_slot, ":faction_liege", ":faction_no", slot_faction_leader),
	(faction_get_slot, reg0, ":faction_no", dplmc_slot_faction_centralization),
	(val_clamp, reg0, -3, 4),
	(val_mul, reg0, -5),
	(try_begin),
		(troop_slot_ge, ":faction_liege", slot_troop_wealth, 20000),
		(val_add, reg0, 20),#20% if the king is at or above his starting gold
	(else_try),
		(val_add, reg0, 50),#50% otherwise
	(try_end),
	(val_add, reg0, 50),
	(store_mul, ":lord_gold", ":king_gold", reg0),#king splits other half among lords
	(val_div, ":lord_gold", 100),
	(val_sub, ":king_gold", ":lord_gold"),
	(try_begin),
		#If there's enough gold to give a meaningful amount to everyone, do so.
		#(This accomplishes two things.  It makes the distribution more even, and
		#it prevents this script from taking an unreasonably long time for very
		#large amounts of gold.)
		#
		#"Meaningful" is at least 300, because that's the minimum amount of gold a
		#lord will to to a fief to collect (it is also the AI recruitment cost on
		#hard).
		(assign, ":num_lords", 0),#<-- number of lords in faction, not including faction leader
		(try_for_range, ":lord_no", heroes_begin, heroes_end),
			(store_troop_faction, ":lord_faction_no", ":lord_no"),
			(eq, ":faction_no", ":lord_faction_no"),
			(troop_set_slot, ":lord_no", slot_troop_temp_slot, 0),
			(neg|faction_slot_eq, ":faction_no", slot_faction_leader, ":lord_no"),
			(troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
			(neg|troop_slot_ge, ":lord_no", slot_troop_prisoner_of_party, 0),
			(troop_get_slot, ":lord_party", ":lord_no", slot_troop_leaded_party),
			(ge, ":lord_party", 0),
			(val_add, ":num_lords", 1),
		(try_end),
		(try_begin),
			#handle player
			(eq, "$players_kingdom", ":faction_no"),
			(neq, "trp_player", ":faction_liege"),
			(neg|troop_slot_ge, "trp_player", slot_troop_prisoner_of_party, 0),
			(val_add, ":num_lords", 1),
		(try_end),
		(gt, ":num_lords", 0),#<-- can fail
		(store_div, ":gold_to_each", ":lord_gold", ":num_lords"),
		(ge, ":gold_to_each", 300),
		(val_div, ":gold_to_each", 150),#regularize (standard reinforcement costs for easy/medium/hard are 600/450/300, which are multiples of 150)
		(val_mul, ":gold_to_each", 150),

		#(try_begin),
		#	(ge, "$cheat_mode", 1),
		#	(assign, reg0, ":num_lords"),
		#	(assign, reg1, ":gold_to_each"),
		#	(str_store_faction_name, s5, ":faction_no"),
		#	(display_message, "@ {reg0} vassals of the {s5} receive {reg1} denars each (dplmc_faction_leader_splits_gold)"),
		#(try_end),

		(try_for_range, ":lord_no", heroes_begin, heroes_end),
			(ge, ":lord_gold", ":gold_to_each"),
			#verify lord is vassal of kingdom
			(store_troop_faction, ":lord_faction_no", ":lord_no"),
			(eq, ":faction_no", ":lord_faction_no"),
			(neg|faction_slot_eq, ":faction_no", slot_faction_leader, ":lord_no"),
			(troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
			(neg|troop_slot_ge, ":lord_no", slot_troop_prisoner_of_party, 0),
			(troop_get_slot, ":lord_party", ":lord_no", slot_troop_leaded_party),
			(ge, ":lord_party", 0),
			#give gold to lord
			(val_sub, ":lord_gold", ":gold_to_each"),
			#(troop_get_slot, reg0, ":lord_no", slot_troop_temp_slot),
			#(val_add, reg0, ":gold_to_each"),
			#(troop_set_slot, ":lord_no", slot_troop_temp_slot, reg0),
			##(call_script, "script_troop_add_gold", ":lord_no", ":gold_to_each"),
			(call_script, "script_dplmc_distribute_gold_to_lord_and_holdings", ":gold_to_each", ":lord_no"),
		(try_end),
		(try_begin),
			(ge, ":lord_gold", ":gold_to_each"),
			#give gold to player if player is vassal of kingdom
			(eq, "$players_kingdom", ":faction_no"),
			(neq, "trp_player", ":faction_liege"),
			(neg|troop_slot_ge, "trp_player", slot_troop_prisoner_of_party, 0),
			(val_sub, ":lord_gold", ":gold_to_each"),
			(troop_get_slot, reg0, "trp_player", slot_troop_temp_slot),
			(val_add, reg0, ":gold_to_each"),
			(troop_set_slot, "trp_player", slot_troop_temp_slot, reg0),
			##(call_script, "script_troop_add_gold", ":lord_no", ":gold_to_each"),
		(try_end),
	(try_end),
	#Now, distribute the remaining gold.  Assign gold in increments of 300,
	#because that's the minimum amount of gold a lord will go to a fief for
	#(also the AI recruitment cost on hard).
	(store_div, ":count", ":lord_gold", 300),
	(val_max, ":count", 1),
	(try_for_range, ":unused", 0, ":count"),
		(ge, ":lord_gold", 300),
		(call_script, "script_cf_get_random_lord_except_king_with_faction", ":faction_no"),
		(is_between, reg0, heroes_begin, heroes_end),
		(assign, ":troop_no", reg0),
		(val_sub, ":lord_gold", 300),
		(troop_get_slot, reg0, ":troop_no", slot_troop_temp_slot),
		(val_add, reg0, 300),
		(troop_set_slot, ":troop_no", slot_troop_temp_slot, reg0),
		#(call_script, "script_troop_add_gold", ":troop_no", 300),
	(try_end),

	#Now the distribution is set.  Give each one his allotment.
	(try_for_range, ":lord_no", heroes_begin, heroes_end),
		(ge, ":lord_gold", ":gold_to_each"),
		#verify lord is vassal of kingdom
		(store_troop_faction, ":lord_faction_no", ":lord_no"),
		(eq, ":faction_no", ":lord_faction_no"),
		(neg|faction_slot_eq, ":faction_no", slot_faction_leader, ":lord_no"),
		(troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
		(neg|troop_slot_ge, ":lord_no", slot_troop_prisoner_of_party, 0),
		(troop_get_slot, ":lord_party", ":lord_no", slot_troop_leaded_party),
		(ge, ":lord_party", 0),
		#get promised gold
		(troop_get_slot, reg0, ":lord_no", slot_troop_temp_slot),
		(neq, reg0, 0),
		#(try_begin),
		#	(ge, "$cheat_mode", 1),
		#	(str_store_troop_name, s4, ":lord_no"),
		#	(str_store_faction_name, s5, ":faction_no"),
		#	(str_store_troop_name, s6, ":faction_liege"),
		#	(display_message, "@{!}{s4} of the {s5} receives {reg0} denars (dplmc_faction_leader_splits_gold)"),
		#(try_end),
		(call_script, "script_dplmc_distribute_gold_to_lord_and_holdings", reg0, ":lord_no"),
		(troop_set_slot, ":lord_no", slot_troop_temp_slot, 0),
	(try_end),

	(val_add, ":king_gold", ":lord_gold"),#Give remaining gold to king
	(try_begin),
		(ge, "$cheat_mode", 1),
		(str_store_troop_name, s4, ":troop_no"),
		(str_store_faction_name, s5, ":faction_no"),
		(str_store_troop_name, s6, ":faction_liege"),
		(display_message, "@{!}{s6} of the {s5} retains the remaining {reg0} denars (dplmc_faction_leader_splits_gold)"),
	(try_end),

	#(call_script, "script_troop_add_gold", ":faction_liege", ":king_gold"),
	(call_script, "script_dplmc_distribute_gold_to_lord_and_holdings", ":king_gold", ":faction_liege"),
	(assign, reg0, ":push_reg0"),#revert register value
	(assign, reg1, ":push_reg1"),#revert register value
	])
]
