# ======================================================================
# SHARED DEPENDENCY
# Entity: castle_outside (menu)
# Called by menus in 4 domains: castle, diplomacy, siege, town
# ======================================================================

# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

castle_outside_menu = [
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
  )
]
