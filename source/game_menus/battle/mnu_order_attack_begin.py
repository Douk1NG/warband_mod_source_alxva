# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

order_attack_begin_menu = [
(
    "order_attack_begin",0,
    "Your troops prepare to attack the enemy.",
    "none",
    [],
    [
      ("order_attack_begin",[],"Order the attack to begin.",
      [
        (party_get_template_id, ":encountered_party_template", "$g_encountered_party"),
        (try_begin),
		  (eq, ":encountered_party_template", "pt_village_farmers"),
		  (unlock_achievement, ACHIEVEMENT_HELP_HELP_IM_BEING_REPRESSED),
		(try_end),

        (assign, "$g_engaged_enemy", 1),
        (jump_to_menu,"mnu_order_attack_2"),
      ]),
      ("call_back",[],"Call them back.",[(jump_to_menu,"mnu_simple_encounter")]),
    ]
  )
]
