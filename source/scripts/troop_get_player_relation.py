# ======================================================================
# SHARED DEPENDENCY
# Entity: troop_get_player_relation (script)
# Called by menus in 6 domains: castle, diplomacy, reports, siege, town, village
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

troop_get_player_relation_scripts = [
("troop_get_player_relation",
      [
        (store_script_param_1, ":troop_no"),
        (troop_get_slot, ":reputation", ":troop_no", slot_lord_reputation_type),
        (troop_get_slot, ":effective_relation", ":troop_no", slot_troop_player_relation),
        (assign, ":honor_bonus", 0),
        (try_begin),
          (eq,  ":reputation", lrep_quarrelsome),
          (val_add, ":effective_relation", -3),
        (try_end),
        (try_begin),
          (ge, "$player_honor", 0),
          (try_begin),
            (this_or_next|eq,  ":reputation", lrep_upstanding),
            (             eq,  ":reputation", lrep_goodnatured),
             (store_div, ":honor_bonus", "$player_honor", 3),
		  ##diplomacy start+
		  (else_try),
			#In general this should not apply to ladies, as they operate by different
			#reputation rules, but if a "kingdom lady" has become a "kingdom hero" instead,
			#it should apply.
		     (eq,  ":reputation", lrep_moralist),#-- verify that the lady is effectively a lord:
		     (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
			 (store_div, ":honor_bonus", "$player_honor", 3),
		  (else_try),
			 #Personality type that values keeping your word
			 (call_script, "script_dplmc_get_troop_morality_value", ":troop_no", tmt_honest),
			 (ge, reg0, 1),
			 (store_div, ":honor_bonus", "$player_honor", 3),
		  ##diplomacy end+
          (try_end),
        (try_end),
        (try_begin),
          (lt, "$player_honor", 0),
          (try_begin),
            (this_or_next|eq,  ":reputation", lrep_upstanding),
            (             eq,  ":reputation", lrep_goodnatured),
            (store_div, ":honor_bonus", "$player_honor", 3),
          ##diplomacy start+
		  (else_try),
			(call_script, "script_dplmc_get_troop_morality_value", ":troop_no", tmt_honest),
			(ge, reg0, 1),#Personality type that values keeping your word
			(store_div, ":honor_bonus", "$player_honor", 3),
		  (else_try),
		  	 #"My kind of scum" - a few rare individuals might actively approve.
		  	 (lt, reg0, 0),#<-- must have negative value for tmt_honest; by default this is only Rolf.
		  	 (this_or_next|eq, ":reputation", lrep_roguish),
		  	 (this_or_next|eq, ":reputation", lrep_custodian),
		  	 (this_or_next|eq, ":reputation", lrep_debauched),
		  	 (this_or_next|eq, ":reputation", lrep_ambitious),
		  		(eq, ":reputation", lrep_cunning),
		  	 (store_div, ":honor_bonus", "$player_honor", -5),
		  	 (val_clamp, ":honor_bonus", 1, 6),
          (else_try),
			#"Honorable" lords can be awful people, so no bonus with benefactors,
			#but dishonorable lords are *guaranteed* to be awful.
            (eq, ":reputation", lrep_benefactor),
            (store_div, ":honor_bonus", "$player_honor", 5),
		  (else_try),
			#Self-righteous lords are moralizing but hypocritical.
			(eq, ":reputation", lrep_selfrighteous),
			(store_div, ":honor_bonus", "$player_honor", 5),
		  (else_try),
			 #In general this should not apply to ladies, as they operate by different
			 #reputation rules, but if a "kingdom lady" has become a "kingdom hero" instead,
			 #it should apply.
			 (eq,  ":reputation", lrep_moralist),#-- verify that the lady is effectively a lord:
		     (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
			 (store_div, ":honor_bonus", "$player_honor", 3),
		  (else_try),
			 (eq,  ":reputation", lrep_conventional),#-- verify that the lady is effectively a lord:
		     (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
			 (store_div, ":honor_bonus", "$player_honor", 5),
          ##diplomacy end+
          (else_try),
            (eq,  ":reputation", lrep_martial),
            (store_div, ":honor_bonus", "$player_honor", 5),
          (try_end),
        (try_end),
        (val_add, ":effective_relation", ":honor_bonus"),
        (val_clamp, ":effective_relation", -100, 101),
        (assign, reg0, ":effective_relation"),
    ])
]
