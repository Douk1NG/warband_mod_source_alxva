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

cf_prisoner_offered_parole_scripts = [
("cf_prisoner_offered_parole",
	[
	  (store_script_param, ":prisoner", 1),

	  (eq, 1, 0), #disabled, this will always return false

	  (troop_get_slot, ":captor_party", ":prisoner", slot_troop_prisoner_of_party),
	  (party_is_active, ":captor_party"),
	  (is_between, ":captor_party", walled_centers_begin, walled_centers_end),
	  (party_get_slot, ":captor", ":captor_party", slot_town_lord),

	  (troop_get_slot, ":prisoner_rep", ":prisoner", slot_lord_reputation_type),
	  (troop_get_slot, ":captor_rep", ":captor", slot_lord_reputation_type),

	  (neq, ":prisoner_rep", lrep_debauched),
	  (neq, ":captor_rep", lrep_debauched),
	  (neq, ":captor_rep", lrep_quarrelsome),

     #Prisoner is a noble, or lord is goodnatured
    (this_or_next|eq, ":captor_rep", lrep_goodnatured),
    (this_or_next|troop_slot_eq, ":prisoner", slot_troop_occupation, slto_kingdom_hero),
    (troop_slot_eq, ":prisoner", slot_troop_occupation, slto_kingdom_lady),

	(call_script, "script_troop_get_relation_with_troop", ":captor", ":prisoner"),
##	(display_message, "str_relation_of_prisoner_with_captor_is_reg0"),
	(ge, reg0, -10),
	])
]
