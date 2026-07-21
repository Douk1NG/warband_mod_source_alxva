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

dplmc_copy_upgrade_to_all_heroes_scripts = [
("dplmc_copy_upgrade_to_all_heroes",
  [
    (store_script_param_1, ":troop"),
    (store_script_param_2, ":type"),

    (try_begin),
      (eq, ":type", dplmc_wpn_setting_1),
      (troop_get_slot,":upg_wpn0", ":troop",dplmc_slot_upgrade_wpn_0),
      (troop_get_slot,":upg_wpn1", ":troop",dplmc_slot_upgrade_wpn_1),
      (troop_get_slot,":upg_wpn2", ":troop",dplmc_slot_upgrade_wpn_2),
      (troop_get_slot,":upg_wpn3", ":troop",dplmc_slot_upgrade_wpn_3),
      (try_for_range, ":hero", heroes_begin, heroes_end),
        (troop_set_slot,":hero",dplmc_slot_upgrade_wpn_0,":upg_wpn0"),
        (troop_set_slot,":hero",dplmc_slot_upgrade_wpn_1,":upg_wpn1"),
        (troop_set_slot,":hero",dplmc_slot_upgrade_wpn_2,":upg_wpn2"),
        (troop_set_slot,":hero",dplmc_slot_upgrade_wpn_3,":upg_wpn3"),
      (try_end),
    (else_try),
      (eq, ":type", dplmc_armor_setting),
      (troop_get_slot,":upg_armor", ":troop",dplmc_slot_upgrade_armor),
      (try_for_range, ":hero", heroes_begin, heroes_end),
        (troop_set_slot,":hero",dplmc_slot_upgrade_armor,":upg_armor"),
      (try_end),
    (else_try),
      (eq, ":type", dplmc_horse_setting),
      (troop_get_slot,":upg_horse", ":troop",dplmc_slot_upgrade_horse),
      (try_for_range, ":hero", heroes_begin, heroes_end),
        (troop_set_slot,":hero",dplmc_slot_upgrade_horse,":upg_horse"),
      (try_end),
    (try_end),
  ])
]
