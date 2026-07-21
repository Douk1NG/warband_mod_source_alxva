# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

village_enslave_complete_menu = [
(
    "village_enslave_complete",mnf_disable_all_keys,
    "On your orders your troops rampage through the village, dragging peasants from their hovels and stripping them of all possessions.\
 In the span of a few hours you've rounded up {reg1} prisoners, leaving the infirm and the younglings behind. As you march the trussed-up villagers away from the cooling ember of their broken hearths, you hear a distant howl...",
    "none",
    [
        (get_achievement_stat, ":number_of_village_raids", ACHIEVEMENT_THE_BANDIT, 0),
        (get_achievement_stat, ":number_of_caravan_raids", ACHIEVEMENT_THE_BANDIT, 1),
        (val_add, ":number_of_village_raids", 1),
        (set_achievement_stat, ACHIEVEMENT_THE_BANDIT, 0, ":number_of_village_raids"),

        (try_begin),
          (ge, ":number_of_village_raids", 3),
          (ge, ":number_of_caravan_raids", 3),
          (unlock_achievement, ACHIEVEMENT_THE_BANDIT),
        (try_end),

        (set_background_mesh, "mesh_pic_prisoner_wilderness"),
        (call_script, "script_objectionable_action", tmt_humanitarian, "str_sell_slavery"),

        # (party_get_slot, ":village_lord", "$current_town", slot_town_lord),
        # (try_begin),
          # (gt,  ":village_lord", 0),
          # (call_script, "script_change_player_relation_with_troop", ":village_lord", -5),
        # (try_end),
        (store_random_in_range, ":enmity", -35, -25),
        (call_script, "script_change_player_relation_with_center", "$current_town", ":enmity"),

        (party_add_particle_system, "$current_town", "psys_map_village_looted_smoke"),
        (store_faction_of_party, ":village_faction", "$current_town"),
        (store_relation, ":relation", ":village_faction", "fac_player_supporters_faction"),
        (try_begin),
          (lt, ":relation", 0),
          (call_script, "script_change_player_relation_with_faction", ":village_faction", -2),
        (try_end),

        (store_mul, ":morale_decrease", "$qst_eliminate_bandits_infesting_village_num_villagers", -150),
        (call_script, "script_change_faction_troop_morale", ":village_faction", ":morale_decrease", 1), #SB : script call
        (assign, reg1, "$qst_eliminate_bandits_infesting_village_num_villagers"),
      ],
    [
      ("continue",[], "Continue...",
       [
            (assign, "$g_leave_town", 1),
            (jump_to_menu, "mnu_village"),
        ]),
    ],
  )
]
