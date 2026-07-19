# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

castle_menus = [
  (
    "castle_outside",mnf_scale_picture,
    "You are outside {s2}.{s11} {s3} {s4}",
    "none",
    [
        (assign, "$g_enemy_party", "$g_encountered_party"),
        (assign, "$g_ally_party", -1),
        (str_store_party_name, s2,"$g_encountered_party"),
        (call_script, "script_encounter_calculate_fit"),
        (assign,"$all_doors_locked",1),
        (assign, "$current_town","$g_encountered_party"),

        (try_begin),
          (eq, "$new_encounter", 1),
          (assign, "$new_encounter", 0),
          (call_script, "script_let_nearby_parties_join_current_battle", 1, 0),
		  ###diplomacy start+
		  ##If terrain advantage is on, use siege settings for estimating strength
          #(assign, ":save_dplmc_terrain_advantage", "$g_dplmc_terrain_advantage"),
		  #(try_begin),
		  #   (eq, "$g_dplmc_terrain_advantage", TERRAIN_ADVANTAGE_ENABLE),
		  #   (assign, "$g_dplmc_terrain_advantage", TERRAIN_ADVANTAGE_FORCE_SIEGE),
		  #(try_end),
		  ###diplomacy end+
          (call_script, "script_encounter_init_variables"),
		  ###diplomacy start+
		  ##Revert terrain advantage settings
		  #(assign, "$g_dplmc_terrain_advantage", ":save_dplmc_terrain_advantage"),
		  ###diplomacy end+
          (assign, "$entry_to_town_forbidden",0),

         (try_begin),         #dckplmc: handle removing disguise here, bug with saving in-mission
             (gt, "$sneaked_into_town", disguise_none),
             (display_message, "@Removing disguise...", message_alert), #SB : colorize
             (try_begin),
               (eq, "$g_dplmc_player_disguise", 1),
               (set_show_messages, 0),
               #equipment is deposited back to inventory, it starts off blank
               (try_for_range, ":i_slot", ek_item_0, ek_food + 1),
                 (troop_get_inventory_slot, ":item", "trp_player", ":i_slot"),
                 (neq, ":item", -1),
                 (troop_get_inventory_slot_modifier, ":imod", "trp_player", ":i_slot"),
                 (troop_add_item, "trp_random_town_sequence", ":item", ":imod"),
               (try_end),
               #less efficient, but merge and respect original player inventory's order
               (call_script, "script_move_inventory_and_gold", "trp_player", "trp_random_town_sequence", 0), #do not move gold
               (call_script, "script_dplmc_copy_inventory", "trp_random_town_sequence", "trp_player"),
               (call_script, "script_troop_transfer_gold", "trp_random_town_sequence", "trp_player", 0), #move remaining gold now
               (set_show_messages, 1),
             (try_end),
             (assign, "$sneaked_into_town", disguise_none),
          (try_end),

          (assign, "$sneaked_into_town", disguise_none),
          (assign, "$town_entered", 0),
#          (assign, "$waiting_for_arena_fight_result", 0),
          (assign, "$encountered_party_hostile", 0),
          (assign, "$encountered_party_friendly", 0),
          (try_begin),
            (gt, "$g_player_besiege_town", 0),
            (neq,"$g_player_besiege_town","$g_encountered_party"),
            (party_slot_eq, "$g_player_besiege_town", slot_center_is_besieged_by, "p_main_party"),
            (call_script, "script_lift_siege", "$g_player_besiege_town", 0),
            (assign,"$g_player_besiege_town",-1),
          (try_end),
          (try_begin),
            (lt, "$g_encountered_party_relation", 0),
            (assign, "$encountered_party_hostile", 1),
            (assign,"$entry_to_town_forbidden",1),
          (try_end),

          ##diplomacy begin
          (try_begin),
            (party_slot_eq, "$g_encountered_party", slot_village_infested_by_bandits, "trp_peasant_woman"),
            (assign, "$encountered_party_hostile", 1),
            (assign,"$entry_to_town_forbidden",1),
          (try_end),
          ##diplomacy end

          (assign,"$cant_sneak_into_town",0),
          (try_begin),
            (eq,"$current_town","$last_sneak_attempt_town"),
            (store_current_hours,reg(2)),
            (val_sub,reg(2),"$last_sneak_attempt_time"),
            (lt,reg(2),12),
            (assign,"$cant_sneak_into_town",1),
          (try_end),
        (else_try), #second or more turn
          (eq, "$g_leave_encounter",1),
          (change_screen_return),
        (try_end),

        (str_clear,s4),
        (try_begin),
          (eq,"$entry_to_town_forbidden",1),
          (try_begin),
            (eq,"$cant_sneak_into_town",1),
            (str_store_string,s4,"str_sneaking_to_town_impossible"),
          (else_try),
            (str_store_string,s4,"str_entrance_to_town_forbidden"),
          (try_end),
        (try_end),

        (party_get_slot, ":center_lord", "$current_town", slot_town_lord),
        (store_faction_of_party, ":center_faction", "$current_town"),
        (str_store_faction_name,s9,":center_faction"),
        (try_begin),
          (ge, ":center_lord", 0),
          (str_store_troop_name,s8,":center_lord"),
          (str_store_string,s7,"@{s8} of {s9}"),
        (try_end),
        ##diplomacy start+

        #SB : move coruler variable up here
		(assign, ":is_coruler", 0),
		(try_begin),
			(eq, "$g_encountered_party_faction", "$players_kingdom"),
			(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
			(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
			(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
			(assign, ":is_coruler", 1),
		(try_end),
		(assign, ":save_reg0", reg0),#save variables
		(assign, ":save_reg4", reg4),
		(assign, ":relation", 0),
		(assign, reg4, 0),
		(try_begin),#If there's a relation of some kind, write it to s11 (which we'll overwrite below)
			(lt, ":center_lord", 1),
		(else_try),
			#your relative
			(call_script, "script_troop_get_family_relation_to_troop", ":center_lord", "trp_player"),#outputs to s11, ":relation", and reg4
			(ge, ":relation", 1),#Fall through if this not a relative
		(else_try),
			#your current liege
			(eq, ":center_faction", "$players_kingdom"),
			(is_between, ":center_faction", kingdoms_begin, kingdoms_end),#include fac_player_supporters_faction for claimant quest
			(faction_slot_eq, ":center_faction", slot_faction_leader, ":center_lord"),
			(str_store_string, s11, "@liege"),
			(assign, ":relation", 1),
		(else_try),
			#your former liege if you renounced a kingdom
			(eq, ":center_faction", "$players_oath_renounced_against_kingdom"),
			(is_between, ":center_faction", npc_kingdoms_begin, npc_kingdoms_end),
			(faction_slot_eq, ":center_faction", slot_faction_leader, ":center_lord"),
			(str_store_string, s11, "@former liege"),
			(assign, ":relation", 1),
		(else_try),
			#stop here for lords you haven't met, or non-hero troops
			(this_or_next|neg|troop_is_hero, ":center_lord"),
			(troop_slot_eq, ":center_lord", slot_troop_met, 0),
		(else_try),
			#check for affiliates
			(call_script, "script_dplmc_is_affiliated_family_member", ":center_lord"),
			(ge, reg0, 1), #SB : substitute register
			(assign, ":relation", 1),
			(try_begin),
				(ge, "$g_encountered_party_relation", 0),#don't say "ally" when you might fight them, as that's confusing
				(str_store_string, s11, "str_dplmc_ally"),
			(else_try),
				(str_store_string, s11, "@affiliate"),
			(try_end),
		(else_try),
			#check for friends (former companions)
			(call_script, "script_troop_get_player_relation", ":center_lord"),
            (assign, ":relation", reg0),
			(is_between, ":center_lord", companions_begin, companions_end),
			(neg|troop_slot_eq, ":center_lord", slot_troop_playerparty_history, dplmc_pp_history_nonplayer_entry),
			(try_begin),
			   (ge, "$g_encountered_party_relation", 0),#don't say "ally" when you might fight them, as that's confusing
			   (ge, ":relation", 50),
			   (str_store_string, s11, "str_dplmc_ally"),
			(else_try),
				(ge, "$g_encountered_party_relation", 0),
				(ge, ":relation", 20),
				(str_store_string, s11, "str_dplmc_friend"),
			(else_try),
				(str_store_string, s11, "@former companion"),
			(try_end),
			(assign, ":relation", 1),
		(else_try),
			#don't print "friend" if you might fight them
			(lt, "$g_encountered_party_relation", 0),
			(assign, ":relation", 0),
		(else_try),
			#check for friends
			# (val_div, ":relation", 50),#right now ":relation" holds the relation with the player
			(ge, ":relation", 50),
			(str_store_string, s11, "str_dplmc_friend"),
		(else_try),
			#check for marshall
			(eq, ":center_faction", "$players_kingdom"),
			(faction_slot_eq, ":center_faction", slot_faction_marshall, ":center_lord"),
			(str_store_string, s11, "@marshall"),
		(else_try), #SB : coruler check above
			# #check for vassal of player if nothing else to say
			# (call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", ":center_faction"),
			# (val_add, ":relation", 1),
			# (val_sub, ":relation", DPLMC_FACTION_STANDING_LEADER_SPOUSE),
			(ge, ":is_coruler", 1),
			(str_store_string, s11, "@vassal"),
            (assign, ":relation", 1),
		(else_try),
			(assign, ":relation", 0),
		(try_end),
		##diplomacy end+
        (try_begin), # same mnu_town
          (party_slot_eq,"$current_town",slot_party_type, spt_castle),
          (try_begin),
            (eq, ":center_lord", "trp_player"),
            (str_store_string,s11,"@ Your own banner flies over the castle gate."),
		  ##diplomacy start+ If ":relation" > 0, a relation string was written to {s11} above
		  (else_try),
			(ge, ":relation", 1),
			(str_store_string, s11, "@ You see the banner of your {s11} {s7} over the castle gate."),
		  ##diplomacy end+
          (else_try),
            (ge, ":center_lord", 0),
            (str_store_string, s11,"@ You see the banner of {s7} over the castle gate."),
          (else_try),
		    (is_between, ":center_faction", kingdoms_begin, kingdoms_end),
            (str_store_string, s11,"str__this_castle_is_temporarily_under_royal_control"),
		  (else_try),
            (str_store_string, s11,"str__this_castle_does_not_seem_to_be_under_anyones_control"),
          (try_end),
        (else_try),
          (try_begin),
            (eq, ":center_lord", "trp_player"),
            (str_store_string, s11,"@ Your own banner flies over the town gates."),
		  ##diplomacy start+ If ":relation" > 0, a relation string was written to {s11} above
		  (else_try),
			(ge, ":relation", 1),
			(str_store_string, s11, "@ You see the banner of your {s11} {s7} over the town gates."),
		  ##diplomacy end+
          (else_try),
            (ge, ":center_lord", 0),
            (str_store_string, s11,"@ You see the banner of {s7} over the town gates."),
          (else_try),
		    (is_between, ":center_faction", kingdoms_begin, kingdoms_end),
            (str_store_string, s11,"str__this_town_is_temporarily_under_royal_control"),
		  (else_try),
            (str_store_string, s11,"str__the_townspeople_seem_to_have_declared_their_independence"),
          (try_end),
        (try_end),

        #SB : get rid of register usage
        (party_get_num_companions, ":num_enemies", "p_collective_enemy"),
        (assign,"$castle_undefended",0),
        (str_clear, s3),
        (try_begin),
          (eq, ":num_enemies", 0),
          (assign,"$castle_undefended",1),
#          (party_set_faction,"$g_encountered_party","fac_neutral"),
#          (party_set_slot, "$g_encountered_party", slot_town_lord, stl_unassigned),
          (str_store_string, s3, "str_castle_is_abondened"),
        (else_try),
        ##diplomacy begin
          (party_slot_eq, "$g_encountered_party", slot_village_infested_by_bandits, "trp_peasant_woman"),
          (str_store_string, s3, "str_dplmc_place_is_occupied_by_insurgents"),
          #SB : assign globals, doesn't make senes
        (else_try),
        ##diplomacy end
		##diplomacy start+ Handle player is co-ruler of kingdom
		  (this_or_next|eq, ":is_coruler", 1),
		##diplomacy end+
          (eq,"$g_encountered_party_faction","fac_player_supporters_faction"),
          (str_store_string, s3, "str_place_is_occupied_by_player"),
        (else_try),
          (lt, "$g_encountered_party_relation", 0),
          (str_store_string, s3, "str_place_is_occupied_by_enemy"),
        (else_try),
#          (str_store_string, s3, "str_place_is_occupied_by_friendly"),
        (try_end),
		##diplomacy start+
		(assign, reg0, ":save_reg0"),#revert variables
		(assign, reg4, ":save_reg4"),
		##diplomacy end+

        (try_begin),
          (eq, "$g_leave_town_outside",1),
          (assign, "$g_leave_town_outside",0),
          (assign, "$g_permitted_to_center", 0),
          (change_screen_return),
        (else_try),
          (check_quest_active, "qst_escort_lady"),
          (quest_slot_eq, "qst_escort_lady", slot_quest_target_center, "$g_encountered_party"),
          (quest_get_slot, ":quest_object_troop", "qst_escort_lady", slot_quest_object_troop),
          # (call_script, "script_get_meeting_scene"), (assign, ":meeting_scene", reg0),
          # (modify_visitors_at_site,":meeting_scene"),
          # (reset_visitors),
          # (set_visitor,0, "trp_player"),
          # (set_visitor,17, ":quest_object_troop"),
          # (set_jump_mission, "mt_conversation_encounter"),
          # (jump_to_scene, ":meeting_scene"),
          (assign, "$talk_context", tc_entering_center_quest_talk),
          # (change_screen_map_conversation, ":quest_object_troop"),
          (call_script, "script_setup_troop_meeting", ":quest_object_troop", -1),
        (else_try),
          (check_quest_active, "qst_kidnapped_girl"),
          (quest_slot_eq, "qst_kidnapped_girl", slot_quest_giver_center, "$g_encountered_party"),
          (quest_slot_eq, "qst_kidnapped_girl", slot_quest_current_state, 3),
          # (call_script, "script_get_meeting_scene"), (assign, ":meeting_scene", reg0),
          # (modify_visitors_at_site,":meeting_scene"),
          # (reset_visitors),
          # (set_visitor,0, "trp_player"),
          # (set_visitor,17, "trp_kidnapped_girl"),
          # (set_jump_mission, "mt_conversation_encounter"),
          # (jump_to_scene, ":meeting_scene"),
          (assign, "$talk_context", tc_entering_center_quest_talk),
          # (change_screen_map_conversation, "trp_kidnapped_girl"),
          (call_script, "script_setup_troop_meeting", "trp_kidnapped_girl", -1),
        (else_try), #SB : automatically talk to caravans
          (check_quest_active, "qst_escort_merchant_caravan"),
          (quest_get_slot, ":quest_target_party", "qst_escort_merchant_caravan", slot_quest_target_party),
          (party_is_active, ":quest_target_party"),
          (quest_get_slot, ":quest_target_center", "qst_escort_merchant_caravan", slot_quest_target_center),
          (eq,"$current_town",":quest_target_center"),
          (quest_slot_eq, "qst_escort_merchant_caravan", slot_quest_current_state, 1),
          (store_distance_to_party_from_party, ":dist", ":quest_target_center",":quest_target_party"),
          (lt,":dist",4),
          # (start_encounter, ":quest_target_party"),
          (assign, "$talk_context", tc_party_encounter),
          (assign, "$g_encountered_party", ":quest_target_party"),
          (party_stack_get_troop_id, ":caravan_leader", ":quest_target_party", 0),
          (party_stack_get_troop_dna, ":caravan_leader_dna", ":quest_target_party", 0),
          (call_script, "script_setup_troop_meeting", ":caravan_leader", ":caravan_leader_dna"),
        (else_try), #SB : should really merge these quests, this is for older savegames
          (eq, "$caravan_escort_state",1),
          (party_is_active, "$caravan_escort_party_id"),
          (eq,"$current_town","$caravan_escort_destination_town"),
          (store_distance_to_party_from_party, ":dist", "$caravan_escort_destination_town", "$caravan_escort_party_id"),
          (lt,":dist", 5),
          # (store_distance_to_party_from_party, ":caravan_distance_to_player","p_main_party","$caravan_escort_party_id"),
          # (lt, ":caravan_distance_to_player", 5),
          # (start_encounter, "$caravan_escorted_party_id"),

          (assign, "$talk_context", tc_party_encounter),
          (assign, "$g_encountered_party", "$caravan_escort_party_id"),
          (party_stack_get_troop_id, ":caravan_leader", "$caravan_escort_party_id", 0),
          (party_stack_get_troop_dna, ":caravan_leader_dna", "$caravan_escort_party_id", 0),
          (call_script, "script_setup_troop_meeting", ":caravan_leader", ":caravan_leader_dna"),
          # (start_map_conversation, ":caravan_leader", ":caravan_leader_dna"),

##        (else_try),
##          (gt, "$lord_requested_to_talk_to", 0),
##          (store_current_hours, ":cur_hours"),
##          (neq, ":cur_hours", "$quest_given_time"),
##          (modify_visitors_at_site,"scn_conversation_scene"),
##          (reset_visitors),
##          (assign, ":cur_lord", "$lord_requested_to_talk_to"),
##          (assign, "$lord_requested_to_talk_to", 0),
##          (set_visitor,0,"trp_player"),
##          (set_visitor,17,":cur_lord"),
##          (set_jump_mission,"mt_conversation_encounter"),
##          (jump_to_scene,"scn_conversation_scene"),
##          (assign, "$talk_context", tc_castle_gate_lord),
##          (change_screen_map_conversation, ":cur_lord"),
        (else_try),
          (eq, "$g_town_visit_after_rest", 1),
          (assign, "$g_town_visit_after_rest", 0),
          (jump_to_menu,"mnu_town"),
        ##diplomacy begin
        (else_try),
          (party_slot_eq, "$g_encountered_party", slot_village_infested_by_bandits, "trp_peasant_woman"),
          (try_begin),
            (eq, "$g_player_besiege_town", "$g_encountered_party"),
            (jump_to_menu, "mnu_castle_besiege"),
          (try_end),
        ##diplomacy end
        (else_try),
          (party_slot_eq, "$g_encountered_party", slot_party_type, spt_castle),
		  ##diplomacy start+ Handle player is co-ruler of kingdom
		  (assign, ":is_coruler",0),
	  	  (try_begin),
			(eq, "$g_encountered_party_faction", "$players_kingdom"),
			(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
			(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
			(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
			(assign, ":is_coruler", 1),
		  (try_end),
		  (this_or_next|eq, ":is_coruler", 1),
		  ##diplomacy end+
          (this_or_next|party_slot_eq, "$g_encountered_party", slot_town_lord, "trp_player"),
          (faction_slot_eq, "$g_encountered_party_faction", slot_faction_leader, "trp_player"),
          (jump_to_menu, "mnu_enter_your_own_castle"),
        (else_try),
          (party_slot_eq,"$g_encountered_party", slot_party_type,spt_castle),
          (ge, "$g_encountered_party_relation", 0),
          (this_or_next|eq,"$castle_undefended", 1),
          (this_or_next|eq, "$g_permitted_to_center", 1),
          (eq, "$g_encountered_party_faction", "$players_kingdom"),
          (jump_to_menu, "mnu_town"),
        (else_try),
          (party_slot_eq,"$g_encountered_party", slot_party_type,spt_town),
          (ge, "$g_encountered_party_relation", 0),
          (jump_to_menu, "mnu_town"),
        (else_try),
          (eq, "$g_player_besiege_town", "$g_encountered_party"),
          (jump_to_menu, "mnu_castle_besiege"),
        (try_end),

          ##diplomacy begin
          (try_begin),
            (party_slot_eq, "$g_encountered_party", slot_village_infested_by_bandits, "trp_peasant_woman"),
            (set_background_mesh, "mesh_pic_townriot"),
          (else_try),
          ##diplomacy end
            (call_script, "script_set_town_picture"),
          ##diplomacy begin
          (try_end),
          ##diplomacy end
        ],
    [
#        ("talk_to_castle_commander",[
#            (party_get_num_companions, ":no_companions", "$g_encountered_party"),
#            (ge, ":no_companions", 1),
#            (eq,"$ruler_meeting_denied",0), #this variable is removed
#            ],
#         "Request a meeting with the lord of the castle.",[
#             (modify_visitors_at_site,"scn_conversation_scene"),(reset_visitors),
#             (set_visitor,0,"trp_player"),
#             (party_stack_get_troop_id, reg(6),"$g_encountered_party",0),
#             (party_stack_get_troop_dna,reg(7),"$g_encountered_party",0),
#             (set_visitor,17,reg(6),reg(7)),
#             (set_jump_mission,"mt_conversation_encounter"),
#             (jump_to_scene,"scn_conversation_scene"),
#             (assign, "$talk_context", tc_castle_commander),
#             (change_screen_map_conversation, reg(6))
#             ]),
      ("approach_gates",[(this_or_next|eq,"$entry_to_town_forbidden",1),
      (try_begin),
        (party_get_slot, ":center_lord", "$current_town", slot_town_lord),
        (ge, ":center_lord", 0),
        (set_fixed_point_multiplier, 100),
        (position_set_x, pos1, 70),
        (position_set_y, pos1, 5),
        (position_set_z, pos1, 75),
        (set_game_menu_tableau_mesh, "tableau_troop_note_mesh", ":center_lord", pos1),
        (try_end),
                          (party_slot_eq,"$g_encountered_party", slot_party_type,spt_castle),
                          #SB : not infested by peasants, they'd just kick you out
                          (neg|party_slot_eq, "$g_encountered_party", slot_village_infested_by_bandits, "trp_peasant_woman"),
                          ],
       "Approach the gates and hail the guard.",[
                                                  (jump_to_menu, "mnu_castle_guard"),
##                                                   (modify_visitors_at_site,"scn_conversation_scene"),(reset_visitors),
##                                                   (set_visitor,0,"trp_player"),
##                                                   (store_faction_of_party, ":cur_faction", "$g_encountered_party"),
##                                                   (faction_get_slot, ":cur_guard", ":cur_faction", slot_faction_guard_troop),
##                                                   (set_visitor,17,":cur_guard"),
##                                                   (set_jump_mission,"mt_conversation_encounter"),
##                                                   (jump_to_scene,"scn_conversation_scene"),
##                                                   (assign, "$talk_context", tc_castle_gate),
##                                                   (change_screen_map_conversation, ":cur_guard")
                                                   ]),

      ("town_sneak",
        [
          (try_begin),
            (party_slot_eq, "$g_encountered_party", slot_party_type,spt_town),
            (str_store_string, s7, "str_town"),
          (else_try),
            (str_store_string, s7, "str_castle"),
          (try_end),

          (eq, "$entry_to_town_forbidden", 1),
          (eq, "$cant_sneak_into_town", 0),
          #SB : do not let player in at all, because the garrison can be managed
          (neg|party_slot_eq, "$g_encountered_party", slot_village_infested_by_bandits, "trp_peasant_woman"),
        ],
       "Disguise yourself and try to sneak into the {s7}",
       [

         #SB : apply different disguises in new system, with outcomes
        (try_begin),
          (eq, "$g_dplmc_player_disguise", 1),
          (troop_get_slot, ":player_disguise", "trp_player", slot_troop_player_disguise_sets),
          (val_max, ":player_disguise", disguise_pilgrim),
          (troop_set_slot, "trp_player", slot_troop_player_disguise_sets, ":player_disguise"),
          # (assign, "$sneaked_into_town", disguise_none), #set no disguise
          (troop_clear_inventory, "trp_random_town_sequence"), # clear items to bring

          (try_for_range, ":i_slot", 0, ek_food + 1), #dckplmc: bugfix - clear equipped items
            (troop_set_inventory_slot, "trp_random_town_sequence", ":i_slot", -1),
          (try_end),

          (store_troop_gold, ":cur_amount", "trp_random_town_sequence"),
          (troop_remove_gold, "trp_random_town_sequence", ":cur_amount"),#clear gold
          (assign, "$temp", 0),
          (jump_to_menu, "mnu_dplmc_choose_disguise"),
        (else_try),
          (faction_get_slot, ":player_alarm", "$g_encountered_party_faction", slot_faction_player_alarm),
          (party_get_num_companions, ":num_men", "p_main_party"),
          (party_get_num_prisoners, ":num_prisoners", "p_main_party"),
          (val_add, ":num_men", ":num_prisoners"),
          (val_mul, ":num_men", 2),
          (val_div, ":num_men", 3),
          (store_add, ":get_caught_chance", ":player_alarm", ":num_men"),
          (store_random_in_range, ":random_chance", 0, 100),
          (try_begin),
            (this_or_next|ge, "$cheat_mode", 1),
            (this_or_next|ge, ":random_chance", ":get_caught_chance"),
            (eq, "$g_last_defeated_bandits_town", "$g_encountered_party"),
            (assign, "$g_last_defeated_bandits_town", 0),
            (assign, "$sneaked_into_town", disguise_pilgrim),
            (assign, "$town_entered", 1),
            (jump_to_menu,"mnu_sneak_into_town_suceeded"),
            (assign, "$g_mt_mode", tcm_disguised),
          (else_try),
            (jump_to_menu,"mnu_sneak_into_town_caught"),
          (try_end),
        (try_end),
        ]),
      ##diplomacy begin
      ("dplmc_riot_start_siege",
       [
           (party_slot_eq, "$g_encountered_party", slot_center_is_besieged_by, -1),
           (party_slot_eq, "$g_encountered_party", slot_village_infested_by_bandits, "trp_peasant_woman"),
           (lt, "$g_encountered_party_2", 1),
           (call_script, "script_party_count_fit_for_battle","p_main_party"),
           (gt, reg0, 5),
           (try_begin),
             (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
             (assign, reg6, 1),
           (else_try),
             (assign, reg6, 0),
           (try_end),
           ],
       "Besiege the {reg6?town:castle} to counter the insurgency.",
       [
         (assign,"$g_player_besiege_town","$g_encountered_party"),
         (jump_to_menu, "mnu_castle_besiege"),
         ]),
       ("dplmc_riot_negotiate",
       [
           (party_slot_eq, "$g_encountered_party", slot_center_is_besieged_by, -1),
           (party_slot_eq, "$g_encountered_party", slot_village_infested_by_bandits, "trp_peasant_woman"),
           (lt, "$g_encountered_party_2", 1),
           (call_script, "script_party_count_fit_for_battle","p_main_party"),
           (gt, reg0, 5),
           (try_begin),
             (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
             (assign, reg6, 1),
           (else_try),
             (assign, reg6, 0),
           (try_end),
           ],
       "Begin negotiations.",
       [
          (jump_to_menu, "mnu_dplmc_riot_negotiate"),
        ]),

     ##diplomacy end
      ("castle_start_siege",
       [
           ##diplomacy begin
           (neg|party_slot_eq, "$g_encountered_party", slot_village_infested_by_bandits, "trp_peasant_woman"),
           ##diplomacy end
           (this_or_next|party_slot_eq, "$g_encountered_party", slot_center_is_besieged_by, -1),
           (             party_slot_eq, "$g_encountered_party", slot_center_is_besieged_by, "p_main_party"),
           (store_relation, ":reln", "$g_encountered_party_faction", "fac_player_supporters_faction"),
           (lt, ":reln", 0),
           (lt, "$g_encountered_party_2", 1),
           (call_script, "script_party_count_fit_for_battle","p_main_party"),
           (gt, reg(0), 5),
           (try_begin),
             (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
             (assign, reg6, 1),
           (else_try),
             (assign, reg6, 0),
           (try_end),
           ],
       "Besiege the {reg6?town:castle}.",
       [
         (assign,"$g_player_besiege_town","$g_encountered_party"),
         (store_relation, ":relation", "fac_player_supporters_faction", "$g_encountered_party_faction"),
         (val_min, ":relation", -40),
         (call_script, "script_set_player_relation_with_faction", "$g_encountered_party_faction", ":relation"),
         (call_script, "script_update_all_notes"),
         (jump_to_menu, "mnu_castle_besiege"),
         ]),

      ("cheat_castle_start_siege",
       [
         (eq, "$cheat_mode", 1),
         (this_or_next|party_slot_eq, "$g_encountered_party", slot_center_is_besieged_by, -1),
         (             party_slot_eq, "$g_encountered_party", slot_center_is_besieged_by, "p_main_party"),
         (store_relation, ":reln", "$g_encountered_party_faction", "fac_player_supporters_faction"),
         (ge, ":reln", 0),
         (lt, "$g_encountered_party_2", 1),
         (call_script, "script_party_count_fit_for_battle","p_main_party"),
         (gt, reg(0), 1),
         (try_begin),
           (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
           (assign, reg6, 1),
         (else_try),
           (assign, reg6, 0),
         (try_end),
           ],
       "{!}CHEAT: Besiege the {reg6?town:castle}...",
       [
           (assign,"$g_player_besiege_town","$g_encountered_party"),
           (jump_to_menu, "mnu_castle_besiege"),
           ]),

      ("castle_leave",[],"Leave.",[(change_screen_return,0)]),
      #SB : the three options below are covered in cheats
      ("castle_cheat", [(ge, "$cheat_mode", 1)], "{!}Use Cheats", [
        # (assign, "$sneaked_into_town", disguise_pilgrim),
        (assign, "$town_entered", 1),
        # (assign, "$g_mt_mode", tcm_disguised),
        (jump_to_menu, "mnu_town_cheats"),
      ]),

      # ("castle_cheat_interior",[(eq, "$cheat_mode", 1)], "{!}CHEAT! Interior.",[(set_jump_mission,"mt_ai_training"),
                                                       # (party_get_slot, ":castle_scene", "$current_town", slot_town_castle),
                                                       # (jump_to_scene,":castle_scene"),
                                                       # (change_screen_mission)]),
      # ("castle_cheat_exterior",[(eq, "$cheat_mode", 1)], "{!}CHEAT! Exterior.",[
# #                                                       (set_jump_mission,"mt_town_default"),
                                                       # (set_jump_mission,"mt_ai_training"),
                                                       # (party_get_slot, ":castle_scene", "$current_town", slot_castle_exterior),
                                                       # (jump_to_scene,":castle_scene"),
                                                       # (change_screen_mission)]),
      # ("castle_cheat_town_walls",[(eq, "$cheat_mode", 1),(party_slot_eq,"$current_town",slot_party_type, spt_town),], "{!}CHEAT! Town Walls.",
       # [
         # (party_get_slot, ":scene", "$current_town", slot_town_walls),
         # (set_jump_mission,"mt_ai_training"),
         # (jump_to_scene,":scene"),
         # (change_screen_mission)]),

    ]
  ),
   (
    "castle_guard",mnf_scale_picture,
    "You approach the gate. The men on the walls watch you closely.",
    "none",
    [
        (call_script, "script_set_town_picture"),
    ],
    [
      ("request_shelter",[(party_slot_eq, "$g_encountered_party",slot_party_type, spt_castle),
                          (ge, "$g_encountered_party_relation", 0)],
       "Request entry to the castle.",
       [(party_get_slot, ":castle_lord", "$g_encountered_party", slot_town_lord),
        (try_begin),
          (lt, ":castle_lord", 0),
          (jump_to_menu, "mnu_castle_entry_granted"),
        (else_try),
          (call_script, "script_troop_get_player_relation", ":castle_lord"),
          (assign, ":castle_lord_relation", reg0),
          #(troop_get_slot, ":castle_lord_relation", ":castle_lord", slot_troop_player_relation),
          (try_begin),
            (gt, ":castle_lord_relation", -15),
            (jump_to_menu, "mnu_castle_entry_granted"),
          (else_try),
            (jump_to_menu, "mnu_castle_entry_denied"),
          (try_end),
        (try_end),
       ]),
      ("request_meeting_commander",[],
       "Request a meeting with someone.",
       [
          (jump_to_menu, "mnu_castle_meeting"),
       ]),
      ("guard_leave",[],
       "Leave.",
       [(change_screen_return,0)]),
    ]
  ),
  (
    "castle_entry_granted",mnf_scale_picture,
    "After a brief wait, the guards open the gates for you and allow your party inside.",
    "none",
    [
        (call_script, "script_set_town_picture"),
    ],
    [
      ("continue",[],
       "Continue...",
       [(jump_to_menu,"mnu_town")]),
    ]
  ),
  (
    "castle_entry_denied",mnf_scale_picture,
    "The lord of this castle has forbidden you from coming inside these walls,\
 and the guard sergeant informs you that his men will fire if you attempt to come any closer.",
    "none",
    [
        (call_script, "script_set_town_picture"),
    ],
    [
      ("continue",[],
       "Continue...",
       [(jump_to_menu,"mnu_castle_guard")]),
    ]
  ),

  #SB : restructue this to call new script
  # (
    # "castle_meeting",mnf_scale_picture,
    # "With whom do you want to meet?",
    # "none",
    # [
        # (assign, "$num_castle_meeting_troops", 0),
        # (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
          # (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
          # (call_script, "script_get_troop_attached_party", ":troop_no"),
          # (eq, "$g_encountered_party", reg0),
          # (troop_set_slot, "trp_temp_array_a", "$num_castle_meeting_troops", ":troop_no"),
          # (val_add, "$num_castle_meeting_troops", 1),
        # (try_end),
        # (call_script, "script_set_town_picture"),
    # ],
    # [
      # ("guard_meet_s5",[(gt, "$num_castle_meeting_troops", 0),(troop_get_slot, ":troop_no", "trp_temp_array_a", 0),(str_store_troop_name, s5, ":troop_no")],
       # "{s5}.",[(troop_get_slot, "$castle_meeting_selected_troop", "trp_temp_array_a", 0),(jump_to_menu,"mnu_castle_meeting_selected")]),
      # ("guard_meet_s5",[(gt, "$num_castle_meeting_troops", 1),(troop_get_slot, ":troop_no", "trp_temp_array_a", 1),(str_store_troop_name, s5, ":troop_no")],
       # "{s5}.",[(troop_get_slot, "$castle_meeting_selected_troop", "trp_temp_array_a", 1),(jump_to_menu,"mnu_castle_meeting_selected")]),
      # ("guard_meet_s5",[(gt, "$num_castle_meeting_troops", 2),(troop_get_slot, ":troop_no", "trp_temp_array_a", 2),(str_store_troop_name, s5, ":troop_no")],
       # "{s5}.",[(troop_get_slot, "$castle_meeting_selected_troop", "trp_temp_array_a", 2),(jump_to_menu,"mnu_castle_meeting_selected")]),
      # ("guard_meet_s5",[(gt, "$num_castle_meeting_troops", 3),(troop_get_slot, ":troop_no", "trp_temp_array_a", 3),(str_store_troop_name, s5, ":troop_no")],
       # "{s5}.",[(troop_get_slot, "$castle_meeting_selected_troop", "trp_temp_array_a", 3),(jump_to_menu,"mnu_castle_meeting_selected")]),
      # ("guard_meet_s5",[(gt, "$num_castle_meeting_troops", 4),(troop_get_slot, ":troop_no", "trp_temp_array_a", 4),(str_store_troop_name, s5, ":troop_no")],
       # "{s5}.",[(troop_get_slot, "$castle_meeting_selected_troop", "trp_temp_array_a", 4),(jump_to_menu,"mnu_castle_meeting_selected")]),
      # ("guard_meet_s5",[(gt, "$num_castle_meeting_troops", 5),(troop_get_slot, ":troop_no", "trp_temp_array_a", 5),(str_store_troop_name, s5, ":troop_no")],
       # "{s5}.",[(troop_get_slot, "$castle_meeting_selected_troop", "trp_temp_array_a", 5),(jump_to_menu,"mnu_castle_meeting_selected")]),
      # ("guard_meet_s5",[(gt, "$num_castle_meeting_troops", 6),(troop_get_slot, ":troop_no", "trp_temp_array_a", 6),(str_store_troop_name, s5, ":troop_no")],
       # "{s5}.",[(troop_get_slot, "$castle_meeting_selected_troop", "trp_temp_array_a", 6),(jump_to_menu,"mnu_castle_meeting_selected")]),
      # ("guard_meet_s5",[(gt, "$num_castle_meeting_troops", 7),(troop_get_slot, ":troop_no", "trp_temp_array_a", 7),(str_store_troop_name, s5, ":troop_no")],
       # "{s5}.",[(troop_get_slot, "$castle_meeting_selected_troop", "trp_temp_array_a", 7),(jump_to_menu,"mnu_castle_meeting_selected")]),
      # ("guard_meet_s5",[(gt, "$num_castle_meeting_troops", 8),(troop_get_slot, ":troop_no", "trp_temp_array_a", 8),(str_store_troop_name, s5, ":troop_no")],
       # "{s5}.",[(troop_get_slot, "$castle_meeting_selected_troop", "trp_temp_array_a", 8),(jump_to_menu,"mnu_castle_meeting_selected")]),
      # ("guard_meet_s5",[(gt, "$num_castle_meeting_troops", 9),(troop_get_slot, ":troop_no", "trp_temp_array_a", 9),(str_store_troop_name, s5, ":troop_no")],
       # "{s5}.",[(troop_get_slot, "$castle_meeting_selected_troop", "trp_temp_array_a", 9),(jump_to_menu,"mnu_castle_meeting_selected")]),

      # ("forget_it",[],
       # "Forget it.",
       # [(jump_to_menu,"mnu_castle_guard")]),
    # ]
  # ),
  # (
    # "castle_meeting_selected",0,
    # "Your request for a meeting is relayed inside, and finally {s6} appears in the courtyard to speak with you.",
    # "none",
    # [(str_store_troop_name, s6, "$castle_meeting_selected_troop")],
    # [
      # ("continue",[],
       # "Continue...",
       # [(jump_to_menu, "mnu_castle_outside"),
        # (modify_visitors_at_site,"scn_conversation_scene"),(reset_visitors),
        # (set_visitor,0,"trp_player"),
        # (set_visitor,17,"$castle_meeting_selected_troop"),
        # (set_jump_mission,"mt_conversation_encounter"),
        # (jump_to_scene,"scn_conversation_scene"),
        # (assign, "$talk_context", tc_castle_gate),
        # (change_screen_map_conversation, "$castle_meeting_selected_troop"),
        # ]),
    # ]
  # ),
  (
    "castle_meeting",mnf_scale_picture,
    "With whom do you want to meet?",
    "none",
    [   (party_clear, "p_temp_party"),
        (call_script, "script_set_town_picture"),
        (call_script, "script_get_heroes_attached_to_center_aux", "$g_encountered_party", "p_temp_party"),#recursive call
        (party_get_num_companion_stacks, "$num_castle_meeting_troops", "p_temp_party"),
        (assign, "$talk_context", tc_castle_gate), #SB : move this up here
    ],
    [ ("guard_meet_"+str(x),[
        (gt, "$num_castle_meeting_troops", x),#test this out
        (party_stack_get_troop_id, ":troop_no", "p_temp_party", x),
        (is_between, ":troop_no", active_npcs_begin, active_npcs_end),
        (str_store_troop_name, s5, ":troop_no")],
       "{s5}.",[(party_stack_get_troop_id, "$castle_meeting_selected_troop", "p_temp_party", x),
       # (party_stack_get_troop_dna, "$temp_2", "p_temp_party", x),
       (jump_to_menu,"mnu_castle_meeting_selected")])
       for x in range(0, 8)
      ]

    +[("forget_it",[], "Forget it.", [(jump_to_menu,"mnu_castle_guard")]),]
  ),
  (
    "castle_meeting_selected",0,
    "Your request for a meeting is relayed inside, and finally {s6} appears in the courtyard to speak with you.",
    "none",
    [
    (try_begin),
		(eq, "$g_leave_encounter", 1),
		(change_screen_return),
	(try_end),

    (str_store_troop_name, s6, "$castle_meeting_selected_troop")],
    [
      ("continue",[],
       "Continue...",
       [(jump_to_menu, "mnu_castle_outside"),
        #do not set context here in case we need to use another one, set tc_castle_gate from parent menu
        (call_script, "script_start_courtyard_conversation", "$castle_meeting_selected_troop", "$current_town"),
        ]),
    ]
  ),

   ( #SB : pic hotkeys
    "castle_besiege",mnf_scale_picture|mnf_enable_hot_keys,
    "You are laying siege to {s1}. {s2} {s3}",
    "none",
    [
          ##diplomacy start+ test gender with script
        #(troop_get_type, ":is_female", "trp_player"),#<- replaced
        (try_begin),
          #(eq, ":is_female", 1),#<- replaced
          (eq, "$character_gender", tf_female),#<- added
          (set_background_mesh, "mesh_pic_siege_sighted_fem"),
        (else_try),
          (set_background_mesh, "mesh_pic_siege_sighted"),
        (try_end),
          ##diplomacy end+
        (assign, "$g_siege_force_wait", 0),
        (try_begin),
          (party_slot_eq, "$g_encountered_party", slot_center_is_besieged_by, -1),
          (party_set_slot, "$g_encountered_party", slot_center_is_besieged_by, "p_main_party"),
          (store_current_hours, ":cur_hours"),
          (party_set_slot, "$g_encountered_party", slot_center_siege_begin_hours, ":cur_hours"),
          (assign, "$g_siege_method", 0),
          (assign, "$g_siege_sallied_out_once", 0),
          #SB : also add sneak variables here
          (assign, "$last_sneak_attempt_town", "$g_encountered_party"),
          (assign, "$last_sneak_attempt_time", ":cur_hours"),
        (try_end),

        (party_get_slot, ":town_food_store", "$g_encountered_party", slot_party_food_store),
        (call_script, "script_center_get_food_consumption", "$g_encountered_party"),
        (assign, ":food_consumption", reg0),
        (assign, reg7, ":food_consumption"),
        (assign, reg8, ":town_food_store"),
        (store_div, reg3, ":town_food_store", ":food_consumption"),

        (try_begin),
          (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
          (assign, reg6, 1),
        (else_try),
          (assign, reg6, 0),
        (try_end),

        (try_begin),
          (gt, reg3, 0),
          (str_store_string, s2, "@The {reg6?town's:castle's} food stores should last for {reg3} more days."),
        (else_try),
          (str_store_string, s2, "@The {reg6?town's:castle's} food stores have run out and the defenders are starving."),
        (try_end),

        (str_store_string, s3, "str_empty_string"),
        (try_begin),
          (ge, "$g_siege_method", 1),
          (store_current_hours, ":cur_hours"),
          (try_begin),
            (lt, ":cur_hours",  "$g_siege_method_finish_hours"),
            (store_sub, reg9, "$g_siege_method_finish_hours", ":cur_hours"),
            (try_begin),
              (eq, "$g_siege_method", 1),
              (str_store_string, s3, "@You're preparing to attack the walls, the work should finish in {reg9} hours."),
            (else_try),
              (eq, "$g_siege_method", 2),
              (str_store_string, s3, "@Your forces are building a siege tower. They estimate another {reg9} hours to complete construction."), #SB : "the build -> construction"
            (try_end),
          (else_try),
            (try_begin),
              (eq, "$g_siege_method", 1),
              (str_store_string, s3, "@You are ready to attack the walls at any time."),
            (else_try),
              (eq, "$g_siege_method", 2),
              (str_store_string, s3, "@The siege tower is built and ready to make an assault."),
            (try_end),
          (try_end),
        (try_end),

        #Check if enemy leaves the castle to us...
        (try_begin),
          (eq, "$g_castle_left_to_player",1), #we come here after dialog. Empty the castle and send parties away.
          (assign, "$g_castle_left_to_player",0),
          (store_faction_of_party, ":castle_faction", "$g_encountered_party"),
          (party_set_faction,"$g_encountered_party","fac_neutral"), #temporarily erase faction so that it is not the closest town
          (party_get_num_attached_parties, ":num_attached_parties_to_castle","$g_encountered_party"),
          (try_for_range_backwards, ":iap", 0, ":num_attached_parties_to_castle"),
            (party_get_attached_party_with_rank, ":attached_party", "$g_encountered_party", ":iap"),
            (party_detach, ":attached_party"),
            (party_get_slot, ":attached_party_type", ":attached_party", slot_party_type),
            (eq, ":attached_party_type", spt_kingdom_hero_party),
            (store_faction_of_party, ":attached_party_faction", ":attached_party"),
            (call_script, "script_get_closest_walled_center_of_faction", ":attached_party", ":attached_party_faction"),
            (try_begin),
              (gt, reg0, 0),
              (call_script, "script_party_set_ai_state", ":attached_party", spai_holding_center, reg0),
            (else_try),
              (call_script, "script_party_set_ai_state", ":attached_party", spai_patrolling_around_center, "$g_encountered_party"),
            (try_end),
          (try_end),
          (call_script, "script_party_remove_all_companions", "$g_encountered_party"),
          (change_screen_return),
          (party_collect_attachments_to_party, "$g_encountered_party", "p_collective_enemy"), #recalculate so that
          (call_script, "script_party_copy", "p_encountered_party_backup", "p_collective_enemy"), #leaving troops will not be considered as captured
          (party_set_faction,"$g_encountered_party",":castle_faction"),
        (try_end),

        #Check for victory or defeat....
        (assign, "$g_enemy_party", "$g_encountered_party"),
        (assign, "$g_ally_party", -1),
        (str_store_party_name, 1,"$g_encountered_party"),
        (call_script, "script_encounter_calculate_fit"),

        (assign, reg11, "$g_enemy_fit_for_battle"),
        (assign, reg10, "$g_friend_fit_for_battle"),


        (try_begin),
          (eq, "$g_leave_encounter",1),
          (change_screen_return),
        ##diplomacy begin
        (else_try),
          (party_slot_eq, "$g_encountered_party", slot_village_infested_by_bandits, "trp_peasant_woman"),
          (call_script, "script_party_count_fit_regulars","p_collective_enemy"),
          (assign, ":enemy_finished", 0),
          (try_begin),
            (eq, "$g_battle_result", 1),
            (assign, ":enemy_finished", 1),
          (else_try),
            (le, "$g_enemy_fit_for_battle", 0),
            (ge, "$g_friend_fit_for_battle", 1),
            (assign, ":enemy_finished", 1),
          (try_end),
          (this_or_next|eq, ":enemy_finished", 1),
          (eq, "$g_enemy_surrenders", 1),
          (assign, "$g_next_menu", "mnu_dplmc_town_riot_removed"),
          (jump_to_menu, "mnu_total_victory"),
        ##diplomacy end
        (else_try),
          (call_script, "script_party_count_fit_regulars","p_collective_enemy"),
          (assign, ":enemy_finished", 0),
          (try_begin),
            (eq, "$g_battle_result", 1),
            (assign, ":enemy_finished", 1),
          (else_try),
            (le, "$g_enemy_fit_for_battle", 0),
            (ge, "$g_friend_fit_for_battle", 1),
            (assign, ":enemy_finished", 1),
          (try_end),
          (this_or_next|eq, ":enemy_finished", 1),
          (eq, "$g_enemy_surrenders", 1),

          (assign, "$g_next_menu", "mnu_castle_taken"),
          (jump_to_menu, "mnu_total_victory"),
        (else_try),
          (call_script, "script_party_count_members_with_full_health", "p_main_party"),
          (assign, ":main_party_fit_regulars", reg0),
          (eq, "$g_battle_result", -1),
          (eq, ":main_party_fit_regulars", 0), #all lost (TODO : )
          (assign, "$g_next_menu", "mnu_captivity_start_castle_defeat"),
          (jump_to_menu, "mnu_total_defeat"),
        (try_end),
    ],
    [
      ("toggle_weapons",
        [
          (call_script, "script_get_num_heroes_of_party", "p_main_party", 0),
          (assign, ":num_of_heroes", reg0),
          (gt, ":num_of_heroes", 1),
          (try_begin),
            (eq, "$g_weapons_set_no", 0),
            (assign, reg1, 2),
          (else_try),
            (assign, reg1, 1),
          (try_end),
        ],
        "Toggle weapons to set {reg1} for heroes.",
        [
          (val_add, "$g_weapons_set_no", 1),
          (val_mod, "$g_weapons_set_no", 2),
          (call_script, "script_all_toggle_weapons_set", 0),
        ]),

      ("siege_request_meeting",[(eq, "$cant_talk_to_enemy", 0)],"Call for a meeting with the castle commander.", [
          (assign, "$cant_talk_to_enemy", 1),
          (assign, "$g_enemy_surrenders",0),
          (assign, "$g_castle_left_to_player",0),
          (assign, "$talk_context", tc_castle_commander),
          (party_get_num_attached_parties, ":num_attached_parties_to_castle","$g_encountered_party"),
          #SB : use start_courtyard_conversation
          (try_begin),
            (gt, ":num_attached_parties_to_castle", 0),
            (party_get_attached_party_with_rank, ":leader_attached_party", "$g_encountered_party", 0),
            (party_stack_get_troop_id, ":leader",":leader_attached_party",0),
          (else_try),
            (party_stack_get_troop_id, ":leader","$g_encountered_party",0),
          (try_end),
          (call_script, "script_start_courtyard_conversation", ":leader", "$g_encountered_party"),
           ]),

      ("wait_24_hours",[],"Wait until tomorrow.", [
          (assign,"$auto_besiege_town","$g_encountered_party"),
          (assign, "$g_siege_force_wait", 1),
          (store_time_of_day,":cur_time_of_day"),
          (val_add, ":cur_time_of_day", 1),
          (assign, ":time_to_wait", 31),
          (val_sub,":time_to_wait",":cur_time_of_day"),
          (val_mod,":time_to_wait",24),
          (val_add, ":time_to_wait", 1),
          (rest_for_hours_interactive, ":time_to_wait", 5, 1), #rest while attackable
          (assign, "$cant_talk_to_enemy", 0),
          (change_screen_return),
          ]),


      ("castle_lead_attack",
       [
         (neg|troop_is_wounded, "trp_player"),
         (ge, "$g_siege_method", 1),
         (gt, "$g_friend_fit_for_battle", 3),
         (store_current_hours, ":cur_hours"),
         (ge, ":cur_hours", "$g_siege_method_finish_hours"),
       ],
       "Lead your soldiers in an assault.",
       [
           (try_begin),
             (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
             (party_get_slot, ":battle_scene", "$g_encountered_party", slot_town_walls),
           (else_try),
             (party_get_slot, ":battle_scene", "$g_encountered_party", slot_castle_exterior),
           (try_end),

           (call_script, "script_calculate_renown_value"),
           (call_script, "script_calculate_battle_advantage"),
           (assign, ":battle_advantage", reg0),
           (val_mul, ":battle_advantage", 2),
           (val_div, ":battle_advantage", 3), #scale down the advantage a bit in sieges.
           (set_battle_advantage, ":battle_advantage"),
           (set_party_battle_mode),
           (assign, "$g_siege_battle_state", 1),
           (assign, ":siege_sally", 0),
           (try_begin),
             (le, ":battle_advantage", -4), #we are outnumbered, defenders sally out
             (eq, "$g_siege_sallied_out_once", 0),
             (set_jump_mission,"mt_castle_attack_walls_defenders_sally"),
             (assign, "$g_siege_battle_state", 0),
             (assign, ":siege_sally", 1),
           (else_try),
             (party_slot_eq, "$current_town", slot_center_siege_with_belfry, 1),
             (set_jump_mission,"mt_castle_attack_walls_belfry"),
           (else_try),
             (set_jump_mission,"mt_castle_attack_walls_ladder"),
           (try_end),
           (assign, "$cant_talk_to_enemy", 0),
           (assign, "$g_siege_final_menu", "mnu_castle_besiege"),
           (assign, "$g_next_menu", "mnu_castle_besiege_inner_battle"),
           (assign, "$g_siege_method", 0), #reset siege timer
           (jump_to_scene,":battle_scene"),
           (try_begin),
             (eq, ":siege_sally", 1),
             (jump_to_menu, "mnu_siege_attack_meets_sally"),
           (else_try),
             (jump_to_menu, "mnu_battle_debrief"),
             (change_screen_mission),
           (try_end),
       ]),
      ("attack_stay_back",
       [
         (ge, "$g_siege_method", 1),
         (gt, "$g_friend_fit_for_battle", 3),
         (store_current_hours, ":cur_hours"),
         (ge, ":cur_hours",  "$g_siege_method_finish_hours"),
         ],
       "Order your soldiers to attack while you stay back...", [(assign, "$cant_talk_to_enemy", 0),(jump_to_menu,"mnu_castle_attack_walls_simulate")]),

      ("build_ladders",[(party_slot_eq, "$current_town", slot_center_siege_with_belfry, 0),(eq, "$g_siege_method", 0)],
       "Prepare ladders to attack the walls.", [(jump_to_menu,"mnu_construct_ladders")]),

      ("build_siege_tower",[(party_slot_eq, "$current_town", slot_center_siege_with_belfry, 1),(eq, "$g_siege_method", 0)],
       "Build a siege tower.", [(jump_to_menu,"mnu_construct_siege_tower")]),

      ("siege_camp",[],"Walk around the siege camp.", #dckplmc
       [(set_jump_mission,"mt_camp"),
        (call_script, "script_setup_camp_scene"),
        (change_screen_mission),
        ]
       ),

      ("cheat_castle_lead_attack",[(eq, "$cheat_mode", 1),
                                   (eq, "$g_siege_method", 0)],
       "{!}CHEAT: Instant build equipments.",
       [
         (assign, "$g_siege_method", 1),
         (assign, "$g_siege_method_finish_hours", 0),
         (jump_to_menu, "mnu_castle_besiege"),
       ]),

      ("cheat_conquer_castle",[(eq, "$cheat_mode", 1),
                                   ],
       "{!}CHEAT: Instant conquer castle.",
       [
        (assign, "$g_next_menu", "mnu_castle_taken"),
        (jump_to_menu, "mnu_total_victory"),
       ]),

      ("lift_siege",[],"Abandon the siege.",
       [
         (call_script, "script_lift_siege", "$g_player_besiege_town", 0),
         (assign,"$g_player_besiege_town", -1),
         (change_screen_return)]),
    ]
  ),
  (
    "castle_taken_by_friends",0,
    "Nothing to see here.",
    "none",
    [
        (party_clear, "$g_encountered_party"),
        (party_stack_get_troop_id, ":leader", "$g_encountered_party_2", 0),
        (party_set_slot, "$g_encountered_party", slot_center_last_taken_by_troop, ":leader"),
        (store_troop_faction, ":faction_no", ":leader"),
        #Reduce prosperity of the center by 5
        (call_script, "script_change_center_prosperity", "$g_encountered_party", -5),
		(try_begin),
			(assign, ":damage", 20),
			(is_between, "$g_encountered_party", towns_begin, towns_end),
			(assign, ":damage", 40),
		(try_end),
		(try_begin),
			(neq, ":faction_no", "$g_encountered_party_faction"),
			(call_script, "script_faction_inflict_war_damage_on_faction", ":faction_no", "$g_encountered_party_faction", ":damage"),
		(try_end),

        (call_script, "script_give_center_to_faction", "$g_encountered_party", ":faction_no"),
        (call_script, "script_add_log_entry", logent_player_participated_in_siege, "trp_player",  "$g_encountered_party", 0, "$g_encountered_party_faction"),
        (call_script, "script_change_player_relation_with_lords_after_battle"),
##        (call_script, "script_change_troop_renown", "trp_player", 1),
        (change_screen_return),
    ],
    [
    ],
  ),
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
  ),
  (
    "castle_taken_2",mnf_disable_all_keys,
    "{s3} has fallen to your troops, and you now have full control of the castle.\
 It is time to send word to {s9} about your victory. {s5}",
    "none",
    [
        (str_store_party_name, s3, "$g_encountered_party"),
        (str_clear, s5),
        (faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
        (str_store_troop_name, s9, ":faction_leader"),
        (try_begin),
          (eq, "$player_has_homage", 0),
          (assign, reg8, 0),
          (try_begin),
		    ##diplomacy start+ FIX: Inserted missing argument
            #(party_slot_eq, "$g_encountered_party", spt_town),
			(party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
			##diplomacy end+
            (assign, reg8, 1),
          (try_end),
          ##diplomacy start+ fix gender of pronoun
          (call_script, "script_dplmc_store_troop_is_female", ":faction_leader"),
          (str_store_string, s5, "@However, since you are not a sworn {man/follower} of {s9}, there is no chance {reg0?she:he} would recognize you as the {lord/lady} of this {reg8?town:castle}."),
          ##diplomacy end+
        (try_end),
    ],
    [
        ("castle_taken_claim",[(eq, "$player_has_homage", 1)],
		"Request that {s3} be awarded to you.",
        [
        (party_set_slot, "$g_encountered_party", slot_center_last_taken_by_troop, "trp_player"),
        (assign, "$g_castle_requested_by_player", "$current_town"),
		(assign, "$g_castle_requested_for_troop", "trp_player"),
        (assign, "$auto_enter_town", "$g_encountered_party"),
        (change_screen_return),
        ]),

		("castle_taken_claim_2",[
		(troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),
		(is_between, ":spouse", active_npcs_begin, active_npcs_end),
		(troop_slot_eq, ":spouse", slot_troop_occupation, slto_kingdom_hero),
		(store_faction_of_troop, ":spouse_faction", ":spouse"),
		(eq, ":spouse_faction", "$players_kingdom"),
		],
		"Request that {s3} be awarded to your {wife/husband}.",
        [
        (party_set_slot, "$g_encountered_party", slot_center_last_taken_by_troop, "trp_player"),
        (assign, "$g_castle_requested_by_player", "$current_town"),
		(troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),
		(assign, "$g_castle_requested_for_troop", ":spouse"),
        (assign, "$auto_enter_town", "$g_encountered_party"),
        (change_screen_return),
        ]),



      ("castle_taken_no_claim",[],"Ask no rewards.",
       [
        (party_set_slot, "$g_encountered_party", slot_center_last_taken_by_troop, -1),
        (assign, "$auto_enter_town", "$g_encountered_party"),
        (change_screen_return),
#        (jump_to_menu, "mnu_town"),
        ]),
    ],
  ),

(
    "requested_castle_granted_to_player",mnf_scale_picture,
    "You receive a message from your liege, {s3}.^^\
 {reg4?She:He} has decided to grant {s2}{reg3? and the nearby village of {s4}:} to you, with all due incomes and titles, to hold in {reg4?her:his} name for as long as you maintain your oath of homage..",
    "none",
    [
		(set_background_mesh, "mesh_pic_messenger"),
		(faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
		(str_store_troop_name, s3, ":faction_leader"),
		(str_store_party_name, s2, "$g_center_to_give_to_player"),
		(try_begin),
			(party_slot_eq, "$g_center_to_give_to_player", slot_party_type, spt_castle),
			(assign, reg3, 1),
			(try_for_range, ":cur_village", villages_begin, villages_end),
				(party_slot_eq, ":cur_village", slot_village_bound_center, "$g_center_to_give_to_player"),
				(str_store_party_name, s4, ":cur_village"),
			(try_end),
		(else_try),
			(assign, reg3, 0),
		(try_end),
		##diplomacy start+ use script for gender
		#(troop_get_type, reg4, ":faction_leader"),#<- OLD
		(call_script, "script_dplmc_store_troop_is_female_reg", ":faction_leader", 4),
		##diplomacy end+
   ],
    [
		("continue",[],"Continue.",
			[
			(call_script, "script_give_center_to_lord", "$g_center_to_give_to_player", "trp_player", 0),
			(jump_to_menu, "mnu_give_center_to_player_2"),
			],
		),
	]
),



(
    "requested_castle_granted_to_player_husband", mnf_scale_picture,
    "You receive a message from your liege, {s3}.^^\
 {reg4?She:He} has decided to grant {s2}{reg3? and the nearby village of {s4}:} to your husband, {s7}.",
    "none",
    [
		(set_background_mesh, "mesh_pic_messenger"),
		(faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
		(str_store_troop_name, s3, ":faction_leader"),
		(str_store_party_name, s2, "$g_center_to_give_to_player"),
		(try_begin),
			(party_slot_eq, "$g_center_to_give_to_player", slot_party_type, spt_castle),
			(assign, reg3, 1),
			(try_for_range, ":cur_village", villages_begin, villages_end),
				(party_slot_eq, ":cur_village", slot_village_bound_center, "$g_center_to_give_to_player"),
				(str_store_party_name, s4, ":cur_village"),
			(try_end),
		(else_try),
			(assign, reg3, 0),
		(try_end),
		##diplomacy start+ use script for gender
		#(troop_get_type, reg4, ":faction_leader"),#<- OLD
		(call_script, "script_dplmc_store_troop_is_female_reg", ":faction_leader", 4),
		##diplomacy end+

		(troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),
		(str_store_troop_name, s11, ":spouse"),
		(str_store_string, s7, "str_to_your_husband_s11"),
    ],
    [
		("continue",[],"Continue.",
			[
			(troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),
			(call_script, "script_give_center_to_lord", "$g_center_to_give_to_player", ":spouse", 0),
			],
		),
	]
),







(
    "requested_castle_granted_to_another",mnf_scale_picture,
    "You receive a message from your monarch, {s3}.^^\
 'I was most pleased to hear of your valiant efforts in the capture of {s2}. Your victory has gladdened all our hearts.\
 You also requested me to give you ownership of the castle, but that is a favor which I fear I cannot grant,\
 as you already hold significant estates in my realm.\
 Instead I have sent you {reg6} denars to cover the expenses of your campaign, but {s2} I give to {s5}.'\
 ",
    "none",
    [(set_background_mesh, "mesh_pic_messenger"),
     (faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
     (str_store_troop_name, s3, ":faction_leader"),
     (str_store_party_name, s2, "$g_center_to_give_to_player"),
     (party_get_slot, ":new_owner", "$g_center_to_give_to_player", slot_town_lord),
     (str_store_troop_name, s5, ":new_owner"),
     (assign, reg6, 900),

	 (assign, "$g_castle_requested_by_player", -1),
	 (assign, "$g_castle_requested_for_troop", -1),

    ],
    [
      ("accept_decision",[],"Accept the decision.",
       [
       (call_script, "script_troop_add_gold", "trp_player", reg6),
        ##diplomacy start+ Remove gold spent by liege
        (faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
        (try_begin),
            (gt, ":faction_leader", 0),
            (neq, ":faction_leader", "trp_kingdom_heroes_including_player_begin"),
            (call_script, "script_dplmc_remove_gold_from_lord_and_holdings", reg6, ":faction_leader"),
        (try_end),
        ##diplomacy end+
       (change_screen_return),
       ]),

       ("leave_faction",[],"You have been wronged! Renounce your oath to your liege! ",
       [
         ##diplomacy start+ Remove gold spent by liege
         (faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
         (try_begin),
            (gt, ":faction_leader", 0),
            (neq, ":faction_leader", "trp_kingdom_heroes_including_player_begin"),
            (call_script, "script_dplmc_remove_gold_from_lord_and_holdings", reg6, ":faction_leader"),
         (try_end),
         ##diplomacy end+
         (jump_to_menu, "mnu_leave_faction"),
         (call_script, "script_troop_add_gold", "trp_player", reg6),
        ]),
     ],
  ),


(
    "requested_castle_granted_to_another_female",mnf_scale_picture,
##diplomacy start+ make gender correct
    "You receive a message from your monarch, {s3}.^^\
 'I was most pleased to hear of your valiant efforts in the capture of {s2}. Your victory has gladdened all our hearts.\
 You also requested me to give ownership of the castle to your {wife/husband}, but that is a favor which I fear I cannot grant,\
 as {she/he} already holds significant estates in my realm.\
 Instead I have sent you {reg6} denars to cover the expenses of your campaign, but {s2} I give to {s5}.'\
 ",
##diplomacy end+
    "none",
    [(set_background_mesh, "mesh_pic_messenger"),
     (faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
     (str_store_troop_name, s3, ":faction_leader"),
     (str_store_party_name, s2, "$g_center_to_give_to_player"),
     (party_get_slot, ":new_owner", "$g_center_to_give_to_player", slot_town_lord),
     (str_store_troop_name, s5, ":new_owner"),
     (assign, reg6, 900),

	 (assign, "$g_castle_requested_by_player", -1),
	 (assign, "$g_castle_requested_for_troop", -1),
    ],

    [
		("accept_decision",[],"Accept the decision.",
        [
        (call_script, "script_troop_add_gold", "trp_player", reg6),
        (change_screen_return),
        ]),
    ],
),
]
