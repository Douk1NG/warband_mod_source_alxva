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

create_kingdom_party_if_below_limit_scripts = [
("create_kingdom_party_if_below_limit",
    [
      (store_script_param_1, ":faction_no"),
      (store_script_param_2, ":party_type"),

      (call_script, "script_count_parties_of_faction_and_party_type", ":faction_no", ":party_type"),
      (assign, ":party_count", reg0),

      (assign, ":party_count_limit", 0),

      (faction_get_slot, ":num_towns", ":faction_no", slot_faction_num_towns),

      (try_begin),
##        (eq, ":party_type", spt_forager),
##        (assign, ":party_count_limit", 1),
##      (else_try),
##        (eq, ":party_type", spt_scout),
##        (assign, ":party_count_limit", 1),
##      (else_try),
##        (eq, ":party_type", spt_patrol),
##        (assign, ":party_count_limit", 1),
##      (else_try),
##        (eq, ":party_type", spt_messenger),
##        (assign, ":party_count_limit", 1),
##      (else_try),
        (eq, ":party_type", spt_kingdom_caravan),
        (try_begin),
          (eq, ":num_towns", 0),
          (assign, ":party_count_limit", 0),
        (else_try),
          (eq, ":num_towns", 1),
          (assign, ":party_count_limit", 1),
        (else_try),
          (eq, ":num_towns", 2),
          (assign, ":party_count_limit", 3),
        (else_try),
          (assign, ":party_count_limit", 5),
        (try_end),
        ##diplomacy begin
          #overwriting party count limit MAX(2 * X - 1, 0)
        (store_mul, ":party_count_limit", ":num_towns", 2),
        (val_sub, ":party_count_limit", 1),
        (val_max, ":party_count_limit", 0),
        ##diplomacy end

##      (else_try),
##        (eq, ":party_type", spt_prisoner_train),
##        (assign, ":party_count_limit", 1),
      (try_end),

      (assign, reg0, -1),
      (try_begin),
        (lt, ":party_count", ":party_count_limit"),
        (call_script,"script_cf_create_kingdom_party", ":faction_no", ":party_type"),
      (try_end),
  ])
]
