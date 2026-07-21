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

deactivate_player_faction_scripts = [
("deactivate_player_faction",
    [
    (faction_set_slot, "fac_player_supporters_faction", slot_faction_state, sfs_inactive),
    (faction_set_slot, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
    (assign, "$players_kingdom", 0),
    (assign, "$players_oath_renounced_against_kingdom", 0),
    (assign, "$players_oath_renounced_given_center", 0),
    (assign, "$players_oath_renounced_begin_time", 0),
    #(call_script, "script_store_average_center_value_per_faction"),
    (call_script, "script_update_all_notes"),

    (try_begin),
        (is_between, "$g_player_minister", companions_begin, companions_end),
        (assign, "$npc_to_rejoin_party", "$g_player_minister"),
    (try_end),
    (assign, "$g_player_minister", -1),

    (call_script, "script_add_notification_menu", "mnu_notification_player_faction_deactive", 0, 0),
    ])
]
