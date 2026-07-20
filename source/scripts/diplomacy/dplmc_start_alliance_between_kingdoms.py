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
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

dplmc_start_alliance_between_kingdoms_scripts = [
#script_dplmc_start_alliance_between_kingdoms, 20 days alliance, 40 days truce after that
# Input: arg1 = kingdom_1, arg2 = kingdom_2, arg3 = initializing_war_peace_cond
# Output: none
("dplmc_start_alliance_between_kingdoms", #sets relations between two kingdoms
    [
      (store_script_param, ":kingdom_a", 1),
      (store_script_param, ":kingdom_b", 2),
      (store_script_param, ":initializing_war_peace_cond", 3),
	  ##diplomacy start+
	  #Since "fac_player_supporters_faction" is used as a shorthand for the faction
	  #run by the player, intercept that here instead of the various places this is
	  #called from.
	  (assign, ":save_reg1", reg1),
	  (call_script, "script_dplmc_translate_inactive_player_supporter_faction_2", ":kingdom_a", ":kingdom_b"),
	  (assign, ":kingdom_a", reg0),
	  (assign, ":kingdom_b", reg1),
	  (assign, reg1, ":save_reg1"),
	  ##diplomacy end+

      (store_relation, ":relation", ":kingdom_a", ":kingdom_b"),
      (val_add, ":relation", 15),
      (val_max, ":relation", 40),
      (set_relation, ":kingdom_a", ":kingdom_b", ":relation"),
      (call_script, "script_exchange_prisoners_between_factions", ":kingdom_a", ":kingdom_b"),

      (try_begin),
        (eq, "$players_kingdom", ":kingdom_a"),
        (store_relation, ":relation", "fac_player_supporters_faction", ":kingdom_b"),
        (val_add, ":relation", 15),
        (val_max, ":relation", 40),
        (call_script, "script_set_player_relation_with_faction", ":kingdom_b", ":relation"),
        #(call_script, "script_event_kingdom_make_peace_with_kingdom", ":kingdom_b", "fac_player_supporters_faction"), #event cancels certain quests
      (else_try),
        (eq, "$players_kingdom", ":kingdom_b"),
        (store_relation, ":relation", "fac_player_supporters_faction", ":kingdom_a"),
        (val_add, ":relation", 15),
        (val_max, ":relation", 40),
        (call_script, "script_set_player_relation_with_faction", ":kingdom_a", ":relation"),
        #(call_script, "script_event_kingdom_make_peace_with_kingdom", ":kingdom_a", "fac_player_supporters_faction"), #event cancels certain quests
      (try_end),

      (try_begin),
        (eq, ":initializing_war_peace_cond", 1),
        (str_store_faction_name_link, s1, ":kingdom_a"),
        (str_store_faction_name_link, s2, ":kingdom_b"),
		##diplomacy start+ #Due to complaints about the wording
        #(display_log_message, "@{s1} and {s2} have concluded an alliance with each other."),
		(display_log_message, "@{s1} and {s2} have entered into an alliance with each other."),
		##diplomacy end+

        (call_script, "script_add_notification_menu", "mnu_dplmc_notification_alliance_declared", ":kingdom_a", ":kingdom_b"), #stability penalty for early peace is in the menu

        (call_script, "script_event_kingdom_make_peace_with_kingdom", ":kingdom_a", ":kingdom_b"), #cancels quests
        (call_script, "script_event_kingdom_make_peace_with_kingdom", ":kingdom_b", ":kingdom_a"), #cancels quests
        (assign, "$g_recalculate_ais", 1),


      (try_end),

	  (try_begin), #add truce
		(store_add, ":truce_slot", ":kingdom_a", slot_faction_truce_days_with_factions_begin),
		(val_sub, ":truce_slot", kingdoms_begin),
	    ##nested diplomacy start+ replace 80 with a named constant
	    #(faction_set_slot, ":kingdom_b", ":truce_slot", 80),
	    (faction_set_slot, ":kingdom_b", ":truce_slot", dplmc_treaty_alliance_days_initial),
	    ##nested diplomacy end+

		(store_add, ":truce_slot", ":kingdom_b", slot_faction_truce_days_with_factions_begin),
		(val_sub, ":truce_slot", kingdoms_begin),
	    ##nested diplomacy start+ replace 80 with a named constant
	    #(faction_set_slot, ":kingdom_a", ":truce_slot", 80),
	    (faction_set_slot, ":kingdom_a", ":truce_slot", dplmc_treaty_alliance_days_initial),
	    ##nested diplomacy end+

		(store_add, ":slot_war_damage_inflicted_on_b", ":kingdom_b", slot_faction_war_damage_inflicted_on_factions_begin),
		(val_sub, ":slot_war_damage_inflicted_on_b", kingdoms_begin),
		(faction_get_slot, ":damage_inflicted_by_a", ":kingdom_a", ":slot_war_damage_inflicted_on_b"),
		(try_begin),
			(lt, ":damage_inflicted_by_a", 100),
			#controversial policy
		(try_end),
		(faction_set_slot, ":kingdom_a", ":slot_war_damage_inflicted_on_b", 0),

		(store_add, ":slot_war_damage_inflicted_on_a", ":kingdom_a", slot_faction_war_damage_inflicted_on_factions_begin),
		(val_sub, ":slot_war_damage_inflicted_on_a", kingdoms_begin),
		(faction_get_slot, ":damage_inflicted_by_b", ":kingdom_b", ":slot_war_damage_inflicted_on_a"),
		(try_begin),
			(lt, ":damage_inflicted_by_b", 100),
			#controversial policy
		(try_end),
		(faction_set_slot, ":kingdom_b", ":slot_war_damage_inflicted_on_a", 0),

	  (try_end),

    # share wars
    (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
      (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
      (neq, ":kingdom_a", ":faction_no"),
      (neq, ":kingdom_b", ":faction_no"),
      (call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction",":kingdom_a", ":faction_no"),
      #result: -1 faction_1 has a casus belli against faction_2. 1, faction_1 has a truce with faction_2, -2, the two factions are at war
      (eq, reg0, -2),
      (call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction",":kingdom_b", ":faction_no"),
      (ge, reg0, -1),
      (call_script, "script_diplomacy_start_war_between_kingdoms", ":kingdom_b", ":faction_no", 2),
    (try_end),
    (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
      (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
      (neq, ":kingdom_a", ":faction_no"),
      (neq, ":kingdom_b", ":faction_no"),
      (call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction",":kingdom_b", ":faction_no"),
      #result: -1 faction_1 has a casus belli against faction_2. 1, faction_1 has a truce with faction_2, -2, the two factions are at war
      (eq, reg0, -2),
      (call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction",":kingdom_a", ":faction_no"),
      (ge, reg0, -1),
      (call_script, "script_diplomacy_start_war_between_kingdoms", ":kingdom_a", ":faction_no", 2),
    (try_end),
  ])
]
