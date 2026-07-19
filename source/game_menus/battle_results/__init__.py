# -*- coding: cp1254 -*-
# package initializer for battle_results menus

from game_menus.battle_results.mnu_battle_debrief import battle_debrief_menu
from game_menus.battle_results.mnu_total_victory import total_victory_menu
from game_menus.battle_results.mnu_enemy_slipped_away import enemy_slipped_away_menu
from game_menus.battle_results.mnu_total_defeat import total_defeat_menu
from game_menus.battle_results.mnu_permanent_damage import permanent_damage_menu

battle_results_menus = []
battle_results_menus.extend(battle_debrief_menu)
battle_results_menus.extend(total_victory_menu)
battle_results_menus.extend(enemy_slipped_away_menu)
battle_results_menus.extend(total_defeat_menu)
battle_results_menus.extend(permanent_damage_menu)

