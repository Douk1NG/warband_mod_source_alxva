# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

village_loot_no_resist_menu = [
(
    "village_loot_no_resist",0,
    "The villagers here are few and frightened, and they quickly scatter and run before you.\
 The village is at your mercy.",
    "none",
    [
    #SB : if we just wanted to steal food, return to doing that instead of plundering
    (try_begin),
      (eq, "$auto_enter_menu_in_center", "mnu_village_take_food"),
      (jump_to_menu, "$auto_enter_menu_in_center"),
    (try_end),

    ],
    [
      ("village_loot",[], "Plunder the village, then raze it.",
        [
          (call_script, "script_village_set_state", "$current_town", svs_being_raided),
          (party_set_slot, "$current_town", slot_village_raided_by, "p_main_party"),
          (assign,"$g_player_raiding_village","$current_town"),

          (try_begin),
            (store_faction_of_party, ":village_faction", "$current_town"),
            (store_relation, ":relation", "$players_kingdom", ":village_faction"),
            (ge, ":relation", 0),
            (call_script, "script_diplomacy_party_attacks_neutral", "p_main_party", "$current_town"),
          (try_end),

          (rest_for_hours_interactive, 3, 5, 1), #rest while attackable (3 hours will be extended by the trigger)
          (party_set_slot, "$current_town", slot_town_last_nearby_fire_time, 1), #raiding mode
          # (assign, "$g_village_raid_evil", 1), #SB : to differentiate between raiding
          (change_screen_return),
        ]),

        #SB : alternative option if that's your thing
      ("village_enslave", [
          (party_get_num_companions, ":amount", "$current_town"),
          (gt, ":amount", 0), #if we haven't killed them all in the first charge
          # (party_get_free_prisoners_capacity, ":capacity", "p_main_party"), #be slightly wary of this operation
          # (gt, ":capacity", 0), #if we have room
          (troops_can_join_as_prisoner, 1),
        ], "Chase after the remaining villagers and enslave them.",
        [
          (call_script, "script_village_set_state", "$current_town", svs_being_raided), #target is deserted, not looted
          (party_set_slot, "$current_town", slot_village_raided_by, "p_main_party"),
          (assign,"$g_player_raiding_village","$current_town"),

          (try_begin),
            (store_faction_of_party, ":village_faction", "$current_town"),
            (store_relation, ":relation", "$players_kingdom", ":village_faction"),
            (ge, ":relation", 0),
            (call_script, "script_diplomacy_party_attacks_neutral", "p_main_party", "$current_town"),
          (try_end),

          #add a party template to represent hiding villagers so we don't go empty-handed
          (party_add_template, "$current_town", "pt_women"),
          (party_add_template, "$current_town", "pt_women"),
          #(party_add_template, "$current_town", "pt_village_defenders"),
          #add some smoke right away
          # (party_add_particle_system, "$current_town", "psys_map_village_fire"),

          (rest_for_hours, 3, 5, 1), #rest while attackable
          # (assign, "$g_village_raid_evil", 2),
          (party_set_slot, "$current_town", slot_town_last_nearby_fire_time, 2), #enslavement mode
          (assign, "$qst_eliminate_bandits_infesting_village_num_villagers", 0),
          (change_screen_return),
        ]),
      ("village_raid_leave",[],"Leave this village alone.",[(change_screen_return)]),
    ],
  )
]
