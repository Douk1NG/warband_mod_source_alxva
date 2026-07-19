# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

captivity_menus = [
  (
    "captivity_avoid_wilderness",0,
    "Suddenly all the world goes black around you.\
 Many hours later you regain your conciousness and find yourself at the spot you fell.\
 Your enemies must have taken you up for dead and left you there.\
 However, it seems that none of your wound were lethal,\
 and altough you feel awful, you find out that can still walk.\
 You get up and try to look for any other survivors from your party.",
    "none",
    [
      ],
    []
  ),
  (
    "captivity_start_wilderness",0,
    "Stub",
    "none",
    [
          (assign, "$g_player_is_captive", 1),
          (try_begin),
            (eq,"$g_player_surrenders",1),
            (jump_to_menu, "mnu_captivity_start_wilderness_surrender"),
          (else_try),
            (jump_to_menu, "mnu_captivity_start_wilderness_defeat"),
          (try_end),
      ],
    []
  ),
  (
    "captivity_start_wilderness_surrender",0,
    "Stub",
    "none",
    [
       (assign, "$g_player_is_captive", 1),
       (assign,"$auto_menu",-1), #We need this since we may come here by something other than auto_menu
       (assign, "$capturer_party", "$g_encountered_party"),
       (jump_to_menu, "mnu_captivity_wilderness_taken_prisoner"),
      ],
    []
  ),
  (
    "captivity_start_wilderness_defeat",0,
    "Your enemies take you prisoner.",
    "none",
    [
       (assign, "$g_player_is_captive", 1),
       (assign,"$auto_menu",-1),
       (assign, "$capturer_party", "$g_encountered_party"),

       (try_begin),
         (party_stack_get_troop_id, ":party_leader", "$g_encountered_party", 0),
         (is_between, ":party_leader", active_npcs_begin, active_npcs_end),
         (troop_slot_eq, ":party_leader", slot_troop_occupation, slto_kingdom_hero),
         (store_sub, ":kingdom_hero_id", ":party_leader", active_npcs_begin),
         (set_achievement_stat, ACHIEVEMENT_BARON_GOT_BACK, ":kingdom_hero_id", 1),
       (try_end),

       (jump_to_menu, "mnu_captivity_wilderness_taken_prisoner"),
    ],
    []
  ),
  #SB : impose various degrees of penalty through permanent wounding,
  (
    "captivity_start_castle_surrender",0,
    "Stub",
    "none",
    [
        (assign, "$g_player_is_captive", 1),
        (assign,"$auto_menu",-1),
        (assign, "$capturer_party", "$g_encountered_party"),
        # (try_begin),
          # (store_random_in_range, ":random_no", -100, 100),
          # (ge, ":random_no", "$g_player_luck"),
          # (assign, "$g_next_menu", "mnu_captivity_castle_taken_prisoner"),
          # (jump_to_menu, "mnu_permanent_damage"),
        # (else_try),
          (jump_to_menu, "mnu_captivity_castle_taken_prisoner"),
        # (try_end),
      ],
    []
  ),
  ( #SB : defeat in castles has chance of wounding
    "captivity_start_castle_defeat",0,
    "Stub",
    "none",
    [
        (assign, "$g_player_is_captive", 1),
        (assign,"$auto_menu",-1),
        (assign, "$capturer_party", "$g_encountered_party"),
        (try_begin),
          (store_random_in_range, ":random_no", -50, 100),
          (ge, ":random_no", "$g_player_luck"),
          (assign, "$g_next_menu", "mnu_captivity_castle_taken_prisoner"),
          (jump_to_menu, "mnu_permanent_damage"),
        (else_try),
          (jump_to_menu, "mnu_captivity_castle_taken_prisoner"),
        (try_end),
      ],
    []
  ),
  ( #SB : defeat while defending has higher penalty
    "captivity_start_under_siege_defeat",0,
    "Your enemies take you prisoner.",
    "none",
    [
        (assign, "$g_player_is_captive", 1),
        (assign,"$auto_menu",-1),
        (assign, "$capturer_party", "$g_encountered_party"),
        (try_begin),
          (store_random_in_range, ":random_no", -50, 150),
          (ge, ":random_no", "$g_player_luck"),
          (assign, "$g_next_menu", "mnu_captivity_castle_taken_prisoner"),
          (jump_to_menu, "mnu_permanent_damage"),
        (else_try),
          (jump_to_menu, "mnu_captivity_castle_taken_prisoner"),
        (try_end),
    ],
    []
  ),
  (
    "captivity_wilderness_taken_prisoner",mnf_scale_picture,
    "Your enemies take you prisoner.",
    "none",
    [
        (set_background_mesh, "mesh_pic_prisoner_wilderness"),
     ],
    [
      ("continue",[],"Continue...",
       [
	     # Explanation of removing below code : heros are already being removed with 50% (was 75%, I decreased it) probability in mnu_total_defeat, why here there is additionally 30% removing of heros?
		 # See codes linked to "mnu_captivity_start_wilderness_surrender" and "mnu_captivity_start_wilderness_defeat" which is connected with here they all also enter
		 # "mnu_total_defeat" and inside the "mnu_total_defeat" there is script_party_remove_all_companions which removes 50% (was 75%, I decreased it) of compainons from player party.

         #(try_for_range, ":npc", companions_begin, companions_end),
         #  (main_party_has_troop, ":npc"),
         #  (store_random_in_range, ":rand", 0, 100),
         #  (lt, ":rand", 30),
         #  (remove_member_from_party, ":npc", "p_main_party"),
         #  (troop_set_slot, ":npc", slot_troop_occupation, 0),
         #  (troop_set_slot, ":npc", slot_troop_playerparty_history, pp_history_scattered),
         #  (assign, "$last_lost_companion", ":npc"),
         #  (store_faction_of_party, ":victorious_faction", "$g_encountered_party"),
         #  (troop_set_slot, ":npc", slot_troop_playerparty_history_string, ":victorious_faction"),
         #  (troop_set_health, ":npc", 100),
         #  (store_random_in_range, ":rand_town", towns_begin, towns_end),
         #  (troop_set_slot, ":npc", slot_troop_cur_center, ":rand_town"),
         #  (assign, ":nearest_town_dist", 1000),
         #  (try_for_range, ":town_no", towns_begin, towns_end),
         #    (store_faction_of_party, ":town_fac", ":town_no"),
         #    (store_relation, ":reln", ":town_fac", "fac_player_faction"),
         #    (ge, ":reln", 0),
         #    (store_distance_to_party_from_party, ":dist", ":town_no", "p_main_party"),
         #    (lt, ":dist", ":nearest_town_dist"),
         #    (assign, ":nearest_town_dist", ":dist"),
         #    (troop_set_slot, ":npc", slot_troop_cur_center, ":town_no"),
         #  (try_end),
         #(try_end),

         # (set_camera_follow_party, "$capturer_party"),
         # (assign, "$g_player_is_captive", 1),
         # (store_random_in_range, ":random_hours", 18, 30),
         # (call_script, "script_event_player_captured_as_prisoner"),
         # (call_script, "script_stay_captive_for_hours", ":random_hours"),
         # (assign,"$auto_menu","mnu_captivity_wilderness_check"),
         # (change_screen_return),


         (assign, "$talk_context", tc_player_defeated),

         (party_stack_get_troop_id, ":capturer_troop", "$capturer_party", 0),
         (party_stack_get_troop_dna, ":capturer_dna", "$capturer_party", 0),
         (party_get_template_id, ":template", "$capturer_party"),
         (store_faction_of_troop, ":troop_faction", ":capturer_troop"),

         (try_begin),
             (eq, "$g_sexual_content", 2),
             (this_or_next|eq, ":template", "pt_deserters"),
             (this_or_next|eq, ":troop_faction", fac_outlaws),
             (this_or_next|eq, ":troop_faction", fac_forest_bandits),
             (this_or_next|eq, ":troop_faction", fac_mountain_bandits),
             (this_or_next|eq, ":troop_faction", fac_black_khergits),
             (this_or_next|eq, ":troop_faction", fac_dark_knights),
             (this_or_next|eq, "$g_encountered_party_faction", fac_outlaws),
             (this_or_next|eq, "$g_encountered_party_faction", fac_forest_bandits),
             (this_or_next|eq, "$g_encountered_party_faction", fac_mountain_bandits),
             (this_or_next|eq, "$g_encountered_party_faction", fac_black_khergits),
             (eq, "$g_encountered_party_faction", fac_dark_knights),
             (call_script, "script_setup_troop_meeting", ":capturer_troop", ":capturer_dna"),
         (else_try),
            (eq, "$g_sexual_content", 2),
            (is_between, ":capturer_troop", heroes_begin, heroes_end),
            (troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_debauched),
            (call_script, "script_setup_troop_meeting", ":capturer_troop", -1),
         (else_try),
             (set_camera_follow_party, "$capturer_party"),
             (assign, "$g_player_is_captive", 1),
             (store_random_in_range, ":random_hours", 18, 30),
             (call_script, "script_event_player_captured_as_prisoner"),
             (call_script, "script_stay_captive_for_hours", ":random_hours"),
             (assign,"$auto_menu","mnu_captivity_wilderness_check"),
             (change_screen_return),
         (try_end),
         ]),
      ]
  ),
  (
    "captivity_wilderness_check",0,
    "stub",
    "none",
    [(jump_to_menu,"mnu_captivity_end_wilderness_escape")],
    []
  ),
  (
    "captivity_end_wilderness_escape", mnf_scale_picture,
    "After painful days of being dragged about as a prisoner, you find a chance and escape from your captors!",
    "none",
    [
        (play_cue_track, "track_escape"),
          ##diplomacy start+ test gender with script
        #(troop_get_type, ":is_female", "trp_player"),#<- replaced
        (try_begin),
          #(eq, ":is_female", 1),#<- replaced
          (eq, "$character_gender", tf_female),#<- added
          (set_background_mesh, "mesh_pic_escape_1_fem"),
        (else_try),
          (set_background_mesh, "mesh_pic_escape_1"),
        (try_end),
          ##diplomacy end+
    ],
    [
      ("continue",[],"Continue...",
       [
           (assign, "$g_player_is_captive", 0),
           (try_begin),
             (party_is_active, "$capturer_party"),
             (party_relocate_near_party, "p_main_party", "$capturer_party", 2),
           (try_end),
           (call_script, "script_set_parties_around_player_ignore_player", 8, 12), #it was radius:2 and hours:4, but players make lots of complains about consequent battle losses after releases from captivity then I changed this.
           (try_begin),
             (neq, "$g_player_icon_state", pis_ship),
           (assign, "$g_player_icon_state", pis_normal),
           (try_end),
           (set_camera_follow_party, "p_main_party"),
           (rest_for_hours, 0, 0, 0), #stop resting
           ##diplomacy begin
           #(assign, "$g_move_fast", 1),
           ##diplomacy end
           (change_screen_return),
        ]),
    ]
  ),
  (
    "captivity_castle_taken_prisoner",0,
    "You are quickly surrounded by guards who take away your weapons. With curses and insults, they throw you into the dungeon where you must while away the miserable days of your captivity.",
    "none",
    [
          ##diplomacy start+ test gender with script
        #(troop_get_type, ":is_female", "trp_player"),#<- replaced
        (try_begin),
          #(eq, ":is_female", 1),#<- replaced
          (eq, "$character_gender", tf_female),#<- added
          (set_background_mesh, "mesh_pic_prisoner_fem"),
        (else_try),
          (set_background_mesh, "mesh_pic_prisoner_man"),
        (try_end),
          ##diplomacy end+
        #SB : deduct relation here, probably
        (call_script, "script_change_player_relation_with_center", "$g_encountered_party", -1),
    ],
    [
      ("continue",[],"Continue...",
       [
           (assign, "$g_player_is_captive", 1),
           (store_random_in_range, ":random_hours", 16, 22),
           (call_script, "script_event_player_captured_as_prisoner"),
           (call_script, "script_stay_captive_for_hours", ":random_hours"),
           (assign,"$auto_menu", "mnu_captivity_castle_check"),
           (change_screen_return)
        ]),
    ]
  ),
  (
    "captivity_rescue_lord_taken_prisoner",0,
    "You remain in disguise for as long as possible before revealing yourself.\
 The guards are outraged and beat you savagely before throwing you back into the cell for God knows how long...",
    "none",
    [
		  ##diplomacy start+ test gender with script
        #(troop_get_type, ":is_female", "trp_player"),#<-replaced
        (try_begin),
          #(eq, ":is_female", 1),#<-replaced
		  (eq, "$character_gender", tf_female),#<- added
          (set_background_mesh, "mesh_pic_prisoner_fem"),
        (else_try),
          (set_background_mesh, "mesh_pic_prisoner_man"),
        (try_end),
		  ##diplomacy end+
   ],
    [
      ("continue",[],"Continue...",
       [
           (assign, "$g_player_is_captive", 1),
           (store_random_in_range, ":random_hours", 16, 22),
           (call_script, "script_event_player_captured_as_prisoner"),
           (call_script, "script_stay_captive_for_hours", ":random_hours"),
           (assign,"$auto_menu", "mnu_captivity_castle_check"),
           (change_screen_return),
        ]),
    ]
  ),
  (
    "captivity_castle_check",0,
    "stub",
    "none",
    [
        (store_random_in_range, reg(7), 0, 100),
        (try_begin),
		  (party_is_active, "$capturer_party"),
		  (store_faction_of_party, ":capturer_faction", "$capturer_party"),
		  (is_between, ":capturer_faction", kingdoms_begin, kingdoms_end),
		  (store_relation, ":relation_w_player_faction", ":capturer_faction", "fac_player_faction"),
		  (ge, ":relation_w_player_faction", 0),
          #SB : this doesn't make much sense when the player is unaffiliated
          (jump_to_menu,"mnu_captivity_end_exchanged_with_prisoner"),
		(else_try),
          (lt, reg(7), 40),
          (troop_get_slot, ":player_renown", "trp_player", slot_troop_renown),
          (val_mul, ":player_renown", 2),
          (store_character_level, ":player_level", "trp_player"),
          (store_mul, "$player_ransom_amount", ":player_level", 50),
          (val_add, "$player_ransom_amount", 100),
          (val_add, "$player_ransom_amount", ":player_renown"),
          (store_troop_gold, reg3, "trp_player"),
          (store_div, ":player_gold_div_20", reg3, 20),
          (val_add, "$player_ransom_amount", ":player_gold_div_20"),

          #(gt, reg3, "$player_ransom_amount"),
          (jump_to_menu,"mnu_captivity_end_propose_ransom"),
        (else_try),
          (lt, reg(7), 45), #4% chance to be set free
          (jump_to_menu,"mnu_captivity_end_exchanged_with_prisoner"),
        (else_try),
          (jump_to_menu,"mnu_captivity_castle_remain"),
        (try_end),
    ],
    []
  ),
  (
    "captivity_end_exchanged_with_prisoner",0,
    "After days of imprisonment, you are finally set free {s0}",
    "none",
    [
      (play_cue_track, "track_escape"),

      (try_begin),
		  (party_is_active, "$capturer_party"),
		  (store_faction_of_party, ":capturer_faction", "$capturer_party"),
		  (is_between, ":capturer_faction", kingdoms_begin, kingdoms_end),
		  (store_relation, ":relation_w_player_faction", ":capturer_faction", "fac_player_faction"),
		  (ge, ":relation_w_player_faction", 0),
          (str_store_party_name, s13, "$capturer_party"),
          (str_store_string, s0, "@as {s13} is no longer held by your enemies."),
      (else_try),
          (str_store_string, s0, "@when your captors exchange you with another prisoner."),
      (try_end),
      ],
    [
      ("continue",[],"Continue...",
       [
           (assign, "$g_player_is_captive", 0),
           (try_begin),
             (party_is_active, "$capturer_party"),
             (party_relocate_near_party, "p_main_party", "$capturer_party", 2),
           (try_end),
           (call_script, "script_set_parties_around_player_ignore_player", 8, 12), #it was radius:2 and hours:12, but players make lots of complains about consequent battle losses after releases from captivity then I changed this.
           (assign, "$g_player_icon_state", pis_normal),
           (set_camera_follow_party, "p_main_party"),
           (rest_for_hours, 0, 0, 0), #stop resting
		   (call_script, "script_simple_remove_disguise"),
           (change_screen_return),
        ]),
    ]
  ),
  (
    "captivity_end_propose_ransom",0,
    "You spend long hours in the sunless dank of the dungeon, more than you can count.\
 Suddenly one of your captors enters your cell with an offer;\
 he proposes to free you in return for {reg5} denars of your hidden wealth. You decide to...",
    "none",
    [
      (assign, reg5, "$player_ransom_amount"),
    ],
    [
      ("captivity_end_ransom_accept",
      [
        (store_troop_gold,":player_gold", "trp_player"),
        (ge, ":player_gold","$player_ransom_amount")
      ],"Accept the offer.",
      [
        (play_cue_track, "track_escape"),
        (assign, "$g_player_is_captive", 0),
        (troop_remove_gold, "trp_player", "$player_ransom_amount"),
        (try_begin),
          (party_is_active, "$capturer_party"),
          (party_relocate_near_party, "p_main_party", "$capturer_party", 1),
        (try_end),
        (call_script, "script_set_parties_around_player_ignore_player", 8, 12), #it was radius:2 and hours:6, but players make lots of complains about consequent battle losses after releases from captivity then I changed this.
        (assign, "$g_player_icon_state", pis_normal),
        (set_camera_follow_party, "p_main_party"),
        (rest_for_hours, 0, 0, 0), #stop resting
        (change_screen_return),
      ]),
      ("captivity_end_ransom_accept_2",
      [
        (store_troop_gold,":player_gold", "trp_player"),
        (lt, ":player_gold","$player_ransom_amount"),

        (try_begin),
          (store_troop_gold, ":player_gold", "trp_player"),
          (assign, reg6, ":player_gold"),
        (try_end),
      ],"Pay him {reg6} denars, promising to pay the rest when you are free.",
      [
        (play_cue_track, "track_escape"),
        (assign, "$g_player_is_captive", 0),

        (party_get_slot, ":town_lord", "$current_town", slot_town_lord),
        (party_get_slot, ":guild_master_troop", "$current_town",slot_town_elder),

        (store_troop_gold,":player_gold", "trp_player"),
        (troop_remove_gold, "trp_player", ":player_gold"),
        (store_sub, ":new_debts", "$player_ransom_amount", ":player_gold"),
        (try_begin),
            (gt, ":town_lord", -1),
            (call_script, "script_change_debt_to_troop", ":town_lord", ":new_debts"),
        (else_try),
            (gt, ":guild_master_troop", -1),
            (call_script, "script_change_debt_to_troop", ":guild_master_troop", ":new_debts"),
        (try_end),

        (val_max, ":new_debts", 1),
        (val_div, ":new_debts", 200),
        (try_begin),
            (gt, ":new_debts", 0),
            (val_mul, ":new_debts", -1),
            (call_script, "script_change_troop_renown", "trp_player", ":new_debts"),
        (try_end),

        (try_begin),
          (party_is_active, "$capturer_party"),
          (party_relocate_near_party, "p_main_party", "$capturer_party", 1),
        (try_end),
        (call_script, "script_set_parties_around_player_ignore_player", 8, 12), #it was radius:2 and hours:6, but players make lots of complains about consequent battle losses after releases from captivity then I changed this.
        (assign, "$g_player_icon_state", pis_normal),
        (set_camera_follow_party, "p_main_party"),
        (rest_for_hours, 0, 0, 0), #stop resting
		(call_script, "script_simple_remove_disguise"),
        (change_screen_return),
      ]),
      ("captivity_end_ransom_deny",
      [
      ],"Refuse him, wait for something better.",
      [
        (try_begin),
            (eq, "$g_sexual_content", 2),
	        (this_or_next|eq, "$character_gender", 1),(eq, "$g_nohomo", 0),
            (jump_to_menu, "mnu_fucked_by_enemy_prison"),
        (else_try),
            (assign, "$g_player_is_captive", 1),
            (store_random_in_range, reg(8), 16, 22),
            (call_script, "script_stay_captive_for_hours", reg8),
            (assign,"$auto_menu", "mnu_captivity_castle_check"),
            (change_screen_return),
        (try_end),
      ]),
    ]
  ),
  (
    "captivity_castle_remain",mnf_scale_picture|mnf_disable_all_keys,
    "More days pass in the darkness of your cell. You get through them as best you can,\
 enduring the kicks and curses of the guards, watching your underfed body waste away more and more...",
    "none",
    [
		  ##diplomacy start+ test gender with script
        #(troop_get_type, ":is_female", "trp_player"),#<- replaced
        (try_begin),
          #(eq, ":is_female", 1),#<- replaced
		  (eq, "$character_gender", tf_female),#<- added
          (set_background_mesh, "mesh_pic_prisoner_fem"),
        (else_try),
          (set_background_mesh, "mesh_pic_prisoner_man"),
        (try_end),
		  ##diplomacy end+
        (store_random_in_range, ":random_hours", 16, 22),
        (call_script, "script_stay_captive_for_hours", ":random_hours"),
        (assign,"$auto_menu", "mnu_captivity_castle_check"),

    ],
    [
      ("continue",[],"Continue...",
       [
           (assign, "$g_player_is_captive", 1),
           (change_screen_return),
        ]),
    ]
  ),

  (
##diplomacy end+ fix gender of pronoun
    "kingdom_army_quest_report_to_army",mnf_scale_picture,
    "{s8} sends word that {reg4?she:he} wishes you to join {reg4?her:his} new military campaign.\
 You need to bring at least {reg13} troops to the army,\
 and are instructed to raise more men with all due haste if you do not have enough.",
##diplomacy end+
    "none",
    [
        (set_background_mesh, "mesh_pic_messenger"),
        (quest_get_slot, ":quest_target_troop", "qst_report_to_army", slot_quest_target_troop),
        (quest_get_slot, ":quest_target_amount", "qst_report_to_army", slot_quest_target_amount),
        (call_script, "script_get_information_about_troops_position", ":quest_target_troop", 0),
        (str_clear, s9),
        (try_begin),
          (eq, reg0, 1), #troop is found and text is correct
          (str_store_string, s9, s1),
        (try_end),
        (str_store_troop_name, s8, ":quest_target_troop"),
        (assign, reg13, ":quest_target_amount"),
		##diplomacy start+
      #Set gender with script
		#(troop_get_type, reg4, ":quest_target_troop"), #<- OLD
		(call_script, "script_dplmc_store_troop_is_female_reg", ":quest_target_troop", 4),
		##diplomacy end+
      ],
    [
      ("continue",[],"Continue...",
       [
           (quest_get_slot, ":quest_target_troop", "qst_report_to_army", slot_quest_target_troop),
           (quest_get_slot, ":quest_target_amount", "qst_report_to_army", slot_quest_target_amount),
           (str_store_troop_name_link, s13, ":quest_target_troop"),
           (assign, reg13, ":quest_target_amount"),
           (setup_quest_text, "qst_report_to_army"),
           ##diplomacy start+ fix gender of pronoun
           (str_store_string, s2, "@{s13} asked you to report to {reg4?her:him} with at least {reg13} troops."),
           ##diplomacy end+
           (call_script, "script_start_quest", "qst_report_to_army", ":quest_target_troop"),
           (call_script, "script_report_quest_troop_positions", "qst_report_to_army", ":quest_target_troop", 3),
           (change_screen_return),
        ]),
     ]
  ),

  (
##diplomacy start+ fix gender of pronouns
    "kingdom_army_quest_messenger",mnf_scale_picture,
    "{s8} sends word that {reg4?she:he} wishes to speak with you about a task {reg4?she:he} needs performed.\
 {reg4?She:He} requests you to come and see {reg4?her:him} as soon as possible.",
##diplomacy end+
    "none",
    [
        (set_background_mesh, "mesh_pic_messenger"),
        (faction_get_slot, ":faction_marshall", "$players_kingdom", slot_faction_marshall),
        ##diplomacy start+ put marshall's gender in reg4
        (call_script, "script_dplmc_store_troop_is_female", ":faction_marshall"),
        (assign, reg4, reg0),
        ##diplomacy end+
        (str_store_troop_name, s8, ":faction_marshall"),
      ],
    [
      ("continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
]
