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

init_custom_armor3_scripts = [
("init_custom_armor3",
    [
    (store_script_param, ":agent_no", 1),
    #(store_script_param, ":troop_no", 2),
    (store_script_param, ":sub_part", 3),
    (store_script_param, ":sub_comp", 4),
	(str_clear, s1),
  #SAVE AGENT ARMOR SLOT FOR SCENE
	(try_begin),
		(neq, ":agent_no", -1),
		(store_add, ":agent_armor_slot", slot_agent_armor_slots_begin, ":sub_part"),
		(agent_set_slot, ":agent_no", ":agent_armor_slot", ":sub_comp"),
	(try_end),
  #MAKE COMPONENT MESH STRING OUTPUT
    (assign, ":value", -1),
    (assign, "$g_custom_armor_param_count", 12),
	(try_begin), #SKIN none, assassin*, chainmail, leather
      (eq, ":sub_part", 0),
      (is_between, ":sub_comp", 0, 4), #3 + none
      (store_add, ":value", ":sub_comp", "itm_ca3_skin_0"),
    (else_try), #CHEST none, plate, scale, angela, -loin, -sonja, -risty
      (eq, ":sub_part", 1),
      (is_between, ":sub_comp", 0, 7), #6 + none
      (store_add, ":value", ":sub_comp", "itm_ca3_bra_0"),
	(else_try), #PANTY none, morag*, chain, risty, angela
      (eq, ":sub_part", 2),
      (is_between, ":sub_comp", 0, 5), #4 + none
      (store_add, ":value", ":sub_comp", "itm_ca3_panty_0"),
	(else_try), #BELT none, assassin*, ?angela, sonja, -risty
      (eq, ":sub_part", 3),
      (is_between, ":sub_comp", 0, 5), #4 + none
      (store_add, ":value", ":sub_comp", "itm_ca3_belt_0"),
    (else_try), #BUTT none, assassin*, ?angela, scale, sonja, -loin
      (eq, ":sub_part", 4),
      (is_between, ":sub_comp", 0, 5), #4 + none
      (store_add, ":value", ":sub_comp", "itm_ca3_ass_0"),
    (else_try), #KNEE none, plate, plated_assassin, angela, -assassin, -sonja, -scale
      (eq, ":sub_part", 5),
      (is_between, ":sub_comp", 0, 7), #6 + none
      (store_add, ":value", ":sub_comp", "itm_ca3_knee_0"),
    (else_try), #PAULDRON LEFT none, plate, scale, assa_shoul, ang_pauld, ang_shold, -assa_pauld, -sonja, -risty,
      (eq, ":sub_part", 6),
      (is_between, ":sub_comp", 0, 9), #8 + none
      (store_add, ":value", ":sub_comp", "itm_ca3_pdn_l_0"),
    (else_try), #PAULDRON RIGHT none, plate, scale, assa_shoul, ang_pauld, ang_shold, -assa_pauld, -sonja, -risty,
      (eq, ":sub_part", 7),
      (is_between, ":sub_comp", 0, 9), #8 + none
      (store_add, ":value", ":sub_comp", "itm_ca3_pdn_r_0"),
    (else_try), #ELBOW LEFT none, plate, angela, -assassin_sleeves
      (eq, ":sub_part", 8),
      (is_between, ":sub_comp", 0, 4), #3 + none
      (store_add, ":value", ":sub_comp", "itm_ca3_elb_l_0"),
    (else_try), #ELBOW RIGHT none, plate, angela, -assassin_sleeves
      (eq, ":sub_part", 9),
      (is_between, ":sub_comp", 0, 4), #3 + none
      (store_add, ":value", ":sub_comp", "itm_ca3_elb_r_0"),
    (else_try), #BRACER LEFT none, plate, sonja, angela, Risty
      (eq, ":sub_part", 10),
      (is_between, ":sub_comp", 0, 5), #4 + none
      (store_add, ":value", ":sub_comp", "itm_ca3_brc_l_0"),
    (else_try), #BRACER RIGHT none, plate, sonja, angela, Risty
      (eq, ":sub_part", 11),
      (is_between, ":sub_comp", 0, 5), #4 + none
      (store_add, ":value", ":sub_comp", "itm_ca3_brc_r_0"),
    (else_try), #NECK none, -sonja
      (eq, ":sub_part", 12),
      (is_between, ":sub_comp", 0, 2), #1 + none
      (store_add, ":value", ":sub_comp", "itm_ca3_neck_0"),
    (else_try), #CAPE none, -angela
      (eq, ":sub_part", 13),
      (is_between, ":sub_comp", 0, 2), #1 + none
      (store_add, ":value", ":sub_comp", "itm_ca3_cape_0"),
	(else_try), #END
      (assign, "$g_custom_armor_param_count", 0),
    (try_end),
    (try_begin),
      (neq, ":value", -1),
      (str_store_item_name, s1, ":value"), 	#<- item name (string)
    (try_end),
	(assign, reg0, ":value"), 				#<- item_no
    ]
  )
]
