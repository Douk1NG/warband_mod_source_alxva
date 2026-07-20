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

diplomacy_party_attacks_neutral_scripts = [
("diplomacy_party_attacks_neutral", #called from game_menus (plundering a village, raiding a village),  from dialogs: surprise attacking a neutral lord, any attack on caravan or villagers
#Has no effect if factions are already at war
    [
      (store_script_param, ":attacker_party", 1),
      (store_script_param, ":defender_party", 2),

	  (store_faction_of_party, ":attacker_faction", ":attacker_party"),
	  (store_faction_of_party, ":defender_faction", ":defender_party"),

	  (party_stack_get_troop_id, ":attacker_leader", ":attacker_party", 0),

	  (try_begin),
		(eq, ":attacker_party", "p_main_party"),
		(neq, ":attacker_faction", "fac_player_supporters_faction"),
		(assign, ":attacker_faction", "$players_kingdom"),
	  (else_try),
		(eq, ":attacker_party", "p_main_party"),
		(eq, ":attacker_faction", "fac_player_supporters_faction"),
	  (try_end),

	  (try_begin),
	    (eq, ":attacker_party", "p_main_party"),
		(store_relation, ":relation", ":attacker_faction", ":defender_faction"),
	    (ge, ":relation", 0),
		(call_script, "script_change_player_honor", -2),
	  (try_end),


	  (try_begin),
		(check_quest_active, "qst_cause_provocation"),
		(quest_slot_eq, "qst_cause_provocation", slot_quest_target_faction, ":defender_faction"),
		(quest_get_slot, ":giver_troop", "qst_cause_provocation", slot_quest_giver_troop),
		(store_faction_of_troop, ":attacker_faction", ":giver_troop"),
		(call_script, "script_succeed_quest", "qst_cause_provocation"),
	  (try_end),

	  (call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", ":attacker_faction", ":defender_faction"),
	  (assign, ":diplomatic_status", reg0),

	  (try_begin),
	    (eq, ":attacker_faction", "fac_player_supporters_faction"),
		(neg|faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
		#player faction inactive, no effect
	  (else_try),
		(eq, ":diplomatic_status", -2),
	    #war, no effect
	  (else_try),

	    (eq, ":attacker_faction", "fac_player_supporters_faction"),
		(faction_slot_eq, ":attacker_faction", slot_faction_leader, "trp_player"),
		(call_script, "script_faction_follows_controversial_policy", "fac_player_supporters_faction",logent_policy_ruler_attacks_without_provocation),
	  (else_try),
		(eq, ":diplomatic_status", 1),
		#truce
		(party_stack_get_troop_id, ":defender_party_leader", ":defender_party", 0),
		(try_begin),
			##diplomacy start+ add support for promoted kingdom ladies
			#(i.e. verify not a promoted kingdom lady, since they exist)
			(this_or_next|neg|is_between, ":defender_party_leader", kingdom_ladies_begin, kingdom_ladies_end),
				(neg|troop_slot_eq, ":defender_party_leader", slot_troop_occupation, slto_kingdom_hero),
			##diplomacy end+
			(neg|is_between, ":defender_party_leader", active_npcs_begin, active_npcs_end),
			(store_faction_of_party, ":defender_party_faction", ":defender_party"),
			(faction_get_slot, ":defender_party_leader", ":defender_party_faction", slot_faction_leader),
		(try_end),

		(call_script, "script_add_log_entry", logent_border_incident_troop_breaks_truce, ":attacker_leader", -1, ":defender_party_leader", ":attacker_faction"),
	  (else_try),
		#truce
		(call_script, "script_add_log_entry", logent_border_incident_troop_attacks_neutral, ":attacker_leader", -1, ":defender_party_leader", ":attacker_faction"),
	  (try_end),

	  (try_begin),
	    (is_between, ":defender_party", villages_begin, villages_end),
	    (call_script, "script_add_log_entry", logent_village_raided, ":attacker_leader",  ":defender_party", -1, ":defender_faction"),
        #SB : add quest cancellation when raiding villages
        (try_begin),
          (eq, ":attacker_party", "p_main_party"),
          (party_get_slot, ":elder", ":defender_party", slot_town_elder),
          (gt, ":elder", 0),
          (try_for_range, ":quest_no", village_elder_quests_begin, village_elder_quests_end),
            (quest_slot_eq, ":quest_no", slot_quest_giver_troop, ":elder"),
            (call_script, "script_abort_quest", ":quest_no", 1),
          (try_end),
        (try_end),
	  (else_try),
	    (party_get_template_id, ":template", ":defender_party"),
	    # (neq, ":template", "pt_kingdom_hero_party"),
	    (eq, ":template", "pt_kingdom_caravan_party"), #SB: fix this to specifically apply to caravans
		(try_begin),
			(ge, "$cheat_mode", 1),
			(str_store_faction_name, s5, ":defender_faction"),
			(display_message, "@{!}Debug - {s5} caravan attacked"),
		(try_end),

	    (call_script, "script_add_log_entry", logent_caravan_accosted, ":attacker_leader",  -1, -1, ":defender_faction"),
	  (try_end),

	  (store_add, ":slot_truce_days", ":attacker_faction", slot_faction_provocation_days_with_factions_begin),
	  (val_sub, ":slot_truce_days", kingdoms_begin),
	  (faction_set_slot, ":defender_faction", ":slot_truce_days", 0),

	  (store_add, ":slot_provocation_days", ":attacker_faction", slot_faction_provocation_days_with_factions_begin),
	  (val_sub, ":slot_provocation_days", kingdoms_begin),
	  (try_begin),
	    (neq, ":diplomatic_status", -2),
		(faction_slot_eq, ":defender_faction", ":slot_provocation_days", 0),
		(faction_set_slot, ":defender_faction", ":slot_provocation_days", 30),
	  (try_end),
	])
]
