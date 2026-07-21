# ======================================================================
# SHARED DEPENDENCY
# Entity: get_player_party_morale_values (script)
# Called by menus in 2 domains: character_creation, reports
# ======================================================================

# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from module_constants import *
from module_constants import *
from header_parties import *
from header_skills import *
from header_mission_templates import *
from header_items import *
from header_triggers import *
from header_terrain_types import *
from header_music import *
from header_map_icons import *
from ID_animations import *

get_player_party_morale_values_scripts = [
("get_player_party_morale_values",
    [
      (party_get_num_companion_stacks, ":num_stacks","p_main_party"),
      (assign, ":num_men", 0),
      (try_for_range, ":i_stack", 1, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop","p_main_party",":i_stack"),
        (try_begin),
          (troop_is_hero, ":stack_troop"),
          (val_add, ":num_men", 1), #it was 3 in "Mount&Blade", now it is 1 in Warband
        (else_try),
          (party_stack_get_size, ":stack_size","p_main_party",":i_stack"),
          (val_add, ":num_men", ":stack_size"),
        (try_end),
      (try_end),
      (assign, "$g_player_party_morale_modifier_party_size", ":num_men"),

      (store_skill_level, ":player_leadership", "skl_leadership", "trp_player"),

      (try_begin),
        (eq, "$players_kingdom", "fac_player_supporters_faction"),
        (faction_get_slot, ":cur_faction_king", "$players_kingdom", slot_faction_leader),
        (eq, ":cur_faction_king", "trp_player"),
        (store_mul, "$g_player_party_morale_modifier_leadership", ":player_leadership", 15),
      (else_try),
        (store_mul, "$g_player_party_morale_modifier_leadership", ":player_leadership", 12),
      (try_end),

      (assign, ":new_morale", "$g_player_party_morale_modifier_leadership"),
      (val_sub, ":new_morale", "$g_player_party_morale_modifier_party_size"),

      (val_add, ":new_morale", 50),

      (assign, "$g_player_party_morale_modifier_food", 0),
      (try_for_range, ":cur_edible", "itm_raw_date_fruit", food_end),
        (neq, ":cur_edible", "itm_furs"),
        (item_slot_eq, ":cur_edible", slot_item_edible, 1),
        (call_script, "script_cf_player_has_item_without_modifier", ":cur_edible", imod_rotten),
        (item_get_slot, ":food_bonus", ":cur_edible", slot_item_food_bonus),

        (val_mul, ":food_bonus", 3),
        (val_div, ":food_bonus", 2),

        (val_add, "$g_player_party_morale_modifier_food", ":food_bonus"),
      (try_end),
      (val_add, ":new_morale", "$g_player_party_morale_modifier_food"),

      (try_begin),
        (eq, "$g_player_party_morale_modifier_food", 0),
        (assign, "$g_player_party_morale_modifier_no_food", 30),
        (val_sub, ":new_morale", "$g_player_party_morale_modifier_no_food"),
      (else_try),
        (assign, "$g_player_party_morale_modifier_no_food", 0),
      (try_end),

      (assign, "$g_player_party_morale_modifier_debt", 0),
      (try_begin),
        (gt, "$g_player_debt_to_party_members", 0),
        (call_script, "script_calculate_player_faction_wage"),
        (assign, ":total_wages", reg0),
        (store_mul, "$g_player_party_morale_modifier_debt", "$g_player_debt_to_party_members", 10),
		(val_max, ":total_wages", 1),
        (val_div, "$g_player_party_morale_modifier_debt", ":total_wages"),
        (val_clamp, "$g_player_party_morale_modifier_debt", 1, 31),
        (val_sub, ":new_morale", "$g_player_party_morale_modifier_debt"),
      (try_end),

      (val_clamp, ":new_morale", 0, 100),
      (assign, reg0, ":new_morale"),
      ])
]
