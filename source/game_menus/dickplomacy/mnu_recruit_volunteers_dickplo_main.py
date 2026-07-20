# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

recruit_volunteers_dickplo_main_menu = [
(
  "recruit_volunteers_dickplo_main",0,
  "How would you like to recruit volunteers?",
  "none",
  [
  #Floris tableau_troop_note_mesh for menus
         (try_begin),
          (party_get_slot, ":center_lord", "$current_town", slot_town_lord),
          (ge, ":center_lord", 0),
          (set_fixed_point_multiplier, 100),
          (position_set_x, pos1, 70),
          (position_set_y, pos1, 5),
          (position_set_z, pos1, 75),
          (set_game_menu_tableau_mesh, "tableau_troop_note_mesh", ":center_lord", pos1),
          (try_end),
  #End tableau mesh
  ],
  [
      #Force Recruit by Topper, heavily moddified by LilyModzStuff
      ("forced_recruits",
      [
        # Standard check
        (neg|party_slot_eq, "$current_town", slot_village_state, svs_looted),
        (neg|party_slot_eq, "$current_town", slot_village_state, svs_being_raided),
        (neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
        # Check if party have enough free slots
        (assign, ":mod_amount", 7),
        (party_get_free_companions_capacity, ":mod_capacity", "p_main_party"),
        (ge, ":mod_capacity", ":mod_amount"),
       ]
       ,"Force villagers to join your army.",
       [
        (assign, ":mod_amount", 7),
        #Center relation check
        (try_begin),
        (assign, ":mod_rel_change", -15),
        (party_get_slot, ":center_relation", "$current_town", slot_center_player_relation),
        (ge, ":mod_rel_change", ":center_relation"),
        (display_message, "@The villagers have decided to revolt!"),
        (jump_to_menu, "mnu_village_start_attack"),
        (else_try),
        (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
        (val_min, ":mod_amount", ":free_capacity"),
        (party_get_slot, ":mod_troop", "$current_town", slot_center_volunteer_troop_type),
        (party_add_members, "p_main_party", ":mod_troop", 7), #the original script used 30 but that was way to high.
        # Change relation and subtract honor, and companion objections
        (call_script, "script_change_player_relation_with_center", "$current_town", -15),
        (call_script, "script_change_player_honor", -3), #Should be an honor loss as well
        (display_message, "@You have forced the villigers to join your army by force."),
        (call_script, "script_objectionable_action", tmt_humanitarian, "str_force_into_party"), #humanitarian don't like it when you steal.
        (try_end),
        ]),
        #End force recruit
              ("recruit_normal_volunteers",
               [
               ],
               "Recruit volunteers.",
               [
               (jump_to_menu,"mnu_recruit_volunteers"),
              ]),
        ("recruit_normal_volunteers",
        [
        ],
        "Return to village.",
        [
        (jump_to_menu,"mnu_village"),
    ]),
  ])
]
