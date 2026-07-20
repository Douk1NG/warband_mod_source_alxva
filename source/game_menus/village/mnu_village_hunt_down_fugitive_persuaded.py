# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

village_hunt_down_fugitive_persuaded_menu = [
(
    "village_hunt_down_fugitive_persuaded",0,
 "As the party member with the highest persuasion, {reg3?you:{s3}} managed to cajole the location of {s50} from his tight-lipped relatives. Backed with superior force of arms, your just argument seemed to take effect and the villagers grudgingly participate in the manhunt for the fugitive.\
 {reg4?But word of you arrival has reached the fugitive and he appears to have taken his own life:Within the hour, you've secured the fugitive on behalf of {s4}}.",
    "none",
    [   (call_script, "script_get_max_skill_of_player_party", "skl_persuasion"),
        (assign, ":max_skill_owner", reg1),
        (quest_get_slot, ":quest_target_dna", "qst_hunt_down_fugitive", slot_quest_target_dna),
        (call_script, "script_get_name_from_dna_to_s50", ":quest_target_dna"),

         #SB : tableau at bottom
         (try_begin),
           (eq, ":max_skill_owner", "trp_player"),
           (assign, reg3, 1),
         (else_try),
           (assign, reg3, 0),
           (str_store_troop_name, s3, ":max_skill_owner"),
           (call_script, "script_change_troop_renown", ":max_skill_owner", dplmc_companion_skill_renown),
         (try_end),

        (set_fixed_point_multiplier, 100),
        (position_set_x, pos0, 70),
        (position_set_y, pos0, 5),
        (position_set_z, pos0, 75),
        (set_game_menu_tableau_mesh, "tableau_troop_note_mesh", ":max_skill_owner", pos0),
        (store_random_in_range, reg4, 0, 2), #TODO add some conditions, renown, time of day, etc
        (try_begin),
          (eq, reg4, 0),
          (party_force_add_prisoners, "p_main_party", "trp_fugitive", 1),
          (quest_get_slot, ":quest_giver_troop", "qst_hunt_down_fugitive", slot_quest_giver_troop),
          (str_store_troop_name, s4, ":quest_giver_troop"),
          (quest_set_slot, "qst_hunt_down_fugitive", slot_quest_current_state, 2),
        (else_try), #killed, player can claim credit
          (quest_set_slot, "qst_hunt_down_fugitive", slot_quest_current_state, 1),
        (try_end),
    ],

    [
      ("continue",[],"Continue...",[
        (call_script, "script_succeed_quest", "qst_hunt_down_fugitive"),
        (jump_to_menu, "mnu_village"),

      ]),
    ],
  )
]
