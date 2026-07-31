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



##diplomacy end
#Zaitenko's Reinforcement Script

zaitenko_reinforcements_triggers = [
(36, 0, 0.0, [], [  ## Set the reinforcements interval to 36 Game hours. Change as you feel like.
                     (try_for_range, ":center", walled_centers_begin, walled_centers_end),
                         (store_faction_of_party, ":faction", ":center"),
                         (party_get_num_companions, ":garrison", ":center"),
                         (faction_get_slot, ":party_template_a", ":faction", slot_faction_reinforcements_a),
                         (faction_get_slot, ":party_template_b", ":faction", slot_faction_reinforcements_b),
                         (faction_get_slot, ":party_template_c", ":faction", slot_faction_reinforcements_c),
                         (assign, ":party_template", 0),
                         (try_begin),
                             (party_slot_eq, ":center", slot_party_type, spt_town),
                             (lt, ":garrison", 200),            ## Under this number of troops will towns get reinforcements
                             (assign, ":party_template", "pt_reinforcements"),
                         (else_try),
                             (party_slot_eq, ":center", slot_party_type, spt_castle),
                             (lt, ":garrison", 70),            ## Under this number of troops will castles get reinforcements
                             (assign, ":party_template", "pt_reinforcements"),
                         (try_end),
                         (try_begin),
                             (gt, ":party_template", 0),
                             (try_for_range, ":village_reinforcements", villages_begin, villages_end),
                                 (try_begin),
                                     (party_slot_eq, ":center", slot_party_type, spt_castle),  ## For Castles
                                     (party_slot_eq, ":village_reinforcements", slot_village_bound_center, ":center"),
                                     (party_slot_eq, ":village_reinforcements", slot_village_state, svs_normal), ## Not if the village is being raided or is looted
                                     (spawn_around_party, ":village_reinforcements", ":party_template"),
                                     (assign, ":result", reg0),
                                     (store_random_in_range, ":rand", 0, 100),
                                     (try_begin),
                                         (is_between, ":rand", 0, 45),  ## Get weakest template
                                         (party_add_template, ":result", ":party_template_a"),
                                     (else_try),
                                         (is_between, ":rand", 45, 85), ## Get stronger template
                                         (party_add_template, ":result", ":party_template_b"),
                                     (else_try),
                                         (ge, ":rand", 85), ## Get strongest template
                                         (party_add_template, ":result", ":party_template_c"),
                                     (try_end),
                                     (party_set_faction, ":result", ":faction"),
                                     (party_set_slot, ":result", slot_party_type, spt_reinforcement_party),
                                     (party_set_slot, ":result", slot_party_ai_object, ":center"),
                                     (str_store_party_name, s14, ":village_reinforcements"),
                                     (party_set_name, ":result", "@Reinforcements from {s14}"),
                                     (party_set_ai_behavior,":result",ai_bhvr_travel_to_party),
                                     (party_set_ai_object,":result", ":center"),
                                     (party_set_flags, ":result", pf_default_behavior, 1),
                                 (else_try),       
                                     (party_slot_eq, ":center", slot_party_type, spt_town), ## For Towns
                                     (party_slot_eq, ":village_reinforcements", slot_village_bound_center, ":center"),
                                     (party_slot_eq, ":village_reinforcements", slot_village_state, svs_normal), ## Not if the village is being raided or is looted
                                     (neg|party_slot_eq, ":center", slot_town_lord, "trp_player"), ## Not a player owned center
                                     (spawn_around_party, ":village_reinforcements", ":party_template"),
                                     (assign, ":result", reg0),
                                     (store_random_in_range, ":rand", 0, 100),
                                     (try_begin),
                                         (is_between, ":rand", 0, 45),  ## Get weakest template
                                         (party_add_template, ":result", ":party_template_a"),
                                     (else_try),
                                         (is_between, ":rand", 40, 85), ## Get stronger template
                                         (party_add_template, ":result", ":party_template_b"),
                                     (else_try),
                                         (ge, ":rand", 85), ## Get strongest template
                                         (party_add_template, ":result", ":party_template_c"),
                                     (try_end),
                                     (party_set_faction, ":result", ":faction"),
                                     (party_set_slot, ":result", slot_party_type, spt_reinforcement_party),
                                     (party_set_slot, ":result", slot_party_ai_object, ":center"),
                                     (str_store_party_name, s14, ":village_reinforcements"),
                                     (party_set_name, ":result", "@Reinforcements from {s14}"),
                                     (party_set_ai_behavior,":result",ai_bhvr_travel_to_party),
                                     (party_set_ai_object,":result", ":center"),
                                     (party_set_flags, ":result", pf_default_behavior, 1),
                                 (try_end),
                             (try_end),
                         (try_end),
                     (try_end)]),
]
