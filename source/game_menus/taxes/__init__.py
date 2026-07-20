# -*- coding: cp1254 -*-
# package initializer for taxes menus

from game_menus.taxes.mnu_collect_taxes_revolt_warning import collect_taxes_revolt_warning_menu
from game_menus.taxes.mnu_collect_taxes import collect_taxes_menu
from game_menus.taxes.mnu_collect_taxes_complete import collect_taxes_complete_menu
from game_menus.taxes.mnu_collect_taxes_revolt import collect_taxes_revolt_menu
from game_menus.taxes.mnu_collect_taxes_failed import collect_taxes_failed_menu
from game_menus.taxes.mnu_collect_taxes_rebels_killed import collect_taxes_rebels_killed_menu

taxes_menus = []
taxes_menus.extend(collect_taxes_revolt_warning_menu)
taxes_menus.extend(collect_taxes_menu)
taxes_menus.extend(collect_taxes_complete_menu)
taxes_menus.extend(collect_taxes_revolt_menu)
taxes_menus.extend(collect_taxes_failed_menu)
taxes_menus.extend(collect_taxes_rebels_killed_menu)

