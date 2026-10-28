# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
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

agent_fix_division_scripts = [
("agent_fix_division", [
      (store_script_param_1, ":agent"),
      (agent_set_slot, ":agent", slot_agent_new_division, -1),
      (get_player_agent_no, ":player"),	#after_mission_start triggers are called after spawn, so globals can't be used
      #yet

      (try_begin),
        (ge, ":player", 0),
        (neq, ":agent", ":player"),
        (agent_is_human, ":agent"),
        # Keep agents already assigned to a custom/hero division untouched.
        (agent_get_division, ":division", ":agent"),
        (gt, ":division", grc_cavalry),
        (else_try),
          (assign, ":target_division", grc_infantry),
          (assign, ":has_bow", 0),
          (try_for_range, ":item_slot", ek_item_0, ek_head),
            (agent_get_item_slot, ":item", ":agent", ":item_slot"),
            (ge, ":item", 0),
            (item_get_type, ":item_type", ":item"),
            (this_or_next | eq, ":item_type", itp_type_bow),
            (eq, ":item_type", itp_type_crossbow),
            (assign, ":has_bow", 1),
          (try_end),

          (try_begin),
            (neq, ":has_bow", 0),
            (assign, ":target_division", grc_archers),
          (else_try),
            (agent_get_horse, ":horse", ":agent"),
            (ge, ":horse", 0),
            (assign, ":target_division", grc_cavalry),
          (try_end),

          (neq, ":division", ":target_division"),
          (agent_set_division, ":agent", ":target_division"),
          (agent_set_slot, ":agent", slot_agent_new_division, ":target_division"),
      (try_end),])
]
