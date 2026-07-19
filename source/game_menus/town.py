# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

town_menus = [
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
   ),
  (
    "town_trade",0,
    "The marketplace is home to shops, inns, warehouses, and merchant hubs. Coming upon the main plaza, you decide where you will go...",
    "none",
    [
                (try_begin),
                (party_get_slot, ":center_lord", "$current_town", slot_town_lord),
                (ge, ":center_lord", 0),
                (set_fixed_point_multiplier, 100),
                (position_set_x, pos1, 70),
                (position_set_y, pos1, 5),
                (position_set_z, pos1, 75),
                (set_game_menu_tableau_mesh, "tableau_troop_note_mesh", ":center_lord", pos1),
                (try_end),],
    [
      #SB : re-order dialog options for consistency, add talk instead of trade option
		##diplomacy start+
		#Begin auto-sell, credit rubik (Custom Commander)
      ## CC
      ("auto_sell",[],
       "Sell items automatically.",
       [
          (assign, "$g_next_menu", "mnu_town"),
          (jump_to_menu,"mnu_dplmc_trade_auto_sell_begin"),
        ]),

      ("auto_buy_food",[
	  (eq,1,0), #Disabled because, again, running out of space. Also this is pretty pointless who uses it.
	  ],
       "Buy food automatically.",
       [
          (assign, "$g_next_menu", "mnu_town"),
          (jump_to_menu,"mnu_dplmc_trade_auto_buy_food_begin"),
        ]),

      ## CC
		#End auto-sell, credit rubik (Custom Commander)
		##diplomacy start+
      ("assess_prices",
       [
         (store_faction_of_party, ":current_town_faction", "$current_town"),
         (store_relation, ":reln", ":current_town_faction", "fac_player_supporters_faction"),
         (ge, ":reln", 0),
         ],
       "Assess the local prices.",
       [
           (jump_to_menu,"mnu_town_trade_assessment_begin"),
        ]),

      ("trade_with_arms_merchant",[(party_slot_ge, "$current_town", slot_town_weaponsmith, 1)],
       "Trade with the arms merchant.",
       [
            (party_get_slot, ":merchant_troop", "$current_town", slot_town_weaponsmith),
            (assign, "$g_talk_troop", ":merchant_troop"),
            (try_begin),
              (this_or_next|key_is_down, key_left_shift),
              (key_is_down, key_right_shift),
              (call_script, "script_start_town_conversation", slot_town_weaponsmith, 10),
            (else_try),
              (troop_set_slot, ":merchant_troop", slot_troop_met, 1),
              (change_screen_trade, ":merchant_troop"),
            (try_end),
        ]),
      ("trade_with_armor_merchant",[(party_slot_ge, "$current_town", slot_town_armorer, 1)],
       "Trade with the armor merchant.",
       [
            (party_get_slot, ":merchant_troop", "$current_town", slot_town_armorer),
            (assign, "$g_talk_troop", ":merchant_troop"),
            (try_begin),
              (this_or_next|key_is_down, key_left_shift),
              (key_is_down, key_right_shift),
              (call_script, "script_start_town_conversation", slot_town_armorer, 9),
            (else_try),
              (troop_set_slot, ":merchant_troop", slot_troop_met, 1),
              (change_screen_trade, ":merchant_troop"),
            (try_end),
        ]),
      ("trade_with_horse_merchant",[(party_slot_ge, "$current_town", slot_town_horse_merchant, 1)],
       "Trade with the horse merchant.",
       [
            (party_get_slot, ":merchant_troop", "$current_town", slot_town_horse_merchant),
            (try_begin),
              (this_or_next|key_is_down, key_left_shift),
              (key_is_down, key_right_shift),
              (call_script, "script_start_town_conversation", slot_town_horse_merchant, 12),
            (else_try),
              (troop_set_slot, ":merchant_troop", slot_troop_met, 1),
              (change_screen_trade, ":merchant_troop"),
            (try_end),
        ]),
      ("trade_with_goods_merchant",[(party_slot_ge, "$current_town", slot_town_merchant, 1)],
       "Trade with the goods merchant.",
       [
            (party_get_slot, ":merchant_troop", "$current_town", slot_town_merchant),
            (assign, "$g_talk_troop", ":merchant_troop"),
            (try_begin),
              (this_or_next|key_is_down, key_left_shift),
              (key_is_down, key_right_shift),
              (call_script, "script_start_town_conversation", slot_town_merchant, 9),
            (else_try),
              (troop_set_slot, ":merchant_troop", slot_troop_met, 1),
              (change_screen_trade, ":merchant_troop"),
            (try_end),
        ]),
      #Autotrade begin
      ("auto_Trade",[],
       "Buy and sell trade goods automatically.",
       [
          (assign, "$g_next_menu", "mnu_town"),
          (jump_to_menu,"mnu_auto_trade"),
        ]),
      #Autotrade end
      ("back_to_town_menu",[],"Head back.",
       [
           (jump_to_menu,"mnu_town"),
        ]),
    ]
  ),


   (
     "dickplo_town_manage",0,
     "The business district is full of opportunities to take advantage of.",
     "none",
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

     ],
     [
 	#	Floris Bank Overhaul	//	Original Idea by Lazeras
 	("town_bank",
        [(party_slot_eq, "$current_town", slot_party_type, spt_town)],
        "Visit the landlords and moneylenders.",
        [
 			(assign, reg10, 0),
 			(start_presentation, "prsnt_bank"),
         ]),

#Troop hiring menu
       ("hire_troops",[],
        "Look to hire some mercenaries.",## You have added a new menu.
        [
            (jump_to_menu,"mnu_town_pre_hire_troops"),
         ]),

      ##diplomacy begin
      ("dplmc_guild_master_meeting",
       [
       (party_slot_eq,"$current_town",slot_party_type, spt_town),
	   ],
       "Meet the Guild Master.",
        [
          (try_begin),
            (call_script, "script_cf_enter_center_location_bandit_check"),
          (else_try), #SB : unified script call
            (call_script, "script_start_town_conversation", slot_town_elder, 11),
          (try_end),
     ]),
       ##diplomacy end


       ("back_to_town_menu",[],"Head back.",
        [
            (jump_to_menu,"mnu_town"),
         ]),
     ]
   ),

