# ======================================================================
# SHARED DEPENDENCY
# Entity: diplomacy_start_peace_between_kingdoms (script)
# Called by menus in 2 domains: diplomacy, kingdom_management
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
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

diplomacy_start_peace_between_kingdoms_scripts = [
("diplomacy_start_peace_between_kingdoms", #sets relations between two kingdoms
    [
      (store_script_param, ":kingdom_a", 1),
      (store_script_param, ":kingdom_b", 2),
      (store_script_param, ":initializing_war_peace_cond", 3), #set to 1 if not the start of the game

      (store_relation, ":relation", ":kingdom_a", ":kingdom_b"),
      (val_max, ":relation", 0),
      (set_relation, ":kingdom_a", ":kingdom_b", ":relation"),
      (call_script, "script_exchange_prisoners_between_factions", ":kingdom_a", ":kingdom_b"),

      (try_begin),
        (eq, "$players_kingdom", ":kingdom_a"),
        (store_relation, ":relation", "fac_player_supporters_faction", ":kingdom_b"),
        (val_max, ":relation", 0),
        (call_script, "script_set_player_relation_with_faction", ":kingdom_b", ":relation"),
        (call_script, "script_event_kingdom_make_peace_with_kingdom", ":kingdom_b", "fac_player_supporters_faction"), #event cancels certain quests
      (else_try),
        (eq, "$players_kingdom", ":kingdom_b"),
        (store_relation, ":relation", "fac_player_supporters_faction", ":kingdom_a"),
        (val_max, ":relation", 0),
        (call_script, "script_set_player_relation_with_faction", ":kingdom_a", ":relation"),
        (call_script, "script_event_kingdom_make_peace_with_kingdom", ":kingdom_a", "fac_player_supporters_faction"), #event cancels certain quests
      (try_end),

      (try_for_range, ":cur_center", centers_begin, centers_end),
        (store_faction_of_party, ":faction_no", ":cur_center"),
        (this_or_next|eq, ":faction_no", ":kingdom_a"),
        (eq, ":faction_no", ":kingdom_b"),
        (party_get_slot, ":besieger_party", ":cur_center", slot_center_is_besieged_by),
        (ge, ":besieger_party", 0), #town is under siege
        (party_is_active, ":besieger_party"),
        (store_faction_of_party, ":besieger_party_faction_no", ":besieger_party"),
        (this_or_next|eq, ":besieger_party_faction_no", ":kingdom_a"),
        (eq, ":besieger_party_faction_no", ":kingdom_b"),
        (call_script, "script_lift_siege", ":cur_center", 0),
      (try_end),

      (try_begin),
        (this_or_next|eq, "$players_kingdom", ":kingdom_a"),
        (eq, "$players_kingdom", ":kingdom_b"),

        (ge, "$g_player_besiege_town", 0),
        (party_is_active, "$g_player_besiege_town"),

        (store_faction_of_party, ":besieged_center_faction_no", "$g_player_besiege_town"),

        (this_or_next|eq, ":besieged_center_faction_no", ":kingdom_a"),
        (eq, ":besieged_center_faction_no", ":kingdom_b"),

        (call_script, "script_lift_siege", "$g_player_besiege_town", 0),
        (assign, "$g_player_besiege_town", -1),
      (try_end),

      (try_begin),
        (eq, ":initializing_war_peace_cond", 1),
        (str_store_faction_name_link, s1, ":kingdom_a"),
        (str_store_faction_name_link, s2, ":kingdom_b"),
        (display_log_message, "@{s1} and {s2} have made peace with each other.", message_alert),
        (call_script, "script_add_notification_menu", "mnu_notification_peace_declared", ":kingdom_a", ":kingdom_b"), #stability penalty for early peace is in the menu
        (call_script, "script_event_kingdom_make_peace_with_kingdom", ":kingdom_a", ":kingdom_b"), #cancels quests
        (call_script, "script_event_kingdom_make_peace_with_kingdom", ":kingdom_b", ":kingdom_a"), #cancels quests
        (assign, "$g_recalculate_ais", 1),
      (try_end),

	  (try_begin), #add truce
		(store_add, ":truce_slot", ":kingdom_a", slot_faction_truce_days_with_factions_begin),
		(val_sub, ":truce_slot", kingdoms_begin),
		##diplomacy begin
	    #(faction_set_slot, ":kingdom_b", ":truce_slot", 40),
        ##nested diplomacy start+ replace "20" with constant for truce length
#        (faction_set_slot, ":kingdom_b", ":truce_slot", 20),
        (faction_set_slot, ":kingdom_b", ":truce_slot", dplmc_treaty_truce_days_initial),
        ##nested diplomacy end+
	    ##diplomacy end
		(store_add, ":truce_slot", ":kingdom_b", slot_faction_truce_days_with_factions_begin),
		(val_sub, ":truce_slot", kingdoms_begin),
	    ##diplomacy begin
	    #(faction_set_slot, ":kingdom_a", ":truce_slot", 40),
        ##nested diplomacy start+ replace "20" with constant for truce length
        #(faction_set_slot, ":kingdom_a", ":truce_slot", 20),
        (faction_set_slot, ":kingdom_a", ":truce_slot", dplmc_treaty_truce_days_initial),
        ##nested diplomacy end+
        ##diplomacy end
		(store_add, ":slot_war_damage_inflicted_on_b", ":kingdom_b", slot_faction_war_damage_inflicted_on_factions_begin),
		(val_sub, ":slot_war_damage_inflicted_on_b", kingdoms_begin),
		#(faction_get_slot, ":damage_inflicted_by_a", ":kingdom_a", ":slot_war_damage_inflicted_on_b"),
		(faction_set_slot, ":kingdom_a", ":slot_war_damage_inflicted_on_b", 0),
		(store_add, ":slot_war_damage_inflicted_on_a", ":kingdom_a", slot_faction_war_damage_inflicted_on_factions_begin),
		(val_sub, ":slot_war_damage_inflicted_on_a", kingdoms_begin),
		#(faction_get_slot, ":damage_inflicted_by_b", ":kingdom_b", ":slot_war_damage_inflicted_on_a"),
		(faction_set_slot, ":kingdom_b", ":slot_war_damage_inflicted_on_a", 0),
	  (try_end),
  ])
]
