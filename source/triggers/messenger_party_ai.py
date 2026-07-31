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



#Messengers
#  (4.2, 0, 0.0, [],
#   [(assign, "$pin_faction", "fac_swadians"),
#    (assign, "$pin_party_template", "pt_swadian_messenger"),
#    (assign, "$pin_limit", peak_kingdom_messengers),
#    (call_script,"script_cf_spawn_party_at_faction_town_if_below_limit"),
#    (party_set_ai_behavior,"$pout_party",ai_bhvr_travel_to_party),
#    (party_set_ai_object,"$pout_party","$pout_town"),
#    ]),

#  (4.2, 0, 0.0, [],
#   [(assign, "$pin_faction", "fac_vaegirs"),
#    (assign, "$pin_party_template", "pt_vaegir_messenger"),
#    (assign, "$pin_limit", peak_kingdom_caravans),
#    (call_script,"script_cf_spawn_party_at_faction_town_if_below_limit"),
#    (party_set_ai_behavior,"$pout_party",ai_bhvr_travel_to_party),
#    (party_set_ai_object,"$pout_party","$pout_town"),
#    ]),

#SB : messengers are deleted upon reaching destination, this should never apply
  

messenger_party_ai_triggers = [
(1.5, 0, 0, [
  # (store_random_party_of_template, reg(2), "pt_messenger_party"),
               # (party_is_in_any_town,reg(2)),
               ],
   [
   
    # (store_faction_of_party, ":faction_no", reg(2)),
    # (call_script,"script_cf_select_random_walled_center_with_faction", ":faction_no", -1),
    # (party_set_ai_behavior,reg(2),ai_bhvr_travel_to_party),
    # (party_set_ai_object,reg(2),reg0),
    # (party_set_flags, reg(2), pf_default_behavior, 0),
    
    ]),
]
