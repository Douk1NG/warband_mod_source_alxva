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

multiplayer_fill_available_factions_combo_button_scripts = [
# script_multiplayer_fill_available_factions_combo_button
# Input: arg1 = overlay_id, arg2 = selected_faction_no, arg3 = opposite_team_selected_faction_no
# Output: none
("multiplayer_fill_available_factions_combo_button",
   [
     (store_script_param, ":overlay_id", 1),
     (store_script_param, ":selected_faction_no", 2),
##     (store_script_param, ":opposite_team_selected_faction_no", 3),
##     (try_for_range, ":cur_faction", "fac_kingdom_1", "fac_kingdoms_end"),
##       (try_begin),
##         (eq, ":opposite_team_selected_faction_no", ":cur_faction"),
##         (try_begin),
##           (gt, ":selected_faction_no", ":opposite_team_selected_faction_no"),
##           (val_sub, ":selected_faction_no", 1),
##         (try_end),
##       (else_try),
##         (str_store_faction_name, s0, ":cur_faction"),
##         (overlay_add_item, ":overlay_id", s0),
##       (try_end),
##     (try_end),
##     (val_sub, ":selected_faction_no", "fac_kingdom_1"),
##     (overlay_set_val, ":overlay_id", ":selected_faction_no"),
     (try_for_range, ":cur_faction", npc_kingdoms_begin, npc_kingdoms_end),
       (str_store_faction_name, s0, ":cur_faction"),
       (overlay_add_item, ":overlay_id", s0),
     (try_end),
     (val_sub, ":selected_faction_no", "fac_kingdom_1"),
     (overlay_set_val, ":overlay_id", ":selected_faction_no"),
     ])
]
