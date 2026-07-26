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

get_spawn_report_line_scripts = [
#script_get_spawn_report_line
# INPUT: arg1 = party_template, arg2 = max_parties (cap), arg3 = has_lair (1/0)
# OUTPUT:
#   reg1 = active roaming parties
#   reg2 = cap
#   reg3 = cooldown left for next patrol (hours)
#   reg4 = lair: 1=active, 0=defeated
#   reg5 = cooldown left for lair respawn (hours, 0=ready)
#   s0 = "active/cap"
#   s3 = patrol cooldown text
#   s4 = lair status text (Active / Defeated)
#   s5 = lair cooldown text
("get_spawn_report_line",
 [
  (store_script_param, ":party_template", 1),
  (store_script_param, ":cap", 2),
  (store_script_param, ":has_lair", 3),

  (store_num_parties_of_template, ":num", ":party_template"),

  (store_current_hours, ":cur_hours"),
  (val_max, ":cur_hours", 0),

  # Party patrol cooldown
  (party_template_get_slot, ":patrol_cd", ":party_template", slot_party_template_respawn_cooldown),
  (val_max, ":patrol_cd", 0),
  (store_sub, ":patrol_left", ":patrol_cd", ":cur_hours"),
  (try_begin),
    (lt, ":patrol_left", 0),
    (assign, ":patrol_left", 0),
  (try_end),

  # Lair status + respawn cooldown
  (assign, ":lair_active", 0),
  (assign, ":lair_cd_left", 0),
  (try_begin),
    (eq, ":has_lair", 1),
    (party_template_get_slot, ":lair_party", ":party_template", slot_party_template_lair_party),
    (gt, ":lair_party", 1),
    (assign, ":lair_active", 1),
    (party_template_get_slot, ":lair_cd", ":party_template", slot_party_template_lair_next_spawn),
    (val_max, ":lair_cd", 0),
    (store_sub, ":lair_cd_left", ":lair_cd", ":cur_hours"),
    (try_begin),
      (lt, ":lair_cd_left", 0),
      (assign, ":lair_cd_left", 0),
    (try_end),
  (try_end),

  (assign, reg1, ":num"),
  (assign, reg2, ":cap"),
  (assign, reg3, ":patrol_left"),
  (assign, reg4, ":lair_active"),
  (assign, reg5, ":lair_cd_left"),

  (str_store_string, s0, "@{reg1}/{reg2} patrols"),

  (try_begin),
    (eq, ":patrol_left", 0),
    (str_store_string, s3, "@ready"),
  (else_try),
    (str_store_string, s3, "@{reg3}h"),
  (try_end),

  (try_begin),
    (eq, ":has_lair", 0),
    (str_store_string, s4, "@-"),
    (str_store_string, s5, "@-"),
  (else_try),
    (eq, ":lair_active", 1),
    (str_store_string, s4, "@Lair UP"),
    (str_store_string, s5, "@next: {s3}"),
  (else_try),
    (str_store_string, s4, "@Lair DOWN"),
    (str_store_string, s5, "@respawn: {s3}"),

    (try_begin),
      (eq, ":lair_cd_left", 0),
      (str_store_string, s3, "@ready"),
    (else_try),
      (str_store_string, s3, "@{reg5}h"),
    (try_end),
    (str_store_string, s5, "@respawn: {s3}  |  next patrol: ready"),
    (str_store_string, s3, "@ready"),
  (try_end),

  (try_begin),
    (eq, ":has_lair", 1),
    (eq, ":lair_active", 1),
    (str_store_string, s0, "@{s0}  |  {s4}  |  {s5}"),
  (else_try),
    (str_store_string, s0, "@{s0}  |  {s4}  |  {s5}"),
  (try_end),
  ])
]
