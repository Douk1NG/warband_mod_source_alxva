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

spawn_party_type_with_cooldown_scripts = [
("spawn_party_type_with_cooldown",
  [
   (store_script_param, ":party_template", 1),
   (store_script_param, ":base_spawn_point", 2),
   (store_script_param, ":num_spawn_points", 3),
   (store_script_param, ":max_parties", 4),

    (assign, reg0, -1),
    (store_num_parties_of_template, ":num", ":party_template"),

    (try_begin),
    (lt, ":num", ":max_parties"),
    (party_template_get_slot, ":next", ":party_template", slot_party_template_respawn_cooldown),
    (store_current_hours, ":cur"),

    (try_begin),
      # initial seed: never spawned yet (slot == 0) -> fill straight to cap at once
      (eq, ":next", 0),
      (assign, ":to_spawn", ":max_parties"),
      (val_sub, ":to_spawn", ":num"),
      (try_for_range, ":i", 0, ":to_spawn"),
        (try_begin),
          (gt, ":num_spawn_points", 1),
          (store_random, ":sp", ":num_spawn_points"),
          (val_add, ":sp", ":base_spawn_point"),
        (else_try),
          (assign, ":sp", ":base_spawn_point"),
        (try_end),
        (try_begin),
          (party_is_active, ":sp"),
          (set_spawn_radius, 0),
          (spawn_around_party, ":sp", ":party_template"),
        (try_end),
      (try_end),
      (party_template_set_slot, ":party_template", slot_party_template_respawn_cooldown, ":cur"),
    (else_try),
      # ongoing trickle: at most 1 party per bandit_respawn_interval_hours
      (ge, ":cur", ":next"),
      (try_begin),
        (gt, ":num_spawn_points", 1),
        (store_random, ":sp", ":num_spawn_points"),
        (val_add, ":sp", ":base_spawn_point"),
      (else_try),
        (assign, ":sp", ":base_spawn_point"),
      (try_end),
      (try_begin),
        (party_is_active, ":sp"),
        (set_spawn_radius, 0),
        (spawn_around_party, ":sp", ":party_template"),
      (try_end),
      (store_current_hours, ":cur2"),
      (val_add, ":cur2", bandit_respawn_interval_hours),
      (party_template_set_slot, ":party_template", slot_party_template_respawn_cooldown, ":cur2"),
    (try_end),
  (try_end),
 ])
]
