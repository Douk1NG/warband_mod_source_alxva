# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

start_phase_2_menu = [
("start_phase_2",mnf_disable_all_keys,
    "You hear about Calradia, a land torn between rival kingdoms battling each other for supremacy,\
 a haven for knights and mercenaries, cutthroats and adventurers, all willing to risk their lives in pursuit of fortune, power, or glory...\
 In this land which holds great dangers and even greater opportunities, you believe you may leave your past behind and start a new life.\
 You feel that finally, you hold the key of your destiny in your hands, free to choose as you will,\
 and that whatever course you take, great adventures will await you. Drawn by the stories you hear about Calradia and its kingdoms, you...",
    "none",
    [
      #SB : auto-sort through inventory, get rid of duplicate armor (and add them as gold)
      #weapons can have duplicates but are mostly a none issue, player might want to reroll anyway
      # (set_show_messages, 0),
      (assign, ":bonus_gold", 0),
      (troop_get_inventory_capacity, ":capacity", "trp_player"),
      (assign, ":helmet_score", -1),
      (assign, ":shield_score", -1),
      (assign, ":chest_score", -1),
      (assign, ":boots_score", -1),
      (assign, ":glove_score", -1),
      # (assign, ":weapon_score", -1),
      (try_for_range, ":i_slot", 0, ":capacity"),
        (troop_get_inventory_slot, ":item_no", "trp_player", ":i_slot"),
        (ge, ":item_no", 0),
        (item_get_type, ":itp", ":item_no"),
        # (this_or_next|is_between, ":itp", itp_type_one_handed_wpn, itp_type_goods),
        (this_or_next|eq, ":itp", itp_type_shield),
        (is_between, ":itp", itp_type_head_armor, itp_type_pistol), #skip horses, food, etc
        (troop_get_inventory_slot_modifier, ":imod_no", "trp_player", ":i_slot"),
        (call_script, "script_dplmc_troop_can_use_item", "trp_player", ":item_no", ":imod_no"),
        (eq, reg0, 1), #only parse those we can use
        (call_script, "script_dplmc_get_item_score_with_imod", ":item_no", ":imod_no"),
        (assign, ":score", reg0),
        (try_begin),
          (eq, ":itp", itp_type_head_armor),
          # (try_begin),
            # (lt, ":score", ":helmet_score"),
            # (troop_set_inventory_slot, "trp_player", ":i_slot", -1),
            # (call_script, "script_dplmc_get_item_value_with_imod", ":item_no", ":imod_no"),
            # (val_add, ":bonus_gold", reg0),
          # (else_try),
          (gt, ":score", ":helmet_score"),
          (assign, ":helmet_score", ":score"),
        (else_try),
          (eq, ":itp", itp_type_body_armor),
          (gt, ":score", ":chest_score"),
          (assign, ":chest_score", ":score"),
        (else_try),
          (eq, ":itp", itp_type_foot_armor),
          (gt, ":score", ":boots_score"),
          (assign, ":boots_score", ":score"),
        (else_try),
          (eq, ":itp", itp_type_hand_armor),
          (gt, ":score", ":glove_score"),
          (assign, ":glove_score", ":score"),
        (else_try),
          (eq, ":itp", itp_type_shield),
          (gt, ":score", ":shield_score"),
          (assign, ":shield_score", ":score"),
        (try_end),
      (try_end),

      (try_for_range, ":i_slot", 0, ":capacity"),
        (troop_get_inventory_slot, ":item_no", "trp_player", ":i_slot"),
        (ge, ":item_no", 0),
        (item_get_type, ":itp", ":item_no"),
        (is_between, ":itp", itp_type_head_armor, itp_type_pistol), #skip horses, food, etc
        (troop_get_inventory_slot_modifier, ":imod_no", "trp_player", ":i_slot"),
        # (call_script, "script_dplmc_troop_can_use_item", "trp_player", ":item_no", ":imod_no"),
        # (eq, reg0, 1), #only parse those we can use
        (call_script, "script_dplmc_get_item_score_with_imod", ":item_no", ":imod_no"),
        (assign, ":score", reg0),
        (try_begin),
          (eq, ":itp", itp_type_head_armor),
          (lt, ":score", ":helmet_score"),
          (assign, ":score", -1),
        (else_try),
          (eq, ":itp", itp_type_body_armor),
          (lt, ":score", ":chest_score"),
          (assign, ":score", -1),
        (else_try),
          (eq, ":itp", itp_type_foot_armor),
          (lt, ":score", ":boots_score"),
          (assign, ":score", -1),
        (else_try),
          (eq, ":itp", itp_type_hand_armor),
          (lt, ":score", ":glove_score"),
          (assign, ":score", -1),
        (else_try),
          (eq, ":itp", itp_type_shield),
          (lt, ":score", ":shield_score"),
          (assign, ":score", -1),
        (try_end),
        (eq, ":score", -1), #found a worse item
        (troop_set_inventory_slot, "trp_player", ":i_slot", -1),
        (call_script, "script_dplmc_get_item_value_with_imod", ":item_no", ":imod_no"),
        (val_add, ":bonus_gold", reg0),
      (try_end),
      (val_div, ":bonus_gold", 2),
      (troop_add_gold, "trp_player", ":bonus_gold"),
      # (set_show_messages, 1),
    ],
    [##diplomacy start+ Replace "join" with "Join" in the following
      ("town_1",[(eq, "$current_startup_quest_phase", 0),],"Join a caravan to Praven, in the Kingdom of Swadia.",
       [
         (assign, "$current_town", "p_town_6"),
         (assign, "$g_starting_town", "$current_town"),
         (assign, "$g_journey_string", "str_journey_to_praven"),
		 (jump_to_menu, "mnu_start_phase_2_5"),
#         (party_relocate_near_party, "p_main_party", "$g_starting_town", 2),
#         (change_screen_return),
       ]),

      ("town_2",[(eq, "$current_startup_quest_phase", 0),],"Join a caravan to Reyvadin, in the Kingdom of the Vaegirs.",
       [
         (assign, "$current_town", "p_town_8"),
         (assign, "$g_starting_town", "$current_town"),
         (assign, "$g_journey_string", "str_journey_to_reyvadin"),
		 (jump_to_menu, "mnu_start_phase_2_5"),
#         (party_relocate_near_party, "p_main_party", "$g_starting_town", 2),
#         (change_screen_return),
       ]),

      ("town_3",[(eq, "$current_startup_quest_phase", 0),],"Join a caravan to Tulga, in the Khergit Khanate.",
       [
         (assign, "$current_town", "p_town_10"),
         (assign, "$g_starting_town", "$current_town"),
         (assign, "$g_journey_string", "str_journey_to_tulga"),
		 (jump_to_menu, "mnu_start_phase_2_5"),
#         (party_relocate_near_party, "p_main_party", "$g_starting_town", 2),
#         (change_screen_return),
       ]),

      ("town_4",[(eq, "$current_startup_quest_phase", 0),],"Take a ship to Sargoth, in the Kingdom of the Nords.",
       [
         (assign, "$current_town", "p_town_1"),
         (assign, "$g_starting_town", "$current_town"),
         (assign, "$g_journey_string", "str_journey_to_sargoth"),
		 (jump_to_menu, "mnu_start_phase_2_5"),
#         (party_relocate_near_party, "p_main_party", "$g_starting_town", 2),
#         (change_screen_return),
       ]),

      ("town_5",[(eq, "$current_startup_quest_phase", 0),],"Take a ship to Jelkala, in the Kingdom of the Rhodoks.",
       [
         (assign, "$current_town", "p_town_5"),
         (assign, "$g_starting_town", "$current_town"),
         (assign, "$g_journey_string", "str_journey_to_jelkala"),
		 (jump_to_menu, "mnu_start_phase_2_5"),
#         (party_relocate_near_party, "p_main_party", "$g_starting_town", 2),
#         (change_screen_return),
       ]),

      ("town_6",[(eq, "$current_startup_quest_phase", 0),],"Join a caravan to Shariz, in the Sarranid Sultanate.",
       [
         (assign, "$current_town", "p_town_19"),
         (assign, "$g_starting_town", "$current_town"),
         (assign, "$g_journey_string", "str_journey_to_shariz"),
		 (jump_to_menu, "mnu_start_phase_2_5"),
#         (party_relocate_near_party, "p_main_party", "$g_starting_town", 2),
#         (change_screen_return),
       ]),
##diplomacy end+ (replaced "join" with "Join")

      ("tutorial_cheat",[(eq,1,0)],"{!}CHEAT!",
       [
         (change_screen_return),
         (assign, "$cheat_mode", 1),
         (set_show_messages, 0),
		 (add_xp_to_troop, 15000, "trp_player"),
         (troop_raise_skill, "trp_player", skl_leadership, 7),
         (troop_raise_skill, "trp_player", skl_prisoner_management, 5),
         (troop_raise_skill, "trp_player", skl_inventory_management, 10),
         (party_add_members, "p_main_party", "trp_swadian_knight", 10),
         (party_add_members, "p_main_party", "trp_vaegir_knight", 10),
         (party_add_members, "p_main_party", "trp_vaegir_archer", 10),
         (party_add_members, "p_main_party", "trp_swadian_sharpshooter", 10),
         (troop_add_item, "trp_player","itm_scale_armor",0),
         (troop_add_item, "trp_player","itm_full_helm",0),

         (troop_add_item, "trp_player","itm_hafted_blade_b",0),
         (troop_add_item, "trp_player","itm_hafted_blade_a",0),
         (troop_add_item, "trp_player","itm_morningstar",0),
         (troop_add_item, "trp_player","itm_tutorial_spear",0),
         (troop_add_item, "trp_player","itm_tutorial_staff",0),
         (troop_add_item, "trp_player","itm_tutorial_staff_no_attack",0),
         (troop_add_item, "trp_player","itm_arena_lance",0),
         (troop_add_item, "trp_player","itm_practice_staff",0),
         (troop_add_item, "trp_player","itm_practice_lance",0),
         (troop_add_item, "trp_player","itm_practice_javelin",0),
         (troop_add_item, "trp_player","itm_scythe",0),
         (troop_add_item, "trp_player","itm_pitch_fork",0),
         (troop_add_item, "trp_player","itm_military_fork",0),
         (troop_add_item, "trp_player","itm_battle_fork",0),
         (troop_add_item, "trp_player","itm_boar_spear",0),
         (troop_add_item, "trp_player","itm_jousting_lance",0),
         (troop_add_item, "trp_player","itm_double_sided_lance",0),
         (troop_add_item, "trp_player","itm_glaive",0),
         (troop_add_item, "trp_player","itm_poleaxe",0),
         (troop_add_item, "trp_player","itm_polehammer",0),
         (troop_add_item, "trp_player","itm_staff",0),
         (troop_add_item, "trp_player","itm_quarter_staff",0),
         (troop_add_item, "trp_player","itm_iron_staff",0),
         (troop_add_item, "trp_player","itm_shortened_spear",0),
         (troop_add_item, "trp_player","itm_spear",0),
         (troop_add_item, "trp_player","itm_war_spear",0),
         (troop_add_item, "trp_player","itm_military_scythe",0),
         (troop_add_item, "trp_player","itm_light_lance",0),
         (troop_add_item, "trp_player","itm_lance",0),
         (troop_add_item, "trp_player","itm_heavy_lance",0),
         (troop_add_item, "trp_player","itm_great_lance",0),
         (troop_add_item, "trp_player","itm_pike",0),
         (troop_add_item, "trp_player","itm_ashwood_pike",0),
         (troop_add_item, "trp_player","itm_awlpike",0),
         (troop_add_item, "trp_player","itm_throwing_spears",0),
         (troop_add_item, "trp_player","itm_javelin",0),
         (troop_add_item, "trp_player","itm_jarid",0),

         (troop_add_item, "trp_player","itm_long_axe_b",0),

         (set_show_messages, 1),

         (try_for_range, ":cur_place", scenes_begin, scenes_end),
           (scene_set_slot, ":cur_place", slot_scene_visited, 1),
         (try_end),

         (call_script, "script_get_player_party_morale_values"),
         (party_set_morale, "p_main_party", reg0),
       ]
	   ),
    ]
  )
]
