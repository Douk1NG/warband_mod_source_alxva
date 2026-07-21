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

init_angela_helm_scripts = [
("init_angela_helm",
    [
    (store_script_param, ":agent_no", 1),
    #(store_script_param, ":troop_no", 2),
    (store_script_param, ":sub_part", 3),
    (store_script_param, ":sub_comp", 4),
	(str_clear, s1),
  #SAVE AGENT ARMOR SLOT FOR SCENE
	(try_begin),
		(neq, ":agent_no", -1),
		(store_add, ":agent_armor_slot", slot_agent_helm_slots_begin, ":sub_part"),
		(agent_set_slot, ":agent_no", ":agent_armor_slot", ":sub_comp"),
	(try_end),
  #MAKE COMPONENT MESH STRING OUTPUT
    (assign, ":value", -1),
    (assign, "$g_custom_armor_param_count", 5),
	(try_begin), #FACE: none, angela
      (eq, ":sub_part", 0),
      (is_between, ":sub_comp", 0, 2), #1 + none
      (store_add, ":value", ":sub_comp", "itm_cah_face_0"),
	(else_try), #WING_UP: none, angela
      (eq, ":sub_part", 1),
      (is_between, ":sub_comp", 0, 2), #1 + none
      (store_add, ":value", ":sub_comp", "itm_cah_wings_up_0"),
	(else_try), #WING_DOWN: none, angela
      (eq, ":sub_part", 2),
      (is_between, ":sub_comp", 0, 2), #1 + none
      (store_add, ":value", ":sub_comp", "itm_cah_wings_down_0"),
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
