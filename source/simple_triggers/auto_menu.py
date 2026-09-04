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




#Auto-menu
 #Auto-menu
#Auto-menu
  

auto_menu_simple_triggers = [
(0,
   [         
     (try_begin),
       (gt, "$g_last_rest_center", 0),
       (eq, "$g_siege_force_wait", 0), #respect player-initiated wait from mnu_castle_besiege wait_24_hours
       (party_get_battle_opponent, ":besieger_party", "$g_last_rest_center"),
       (gt, ":besieger_party", 0),
       (store_faction_of_party, ":encountered_faction", "$g_last_rest_center"),
       (store_relation, ":faction_relation", ":encountered_faction", "fac_player_supporters_faction"),
       (store_faction_of_party, ":besieger_party_faction", ":besieger_party"),
       (store_relation, ":besieger_party_relation", ":besieger_party_faction", "fac_player_supporters_faction"),
       (ge, ":faction_relation", 0),
       (lt, ":besieger_party_relation", 0),
       (start_encounter, "$g_last_rest_center"),
       (rest_for_hours, 0, 0, 0), #stop resting
     (else_try),
       (store_current_hours, ":cur_hours"),
       (assign, ":check", 0),
       (try_begin),
         (neq, "$g_check_autos_at_hour", 0),
         (ge, ":cur_hours", "$g_check_autos_at_hour"),
         (assign, ":check", 1),
         (assign, "$g_check_autos_at_hour", 0),
       (try_end),
       (this_or_next|eq, ":check", 1),
       (map_free),
       (try_begin),
         (ge,"$auto_menu",1),
         (jump_to_menu,"$auto_menu"),
         (assign,"$auto_menu",-1),
       (else_try),
         (ge,"$auto_enter_town",1),
         (start_encounter, "$auto_enter_town"),
       #(else_try),  ### Comment out this entire else_try
         #(ge,"$auto_besiege_town",1), ### Here
         #(start_encounter, "$auto_besiege_town"), ###And here, too
       (else_try),
         (ge,"$g_camp_mode", 1),
         (assign, "$g_camp_mode", 0),
         (assign, "$g_infinite_camping", 0),
         (assign, "$g_player_icon_state", pis_normal),
         
         (rest_for_hours, 0, 0, 0), #stop camping
                 
         (display_message, "@Breaking camp..."),
       (try_end),
     (try_end),
     ]),
]
