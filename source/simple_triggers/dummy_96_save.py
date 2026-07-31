# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from header_parties import *
from header_items import *
from header_skills import *
from header_triggers import *
from header_troops import *
from header_music import *
from header_terrain_types import *
from module_factions import dplmc_factions_end

from module_constants import *

from compiler import *

dummy_96_save_simple_triggers = [
(96, # Dummy trigger because removing it crashes saves.
   [
    #(eq, "$g_player_banner_granted", 1),
    #(neq, "$g_custom_banner_new_game", 1),
    #(assign, "$g_custom_banner_new_game", 1),
    #(le,"$auto_menu",0),
    #(troop_get_slot, ":flag_spr", "trp_player", slot_troop_custom_banner_flag_type),
    #(lt, ":flag_spr", 0),
	#normal_banner_begin
	#    (start_presentation, "prsnt_banner_selection"),
	#custom_banner_begin
	#    (start_presentation, "prsnt_custom_banner"),
    #(assign, "$g_edit_banner_troop", "trp_player"),
    #(jump_to_menu, "mnu_choose_banner"),
   ]),
]
