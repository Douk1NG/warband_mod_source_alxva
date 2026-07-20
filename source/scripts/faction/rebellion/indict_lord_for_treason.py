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

indict_lord_for_treason_scripts = [
("indict_lord_for_treason",#originally included in simple_triggers. Needed to be moved here to allow player to indict
   [
    (store_script_param, ":troop_no", 1),
    (store_script_param, ":faction", 2),

	##diplomacy start+ use gender script
	#(troop_get_type, reg4, ":troop_no"),
	(assign, ":save_reg0", reg0),
	(assign, ":save_reg3", reg3),
	(assign, ":save_reg4", reg4),
	##diplomacy end+

	(try_for_range, ":center", centers_begin, centers_end), #transfer properties to liege
		(party_slot_eq, ":center", slot_town_lord, ":troop_no"),
		(party_set_slot, ":center", slot_town_lord, stl_unassigned),
		###(((removing banner FIX
		(party_set_banner_icon, ":center", 0),
		###)))
	(try_end),

	(faction_get_slot, ":faction_leader", ":faction", slot_faction_leader),
	(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":faction_leader"),
	(assign, ":liege_to_lord_relation", reg0),
	(store_sub, ":base_relation_modifier", -150, ":liege_to_lord_relation"),
	(val_div, ":base_relation_modifier", 40),#-1 at -100, -2 at -70, -3 at -30,etc.
	(val_min, ":base_relation_modifier", -1),

    # #SB : redistribute wealth to faction ruler
    (try_begin),
      (ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_HIGH),
    # (troop_get_slot, ":cur_wealth", ":troop_no", slot_troop_wealth),
    # (troop_set_slot, ":troop_no", slot_troop_wealth, 0),
    # (call_script, "script_dplmc_distribute_gold_to_lord_and_holdings", ":cur_wealth", ":faction_leader"), #add to ruler
    (try_end),
	#Indictments, cont: Influence relations
	##diplomacy start+ Alter to include promoted ladies
	##OLD:
	#(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end), #this effects all lords in all factions
	##NEW:
	(try_for_range, ":active_npc", heroes_begin, heroes_end), #this effects all lords in all factions
		(this_or_next|is_between, ":active_npc", active_npcs_begin, active_npcs_end),
			(troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
	##diplomacy end+
		(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
		(eq, ":faction", ":active_npc_faction"),

		(call_script, "script_troop_get_family_relation_to_troop", ":troop_no", ":active_npc"),
		(assign, ":family_relation", reg0),

		##diplomacy start+
		(val_max, ":family_relation", 0),
		#Take into account friendship or enmity
		(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":faction_leader"),
		(assign, ":liking_relation", reg0),
		(try_begin),
			(ge, ":liking_relation", 20),
			(store_div, reg0, ":liking_relation", 20),
			(val_add, ":family_relation", reg0),
		(else_try),
			(lt, ":liking_relation", 0),
			(store_div, reg0, ":liking_relation", 20),
			(val_sub, reg0, 1),
			(val_add, ":family_relation", reg0),
		(try_end),
		(store_random_in_range, reg0, 0, 3),#+0, +1, or +2 (because below we divide by three...)
		(val_add, ":family_relation", reg0),
		(assign, reg0, ":family_relation"),
		##diplomacy end+
		(assign, ":relation_modifier", ":base_relation_modifier"),
		(try_begin),
			##diplomacy start+
			#(gt, ":family_relation", 1),##OLD
			(neq, ":family_relation", 0),##NEW (allow lessening penalty for hated characters)
			##diplomacy end+
			(store_div, ":family_multiplier", reg0, 3),
			(val_sub, ":relation_modifier", ":family_multiplier"),
		(try_end),

		(lt, ":relation_modifier", 0),

		(call_script, "script_troop_change_relation_with_troop", ":faction_leader", ":active_npc", ":relation_modifier"),
		(val_add, "$total_indictment_changes", ":relation_modifier"),
		(try_begin),
			(eq, "$cheat_mode", 1),
			(str_store_troop_name, s17, ":active_npc"),
			(str_store_troop_name, s18, ":faction_leader"),

			(assign, reg3, ":relation_modifier"),
			(display_message, "str_trial_influences_s17s_relation_with_s18_by_reg3"),
		(try_end),
	(try_end),

	#Indictments, cont: Check for other factions
	(assign, ":new_faction", "fac_outlaws"),
	(try_begin),
		(eq, ":troop_no", "trp_player"),
		(assign, ":new_faction", 0), #kicked out of faction
	(else_try),
		(call_script, "script_lord_find_alternative_faction", ":troop_no"),
		(assign, ":new_faction", reg0),
	(try_end),

	#Indictments, cont: Finalize where the lord goes
	(try_begin),
		(is_between, ":new_faction", kingdoms_begin, kingdoms_end),


		(try_begin),
			(ge, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":troop_no"),
			(display_message, "@{!}DEBUG - {s4} faction changed in indictment"),
		(try_end),

		(call_script, "script_change_troop_faction", ":troop_no", ":new_faction"),
		(try_begin), #new-begin
		  (neq, ":new_faction", "fac_player_supporters_faction"),
		  (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_inactive),
		  (troop_set_slot, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
		(try_end), #new-end
		(str_store_faction_name_link, s10, ":new_faction"),
		(str_store_string, s11, "str_with_the_s10"),
	(else_try),
		(neq, ":troop_no", "trp_player"),
		##diplomacy start+
		#Set "exile" occupation to differentiate between someone outside of Calradia
		#and an outlaw lord leading a party of bandits.
		(troop_set_slot, ":troop_no", slot_troop_occupation, dplmc_slto_exile),
		##diplomacy end+
		(call_script, "script_change_troop_faction", ":troop_no", "fac_outlaws"),
		(str_store_string, s11, "str_outside_calradia"),
	(else_try),
		(eq, ":troop_no", "trp_player"),
		(call_script, "script_player_leave_faction", 1),
	(try_end),

	#Indictments, cont: Set up string
	(try_begin),
		(eq, ":troop_no", "trp_player"),
		(str_store_string, s9, "str_you_have_been_indicted_for_treason_to_s7_your_properties_have_been_confiscated_and_you_would_be_well_advised_to_flee_for_your_life"),
	(else_try),
		# (str_store_troop_name_plural, s4, ":troop_no"), #this now holds the new faction title, need to be changed
		(str_store_faction_name_link, s5, ":faction"),
		(str_store_troop_name_link, s6, ":faction_leader"),

		##diplomacy start+
		#(troop_get_type, reg4, ":troop_no"),
		(call_script, "script_dplmc_store_troop_is_female", ":troop_no"),
		(assign, reg4, reg0),
		(store_sub, ":title", ":faction", kingdoms_begin),
		(try_begin),
		  (eq, reg4, tf_male),
		  (val_add, ":title", kingdom_titles_male_begin),
		(else_try),
		  (eq, reg4, tf_female),
		  (val_add, ":title", kingdom_titles_female_begin),
		(else_try), #default to lord
		  (assign, ":title", kingdom_titles_male_begin),
		(try_end),
		(str_store_troop_name_plural, s0, ":troop_no"),
		(str_store_string, s4, ":title"),
		##diplomacy end+
		(str_store_string, s9, "str_by_order_of_s6_s4_of_the_s5_has_been_indicted_for_treason_the_lord_has_been_stripped_of_all_reg4herhis_properties_and_has_fled_for_reg4herhis_life_he_is_rumored_to_have_gone_into_exile_s11"),
	(try_end),
	##diplomacy start+ important political events should be in the log
    #SB : colorize with former faction
    (faction_get_color, ":color", s9),
	(display_log_message, s9, ":color"),#display_message changed to display_log_message
	##diplomacy end+

	#Indictments, cont: Remove party
	(troop_get_slot, ":led_party", ":troop_no", slot_troop_leaded_party),
	(try_begin),
		(party_is_active, ":led_party"),
		(neq, ":led_party", "p_main_party"),
		(remove_party, ":led_party"),
		(troop_set_slot, ":troop_no", slot_troop_leaded_party, -1),
	(try_end),

	(try_begin),
		(eq, "$cheat_mode", 1),
		##diplomacy start+
		(this_or_next|eq, ":faction", "fac_player_supporters_faction"),
		(this_or_next|eq, ":new_faction", "fac_player_supporters_faction"),
		##diplomacy end+
		(this_or_next|eq, ":faction", "$players_kingdom"),
			(eq, ":new_faction", "$players_kingdom"),
		(call_script, "script_add_notification_menu", "mnu_notification_treason_indictment", ":troop_no", ":faction"),
	(try_end),
	##diplomacy start+
	(assign, reg0, ":save_reg0"),
	(assign, reg3, ":save_reg3"),
	(assign, reg4, ":save_reg4"),
	##diplomacy end+
   ])
]
