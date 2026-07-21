# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

village_take_food_menu = [
(
    "village_take_food",0,
    "The villagers grudgingly bring out what they have for you.",
    "none",
    [
       (call_script, "script_party_count_members_with_full_health","p_main_party"),
       (assign, ":player_party_size", reg0),
       (call_script, "script_party_count_members_with_full_health","$current_town"),
       (assign, ":villagers_party_size", reg0),
       (try_begin),
         (lt, ":player_party_size", 6),
         (ge, ":villagers_party_size", 40),
         (neg|party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
         (jump_to_menu, "mnu_village_start_attack"),
       (try_end),
    ],
    [
      ("take_supplies",[],"Take the supplies.",
       [
         (try_begin),
           (party_slot_ge, "$current_town", slot_center_player_relation, -55),
           (try_begin),
             (party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
             (call_script, "script_change_player_relation_with_center", "$current_town", -1),
           (else_try),
             (call_script, "script_change_player_relation_with_center", "$current_town", -3),
           (try_end),
         (try_end),
         (party_get_slot, ":village_lord", "$current_town", slot_town_lord),
         (try_begin),
           (gt,  ":village_lord", 1),
           (call_script, "script_change_player_relation_with_troop", ":village_lord", -1),
          (try_end),
         (party_get_slot, ":merchant_troop", "$current_town", slot_town_elder),
         (party_get_skill_level, ":player_party_looting", "p_main_party", "skl_looting"),
         (val_mul, ":player_party_looting", 3),
         (store_sub, ":random_chance", 70, ":player_party_looting"), #Increases the chance of looting by 3% per skill level
         (try_for_range, ":slot_no", num_equipment_kinds ,max_inventory_items + num_equipment_kinds),
           (store_random_in_range, ":rand", 0, 100),
           (lt, ":rand", ":random_chance"),
           (troop_set_inventory_slot, ":merchant_troop", ":slot_no", -1),
         (try_end),

###NPC companion changes begin
         (call_script, "script_objectionable_action", tmt_humanitarian, "str_steal_from_villagers"),
#NPC companion changes end
#Troop commentary changes begin
          (call_script, "script_add_log_entry", logent_village_extorted, "trp_player",  "$current_town", -1, -1),
          (store_faction_of_party,":village_faction",  "$current_town"),
          #SB : this war penalty should be lower for accosting farmers instead of raiding outright
          (call_script, "script_faction_inflict_war_damage_on_faction", "$players_kingdom", ":village_faction", 3),
#Troop commentary changes end

         #SB : sometimes this will actually be empty
         (jump_to_menu, "mnu_village"),
         (troop_sort_inventory, ":merchant_troop"),
         (change_screen_loot, ":merchant_troop"),
         ]),
      ("let_them_keep_it",[],"Let them keep it.",[(jump_to_menu, "mnu_village")]),
    ],
  )
]