##diplomacy start+
##Begin auto-sell credit rubik (Custom Commander)
##Altered to only sell items from the player's inventory, not his companions'.
#
#Uses global variable $g_auto_sell_price_limit changed to $g_dplmc_auto_sell_price_limit
## CC,
  (
    "dplmc_trade_auto_sell_begin",0,
    "Items in your inventory whose type is marked as sellable and whose prices \
are below {reg1} denars will be sold to the {reg2?appropriate merchants:elder} \
in the current {reg2?town:village} automatically.  Specifically food, trade \
goods, and books will never be sold. ^^You can change some settings here freely.",
    "none",
  [
	##dplmc+ added section begin
    (this_or_next|is_between, "$current_town", towns_begin, towns_end),
	    (is_between, "$current_town", villages_begin, villages_end),
	(call_script, "script_dplmc_initialize_autoloot", 0),#argument "0" means this does nothing if deemed unnecessary
	##dplmc+ added section end
    (assign, reg1, "$g_dplmc_auto_sell_price_limit"),
	 (assign, reg2, 0),
    (try_begin),
      (is_between, "$current_town", towns_begin, towns_end),
      (assign, reg2, 1),
    (try_end),
  ],
  [
    ("continue",[],"Continue...",
    [
      #(call_script, "script_auto_sell_all"),
	  (call_script, "script_dplmc_player_auto_sell_at_center", "$current_town"),
      (jump_to_menu, "$g_next_menu"),
      ]),
    ("change_settings",[],"Change settings.",[(start_presentation, "prsnt_dplmc_auto_sell_options"),]),
    ("go_back",[],"Go back",[(jump_to_menu, "$g_next_menu")]),
  ]
  ),
  (
    "dplmc_trade_auto_buy_food_begin",0,
    "You will automatically buy food according to your shopping list. Do you want to continue?^^You can view and configure the shopping list here.",
    "none", [],
  [
    ("continue",[
	  #dplmc+ added to check against weird conditions
 	  (assign, ":merchant_troop", -1),
	  (try_begin),
		  (is_between, "$current_town", towns_begin, towns_end),
        (party_get_slot, ":merchant_troop", "$current_town", slot_town_merchant),
     (else_try),
		  (is_between, "$current_town", villages_begin, villages_end),
        (party_get_slot, ":merchant_troop", "$current_town", slot_town_elder),
     (try_end),
	  (ge, ":merchant_troop", 1),
	  #dplmc+ end addition
	 ],"Continue...",
    [
 	   (assign, ":merchant_troop", -1),
	   (try_begin),
		  (is_between, "$current_town", towns_begin, towns_end),
        (party_get_slot, ":merchant_troop", "$current_town", slot_town_merchant),
      (else_try),
		  (is_between, "$current_town", villages_begin, villages_end),
        (party_get_slot, ":merchant_troop", "$current_town", slot_town_elder),
      (try_end),
	   (call_script, "script_dplmc_auto_buy_food", "trp_player", ":merchant_troop"),
      (jump_to_menu, "$g_next_menu"),
      ]),

    ("dplmc_change_shopping_list_of_food",[],"Configure your shopping list.",[(start_presentation, "prsnt_dplmc_shopping_list_of_food"),]),
    ("go_back",[],"Go back",[(jump_to_menu, "$g_next_menu")]),
   ]
  ),
