import collections

import module_skills

from header_common import *
from header_presentations import *
from header_mission_templates import *
from ID_meshes import *
from header_operations import *
from header_triggers import *
from header_items import *
from module_constants import *
import string

from custom_troops_header_presentations import *

####################################################################################################################
#	Each presentation record contains the following fields:
#	1) Presentation id: used for referencing presentations in other files. The prefix prsnt_ is automatically added before each presentation id.
#	2) Presentation flags. See header_presentations.py for a list of available flags
#	3) Presentation background mesh: See module_meshes.py for a list of available background meshes
#	4) Triggers: Simple triggers that are associated with the presentation
####################################################################################################################

ACTIVE_FIGHTING_SKILLS = [skill for skill in module_skills.skills if skill[2] & sf_inactive == 0 and skill[2] & 0xf in (ca_strength, ca_agility)]
#print "\n".join([skill[1] for skill in ACTIVE_FIGHTING_SKILLS])

CSTM_INV_SLOT_SIZE = 80
CSTM_INV_CONT_WIDTH = 3
CSTM_INV_CONT_HEIGHT = 4

CSTM_INV_POS_X = 40
CSTM_INV_POS_Y = 50

CSTM_NAME_POS_X = CSTM_INV_POS_X
CSTM_NAME_POS_Y = 685
CSTM_NAME_LABEL_WIDTH = 125
CSTM_NAME_GAP = 340

CSTM_STORE_SLOT_SIZE = 80
CSTM_STORE_CONT_WIDTH = 3
CSTM_STORE_CONT_HEIGHT = 7

CSTM_STORE_POS_X = CSTM_INV_POS_X + CSTM_INV_SLOT_SIZE * CSTM_INV_CONT_WIDTH + 45
CSTM_STORE_POS_Y = CSTM_INV_POS_Y

CSTM_STATS_POS_X = CSTM_STORE_POS_X + CSTM_STORE_SLOT_SIZE * CSTM_STORE_CONT_WIDTH + 35
CSTM_STATS_POS_Y = 0

CSTM_STATS_SIZE_X = 960 - CSTM_STATS_POS_X
CSTM_STATS_SIZE_Y = CSTM_STORE_CONT_HEIGHT * CSTM_STORE_SLOT_SIZE + CSTM_STORE_POS_Y - CSTM_STATS_POS_Y - 15

CSTM_STATS_ATTR_TEXT_SIZE = 1000
CSTM_STATS_ATTR_ROW_HEIGHT = 27
CSTM_STATS_ATTR_COL_WIDTH = 185
CSTM_STATS_ATTR_CONT_WIDTH = 2
CSTM_STATS_ATTR_SECTION_HEIGHT = int((((attributes_end - 1) / CSTM_STATS_ATTR_CONT_WIDTH)) + 1) * CSTM_STATS_ATTR_ROW_HEIGHT

CSTM_STATS_PROF_TEXT_SIZE = 950
CSTM_STATS_PROF_ROW_HEIGHT = 27
CSTM_STATS_PROF_COL_WIDTH = 185
CSTM_STATS_PROF_CONT_WIDTH = 2
CSTM_STATS_PROF_SECTION_HEIGHT = int((((proficiencies_end - 1) / CSTM_STATS_PROF_CONT_WIDTH)) + 1) * CSTM_STATS_PROF_ROW_HEIGHT

CSTM_STATS_SKL_TEXT_SIZE = 900
CSTM_STATS_SKL_ROW_HEIGHT = 27
CSTM_STATS_SKL_COL_WIDTH = 185
CSTM_STATS_SKL_CONT_WIDTH = 2
CSTM_STATS_SKL_SECTION_HEIGHT = int((((len(ACTIVE_FIGHTING_SKILLS) - 1) / CSTM_STATS_SKL_CONT_WIDTH)) + 1) * CSTM_STATS_SKL_ROW_HEIGHT

CSTM_STATS_POINTS_TEXT_SIZE = 900
CSTM_STATS_POINTS_ROW_HEIGHT = 25
CSTM_STATS_POINTS_COL_WIDTH = 185
CSTM_STATS_POINTS_SECTION_HEIGHT = 2 * CSTM_STATS_POINTS_ROW_HEIGHT

CSTM_STATS_GAP_Y = 40

CSTM_BUTTONS_POS_X = 800
CSTM_BUTTONS_POS_Y = CSTM_NAME_POS_Y
CSTM_BUTTONS_SIZE_X = 100
CSTM_BUTTONS_SIZE_Y = 30
CSTM_BUTTONS_GAP = 20

CSTM_TREE_TITLE_SIZE = 2000
CSTM_TREE_TITLE_POS_X = 50
CSTM_TREE_TITLE_POS_Y = 650

CSTM_TREE_POS_X = 100
CSTM_TREE_POS_Y = 75
CSTM_TREE_X_RIGHT_PADDING = 150

CSTM_TREE_X_OFFSET = 170
CSTM_TREE_Y_OFFSET = 145

CSTM_PREFIX_LABEL_POS_X = CSTM_TREE_TITLE_POS_X
CSTM_PREFIX_LABEL_WIDTH = 75
CSTM_PREFIX_POS_Y = 590

new_presentations = [

	("cstm_start_name_kingdom", 0, mesh_load_window, [
		(ti_on_presentation_load,
		[
			(set_fixed_point_multiplier, 1000),
			(call_script, "script_gpu_create_text_overlay", "str_name_kingdom_text", 500, 450, 1000, 500, 50, tf_center_justify),
			
			(str_store_troop_name, s0, "trp_player"),
			(str_store_string, s7, "str_default_kingdom_name"),
			(call_script, "script_gpu_create_text_box_overlay", "str_default_kingdom_name", 400, 400),
			(assign, "$g_presentation_obj_name_kingdom_1", reg1),
			
			(str_store_string, s0, "@Continue..."),
			(call_script, "script_gpu_create_game_button_overlay", "str_s0", 500, 300),
			(assign, "$g_presentation_obj_name_kingdom_2", reg1),
			
			(presentation_set_duration, 999999),
		]),
		
		(ti_on_presentation_event_state_change,
		[
			(store_trigger_param_1, ":object"),
			(try_begin),
				(eq, ":object", "$g_presentation_obj_name_kingdom_1"),
				
				(str_store_string, s7, s0),
			(else_try),
				(eq, ":object", "$g_presentation_obj_name_kingdom_2"),
				
				(faction_set_name, "fac_player_supporters_faction", s7),
				(faction_set_color, "fac_player_supporters_faction", 0xFF0000),
				(assign, "$players_kingdom_name_set", 1),
				
				(assign, "$cstm_open_troop_tree_view", 1),
				(presentation_set_duration, 0),
			(try_end),
		]),
	]),
	
]

def modmerge(var_set):
	try:
		var_name_1 = "presentations"
		orig_presentations = var_set[var_name_1]
	except KeyError:
		errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
		raise ValueError(errstring)
	
	orig_presentations.extend(new_presentations)
	
	#print var_name_1 + " done"
