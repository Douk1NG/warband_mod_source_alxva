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

change_debt_to_troop_scripts = [
("change_debt_to_troop",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":new_debt"),

      (troop_get_slot, ":cur_debt", ":troop_no", slot_troop_player_debt),
      (assign, reg1, ":cur_debt"),
      (val_add, ":cur_debt", ":new_debt"),
      (assign, reg2, ":cur_debt"),
      (troop_set_slot, ":troop_no", slot_troop_player_debt, ":cur_debt"),
      (try_begin), #SB : display only if > 0
        (gt, ":cur_debt", 0),
        (str_store_troop_name_link, s1, ":troop_no"),
        (display_message, "@You now owe {reg2} denars to {s1}.", message_negative),
      (try_end),
  ])
]
