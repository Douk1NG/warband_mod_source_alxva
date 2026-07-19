# -*- coding: cp1254 -*-
# package initializer for encounter menus

from game_menus.encounter.mnu_simple_encounter import simple_encounter_menu
from game_menus.encounter.mnu_encounter_retreat_confirm import encounter_retreat_confirm_menu
from game_menus.encounter.mnu_encounter_retreat import encounter_retreat_menu

encounter_menus = []
encounter_menus.extend(simple_encounter_menu)
encounter_menus.extend(encounter_retreat_confirm_menu)
encounter_menus.extend(encounter_retreat_menu)

