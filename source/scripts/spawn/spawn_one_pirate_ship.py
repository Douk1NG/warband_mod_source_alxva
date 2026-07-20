# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from module_constants import *
from header_parties import *
from header_troops import *
from header_skills import *
from header_mission_templates import *
from header_items import *
from header_triggers import *
from header_terrain_types import *
from header_music import *
from header_map_icons import *
from ID_animations import *

spawn_one_pirate_ship_scripts = [
#script_spawn_one_pirate_ship
# Spawns ONE ship of the currently least-represented pirate type and tags it.
("spawn_one_pirate_ship",
 [
  (store_num_parties_of_template, ":n_sr", "pt_sea_raiders_ship"),
  (store_num_parties_of_template, ":n_co", "pt_corsair_ship"),
  (store_num_parties_of_template, ":n_pi", "pt_pirate_ship"),
  (assign, ":spawn_tpl", "pt_sea_raiders_ship"),
  (assign, ":spawn_tag", 1),
  (assign, ":min_n", ":n_sr"),
  (try_begin),
    (lt, ":n_co", ":min_n"),
    (assign, ":spawn_tpl", "pt_corsair_ship"),
    (assign, ":spawn_tag", 2),
    (assign, ":min_n", ":n_co"),
  (try_end),
  (try_begin),
    (lt, ":n_pi", ":min_n"),
    (assign, ":spawn_tpl", "pt_pirate_ship"),
    (assign, ":spawn_tag", 4),
    (assign, ":min_n", ":n_pi"),
  (try_end),
  (try_begin),
    (eq, ":spawn_tpl", "pt_sea_raiders_ship"),
    (assign, ":spawn_point", "p_reserved_1"),
  (else_try),
    (eq, ":spawn_tpl", "pt_corsair_ship"),
    (assign, ":spawn_point", "p_reserved_3"),
  (else_try),
    (assign, ":spawn_point", "p_reserved_2"),
  (try_end),
  (set_spawn_radius, 25),
  (spawn_around_party, ":spawn_point", ":spawn_tpl"),
  (assign, ":party_no", reg0),
  (gt, ":party_no", 0),
  (party_set_slot, ":party_no", slot_party_ship_type, ":spawn_tag"),
 ])
]
