# ======================================================================
# SHARED DEPENDENCY
# Entity: center_manage (menu)
# Called by menus in 5 domains: center_management, cheats, court, town, village
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

center_manage_menu = [
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
  )
]
