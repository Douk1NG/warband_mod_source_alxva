# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

village_infestation_removed_menu = [
(
    "village_infestation_removed",mnf_disable_all_keys,
    "In a battle worthy of song, you and your men drive the bandits out of the village, making it safe once more.\
 The villagers have little left in the way of wealth after their ordeal, but they offer you {reg10?all they can find:a few heads of cattle}.",
    "none",
    [(party_get_slot, ":bandit_troop", "$g_encountered_party", slot_village_infested_by_bandits),
     (party_set_slot, "$g_encountered_party", slot_village_infested_by_bandits, 0),
     (party_clear, "p_temp_party"),
     (party_add_members, "p_temp_party", ":bandit_troop", "$qst_eliminate_bandits_infesting_village_num_bandits"),
     #SB : tweaked player contribution by whether village is the same faction
     (try_begin),
       (eq, "$players_kingdom", "$g_encountered_party_faction"),
       (assign, "$g_strength_contribution_of_player", 65),
     (else_try),
       (assign, "$g_strength_contribution_of_player", 50),
     (try_end),
     (call_script, "script_party_give_xp_and_gold", "p_temp_party"),
     (try_begin),
       (check_quest_active, "qst_eliminate_bandits_infesting_village"),
       (quest_slot_eq, "qst_eliminate_bandits_infesting_village", slot_quest_target_center, "$g_encountered_party"),
       (call_script, "script_end_quest", "qst_eliminate_bandits_infesting_village"),
       #Add quest reward
       (call_script, "script_change_player_relation_with_center", "$g_encountered_party", 5),
     (else_try),
       (check_quest_active, "qst_deal_with_bandits_at_lords_village"),
       (quest_slot_eq, "qst_deal_with_bandits_at_lords_village", slot_quest_target_center, "$g_encountered_party"),
       (call_script, "script_succeed_quest", "qst_deal_with_bandits_at_lords_village"),
       (call_script, "script_change_player_relation_with_center", "$g_encountered_party", 3),
     (else_try),
     #Add normal reward
       (call_script, "script_change_player_relation_with_center", "$g_encountered_party", 4),
     (try_end),

     (party_get_slot, ":merchant_troop", "$current_town", slot_town_elder),
     #SB : calculate amount of merchandise remaining
     (assign, ":num_items", 0),
     (try_for_range, ":slot_no", num_equipment_kinds, max_inventory_items + num_equipment_kinds),
        (store_random_in_range, ":rand", 0, 100),
        (lt, ":rand", 70),
        (troop_set_inventory_slot, ":merchant_troop", ":slot_no", -1),
     (else_try),
        (troop_get_inventory_slot, ":item_no", ":merchant_troop", ":slot_no"),
        (gt, ":item_no", 0),
        (item_get_type, ":itp", ":item_no"),
        (eq, ":itp", itp_type_goods),
        (val_add, ":num_items", 1),
     (try_end),
     #SB : check before we disappoint the player
       # (store_free_inventory_capacity, ":capacity", ":merchant_troop"),
       # (eq, ":capacity", max_inventory_items),
     (assign, reg10, ":num_items"),
     #SB : background mesh
     #(set_background_mesh, "mesh_pic_mb_warrior_3"), #dckplmc - obscures text
    ],
    [
    #SB : add other option
      # ("village_bandits_defeated_accept_cattle",[(eq, reg10, 1)],"Looks like meat's back on the menu.",[(jump_to_menu, "mnu_village"),
                                                                         # (call_script, "script_create_cattle_herd", "$current_town", 1),
                                                                       # ]),
      ("village_bandits_defeated_accept",[],"Take it as your just due.",[(jump_to_menu, "mnu_village"),
                                                                         (party_get_slot, ":merchant_troop", "$current_town", slot_town_elder),
                                                                         (troop_sort_inventory, ":merchant_troop"),
                                                                         (try_begin),
                                                                           (gt, reg10, 0),
                                                                           (change_screen_loot, ":merchant_troop"),
                                                                         (else_try), #arbitrary amount
                                                                           (store_random_in_range, reg10, 2, 5),
                                                                           (call_script, "script_create_cattle_herd", "$current_town", reg10),
                                                                         (try_end),
                                                                       ]),

      ("village_bandits_defeated_cont",[],  "Refuse, stating that they need these items more than you do.",
      [
        (call_script, "script_change_player_relation_with_center", "$g_encountered_party", 3),
        (call_script, "script_change_player_honor", 1),
        (jump_to_menu, "mnu_village")]),
    ],
  )
]
