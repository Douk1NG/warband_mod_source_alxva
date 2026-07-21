# ======================================================================
# SHARED DEPENDENCY
# Entity: change_player_relation_with_lords_after_battle (script)
# Called by menus in 2 domains: battle, castle
# ======================================================================

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

change_player_relation_with_lords_after_battle_scripts = [
("change_player_relation_with_lords_after_battle",
    [
      (try_for_range, ":hero", active_npcs_begin, active_npcs_end),
        (party_count_companions_of_type, ":hero_present", "p_collective_friends", ":hero"),
        (gt, ":hero_present", 0),
        (troop_slot_eq, ":hero", slot_troop_occupation, slto_kingdom_hero),
        (troop_get_slot, ":reputation", ":hero", slot_lord_reputation_type),
        (call_script, "script_troop_get_player_relation", ":hero"),
        (assign, ":troop_relation", reg0),
        (assign, ":relation_change", 1),
        (try_begin),
          (lt, ":troop_relation", -5),
          (assign, ":relation_change", 0),
        (else_try),
          (eq, ":reputation", lrep_martial),
          (assign, ":relation_change", 2),
        (try_end),
        (call_script, "script_change_player_relation_with_troop", ":hero", ":relation_change"),
      (try_end),
    ])
]
