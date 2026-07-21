# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

dplmc_negotiate_besieger_menu = [
(
    "dplmc_negotiate_besieger",0,
    "You appear with a white flag at the top of the wall. After a while a negotiator of {s11} approaches you. He demands {s6} and all associated villages as well as {reg0} denars for safe conduct.",
    "none",
    [
      (party_get_slot, ":besieger", "$current_town", slot_center_is_besieged_by),
      (party_stack_get_troop_id, ":enemy_party_leader", ":besieger", 0),
      (str_store_troop_name, s11, ":enemy_party_leader"),
      (store_faction_of_troop, ":besieger_faction", ":enemy_party_leader"),

      ##diplomacy start+
	  #1) Support promoted kingdom ladies, mercenary parties, etc.
	  #2) Fix mistake with potentially not counting besieger party in the size calculation!
	  ##OLD:
	  #(assign, ":besieger_size", 0),
      #(try_for_range, ":lord", active_npcs_begin, active_npcs_end),
      #  (store_faction_of_troop, ":lord_faction", ":lord"),
      #  (eq, ":lord_faction", ":besieger_faction"),
      #  (troop_get_slot, ":led_party", ":lord", slot_troop_leaded_party),
      ##NEW:
      (party_get_num_companions, ":besieger_size", ":besieger"),

	  (try_for_parties, ":led_party"),
        (ge, ":led_party", spawn_points_end),
        (neq, ":led_party", ":besieger"),#don't double count
        (store_faction_of_party, ":party_faction", ":led_party"),
        (eq, ":party_faction", ":besieger_faction"),
	  ##diplomacy end+
        (party_is_active, ":led_party"),

        (party_slot_eq, ":led_party", slot_party_ai_state, spai_accompanying_army),
        (party_slot_eq, ":led_party", slot_party_ai_object, ":besieger"),

        (party_is_active, ":besieger"),
        (store_distance_to_party_from_party, ":distance_to_marshal", ":led_party", ":besieger"),
        (lt, ":distance_to_marshal", 25),
        (party_get_num_companions, ":party_size", ":led_party"),
        (val_add, ":besieger_size", ":party_size"),
      (try_end),

      (assign, ":garrison_size", 0),
      (party_get_num_companion_stacks, ":num_stacks", "$current_town"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_size, ":stack_size", "$current_town", ":i_stack"),
        (val_add, ":garrison_size", ":stack_size"),
      (try_end),
      (val_sub, ":besieger_size", ":garrison_size"),

      (store_skill_level, ":player_persuasion_skill", "skl_persuasion", "trp_player"),
      (val_mul, ":player_persuasion_skill", 10),
      (store_sub, "$diplomacy_var", ":besieger_size", ":player_persuasion_skill"),
      (val_mul, "$diplomacy_var", 4),
      ##diplomacy start+ : include ransom cost in calculation
      (call_script, "script_calculate_ransom_amount_for_troop", "trp_player"),
      (val_add, "$diplomacy_var", reg0),
      ##diplomacy end+
      (val_max,"$diplomacy_var",500),
      (val_div, "$diplomacy_var", 100),
      (val_mul, "$diplomacy_var", 100),
      (assign, reg0, "$diplomacy_var"),

      (str_store_party_name, s6, "$current_town"),

    ],
      [
      ("dplmc_comply_treasury",
      [
        (store_troop_gold, ":gold", "trp_household_possessions"),
        (ge, ":gold", "$diplomacy_var"),
      ],"Comply and induce your chamberlain to pay the money from the treasury.",
      [
        (call_script, "script_dplmc_withdraw_from_treasury", "$diplomacy_var"),
		##diplomacy start+ when the player pays, give the gold to the lord
		(party_get_slot, ":besieger", "$current_town", slot_center_is_besieged_by),
		(party_stack_get_troop_id, ":enemy_party_leader", ":besieger", 0),
		(call_script, "script_dplmc_distribute_gold_to_lord_and_holdings", "$diplomacy_var", ":enemy_party_leader"),
		##diplomacy end+
        (call_script, "script_dplmc_player_center_surrender", "$current_town"),
        (change_screen_return),
      ]),

      ("dplmc_comply",
      [
        (store_troop_gold, ":gold", "trp_player"),
        (ge, ":gold", "$diplomacy_var"),
      ],"Comply and pay the gold.",
      [
        (troop_remove_gold, "trp_player", "$diplomacy_var"),
		##diplomacy start+ when the player pays, give the gold to the lord
		(party_get_slot, ":besieger", "$current_town", slot_center_is_besieged_by),
		(party_stack_get_troop_id, ":enemy_party_leader", ":besieger", 0),
		(call_script, "script_dplmc_distribute_gold_to_lord_and_holdings", "$diplomacy_var", ":enemy_party_leader"),
		##diplomacy end+
        (call_script, "script_dplmc_player_center_surrender", "$current_town"),
        (change_screen_return),
      ]),

      ("dplmc_break_off",[],"Break off negotiations.",
       [
          (jump_to_menu, "mnu_town"),
        ]),
     ]
  )
]
