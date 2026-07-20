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

faction_last_reconnoitered_center_scripts = [
("faction_last_reconnoitered_center",
  [
    (store_script_param, ":faction_no", 1),
    (store_script_param, ":center_no", 2),

    (store_sub, ":faction_recce_slot", ":faction_no", kingdoms_begin),
    (val_add, ":faction_recce_slot", slot_center_last_reconnoitered_by_faction_time),
    (store_current_hours, ":hours_since_last_recon"),
    (party_get_slot, ":last_recon_time", ":center_no", ":faction_recce_slot"),

    (try_begin),
      (lt, ":last_recon_time", 1),
      (assign, ":hours_since_last_recon", 1000),
    (else_try),
      (val_sub, ":hours_since_last_recon", ":last_recon_time"),
    (try_end),

    (assign, reg0, ":hours_since_last_recon"),
    (assign, reg1, ":last_recon_time"),
  ])
]