## CC
##End auto-sell credit rubik (Custom Commander)
##diplomacy start+,
  (
   "town_trade_assessment_begin",0,
   #"You overhear the following details about the roads out of town :^(experimental feature -- this may go into dialogs)^{s42}^You also overhear several discussions about the price of trade goods across the local area.^You listen closely, trying to work out the best deals around.",
   "You overhear several discussions about the price of trade goods across the local area.^You listen closely, trying to work out the best deals around.",
    "none",
    [
	(str_clear, s42),
##	(call_script, "script_merchant_road_info_to_s42", "$g_encountered_party"),

    ],

    [
      ("continue",[],"Continue...",
       [
           (assign,"$auto_enter_town", "$current_town"),
           (assign, "$g_town_assess_trade_goods_after_rest", "$current_town"), #SB : save this
           (call_script, "script_get_max_skill_of_player_party", "skl_trade"),
           (val_div, reg0, 2),
           (store_sub, ":num_hours", 6, reg0),
           (assign, "$g_last_rest_center", "$current_town"),
           (assign, "$g_last_rest_payment_until", -1),
           (rest_for_hours, ":num_hours", 5, 0), #rest while not attackable
           (change_screen_return),
        ]),
      ("go_back_dot",[],"Go back.",
       [
           (jump_to_menu,"mnu_town_trade"),
        ]),
    ]
  ),
      (
    "town_pre_hire_troops",0,
    "Upon entering a seedy tavern you note the assortment of mercenaries, cut-throuts, refugees, and adventerous warriors. With some time and a little investigation, they could give you an overview of who's available for hire..^(this takes 1 hours)",
    "none",
    [],
    [
      ("continue",[],"Ask about..",
       [
           (store_sub, ":num_hours", 1),
           (rest_for_hours, ":num_hours", 5, 0), #rest while not attackable
           (change_screen_return),
           (jump_to_menu,"mnu_town_hire_troops"),
        ]),
      ("go_back",[],"Go back..",
       [
           (jump_to_menu,"mnu_dickplo_town_manage"),
        ]),
    ]
  ),

    (
    "town_hire_troops",0,
    "This is the list you've managed to scrap together:",
    "none",
    [],
    [
      ("hire_farmers",[],"Hire farmers.",
       [
           (jump_to_menu,"mnu_town_hire_farmers"),
        ]),
      ("hire_cutthroats",[],"Hire villains, cutthrroats and looters.",
       [
           (jump_to_menu,"mnu_town_hire_cutthroats"),
        ]),
      ("hire_knights",[],"Hire knights in shiny armour.",
       [
           (jump_to_menu,"mnu_town_hire_knights"),
        ]),
      ("go_back",[],"Go back..",
       [
           (jump_to_menu,"mnu_dickplo_town_manage"),
        ]),
    ]
  ),
