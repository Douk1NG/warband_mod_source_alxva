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

appoint_faction_marshall_scripts = [
("appoint_faction_marshall",
    [
	(store_script_param, ":faction_no", 1),
	(store_script_param, ":faction_marshall", 2),


    (faction_get_slot, ":faction_leader", ":faction_no", slot_faction_leader),
    (faction_get_slot, ":old_marshall", ":faction_no", slot_faction_marshall),

    (faction_set_slot, ":faction_no", slot_faction_marshall, ":faction_marshall"),

    (try_begin),
		(ge, ":old_marshall", 0),
		(troop_get_slot, ":old_marshall_party", ":old_marshall", slot_troop_leaded_party),
        (party_is_active, ":old_marshall_party"),
        (party_set_marshal, ":old_marshall_party", 0),
    (try_end),


    (try_begin),
      (ge, ":faction_marshall", 0),
	  (troop_get_slot, ":new_marshall_party", ":faction_marshall", slot_troop_leaded_party),
      (party_is_active, ":new_marshall_party"),
      (party_set_marshal,":new_marshall_party", 1),
    (try_end),


	(try_begin),
		(neq, ":faction_marshall", ":faction_leader"),
		(neq, ":faction_marshall", ":old_marshall"),
		##diplomacy start+ Support promoted kingdom ladies
		(this_or_next|eq, ":faction_marshall", "trp_player"),
			(is_between, ":faction_marshall", heroes_begin, heroes_end),
		(this_or_next|troop_slot_eq, ":faction_marshall", slot_troop_occupation, slto_kingdom_hero),
		##diplomacy end+
		(this_or_next|eq, ":faction_marshall", "trp_player"),
			(is_between, ":faction_marshall", active_npcs_begin, active_npcs_end),

		(this_or_next|neq, ":faction_no", "fac_player_supporters_faction"),
			(neg|check_quest_active, "qst_rebel_against_kingdom"),

		(try_begin),
			(eq, "$cheat_mode", 1),
			(str_store_faction_name, s15, ":faction_no"),
			(display_message, "str_checking_lord_reactions_in_s15"),
		(try_end),


		(call_script, "script_troop_change_relation_with_troop", ":faction_marshall", ":faction_leader", 5),
		(val_add, "$total_promotion_changes", 5),

		##diplomacy start+
		(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", ":faction_no"),
		(assign, ":player_standing_in_faction", reg0),
		#(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),

		#Support promoted kingdom ladies
		##OLD:
		#(try_for_range, ":lord", active_npcs_begin, active_npcs_end),
		##NEW:
		(try_for_range, ":lord", heroes_begin, heroes_end),
		##diplomacy end+
			(troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
			(store_faction_of_troop, ":lord_faction", ":lord"),
			(eq, ":lord_faction", ":faction_no"),

			(neq, ":lord", ":faction_marshall"),
			(neq, ":lord", ":faction_leader"),

			(call_script, "script_troop_get_relation_with_troop", ":faction_marshall", ":lord"),
#			(try_begin),
#				(eq, "$cheat_mode", 1),
#				(str_store_troop_name, s14, ":lord"),
#				(str_store_troop_name, s17, ":faction_marshall"),
#				(display_message, "@{!}{s14}'s relation with {s17} is {reg0}"),
#			(try_end),
			(store_sub, ":adjust_relations", reg0, 10),
			(val_div, ":adjust_relations", 15),
			##diplomacy start+
			#In some situtations the player can set the marshall freely even though he isn't the faction leader.
			(try_begin),
				(eq, ":faction_marshall", "trp_player"),
				(ge, ":player_standing_in_faction", DPLMC_FACTION_STANDING_LEADER_SPOUSE),
				#Still allow a relation gain below if the lord had actively supported the player
				#(which doesn't happen now if the player is the ruler, but could).
				(val_min, ":adjust_relations", 0),
			(try_end),
			##diplomacy end+
			(neq, ":adjust_relations", 0),

			#Not negatively affected if they favored the lord
			(try_begin),
				(troop_slot_eq, ":lord", slot_troop_stance_on_faction_issue, ":faction_marshall"),
				(val_add, ":adjust_relations", 1),
				(val_max, ":adjust_relations", 0),
			(try_end),

			(call_script, "script_troop_change_relation_with_troop", ":faction_leader", ":lord", ":adjust_relations"),
			(val_add, "$total_promotion_changes", ":adjust_relations"),

			(lt, ":adjust_relations", -2),
			(store_random_in_range, ":random", 1, 10),

			(val_add, ":adjust_relations", ":random"),

			(lt, ":adjust_relations", 0),

			(str_store_troop_name, s14, ":lord"),
			(str_store_troop_name, s15, ":faction_marshall"),

			(try_begin),
			##diplomacy start+ Show protest information for your own kingdom if you have a chancellor or are the ruler
				(ge, ":player_standing_in_faction", DPLMC_FACTION_STANDING_MEMBER),
				(this_or_next|ge, ":player_standing_in_faction", DPLMC_FACTION_STANDING_LEADER_SPOUSE),#<- via the minister, or just hearing about it
					(gt, "$g_player_chancellor", 0),#<- via your chancellor
				(neg|troop_slot_eq, ":lord", slot_troop_met, 0),
				(display_message, "str_s14_protests_the_appointment_of_s15_as_marshall"),
			(else_try),
				(call_script, "script_dplmc_store_troop_is_eligible_for_affiliate_messages", ":lord"),
				(this_or_next|gt, reg0, 0),
			##diplomacy end+
                (eq, "$cheat_mode", 1),
                (display_message, "str_s14_protests_the_appointment_of_s15_as_marshall"),
            (try_end),

			(call_script, "script_troop_change_relation_with_troop", ":faction_leader", ":lord", -10),
			(call_script, "script_troop_change_relation_with_troop", ":faction_marshall", ":lord", -5),
			(val_add, "$total_promotion_changes", -15),

			(call_script, "script_add_log_entry", logent_lord_protests_marshall_appointment, ":lord",  ":faction_marshall", ":faction_leader", "$g_encountered_party_faction"),

		(try_end),
	(try_end),

		])
]
