# -*- coding: cp1254 -*-
# package initializer for battle menus

from game_menus.battle.mnu_enemy_slipped_away import enemy_slipped_away_menu
from game_menus.battle.mnu_order_attack_begin import order_attack_begin_menu
from game_menus.battle.mnu_total_defeat import total_defeat_menu
from game_menus.battle.mnu_order_attack_2 import order_attack_2_menu
from game_menus.battle.mnu_encounter_retreat import encounter_retreat_menu
from game_menus.battle.mnu_permanent_damage import permanent_damage_menu
from game_menus.battle.mnu_pre_join import pre_join_menu
from game_menus.battle.mnu_simple_encounter import simple_encounter_menu
from game_menus.battle.mnu_join_order_attack import join_order_attack_menu
from game_menus.battle.mnu_battle_debrief import battle_debrief_menu
from game_menus.battle.mnu_total_victory import total_victory_menu
from game_menus.battle.mnu_join_battle import join_battle_menu
from game_menus.battle.mnu_encounter_retreat_confirm import encounter_retreat_confirm_menu
from game_menus.battle.mnu_bandit_lair import bandit_lair_menu

battle_menus = []
battle_menus.extend(enemy_slipped_away_menu)
battle_menus.extend(order_attack_begin_menu)
battle_menus.extend(total_defeat_menu)
battle_menus.extend(order_attack_2_menu)
battle_menus.extend(encounter_retreat_menu)
battle_menus.extend(permanent_damage_menu)
battle_menus.extend(pre_join_menu)
battle_menus.extend(simple_encounter_menu)
battle_menus.extend(join_order_attack_menu)
battle_menus.extend(battle_debrief_menu)
battle_menus.extend(total_victory_menu)
battle_menus.extend(join_battle_menu)
battle_menus.extend(encounter_retreat_confirm_menu)
battle_menus.extend(bandit_lair_menu)

