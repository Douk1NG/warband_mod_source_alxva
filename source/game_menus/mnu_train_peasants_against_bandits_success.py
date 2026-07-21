# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

train_peasants_against_bandits_success_menu = [
(
    "train_peasants_against_bandits_success",mnf_disable_all_keys,
    "The bandits are broken!\
 Those few who remain run off with their tails between their legs,\
 terrified of the peasants and their new champion.\
 The villagers have little left in the way of wealth after their ordeal,\
 but they offer you all they can find to show their gratitude.",
    "none",
    [(party_clear, "p_temp_party"),
     #SB : probably apply casualties before adding new troops?
     (quest_get_slot, ":amount_trained", "qst_train_peasants_against_bandits", slot_quest_target_amount),
     (store_faction_of_party, ":village_faction", "$current_town"), #assuming player trains them with local weapons
     (faction_get_slot, ":recruit_troop", ":village_faction", slot_faction_tier_1_troop),
     (party_add_members, "$current_town", ":recruit_troop", ":amount_trained"),
     (party_remove_members, "$current_town", "trp_farmer", ":amount_trained"),

     (call_script, "script_end_quest", "qst_train_peasants_against_bandits"),
     (call_script, "script_change_player_relation_with_center", "$current_town", 4),

     (party_get_slot, ":merchant_troop", "$current_town", slot_town_elder),
     (try_for_range, ":slot_no", num_equipment_kinds ,max_inventory_items + num_equipment_kinds),
        (store_random_in_range, ":rand", 0, 100),
        (lt, ":rand", 50),
        (troop_set_inventory_slot, ":merchant_troop", ":slot_no", -1),
     (try_end),
     (call_script, "script_add_log_entry", logent_helped_peasants, "trp_player",  "$current_town", -1, -1),
     #(set_background_mesh, "mesh_pic_mb_warrior_3"), #SB : background mesh
    ],
    [
      ("village_bandits_defeated_accept",[],"Take it as your just due.",[(jump_to_menu, "mnu_auto_return_to_map"),
                                                                         (party_get_slot, ":merchant_troop", "$current_town", slot_town_elder),
                                                                         (troop_sort_inventory, ":merchant_troop"),
                                                                         (change_screen_loot, ":merchant_troop"),
                                                                       ]),
      ("village_bandits_defeated_cont",[],  "Refuse, stating that they need these items more than you do.",[
      (call_script, "script_change_player_relation_with_center", "$g_encountered_party", 3),
      (call_script, "script_change_player_honor", 1),
      (change_screen_map)]),
    ],
  )
]
