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
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

dplmc_affiliate_end_scripts = [
("dplmc_affiliate_end",
  [
    (store_script_param, ":cause", 1),

    (assign, "$g_player_affiliated_troop", 0),

    (try_begin),
      (eq, ":cause", 1),
      (assign, ":max_penalty", -16),
      (assign, ":term", 20),
      (assign, ":honor_val", 10),
    (else_try),
      (assign, ":max_penalty", -12),
      (assign, ":honor_val", 5),
      (assign, ":term", 15),
    (try_end),

    (try_for_range, ":family_member", lords_begin, kingdom_ladies_end),
      (call_script, "script_dplmc_is_affiliated_family_member", ":family_member"),
      (gt, reg0, 0),

      (store_skill_level, ":value", "skl_persuasion", "trp_player"),
      (store_random_in_range, ":value", 0, ":value"),
      ##nested diplomacy start+   Fix mistake.
      ##
      ##OLD:
      #(val_add, ":value", ":max_penalty", ":value"),
      #
      #NEW:
      #I'm pretty sure this is what was intended.
      (val_add, ":value", ":max_penalty"),
      ##nested diplomacy end+
      (val_min, ":value", 0),
      (call_script, "script_change_player_relation_with_troop", ":family_member", ":value"),
    (try_end),

    (try_begin),
      (gt, "$player_honor", ":honor_val"),
      (val_add, ":term", ":honor_val"),
    (else_try),
      (val_add, ":term", "$player_honor"),
    (try_end),

    (store_current_hours, ":cur_hours"),
    (store_sub, ":affiliated_hours", ":cur_hours", "$g_player_affiliated_time"),
    (store_div, ":affiliated_days", ":affiliated_hours", 24),
    (val_sub, ":term", ":affiliated_days"),
    (val_max, ":term", 0),
    (val_min, ":term", 40),


    (troop_get_slot, ":controversy", "trp_player", slot_troop_controversy),
    (val_add, ":controversy", ":term"),
    (val_min, ":controversy", 100),
    (troop_set_slot, "trp_player", slot_troop_controversy, ":controversy"),

  ])
]
