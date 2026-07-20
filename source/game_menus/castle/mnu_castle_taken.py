# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

castle_taken_menu = [
(
    "castle_taken",mnf_disable_all_keys,
  ##diplomacy begin
    "{s3} has fallen to your troops, and you now have full control of the {reg2?town:castle}. You can plunder spoils of war worth {reg3} denars.\
{reg1? You may station troops here to defend it against enemies who may try to recapture it. Also, you should select now whether you will hold the {reg2?town:castle} yourself or give it to a faithful vassal...:}",# Only visible when castle is taken without being a vassal of a kingdom.
  ##diplomacy end
    "none",
    [
        (party_clear, "$g_encountered_party"),
        #SB : clear talk_context
        (try_begin),
          (eq, "$talk_context", tc_give_center_to_fief),
          (assign, "$talk_context", tc_town_talk),
        (try_end),
        ##diplomacy start+ Handle player is co-ruler of kingdom
        (assign, ":is_coruler", 0),
        (try_begin),
            (is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
            (call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
            (ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
            (assign, ":is_coruler", 1),
        (try_end),
        ##diplomacy end+
        (try_begin),
          ##diplomacy start+
          (this_or_next|eq, ":is_coruler", 1),
          ##diplomacy end+
          (eq, "$players_kingdom", "fac_player_supporters_faction"),
          (party_get_slot, ":new_owner", "$g_encountered_party", slot_town_lord),
          (neq, ":new_owner", "trp_player"),

          (try_for_range, ":unused", 0, 4),
            (call_script, "script_cf_reinforce_party", "$g_encountered_party"),
          (try_end),
        (try_end),

        (call_script, "script_lift_siege", "$g_encountered_party", 0),
        (assign, "$g_player_besiege_town", -1),

        (party_set_slot, "$g_encountered_party", slot_center_last_taken_by_troop, "trp_player"),
        ##diplomacy start+ Set last taken time
        (store_current_hours, ":cur_hours"),
        (party_set_slot, "$g_encountered_party", dplmc_slot_center_last_transfer_time, ":cur_hours"),
        ##diplomacy end+
        ##diplomacy begin
        #Reduce prosperity of the center by 5
        #(call_script, "script_change_center_prosperity", "$g_encountered_party", -5),
         (try_begin),
             (is_between, "$g_encountered_party", towns_begin, towns_end),
             (store_random_in_range, ":random", 4000, 10000),
         (else_try),
           (store_random_in_range, ":random", 1000, 8000),
         (try_end),
         (val_div, ":random", 100),
         (val_mul, ":random", 100),
         (assign, "$diplomacy_var", ":random"),
         # (assign, reg3, "$diplomacy_var"), #SB : move variable to last place
        ##diplomacy end

        (call_script, "script_change_troop_renown", "trp_player", 5),

        (assign, ":damage", 20),
        (try_begin),
            (is_between, "$g_encountered_party", towns_begin, towns_end),
            (assign, ":damage", 40),
        (try_end),
        (call_script, "script_faction_inflict_war_damage_on_faction", "$players_kingdom", "$g_encountered_party_faction", ":damage"),

        #removed, is it duplicate (useless)? See 20 lines above.
        #(call_script, "script_add_log_entry", logent_castle_captured_by_player, "trp_player", "$g_encountered_party", -1, "$g_encountered_party_faction"),

        (try_begin),
          (is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
          (neq, "$players_kingdom", "fac_player_supporters_faction"),
          (call_script, "script_give_center_to_faction", "$g_encountered_party", "$players_kingdom"),
          (call_script, "script_order_best_besieger_party_to_guard_center", "$g_encountered_party", "$players_kingdom"),
          (jump_to_menu, "mnu_castle_taken_2"),
        (else_try),
          (call_script, "script_give_center_to_faction", "$g_encountered_party", "fac_player_supporters_faction"),
          (call_script, "script_order_best_besieger_party_to_guard_center", "$g_encountered_party", "fac_player_supporters_faction"),
          (str_store_party_name, s3, "$g_encountered_party"),
          (assign, reg1, 0),
          (try_begin),
            (faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
            (assign, reg1, 1),
          (try_end),
        #(party_set_slot, "$g_encountered_party", slot_town_lord, stl_unassigned),
        (try_end),
        (assign, reg2, 0),
        (try_begin),
          (is_between, "$g_encountered_party", towns_begin, towns_end),
          (assign, reg2, 1),
        (try_end),
        (assign, reg3, "$diplomacy_var"), #SB : registers last
    ],
    [
##diplomacy begin
      ("dplmc_spoils_yourself",[],"Plunder it and keep the spoils all for yourself.",
       [
         #SB : spawn some looters
         (call_script, "script_spawn_looters", "$g_encountered_party", 4),
         (call_script, "script_change_center_prosperity", "$g_encountered_party", -8),
		 ##diplomacy start+
		 (assign, ":is_kingdom_leader", 0),
		 (try_begin),
			(is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
			(faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
			(ge, ":faction_leader", 0),
			(this_or_next|eq, ":faction_leader", "trp_player"),
			(this_or_next|troop_slot_eq, ":faction_leader", slot_troop_spouse, "trp_player"),
				(troop_slot_eq, "trp_player", slot_troop_spouse, ":faction_leader"),
			(assign, ":is_kingdom_leader", 1),
		 (else_try),
			(eq, "$players_kingdom", "fac_player_supporters_faction"),
			(assign, ":is_kingdom_leader", 1),
		 (try_end),
		 #Add support for promoted ladies
         #(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
         (try_for_range, ":troop_no", heroes_begin, heroes_end),
		 ##diplomacy end+
           (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
           (store_troop_faction, ":troop_faction_no", ":troop_no"),
		   ##diplomacy start+
		   (this_or_next|eq, "$players_kingdom", ":troop_faction_no"),
			  (eq, "fac_player_supporters_faction", ":troop_faction_no"),
		   (this_or_next|eq, ":is_kingdom_leader", 1),
		   ##diplomacy end+
           (eq, "fac_player_supporters_faction", ":troop_faction_no"),
           (call_script, "script_change_player_relation_with_troop", ":troop_no", -2),
         (try_end),
         (try_begin),
           (gt, "$g_player_chamberlain", 0),
           (call_script, "script_dplmc_pay_into_treasury", "$diplomacy_var"),
         (else_try),
           (troop_add_gold, "trp_player", "$diplomacy_var"),
         (try_end),
         (call_script, "script_change_player_honor", -3),
         (assign, "$auto_enter_town", "$g_encountered_party"),
         (change_screen_return),
        ]),
      ("dplmc_spoils_accompanying_vassals",
      [
		##nested diplomacy start+
		#Add support for being the ruler or co-ruler of an original kingdom
          (is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
		  (faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
		  (this_or_next|eq, ":faction_leader", "trp_player"),
		  (this_or_next|troop_slot_eq, ":faction_leader", slot_troop_spouse, "trp_player"),
  		##nested diplomacy end+
          (eq, "$players_kingdom", "fac_player_supporters_faction"),
          (assign, ":vassal_count", 0),
		##nested diplomacy start+ add support for kingdom ladies, and the other faction options
        # (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
		 (try_for_range, ":troop_no", heroes_begin, heroes_end),
  	    ##nested diplmacy end+
           (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
           (store_troop_faction, ":troop_faction_no", ":troop_no"),
		   ##nested diplomacy start+
		   (this_or_next|eq, "$players_kingdom", ":troop_faction_no"),
		   ##nested diplomacy end+
           (eq, "fac_player_supporters_faction", ":troop_faction_no"),
           (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
           (ge, ":party_no", 1),
           (store_distance_to_party_from_party, ":distance","p_main_party", ":party_no"),
           (le, ":distance", 25),
           (val_add, ":vassal_count", 1),
         (try_end),
		 (gt, ":vassal_count", 0),
      ],"Plunder it and share the spoils equally between the vassals accompanying you and yourself.",
       [
         (assign, ":vassal_count", 1),
		 ##nested diplomacy start+
		 ##OLD:
         #(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
         #  (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
         #  (store_troop_faction, ":troop_faction_no", ":troop_no"),
         #  (eq, "fac_player_supporters_faction", ":troop_faction_no"),
         #  (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
         #  (ge, ":party_no", 1),
         #  (store_distance_to_party_from_party, ":distance","p_main_party", ":party_no"),
         #  (le, ":distance", 25),
         #  (val_add, ":vassal_count", 1),
         #  (call_script, "script_change_player_relation_with_troop", ":troop_no", 3),
         #(try_end),
		 #
		 #NEW:
		 #first loop through to count
		 (try_for_range, ":troop_no", heroes_begin, heroes_end),#promoted lady support
			(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
			(store_troop_faction, ":troop_faction_no", ":troop_no"),
			(this_or_next|eq, "$players_kingdom", ":troop_faction_no"),#support for other faction arrangements
				(eq, "fac_player_supporters_faction", ":troop_faction_no"),
			(troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
			(ge, ":party_no", 1),
			(store_distance_to_party_from_party, ":distance","p_main_party", ":party_no"),
			(le, ":distance", 25),
			(val_add, ":vassal_count", 1),
		 (try_end),
		 (store_div, ":gold_per_lord", "$diplomacy_var", ":vassal_count"),
		 #now loop through to add gold/relation
		 (try_for_range, ":troop_no", heroes_begin, heroes_end),#promoted lady support
			(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
			(store_troop_faction, ":troop_faction_no", ":troop_no"),
			(this_or_next|eq, "$players_kingdom", ":troop_faction_no"),#support for other faction arrangements
				(eq, "fac_player_supporters_faction", ":troop_faction_no"),
			(troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
			(ge, ":party_no", 1),
			(store_distance_to_party_from_party, ":distance","p_main_party", ":party_no"),
			(le, ":distance", 25),
			#add gold
			(call_script, "script_dplmc_distribute_gold_to_lord_and_holdings", ":gold_per_lord", ":troop_no"),
			#Relation adjustment
			(store_random_in_range, reg0, 0, 1000),
			(val_add, reg0, ":gold_per_lord"),
			(val_div, reg0, 1000),
			(gt, reg0, 0),
			(val_min, reg0, 4),
			(assign, ":relation_change", reg0),
			#Modify for personality
			(try_begin),
				#Lords who dislike raiding will be displeased by looting a town (but not a castle)
				(party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
				(call_script, "script_dplmc_get_troop_morality_value", ":troop_no", tmt_humanitarian),
				(try_begin),
					(gt, reg0, 0),#Some lords like raiding settlements less than others
					(val_sub, ":relation_change", reg0),
					(val_min, ":relation_change", -1),
				(else_try),
					(lt, reg0, 0),#Some lords like raiding settlements more than others
					(val_sub, ":relation_change", reg0),
					(val_min, ":relation_change", 5),
				(else_try),
					(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_custodian),
					(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_benefactor),
						(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_moralist),
					(val_sub, ":relation_change", 1),
			    (try_end),
			(try_end),
			(call_script, "script_change_player_relation_with_troop", ":troop_no", ":relation_change"),
		 (try_end),
		 ##nested diplomacy end+
         # (store_random_in_range, ":num_looters", 0, ":vassal_count"),
         # (val_max, ":num_looters", 3),
         (call_script, "script_spawn_looters", "$g_encountered_party", 5), #SB : spawn some looters
         (val_div, "$diplomacy_var", ":vassal_count"),
         (try_begin),
           (gt, "$g_player_chamberlain", 0),
           (call_script, "script_dplmc_pay_into_treasury", "$diplomacy_var"),
         (else_try),
           (troop_add_gold, "trp_player", "$diplomacy_var"),
         (try_end),
         (call_script, "script_change_center_prosperity", "$g_encountered_party", -8),
         (call_script, "script_change_player_honor", -1),
         (assign, "$auto_enter_town", "$g_encountered_party"),
         (change_screen_return),
        ]),
      ("dplmc_spoils_all_vassals",
        [
          (is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
          ##nested diplomacy start+
          #Support for being co-ruler of an original kingdom
          (faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
          (this_or_next|eq, ":faction_leader", "trp_player"),
          (this_or_next|troop_slot_eq, ":faction_leader", slot_troop_spouse, "trp_player"),
          ##nested diplomacy end+
          (eq, "$players_kingdom", "fac_player_supporters_faction"),
          #SB : check if we even have any vassals
          (assign, ":end", heroes_end),
          (try_for_range, ":troop_no", heroes_begin, ":end"),
            (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
            (store_troop_faction, ":troop_faction_no", ":troop_no"),
            (this_or_next|eq, ":troop_faction_no", "fac_player_supporters_faction"),
            (eq, ":troop_faction_no", "$players_kingdom"),
            (assign, ":end", heroes_begin),
          (try_end),
          (eq, ":end", heroes_begin),

      ],"Plunder it and share the spoils equally between your vassals and yourself.",
       [
         (assign, ":vassal_count", 1),
		 ##nested diplomacy start+
		 #OLD:
         #(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
         #  (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
         #  (store_troop_faction, ":troop_faction_no", ":troop_no"),
         #  (eq, "fac_player_supporters_faction", ":troop_faction_no"),
         #  (val_add, ":vassal_count", 1),
         #  (call_script, "script_change_player_relation_with_troop", ":troop_no", 2),
         #(try_end),
		 #
		 #NEW:
		 #  1. Actually give the gold to your vassals;
		 #  2. Support kingdom ladies as vassals
		 #  3. Support being the ruler or co-ruler of an original kingdom
		 #  4. The relationship gain should not exceed 1 per 1000 gold pieces.
		 (try_for_range, ":troop_no", heroes_begin, heroes_end),
			(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
			(store_troop_faction, ":troop_faction_no", ":troop_no"),
			(this_or_next|eq, ":troop_faction_no", "fac_player_supporters_faction"),
				(eq, ":troop_faction_no", "$players_kingdom"),
			(val_add, ":vassal_count", 1),
		 (try_end),

		 (store_div, ":gold_per_lord", "$diplomacy_var", ":vassal_count"),
		 (try_for_range, ":troop_no", heroes_begin, heroes_end),
			(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
			(store_troop_faction, ":troop_faction_no", ":troop_no"),
			(this_or_next|eq, ":troop_faction_no", "fac_player_supporters_faction"),
				(eq, ":troop_faction_no", "$players_kingdom"),
			(call_script, "script_dplmc_distribute_gold_to_lord_and_holdings", ":gold_per_lord", ":troop_no"),
			#Relation adjustment
			(store_random_in_range, reg0, 0, 1000),
			(val_add, reg0, ":gold_per_lord"),
			(val_div, reg0, 1000),
			(gt, reg0, 0),
			(val_min, reg0, 3),
			(assign, ":relation_change", reg0),
			#Modify for personality
			(try_begin),
				#Lords who dislike raiding will be displeased by looting a town (but not a castle)
				(party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
				(call_script, "script_dplmc_get_troop_morality_value", ":troop_no", tmt_humanitarian),
				(try_begin),
					(gt, reg0, 0),#Some lords like raiding settlements less than others
					(val_sub, ":relation_change", reg0),
					(val_min, ":relation_change", -1),
				(else_try),
					(lt, reg0, 0),#Some lords like raiding settlements more than others
					(val_sub, ":relation_change", reg0),
					(val_min, ":relation_change", 4),
				(else_try),
					(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_custodian),
					(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_benefactor),
						(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_moralist),
					(val_sub, ":relation_change", 1),
			    (try_end),
			(call_script, "script_change_player_relation_with_troop", ":troop_no", ":relation_change"),
 		    (try_end),
		 (try_end),
		 ##nested diplomacy end+
         (call_script, "script_spawn_looters", "$g_encountered_party", 4), #SB : spawn some looters
         (val_div, "$diplomacy_var", ":vassal_count"),
         (try_begin),
           (gt, "$g_player_chamberlain", 0),
           (call_script, "script_dplmc_pay_into_treasury", "$diplomacy_var"),
         (else_try),
           (troop_add_gold, "trp_player", "$diplomacy_var"),
         (try_end),
         (call_script, "script_change_center_prosperity", "$g_encountered_party", -8),
         (assign, "$auto_enter_town", "$g_encountered_party"),
         (change_screen_return),
        ]),
##diplomacy end
      ("continue",[],"Continue...",
       [
         ##diplomacy begin
         (call_script, "script_change_center_prosperity", "$g_encountered_party", -3),
         ##diplomacy end
         (assign, "$auto_enter_town", "$g_encountered_party"),
         (change_screen_return),
        ]),
    ],
  )
]
