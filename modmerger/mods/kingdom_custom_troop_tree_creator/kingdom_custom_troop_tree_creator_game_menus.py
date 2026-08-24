# -*- coding: cp1254 -*-
import collections

from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_operations import *
from module_constants import *

from util_wrappers import GameMenuWrapper

# KCT guard integration - game-menu side (guard_kct_integration_tasks.md T8).
#
# T8: the "fucked by the enemy prison" menu (mnu_fucked_by_enemy_prison) falls
# back to trp_hired_blade when the capturer faction's prison-guard slot is
# unset, but it tests `(eq, ":troop_prison_guard", -1)`. faction_get_slot
# returns 0 (not -1) for an unassigned slot, so the fallback never fires and
# the menu would spawn troop 0. The check must be `== 0`.
def modmerge(var_set):
	try:
		var_name = "game_menus"
		orig_menus = var_set[var_name]
	except KeyError:
		raise ValueError("Variable set does not contain expected variable: \"%s\"." % var_name)

	menus = collections.OrderedDict()
	for menu_tuple in orig_menus:
		menus[menu_tuple[0]] = GameMenuWrapper(menu_tuple)

	# T8: fix the unset prison-guard sentinel test.
	prison_continue = menus["fucked_by_enemy_prison"].GetMenuOption("continue")
	if prison_continue is not None:
		consequences = prison_continue.GetConsequenceBlock().Unwrap()
		for i, op in enumerate(consequences):
			if op == (eq, ":troop_prison_guard", -1):
				consequences[i] = (eq, ":troop_prison_guard", 0)

	del orig_menus[:]
	for menu_id in menus:
		orig_menus.append(menus[menu_id].data)