(
    "town_hire_farmers",0,
    "Their clothing is tattered and their pockets are empty, but their bravery has no boundaries. They have been driven out of their lands for different reasons and their husbands have been killed in the wars, and now the only way for these women make a living is to join a mercenary band. 100 denars each refugee.",
    "none",
    [],
    [
      ("farmer1",[(store_troop_gold,":total_money","trp_player"),(ge, ":total_money",100),
                       (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                       (ge, ":free_capacity",1),
],
       "1 Farmer.",
       [
           (party_add_members, "p_main_party", "trp_farmer", 1),
           (troop_remove_gold, "$g_player_troop", 100),
        ]),
("farmer5",[(store_troop_gold,":total_money","trp_player"),(ge, ":total_money",500),
                 (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                 (ge, ":free_capacity",5),
],"5 Farmers.",
       [
           (party_add_members, "p_main_party", "trp_refugee", 5),
           (troop_remove_gold, "$g_player_troop", 500),
        ]),
("farmer10",[(store_troop_gold,":total_money","trp_player"),(ge, ":total_money",1000),
                 (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                 (ge, ":free_capacity",5),
],"10 Farmers.",
       [
           (party_add_members, "p_main_party", "trp_refugee", 10),
           (troop_remove_gold, "$g_player_troop", 1000),
        ]),
      ("back_to_town_hire_troops",[],"Go back..",
       [
           (jump_to_menu,"mnu_town_hire_troops"),
        ]),
    ]
  ),
  (
    "town_hire_cutthroats",0,
    "Vile and vicious people with rotten theeth glares at you whilst you question their value and usefulness in your party. 150 for each Looter, 700 for each Nord archer, 300 for each bandit and 500 for each Brigand.",
    "none",
    [],
    [
      ("looter1",[(store_troop_gold,":total_money","trp_player"),(ge, ":total_money",150),
                       (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                       (ge, ":free_capacity",1),
],
       "1 Looter.",
       [
           (party_add_members, "p_main_party", "trp_looter", 1),
           (troop_remove_gold, "trp_player", 150),
        ]),
      ("looter5",[(store_troop_gold,":total_money","trp_player"),(ge, ":total_money",750),
                       (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                       (ge, ":free_capacity",1),
],
       "5 Looters.",
       [
           (party_add_members, "p_main_party", "trp_looter", 5),
           (troop_remove_gold, "trp_player", 750),
        ]),
      ("looter10",[(store_troop_gold,":total_money","trp_player"),(ge, ":total_money",1500),
                       (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                       (ge, ":free_capacity",1),
],
       "10 Looters.",
       [
           (party_add_members, "p_main_party", "trp_looter", 10),
           (troop_remove_gold, "trp_player", 1500),
        ]),
            ("bandit1",[(store_troop_gold,":total_money","trp_player"),(ge, ":total_money",300),
                       (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                       (ge, ":free_capacity",1),
],
       "1 Bandit.",
       [
           (party_add_members, "p_main_party", "trp_bandit", 1),
           (troop_remove_gold, "trp_player", 300),
        ]),
            ("bandit5",[(store_troop_gold,":total_money","trp_player"),(ge, ":total_money",1500),
                       (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                       (ge, ":free_capacity",1),
],
       "1 Bandits.",
       [
           (party_add_members, "p_main_party", "trp_bandit", 5),
           (troop_remove_gold, "trp_player", 1500),
        ]),
        ("bandit10",[(store_troop_gold,":total_money","trp_player"),(ge, ":total_money",3000),
                       (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                       (ge, ":free_capacity",1),
],
       "1 Bandits.",
       [
           (party_add_members, "p_main_party", "trp_bandit", 10),
           (troop_remove_gold, "trp_player", 3000),
        ]),
              ("brigand1",[(store_troop_gold,":total_money","trp_player"),(ge, ":total_money",500),
                       (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                       (ge, ":free_capacity",1),
],
       "1 Brigand.",
       [
           (party_add_members, "p_main_party", "trp_brigand", 1),
           (troop_remove_gold, "trp_player", 500),
        ]),
                    ("brigand5",[(store_troop_gold,":total_money","trp_player"),(ge, ":total_money",2500),
                       (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                       (ge, ":free_capacity",1),
],
       "1 Brigands.",
       [
           (party_add_members, "p_main_party", "trp_brigand", 5),
           (troop_remove_gold, "trp_player", 2500),
        ]),
                    ("brigand10",[(store_troop_gold,":total_money","trp_player"),(ge, ":total_money",5000),
                       (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                       (ge, ":free_capacity",1),
],
       "10 Brigands.",
       [
           (party_add_members, "p_main_party", "trp_brigand", 10),
           (troop_remove_gold, "trp_player", 5000),
        ]),
                      ("nord_archer",[(store_troop_gold,":total_money","trp_player"),(ge, ":total_money",7000),
                       (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                       (ge, ":free_capacity",1),
],
       "1 Nord Archers.",
       [
           (party_add_members, "p_main_party", "trp_nord_archer", 10),
           (troop_remove_gold, "trp_player", 7000),
        ]),
      ("back_to_town_hire_troops",[],"Go back..",
       [
           (jump_to_menu,"mnu_town_hire_troops"),
        ]),
        ]
  ),
  (
    "town_hire_knights",0,
    "Wearing shiny armour and swords ready to cut through flesh, they stand in front of you with their honour held high(as long as you pay them.).. 1000 denars each knight.",
    "none",
    [],
    [

              ("swadian_knight1",[(store_troop_gold,":total_money","trp_player"),(ge, ":total_money",1000),
                       (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                       (ge, ":free_capacity",1),
],

       "1 Swadian Knight.",
       [
           (party_add_members, "p_main_party", "trp_swadian_knight", 1),
           (troop_remove_gold, "trp_player", 1000),
        ]),
                       ("swadian_knight5",[(store_troop_gold,":total_money","trp_player"),(ge, ":total_money",5000),
                       (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                       (ge, ":free_capacity",1),
],
       "5 Swadian Knights.",
       [
           (party_add_members, "p_main_party", "trp_swadian_knight", 5),
           (troop_remove_gold, "trp_player", 5000),
        ]),
                       ("swadian_knight10",[(store_troop_gold,":total_money","trp_player"),(ge, ":total_money",10000),
                       (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                       (ge, ":free_capacity",1),
],
       "10 Swadian Knights.",
       [
           (party_add_members, "p_main_party", "trp_swadian_knight", 10),
           (troop_remove_gold, "trp_player", 10000),
        ]),
                      ("vaegir_knight1",[(store_troop_gold,":total_money","trp_player"),(ge, ":total_money",1000),
                       (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                       (ge, ":free_capacity",1),
],
       "1 Vaegir Knights.",
       [
           (party_add_members, "p_main_party", "trp_Vaegir_knight", 1),
           (troop_remove_gold, "trp_player", 1000),
        ]),
                      ("vaegir_knight5",[(store_troop_gold,":total_money","trp_player"),(ge, ":total_money",5000),
                       (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                       (ge, ":free_capacity",1),
],
       "5 Vaegir Knights.",
       [
           (party_add_members, "p_main_party", "trp_vaegir_knight", 5),
           (troop_remove_gold, "trp_player", 5000),
        ]),
                      ("vaegir_knight10",[(store_troop_gold,":total_money","trp_player"),(ge, ":total_money",10000),
                       (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                       (ge, ":free_capacity",1),
],
       "10 Vaegir Knights.",
       [
           (party_add_members, "p_main_party", "trp_vaegir_knight", 10),
           (troop_remove_gold, "trp_player", 10000),
        ]),
      ("back_to_town_hire_troops",[],"Go back..",
       [
           (jump_to_menu,"mnu_town_hire_troops"),
        ]),
        ]
  ),
  (
    "town_trade_assessment",mnf_disable_all_keys,
    "As the party member with the highest trade skill ({reg2}), {reg3?you try to figure out:{s1} tries to figure out} the best goods to trade in. {s2}",
    "none",
    [

     (call_script, "script_get_max_skill_of_player_party", "skl_trade"),
     (assign, ":max_skill", reg0),
     (assign, ":max_skill_owner", reg1),

     (assign, ":num_best_results", 0),
     (assign, ":best_result_1_item", -1),
     (assign, ":best_result_1_town", -1),
     (assign, ":best_result_1_profit", 0),
     (assign, ":best_result_2_item", -1),
     (assign, ":best_result_2_town", -1),
     (assign, ":best_result_2_profit", 0),
     (assign, ":best_result_3_item", -1),
     (assign, ":best_result_3_town", -1),
     (assign, ":best_result_3_profit", 0),
     (assign, ":best_result_4_item", -1),
     (assign, ":best_result_4_town", -1),
     (assign, ":best_result_4_profit", 0),
     (assign, ":best_result_5_item", -1),
     (assign, ":best_result_5_town", -1),
     (assign, ":best_result_5_profit", 0),

     (store_sub, ":num_towns", walled_centers_end, walled_centers_begin),
     (store_sub, ":num_goods", trade_goods_end, trade_goods_begin),
     (store_mul, ":max_iteration", ":num_towns", ":num_goods"),
     (val_mul, ":max_iteration", ":max_skill"),
     (val_div, ":max_iteration", 20),

     (assign, ":org_encountered_party", "$g_encountered_party"),

     (try_for_range, ":unused", 0, ":max_iteration"),
       (store_random_in_range, ":random_trade_good", trade_goods_begin, trade_goods_end),
       (store_random_in_range, ":random_town", towns_begin, towns_end),

       (party_get_slot, ":cur_merchant", ":org_encountered_party", slot_town_merchant),
	   (assign, ":num_items_in_town_inventory", 0),
       (try_for_range, ":i_slot", num_equipment_kinds, max_inventory_items + num_equipment_kinds),
         (troop_get_inventory_slot, ":slot_item", ":cur_merchant", ":i_slot"),
         (try_begin),
           (eq, ":slot_item", ":random_trade_good"),
		   (val_add, ":num_items_in_town_inventory", 1),
         (try_end),
       (try_end),

       (ge, ":num_items_in_town_inventory", 1),

       (assign, ":already_best", 0),

       (try_begin),
         (eq, ":random_trade_good", ":best_result_1_item"),
         (eq, ":random_town", ":best_result_1_town"),
         (val_add, ":already_best", 1),
       (try_end),

	   (try_begin),
         (eq, ":random_trade_good", ":best_result_2_item"),
         (eq, ":random_town", ":best_result_2_town"),
         (val_add, ":already_best", 1),
       (try_end),

	   (try_begin),
         (eq, ":random_trade_good", ":best_result_3_item"),
         (eq, ":random_town", ":best_result_3_town"),
         (val_add, ":already_best", 1),
       (try_end),

	   (try_begin),
         (eq, ":random_trade_good", ":best_result_4_item"),
         (eq, ":random_town", ":best_result_4_town"),
         (val_add, ":already_best", 1),
       (try_end),

	   (try_begin),
         (eq, ":random_trade_good", ":best_result_5_item"),
         (eq, ":random_town", ":best_result_5_town"),
         (val_add, ":already_best", 1),
       (try_end),

       (le, ":already_best", 1),

       (store_item_value, ":random_trade_good_price", ":random_trade_good"),
       (assign, "$g_encountered_party", ":org_encountered_party"),
       (call_script, "script_game_get_item_buy_price_factor", ":random_trade_good"),
       (store_mul, ":random_trade_good_buy_price", ":random_trade_good_price", reg0),
       (val_div, ":random_trade_good_buy_price", 100),
       (val_max, ":random_trade_good_buy_price", 1),
       (assign, "$g_encountered_party", ":random_town"),
       (call_script, "script_game_get_item_sell_price_factor", ":random_trade_good"),
       (store_mul, ":random_trade_good_sell_price", ":random_trade_good_price", reg0),
       (val_div, ":random_trade_good_sell_price", 100),
       (val_max, ":random_trade_good_sell_price", 1),
       (store_sub, ":difference", ":random_trade_good_sell_price", ":random_trade_good_buy_price"),

       (try_begin),
	     (this_or_next|eq, ":best_result_1_item", ":random_trade_good"),
		 (this_or_next|eq, ":best_result_2_item", ":random_trade_good"),
		 (this_or_next|eq, ":best_result_3_item", ":random_trade_good"),
		 (this_or_next|eq, ":best_result_4_item", ":random_trade_good"),
		 (eq, ":best_result_5_item", ":random_trade_good"),

         (try_begin),
		   (eq, ":best_result_1_item", ":random_trade_good"),
		   (gt, ":difference", ":best_result_1_profit"),
           (assign, ":best_result_1_item", ":random_trade_good"),
           (assign, ":best_result_1_town", ":random_town"),
           (assign, ":best_result_1_profit", ":difference"),
         (else_try),
		   (eq, ":best_result_2_item", ":random_trade_good"),
		   (gt, ":difference", ":best_result_2_profit"),
           (assign, ":best_result_2_item", ":random_trade_good"),
           (assign, ":best_result_2_town", ":random_town"),
           (assign, ":best_result_2_profit", ":difference"),
		 (else_try),
		   (eq, ":best_result_3_item", ":random_trade_good"),
		   (gt, ":difference", ":best_result_3_profit"),
           (assign, ":best_result_3_item", ":random_trade_good"),
           (assign, ":best_result_3_town", ":random_town"),
           (assign, ":best_result_3_profit", ":difference"),
		 (else_try),
		   (eq, ":best_result_4_item", ":random_trade_good"),
		   (gt, ":difference", ":best_result_4_profit"),
           (assign, ":best_result_4_item", ":random_trade_good"),
           (assign, ":best_result_4_town", ":random_town"),
           (assign, ":best_result_4_profit", ":difference"),
		 (else_try),
		   (eq, ":best_result_5_item", ":random_trade_good"),
		   (gt, ":difference", ":best_result_5_profit"),
           (assign, ":best_result_5_item", ":random_trade_good"),
           (assign, ":best_result_5_town", ":random_town"),
           (assign, ":best_result_5_profit", ":difference"),
		 (try_end),
	   (else_try),
       (try_begin),
         (gt, ":difference", ":best_result_1_profit"),
         (val_add, ":num_best_results", 1),
           (val_min, ":num_best_results", 5),
           (assign, ":best_result_5_item", ":best_result_4_item"),
           (assign, ":best_result_5_town", ":best_result_4_town"),
           (assign, ":best_result_5_profit", ":best_result_4_profit"),
           (assign, ":best_result_4_item", ":best_result_3_item"),
           (assign, ":best_result_4_town", ":best_result_3_town"),
           (assign, ":best_result_4_profit", ":best_result_3_profit"),
         (assign, ":best_result_3_item", ":best_result_2_item"),
         (assign, ":best_result_3_town", ":best_result_2_town"),
         (assign, ":best_result_3_profit", ":best_result_2_profit"),
         (assign, ":best_result_2_item", ":best_result_1_item"),
         (assign, ":best_result_2_town", ":best_result_1_town"),
         (assign, ":best_result_2_profit", ":best_result_1_profit"),
         (assign, ":best_result_1_item", ":random_trade_good"),
         (assign, ":best_result_1_town", ":random_town"),
         (assign, ":best_result_1_profit", ":difference"),
       (else_try),
         (gt, ":difference", ":best_result_2_profit"),
         (val_add, ":num_best_results", 1),
           (val_min, ":num_best_results", 5),
           (assign, ":best_result_5_item", ":best_result_4_item"),
           (assign, ":best_result_5_town", ":best_result_4_town"),
           (assign, ":best_result_5_profit", ":best_result_4_profit"),
           (assign, ":best_result_4_item", ":best_result_3_item"),
           (assign, ":best_result_4_town", ":best_result_3_town"),
           (assign, ":best_result_4_profit", ":best_result_3_profit"),
         (assign, ":best_result_3_item", ":best_result_2_item"),
         (assign, ":best_result_3_town", ":best_result_2_town"),
         (assign, ":best_result_3_profit", ":best_result_2_profit"),
         (assign, ":best_result_2_item", ":random_trade_good"),
         (assign, ":best_result_2_town", ":random_town"),
         (assign, ":best_result_2_profit", ":difference"),
       (else_try),
         (gt, ":difference", ":best_result_3_profit"),
         (val_add, ":num_best_results", 1),
           (val_min, ":num_best_results", 5),
           (assign, ":best_result_5_item", ":best_result_4_item"),
           (assign, ":best_result_5_town", ":best_result_4_town"),
           (assign, ":best_result_5_profit", ":best_result_4_profit"),
           (assign, ":best_result_4_item", ":best_result_3_item"),
           (assign, ":best_result_4_town", ":best_result_3_town"),
           (assign, ":best_result_4_profit", ":best_result_3_profit"),
         (assign, ":best_result_3_item", ":random_trade_good"),
         (assign, ":best_result_3_town", ":random_town"),
         (assign, ":best_result_3_profit", ":difference"),
         (else_try),
           (gt, ":difference", ":best_result_4_profit"),
           (val_add, ":num_best_results", 1),
           (val_min, ":num_best_results", 5),
           (assign, ":best_result_5_item", ":best_result_4_item"),
           (assign, ":best_result_5_town", ":best_result_4_town"),
           (assign, ":best_result_5_profit", ":best_result_4_profit"),
           (assign, ":best_result_4_item", ":random_trade_good"),
           (assign, ":best_result_4_town", ":random_town"),
           (assign, ":best_result_4_profit", ":difference"),
         (else_try),
           (gt, ":difference", ":best_result_5_profit"),
           (val_add, ":num_best_results", 1),
           (val_min, ":num_best_results", 5),
           (assign, ":best_result_5_item", ":best_result_4_item"),
           (assign, ":best_result_5_town", ":best_result_4_town"),
           (assign, ":best_result_5_profit", ":best_result_4_profit"),
         (try_end),
       (try_end),
     (try_end),

     (assign, "$g_encountered_party", ":org_encountered_party"),

     (str_clear, s3),

     (assign, reg2, ":max_skill"),
     (try_begin),
       (eq, ":max_skill_owner", "trp_player"),
       (assign, reg3, 1),
     (else_try),
       (assign, reg3, 0),
       (str_store_troop_name, s1, ":max_skill_owner"),
     (try_end),
     (try_begin),
       (le, ":num_best_results", 0),
       (str_store_string, s2, "@However, {reg3?You are:{s1} is} unable to find any trade goods that would bring a profit."),
     (else_try),
        #SB : add lesser renown bonus
        (try_begin),
          (call_script, "script_get_max_skill_of_player_party", "skl_trade"),
          (neq, reg1, "trp_player"),
          (call_script, "script_change_troop_renown", reg1, dplmc_companion_skill_renown / 2),
        (try_end),
       (try_begin),
         (ge, ":best_result_5_item", 0),
         (assign, reg6, ":best_result_5_profit"),
         (str_store_item_name, s4, ":best_result_5_item"),
         (str_store_party_name, s5, ":best_result_5_town"),
         (str_store_string, s3, "@^Buying {s4} here and selling it at {s5} would bring a profit of {reg6} denars per item.{s3}"),
       (try_end),
       (try_begin),
         (ge, ":best_result_4_item", 0),
         (assign, reg6, ":best_result_4_profit"),
         (str_store_item_name, s4, ":best_result_4_item"),
         (str_store_party_name, s5, ":best_result_4_town"),
         (str_store_string, s3, "@^Buying {s4} here and selling it at {s5} would bring a profit of {reg6} denars per item.{s3}"),
       (try_end),
       (try_begin),
         (ge, ":best_result_3_item", 0),
         (assign, reg6, ":best_result_3_profit"),
         (str_store_item_name, s4, ":best_result_3_item"),
         (str_store_party_name, s5, ":best_result_3_town"),
         (str_store_string, s3, "@^Buying {s4} here and selling it at {s5} would bring a profit of {reg6} denars per item.{s3}"),
       (try_end),
       (try_begin),
         (ge, ":best_result_2_item", 0),
         (assign, reg6, ":best_result_2_profit"),
         (str_store_item_name, s4, ":best_result_2_item"),
         (str_store_party_name, s5, ":best_result_2_town"),
         (str_store_string, s3, "@^Buying {s4} here and selling it at {s5} would bring a profit of {reg6} denars per item.{s3}"),
       (try_end),
       (try_begin),
         (ge, ":best_result_1_item", 0),
         (assign, reg6, ":best_result_1_profit"),
         (str_store_item_name, s4, ":best_result_1_item"),
         (str_store_party_name, s5, ":best_result_1_town"),
         (str_store_string, s3, "@^Buying {s4} here and selling it at {s5} would bring a profit of {reg6} denars per item.{s3}"),
       (try_end),
       (str_store_string, s2, "@{reg3?You find:{s1} finds} out the following:^{s3}"),
     (try_end),
     ],
    [
      ("continue",[],"Continue...",
       [
           (jump_to_menu,"mnu_town_trade"),
        ]),
    ]
  ),




  #SB : flavour text,
]
