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

roll_for_charisma_scripts = [
#script_set_calves - This is for SANDALS!!!
# INPUT: 	1:agent_no, 2:troop_no,2, reg1(:troop_item_slots_begin), reg2(:agent_item_slots_begin)
# OUTPUT:	NONE
#("set_calves", [
#	(store_trigger_param_1, ":agent_no"), # -1 if not in scene
#	(store_trigger_param_2, ":troop_no"),
#	(try_begin),
#		(eq, ":agent_no", -1),	#not in scene (presentation)
#		(is_between, ":troop_no", "trp_town_1_armorer", "trp_merchants_end"),	#trade - item from merchant inventory gives merchant no despite player equips it
#		(assign, ":troop_no", "trp_player"),
#	(try_end),
#	(try_begin),
#		(troop_get_type, ":troop_type", ":troop_no"),
#		(try_begin),
#			(this_or_next|eq, ":troop_type", tf_female), #female || tf_woman_nude || calfwoman (don't change male!)
#			(this_or_next|eq, ":troop_type", tf_woman_nude),
#			(eq, ":troop_type", tf_calfwoman),
#			(try_begin),
#				(this_or_next|troop_has_item_equipped , ":troop_no", "itm_risty_sandals"), #tf_calfwoman and has sandals on -> no change
#				(this_or_next|troop_has_item_equipped , ":troop_no", "itm_sonja_boots"),
#				(this_or_next|troop_has_item_equipped , ":troop_no", "itm_sonja_armor"),
#				(this_or_next|troop_has_item_equipped , ":troop_no", "itm_diabassa_armor"),
#				(this_or_next|troop_has_item_equipped , ":troop_no", "itm_plate_armor_dthun"),
#				(this_or_next|troop_has_item_equipped , ":troop_no", "itm_custom_armor3"),
#				(this_or_next|troop_has_item_equipped , ":troop_no", "itm_custom_armor2"),
#				(this_or_next|troop_has_item_equipped , ":troop_no", "itm_custom_armor1"),
#				(this_or_next|troop_has_item_equipped , ":troop_no", "itm_risty_armor"),
#				(this_or_next|troop_has_item_equipped , ":troop_no", "itm_scale_armor_dthun"),
#				(this_or_next|troop_has_item_equipped , ":troop_no", "itm_loincloth"),
#				(this_or_next|troop_has_item_equipped , ":troop_no", "itm_loin_top"),
#				(this_or_next|troop_has_item_equipped , ":troop_no", "itm_loin_skirt"),
#				(troop_has_item_equipped , ":troop_no", "itm_body_fem"),
#				(try_begin),
#					(this_or_next|eq, ":troop_type", tf_female),(eq, ":troop_type", tf_woman_nude),
#					(troop_set_type, ":troop_no", tf_calfwoman),
#					(assign, ":troop_changed", 1),
#				(try_end),
#			(else_try),
#				(eq, ":troop_type", tf_calfwoman),
#				(troop_set_type, ":troop_no", tf_female),
#				(assign, ":troop_changed", 1),
#			(try_end),
#			(ge, ":agent_no", 0), # in scene - warnings from map else
#			(eq, ":troop_changed", 1),
#			(troop_get_inventory_slot, ":item_no", ":troop_no", ek_body),
#			(ge, ":item_no", 0), # has body armor -> must refresh to see the change in scene
#			(agent_unequip_item, ":agent_no", ":item_no"),
#			(agent_equip_item, ":agent_no", ":item_no"),
#		(try_end),
#	(try_end),
#	]
# ),
# script_roll_for_charisma
# ex:
# (call_script, "script_roll_for_charisma", Difficulty_Modifier, Target_Troop, Propositioning_Troop),
# Outputs none
("roll_for_charisma", [
  (store_trigger_param_1, ":difmod"),
  (store_trigger_param_2, ":target"), # Should default to 0, which is the player troop
  (store_trigger_param_3, ":roller"),

  (assign, ":end", 0),

    (store_attribute_level, ":cha", ":roller", ca_charisma),
    (assign, ":required_cha", 12),
	(val_add, ":required_cha", ":difmod"),
    (troop_get_slot, ":renown", ":roller", slot_troop_renown),
    (val_div, ":renown", 100),

    (store_skill_level, ":persuasion", "skl_persuasion", ":roller"),

    (call_script, "script_dplmc_store_is_female_troop_1_troop_2", ":target", ":roller"),
    (assign, ":target_gender", reg0),
	(assign, ":roller_gender", reg1),

    (try_begin),
		# Same-gender is a lot harder.
		(eq, ":target_gender", ":roller_gender"),
        (val_add, ":required_cha", 8),
    (else_try),
		# Women are harder.
		(eq, ":target_gender", 1),
        (val_add, ":required_cha", 6),
	(else_try),
		# Men are easier.
        (eq, ":target_gender", 0),
        (val_sub, ":required_cha", 6),
    (try_end),

    (try_begin),
        (is_between, ":target", heroes_begin, heroes_end),

        (val_div, ":renown", 2),

        (try_begin), # Noble ladies are even harder.
            (is_between, ":target", kingdom_ladies_begin, kingdom_ladies_end),
            (val_add, ":required_cha", 10),
            (try_begin),
                (this_or_next|troop_slot_eq, ":target", slot_lord_reputation_type, lrep_moralist),
                (troop_slot_eq, ":target", slot_lord_reputation_type, lrep_conventional),
                (val_add, ":required_cha", 10),
            (else_try),
                (troop_slot_eq, ":target", slot_lord_reputation_type, lrep_adventurous),
                (val_sub, ":required_cha", 5),
            (else_try),
                (troop_slot_eq, ":target", slot_lord_reputation_type, lrep_ambitious),
                (val_add, ":required_cha", 5),
                (val_sub, ":required_cha", ":renown"),
            (try_end),
        (try_end),
    (try_end),

	(try_begin), # Pretenders are MUCH harder. O . O . F .
		(eq, ":target", "$supported_pretender"),
		(troop_get_slot, ":troop_renown", ":target", slot_troop_renown),
		(try_begin),
			(gt, ":troop_renown", ":renown"),
			(store_sub, ":renown_diff", ":troop_renown", ":renown"),
			(val_div, ":renown_diff", 50),
			(val_add, ":required_cha", ":renown_diff"),
		(try_end),
		(val_add, ":required_cha", 20),
	(try_end),

    (call_script, "script_troop_get_relation_with_troop", ":roller", ":target"),
    (assign, ":rel", reg0),
    (try_begin), # Negative relation is a no-go
        (lt, ":rel", 0),
        (assign, ":end", 1),
    (try_end),
    (val_div, ":rel", 5), # Every 5 relation is equal to 1 Cha
    (val_sub, ":required_cha", ":rel"),
    (val_sub, ":persuasion"),
    (val_sub, ":required_cha", ":renown"),

    (val_max, ":required_cha", 9),

    (try_begin),
        (ge, "$cheat_mode", 1),
		(eq, ":roller", "trp_player"),
        (assign, reg0, ":required_cha"),
        (display_message, "@Required Charisma: {reg0}"),
    (try_end),

	(eq, ":end", 0),
    (ge, ":cha", ":required_cha"),
  ])
]
