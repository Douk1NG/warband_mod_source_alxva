# ======================================================================
# SHARED DEPENDENCY
# Entity: collect_taxes (menu)
# Called by menus in 2 domains: town, village
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

collect_taxes_menu = [
(
    "collect_taxes",mnf_disable_all_keys,
    "As the party member with the highest trade skill ({reg2}), {reg3?you expect:{s1} expects} that collecting taxes from here will take {reg4} days...",
    "none",
    [(call_script, "script_get_max_skill_of_player_party", "skl_trade"),
     (assign, ":max_skill", reg0),
     (assign, reg2, reg0),
     (assign, ":max_skill_owner", reg1),
     (try_begin),
       (eq, ":max_skill_owner", "trp_player"),
       (assign, reg3, 1),
     (else_try),
       (assign, reg3, 0),
       (str_store_troop_name, s1, ":max_skill_owner"),
     (try_end),
     (assign, ":tax_quest_expected_revenue", 3000),
     (try_begin),
       (party_slot_eq, "$current_town", slot_party_type, spt_town),
       (assign, ":tax_quest_expected_revenue", 6000),
     (try_end),

     (try_begin),
       (quest_slot_eq, "qst_collect_taxes", slot_quest_current_state, 0),
       (store_add, ":max_skill_plus_thirty", ":max_skill", 30),
       (try_begin),
         (party_slot_eq, "$current_town", slot_party_type, spt_town),
         (store_div, "$qst_collect_taxes_total_hours", 24* 7 * 30, ":max_skill_plus_thirty"),
       (else_try),
         #Village
         (store_div, "$qst_collect_taxes_total_hours", 24 * 3 * 30, ":max_skill_plus_thirty"),
       (try_end),

       (call_script, "script_party_count_fit_for_battle", "p_main_party"),
       (val_add, reg0, 20),
       (val_mul, "$qst_collect_taxes_total_hours", 20),
       (val_div, "$qst_collect_taxes_total_hours", reg0),


       (quest_set_slot, "qst_collect_taxes", slot_quest_target_amount, "$qst_collect_taxes_total_hours"),
       (store_div, ":menu_begin_time", "$qst_collect_taxes_total_hours", 20),#between %5-%25
       (store_div, ":menu_end_time", "$qst_collect_taxes_total_hours", 4),
       (assign, ":unrest_begin_time", ":menu_end_time"),#between %25-%75
       (store_mul, ":unrest_end_time", "$qst_collect_taxes_total_hours", 3),
       (val_div, ":unrest_end_time", 4),

       (val_mul, ":tax_quest_expected_revenue", 2),
       (store_div, "$qst_collect_taxes_hourly_income", ":tax_quest_expected_revenue", "$qst_collect_taxes_total_hours"),

       (store_random_in_range, "$qst_collect_taxes_menu_counter", ":menu_begin_time", ":menu_end_time"),
       (store_random_in_range, "$qst_collect_taxes_unrest_counter", ":unrest_begin_time", ":unrest_end_time"),
       (assign, "$qst_collect_taxes_halve_taxes", 0),
     (try_end),
     (quest_get_slot, ":target_hours", "qst_collect_taxes", slot_quest_target_amount),
     (store_div, ":target_days", ":target_hours", 24),
     (val_mul, ":target_days", 24),
     (try_begin),
       (lt, ":target_days", ":target_hours"),
       (val_add, ":target_days", 24),
     (try_end),
     (val_div, ":target_days", 24),
     (assign, reg4, ":target_days"),
     ],
    [
      ("start_collecting", [], "Start collecting.",
       [(assign, "$qst_collect_taxes_currently_collecting", 1),
        (try_begin),
          (quest_slot_eq, "qst_collect_taxes", slot_quest_current_state, 0),
          (quest_set_slot, "qst_collect_taxes", slot_quest_current_state, 1),
        (try_end),
        (rest_for_hours_interactive, 1000, 5, 0), #rest while not attackable
        (assign,"$auto_enter_town","$current_town"),
        (assign, "$g_town_visit_after_rest", 1),
        (change_screen_return),
        ]),
      ("collect_later", [], "Put it off until later.",
       [(try_begin),
          (party_slot_eq, "$current_town", slot_party_type, spt_town),
          (jump_to_menu, "mnu_town"),
        (else_try),
          (jump_to_menu, "mnu_village"),
        (try_end),
        ]),
    ]
  )
]
