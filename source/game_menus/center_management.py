# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

center_management_menus = [
  (
    "center_manage",0,
    "{s19}^{reg6?^^You are\
 currently building {s7}. The building will be completed after {reg8} day{reg9?s:}.:}",
    "none",
    [(assign, ":num_improvements", 0),
     (str_clear, s18),
     #SB : spt strings
     (try_begin),
       (party_slot_eq, "$g_encountered_party", slot_party_type, spt_village),
       (assign, ":begin", village_improvements_begin),
       (assign, ":end", village_improvements_end),
       (str_store_string, s17, "@village"),
     (else_try),
       (assign, ":begin", walled_center_improvements_begin),
       (assign, ":end", walled_center_improvements_end),
       (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
       (str_store_string, s17, "@town"),
     (else_try),
       (str_store_string, s17, "@castle"),
     (try_end),

     (try_for_range, ":improvement_no", ":begin", ":end"),
       (party_slot_ge, "$g_encountered_party", ":improvement_no", 1),
       (val_add,  ":num_improvements", 1),
       (call_script, "script_get_improvement_details", ":improvement_no"),
       (try_begin),
         (eq,  ":num_improvements", 1),
         (str_store_string_reg, s18, s0),
       (else_try),
         (str_store_string, s18, "@{!}{s18}, {s0}"),
       (try_end),
     (try_end),

     (try_begin),
       (eq,  ":num_improvements", 0),
       (str_store_string, s19, "@The {s17} has no improvements."),
     (else_try),
       (str_store_string, s19, "@The {s17} has the following improvements:{s18}."),
     (try_end),

     (assign, reg6, 0),
     (try_begin),
       (party_get_slot, ":cur_improvement", "$g_encountered_party", slot_center_current_improvement),
       (gt, ":cur_improvement", 0),
       (call_script, "script_get_improvement_details", ":cur_improvement"),
       (str_store_string, s7, s0),
       (assign, reg6, 1),
       (store_current_hours, ":cur_hours"),
       (party_get_slot, ":finish_time", "$g_encountered_party", slot_center_improvement_end_hour),
       (val_sub, ":finish_time", ":cur_hours"),
       (store_div, reg8, ":finish_time", 24),
       (val_max, reg8, 1),
       (store_sub, reg9, reg8, 1),
     (try_end),
    ],
    [
      ("walled_center_move_court",
      [ #SB : move conditions around
		(neg|party_slot_eq, "$g_encountered_party", slot_party_type, spt_village), # Because it says walled in the name
        (neg|party_slot_eq, "$current_town", slot_village_state, svs_under_siege),
        (party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
        (eq, "$g_encountered_party_faction", "$players_kingdom"),
        (neq, "$g_player_court", "$current_town"),
        ##diplomacy start+ Handle player is co-ruler of kingdom
        (assign, ":is_coruler", 0),
        (try_begin),
          (is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
          (call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
          (ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
          (assign, ":is_coruler", 1),
        (else_try),
          (faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
          (eq, "$g_encountered_party_faction", "fac_player_supporters_faction"),
          (assign, ":is_coruler", 1),
        (try_end),
        (eq, ":is_coruler", 1),

      ],
      "Move your court here.",
      [
        (jump_to_menu, "mnu_establish_court"),
      ]),

      ("center_build_manor",[(eq, reg6, 0),
                             (party_slot_eq, "$g_encountered_party", slot_party_type, spt_village),
                             (party_slot_eq, "$g_encountered_party", slot_center_has_manor, 0),
                                  ],
       "Build a manor.",[(assign, "$g_improvement_type", slot_center_has_manor),
                         (jump_to_menu, "mnu_center_improve"),]),
      ("center_build_fish_pond",[(eq, reg6, 0),
                                 (party_slot_eq, "$g_encountered_party", slot_party_type, spt_village),
                                 (party_slot_eq, "$g_encountered_party", slot_center_has_fish_pond, 0),
                                  ],
       "Build a mill.",[(assign, "$g_improvement_type", slot_center_has_fish_pond),
                             (jump_to_menu, "mnu_center_improve"),]),
      ("center_build_watch_tower",[(eq, reg6, 0),
                                   (party_slot_eq, "$g_encountered_party", slot_party_type, spt_village),
                                   (party_slot_eq, "$g_encountered_party", slot_center_has_watch_tower, 0),
                                  ],
       "Build a watch tower.",[(assign, "$g_improvement_type", slot_center_has_watch_tower),
                               (jump_to_menu, "mnu_center_improve"),]),
      ("center_build_school",[(eq, reg6, 0),
                              (party_slot_eq, "$g_encountered_party", slot_party_type, spt_village),
                              (party_slot_eq, "$g_encountered_party", slot_center_has_school, 0),
                                  ],
       "Build a school.",[(assign, "$g_improvement_type", slot_center_has_school),
                          (jump_to_menu, "mnu_center_improve"),]),
      ("center_build_messenger_post",[(eq, reg6, 0),
                                      (party_slot_eq, "$g_encountered_party", slot_center_has_messenger_post, 0),
                                       ],
       "Build a messenger post.",[(assign, "$g_improvement_type", slot_center_has_messenger_post),
                                  (jump_to_menu, "mnu_center_improve"),]),
      ("center_build_prisoner_tower",[(eq, reg6, 0),
                                      (this_or_next|party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
                                      (party_slot_eq, "$g_encountered_party", slot_party_type, spt_castle),
                                      (party_slot_eq, "$g_encountered_party", slot_center_has_prisoner_tower, 0),
                                       ],
       "Build a prisoner tower.",[(assign, "$g_improvement_type", slot_center_has_prisoner_tower),
                                  (jump_to_menu, "mnu_center_improve"),]),

      #SB: cancel current improvement
      ("center_cancel_build",[(eq, reg6, 1),],
      "Cancel building the {s7}.",[
        (call_script, "script_change_center_prosperity", "$current_town", -4),
        (call_script, "script_change_player_relation_with_center", "$current_town", -2),
        (party_set_slot, "$current_town", slot_center_current_improvement, 0),
        (party_set_slot, "$current_town", slot_village_recover_progress, 0),
        (party_get_slot, ":hours_left", "$current_town", slot_center_improvement_end_hour),

        #reinvest in economy, not household possessions
        # (party_get_slot, ":cur_wealth", "$current_town", slot_town_wealth),
        (try_begin),
          (is_between, "$current_town", towns_begin, towns_end),
          (party_get_slot, ":merchant_troop", "$current_town", slot_town_merchant),
          (troop_add_gold, ":merchant_troop", ":hours_left"),
        (else_try),
          (is_between, "$current_town", villages_begin, villages_end),
          (party_get_slot, ":merchant_troop", "$current_town", slot_town_elder),
        (else_try),
          (assign, ":merchant_troop", -1),
        (try_end),

        (store_current_hours, ":cur_hours"),
        (val_sub, ":hours_left", ":cur_hours"),
        (val_mul, ":hours_left", 15), #a paltry sum
        (try_begin),
          (gt, ":merchant_troop", 0),
          (troop_add_gold, ":merchant_troop", ":hours_left"),
        (else_try), #castle has no seneschal
          (party_get_slot, ":cur_gold", "$current_town", slot_center_accumulated_tariffs),
          (val_add, ":cur_gold", ":hours_left"),
          (party_set_slot, "$current_town", slot_center_accumulated_tariffs, ":cur_gold"),
        (try_end),
        (jump_to_menu, "$g_next_menu"),
        ]),
      ("go_back_dot",[],"Go back.",[(jump_to_menu, "$g_next_menu")]),
    ],
  ),
  (
    "center_improve",0,
    "{s19} As the party member with the highest engineer skill ({reg2}), {reg3?you reckon:{s3} reckons} that building the {s4} will cost you\
 {reg5} denars and will take {reg6} days.",
    "none",
    [#SB : town pictures
     (call_script, "script_set_town_picture"),
     (call_script, "script_get_improvement_details", "$g_improvement_type"),
     (assign, ":improvement_cost", reg0),
     (str_store_string, s4, s0),
     (str_store_string, s19, s1),
     (call_script, "script_get_max_skill_of_player_party", "skl_engineer"),
     (assign, ":max_skill", reg0),
     (assign, ":max_skill_owner", reg1),
     (assign, reg2, ":max_skill"),

     (store_sub, ":multiplier", 20, ":max_skill"),
     (val_mul, ":improvement_cost", ":multiplier"),
     (val_div, ":improvement_cost", 20),

     (store_div, ":improvement_time", ":improvement_cost", 100),
     (val_add, ":improvement_time", 3),

     (assign, reg5, ":improvement_cost"),
     (assign, reg6, ":improvement_time"),

     #SB : tableau at bottom
     (try_begin),
       (eq, ":max_skill_owner", "trp_player"),
       (assign, reg3, 1),
     (else_try),
       (assign, reg3, 0),
       (str_store_troop_name, s3, ":max_skill_owner"),
     (try_end),

    #SB : assign globals to be safe
    (assign, "$diplomacy_var", ":improvement_cost"),
    (assign, "$diplomacy_var2", ":improvement_time"),
    (assign, "$lord_selected", ":max_skill_owner"),
    (set_fixed_point_multiplier, 100),
    (position_set_x, pos0, 70),
    (position_set_y, pos0, 5),
    (position_set_z, pos0, 75),
    (set_game_menu_tableau_mesh, "tableau_troop_note_mesh", ":max_skill_owner", pos0),
    ],
    [
      ##diplomacy begin
      ("dplmc_improve_cont",
      [
        (gt, "$g_player_chamberlain", 0),
        (store_troop_gold, ":cur_gold", "trp_household_possessions"),
        (ge, ":cur_gold", "$diplomacy_var"),
      ], "Go on. (Pay from treasury)",
        [
          (call_script, "script_dplmc_withdraw_from_treasury", "$diplomacy_var"),
          # (call_script, "script_get_max_skill_of_player_party", "skl_engineer"), #SB : re-fetch skill
          (call_script, "script_improve_center", "$g_encountered_party", "$lord_selected", "$diplomacy_var2"),
          (jump_to_menu,"mnu_center_manage"),
         ]
      ),
      ("improve_not_enough_gold",[(gt, "$g_player_chamberlain", 0),
                                  (store_troop_gold, ":cur_gold", "trp_household_possessions"),
                                  (lt, ":cur_gold", "$diplomacy_var"),
                                  #SB : disable_menu_option
                                  (disable_menu_option)],
       "Insufficient fund in the treasury.", []),
      ##diplomacy end

      ("improve_cont",[(store_troop_gold, ":cur_gold", "trp_player"),
                       (ge, ":cur_gold", "$diplomacy_var")],
       "Go on.", [
                  (try_begin), #fast build
                    (ge, "$cheat_mode", 1),
                    (assign, "$diplomacy_var2", 0),
                  (else_try),
                    (troop_remove_gold, "trp_player", "$diplomacy_var"),
                  (try_end),
                  (call_script, "script_improve_center", "$g_encountered_party", "$lord_selected", "$diplomacy_var2"),
                  (jump_to_menu,"mnu_center_manage"),
                  ]),
      ("improve_not_enough_gold",[(store_troop_gold, ":cur_gold", "trp_player"),
                                  (lt, ":cur_gold", "$diplomacy_var"),
                                  #SB : disable_menu_option
                                  (disable_menu_option)],
       "I don't have enough money for that.", []),
      ("forget_it",[], "Forget it.", [(jump_to_menu,"mnu_center_manage")]),

    ],
  ),
]
