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

overlay_container_add_listbox_item_scripts = [
("overlay_container_add_listbox_item", [
        (store_script_param, ":line_y", 1),
        (store_script_param, ":npc_id", 2),

        (set_container_overlay, "$g_jrider_character_relation_listbox"),

        # create text overlay for entry
        (create_text_overlay, reg10, s1, tf_left_align),
        (overlay_set_color, reg10, 0xDDDDDD),
        (position_set_x, pos1, 650),
        (position_set_y, pos1, 750),
        (overlay_set_size, reg10, pos1),
        (position_set_x, pos1, 0),
        (position_set_y, pos1, ":line_y"),
        (overlay_set_position, reg10, pos1),

        # create button
        (create_image_button_overlay, reg10, "mesh_white_plane", "mesh_white_plane"),
        (position_set_x, pos1, 0), # 590 real, 0 scrollarea
        (position_set_y, pos1, ":line_y"),
        (overlay_set_position, reg10, pos1),
        (position_set_x, pos1, 16000),
        (position_set_y, pos1, 750),
        (overlay_set_size, reg10, pos1),
        (overlay_set_alpha, reg10, 0),
        (overlay_set_color, reg10, 0xDDDDDD),

        # store relation of button id to character number for use in triggers
        (store_add, ":current_storage_index", "$g_base_character_presentation_storage_index", reg10),
        (troop_set_slot, "trp_temp_array_b", ":current_storage_index", "$num_charinfo_candidates"),

        # reset variables if appropriate flags are up
        (try_begin),
            (try_begin),
                (this_or_next|eq, "$g_jrider_pres_called_from_menu", 1),
                (ge, "$g_jrider_reset_selected_on_faction", 1),

                (assign, "$character_info_id", ":npc_id"),
                (assign, "$g_jrider_last_checked_indicator", reg10),
                (assign, "$g_latest_character_relation_entry", "$num_charinfo_candidates"),
            (try_end),
        (try_end),

        # close the container
        (set_container_overlay, -1),
   ])
]
