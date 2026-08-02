# -*- coding: cp1254 -*-
import collections

from header_game_menus import *
from header_operations import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from ID_menus import *
from module_constants import *

# Test entry point: adds a "Test troop tree picker" option to the camp menu that
# opens prsnt_cstm_choose_troop_tree. For M1 only - removes once the real flow is wired.

def modmerge(var_set):
	try:
		orig_game_menus = var_set["game_menus"]
	except KeyError:
		raise ValueError("Variable set does not contain expected variable: \"game_menus\".")

	for menu in orig_game_menus:
		if menu[0] == "camp":
			menu[5].append(
				("kct_test_tree_picker", [], "Test troop tree picker",
				 [
					(start_presentation, "prsnt_cstm_choose_troop_tree"),
				 ])
			)
			return
