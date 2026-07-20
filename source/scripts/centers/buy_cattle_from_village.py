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

buy_cattle_from_village_scripts = [
##  # script_get_random_enemy_town
# Input: arg1 = village_no, arg2 = amount, arg3 = single_cost
# Output: reg0 = party_no
("buy_cattle_from_village",
    [
      (store_script_param, ":village_no", 1),
      (store_script_param, ":amount", 2),
      (store_script_param, ":single_cost", 3),

      #Changing price of the cattle
      (try_for_range, ":unused", 0, ":amount"),
        (call_script, "script_game_event_buy_item", "itm_cattle_meat", 0),
        (call_script, "script_game_event_buy_item", "itm_cattle_meat", 0),
      (try_end),

      (party_get_slot, ":num_cattle", ":village_no", slot_village_number_of_cattle),
      (val_sub, ":num_cattle", ":amount"),
      (party_set_slot, ":village_no", slot_village_number_of_cattle, ":num_cattle"),
      (store_mul, ":cost", ":single_cost", ":amount"),
      (troop_remove_gold, "trp_player", ":cost"),
      #SB : add gold back to elder
      (try_begin),
        (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_MEDIUM),
        (party_get_slot, ":elder", ":village_no", slot_town_elder),
        (gt, ":elder", 0),
        (troop_add_gold, ":elder", ":cost"),
      (try_end),

      (assign, ":continue", 1),
      (try_for_parties, ":cur_party"),
        (eq, ":continue", 1),
        (party_slot_eq, ":cur_party", slot_party_type, spt_cattle_herd),
        (store_distance_to_party_from_party, ":dist", ":village_no", ":cur_party"),
        (lt, ":dist", 6),
        (assign, ":subcontinue", 1),
        (try_begin),
          (check_quest_active, "qst_move_cattle_herd"),
          (quest_slot_eq, "qst_move_cattle_herd", slot_quest_target_party, ":cur_party"),
          (assign, ":subcontinue", 0),
        (try_end),
        (eq, ":subcontinue", 1),
        (party_add_members, ":cur_party", "trp_cattle", ":amount"),
        (assign, ":continue", 0),
        (assign, reg0, ":cur_party"),
      (try_end),
      (try_begin),
        (eq, ":continue", 1),
        (call_script, "script_create_cattle_herd", ":village_no", ":amount"),
      (try_end),
  ])
]
