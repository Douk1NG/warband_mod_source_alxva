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
from ID_strings import str_key_0
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

wse_get_agent_scale_scripts = [
("wse_get_agent_scale", [

    # (set_fixed_point_multiplier, 100),

    # (assign, ":scale", 100),

    # # (try_begin),
        # # (gt, ":horse_item_no", -1),
        # # (eq, ":horse_item_modifier", imodbit_heavy),
        # # (val_add, ":scale", 5),
        # # (set_trigger_result, ":scale"),
    # # (try_end),

    # (try_begin),
        # (gt, ":troop_no", -1),
        # (neg|troop_is_hero, ":troop_no"),
        # (troop_get_type, ":type", ":troop_no"),
        # (lt, ":type", 2),
        # (store_random_in_range, ":scale", 95, 105),
        # (store_attribute_level, ":str", ":troop_no", ca_strength),
        # (val_sub, ":str", 6),
        # (val_div, ":str", 3),
        # (val_add, ":scale", ":str"),

        # (try_begin),
            # (eq, ":type", 1),
            # (val_mul, ":scale", 93),
            # (val_div, ":scale", 100),
        # (try_end),

        # # (assign, reg0, ":scale"),
        # # (display_message, "@{reg0}"),

        # (set_trigger_result, ":scale"),
    # (try_end),


])
]
