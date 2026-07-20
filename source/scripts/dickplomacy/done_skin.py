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

done_skin_scripts = [
("done_skin",
	[
		(store_script_param, ":agent_no", 1),
		(try_begin),
			(agent_is_active, ":agent_no"),
			(agent_is_alive, ":agent_no"),
			(agent_is_human, ":agent_no"),
			(agent_get_troop_id, ":troop_no", ":agent_no"),
			(troop_get_type, ":is_female", ":troop_no"),
			(ge, ":is_female", 1),
			(agent_get_item_slot, ":body_armor", ":agent_no", ek_body),
			(try_begin),
				(neq, ":body_armor", -1),
				(agent_unequip_item, ":agent_no", ":body_armor"),	# (may have changed in inventory, and have the same base name -> changes only second time without unequipping)
			(try_end),
			(try_begin),
				(this_or_next|eq, ":body_armor", -1),
				(this_or_next|eq, ":body_armor", "itm_body_fem"), # <- remained back from character window equip
				(this_or_next|eq, ":body_armor", "itm_loin_top"),
				(eq, ":body_armor",  "itm_loin_skirt"),	# <- trp_looter_woman
				(try_begin), #Nincs -> cenzura -> "loincloth" felvesz
					(eq, "$g_cenzura", 1),
					(agent_equip_item, ":agent_no", "itm_loincloth"),
				(else_try), #Volt rajta?
					(this_or_next|eq, ":body_armor", -1),
					(eq, ":body_armor", "itm_body_fem"),
					(troop_get_inventory_slot, ":item_no", ":troop_no", ek_body),
					(try_begin),
					#Had the troop clothes training before mission?
						#mtf_override body -> equip loin parts corresponding to base armor components (bra?, bottom?)
						(gt, ":item_no", -1),
						(neq, ":item_no", "itm_body_fem"), # <- remained back from character window equip
						(try_begin), #save first customizable
						#Custom
							(item_slot_ge, ":item_no", slot_item_num_components, 1),
							(assign, ":cur_mesh_slot", slot_troop_armor_slots_begin), 	#0.: skin slot
							(try_begin),
							#Has Skin -> loincloth
								(troop_get_slot, ":skin", ":troop_no", ":cur_mesh_slot"),
								(neq, ":skin", 0),
								(agent_equip_item, ":agent_no", "itm_loincloth"),
							(else_try),
							#!Skin, Panty, Bra -> loincloth
								(val_add, ":cur_mesh_slot", 1),							#1.: chest slot
								(troop_get_slot, ":bra", ":troop_no", ":cur_mesh_slot"),
								(val_add, ":cur_mesh_slot", 1),							#2.: panty slot
								(troop_get_slot, ":panty", ":troop_no", ":cur_mesh_slot"),
							   #(eq, ":skin", 0),
								(neq, ":bra", 0),
								(neq, ":panty", 0),
								(agent_equip_item, ":agent_no", "itm_loincloth"),
							(else_try),
							#!Skin, Bra, !Panty -> loin_top
							   #(eq, ":skin", 0),
								(neq, ":bra", 0),
								(eq, ":panty", 0),
								(agent_equip_item, ":agent_no", "itm_loin_top"),
							(else_try),
							#!Skin, !Bra, Panty -> loin_skirt
							   #(eq, ":skin", 0),
								(eq, ":bra", 0),
								(neq, ":panty", 0),
								(agent_equip_item, ":agent_no", "itm_loin_skirt"),
							(else_try),
							#!Skin, !Bra, !Panty -> body for TATTOOS
							   #(eq, ":skin", 0),
							   #(eq, ":bra", 0),
							   #(eq, ":panty", 0),
								(agent_equip_item, ":agent_no", "itm_body_fem"),
							(try_end),
						(else_try),
						#Egyeb ruha	-> "loincloth" felvesz
							(agent_equip_item, ":agent_no", "itm_loincloth"),
						(try_end),
					(else_try),
					#Was nude before mission -> body for TATTOOS
						(agent_equip_item, ":agent_no", "itm_body_fem"),
					(try_end),
				(try_end),
			(else_try),	#Equip back original item
				(agent_equip_item, ":agent_no", ":body_armor"),
			(try_end),
		(try_end),
	]
  )
]
