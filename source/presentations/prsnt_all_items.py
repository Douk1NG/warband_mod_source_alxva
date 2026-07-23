# -*- coding: cp1254 -*-
import string
from header_common import *
from header_presentations import *
from header_mission_templates import *
from ID_meshes import *
from header_operations import *
from header_triggers import *
#SB: import skills from ID_skills import *
from module_constants import *
##diplomacy start+ Import for use with terrain advantage
from header_terrain_types import *
from module_items import *
#SB : import colors
from module_factions import *
from header_items import *
##diplomacy end
from compiler import *

all_items = ("all_items", 0, 0, [
    (ti_on_presentation_load,
      [
        # Commented out - modmerge takes over
        ]),

    (ti_on_presentation_mouse_enter_leave,
      [
        # Commented out - modmerge takes over
        ]),

    (ti_on_presentation_event_state_change,
      [
        # Commented out - modmerge takes over
        ]),
  ])
