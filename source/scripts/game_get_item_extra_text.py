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
from ID_strings import str_key_0
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

game_get_item_extra_text_scripts = [
#script_game_get_item_extra_text:
# This script is called from the game engine when an item's properties are displayed.
# INPUT: arg1 = item_no, arg2 = extra_text_id (this can be between 0-7 (7 included)), arg3 = item_modifier
# OUTPUT: result_string = item extra text, trigger_result = text color (0 for default)
("game_get_item_extra_text",
    [
      (store_script_param, ":item_no", 1),
      (store_script_param, ":extra_text_id", 2),
      (store_script_param, ":item_modifier", 3),
      (try_begin),
        (is_between, ":item_no", "itm_raw_date_fruit", food_end),
        (neq, ":item_no", "itm_furs"),
        (try_begin),
          (eq, ":extra_text_id", 0),
          (assign, ":continue", 1),
          (try_begin),
            (this_or_next|eq, ":item_no", "itm_cattle_meat"),
            (this_or_next|eq, ":item_no", "itm_pork"),
            (eq, ":item_no", "itm_chicken"),

            (eq, ":item_modifier", imod_rotten),
            (assign, ":continue", 0),
          (try_end),
          (eq, ":continue", 1),
          (item_get_slot, ":food_bonus", ":item_no", slot_item_food_bonus),
          (assign, reg1, ":food_bonus"),
          (set_result_string, "@+{reg1} to party morale"),
          (set_trigger_result, 0x4444FF),
        (else_try),
          (eq, ":extra_text_id", 1),
          (assign, ":quest_no", -1), #no quest selected
          (try_begin),
            (check_quest_active, "qst_deliver_wine"),
            (quest_slot_eq, "qst_deliver_wine", slot_quest_target_item, ":item_no"),
            (assign, ":quest_no", "qst_deliver_wine"),
            (quest_get_slot, ":quest_target_center", ":quest_no", slot_quest_target_center),
          (try_end),

          (try_begin), #prioritize town missions
            (eq, ":quest_no", -1),
            (check_quest_active, "qst_deliver_grain"),
            (quest_slot_eq, "qst_deliver_grain", slot_quest_target_item, ":item_no"),
            (assign, ":quest_no", "qst_deliver_grain"),
            (quest_get_slot, ":quest_target_center", ":quest_no", slot_quest_giver_center),
          (try_end),
          (neq, ":item_modifier", imod_rotten),
          (neq, ":quest_no", -1),
          (quest_get_slot, reg5, ":quest_no", slot_quest_target_amount),
          #probably do a x/n items counter here or something
          (str_store_party_name, s5, ":quest_target_center"),
          (set_result_string, "@Deliver {reg5} units to {s5}"),
          (set_trigger_result, message_alert),
        (try_end),
      (else_try),
        (is_between, ":item_no", readable_books_begin, readable_books_end),
        (try_begin),
          (eq, ":extra_text_id", 0),
          (item_get_slot, reg1, ":item_no", slot_item_intelligence_requirement),
          (set_result_string, "@Requires {reg1} intelligence to read"),
          (set_trigger_result, 0xFFEEDD),
        (else_try),
          (eq, ":extra_text_id", 1),
          (item_get_slot, ":progress", ":item_no", slot_item_book_reading_progress),
          (val_div, ":progress", 10),
          (assign, reg1, ":progress"),
          (set_result_string, "@Reading Progress: {reg1}%"),
          (set_trigger_result, 0xFFEEDD),
        ###(((item extra text
        (else_try),
          (eq, ":extra_text_id", 2),
          (try_begin),
            (eq, ":item_no", "itm_book_tactics"),
            (str_store_string, s1, "@tactics"),
          (else_try),
            (eq, ":item_no", "itm_book_persuasion"),
            (str_store_string, s1, "@persuasion"),
          (else_try),
            (eq, ":item_no", "itm_book_leadership"),
            (str_store_string, s1, "@leadership"),
          (else_try),
            (eq, ":item_no", "itm_book_intelligence"),
            (str_store_string, s1, "@intelligence"),
          (else_try),
            (eq, ":item_no", "itm_book_trade"),
            (str_store_string, s1, "@trade"),
          (else_try),
            (eq, ":item_no", "itm_book_weapon_mastery"),
            (str_store_string, s1, "@weapon mastery"),
          (else_try),
            (eq, ":item_no", "itm_book_engineering"),
            (str_store_string, s1, "@engineer"),
          (try_end),
          (set_result_string, "@+1 to {s1} after reading"),
          (set_trigger_result, 0xFFEEDD),
        ###)))
        (try_end),
      (else_try),
        (is_between, ":item_no", reference_books_begin, reference_books_end),
        (try_begin),
          (eq, ":extra_text_id", 0),
          (try_begin),
            (eq, ":item_no", "itm_book_wound_treatment_reference"),
            (str_store_string, s1, "@wound treament"),
          (else_try),
            (eq, ":item_no", "itm_book_training_reference"),
            (str_store_string, s1, "@trainer"),
          (else_try),
            (eq, ":item_no", "itm_book_surgery_reference"),
            (str_store_string, s1, "@surgery"),
          (try_end),
          (set_result_string, "@+1 to {s1} while in inventory"),
          (set_trigger_result, 0xFFEEDD),
        (try_end),
      ###(((item extra text
      (else_try),
        (assign, ":cur_text_id", -1),
        (item_get_type, ":type", ":item_no"),
        # itp_can_penetrate_shield
        (try_begin),
          (item_has_property, ":item_no", itp_can_penetrate_shield),
          (this_or_next|is_between, ":type", itp_type_one_handed_wpn, itp_type_goods),
          (is_between, ":type", itp_type_pistol, itp_type_animal),
          (val_add, ":cur_text_id", 1),
          (eq, ":extra_text_id", ":cur_text_id"),
          (set_result_string, "@Can penetrate shield"),
          (set_trigger_result, 0xFF0088),
        (try_end),
        # itp_civilian
        (try_begin),
          (item_has_property, ":item_no", itp_civilian),
          (is_between, ":type", itp_type_head_armor, itp_type_pistol),
          (val_add, ":cur_text_id", 1),
          (eq, ":extra_text_id", ":cur_text_id"),
          (set_result_string, "@Civilian clothing"),
          (set_trigger_result, 0x00FFFF),
        (try_end),
        # itp_couchable
        (try_begin),
          (item_has_property, ":item_no", itp_couchable),
          (this_or_next|is_between, ":type", itp_type_one_handed_wpn, itp_type_goods),
          (is_between, ":type", itp_type_pistol, itp_type_animal),
          (val_add, ":cur_text_id", 1),
          (eq, ":extra_text_id", ":cur_text_id"),
          (set_result_string, "@Couchable"),
          (set_trigger_result, 0xFF0000),
        (try_end),
        # itp_can_knock_down
        (try_begin),
          (item_has_property, ":item_no", itp_can_knock_down),
          (val_add, ":cur_text_id", 1),
          (eq, ":extra_text_id", ":cur_text_id"),
          (set_result_string, "@Can knock down"),
          (set_trigger_result, 0xFFFF00),
        (try_end),
        # missile speed
        (try_begin),
          (this_or_next|is_between, ":type", itp_type_bow, itp_type_goods),
          (is_between, ":type", itp_type_pistol, itp_type_bullets),
          (val_add, ":cur_text_id", 1),
          (eq, ":extra_text_id", ":cur_text_id"),
          (item_get_missile_speed, ":missile_speed", ":item_no"),
          (assign, reg1, ":missile_speed"),
          (set_result_string, "@Missile speed: {reg1}"),
          (set_trigger_result, 0xFFFFFF),
        (try_end),
        # difficulty
        (try_begin),
          (is_presentation_active, "prsnt_manage_inventory"), ###(((manage_inventory)))
          (call_script, "script_get_item_difficulty_with_imod", ":item_no", ":item_modifier"),
          (assign, ":difficulty", reg0),
          (gt, ":difficulty", 0),
          (val_add, ":cur_text_id", 1),
          (eq, ":extra_text_id", ":cur_text_id"),
          (assign, reg1, ":difficulty"),
          (set_result_string, "@Difficulty: {reg1}"),
          (set_trigger_result, 0x0066FF),
        (try_end),
        # test
        (try_begin),
          (eq, "$cheat_mode", 1),
          (neq, ":type", itp_type_goods),
          (call_script, "script_get_item_capability_with_imod", ":item_no", ":item_modifier"),
          (assign, ":capability", reg0),
          (val_add, ":cur_text_id", 1),
          (eq, ":extra_text_id", ":cur_text_id"),
          (assign, reg1, ":capability"),
          (set_result_string, "@Capability: {reg1}"),
          (set_trigger_result, 0x000000),
        (try_end),
      ###)))
      (try_end),

      # sb : debug
        (try_begin),
          (ge, "$cheat_mode", 1),
          (eq, ":extra_text_id", 4),
          (call_script, "script_dplmc_get_item_value_with_imod", ":item_no", ":item_modifier"),
          (assign, ":value", reg0),
          (call_script, "script_dplmc_get_item_score_with_imod", ":item_no", ":item_modifier"),
          (store_div, reg1, ":value", 100),
          (set_result_string, "@item score:{reg0}, value:{reg1}"),
          (set_trigger_result, 0x0DDEEE),
        (try_end),

        (try_begin), #SB : display this block when in item pool mode
          (eq, ":extra_text_id", 2),
          (eq, "$pool_troop", "trp_temp_troop"), #new exit code resets condition
          (this_or_next|eq, "$lord_selected", "trp_player"),
          (is_between, "$lord_selected", companions_begin, companions_end),
          (call_script, "script_item_get_type_aux", ":item_no"),
          (assign, ":meta_type", reg0),
          (gt, ":meta_type", meta_itp_mask), #has a valid meta-type
          (assign, ":string", "str_empty_string"),
          (try_begin), #doesn't need it, Native item type already shows
            # (eq, ":meta_type", dplmc_itp_morningstar),
            # (assign, ":string", "str_dplmc_hero_wpn_slot_two_handed_one_handed"),
          # (else_try),
            (eq, ":meta_type", dplmc_itp_lance),
            (assign, ":string", "str_dplmc_hero_wpn_slot_lance"),
          (else_try),
            (eq, ":meta_type", dplmc_itp_pike),
            (assign, ":string", "str_dplmc_hero_wpn_slot_pikes"),
          (else_try),
            (eq, ":meta_type", dplmc_itp_halberd),
            (assign, ":string", "str_dplmc_hero_wpn_slot_halberd"),
          (try_end),
          (gt, ":string", "str_empty_string"), #could use directly
           (set_result_string, ":string"),
           (set_trigger_result, 0xDDEEFF),
         (try_end),

  ])
]
