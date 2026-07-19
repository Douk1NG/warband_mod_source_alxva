# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

town_menu = [
(
    "town",mnf_enable_hot_keys|mnf_scale_picture,
    "{s10} {s14}^{s11}{s12}{s13}",
    "none",
    [
        #Begin floris town lord
        (try_begin),
        (party_get_slot, ":center_lord", "$current_town", slot_town_lord),
        (ge, ":center_lord", 0),
        (set_fixed_point_multiplier, 100),
        (position_set_x, pos1, 70),
        (position_set_y, pos1, 5),
        (position_set_z, pos1, 75),
        (set_game_menu_tableau_mesh, "tableau_troop_note_mesh", ":center_lord", pos1),
        (try_end),
        #End Floris town lord
        (try_begin),
          (gt, "$sneaked_into_town", disguise_none),
          (call_script, "script_music_set_situation_with_culture", mtf_sit_town_infiltrate),
        (else_try),
          (call_script, "script_music_set_situation_with_culture", mtf_sit_travel),
        (try_end),
        (store_encountered_party, "$current_town"),
        (call_script, "script_update_center_recon_notes", "$current_town"),
        #SB : move prisoners to dungeon if we are the lord
        (try_begin),
          (party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
          (party_get_num_prisoners, ":num_player_prisoners", "p_main_party"),
          (gt, ":num_player_prisoners", 0),
          (assign, "$g_move_heroes", 1),
          (call_script, "script_party_prisoners_add_party_prisoners", "$current_town", "p_main_party"),
          (call_script, "script_party_remove_all_prisoners", "p_main_party"),
          (assign, "$g_move_heroes", 0),
          (assign, reg0, ":num_player_prisoners"),
          (display_message, "@{reg0} prisoners have been moved to your dungeon."),
        (try_end),
        (assign, "$g_defending_against_siege", 0),
        (str_clear, s3),
        (party_get_battle_opponent, ":besieger_party", "$current_town"),
        (store_faction_of_party, ":encountered_faction", "$g_encountered_party"),
        (store_relation, ":faction_relation", ":encountered_faction", "fac_player_supporters_faction"),
        (try_begin),
          (gt, ":besieger_party", 0),
          (ge, ":faction_relation", 0),
          (store_faction_of_party, ":besieger_party_faction", ":besieger_party"),
          (store_relation, ":besieger_party_relation", ":besieger_party_faction", "fac_player_supporters_faction"),
          (lt, ":besieger_party_relation", 0),
          (assign, "$g_defending_against_siege", 1),
          (assign, "$g_siege_first_encounter", 1),
          (jump_to_menu, "mnu_siege_started_defender"),
        (try_end),

        (try_begin),
          (is_between, "$g_encountered_party", towns_begin, towns_end),
          (store_sub, ":encountered_town_no", "$g_encountered_party", towns_begin),
          (set_achievement_stat, ACHIEVEMENT_MIGRATING_COCONUTS, ":encountered_town_no", 1),

          (assign, ":there_are_villages_not_visited", 0),
          (try_for_range, ":cur_town", towns_begin, towns_end),
            (store_sub, ":encountered_town_no", ":cur_town", towns_begin),
            (get_achievement_stat, ":town_is_visited", ACHIEVEMENT_MIGRATING_COCONUTS, ":encountered_town_no"),
            (eq, ":town_is_visited", 0),
            (assign, ":there_are_villages_not_visited", 1),
          (try_end),

          (try_begin),
            (eq, ":there_are_villages_not_visited", 0),
            (unlock_achievement, ACHIEVEMENT_MIGRATING_COCONUTS),
          (try_end),
        (try_end),

        #Quest menus

        (assign, "$qst_collect_taxes_currently_collecting", 0),

        (try_begin),
          (gt, "$quest_auto_menu", 0),
          (jump_to_menu, "$quest_auto_menu"),
          (assign, "$quest_auto_menu", 0),
        (try_end),

        (try_begin),
##          (eq, "$g_center_under_siege_battle", 1),
##          (jump_to_menu,"mnu_siege_started_defender"),
##        (else_try),
          (eq, "$g_town_assess_trade_goods_after_rest", "$current_town"), #SB : loop fix
          (assign, "$g_town_assess_trade_goods_after_rest", 0),
          (jump_to_menu,"mnu_town_trade_assessment"),
        (try_end),

        (assign, "$talk_context", 0),
        (assign,"$all_doors_locked",0),

        (try_begin),
          (eq, "$g_town_visit_after_rest", 1),
          (assign, "$g_town_visit_after_rest", 0),
          (assign, "$town_entered", 1),
        (try_end),

        (try_begin),
          (eq,"$g_leave_town",1),
          (assign,"$g_leave_town",0),
          (assign,"$g_permitted_to_center",0),

          #SB : handle disguise removal here or in trigger


          (leave_encounter),
          (change_screen_return),
        (try_end),

        (str_store_party_name, s2, "$current_town"),
        (party_get_slot, ":center_lord", "$current_town", slot_town_lord),
        (store_faction_of_party, ":center_faction", "$current_town"),
        (str_store_faction_name, s9, ":center_faction"),
        (try_begin),
          (ge, ":center_lord", 0),
          (str_store_troop_name,s8,":center_lord"),
          (str_store_string,s7,"@{s8} of {s9}"),
        (try_end),

        (try_begin),
          (party_slot_eq,"$current_town",slot_party_type, spt_town),

          (str_store_string, s60, s2),

          (party_get_slot, ":prosperity", "$current_town", slot_town_prosperity),
          (try_begin),
            (ge, "$cheat_mode", 1),
            (assign, reg4, ":prosperity",),
            (display_message, "@{!}DEBUG -- Prosperity: {reg4}"),
          (try_end),

     #          (val_add, ":prosperity", 5),
          (store_div, ":str_id", ":prosperity", 10),
          (val_min, ":str_id", 9),
          (val_add, ":str_id", "str_town_prosperity_0"),
          (str_store_string, s10, ":str_id"),

          (store_div, ":str_id", ":prosperity", 20),
          (val_min, ":str_id", 4),
          (val_add, ":str_id", "str_town_alt_prosperity_0"),

          (str_store_string, s14, ":str_id"),


        (else_try),
          (str_clear, s14),
          (str_store_string,s10,"@You are at {s2}."),
        (try_end),
        ##diplomacy start+
        (assign, ":save_reg0", reg0),#save variables
        (assign, ":save_reg4", reg4),
        (assign, reg0, 0),
        (assign, reg4, 0),
        (try_begin),#If there's a relation of some kind, write it to s11 (which we'll overwrite below)
            (lt, ":center_lord", 1),
        (else_try),
            #your relative
            (call_script, "script_troop_get_family_relation_to_troop", ":center_lord", "trp_player"),#outputs to s11, reg0, and reg4
            (ge, reg0, 1),#Fall through if this not a relative
        (else_try),
            #your current liege
            (eq, ":center_faction", "$players_kingdom"),
            (is_between, ":center_faction", kingdoms_begin, kingdoms_end),#include fac_player_supporters_faction for claimant quest
            (faction_slot_eq, ":center_faction", slot_faction_leader, ":center_lord"),
            (str_store_string, s11, "@liege"),
            (assign, reg0, 1),
        (else_try),
            #your former liege if you renounced a kingdom
            (eq, ":center_faction", "$players_oath_renounced_against_kingdom"),
            (is_between, ":center_faction", npc_kingdoms_begin, npc_kingdoms_end),
            (faction_slot_eq, ":center_faction", slot_faction_leader, ":center_lord"),
            (str_store_string, s11, "@former liege"),
            (assign, reg0, 1),
        (else_try),
            #stop here for lords you haven't met, or non-hero troops
            (this_or_next|neg|troop_is_hero, ":center_lord"),
            (troop_slot_eq, ":center_lord", slot_troop_met, 0),
        (else_try),
            #check for affiliates
            (call_script, "script_dplmc_is_affiliated_family_member", ":center_lord"),
            (ge, reg0, 1),
            (try_begin),
                (ge, "$g_encountered_party_relation", 0),#don't say "ally" when you might fight them, as that's confusing
                (str_store_string, s11, "str_dplmc_ally"),
            (else_try),
                (str_store_string, s11, "@affiliate"),
            (try_end),
        (else_try),
            #check for former companions
            (call_script, "script_troop_get_player_relation", ":center_lord"),
            (is_between, ":center_lord", companions_begin, companions_end),
            (neg|troop_slot_eq, ":center_lord", slot_troop_playerparty_history, dplmc_pp_history_nonplayer_entry),
            (try_begin),
               (ge, "$g_encountered_party_relation", 0),#don't say "ally" when you might fight them, as that's confusing
               (ge, reg0, 50),
               (str_store_string, s11, "str_dplmc_ally"),
            (else_try),
                (ge, "$g_encountered_party_relation", 0),
                (ge, reg0, 20),
                (str_store_string, s11, "str_dplmc_friend"),
            (else_try),
                (str_store_string, s11, "@former companion"),
            (try_end),
            (assign, reg0, 1),
        (else_try),
            #don't print "friend" if you might fight them
            (lt, "$g_encountered_party_relation", 0),
            (assign, reg0, 0),
        (else_try),
            #check for friends
            (val_div, reg0, 50),#right now reg0 holds the relation with the player
            (ge, reg0, 1),
            (str_store_string, s11, "str_dplmc_friend"),
        (else_try),
            #check for marshall
            (eq, ":center_faction", "$players_kingdom"),
            (faction_slot_eq, ":center_faction", slot_faction_marshall, ":center_lord"),
            (str_store_string, s11, "@marshall"),
        (else_try),
            #check for vassal of player if nothing else to say
            (call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", ":center_faction"),
            (val_add, reg0, 1),
            (val_sub, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
            (ge, reg0, 1),
            (str_store_string, s11, "@vassal"),
        (else_try),
            (assign, reg0, 0),
        (try_end),
        ##diplomacy end+
        (try_begin),
          (party_slot_eq,"$current_town",slot_party_type, spt_castle),
          (try_begin),
            (eq, ":center_lord", "trp_player"),
            (str_store_string,s11,"@ Your own banner flies over the castle gate."),
          ##diplomacy start+ If reg0 > 0, a relation string was written to {s11} above
          (else_try),
            (ge, reg0, 1),
            (str_store_string, s11, "@ You see the banner of your {s11} {s7} over the castle gate."),
          ##diplomacy end+
          (else_try),
            (gt, ":center_lord", -1),
            (troop_slot_eq, ":center_lord", slot_troop_spouse, "trp_player"),
            (str_store_string,s11,"str__you_see_the_banner_of_your_wifehusband_s7_over_the_castle_gate"),
          (else_try),
            (ge, ":center_lord", 0),
            (str_store_string,s11,"@ You see the banner of {s7} over the castle gate."),
          (else_try),
    ##            (str_store_string,s11,"@ This castle seems to belong to no one."),
            (str_store_string,s11,"@ This castle has no garrison."),
          (try_end),
        (else_try),
          (try_begin),
            (eq, ":center_lord", "trp_player"),
            (str_store_string,s11,"@ Your own banner flies over the town gates."),
          ##diplomacy start+ If reg0 > 0, a relation string was written to {s11} above
          (else_try),
            (ge, reg0, 1),
            (str_store_string, s11, "@ The banner of your {s11} {s7} flies over the town gates."),
          ##diplomacy end+
          (else_try),
            (gt, ":center_lord", -1),
            (troop_slot_eq, ":center_lord", slot_troop_spouse, "trp_player"),
            (str_store_string,s11,"str__the_banner_of_your_wifehusband_s7_flies_over_the_town_gates"),
          (else_try),
            (ge, ":center_lord", 0),
            (str_store_string,s11,"@ You see the banner of {s7} over the town gates."),
          (else_try),
    ##            (str_store_string,s11,"@ The townsfolk here have declared their independence."),
            (str_store_string,s11,"@ This town has no garrison."),
          (try_end),
        (try_end),
        ##diplomacy start+
        (assign, reg0, ":save_reg0"),#revert variables
        (assign, reg4, ":save_reg4"),
        ##diplomacy end+

        (str_clear, s12),
        (try_begin),
          (party_slot_eq,"$current_town",slot_party_type, spt_town),
          (party_get_slot, ":center_relation", "$current_town", slot_center_player_relation),
          (call_script, "script_describe_center_relation_to_s3", ":center_relation"),
          (assign, reg9, ":center_relation"),
          (str_store_string, s12, "@{!} {s3} ({reg9})."),
        (try_end),

        (str_clear, s13),
        (try_begin),
          (gt,"$entry_to_town_forbidden",0),
          (str_store_string, s13, "@ You have successfully sneaked in."),
        (else_try),
          (faction_slot_eq, ":center_faction", slot_faction_ai_state, sfai_feast),
          (faction_slot_eq, ":center_faction", slot_faction_ai_object, "$current_town"),

          (str_store_string, s13, "str__the_lord_is_currently_holding_a_feast_in_his_hall"),
        (else_try), #SB : we use this incidental information to reflect on the player's residence/court
          (troop_get_slot, ":player_spouse", "trp_player", slot_troop_spouse),
          (try_begin),
            (lt, ":player_spouse", 0), #to make registers work
            (assign, ":player_spouse", 0),
          (else_try),
            (this_or_next|neg|troop_slot_eq, ":player_spouse", slot_troop_occupation, slto_kingdom_lady),
            (neg|troop_slot_eq, ":player_spouse", slot_troop_cur_center, "$current_town"),
            (assign, ":player_spouse", 0),
          (try_end),
          (try_begin),
            (eq, "$g_player_court", "$current_town"),
            (assign, reg0, ":player_spouse"),
            (store_and, reg1, "$players_kingdom_name_set", rename_center), #check if it's "court" or "capital"
            (str_store_troop_name, s0, ":player_spouse"),
            (str_store_string, s13, "@ Your {reg1?capital is:court can be found} here{reg0? with your spouse, {s0} in residence:}."),
          (else_try),
            (neq, "$g_player_court", "$current_town"),
            (gt, ":player_spouse", 0),
            (str_store_string, s13, "@ Your household can be found here."),
          (try_end),
        (try_end),

        #forbidden to enter?
        (try_begin),
          (store_time_of_day,reg(12)),
          (ge,reg(12),5),
          (lt,reg(12),21),
          (assign,"$town_nighttime",0),
        (else_try),
          (assign,"$town_nighttime",1),
          (party_slot_eq,"$current_town",slot_party_type, spt_town),
          (str_store_string, s13, "str_town_nighttime"),
        (try_end),

        (try_begin),
          (party_slot_ge, "$current_town", slot_town_has_tournament, 1),
          (neg|is_currently_night),
          (party_set_slot, "$current_town", slot_town_has_tournament, 1),
          (str_store_string, s13, "@{s13} A tournament will be held here soon."),
        (try_end),

        (assign,"$castle_undefended",0),
        (party_get_num_companions, ":castle_garrison_size", "p_collective_enemy"),
        (try_begin),
          (eq,":castle_garrison_size",0),
          (assign,"$castle_undefended",1),
        (try_end),

        (call_script, "script_set_town_picture"),

#		(str_clear, s5), #alert player that there are new rumors
#		(try_begin),
#			(eq, 1, 0),
#			(neg|is_currently_night),
#			(str_store_string, s5, "@^The buzz of excited voices as you come near the gate suggests to you that news of some import is circulating among the townsfolk."),
#			(lt, "$last_town_log_entry_checked", "$num_log_entries"),
#			(assign, "$g_town_rumor_log_entry", 0),
#			(try_for_range, ":log_entry", "$last_town_log_entry_checked", "$num_log_entries"),
#				(eq, ":log_entry", 4123), #placeholder to avoid having unused variable error message
#			(try_end),
#			(assign, "$last_town_log_entry_checked", "$num_log_entries"),
#		(try_end),
        ],
    [
      ("castle_castle",
      [
        (party_slot_eq,"$current_town",slot_party_type, spt_castle),

        (eq, "$sneaked_into_town", disguise_none),

        (str_clear, s1),
        (try_begin),
          (store_faction_of_party, ":center_faction", "$current_town"),
          (faction_slot_eq, ":center_faction", slot_faction_ai_state, sfai_feast),
          (faction_slot_eq, ":center_faction", slot_faction_ai_object, "$current_town"),
          (str_store_string, s1, "str__join_the_feast"),
        (try_end),
        #SB : some gender string tweaks
        (try_begin),
          (party_get_slot, ":town_lord", "$current_town", slot_town_lord),
          (lt, ":town_lord", 0),
          (assign, reg4, 0), #default to lord
        (else_try),
          (call_script, "script_dplmc_store_troop_is_female_reg", ":town_lord", 4),
        (try_end),
        (try_begin),
        (party_get_slot, ":center_lord", "$current_town", slot_town_lord),
        (ge, ":center_lord", 0),
        (set_fixed_point_multiplier, 100),
        (position_set_x, pos1, 70),
        (position_set_y, pos1, 5),
        (position_set_z, pos1, 75),
        (set_game_menu_tableau_mesh, "tableau_troop_note_mesh", ":center_lord", pos1),
        (try_end),
        #possibly replace "the" with "your"
        ],"Go to the {reg4?Lady:Lord}'s hall{s1}.",
       [
           (try_begin),
             (this_or_next|eq, "$all_doors_locked", 1),
             (gt, "$sneaked_into_town", disguise_none),
             (display_message,"str_door_locked",message_locked),
           (else_try),
             (this_or_next|neq, "$players_kingdom", "$g_encountered_party_faction"),
             (neg|troop_slot_ge, "trp_player", slot_troop_renown, 50),
             (neg|troop_slot_ge, "trp_player", slot_troop_renown, 125),
             (neq, "$g_player_eligible_feast_center_no", "$current_town"),

             (faction_slot_eq, "$g_encountered_party_faction", slot_faction_ai_state, sfai_feast),
             (faction_slot_eq, "$g_encountered_party_faction", slot_faction_ai_object, "$g_encountered_party"),

             (neg|check_quest_active, "qst_wed_betrothed"),
             (neg|check_quest_active, "qst_wed_betrothed_female"),

             (neg|troop_slot_ge, "trp_player", slot_troop_spouse, active_npcs_begin), #Married players always make the cut

             (jump_to_menu, "mnu_cannot_enter_court"),
           (else_try),
             (assign, "$town_entered", 1),
             (call_script, "script_enter_court", "$current_town"),
           (try_end),
        ], "Door to the castle."),

      ("join_tournament", [
        (neg|is_currently_night),
        (party_slot_ge, "$current_town", slot_town_has_tournament, 1),
        (eq,"$entry_to_town_forbidden",0), #SB : can't participate while disguised
        ]
       ,"Join the tournament.",
       [
           (call_script, "script_fill_tournament_participants_troop", "$current_town", 1),
           (assign, "$g_tournament_cur_tier", 0),
           (assign, "$g_tournament_player_team_won", -1),
           (assign, "$g_tournament_bet_placed", 0),
           (assign, "$g_tournament_bet_win_amount", 0),
           (assign, "$g_tournament_last_bet_tier", -1),
           (assign, "$g_tournament_next_num_teams", 0),
           (assign, "$g_tournament_next_team_size", 0),
           (jump_to_menu, "mnu_town_tournament"),
        ]),

      ("town_castle",[
          (party_slot_eq,"$current_town",slot_party_type, spt_town),
          (eq,"$entry_to_town_forbidden",0),
          (str_clear, s1),
          (try_begin),
            (store_faction_of_party, ":center_faction", "$current_town"),
            (faction_slot_eq, ":center_faction", slot_faction_ai_state, sfai_feast),
            (faction_slot_eq, ":center_faction", slot_faction_ai_object, "$current_town"),
            (str_store_string, s1, "str__join_the_feast"),
          (try_end),

          ],"Go to the castle{s1}.",
       [
           (try_begin),
        (party_get_slot, ":center_lord", "$current_town", slot_town_lord),
        (ge, ":center_lord", 0),
        (set_fixed_point_multiplier, 100),
        (position_set_x, pos1, 70),
        (position_set_y, pos1, 5),
        (position_set_z, pos1, 75),
        (set_game_menu_tableau_mesh, "tableau_troop_note_mesh", ":center_lord", pos1),
        (try_end),
           (try_begin),
             (this_or_next|eq, "$all_doors_locked", 1),
             (gt, "$sneaked_into_town", disguise_none),
             (display_message,"str_door_locked",message_locked),
           (else_try),
             (this_or_next|neq, "$players_kingdom", "$g_encountered_party_faction"),
             (neg|troop_slot_ge, "trp_player", slot_troop_renown, 50),
             (neg|troop_slot_ge, "trp_player", slot_troop_renown, 125),
             (neq, "$g_player_eligible_feast_center_no", "$current_town"),

             (faction_slot_eq, "$g_encountered_party_faction", slot_faction_ai_state, sfai_feast),
             (faction_slot_eq, "$g_encountered_party_faction", slot_faction_ai_object, "$g_encountered_party"),

             (neg|check_quest_active, "qst_wed_betrothed"),
             (neg|check_quest_active, "qst_wed_betrothed_female"),

             (neg|troop_slot_ge, "trp_player", slot_troop_spouse, active_npcs_begin), #Married players always make the cut

             (jump_to_menu, "mnu_cannot_enter_court"),
            (else_try),
              (assign, "$town_entered", 1),
              (call_script, "script_enter_court", "$current_town"),
           (try_end),
        ], "Door to the castle."),

      ("town_center",
      [
        (party_slot_eq, "$current_town", slot_party_type, spt_town),
        (this_or_next|eq,"$entry_to_town_forbidden",0),
        (gt, "$sneaked_into_town", disguise_none), #SB : condition for disguise
      ],
      "Take a walk around the streets.",
       [
         #If the player is fighting his or her way out
         (try_begin),
           (eq, "$talk_context", tc_prison_break),
           (assign, "$talk_context", tc_escape),
           (assign, "$g_mt_mode", tcm_escape),
           (store_faction_of_party, ":town_faction", "$current_town"),
           (faction_get_slot, ":tier_2_troop", ":town_faction", slot_faction_tier_3_troop),
           (faction_get_slot, ":tier_3_troop", ":town_faction", slot_faction_tier_3_troop),
           (faction_get_slot, ":tier_4_troop", ":town_faction", slot_faction_tier_4_troop),
           (party_get_slot, ":town_scene", "$current_town", slot_town_center),
           (modify_visitors_at_site, ":town_scene"),
           (reset_visitors),
           #SB : TODO : take account slot_center_has_prisoner_tower
           #ideally we could alarm troops at locations
           (try_begin),
	         #if guards have not gone to some other important happening at nearby villages, then spawn 4 guards. (example : fire)
             (party_get_slot, ":last_nearby_fire_time", "$current_town", slot_town_last_nearby_fire_time),
             (store_current_hours, ":cur_time"),
             (store_add, ":fire_finish_time", ":last_nearby_fire_time", fire_duration),

             (neg|is_between, ":cur_time", ":last_nearby_fire_time", ":fire_finish_time"),
             (store_time_of_day, ":cur_day_hour"),
             (try_begin), #there are 6 guards at day time (no fire ext)
               (ge, ":cur_day_hour", 6),
               (lt, ":cur_day_hour", 22),
               (set_visitors, 25, ":tier_2_troop", 2),
               (set_visitors, 26, ":tier_2_troop", 1),
               (set_visitors, 27, ":tier_3_troop", 2),
               (set_visitors, 28, ":tier_4_troop", 1),
             (else_try),  #only 4 guards because of night
               (set_visitors, 25, ":tier_2_troop", 1),
               (set_visitors, 26, ":tier_2_troop", 1),
               (set_visitors, 27, ":tier_3_troop", 1),
               (set_visitors, 28, ":tier_4_troop", 1),
             (try_end),
           (else_try),
	         #if guards have gone to some other important happening at nearby villages, then spawn only 1 guard. (example : fire)
             (store_time_of_day, ":cur_day_hour"),
             (try_begin), #only 2 guard because there is a fire at one owned village
               (ge, ":cur_day_hour", 6),
               (lt, ":cur_day_hour", 22),
               (set_visitors, 25, ":tier_2_troop", 1),
               (set_visitors, 26, ":tier_2_troop", 0),
               (set_visitors, 27, ":tier_3_troop", 1),
               (set_visitors, 28, ":tier_4_troop", 0),
             (else_try), #only 1 guard because both night and there is a fire at one owned village
               (set_visitors, 25, ":tier_2_troop", 1),
               (set_visitors, 26, ":tier_2_troop", 0),
               (set_visitors, 27, ":tier_3_troop", 0),
               (set_visitors, 28, ":tier_4_troop", 0),
             (try_end),
           (try_end),
           (set_jump_mission,"mt_town_center"),
           (try_begin),
             (gt, "$sneaked_into_town", disguise_none), #setup disguise
             (assign, ":override_state", af_override_everything),
           (try_end),
           #SB : override disguise and set flags for entries
           (try_for_range, ":entry_no", 0, 8),
			 (eq, "$g_dplmc_player_disguise", 1),
             (gt, "$sneaked_into_town", disguise_none),
             (mission_tpl_entry_set_override_flags, "mt_town_center", ":entry_no", ":override_state"),
             (call_script, "script_set_disguise_override_items", "mt_town_center", ":entry_no", 1),
           (try_end),

           (jump_to_scene, ":town_scene"),
           (change_screen_mission),
            #If you're already at escape, then talk context will reset
         (else_try),
           (assign, "$talk_context", 0),
           (call_script, "script_cf_enter_center_location_bandit_check"),
           #All other circumstances...
         (else_try),
           (party_get_slot, ":town_scene", "$current_town", slot_town_center),
           (modify_visitors_at_site, ":town_scene"),
           (reset_visitors),
           (assign, "$g_mt_mode", tcm_default),
           (store_faction_of_party, ":town_faction","$current_town"),

           (try_begin),
             (neq, ":town_faction", "fac_player_supporters_faction"),
             (faction_get_slot, ":troop_prison_guard", "$g_encountered_party_faction", slot_faction_prison_guard_troop),
             (faction_get_slot, ":troop_castle_guard", "$g_encountered_party_faction", slot_faction_castle_guard_troop),
             (faction_get_slot, ":tier_2_troop", ":town_faction", slot_faction_tier_2_troop),
             (faction_get_slot, ":tier_3_troop", ":town_faction", slot_faction_tier_3_troop),
           (else_try),
             (party_get_slot, ":town_original_faction", "$current_town", slot_center_original_faction),
             (faction_get_slot, ":troop_prison_guard", ":town_original_faction", slot_faction_prison_guard_troop),
             (faction_get_slot, ":troop_castle_guard", ":town_original_faction", slot_faction_castle_guard_troop),
             (faction_get_slot, ":tier_2_troop", ":town_original_faction", slot_faction_tier_2_troop),
             (faction_get_slot, ":tier_3_troop", ":town_original_faction", slot_faction_tier_3_troop),
           (try_end),
           (try_begin), #think about this, should castle guard have to go nearby fire too? If he do not go, killing 2 armored guard is too hard for player. For now he goes too.
             #if guards have not gone to some other important happening at nearby villages, then spawn 4 guards. (example : fire)
             (party_get_slot, ":last_nearby_fire_time", "$current_town", slot_town_last_nearby_fire_time),
             (store_current_hours, ":cur_time"),
             (store_add, ":fire_finish_time", ":last_nearby_fire_time", fire_duration),

             (neg|is_between, ":cur_time", ":last_nearby_fire_time", ":fire_finish_time"),
             (set_visitor, 23, ":troop_castle_guard"),
           (try_end),
           (set_visitor, 24, ":troop_prison_guard"),

           (try_begin),
             (gt,":tier_2_troop", 0),
             (assign,reg0,":tier_3_troop"),
             (assign,reg1,":tier_3_troop"),
             (assign,reg2,":tier_2_troop"),
             (assign,reg3,":tier_2_troop"),
           (else_try),
             (assign,reg0,"trp_vaegir_infantry"),
             (assign,reg1,"trp_vaegir_infantry"),
             (assign,reg2,"trp_vaegir_archer"),
             (assign,reg3,"trp_vaegir_footman"),
           (try_end),
           (shuffle_range,0,4),

           (try_begin),
             #if guards have not gone to some other important happening at nearby villages, then spawn 4 guards. (example : fire)
             (party_get_slot, ":last_nearby_fire_time", "$current_town", slot_town_last_nearby_fire_time),
             (store_current_hours, ":cur_time"),
             (store_add, ":fire_finish_time", ":last_nearby_fire_time", fire_duration),

             (neg|is_between, ":cur_time", ":last_nearby_fire_time", ":fire_finish_time"),
             (set_visitor,25,reg0),
             (set_visitor,26,reg1),
             (set_visitor,27,reg2),
             (set_visitor,28,reg3),
           (try_end),

           (party_get_slot, ":spawned_troop", "$current_town", slot_town_armorer),
           (set_visitor, 9, ":spawned_troop"),
           (party_get_slot, ":spawned_troop", "$current_town", slot_town_weaponsmith),
           (set_visitor, 10, ":spawned_troop"),
           (party_get_slot, ":spawned_troop", "$current_town", slot_town_elder),
           (set_visitor, 11, ":spawned_troop"),
           (party_get_slot, ":spawned_troop", "$current_town", slot_town_horse_merchant),
           (set_visitor, 12, ":spawned_troop"),
           (call_script, "script_init_town_walkers"),
           (set_jump_mission,"mt_town_center"),
           (assign, ":override_state", af_override_horse),
           (try_begin),
             (gt, "$sneaked_into_town", disguise_none), #setup disguise
             (assign, ":override_state", af_override_everything),
           (try_end),
           #SB : override disguise and set flags for entries
           (try_for_range, ":entry_no", 0, 8),
			 (neq, ":entry_no", 1), #dckplmc: we want to ride our horses
             (mission_tpl_entry_set_override_flags, "mt_town_center", ":entry_no", ":override_state"),
             (call_script, "script_set_disguise_override_items", "mt_town_center", ":entry_no", 1),
           (try_end),

           (try_begin),
             (eq, "$town_entered", 0),
             (assign, "$town_entered", 1),
             (eq, "$town_nighttime", 0),
             (set_jump_entry, 1),
           (try_end),
           (jump_to_scene, ":town_scene"),
           (change_screen_mission),
         (try_end),
      ],"Door to the town center."),

      ("town_tavern",[
          (party_slot_eq,"$current_town",slot_party_type, spt_town),
          (this_or_next|eq,"$entry_to_town_forbidden",0),
          (gt, "$sneaked_into_town", disguise_none),
#          (party_get_slot, ":scene", "$current_town", slot_town_tavern),
#          (scene_slot_eq, ":scene", slot_scene_visited, 1), #check if scene has been visited before to allow entry from menu. Otherwise scene will only be accessible from the town center.
          ]
       ,"Visit the tavern.",
       [
           (try_begin),
             (eq,"$all_doors_locked",1),
             (display_message,"str_door_locked",message_locked),
           (else_try),
             (call_script, "script_cf_enter_center_location_bandit_check"),
           (else_try),
             (assign, "$town_entered", 1),
             (set_jump_mission, "mt_town_default"),
             (mission_tpl_entry_set_override_flags, "mt_town_default", 0, af_override_horse),
             (try_begin), #SB : adjust sneaking overrides
               (gt, "$sneaked_into_town", disguise_none),
               (mission_tpl_entry_set_override_flags, "mt_town_default", 0, af_override_everything),
               (call_script, "script_set_disguise_override_items", "mt_town_default", 0, 1), #need weaposn for tavern fights
             (try_end),
             (party_get_slot, ":cur_scene", "$current_town", slot_town_tavern),
             (jump_to_scene, ":cur_scene"),
             (scene_set_slot, ":cur_scene", slot_scene_visited, 1),

             (assign, "$talk_context", tc_tavern_talk),
             (call_script, "script_initialize_tavern_variables"),

             (store_random_in_range, ":randomize_attacker_placement", 0, 4),

             (modify_visitors_at_site, ":cur_scene"),
             (reset_visitors),

             (assign, ":cur_entry", 17),

			 #this is just a cheat right now
             #(troop_set_slot, "trp_belligerent_drunk", slot_troop_cur_center, "$g_encountered_party"),
			 (try_begin),
				(eq, "$cheat_mode", 1),
				(troop_get_slot, ":drunk_location", "trp_belligerent_drunk", slot_troop_cur_center),
				(try_begin),
					(eq, "$cheat_mode", 0),
				(else_try),
					(is_between, ":drunk_location", centers_begin, centers_end),
					(str_store_party_name, s4, ":drunk_location"),
					(display_message, "str_belligerent_drunk_in_s4"),
			    (else_try),
					(display_message, "str_belligerent_drunk_not_found"),
				(try_end),

				# (troop_get_slot, ":promoter_location", "trp_fight_promoter", slot_troop_cur_center),
				# (try_begin),
					# (eq, "$cheat_mode", 0),
				# (else_try),
					# (is_between, ":promoter_location", centers_begin, centers_end),
					# (str_store_party_name, s4, ":promoter_location"),
					# (display_message, "str_roughlooking_character_in_s4"),
			    # (else_try),
					# (display_message, "str_roughlooking_character_not_found"),
				# (try_end),
			 (try_end),

			 #this determines whether or not a lord who dislikes you will commission an assassin
			 (try_begin),
				(store_current_hours, ":hours"),
				(store_sub, ":hours_since_last_attempt", ":hours", "$g_last_assassination_attempt_time"),
				(gt, ":hours_since_last_attempt", 168),
				##diplomacy start+ Support ladies owning fiefs
				#(try_for_range, ":lord", active_npcs_begin, active_npcs_end),
				(try_for_range, ":lord", heroes_begin, heroes_end),
					(this_or_next|is_between, ":lord", active_npcs_begin, active_npcs_end),
						(troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
					#Make sure they're not retired or dead
					(neg|troop_slot_ge, ":lord", slot_troop_occupation, slto_retirement),
					#add support for non-noble personalities
					(this_or_next|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_ambitious),#"Lady MacBeth"
					(this_or_next|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_roguish),
					##diplomacy end+
					(troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_debauched),
					(troop_get_slot, ":led_party", ":lord", slot_troop_leaded_party),
					(party_is_active, ":led_party"),
					(party_get_attached_to, ":led_party_attached", ":led_party"),
					(eq, ":led_party_attached", "$g_encountered_party"),
					(call_script, "script_troop_get_relation_with_troop", "trp_player", ":lord"),
					(lt, reg0, -20),
					(assign, "$g_last_assassination_attempt_time", ":hours"),
#					(assign, "$g_last_assassination_attempt_location", "$g_encountered_party"),
#					(assign, "$g_last_assassination_attempt_perpetrator", ":lord"),

					(troop_set_slot, "trp_hired_assassin", slot_troop_cur_center, "$g_encountered_party"),
				(try_end),
				##diplomacy start+
				#"Lady MacBeth" noblewomen will also attempt to have people killed on their husbands' behalf.
				(lt, "$g_last_assassination_attempt_time", ":hours"),
				(neg|troop_slot_eq, "trp_hired_assassin", slot_troop_cur_center, "$g_encountered_party"),
				(try_for_range, ":lady", kingdom_ladies_begin, kingdom_ladies_end),
					(troop_slot_eq, ":lady", slot_troop_cur_center, "$g_encountered_party"),
					(troop_slot_eq, ":lady", slot_lord_reputation_type, lrep_ambitious),#"Lady MacBeth"
					(troop_slot_eq, ":lady", slot_troop_occupation, slto_kingdom_lady),

					(call_script, "script_troop_get_player_relation", ":lady"),
					(lt, reg0, 1),
					#Will send an assassin if she doesn't like the player, and either she or her husband
					#is at -20 or worse with the player.
					(try_begin),
						(ge, reg0, -20),
						(troop_slot_ge, ":lady", slot_troop_spouse, 1),
						(troop_get_slot, reg0, ":lady", slot_troop_spouse),
						(call_script, "script_troop_get_player_relation", reg0),
					(try_end),
					(lt, reg0, -20),

					(assign, "$g_last_assassination_attempt_time", ":hours"),
					(troop_set_slot, "trp_hired_assassin", slot_troop_cur_center, "$g_encountered_party"),
				(try_end),
				##diplomacy end+
			 (try_end),

			 (try_begin),
				 (eq, ":randomize_attacker_placement", 0),
				 (call_script, "script_setup_tavern_attacker", ":cur_entry"),

				 (val_add, ":cur_entry", 1),
			 (try_end),

			 # (try_begin),
				# (eq, 1, 0),
				# (troop_slot_eq, "trp_fight_promoter", slot_troop_cur_center, "$current_town"),
                # (set_visitor, ":cur_entry", "trp_fight_promoter"),

                # (val_add, ":cur_entry", 1),
			 # (try_end),

             (party_get_slot, ":mercenary_troop", "$current_town", slot_center_mercenary_troop_type),
             (party_get_slot, ":mercenary_amount", "$current_town", slot_center_mercenary_troop_amount),
             (try_begin),
			   (gt, ":mercenary_troop", 0),
               (gt, ":mercenary_amount", 0),
               (set_visitor, ":cur_entry", ":mercenary_troop"),
               (val_add, ":cur_entry", 1),
             (try_end),

			 (try_begin),
				 (eq, ":randomize_attacker_placement", 1),
				 (call_script, "script_setup_tavern_attacker", ":cur_entry"),
				 (val_add, ":cur_entry", 1),
			 (try_end),

             (try_for_range, ":companion_candidate", companions_begin, companions_end),
               (troop_slot_eq, ":companion_candidate", slot_troop_occupation, 0),
               (troop_slot_eq, ":companion_candidate", slot_troop_cur_center, "$current_town"),
			   (neg|troop_slot_ge, ":companion_candidate", slot_troop_prisoner_of_party, centers_begin),

               (set_visitor, ":cur_entry", ":companion_candidate"),

               (val_add, ":cur_entry", 1),
             (try_end),

			 (try_begin),
				 (eq, ":randomize_attacker_placement", 2),
				 (call_script, "script_setup_tavern_attacker", ":cur_entry"),
				 (val_add, ":cur_entry", 1),
			 (try_end),

             (try_begin), #this doubles the incidence of ransom brokers and (below) minstrels
               (party_get_slot, ":ransom_broker", "$current_town", slot_center_ransom_broker),
               (gt, ":ransom_broker", 0),

               # (assign, reg0, ":ransom_broker"),
               # (assign, reg1, "$current_town"),

               (set_visitor, ":cur_entry", ":ransom_broker"),
               (val_add, ":cur_entry", 1),
             (else_try), #SB : move to script call
               # (is_between, "$g_talk_troop", ransom_brokers_begin, ransom_brokers_end), #wtf is this
               (call_script, "script_cf_find_alternative_town_for_taverngoers", "$current_town", 9),
               (assign, ":alternative_town", reg0),

               (party_get_slot, ":ransom_broker", ":alternative_town", slot_center_ransom_broker),
               (gt, ":ransom_broker", 0),
               (is_between, ":ransom_broker", ransom_brokers_begin, ransom_brokers_end), #prevent ramun and galeas from spawning other towns

               (set_visitor, ":cur_entry", ":ransom_broker"),
               (val_add, ":cur_entry", 1),
             (try_end),

             (try_begin),
               (party_get_slot, ":tavern_traveler", "$current_town", slot_center_tavern_traveler),
               (gt, ":tavern_traveler", 0),
               (set_visitor, ":cur_entry", ":tavern_traveler"),
               (val_add, ":cur_entry", 1),
             (try_end),

             (try_begin),
               (party_get_slot, ":tavern_minstrel", "$current_town", slot_center_tavern_minstrel),
               (gt, ":tavern_minstrel", 0),

               (set_visitor, ":cur_entry", ":tavern_minstrel"),
               (val_add, ":cur_entry", 1),
             (else_try), #SB : move to script call
               (call_script, "script_cf_find_alternative_town_for_taverngoers", "$current_town", 9),
               (assign, ":alternative_town", reg0),
               (party_get_slot, ":tavern_minstrel", ":alternative_town", slot_center_tavern_minstrel),
               (gt, ":tavern_minstrel", 0),

               (set_visitor, ":cur_entry", ":tavern_minstrel"),
               (val_add, ":cur_entry", 1),
             (try_end),

             (try_begin),
               (party_get_slot, ":tavern_bookseller", "$current_town", slot_center_tavern_bookseller),
               (gt, ":tavern_bookseller", 0),
               (set_visitor, ":cur_entry", ":tavern_bookseller"),
               (val_add, ":cur_entry", 1),
             (try_end),

			 (try_begin),
				 (eq, ":randomize_attacker_placement", 3),
				 (call_script, "script_setup_tavern_attacker", ":cur_entry"),
				 (val_add, ":cur_entry", 1),
			 (try_end),

             (try_begin),
               (neg|check_quest_active, "qst_eliminate_bandits_infesting_village"),
               (neg|check_quest_active, "qst_deal_with_bandits_at_lords_village"),
               (assign, ":end_cond", villages_end),
               (try_for_range, ":cur_village", villages_begin, ":end_cond"),
                 (party_slot_eq, ":cur_village", slot_village_bound_center, "$current_town"),
                 (party_slot_ge, ":cur_village", slot_village_infested_by_bandits, 1),
                 (neg|party_slot_eq, ":cur_village", slot_town_lord, "trp_player"),
                 (set_visitor, ":cur_entry", "trp_farmer_from_bandit_village"),
                 (val_add, ":cur_entry", 1),
                 (assign, ":end_cond", 0),
               (try_end),
             (try_end),

             (try_begin),
               (eq, "$g_starting_town", "$current_town"),

               (this_or_next|neg|check_quest_finished, "qst_collect_men"),
               (this_or_next|neg|check_quest_finished, "qst_learn_where_merchant_brother_is"),
               (this_or_next|neg|check_quest_finished, "qst_save_relative_of_merchant"),
               (this_or_next|neg|check_quest_finished, "qst_save_town_from_bandits"),
               (eq,  "$g_do_one_more_meeting_with_merchant", 1),

               #SB : offset for merchant troop
               (call_script, "script_get_troop_of_merchant"),
               (set_visitor, ":cur_entry", reg0),
               (val_add, ":cur_entry", 1),
             (try_end),

			#dedal begin
			(party_get_slot, ":center_faction", "$current_town", slot_center_original_faction), #dckplmc - tavern patrons same culture as town
			(faction_get_slot, ":center_culture", ":center_faction", slot_faction_culture),
			(faction_get_slot, ":walker_troop_id", ":center_culture", slot_faction_town_walker_male_troop),
			(try_for_range,":entry",32,41),
						(store_random_in_range,":rand",0,2), #dckplmc - randomly male or female
						(store_add, ":town_walker", ":rand", ":walker_troop_id"),
						(store_random_in_range,":dna",0,1000),
						(mission_tpl_entry_clear_override_items,"mt_town_default",":entry"),
						(store_random_in_range,":r",0,10),
						(try_begin),
							(gt,":r",2),
							(mission_tpl_entry_add_override_item,"mt_town_default",":entry","itm_dedal_kufel"),
						(try_end),
						(set_visitor,":entry",":town_walker",":dna"),

                        (troop_set_slot, "trp_temp_array_c", ":entry", ":dna"),

			(try_end),
			#dedal end

             (change_screen_mission),
           (try_end),
        ],"Door to the tavern."),

#      ("town_smithy",[
#          (eq,"$entry_to_town_forbidden",0),
#          (eq,"$town_nighttime",0),
#          ],
#       "Visit the smithy.",
#       [
#           (set_jump_mission,"mt_town_default"),
#           (jump_to_scene,"$pout_scn_smithy"),
#           (change_screen_mission,0),
#        ]),


      ("town_merchant",
       [(party_slot_eq,"$current_town",slot_party_type, spt_town),
           (eq,"$town_nighttime",0),
           (this_or_next|eq,"$entry_to_town_forbidden",0),
           (gt, "$sneaked_into_town", disguise_none),
		   (eq, 1, 0), # Disabled for now because we're running out of space.
					   # Can still get here from the town scene.
#           (party_get_slot, ":scene", "$current_town", slot_town_store),
#           (scene_slot_eq, ":scene", slot_scene_visited, 1), #check if scene has been visited before to allow entry from menu. Otherwise scene will only be accessible from the town center.
           ],
       "Speak with the merchant.",
       [
           (try_begin),
             (this_or_next|eq,"$all_doors_locked",1),
             (eq,"$town_nighttime",1),
             (display_message,"str_door_locked",message_locked),
           (else_try),
             (assign, "$town_entered", 1),
             (set_jump_mission, "mt_town_default"),
             (mission_tpl_entry_set_override_flags, "mt_town_default", 0, af_override_horse),
             (try_begin),
               #(gt, "$sneaked_into_town", disguise_none),
               #(mission_tpl_entry_set_override_flags, "mt_town_default", 0, af_override_all),
               #SB : adjust sneaking overrides
               (gt, "$sneaked_into_town", disguise_none),
               (mission_tpl_entry_set_override_flags, "mt_town_default", 0, af_override_everything),
               (call_script, "script_set_disguise_override_items", "mt_town_default", 0, 1), #need weaposn for tavern fights
             (try_end),
             (party_get_slot, ":cur_scene", "$current_town", slot_town_store),
             (jump_to_scene, ":cur_scene"),
             (scene_set_slot, ":cur_scene", slot_scene_visited, 1),
             (change_screen_mission),
           (try_end),
        ],"Door to the shop."),

      ("town_arena",
       [(party_slot_eq,"$current_town",slot_party_type, spt_town),
        (eq, "$sneaked_into_town", 0),
#           (party_get_slot, ":scene", "$current_town", slot_town_arena),
#           (scene_slot_eq,  ":scene", slot_scene_visited, 1), #check if scene has been visited before to allow entry from menu. Otherwise scene will only be accessible from the town center.
           ],
       "Enter the arena.",
       [
           (try_begin),
             (this_or_next|eq,"$all_doors_locked",1),
             (eq,"$town_nighttime",1),
             (display_message,"str_door_locked",message_locked),
           (else_try),
             (assign, "$g_mt_mode", abm_visit),
             (assign, "$town_entered", 1),
             (set_jump_mission, "mt_arena_melee_fight"),
             (party_get_slot, ":arena_scene", "$current_town", slot_town_arena),
             (modify_visitors_at_site, ":arena_scene"),
             (reset_visitors),
             (set_visitor, 43, "trp_veteran_fighter"),
             (set_visitor, 44, "trp_hired_blade"),
             (set_jump_entry, 50),
             (jump_to_scene, ":arena_scene"),
             (scene_set_slot, ":arena_scene", slot_scene_visited, 1),
             (change_screen_mission),
           (try_end),
        ],"Door to the arena."),
      ("town_dungeon",
       #[(party_slot_eq, "$current_town", slot_town_lord, "trp_player"), #dckplmc: add quick access to dungeon for owner
	   [(eq, 1, 0),], # This was nice but we're running out of menus here.
       "Enter the prison.",
       [
           (try_begin),
		    (eq, "$talk_context", tc_prison_break),
			(gt, "$g_main_attacker_agent", 0),

		   	(neg|agent_is_alive, "$g_main_attacker_agent"),

			(agent_get_troop_id, ":agent_type", "$g_main_attacker_agent"),
			(try_begin),
			  (eq, "$g_encountered_party_faction", "fac_player_supporters_faction"),
			  (party_get_slot, ":prison_guard_faction", "$current_town", slot_center_original_faction),
			(else_try),
			  (assign, ":prison_guard_faction", "$g_encountered_party_faction"),
			(try_end),
			(faction_slot_eq, ":prison_guard_faction", slot_faction_prison_guard_troop, ":agent_type"),

			(call_script, "script_deduct_casualties_from_garrison"),
            (call_script, "script_enter_dungeon", "$current_town", "mt_visit_town_castle"),

		   (else_try),
             (eq,"$all_doors_locked",1),
             (display_message,"str_door_locked",message_locked),
           (else_try),
             (this_or_next|party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
             (eq, "$g_encountered_party_faction", "$players_kingdom"),
             (assign, "$town_entered", 1),
             (call_script, "script_enter_dungeon", "$current_town", "mt_visit_town_castle"),
           (else_try),
             (display_message,"str_door_locked",message_locked),
           (try_end),
        ],"Door to the dungeon."),

      ("castle_inspect",
      [
         (party_slot_eq,"$current_town",slot_party_type, spt_castle),
      ],
       "Take a walk around the courtyard.",
       [
         (try_begin),
           (eq, "$talk_context", tc_prison_break),
           (assign, "$talk_context", tc_escape),

           (party_get_slot, ":cur_castle_exterior", "$current_town", slot_castle_exterior),
           (modify_visitors_at_site, ":cur_castle_exterior"),
           (reset_visitors),

           (assign, ":guard_no", 40),

           (party_get_num_companion_stacks, ":num_stacks", "$g_encountered_party"),
           (try_for_range, ":troop_iterator", 0, ":num_stacks"),
             #nearby fire condition start
             (party_get_slot, ":last_nearby_fire_time", "$current_town", slot_town_last_nearby_fire_time),
             (store_current_hours, ":cur_time"),
             (store_add, ":fire_finish_time", ":last_nearby_fire_time", fire_duration),
             (this_or_next|eq, ":guard_no", 40),
             (neg|is_between, ":cur_time", ":last_nearby_fire_time", ":fire_finish_time"),
             #nearby fire condition end

             (lt, ":guard_no", 47),
             (party_stack_get_troop_id, ":cur_troop_id", "$g_encountered_party", ":troop_iterator"),
             (neg|troop_is_hero, ":cur_troop_id"),
             (party_stack_get_size, ":stack_size","$g_encountered_party",":troop_iterator"),
             (party_stack_get_num_wounded, ":num_wounded","$g_encountered_party",":troop_iterator"),
             (val_sub, ":stack_size", ":num_wounded"),
             (gt, ":stack_size", 0),
             (party_stack_get_troop_dna,":troop_dna", "$g_encountered_party", ":troop_iterator"),
             (set_visitor, ":guard_no", ":cur_troop_id", ":troop_dna"),
             (val_add, ":guard_no", 1),
           (try_end),
           #(set_jump_entry, 1),
           (set_visitor, 7, "trp_player"), #SB : g_player_troop back to trp_player

           (set_jump_mission,"mt_castle_visit"),

           (try_begin),
             (gt, "$sneaked_into_town", disguise_none), #setup disguise
             (assign, ":override_state", af_override_everything),
           (try_end),
           #SB : override disguise and set flags for entries
           (try_for_range, ":entry_no", 0, 8),
			 (eq, "$g_dplmc_player_disguise", 1),
             (gt, "$sneaked_into_town", disguise_none),
             (mission_tpl_entry_set_override_flags, "mt_castle_visit", ":entry_no", ":override_state"),
             (call_script, "script_set_disguise_override_items", "mt_castle_visit", ":entry_no", 1),
           (try_end),

           (jump_to_scene, ":cur_castle_exterior"),
           (change_screen_mission),
            #If you're already at escape, then talk context will reset
         (else_try),
           (assign, "$talk_context", tc_town_talk),

           (assign, "$g_mt_mode", tcm_default),

           (party_get_slot, ":cur_castle_exterior", "$current_town", slot_castle_exterior),
           (modify_visitors_at_site,":cur_castle_exterior"),
           (reset_visitors),

           (try_begin),
             (neq, "$g_encountered_party_faction", "fac_player_supporters_faction"),
             (faction_get_slot, ":troop_prison_guard", "$g_encountered_party_faction", slot_faction_prison_guard_troop),
           (else_try),
             (party_get_slot, ":town_original_faction", "$current_town", slot_center_original_faction),
             (faction_get_slot, ":troop_prison_guard", ":town_original_faction", slot_faction_prison_guard_troop),
           (try_end),
           (set_visitor, 24, ":troop_prison_guard"),

           (assign, ":guard_no", 40),

           (party_get_num_companion_stacks, ":num_stacks", "$g_encountered_party"),
           (try_for_range, ":troop_iterator", 0, ":num_stacks"),
             #nearby fire condition start
             (party_get_slot, ":last_nearby_fire_time", "$current_town", slot_town_last_nearby_fire_time),
             (store_current_hours, ":cur_time"),
             (store_add, ":fire_finish_time", ":last_nearby_fire_time", fire_duration),
             (neg|is_between, ":cur_time", ":fire_finish_time", ":last_nearby_fire_time"),

             (lt, ":guard_no", 47),
             (party_stack_get_troop_id, ":cur_troop_id", "$g_encountered_party", ":troop_iterator"),
             (neg|troop_is_hero, ":cur_troop_id"),
             (party_stack_get_size, ":stack_size","$g_encountered_party",":troop_iterator"),
             (party_stack_get_num_wounded, ":num_wounded","$g_encountered_party",":troop_iterator"),
             (val_sub, ":stack_size", ":num_wounded"),
             (gt, ":stack_size", 0),
             (party_stack_get_troop_dna,":troop_dna","$g_encountered_party",":troop_iterator"),
             (set_visitor, ":guard_no", ":cur_troop_id", ":troop_dna"),

             (val_add, ":guard_no", 1),
           (try_end),

           (try_begin),
             (eq, "$town_entered", 0),
             (assign, "$town_entered", 1),
           (try_end),
           (set_jump_entry, 1),

           (assign, ":override_state", af_override_horse),
           (try_begin),
             (gt, "$sneaked_into_town", disguise_none), #setup disguise
             (assign, ":override_state", af_override_everything),
           (try_end),
           (set_jump_mission, "mt_castle_visit"),

           #SB : populate disguise and set flags for entries
           (try_for_range, ":entry_no", 0, 8),
             (mission_tpl_entry_set_override_flags, "mt_castle_visit", ":entry_no", ":override_state"),
             (call_script, "script_set_disguise_override_items", "mt_castle_visit", ":entry_no", 1),
           (try_end),
           # (mission_tpl_entry_set_override_flags, "mt_castle_visit", 0, ":override_state"),
           # (mission_tpl_entry_set_override_flags, "mt_castle_visit", 1, ":override_state"),
           # (mission_tpl_entry_set_override_flags, "mt_castle_visit", 2, ":override_state"),
           # (mission_tpl_entry_set_override_flags, "mt_castle_visit", 3, ":override_state"),
           # (mission_tpl_entry_set_override_flags, "mt_castle_visit", 4, ":override_state"),
           # (mission_tpl_entry_set_override_flags, "mt_castle_visit", 5, ":override_state"),
           # (mission_tpl_entry_set_override_flags, "mt_castle_visit", 6, ":override_state"),
           # (mission_tpl_entry_set_override_flags, "mt_castle_visit", 7, ":override_state"),

           (jump_to_scene, ":cur_castle_exterior"),
           (change_screen_mission),
         (try_end),
        ], "To the castle courtyard."),

     ("town_enterprise",
      [
        (party_slot_eq,"$current_town",slot_party_type, spt_town),
        (party_get_slot, ":item_produced", "$current_town", slot_center_player_enterprise),
		(gt, ":item_produced", 1),
        (eq,"$entry_to_town_forbidden",0),
		(call_script, "script_get_enterprise_name", ":item_produced"),
		(str_store_string, s3, reg0),
      ],
      "Visit your {s3}.",
      [
        (store_sub, ":town_order", "$current_town", towns_begin),
		(store_add, ":master_craftsman", "trp_town_1_master_craftsman", ":town_order"),
        (party_get_slot, ":item_produced", "$current_town", slot_center_player_enterprise),
		(assign, ":enterprise_scene", "scn_enterprise_mill"),
		(try_begin),
			(eq, ":item_produced", "itm_bread"),
			(assign, ":enterprise_scene", "scn_enterprise_mill"),
		(else_try),
			(eq, ":item_produced", "itm_ale"),
			(assign, ":enterprise_scene", "scn_enterprise_brewery"),
		(else_try),
			(eq, ":item_produced", "itm_oil"),
			(assign, ":enterprise_scene", "scn_enterprise_oil_press"),
		(else_try),
			(eq, ":item_produced", "itm_wine"),
			(assign, ":enterprise_scene", "scn_enterprise_winery"),
		(else_try),
			(eq, ":item_produced", "itm_leatherwork"),
			(assign, ":enterprise_scene", "scn_enterprise_tannery"),
		(else_try),
			(eq, ":item_produced", "itm_wool_cloth"),
			(assign, ":enterprise_scene", "scn_enterprise_wool_weavery"),
		(else_try),
			(eq, ":item_produced", "itm_linen"),
			(assign, ":enterprise_scene", "scn_enterprise_linen_weavery"),
		(else_try),
			(eq, ":item_produced", "itm_velvet"),
			(assign, ":enterprise_scene", "scn_enterprise_dyeworks"),
		(else_try),
			(eq, ":item_produced", "itm_tools"),
			(assign, ":enterprise_scene", "scn_enterprise_smithy"),
		(try_end),
        (modify_visitors_at_site,":enterprise_scene"),
		(reset_visitors),
        (set_visitor,0,"trp_player"),
        (set_visitor,17,":master_craftsman"),
        (set_jump_mission,"mt_town_default"),
        (jump_to_scene,":enterprise_scene"),
        (change_screen_mission),
      ],"Door to your enterprise."),

     ("town_brothel",
      [
        (party_slot_eq,"$current_town",slot_party_type, spt_town),
        (party_slot_eq, "$current_town", slot_town_has_brothel, 1),
        (eq,"$entry_to_town_forbidden",0),
      ],
      "Visit your tavern and bath-house.",
      [
        (assign, "$talk_context", tc_tavern_talk),

        (troop_set_type, "trp_brothel_madam", 1), #savegames
        (troop_set_type, "trp_prostitute", 3),
        (troop_set_type, "trp_courtesan", 3),
        (troop_set_type, "trp_townsman", 2),

        (modify_visitors_at_site,"scn_tavern"),
		(reset_visitors),
        (set_visitor,0,"trp_player"),
        (set_visitor,9,"trp_brothel_madam"),

        #dedal begin
        (party_get_slot, ":center_faction", "$current_town", slot_center_original_faction), #dckplmc - tavern patrons same culture as town
        (faction_get_slot, ":center_culture", ":center_faction", slot_faction_culture),
        (faction_get_slot, ":walker_troop_id", ":center_culture", slot_faction_town_walker_male_troop),
        (try_for_range,":entry",1,11),
            (neq, ":entry", 9),
            (store_random_in_range,":dna",0,1000),
            (mission_tpl_entry_clear_override_items,"mt_brothel",":entry"),
            (store_random_in_range,":r",0,10),
            (try_begin),
                (gt,":r",2),
                (mission_tpl_entry_add_override_item,"mt_brothel",":entry","itm_dedal_kufel"),
            (try_end),
            (set_visitor,":entry",":walker_troop_id",":dna"),

            (troop_set_slot, "trp_temp_array_c", ":entry", ":dna"),
        (try_end),
        #dedal end


        (assign, ":cur_entry", 40),
        (try_for_range, ":lady", heroes_begin, heroes_end),
            (try_begin),
                (gt, ":cur_entry", 25),
                (troop_slot_eq, ":lady", slot_troop_courtesan, "$g_encountered_party"),
                (troop_set_type, ":lady", 3),
                (set_visitor, ":cur_entry",":lady",),
                (val_add, ":cur_entry", 1),
                (set_visitor, ":cur_entry","trp_townsman"),
                (val_add, ":cur_entry", 1),
                (try_begin),
                    (ge, ":cur_entry", 48),
                    (assign, ":cur_entry", 18),
                (try_end),
            (else_try),
                (lt, ":cur_entry", 25),
                (troop_slot_eq, ":lady", slot_troop_courtesan, "$g_encountered_party"),
                (troop_set_type, ":lady", 3),
                (set_visitor, ":cur_entry",":lady",),
                (val_add, ":cur_entry", 1),
            (try_end),
        (try_end),

        (party_get_slot, ":num_workers", "$current_town", slot_town_brothel_num_workers),

        (try_for_range, ":worker", 0, 12),
            (try_begin),
                (gt, ":cur_entry", 25),
                (gt, ":num_workers", 0),
                (store_random_in_range,":dna",0,1000),
                (set_visitor, ":cur_entry","trp_prostitute",":dna"),
                (troop_set_slot, "trp_temp_array_c", ":cur_entry", ":dna"),
                (val_sub, ":num_workers", 1),
                (val_add, ":cur_entry", 1),
                (set_visitor, ":cur_entry","trp_townsman"),
                (val_add, ":cur_entry", 1),
                (try_begin),
                    (ge, ":cur_entry", 48),
                    (assign, ":cur_entry", 18),
                (try_end),
            (else_try),
                (lt, ":cur_entry", 25),
                (gt, ":num_workers", 0),
                (store_random_in_range,":dna",0,1000),
                (set_visitor, ":cur_entry","trp_prostitute",":dna"),
                (troop_set_slot, "trp_temp_array_c", ":cur_entry", ":dna"),
                (val_sub, ":num_workers", 1),
                (val_add, ":cur_entry", 1),
            (try_end),
        (try_end),

        (assign, ":cur_entry", 17),

        (store_random_in_range, ":minstrel_troop",tavern_minstrels_begin,tavern_minstrels_end),
        (set_visitor, ":cur_entry",":minstrel_troop"),
        (val_add, ":cur_entry", 1),

        (set_jump_mission,"mt_brothel"),
        (jump_to_scene,"scn_tavern"),
        (change_screen_mission),
      ],"Door to your enterprise."),

    ("visit_lady",
	[

  (this_or_next|eq, "$g_polygamy", 1),
	(neg|troop_slot_ge, "trp_player", slot_troop_spouse, kingdom_ladies_begin),

	(assign, "$love_interest_in_town", 0),
	(assign, "$love_interest_in_town_2", 0),
	(assign, "$love_interest_in_town_3", 0),
	(assign, "$love_interest_in_town_4", 0),
	(assign, "$love_interest_in_town_5", 0),
	(assign, "$love_interest_in_town_6", 0),
	(assign, "$love_interest_in_town_7", 0),
	(assign, "$love_interest_in_town_8", 0),

	(try_for_range, ":lady_no", kingdom_ladies_begin, kingdom_ladies_end),
		(troop_slot_eq, ":lady_no", slot_troop_cur_center, "$current_town"),
		(call_script, "script_get_kingdom_lady_social_determinants", ":lady_no"),
		(assign, ":lady_guardian", reg0),

		(troop_slot_eq, ":lady_no", slot_troop_spouse, -1),
		(ge, ":lady_guardian", 0), #not sure when this would not be the case


		#must have spoken to either father or lady
		(this_or_next|troop_slot_ge, ":lady_no", slot_troop_met, 2),
			(troop_slot_eq, ":lady_guardian", slot_lord_granted_courtship_permission, 1),

		(neg|troop_slot_eq, ":lady_no", slot_troop_met, 4),

		#must have approached father
#		(this_or_next|troop_slot_eq, ":lady_guardian", slot_lord_granted_courtship_permission, 1),
#			(troop_slot_eq, ":lady_guardian", slot_lord_granted_courtship_permission, -1),


		(try_begin),
			(eq, "$love_interest_in_town", 0),
			(assign, "$love_interest_in_town", ":lady_no"),
		(else_try),
			(eq, "$love_interest_in_town_2", 0),
			(assign, "$love_interest_in_town_2", ":lady_no"),
		(else_try),
			(eq, "$love_interest_in_town_3", 0),
			(assign, "$love_interest_in_town_3", ":lady_no"),
		(else_try),
			(eq, "$love_interest_in_town_4", 0),
			(assign, "$love_interest_in_town_4", ":lady_no"),
		(else_try),
			(eq, "$love_interest_in_town_5", 0),
			(assign, "$love_interest_in_town_5", ":lady_no"),
		(else_try),
			(eq, "$love_interest_in_town_6", 0),
			(assign, "$love_interest_in_town_6", ":lady_no"),
		(else_try),
			(eq, "$love_interest_in_town_7", 0),
			(assign, "$love_interest_in_town_7", ":lady_no"),
		(else_try),
			(eq, "$love_interest_in_town_8", 0),
			(assign, "$love_interest_in_town_8", ":lady_no"),
		(try_end),
	(try_end),

	(gt, "$love_interest_in_town", 0),
	],
	  "Attempt to visit a lady",
       [
        (jump_to_menu, "mnu_lady_visit"),
        ], "Door to the garden."),

      ("trade_with_merchants",
       [
           (party_slot_eq,"$current_town",slot_party_type, spt_town)
        ],
         "Go to the marketplace.",
         [
           (try_begin),
             (call_script, "script_cf_enter_center_location_bandit_check"),
           (else_try),
             (jump_to_menu,"mnu_town_trade"),
           (try_end),
          ]),


      ("manage_this_town",
      [
             (party_slot_eq, "$current_town", slot_party_type, spt_town)
       ],
       "Go to the guild district.",
      [
       (jump_to_menu,"mnu_dickplo_town_manage"),
      ]),


      ("walled_center_manage",
      [
        (neg|party_slot_eq, "$current_town", slot_village_state, svs_under_siege),
        (party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
        (assign, reg0, 1),
        (try_begin),
          (party_slot_eq, "$current_town", slot_party_type, spt_castle),
          (assign, reg0, 0),
        (try_end),
       ],
       "Manage this {reg0?town:castle}.",
       [
           (assign, "$g_next_menu", "mnu_town"),
           (jump_to_menu, "mnu_center_manage"),
       ]),

      ("castle_station_troops",
      [
		(party_get_slot, ":town_lord", "$current_town", slot_town_lord),
	    (str_clear, s10),

	    (assign, ":player_can_draw_from_garrison", 0),
		(try_begin), #option 1 - player is town lord
		  (eq, ":town_lord", "trp_player"),
		  (assign, ":player_can_draw_from_garrison", 1),
		(else_try), #option 2 - town is unassigned and part of the player faction
		  (store_faction_of_party, ":faction", "$g_encountered_party"),
		  (eq, ":faction", "fac_player_supporters_faction"),
		  (neg|party_slot_ge, "$g_encountered_party", slot_town_lord, active_npcs_begin), #ie, zero or -1

		  (assign, ":player_can_draw_from_garrison", 1),
		(else_try), #option 3 - town was captured by player
		  (lt, ":town_lord", 0), #ie, unassigned
		  (store_faction_of_party, ":castle_faction", "$g_encountered_party"),
		  (eq, "$players_kingdom", ":castle_faction"),

		  (eq, "$g_encountered_party", "$g_castle_requested_by_player"),

		  (str_store_string, s10, "str_retrieve_garrison_warning"),
		  (assign, ":player_can_draw_from_garrison", 1),
		(else_try),
		  (lt, ":town_lord", 0), #ie, unassigned
		  (store_faction_of_party, ":castle_faction", "$g_encountered_party"),
		  (eq, "$players_kingdom", ":castle_faction"),

		  (store_party_size_wo_prisoners, ":party_size", "$g_encountered_party"),
		  (eq, ":party_size", 0),

		  (str_store_string, s10, "str_retrieve_garrison_warning"),
		  (assign, ":player_can_draw_from_garrison", 1),
		(else_try),
		  (party_slot_ge, "$g_encountered_party", slot_town_lord, active_npcs_begin),
		  (store_faction_of_party, ":castle_faction", "$g_encountered_party"),
		  (eq, "$players_kingdom", ":castle_faction"),
		  ##diplomacy start+ can arise if using this to represent polygamy
		  (this_or_next|troop_slot_eq, ":town_lord", slot_troop_spouse, "trp_player"),
		     (troop_slot_eq, "trp_player", slot_troop_spouse, ":town_lord"),
		  (this_or_next|is_between, ":town_lord", heroes_begin, heroes_end),
		  ##diplomacy end+
		  (troop_slot_eq, "trp_player", slot_troop_spouse, ":town_lord"),

		  (assign, ":player_can_draw_from_garrison", 1),
		(try_end),

        (eq, ":player_can_draw_from_garrison", 1),
      ],
      "Manage the garrison {s10}",
      [
        (troop_set_slot, "trp_temp_array_d", slot_adv_transfer_mode, 12),
        (change_screen_exchange_members,1),
      ]),
	  ##diplomacy start+
	  #Other option to add troops to garrison
      ("dplmc_castle_give_troops",
      [
		(party_get_slot, ":town_lord", "$current_town", slot_town_lord),
		(store_faction_of_party, ":castle_faction", "$g_encountered_party"),
		(is_between, ":castle_faction", kingdoms_begin, kingdoms_end),

		#The player can add troops but not remove them:
		#Not owned by the player
		(neq, ":town_lord", "trp_player"),
		#Not unassigned
		(ge, ":town_lord", heroes_begin),
		#Not owned by the player's spouse
		(neg|troop_slot_eq, "trp_player", slot_troop_spouse, ":town_lord"),
		(neg|troop_slot_eq, ":town_lord", slot_troop_spouse, "trp_player"),
		#But nevertheless the owner will accept troops
		(call_script, "script_dplmc_player_can_give_troops_to_troop", ":town_lord"),

        (ge, reg0, 1),
      ],
      "Give troops to the garrison (cannot remove)",
      [
        (change_screen_give_members, "$current_town"),
      ]),
      ##diplomacy end+

      ("castle_wait",
      [
        #(party_slot_eq,"$current_town",slot_party_type, spt_castle),
        (this_or_next|ge, "$g_encountered_party_relation", 0),
        (eq,"$castle_undefended",1),
        (assign, ":can_rest", 1),
        (str_clear, s1),
        (try_begin),
          (neg|party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
          (troop_get_slot, ":player_spouse", "trp_player", slot_troop_spouse),
          (neg|party_slot_eq, "$current_town", slot_town_lord, ":player_spouse"),

          (party_slot_ge, "$current_town", slot_town_lord, "trp_player"), #can rest for free in castles and towns with unassigned lords
          (store_faction_of_party, ":current_town_faction", "$current_town"),
          (neq, ":current_town_faction", "fac_player_supporters_faction"),
          (party_get_num_companions, ":num_men", "p_main_party"),
          (store_div, reg1, ":num_men", 4),
          (val_add, reg1, 1),
          (str_store_string, s1, "@ ({reg1} denars per night)"),
          (store_troop_gold, ":gold", "trp_player"),
          (lt, ":gold", reg1),
          (assign, ":can_rest", 0),
        (try_end),
        (eq, ":can_rest", 1),
      ],
      "Wait here for some time{s1}.",
      [
        (assign, "$auto_enter_town", "$current_town"),
        (assign, "$g_town_visit_after_rest", 1),
        (assign, "$g_last_rest_center", "$current_town"),
        (assign, "$g_last_rest_payment_until", -1),

        (try_begin),
          (party_is_active, "p_main_party"),
          (party_get_current_terrain, ":cur_terrain", "p_main_party"),
          (try_begin),
            (eq, ":cur_terrain", rt_desert),
            (unlock_achievement, ACHIEVEMENT_SARRANIDIAN_NIGHTS),
          (try_end),
        (try_end),

        (rest_for_hours_interactive, 24 * 7, 5, 0), #rest while not attackable
        (change_screen_return),
      ]),

##      ("rest_until_morning",
##       [
##           (this_or_next|ge, "$g_encountered_party_relation", 0),
##           (eq,"$castle_undefended",1),
##           (store_time_of_day,reg(1)),(neg|is_between,reg(1), 5, 18),
##           (eq, "$g_defending_against_siege", 0),
##        ],
##         "Rest until morning.",
##         [
##           (store_time_of_day,reg(1)),
##           (assign, reg(2), 30),
##           (val_sub,reg(2),reg(1)),
##           (val_mod,reg(2),24),
##           (assign,"$auto_enter_town","$current_town"),
##           (assign, "$g_town_visit_after_rest", 1),
##           (rest_for_hours_interactive, reg(2)),
##           (change_screen_return),
##          ]),
##
##      ("rest_until_evening",
##       [
##           (this_or_next|ge, "$g_encountered_party_relation", 0),
##           (eq,"$castle_undefended",1),
##           (store_time_of_day,reg(1)), (is_between,reg(1), 5, 18),
##           (eq, "$g_defending_against_siege", 0),
##        ],
##         "Rest until evening.",
##         [
##           (store_time_of_day,reg(1)),
##           (assign, reg(2), 20),
##           (val_sub,reg(2),reg(1)),
##           (assign,"$auto_enter_town","$current_town"),
##           (assign, "$g_town_visit_after_rest", 1),
##           (rest_for_hours_interactive, reg(2)),
##           (change_screen_return),
##          ]),
      # ("town_alley",
      # [
        # (party_slot_eq,"$current_town",slot_party_type, spt_town),
        # (eq, "$cheat_mode", 1),
      # ],
      # "{!}CHEAT: Go to the alley.",
      # [
        # (party_get_slot, reg11, "$current_town", slot_town_alley),
        # (set_jump_mission, "mt_ai_training"),
        # (jump_to_scene, reg11),
        # (change_screen_mission),
      # ]),

      ("collect_taxes_qst",
      [
        (check_quest_active, "qst_collect_taxes"),
        (quest_slot_eq, "qst_collect_taxes", slot_quest_target_center, "$current_town"),
        (neg|quest_slot_eq, "qst_collect_taxes", slot_quest_current_state, 4),
        (quest_get_slot, ":quest_giver_troop", "qst_collect_taxes", slot_quest_giver_troop),
        (str_store_troop_name, s1, ":quest_giver_troop"),
        (quest_get_slot, reg5, "qst_collect_taxes", slot_quest_current_state),
      ],
      "{reg5?Continue collecting taxes:Collect taxes} due to {s1}.",
      [
        (jump_to_menu, "mnu_collect_taxes"),
      ]),

      ("sail_from_port",
      [
        (party_slot_ge, "$current_town", slot_town_port, "p_port_1"),
      ],
      "Visit the Shipyard.",
      [
        (jump_to_menu, "mnu_buy_ship"),
      ]),

      #SB : consolidated cheat options
      ("town_cheat", [(ge, "$cheat_mode", 1),],
      "Use cheats.",
      [(jump_to_menu, "mnu_town_cheats"),
      ]),
      # ("castle_cheat_interior",
      # [
        # (eq, "$cheat_mode", 1),
      # ],
      # "{!}CHEAT! Interior.",
      # [
        # (set_jump_mission,"mt_ai_training"),
        # (party_get_slot, ":castle_scene", "$current_town", slot_town_castle),
        # (jump_to_scene,":castle_scene"),
        # (change_screen_mission),
      # ]),

      # ("castle_cheat_town_exterior",
      # [
        # (eq, "$cheat_mode", 1),
      # ],
      # "{!}CHEAT! Exterior.",
      # [
        # (try_begin),
          # (party_slot_eq, "$current_town",slot_party_type, spt_castle),
          # (party_get_slot, ":scene", "$current_town", slot_castle_exterior),
        # (else_try),
          # (party_get_slot, ":scene", "$current_town", slot_town_center),
        # (try_end),
        # (set_jump_mission,"mt_ai_training"),
        # (jump_to_scene,":scene"),
        # (change_screen_mission),
      # ]),

      # ("castle_cheat_dungeon",
      # [
        # (eq, "$cheat_mode", 1),
      # ],
      # "{!}CHEAT! Prison.",
      # [
        # (set_jump_mission,"mt_ai_training"),
        # (party_get_slot, ":castle_scene", "$current_town", slot_town_prison),
        # (jump_to_scene,":castle_scene"),
        # (change_screen_mission),
      # ]),

      # ("castle_cheat_town_walls",
      # [
        # (eq, "$cheat_mode", 1),
        # (party_slot_eq,"$current_town",slot_party_type, spt_town),
      # ],
      # "{!}CHEAT! Town Walls.",
      # [
        # (party_get_slot, ":scene", "$current_town", slot_town_walls),
        # (set_jump_mission,"mt_ai_training"),
        # (jump_to_scene,":scene"),
        # (change_screen_mission),
      # ]),

      # ("cheat_town_start_siege",
      # [
        # (eq, "$cheat_mode", 1),
        # (party_slot_eq, "$g_encountered_party", slot_center_is_besieged_by, -1),
        # (lt, "$g_encountered_party_2", 1),
        # (call_script, "script_party_count_fit_for_battle","p_main_party"),
        # (gt, reg(0), 1),
        # (try_begin),
          # (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
          # (assign, reg6, 1),
        # (else_try),
          # (assign, reg6, 0),
        # (try_end),
      # ],
      # "{!}CHEAT: Besiege the {reg6?town:castle}...",
      # [
        # (assign,"$g_player_besiege_town","$g_encountered_party"),
        # (jump_to_menu, "mnu_castle_besiege"),
      # ]),

      # ("center_reports",
      # [
        # (eq, "$cheat_mode", 1),
      # ],
      # "{!}CHEAT! Show reports.",
      # [
        # (jump_to_menu,"mnu_center_reports"),
      # ]),

      # ("sail_from_port",
      # [
        # (party_slot_eq,"$current_town",slot_party_type, spt_town),
        # (eq, "$cheat_mode", 1),
        # #(party_slot_eq,"$current_town",slot_town_near_shore, 1),
      # ],
      # "{!}CHEAT: Sail from port.",
      # [
        # (assign, "$g_player_icon_state", pis_ship),
        # (party_set_flags, "p_main_party", pf_is_ship, 1),
        # (party_get_position, pos1, "p_main_party"),
        # (map_get_water_position_around_position, pos2, pos1, 6),
        # (party_set_position, "p_main_party", pos2),
        # (assign, "$g_main_ship_party", -1),
        # (change_screen_return),
      # ]),

	  # For consistency's sake this should always be the bottom option.
      ("town_leave",[],"Leave...",
      [
	  (assign, "$g_permitted_to_center",0),
      (try_begin), # Disguise only gets removed from this screen, should probably just copy it to here or make it a script at some point, but this is faster.
		 (gt, "$sneaked_into_town", disguise_none),
		 (assign, "$new_encounter", 1),
		 (jump_to_menu,"mnu_castle_outside"),
	  (else_try),
        (change_screen_return,0),
	  (try_end),
		##diplomacy start+
		#Porting rubik's autobuy/autosell from Custom Commander
		(try_begin),
		  (eq, "$sneaked_into_town", disguise_none), #SB : disable while disguised
		  (neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
		  (call_script, "script_dplmc_initialize_autoloot", 0),#argument "0" means this does nothing if deemed unnecessary
		  (try_begin),
			(eq, "$g_dplmc_buy_food_when_leaving", 1),
			(party_get_slot, ":merchant_troop", "$current_town", slot_town_merchant),
			(gt, ":merchant_troop", 0),
			(call_script, "script_dplmc_auto_buy_food", "trp_player", ":merchant_troop"),
		  (try_end),
		  (try_begin),
			(eq, "$g_dplmc_sell_items_when_leaving", 1),
			(call_script, "script_dplmc_player_auto_sell_at_center", "$current_town"),
		  (try_end),
      #AutoTrade Begin
      #Automatically buy and sell trade goods with this town if enabled
      (try_begin),
        (eq, "$g_auto_trade_items_when_leaving", 1),
        (call_script, "script_auto_trade_at_center", "$current_town"),
      (try_end),
      #AutoTrade End
		(else_try), #SB : process leaving town guard check
          (gt, "$sneaked_into_town", disguise_none),
        (try_end),
		##diplomacy end+
      ],"Leave Area."),
    ]
   )
]
