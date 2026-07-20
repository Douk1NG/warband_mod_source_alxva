# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

party_size_report_menu = [
("party_size_report",0,
   "{s1}",
   "none",
   [(call_script, "script_game_get_party_companion_limit"),
    (assign, ":party_size_limit", reg0),

    (store_skill_level, ":leadership", "skl_leadership", "trp_player"),
    (val_mul, ":leadership", 5),
    (store_attribute_level, ":charisma", "trp_player", ca_charisma),

    (troop_get_slot, ":renown", "trp_player", slot_troop_renown),
    (val_div, ":renown", 25),
    (try_begin),
      (gt, ":leadership", 0),
      (str_store_string, s2, "@{!} +"),
    (else_try),
      (str_store_string, s2, "str_space"),
    (try_end),
    (try_begin),
      (gt, ":charisma", 0),
      (str_store_string, s3, "@{!} +"),
    (else_try),
      (str_store_string, s3, "str_space"),
    (try_end),
    (try_begin),
      (gt, ":renown", 0),
      (str_store_string, s4, "@{!} +"),
    (else_try),
      (str_store_string, s4, "str_space"),
    (try_end),


    #SB : other modifiers from party_get_ideal_size, listed in order of precedence
    (try_for_range, ":sreg", s6, s10),
      (str_clear, ":sreg"),
    (try_end),

    (try_begin),
      (is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
      # (call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
      # the above script doesn't exactly work for pretender
      (try_begin),
        # (ge, reg0, DPLMC_FACTION_STANDING_LEADER), #exclude spouse
        (faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),
        (store_mul, ":king_bonus", 5, "$player_right_to_rule"), #20 is "legit" ruler
        (val_clamp, ":king_bonus", dplmc_marshal_party_bonus, dplmc_monarch_party_bonus + 1),
        (assign, reg6, ":king_bonus"),
        (str_store_string, s8, "@Monarch: +{reg6}^"),
      (else_try),
        (assign, ":king_bonus", 0),
      (try_end),

      (try_begin),
        (faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
        (assign, ":marshal_bonus", dplmc_marshal_party_bonus),
        (assign, reg6, ":marshal_bonus"),
        (str_store_string, s7, "@Marshal: +{reg6}^"),
      (else_try),
        (assign, ":marshal_bonus", 0),
      (try_end),
      #percentage calculation follows
      (assign, ":faction_id", "$players_kingdom"),
      (assign, ":percent", 100),
      #Limit effects of policies for nascent kingdoms.
      (assign, ":policy_min", -3),
      (assign, ":policy_max", 4),#one greater than the maximum
      (try_begin),
          (this_or_next|eq, ":faction_id", "fac_player_supporters_faction"),
          (faction_slot_eq, ":faction_id", slot_faction_leader, "trp_player"),
          (faction_get_slot, ":policy_max", ":faction_id", slot_faction_num_towns),
          (faction_get_slot, reg0, ":faction_id", slot_faction_num_castles),
          (val_add, ":policy_max", reg0),
          (val_clamp, ":policy_max", 0, 4),#0, 1, 2, 3
          (store_mul, ":policy_min", ":policy_max", -1),
          (val_add, ":policy_max", 1),#one greater than the maximum
      (try_end),
      (try_begin), #we detecting rulership using king_bonus to determine which percent to apply
        (gt, ":king_bonus", 0),
        (try_begin),
          (faction_get_slot, ":centralization", ":faction_id", dplmc_slot_faction_centralization),
          (val_clamp, ":centralization", ":policy_min", ":policy_max"),
          (val_mul, ":centralization", 10),
          (val_add, ":percent", ":centralization"),
        (try_end),
      (else_try), #player is a regular vassal
        (try_begin),
          (faction_get_slot, ":centralization", ":faction_id", dplmc_slot_faction_centralization),
          (val_clamp, ":centralization", ":policy_min", ":policy_max"),
          (val_mul, ":centralization", -3),
          (val_add, ":percent", ":centralization"),
        (try_end),
        (try_begin),
          (faction_get_slot, ":aristocracy", ":faction_id", dplmc_slot_faction_aristocracy),
          (val_clamp, ":aristocracy", ":policy_min", ":policy_max"),
          (val_mul, ":aristocracy", 3),
          (val_add, ":percent", ":aristocracy"),
        (try_end),
        (try_begin),
          (faction_get_slot, ":quality", ":faction_id", dplmc_slot_faction_quality),
          (val_clamp, ":quality", ":policy_min", ":policy_max"),
          (val_mul, ":quality", -4),
          (val_add, ":percent", ":quality"),
        (try_end),
        ##diplomacy end
      (try_end),
      (try_begin),
        (faction_get_slot, ":serfdom", ":faction_id", dplmc_slot_faction_serfdom),
        (val_clamp, ":serfdom", ":policy_min", ":policy_max"),
        (val_mul, ":serfdom", 2), #SB : no multiplier as per description
        (val_add, ":percent", ":serfdom"),
      (try_end),
      #if no change from default, do not display
      (try_begin),
        (eq, ":percent", 100),
        (assign, ":percent", 0),
      (else_try), #last new string
        (assign, reg6, ":percent"),
        (str_store_string, s9, "@Policy: {reg6}%^"),
      (try_end),
    (else_try), #not affiliated, do not show position-based bonus
      (assign, ":king_bonus", 0),
      (assign, ":marshal_bonus", 0),
      (assign, ":percent", 0),
    (try_end),
    ## CC
    (assign, ":center_bonus", 0),
    (try_for_range, ":cur_center", castles_begin, castles_end),
      (party_slot_eq, ":cur_center", slot_town_lord, "trp_player"),
      (val_add, ":center_bonus", dplmc_castle_party_bonus),
    (try_end),
    (try_begin),
      (gt, ":center_bonus", 0),
      (assign, reg6, ":center_bonus"),
      (str_store_string, s6, "@Castellan: +{reg6}^"),
    (try_end),
    ## CC

    # (assign, reg9, ":percent"),
    # (assign, reg8, ":king_bonus"),
    # (assign, reg7, ":marshal_bonus"),
    # (assign, reg6, ":center_bonus"),
    (assign, reg5, ":party_size_limit"),
    (assign, reg1, ":leadership"),
    (assign, reg2, ":charisma"),
    (assign, reg3, ":renown"),
    #SB : might as well show player party size
    (party_get_num_companions, reg10, "p_main_party"),
    (str_store_string, s1, "@Current party size is {reg10}/{reg5}.^\
Current party size modifiers are:^^\
Base size:  +30^\
Leadership: {s2}{reg1}^\
Charisma: {s3}{reg2}^\
Renown: {s4}{reg3}^^\
{s8}{s7}{s6}{s9}\
TOTAL:  {reg5}"),
    ],
    [
      ("continue",[],"Continue...",
       [(jump_to_menu, "mnu_reports"),
        ]
       ),
      ]
  )
]
