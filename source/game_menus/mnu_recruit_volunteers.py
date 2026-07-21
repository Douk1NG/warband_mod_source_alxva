# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

recruit_volunteers_menu = [
(
    "recruit_volunteers",0,
    "{s18}",
    "none",
    [
		 (start_presentation, "prsnt_recruit_volunteers"),
    ],
    [


      ("continue",
      [
        (eq, reg7, 0),
        (eq, reg5, 0),
      ], #noone willing to join
      "Continue...",
      [
        (party_set_slot, "$current_town", slot_center_volunteer_troop_amount, -1),
        (jump_to_menu,"mnu_village"),
      ]),

      ("recruit_them",
      [
        (eq, reg7, 0),
        (gt, reg5, 0),
      ],
      "Recruit them ({reg6} denars).",
      [
        (call_script, "script_village_recruit_volunteers_recruit"),

        (jump_to_menu,"mnu_village"),
      ]),

      #SB : disable_menu_option
      ("continue_not_enough_gold",
      [
        (eq, reg7, 1),
        (disable_menu_option),
      ],
      "I don't have enough money...",
      [
        (jump_to_menu,"mnu_village"),
      ]),

      ("forget_it",
      [
      #SB : conditions now not applied
        # (eq, reg7, 0),
        # (gt, reg5, 0),
      ],
      "Forget it.",
      [
        (jump_to_menu,"mnu_village"),
      ]),
    ],
  )
]
